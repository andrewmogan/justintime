#!/usr/bin/env python

from cruncher.datamanager import RawDartaManager
import sys
import rich

def main(data_path: str) -> None:

    rdm = RawDartaManager(data_path)
    rich.print(rdm.list_files())

if __name__ == "__main__":

    if len(sys.argv) != 2:
        rich.print(f"Usage: {sys.argv[0]} <dir>")
    main(sys.argv[1])