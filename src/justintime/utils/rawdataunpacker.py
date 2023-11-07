# import pathlib
import collections
import fddetdataformats
import trgdataformats
import daqdataformats
import detchannelmaps

import logging

import pandas as pd
import numpy as np

import rawdatautils.unpack.wib2 as wib_unpack
import rawdatautils.unpack.wibeth as wibeth_unpack

from rich import print


class FragmentUnpacker:

    def __init__(self):
        pass

    def match(self, frag_type, subsys):
        return None
    
    def unpack(self, frag):
        return {}


class WIBEthFragmentNumpyUnpacker(FragmentUnpacker):
    
    def __init__(self):
        super().__init__()
    
    def match(self, frag_type, subsys):
        return (frag_type == daqdataformats.FragmentType.kWIBEth) and (subsys == daqdataformats.SourceID.kDetectorReadout)
    
    def unpack(self, frag):
        frag_hdr = frag.get_header()

        if not frag.get_data_size():
            return None, None
        
        if True:
            wf = fddetdataformats.WIBEthFrame(frag.get_data())
            dh = wf.get_daqheader()
            wh = wf.get_wibheader()
            ts, det_id, crate_no, slot_no, stream_no = (dh.timestamp, dh.det_id, dh.crate_id, dh.slot_id, dh.stream_id)

            logging.info(f"ts: 0x{ts:016x} (15 lsb: 0x{ts&0x7fff:04x}) cd_ts_0: 0x{wh.colddata_timestamp_0:04x} cd_ts_1: 0x{wh.colddata_timestamp_1:04x} crate: {crate_no}, slot: {slot_no}, stream: {stream_no}")

        ts = wibeth_unpack.np_array_timestamp(frag)
        adcs = wibeth_unpack.np_array_adc(frag)

        return ts, adcs
    
    
class WIBEthFragmentPandasUnpacker(WIBEthFragmentNumpyUnpacker):

    def __init__(self, channel_map):
        super().__init__()
        # self.chan_map = detchannelmaps.make_map(f'{channel_map}ChannelMap') if not channel_map is None else None
        if isinstance(channel_map, str):
            self.chan_map = detchannelmaps.make_map(f'{channel_map}ChannelMap') if not channel_map is None else None
        else:
            self.chan_map = channel_map

    def unpack(self, frag):

        payload_size = frag.get_data_size()
        # print(f"fragment payload size {payload_size}")
        if not payload_size:
            return None
        
        wf = fddetdataformats.WIBEthFrame(frag.get_data())
        dh = wf.get_daqheader()
        wh = wf.get_wibheader()
        ts, det_id, crate_no, slot_no, stream_no = (dh.timestamp, dh.det_id, dh.crate_id, dh.slot_id, dh.stream_id)
        n_chan_per_stream = 64
        n_streams_per_link = 4

        logging.info(f"ts: 0x{ts:016x} (15 lsb: 0x{ts&0x7fff:04x}) cd_ts_0: 0x{wh.colddata_timestamp_0:04x} cd_ts_1: 0x{wh.colddata_timestamp_1:04x} crate: {crate_no}, slot: {slot_no}, stream: {stream_no}")

        # link_no = stream_no >> 6;
        # substream_no = stream_no & 0x3f;

        # first_chan = n_chan_per_stream*substream_no
        if self.chan_map:
            # off_chans = [self.chan_map.get_offline_channel_from_crate_slot_fiber_chan(crate_no, slot_no, link_no, c) for c in range(first_chan,first_chan+n_chan_per_stream)]
            off_chans = [self.chan_map.get_offline_channel_from_crate_slot_stream_chan(crate_no, slot_no, stream_no, c) for c in range(n_chan_per_stream)]
        else:
            first_chan += link_no*n_chan_per_stream*n_streams_per_link
            off_chans = [c for c in range(first_chan,first_chan+n_chan_per_stream)]

        ts, adcs = super().unpack(frag)

        if ts is None or adcs is None:
            return None

        df = pd.DataFrame(collections.OrderedDict([('ts', ts)]+[(off_chans[c], adcs[:,c]) for c in range(64)]))
        df = df.set_index('ts')

        return df

