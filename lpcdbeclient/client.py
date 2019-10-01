#!/usr/bin/env python
# coding: utf-8

import logging
logger = logging.getLogger('root')

from timeit import default_timer as timer

from .data import Data
from .utils import EnterExitPrint

import os
import tables
import numpy as np
import glob, os
from sklearn.metrics import roc_auc_score, accuracy_score, roc_curve
from tqdm import tqdm, tqdm_notebook
import traceback


PredictionClient = None
def import_dependencies():
    global PredictionClient
    with EnterExitPrint('Importing azureml dependencies...', 'Done importing'):
        from azureml.accel._client import PredictionClient
        # from grpc._channel import _Rendezvous


class Client(object):
    """docstring for Client"""
    def __init__(
            self,
            module_name,
            address,
            port = 50051,
            use_ssl = False,
            ):
        super(Client, self).__init__()
        self.iot_hub_name = "fermi-iot"
        self.iot_device_id = "fermi-edge"

        self.module_name = module_name
        self.address = address
        self.port = port
        self.use_ssl = use_ssl

        import_dependencies()
        self.setup_client()


    def setup_client(self):
        # Initialize AzureML Accelerated Models client
        self.client = PredictionClient(
            address = self.address,
            port = self.port,
            use_ssl = self.use_ssl,
            service_name = self.module_name
            )
        logger.info(str(self.client))


    def inference_np_array(self, np_array):
        np_array = np.float32(np_array)
        start = timer()
        result = self.client.score_numpy_arrays(
            input_map = {
                'Placeholder:0' : np_array
                }
            )
        end = timer()
        execution_time = end - start  # in seconds
        return result, execution_time


    def inference_npy(self, npy_file):
        np_array = np.load(npy_file)
        return self.inference_np_array(np_array)


    def inference_data(self, data, max_count=None):
        truths = []
        predictions = []
        times = []
        chunk_iterator = data.get_chunk_iterator(max_count=max_count)
        for img_chunk, label_chunk, real_chunk_size in chunk_iterator:
            prediction, execution_time = self.inference_np_array(img_chunk)
            truths.append(label_chunk)
            predictions.append(prediction)
            times.append(execution_time)
        return truths, predictions, times





