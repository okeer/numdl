import unittest
import numpy as np

from ReluLayer import ReluLayer
from SigmoidLayer import SigmoidLayer
from models.LayerBase import LayerBase


class LayerTest(unittest.TestCase):
    def __init_test_layer(self, cls):
        self.layer = cls(2, lambda x: x)
        self.layer.weights = np.array([[0.5, 0.3], [0.1, 0.2]])
        self.layer.bias = np.array([[0.1, 0.2]]).reshape((2, 1))
        self.features = np.array([[1, 2, 3], [2, 1, 0.5]])

    def test_givenBaseLayer_whenForward_shouldCalculatePreActivation(self):
        self.__init_test_layer(LayerBase)
        pre_activation_assrt = np.array([[1.2, 1.4, 1.75], [0.7, 0.6, 0.6]])

        self.layer._LayerBase__forward_linear(self.features)

        self.assertEqual(True, isinstance(self.layer.pre_activation, np.ndarray))
        np.testing.assert_array_almost_equal(pre_activation_assrt, self.layer.pre_activation)

    def test_givenSigmoidLayer_whenForward_shouldCalculateActivation(self):
        self.__init_test_layer(SigmoidLayer)
        sigmoid_activation_assert = np.array([[0.76852478, 0.80218389, 0.8519528],
                                              [0.66818777, 0.64565631, 0.64565631]])

        activation = self.layer.forward(self.features)

        np.testing.assert_array_almost_equal(sigmoid_activation_assert, activation)

    def test_givenReluLayer_whenForward_shouldCalculateActivation(self):
        self.__init_test_layer(ReluLayer)
        relu_activation_assert = np.array([[1, 1, 1],
                                           [1, 1, 1]])

        activation = self.layer.forward(self.features)

        np.testing.assert_array_almost_equal(relu_activation_assert, activation)

    def test_givenSigmoidLayer_whenBackward_shouldCalculateSlope(self):
        self.__init_test_layer(SigmoidLayer)
        classes = np.array([[1, 1, 1],
                            [1, 1, 1]])

        activation = self.layer.forward(self.features)

        d_activation = (np.divide(classes, activation) - np.divide(1 - classes, 1 - activation))
        d_act_prev = self.layer.backward(d_activation)

        print(d_activation)
        print(d_act_prev)

        pass


if __name__ == '__main__':
    unittest.main()
