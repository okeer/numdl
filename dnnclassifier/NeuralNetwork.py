import numpy as np

from dnnclassifier.utils.ShuffledDataset import ShuffledDataset


class NeuralNetwork(object):
    def __init__(self, layers, learning_rate, iterations):
        self.layers = layers
        self.layers_count = len(self.layers)
        self.propagation_features = None
        self.learning_rate = learning_rate
        self.iterations = iterations

    def __forward_propagation(self, features):
        self.propagation_features = features

        for index in range(self.layers_count):
            self.propagation_features = self.layers[index].forward(self.propagation_features)

    def __backward_propagation(self, classes):
        d_activation = - (np.divide(classes, self.propagation_features) - np.divide(1 - classes,
                                                                                    1 - self.propagation_features))
        for index in reversed(range(len(self.layers))):
            d_activation = self.layers[index].backward(d_activation)
            self.layers[index].update(self.learning_rate)

    def __compute_loss(self, activation_layer, classes):
        m = classes.shape[1]
        return 1. / m * np.nansum(
            np.multiply(-np.log(activation_layer), classes) + np.multiply(-np.log(1 - activation_layer), 1 - classes))

    def train(self, features, classes, chunk_size=None):
        shuffled_dataset = ShuffledDataset(features, classes, chunk_size)

        for epoch in range(self.iterations):
            shuffled_dataset.shuffle()
            for minibatch in shuffled_dataset:
                mini_X, mini_Y = minibatch
                self.__forward_propagation(mini_X)
                self.__backward_propagation(mini_Y)

                if epoch % 500 == 0:
                    print(f"Epoch {epoch} loss is {self.__compute_loss(self.propagation_features, mini_Y)}")

    def predict(self, features):
        self.__forward_propagation(features)
        return self.propagation_features