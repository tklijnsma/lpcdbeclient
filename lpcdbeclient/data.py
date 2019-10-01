import os.path as osp
import glob
from tqdm import tqdm
import logging
logger = logging.getLogger('root')

from . import utils

class Data(object):
    """docstring for Data"""

    @classmethod
    def from_file(cls, file):
        instance = cls()
        instance.files = [file]
        instance.dir = osp.basename(file)
        return instance

    def __init__(self, dir=None):
        super(Data, self).__init__()
        self.dir = dir
        self.datasize = 224
        if not(dir is None):
            self.files = self.list_test_files()

    def list_test_files(self):
        files = glob.glob(osp.join(self.dir, 'test_*'))
        return [ osp.abspath(f) for f in files ]

    def get_chunk_iterator(self, shuffle=False, max_count=None):
        chunk_size = 1
        total = self.get_n_events()
        if max_count: total = min(total, max_count)
        chunk_iterator = tqdm(
            utils.chunks(
                self.files,
                chunk_size,
                max_q_size=1,
                shuffle=shuffle,
                max_count=max_count
                ),
            total = total,
            desc='events'
            )
        return chunk_iterator

    def get_n_events(self):
        return utils.count_events(self.files)
