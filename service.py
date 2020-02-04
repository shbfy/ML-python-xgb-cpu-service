#!/usr/bin/python

import json
import time

import falcon
import numpy as np
import onnxruntime as rt
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler

PORT_NUMBER = 8080
start = time.time()

# instantiate the scaler
scaler = StandardScaler()

# get test data
X, y, labels = load_iris().data, load_iris().target, load_iris().target_names
X_count = X.shape[0]

# scale data
X_scaled = scaler.fit_transform(X)

end = time.time()
print("Loading time: {0:f} secs)".format(end - start))


# API Handler for Iris images
class Iris(object):
    """Handle classification requests for Iris dataset by ID"""

    def __init__(self):
        self.xgb = rt.InferenceSession("model.onnx")
        self.input_name = self.xgb.get_inputs()[0].name
        self.label_name = self.xgb.get_outputs()[0].name

    def on_get(self, req, resp, index):
        if index < X_count:
            y_pred = self.xgb.run([self.label_name], {self.input_name: X_scaled[index].reshape(1, -1).astype(
                np.float32)})[0]
            payload = {'index': index, 'predicted_label': list(labels)[y_pred[0]], 'predicted': int(y_pred[0])}
            resp.body = json.dumps(payload)
            resp.status = falcon.HTTP_200
        else:
            raise falcon.HTTPBadRequest(
                "Index Out of Range. ",
                "The requested index must be between 0 and {:d}, inclusive.".format(X_count - 1)
            )


# API Handler for example message
class Intro(object):
    """Example of invoking the endpoint for classifying a flower from the Iris dataset"""

    def on_get(self, req, resp):
        resp.body = '{"message": \
                    "This service verifies a model using the Iris Test data set. Invoke using the form /Iris/<index of ' \
                    'test sample>. For example, /iris/24"}'
        resp.status = falcon.HTTP_200
