import numpy as np
import pandas as pd
import src.constants as CONSTANTS
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense


def define_model(n_inputs, n_outputs):
    model = Sequential()
    model.add(Dense(32, input_dim=n_inputs, kernel_initializer='he_uniform', activation='relu'))
    model.add(Dense(8, activation='relu', kernel_initializer='he_uniform'))
    model.add(Dense(n_outputs, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam')
    return model

# evaluate a model using repeated k-fold cross-validation
def save_model(X, y):
    n_inputs, n_outputs = X.shape[1], y.shape[1]
    # define model
    model = define_model(n_inputs, n_outputs)
    # fit model
    model.fit(X, y, verbose=0, epochs=100)
    # save model
    model.save(CONSTANTS.MODEL_NAME)

def train_and_save_model():
    data = pd.read_csv(CONSTANTS.GAMESTATE_FILE)

    # Cleaning data
    data = data.drop(data[(data.W == 0) & (data.A == 0) & (data.S == 0) & (data.D == 0)].index)

    X = data[CONSTANTS.TRAINING_NAMES]
    y = data[CONSTANTS.TARGET_NAMES]

    save_model(X, y)

def get_model():
    return load_model(CONSTANTS.MODEL_NAME)

def predict_action(x):
    model = get_model()
    actions = model.predict(x)
    return actions.round()

