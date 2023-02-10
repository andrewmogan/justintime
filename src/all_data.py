from itertools import groupby
import datetime
from cruncher import signal
import rich
import numpy as np
from dash import Dash, html
class all_data_storage:
	def __init__(self, engine):
		self.engine = engine
		self.raw_data_files = {}
		self.shown_plots = []

	def update_shown_plots(self, new_shown_plots):
		self.shown_plots = new_shown_plots

	def get_trigger_record_data(self, trigger_record, raw_data_file):
		if raw_data_file in self.raw_data_files:
			if trigger_record in self.raw_data_files[raw_data_file]:
				return(self.raw_data_files[raw_data_file][trigger_record])
			return(self.add_trigger_record_to_file(trigger_record, raw_data_file))
		return(self.add_file(trigger_record, raw_data_file))

	def add_trigger_record_to_file(self, trigger_record, raw_data_file):
		self.raw_data_files[raw_data_file][trigger_record] = trigger_record_data(self.engine, trigger_record, raw_data_file)
		return(self.raw_data_files[raw_data_file][trigger_record])

	def add_file(self, trigger_record, raw_data_file):
		self.raw_data_files[raw_data_file] = {}
		return(self.add_trigger_record_to_file(trigger_record, raw_data_file))

_cache=None
class trigger_record_data:
	
	def __init__(self, engine, trigger_record, raw_data_file):
		self.engine = engine
		self.info, self.df, self.tp_df, self.fwtp_df = engine.load_entry(raw_data_file, int(trigger_record))

		global _cache 
		if _cache is None:
			_cache = self.df.index.min()
		self.t0_min=_cache
		self.df.index=self.df.index-self.df.index.min()

		self.tr_ts_sec = self.info['trigger_timestamp']*20/1000000000 # Move to 63.5 MHz
		#rich.print(self.tr_ts_sec)
		#rich.print(self.info)
		self.dt = datetime.datetime.fromtimestamp(self.tr_ts_sec).strftime('%c')
		self.channels = list(self.df.columns)
		#rich.print(self.channels[0])
		self.group_planes = groupby(self.channels, lambda ch: engine.ch_map.get_plane_from_offline_channel(int(ch)))
		
		self.planes = {k: [x for x in d if x] for k,d in self.group_planes}
		self.self_planes = {k:sorted(set(v) & set(self.df.columns)) for k,v in self.planes.items()}
		self.df_U =  self.df[self.self_planes.get(0, {})]
		self.df_V =  self.df[self.self_planes.get(1, {})]
		self.df_Z =  self.df[self.self_planes.get(2, {})]
		self.df_U_mean, self.df_U_std = self.df_U.mean(), self.df_U.std()
		self.df_V_mean, self.df_V_std = self.df_V.mean(), self.df_V.std()
		self.df_Z_mean, self.df_Z_std = self.df_Z.mean(), self.df_Z.std()
		self.fft_phase = {}
		#rich.print(self.df_U)


	def find_plane(self, offch):
		m={0:'U', 1:'V', 2:'Z'}
		p = self.engine.ch_map.get_plane_from_offline_channel(offch)
		if p in m:
			return m[p]
		else:
			return 'D'

	def init_fft(self):
		try: self.df_fft
		except AttributeError: 
			self.df_fft = signal.calc_fft_2(self.df)

	def init_fft2(self):
		try: self.df_fft2
		except AttributeError: self.df_fft2 = signal.calc_fft_sum_by_plane(self.df, self.planes)
		try: self.df_U_plane
		except AttributeError: self.df_U_plane = self.df_fft2['U-plane']
		try: self.df_V_plane
		except AttributeError: self.df_V_plane = self.df_fft2['V-plane']
		try: self.df_Z_plane
		except AttributeError: self.df_Z_plane = self.df_fft2['Z-plane']

	def init_fft_phase(self, fmin, fmax):
		try: self.df_fft
		except AttributeError: self.df_fft = signal.calc_fft(self.df)
		try: self.fft_phase[f"{fmin}-{fmax}"]
		except KeyError:

			self.fft_phase[f"{fmin}-{fmax}"] = signal.calc_fft_phase(self.df_fft, fmin, fmax)
			print(self.fft_phase[f"{fmin}-{fmax}"])
			self.fft_phase[f"{fmin}-{fmax}"]['femb']  = self.fft_phase[f"{fmin}-{fmax}"].index.map(self.engine.femb_id_from_offch)
			self.fft_phase[f"{fmin}-{fmax}"]['plane'] = self.fft_phase[f"{fmin}-{fmax}"].index.map(self.find_plane)				
			
		

	def init_tp(self):
		#rich.print(self.tp_df)
		self.tp_df_tsoff = self.tp_df.copy()
		self.ts_min = self.tp_df_tsoff['start_time'].min()
		self.tp_df_tsoff['peak_time'] = (self.tp_df_tsoff['peak_time']-self.ts_min)
		self.tp_df_tsoff['start_time'] = (self.tp_df_tsoff['start_time']-self.ts_min)

		self.tp_df_U = self.tp_df_tsoff[self.tp_df_tsoff['offline_ch'].isin(self.planes.get(0, {}))]
		self.tp_df_V = self.tp_df_tsoff[self.tp_df_tsoff['offline_ch'].isin(self.planes.get(1, {}))]
		self.tp_df_Z = self.tp_df_tsoff[self.tp_df_tsoff['offline_ch'].isin(self.planes.get(2, {}))]
		self.tp_df_O = self.tp_df_tsoff[self.tp_df_tsoff['offline_ch'].isin(self.planes.get(9999, {}))]
		
		self.xmin_U = min(self.planes.get(0,{}),default=0)
		self.xmax_U = max(self.planes.get(0,{}),default=0)
		self.xmin_V = min(self.planes.get(1,{}),default=0)
		self.xmax_V = max(self.planes.get(1,{}),default=0)
		self.xmin_Z = min(self.planes.get(2,{}),default=0)
		self.xmax_Z = max(self.planes.get(2,{}),default=0)
		self.xmin_O = min(self.planes.get(9999,{}),default=0)
		self.xmax_O = max(self.planes.get(9999,{}),default=0)


	# def init_fft_phase_22(self):
	# 	try: self.df_fft
	# 	except AttributeError: self.df_fft = signal.calc_fft(self.df)
	# 	fmin = 21000
	# 	fmax = 24000
	# 	try: self.df_phase_22
	# 	except AttributeError: 
	# 		self.df_phase_22 = signal.calc_fft_phase(self.df_fft, fmin, fmax)
	# 		self.df_phase_22['femb']  = self.df_phase_22.index.map(self.engine.femb_id_from_offch)
	# 		self.df_phase_22['plane'] = self.df_phase_22.index.map(self.find_plane)

	# def init_fft_phase_210(self):
	# 	try: self.df_fft
	# 	except AttributeError: self.df_fft = signal.calc_fft(self.df)
	# 	fmin = 129000
	# 	fmax = 220000
	# 	try: self.df_phase_210
	# 	except AttributeError: 
	# 		self.df_phase_210 = signal.calc_fft_phase(self.df_fft, fmin, fmax)
	# 		self.df_phase_210['femb']  = self.df_phase_210.index.map(self.engine.femb_id_from_offch)
	# 		self.df_phase_210['plane'] = self.df_phase_210.index.map(self.find_plane)

	# def init_fft_phase_430(self):
	# 	try: self.df_fft
	# 	except AttributeError: self.df_fft = signal.calc_fft(self.df)
	# 	fmin=405000
	# 	fmax=435000
	# 	try: self.df_phase_430
	# 	except AttributeError: 
	# 		self.df_phase_430 = signal.calc_fft_phase(self.df_fft, fmin, fmax)
	# 		self.df_phase_430['femb']  = self.df_phase_430.index.map(self.engine.femb_id_from_offch)
	# 		self.df_phase_430['plane'] = self.df_phase_430.index.map(self.find_plane)

	def init_cnr(self):
		try: self.df_cnr
		except AttributeError: 
			self.df_cnr = self.df.copy()
			self.df_cnr = self.df_cnr-self.df_cnr.mean()
			for p, p_chans in self.planes.items():
				for f,f_chans in self.engine.femb_to_offch.items():
					chans = list(set(p_chans) & set(f_chans))
					self.df_cnr[chans] = self.df_cnr[chans].sub(self.df_cnr[chans].mean(axis=1), axis=0)