# class WIBEthFragmentUnpacker(FragmentUnpacker):
    
#     def __init__(self, channel_map):
#         super().__init__()
#         self.chan_map = detchannelmaps.make_map(f'{channel_map}ChannelMap') if not channel_map is None else None
#         # self.dump = True
    
#     def match(self, frag_type, subsys):
#         return (frag_type == daqdataformats.FragmentType.kWIBEth) and (subsys == daqdataformats.SourceID.kDetectorReadout)
    
#     def unpack(self, frag):

#         payload_size = frag.get_data_size()
#         print(f"fragment payload size {payload_size}")
#         if not payload_size:
#             return None
        
#         wf = fddetdataformats.WIBEthFrame(frag.get_data())
#         dh = wf.get_daqheader()
#         wh = wf.get_wibheader()
#         ts, det_id, crate_no, slot_no, stream_no = (dh.timestamp, dh.det_id, dh.crate_id, dh.slot_id, dh.stream_id)
#         n_chan_per_stream = 64
#         n_streams_per_link = 4

#         logging.info(f"ts: 0x{ts:016x} (15 lsb: 0x{ts&0x7fff:04x}) cd_ts_0: 0x{wh.colddata_timestamp_0:04x} cd_ts_1: 0x{wh.colddata_timestamp_1:04x} crate: {crate_no}, slot: {slot_no}, stream: {stream_no}")

#         off_chans = [self.chan_map.get_offline_channel_from_crate_slot_stream_chan(crate_no, slot_no, stream_no, c) for c in range(n_chan_per_stream)]

#         ts = wibeth_unpack.np_array_timestamp(frag)
#         adcs = wibeth_unpack.np_array_adc(frag)

#         df = pd.DataFrame(collections.OrderedDict([('ts', ts)]+[(off_chans[c], adcs[:,c]) for c in range(n_chan_per_stream)]))
#         df = df.set_index('ts')

#         return df

class WIBFragmentUnpacker(FragmentUnpacker):
    """Legacy WIB2 fragment unpacker"""
    
    def __init__(self, channel_map):
        super().__init__()
        # self.chan_map = detchannelmaps.make_map(f'{channel_map}ChannelMap')
        if isinstance(channel_map, str):
            self.chan_map = detchannelmaps.make_map(f'{channel_map}ChannelMap') if not channel_map is None else None
        else:
            self.chan_map = channel_map

    def match(self, frag_type, subsys):
        return (frag_type == daqdataformats.FragmentType.kWIB) and (subsys == daqdataformats.SourceID.kDetectorReadout)
    
    def unpack(self, frag):
        frag_hdr = frag.get_header()

        payload_size = (frag.get_size()-frag_hdr.sizeof())
        if not payload_size:
            return None
        print(f"fragment payload size {payload_size}")
        
        wf = fddetdataformats.WIB2Frame(frag.get_data())
        wh = wf.get_header()
        det_id, crate_no, slot_no, link_no = (wh.detector_id, wh.crate, wh.slot, wh.link)

        logging.debug(f"crate: {crate_no}, slot: {slot_no}, fibre: {link_no}")
        n_chan_per_link = 256

        off_chans = [self.chan_map.get_offline_channel_from_crate_slot_fiber_chan(crate_no, slot_no, link_no, c) for c in range(n_chan_per_link)]

        ts = wib_unpack.np_array_timestamp(frag)
        adcs = wib_unpack.np_array_adc(frag)


        df = pd.DataFrame(collections.OrderedDict([('ts', ts)]+[(off_chans[c], adcs[:,c]) for c in range(n_chan_per_link)]))
        df = df.set_index('ts')

        return df


