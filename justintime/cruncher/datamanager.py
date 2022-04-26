# from . watcher import Watcher
import os.path
import fnmatch
from os import walk
import re

# DUNE DAQ includes
import daqdataformats
import detdataformats.wib
import detchannelmaps
import hdf5libs
import rawdatautils.unpack.wib as wib_unpack
import logging

import numpy as np
import pandas as pd
import collections
# import rich
from itertools import groupby

"""
RawDataManager is responsible of raw data information management: discovery, loading, and reference runs handling

"""


class RawDataManager:

    # match_exprs = ['*.hdf5','*.hdf5.copied']
    match_exprs = ['*.hdf5', '*.hdf5.copied']
    max_cache_size = 100

    def __init__(self, data_path: str, ch_map_id: str = 'VDColdboxChannelMap') -> None:

        if not os.path.isdir(data_path):
            raise ValueError(f"Directory {data_path} does not exist")

        self.data_path = data_path
        self.ch_map_name = 'VDColdboxChannelMap'
        self.ch_map = detchannelmaps.make_map(ch_map_id)
        self.offch_to_hw_map = self._init_o2h_map()
        self.femb_to_offch = {k: [int(x) for x in d] for k,d in groupby(self.offch_to_hw_map, self.femb_id_from_offch)}

        # self.trig_rec_hdr_regex = re.compile(r"\/\/TriggerRecord(\d{5})\/TriggerRecordHeader")
        self.cache = collections.OrderedDict()
    


    def _init_o2h_map(self):
        if self.ch_map_name == 'VDColdboxChannelMap':
            crate_no = 4
            slots = range(4)
            fibres = range(1,3)
            chans = range(256)
        else:
            return {}

        o2h_map = {}
        for slot_no in slots:
            for fiber_no in fibres:
                for ch_no in chans:
                    off_ch = self.ch_map.get_offline_channel_from_crate_slot_fiber_chan(crate_no, slot_no, fiber_no, ch_no)
                    if off_ch == 4294967295:
                        continue
                    o2h_map[off_ch] = (crate_no, slot_no, fiber_no, ch_no)

        return o2h_map

    def femb_id_from_offch(self, off_ch):
        # off_ch_str = str(off_ch)
        crate, slot, link, ch = self.offch_to_hw_map[off_ch]
        return (4*slot+2*(link-1)+ch//128)+1 


    def list_files(self) -> list:
        files = []
        for m in self.match_exprs:
            files += fnmatch.filter(next(walk(self.data_path), (None, None, []))[2], m)  # [] if no file

        return sorted(files, reverse=True, key=lambda f: os.path.getmtime(os.path.join(self.data_path, f)))


    def get_trigger_record_list(self, file_name: str) -> list:
        file_path = os.path.join(self.data_path, file_name)
        rdf = hdf5libs.HDF5RawDataFile(file_path) # number of events = 10000 is not used
        return [ n for n,_ in rdf.get_all_trigger_record_ids()]
    

    def load_trigger_record(self, file_name: str, tr_num: int) -> list:

        uid = (file_name, tr_num)
        if uid in self.cache:
            logging.info(f"{file_name}:{tr_num} already loaded. returning cached dataframe")
            tr_info, tr_df = self.cache[uid]
            self.cache.move_to_end(uid, False)
            return tr_info, tr_df

        file_path = os.path.join(self.data_path, file_name)
        rdf = hdf5libs.HDF5RawDataFile(file_path) # number of events = 10000 is not used
        # datasets = dd.get_datasets()

        # TODO: replace with regex?
        # frag_datasets = [ d for d in datasets if d.startswith(f'//TriggerRecord{tr_num:05}') and 'TriggerRecordHeader' not in d]
        # trghdr_datasets = [ d for d in datasets if d.startswith(f'//TriggerRecord{tr_num:05}') and 'TriggerRecordHeader' in d]

        # if len(trghdr_datasets) != 1:
            # logging.warning(f"Multiple trigger record headers found {trghdr_datasets}")

        # trghdr = dd.get_trh_ptr(trghdr_datasets[0])

        tr_hdr = rdf.get_trh((tr_num,0))
        tr_geo_ids = rdf.get_geo_ids((tr_num, 0))


        tr_info = {
            'run_number': tr_hdr.get_run_number(),
            'trigger_number': tr_hdr.get_trigger_number(),
            'trigger_timestamp': tr_hdr.get_trigger_timestamp(),
        }

        tr_ts = tr_hdr.get_trigger_timestamp()

        dfs = []
        for geoid in tr_geo_ids:
            frag = rdf.get_frag((tr_num, 0),geoid)
            frag_hdr = frag.get_header()

            logging.debug(f"Inspecting {geoid.system_type} {geoid.region_id} {geoid.element_id}")
            logging.debug(f"Run number : {frag.get_run_number()}")
            logging.debug(f"Trigger number : {frag.get_trigger_number()}")
            logging.debug(f"Trigger TS    : {frag.get_trigger_timestamp()}")
            logging.debug(f"Window begin  : {frag.get_window_begin()}")
            logging.debug(f"Window end    : {frag.get_window_end()}")
            logging.debug(f"Fragment type : {frag.get_fragment_type()}")
            logging.debug(f"Fragment code : {frag.get_fragment_type_code()}")
            logging.debug(f"Size          : {frag.get_size()}")

            n_frames = (frag.get_size()-frag_hdr.sizeof())//detdataformats.wib.WIBFrame.sizeof()
            # rich.print(f"Number of WIB frames: {n_frames}")
            if not n_frames:
                continue

            wf = detdataformats.wib.WIBFrame(frag.get_data())
            wh = wf.get_wib_header()

            logging.debug(f"crate: {wh.crate_no}, slot: {wh.slot_no}, fibre: {wh.fiber_no}")
            crate_no = wh.crate_no 
            slot_no = wh.slot_no
            fiber_no = wh.fiber_no
            off_chans = [self.ch_map.get_offline_channel_from_crate_slot_fiber_chan(crate_no, slot_no, fiber_no, c) for c in range(256)]

            # ts = np.zeros(n_frames, dtype='int64')
            # adcs = np.zeros(n_frames, dtype=('uint16', 256))

            # for i in range(n_frames):
            #     # progress.update(task2, advance=1)

            #     wf = detdataformats.wib.WIBFrame(frag.get_data(i*detdataformats.wib.WIBFrame.sizeof())) 
            #     ts[i] = wf.get_timestamp()-tr_ts
            #     adcs[i] = [wf.get_channel(c) for c in range(256)]
            ts = wib_unpack.np_array_timestamp(frag)
            adcs = wib_unpack.np_array_adc(frag)
            ts = (ts - tr_ts).astype('int64')
            logging.debug(f"Unpacking {geoid.system_type} {geoid.region_id} {geoid.element_id} completed")

            df = pd.DataFrame(collections.OrderedDict([('ts', ts)]+[(off_chans[c], adcs[:,c]) for c in range(256)]))
            df = df.set_index('ts')

            dfs.append(df)

        tr_df = pd.concat(dfs, axis=1)
        # Sort columns (channels)
        tr_df = tr_df.reindex(sorted(tr_df.columns), axis=1)
        # Reverse timestamps (rows)
        tr_df = tr_df[::-1]
        self.cache[uid] = (tr_info, tr_df)
        if len(self.cache) > self.max_cache_size:
            old_uid, _ = self.cache.popitem(False)
            logging.info(f"Removing {old_uid[0]}:{old_uid[1]} from cache")

        return tr_info, tr_df