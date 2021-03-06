import numpy as np

from utils import _build_architecture, _build_data_loader
from base import ACTIVATIONS, OPTIMIZERS, LOSS_FUNCS

import torch
import torch.nn as nn
import torch.optim as optim
from torch.autograd import Variable


class MLPClassifier(nn.Module):
    def __init__(self,
                 n_features,
                 n_classes,
                 hidden_layer_sizes=(100,),
                 activation='relu',
                 max_iter=200,
                 validation_fraction=0.1,
                 early_stopping=False):

        super(MLPClassifier, self).__init__()
        self.mlp = _build_architecture(n_features, n_classes, hidden_layer_sizes,
                                       ACTIVATIONS[activation])

    def forward(self, x):
        return self.mlp(x)

    def fit(self,
            X,
            y,
            epochs=10,
            loss='bce',
            learning_rate=1e-3,
            batch_size=10,
            solver='adam',
            verbose=False):

        self.batch_size = batch_size
        loader = _build_data_loader(self.batch_size, X, y)
        opt = OPTIMIZERS[solver](self.parameters(), lr=learning_rate)
        crit = LOSS_FUNCS[loss]
        for e in range(epochs):
            if verbose:
                print('\rEpoch {}'.format(e + 1), end='')
            for x, y in loader:
                opt.zero_grad()
                y_hat = self(x.float())
                loss = crit(y_hat, y.float())
                loss.backward()
                opt.step()

    def predict_proba(self, X):
        loader = _build_data_loader(self.batch_size, X)
        for idx, x in enumerate(loader):
            if idx == 0:
                y_hat = self(x.float()).data.numpy()
            else:
                y_hat = np.vstack([y_hat, self(x.float()).data.numpy()])
        return y_hat

    def predict_log_proba(self, X):
        return np.log(self.predict_proba(X))

    def predict(self, X):
        return np.argmax(self.predict_proba(X), axis=1)


class MLPRegressor(nn.Module):
    def __init__(self,
                 n_features,
                 hidden_layer_sizes=(100,),
                 activation='relu',
                 max_iter=200,
                 validation_fraction=0.1,
                 early_stopping=False):

        super(MLPRegressor, self).__init__()
        self.mlp = _build_architecture(n_features, 1, hidden_layer_sizes,
                                       ACTIVATIONS[activation])

    def forward(self, x):
        return self.mlp(x)

    def fit(self,
            X,
            y,
            epochs=10,
            loss='mse',
            learning_rate=1e-3,
            batch_size=10,
            solver='adam',
            verbose=False):

        self.batch_size = batch_size
        loader = _build_data_loader(self.batch_size, X, y)
        opt = OPTIMIZERS[solver](self.parameters(), lr=learning_rate)
        crit = LOSS_FUNCS[loss]
        for _ in range(epochs):
            for x, y in loader:
                opt.zero_grad()
                y_hat = self(x.float())
                loss = crit(y_hat, y.float())
                loss.backward()
                opt.step()

    def predict_proba(self, X):
        loader = _build_data_loader(self.batch_size, X)
        for idx, x in enumerate(loader):
            if idx == 0:
                y_hat = self(x.float()).data.numpy()
            else:
                y_hat = np.vstack([y_hat, self(x.float()).data.numpy()])
        return y_hat

    def predict_log_proba(self, X):
        return np.log(self.predict_proba(X))

    def predict(self, X):
        return np.argmax(self.predict_proba(X), axis=1)
#%% Convolutional Neural Network


class ConvNet(nn.Module):
    """Docstring.
    """

    def __init__(self,
                 n_classes,
                 in_channels,
                 out_layer_channels=(128, 256, 256),
                 fc_layer_channels=(100,),
                 activation='relu',
                 max_iter=200,
                 validation_fraction=0.1,
                 early_stopping=False):

        super(ConvNet, self).__init__()
        # Create the convlayers.
        self.convlayers = [nn.Conv2d(
            self, in_channels, out_channel, 3) for out_channel in out_layer_channels]
        # Create the fully connected layers, adding the n_classes layer at the end.
        self.fclayers = [nn.Linear(out_layer_channels[-1], fc_layer_channel)
                         for fc_layer_channel in fc_layer_channels.append(n_classes)]
        # Create the full pipeline.
        self.net = nn.Sequential(self.convlayers + self.fclayers)
    
    def forward(self, x):
        return self.net(x)

    def fit(self,
            X,
            y,
            epochs=10,
            loss='crossentropy',
            learning_rate=1e-3,
            batch_size=10,
            optim='adam',
            verbose=False):

        self.batch_size = batch_size
        loader = _build_data_loader(self.batch_size, X, y)
        opt = OPTIMIZERS[optim](self.parameters(), lr=learning_rate)
        crit = LOSS_FUNCS[loss]
        for e in range(epochs):
            if verbose:
                print('\rEpoch {}'.format(e + 1), end='')
            for x, y in loader:
                opt.zero_grad()
                y_hat = self(x.float())
                loss = crit(y_hat, y.float())
                loss.backward()
                opt.step()

    def predict_proba(self, X):
        loader = _build_data_loader(self.batch_size, X)
        for idx, x in enumerate(loader):
            if idx == 0:
                y_hat = self(x.float()).data.numpy()
            else:
                y_hat = np.vstack([y_hat, self(x.float()).data.numpy()])
        return y_hat

    def predict_log_proba(self, X):
        return np.log(self.predict_proba(X))

    def predict(self, X):
        return np.argmax(self.predict_proba(X), axis=1)