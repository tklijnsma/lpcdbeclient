from unittest import TestCase

import os.path as osp
import lpcdbeclient


class TestData(TestCase):

    test_dir = '/uscms/home/klijnsma/nobackup/data/dbe/test'
    test_file = osp.abspath('/uscms/home/klijnsma/nobackup/data/dbe/test/test_file_0.h5')

    def test_list_test_files(self):
        data = lpcdbeclient.Data(self.test_dir)
        self.assertTrue(osp.samefile(
            data.files[0],
            osp.join(self.test_dir, 'test_file_0.h5')
            ))

    def test_from_file(self):
        data = lpcdbeclient.Data.from_file(self.test_file)
        self.assertTrue(osp.samefile(
            data.files[0], self.test_file
            ))
        self.assertIsInstance(data, lpcdbeclient.Data)


class TestUtils(TestCase):

    test_file = osp.abspath('/uscms/home/klijnsma/nobackup/data/dbe/test/test_file_0.h5')

    def test_count_events(self):
        n = lpcdbeclient.utils.count_events([self.test_file])
        self.assertEqual(n, 10000)

    def test_chunk_with_max_count(self):
        data = lpcdbeclient.Data.from_file(self.test_file)
        iterator = data.get_chunk_iterator(max_count=10)        
        self.assertEqual(len(list(iterator)), 10)

    # def test_chunk_without_max_count(self):
    #     data = lpcdbeclient.Data.from_file(self.test_file)
    #     iterator = data.get_chunk_iterator()
    #     self.assertEqual(len(list(iterator)), 10000)
