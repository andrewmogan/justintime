#!/usr/bin/env python   

import logging
import rich

from .cruncher.datamanager import RawDataManager
from .dashboard import init_app


rdm = RawDataManager('/data0/')
data_files = rdm.list_files()
rich.print(data_files)
app = init_app(rdm)

# Run the server
if __name__ == "__main__":
    from rich.logging import RichHandler

    logging.basicConfig(
        level="DEBUG",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)]
    )

    app.run_server(debug=True, host='0.0.0.0')
