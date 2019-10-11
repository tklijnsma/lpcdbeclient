#!/usr/bin/env python
# coding: utf-8

print('Importing azureml...')
from azureml.core import Workspace
from azureml.contrib.core.compute import IotHubCompute
from azureml.core.compute import ComputeTarget
from azureml.contrib.core.webservice import IotWebservice, IotBaseModuleSettings, IotModuleSettings

from azureml.core import Image, Webservice
from azureml.contrib.core.webservice import IotWebservice
from azureml.accel import AccelContainerImage

from azureml.accel._client import PredictionClient
print('Done importing azureml')

import tables
import numpy as np
import glob, os
from sklearn.metrics import roc_auc_score, accuracy_score, roc_curve
from tqdm import tqdm, tqdm_notebook

DISABLE_ACTUAL_DEPLOYMENT = True
if DISABLE_ACTUAL_DEPLOYMENT:
    print('Disabling IotWebservice.deploy_from_image (demo)')
    def mocked_deploy_from_image(*args, **kwargs):
        print('IotWebservice.deploy_from_image called but is disabled for this demo')
        print('args: {0}'.format(args))
        print('kwargs: {0}'.format(kwargs))
    IotWebservice.deploy_from_image = mocked_deploy_from_image


class Service(object):
    """Deploys a new service to the DBE at Fermilab"""

    def __init__(self):
        super(Service, self).__init__()

        print('Setting up ws...')
        if not os.path.isfile('config.json'):
            raise RuntimeError(
                'No file config.json is found, which is needed to setup '
                'the workspace. Please first download the config.json from '
                'the Azure portal (https://portal.azure.com) and put it in '
                'this directory.'
                )
        self.ws = Workspace.from_config()
        self.iot_device_id = "fermi-edge"
        print(self.ws)

        self.module_name = "test-module-kl3"
        self.image_name = "im-klijnsma-tquarkrn50-v1-s0"
        self.port = 50051


    def get_service(self):
        self.iot_service = IotWebservice(self.ws, self.module_name)
        print(self.iot_service)


    def create_service(self):
        self.iothub_compute = IotHubCompute(self.ws, self.iot_device_id)

        compute_targets = ComputeTarget.list(self.ws)
        for t in compute_targets: 
            if t.type == "IotHub":
                print("IotHub '{}' has provisioning state '{}'.".format(t.name, t.provisioning_state))


        self.container_config = """{
  "ExposedPorts": {
    "50051/tcp": {}
  },
  "HostConfig": {
    "Binds": [
      "/etc/hosts:/etc/hosts"
    ],
    "Privileged": true,
    "Devices": [
      {
        "PathOnHost": "/dev/catapult0",
        "PathInContainer": "/dev/catapult0"
      },
      {
        "PathOnHost": "/dev/catapult1",
        "PathInContainer": "/dev/catapult1"
      }
    ],
    "PortBindings": {
      "50051/tcp": [
        {
          "HostPort": "50051"
        }
      ]
    }
  }
}"""

        self.routes = {
            "route": "FROM /messages/* INTO "
            }

        # Here, we define the Azure ML module with the container_config options above
        self.aml_module = IotBaseModuleSettings(
            name = self.module_name,
            create_option = self.container_config
            )

        # This time, we will leave off the external module from the deployment manifest
        self.deploy_config = IotWebservice.deploy_configuration(
            device_id = self.iot_device_id,
            routes = self.routes,
            aml_module = self.aml_module
            )

        # Deploy from latest version of image, using module_name as your IotWebservice name
        iot_service_name = self.module_name

        # Can specify version=x, otherwise will grab latest
        self.image = Image(self.ws, self.image_name) 
        self.iot_service = IotWebservice.deploy_from_image(
            self.ws,
            iot_service_name,
            self.image,
            self.deploy_config,
            self.iothub_compute
            )


#____________________________________________________________________
def main():
    service = Service()
    service.create_service()


#____________________________________________________________________
if __name__ == "__main__":
    main()


