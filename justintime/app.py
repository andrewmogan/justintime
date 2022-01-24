#!/usr/bin/env python   

import logging
import rich
import click

from .cruncher.datamanager import RawDataManager
from .dashboard import init_app

@click.command()
@click.argument('raw_data_path', type=click.Path(exists=True, file_okay=False))
@click.argument('channel_map_id', type=click.Choice(['VDColdboxChannelMap', 'ProtoDUNESP1ChannelMap']))
def cli(raw_data_path :str, channel_map_id:str):

    rdm = RawDataManager(raw_data_path, channel_map_id)
    data_files = rdm.list_files()
    rich.print(data_files)
    app = init_app(rdm)

    app.run_server(debug=True, host='0.0.0.0')

# Run the server
if __name__ == "__main__":
    from rich.logging import RichHandler

    logging.basicConfig(
        level="DEBUG",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)]
    )

    cli()
