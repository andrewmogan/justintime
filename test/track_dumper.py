#!/usr/bin/env python

import rich
import logging
from justintime.cruncher.datamanager import RawDataManager



def main():
    # Signal: run: 12088  trg:1798
    # /data0/np02_bde_coldbox_run012081_0000_20211110T094009.hdf5.copied
    # Subtraction: run: 12081, trg: 1
    #  /data0/np02_bde_coldbox_run012088_0011_20211110T160927.hdf5.copied

    trg_sig = 1798
    raw_path_sig = '/data0/np02_bde_coldbox_run012088_0011_20211110T160927.hdf5.copied'
    trg_ref = 1
    raw_path_ref = '/data0/np02_bde_coldbox_run012081_0000_20211110T094009.hdf5.copied'

    rdm = RawDataManager('/data0')

    info_sig, df_sig = rdm.load_trigger_record(raw_path_sig, trg_sig)
    info_ref, df_ref = rdm.load_trigger_record(raw_path_ref, trg_ref)


    df_sig.to_hdf('run12088_trg1798.h5', key='df')
    df_ref.to_hdf('run12081_trg0001.h5', key='df')

    rich.print(info_sig)
    rich.print(info_ref)


if __name__ == '__main__':
    from rich.logging import RichHandler

    logging.basicConfig(
        level="DEBUG",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)]
    )

    main()