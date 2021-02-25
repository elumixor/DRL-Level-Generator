from typing import Dict
from unittest import TestCase

import torch

import remote_computation.model_manager as mm
from common import ByteReader
from remote_computation import RemoteModel
from remote_computation.models import ModelType, DQNModel
from serialization import to_bytes

model_dict: Dict[int, RemoteModel]


class RemoteModelLocalTests(TestCase):

    def setUp(cls):
        global model_dict
        model_dict = dict()

    def test_obtain_works(self):
        b = b''

        # model type (DQN)
        b += to_bytes(ModelType.DQN)
        # input_size
        b += to_bytes(5)
        # output_size
        b += to_bytes(7)

        model: DQNModel = mm.obtain_new(ByteReader(b))

        self.assertEqual(model.input_size, 5)
        self.assertEqual(model.output_size, 7)
        self.assertIsInstance(model.nn, torch.nn.Sequential)

    def test_save_load_model_works(self):
        b = b''

        # model type (DQN)
        b += to_bytes(ModelType.DQN)
        # input_size
        input_size = 5
        b += to_bytes(input_size)
        # output_size
        b += to_bytes(7)

        model: DQNModel = mm.obtain_new(ByteReader(b))

        file_path = "./dqn_model.m"

        mm.save_model(model.model_id, file_path)
        restored = mm.load_model(file_path)

        self.assertIsInstance(restored, DQNModel)
        self.assertEqual(restored.model_type, ModelType.DQN)
        self.assertEqual(restored.input_size, model.input_size)
        self.assertEqual(restored.output_size, model.output_size)

        x = torch.ones([input_size])

        y1 = model.nn.forward(x)
        y2 = restored.nn.forward(x)

        self.assertTrue(y1.equal(y2))

        # TODO: assert observation dict equality
        s1 = model.nn.state_dict()
        s2 = restored.nn.state_dict()
