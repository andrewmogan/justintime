#!/usr/bin/env python
# DUNE DAQ includes
import daqdataformats
import detdataformats.wib
import detchannelmaps
import hdf5libs
import logging
import collections

import re
import rich
import numpy as np
import pandas as pd

trig_rec_hdr_regex = re.compile(r"\/\/TriggerRecord(\d{5})\/TriggerRecordHeader")
ch_map = detchannelmaps.make_map('VDColdboxChannelMap')



def get_trigger_record_list(file_path: str) -> list:
    dd = hdf5libs.DAQDecoder(file_path, 10000) # number of events = 10000 is not used
    datasets = dd.get_datasets()
    return [int(m.group(1)) for m in (trig_rec_hdr_regex.match(d) for d in datasets) if m]

def read_trigger_record(file_path, tr_num):
    dd = hdf5libs.DAQDecoder(file_path, 10000) # number of events = 10000 is not used
    datasets = dd.get_datasets()

    # TODO: replace with regex?
    frag_datasets = [ d for d in datasets if d.startswith(f'//TriggerRecord{tr_num:05}') and 'TriggerRecordHeader' not in d]
    trghdr_datasets = [ d for d in datasets if d.startswith(f'//TriggerRecord{tr_num:05}') and 'TriggerRecordHeader' in d]

    if len(trghdr_datasets) != 1:
        logging.warning(f"Multiple trigger record headers found {trghdr_datasets}")

    trghdr = dd.get_trh_ptr(trghdr_datasets[0])

    tr_info = {
        'run_number': trghdr.get_run_number(),
        'trigger_number': trghdr.get_trigger_number(),
        'trigger_timestamp': trghdr.get_trigger_timestamp(),
    }

    dfs = []
    for d in frag_datasets:
        frag = dd.get_frag_ptr(d)
        frag_hdr = frag.get_header()

        logging.debug(f"Inspecting {d}")
        logging.debug(f"Run number : {frag.get_run_number()}")
        logging.debug(f"Trigger number : {frag.get_trigger_number()}")
        logging.debug(f"Trigger TS    : {frag.get_trigger_timestamp()}")
        logging.debug(f"Window begin  : {frag.get_window_begin()}")
        logging.debug(f"Window end    : {frag.get_window_end()}")
        logging.debug(f"Fragment type : {frag.get_fragment_type()}")
        logging.debug(f"Fragment code : {frag.get_fragment_type_code()}")
        logging.debug(f"Size          : {frag.get_size()}")

        n_frames = (frag.get_size()-frag_hdr.sizeof())//detdataformats.wib.WIBFrame.sizeof()
        if not n_frames:
            continue

        wf = detdataformats.wib.WIBFrame(frag.get_data())
        wh = wf.get_wib_header()

        logging.debug(f"crate: {wh.crate_no}, slot: {wh.slot_no}, fibre: {wh.fiber_no}")
        crate_no = wh.crate_no 
        slot_no = wh.slot_no
        fiber_no = wh.fiber_no

        ts = np.zeros(n_frames, dtype='uint64')
        adcs = np.zeros(n_frames, dtype=('uint16', 256))
        off_chans = [ch_map.get_offline_channel_from_crate_slot_fiber_chan(crate_no, slot_no, fiber_no, c) for c in range(256)]

        for i in range(n_frames):
        #     # progress.update(task2, advance=1)

            wf = detdataformats.wib.WIBFrame(frag.get_data(i*detdataformats.wib.WIBFrame.sizeof())) 
            ts[i] = wf.get_timestamp()
            for c in range(256):
                # wf.get_channel(c)
                adcs[i][c] = wf.get_channel(c)
        logging.debug(f"Unpacking {d} completed")
        df = pd.DataFrame(collections.OrderedDict([('ts', ts)]+[(off_chans[c], adcs[:,c]) for c in range(256)]))
        df = df.set_index('ts')

        dfs.append(df)
    tr_df = pd.concat(dfs, axis=1)
    tr_df = tr_df.reindex(sorted(tr_df.columns), axis=1)
    return tr_info, tr_df

if __name__ == '__main__':

    from rich.logging import RichHandler

    logging.basicConfig(
        level="DEBUG",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)]
    )

    file_path = '/data0/np02_bde_coldbox_run011913_0011_20211028T161244.hdf5.copied'
    rich.print(file_path)

    tr_list = get_trigger_record_list(file_path)
    rich.print(tr_list)
    
    tr_info, tr_df = read_trigger_record(file_path, tr_list[0])
    rich.print(tr_list)
    rich.print(tr_df)