from unittest import TestCase

import torch
import torch.nn as nn

import serialization


class PyTorchSerializationTests(TestCase):
    def assert_tensors_equal(self, t1, t2):
        self.assertEqual(t1.shape, t2.shape)
        t1_flat = t1.flatten().tolist()
        t2_flat = t2.flatten().tolist()

        for i in range(t1.numel()):
            self.assertAlmostEqual(t1_flat[i], t2_flat[i], 7)

    def assert_state_dicts_equal(self, d1, d2):
        self.assertEqual(d1.keys(), d2.keys())
        for k in d1.keys():
            v1 = d1[k]
            v2 = d2[k]

            self.assert_tensors_equal(v1, v2)

    def test_int_tensor_serialization(self):
        t = torch.tensor([1, 2, 3])
        bytes_value = serialization.to_bytes(t)
        result, bytes_read = serialization.to_tensor_int(bytes_value)
        self.assert_tensors_equal(t, result)

    def test_float_tensor_serialization(self):
        t = torch.tensor([[1.0, 2.2, 3.3], [-1.3, 0.5, -10000.5]])
        bytes_value = serialization.to_bytes(t)

        result, bytes_read = serialization.to_tensor_float(bytes_value)
        self.assert_tensors_equal(t, result)

    def test_linear_layer_serialization(self):
        sd = nn.Linear(3, 5).state_dict()

        bytes_data = serialization.to_bytes(sd)
        result, bytes_read = serialization.to_state_dict(bytes_data)
        self.assert_state_dicts_equal(sd, result)

    def test_sequential_model_serialization(self):
        sd = nn.Sequential(nn.Linear(3, 5), nn.ReLU(), nn.Linear(2, 2)).state_dict()

        bytes_data = serialization.to_bytes(sd)
        result, bytes_read = serialization.to_state_dict(bytes_data)
        self.assert_state_dicts_equal(sd, result)