class TPFragmentPandasUnpacker(FragmentUnpacker):

    def __init__(self, channel_map):
        super().__init__()
        if isinstance(channel_map, str):
            self.chan_map = detchannelmaps.make_map(f'{channel_map}ChannelMap') if not channel_map is None else None
        else:
            self.chan_map = channel_map
    
    def match(self, frag_type, subsys):
        return (frag_type == daqdataformats.FragmentType.kTriggerPrimitive) and (subsys == daqdataformats.SourceID.kTrigger)
    
    @classmethod
    def dtypes(cls):
        return [
                ('time_start', np.uint64), 
                ('time_peak', np.uint64), 
                ('time_over_threshold', np.uint64), 
                ('channel',np.uint32),
                ('adc_integral', np.uint32), 
                ('adc_peak', np.uint16), 
                ('flag', np.uint16),
            ]
    
    @classmethod
    def empty(cls):
        return pd.DataFrame(np.empty(0, cls.dtypes()))

    def unpack(self, frag):

        tp_array = []
        tp_size = trgdataformats.TriggerPrimitive.sizeof()

        frag_hdr = frag.get_header()

        n_frames = (frag.get_size()-frag_hdr.sizeof())//tp_size
        logging.debug(f"Number of TP frames: {n_frames}")
        
        # Initialize the TP array buffer
        tp_array = np.zeros(
            n_frames, 
            dtype=self.dtypes()
        )

        
        # Populate the buffer
        for i in range(n_frames):
            tp = trgdataformats.TriggerPrimitive(frag.get_data(i*tp_size))
            tp_array[i] = (tp.time_start, tp.time_peak, tp.time_over_threshold, tp.channel, tp.adc_integral, tp.adc_peak, tp.flag)

        # Create the dataframe
        df = pd.DataFrame(tp_array)

        logging.debug(f"TP Dataframe size {len(df)}")
        # print(df)
        # Add plane information (here or in user code?)
        df['plane'] = df['channel'].apply(lambda x: self.chan_map.get_plane_from_offline_channel(x)).astype(np.uint8)
        return df


class DAPHNEStreamFragmentPandasUnpacker(FragmentUnpacker):
    
    def __init__(self):
        super().__init__()
    
    def match(self, frag_type, subsys):
        return (frag_type == daqdataformats.FragmentType.kDAPHNE) and (subsys == daqdataformats.SourceID.kDetectorReadout)
    
    def unpack(self, frag):
        frag_hdr = frag.get_header()

        payload_size = (frag.get_size()-frag_hdr.sizeof())
        if not payload_size:
            return None
        
        print(f"DAPHNE payload size {payload_size}")
        
        df = fddetdataformats.DAPHNEStreamFrame(frag.get_data())

        dh = df.get_daqheader()

        ts, det_id, crate_no, slot_no, stream_no = (dh.get_timestamp(), dh.det_id, dh.crate_id, dh.slot_id, dh.link_id)
        print(ts, det_id, crate_no, slot_no, stream_no)


        df = pd.DataFrame()
        return df



class UnpackerService:
    """Helper class to unpack Trigger Records"""
    
    def __init__(self):
        self.fragment_unpackers = {}


    def add_unpacker(self, name, unpacker):

        if name in self.fragment_unpackers:
            raise KeyError(f"UnpackerService {name} already registered")

        self.fragment_unpackers[name] = unpacker

    def get_unpacker(self, name):
        return self.fragment_unpackers[name]
        

    def unpack(self, raw_data_file, tr_id: int, seq_id: int=0) -> dict:

        res = {}

        trh = raw_data_file.get_trh((tr_id, seq_id))
        tr_source_ids = raw_data_file.get_source_ids((tr_id, seq_id))

        for sid in tr_source_ids:
            frag = raw_data_file.get_frag((tr_id, seq_id),sid)

            for n,up in self.fragment_unpackers.items():
                if not up.match(frag.get_fragment_type(), sid.subsystem):
                    # logging.debug(f"fragment {sid} (type {frag.get_fragment_type()}) and unpacker {n} - no match")
                    continue
                
                logging.debug(f"[{n}] Unpacking Subsys={sid.subsystem}, id={sid.id}")                
                r = up.unpack(frag)
                logging.debug(f"[{n}] Unpacking Subsys={sid.subsystem}, id={sid.id} completed ({len(r) if r is not None else 0})")
                res.setdefault(n,{})[sid.id] = r

        return res
