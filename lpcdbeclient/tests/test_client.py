from unittest import TestCase

import os.path as osp
import lpcdbeclient

from azureml.accel._client import PredictionClient
import mock
import numpy as np

from time import sleep
def mock_score_numpy_arrays(*args, **kwargs):
    sleep(0.5)
    return 0.9

PredictionClient.score_numpy_arrays = mock.create_autospec(
    PredictionClient.score_numpy_arrays,
    side_effect = mock_score_numpy_arrays
    )

class TestClient(TestCase):

    def test_time_measurement(self):
        client = lpcdbeclient.Client(
            module_name = 'mock.test3-module-kl',
            address = 'mock.azurb.fnal.gov'
            )
        np_array = np.array([0.0])
        result, time = client.inference_np_array(np_array)
        self.assertAlmostEqual(time, 0.5, delta=0.05)



