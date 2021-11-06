# from . watcher import Watcher
import os.path
import fnmatch
from os import walk
"""
RawDataManager is responsible of raw data information management: discovery, loading, and reference runs handling

"""
class RawDartaManager:
    
    match_expr = '*.hd5'
    
    def __init__(self, data_path: str) -> None:


        if not os.path.isdir(data_path):
            raise ValueError(f"Directory {data_path} does not exist" )


        self.data_path = data_path
    

    def list_files(self) -> list:
        return fnmatch.filter(next(walk(self.data_path), (None, None, []))[2], self.match_expr)  # [] if no file



