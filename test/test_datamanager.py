#!/usr/bin/env python

from justintime.cruncher.datamanager import RawDataManager
import sys
import rich
import logging
import click
from rich import print
from pathlib import Path

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('file_path', type=click.Path(exists=True))

def cli(file_path: str) -> None:

    dp = Path(file_path)
    print(dp.parent)
    print(dp.name)


    rdm = RawDataManager(dp.parent, 'ProtoWIB', 'VDColdbox')
    data_files = sorted(rdm.list_files(), reverse=True)
    rich.print(data_files)
    # for f in data_files[:1]:w
    f = dp.name
    rich.print(f)
    trl = rdm.get_trigger_record_list(f)
    rich.print(trl)

    rich.print(f"Reading trigger record {trl[0]}")
    info, df = rdm.load_trigger_record(f, trl[0])
    rich.print(info)

    rich.print(df)

    #     df.reset_index(inplace=True)
    #     df.to_feather("trigger_record.feather")
    #     df.from_feather("trigger_record.feather")


if __name__ == "__main__":
    from rich.logging import RichHandler

    logging.basicConfig(
        level="DEBUG",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)]
    )

    # if len(sys.argv) != 2:
    #     rich.print(f"Usage: {sys.argv[0]} <dir>")
    # main(sys.argv[1])
    cli()