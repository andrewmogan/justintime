#!/usr/bin/env python   

import logging
import rich

from .dashboard import init_app

app = init_app()

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