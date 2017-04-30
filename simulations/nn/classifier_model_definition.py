import numpy as np
from keras.layers import Dense, Merge
from keras.layers.recurrent import LSTM
from keras.models import Sequential


def build_model(m):
    m.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])


def fit_model(m, kx_train, ky_train, max_epochs=1000):
    m.fit(kx_train,
          ky_train,
          batch_size=32,
          epochs=max_epochs,
          verbose=1)


def inference_model(m, input_list):
    log_probabilities = predict(m, input_list, log=True)
    k_star = np.argmax(np.sum(log_probabilities, axis=0))
    return k_star


def predict(m, norm_inputs, log=False):
    probabilities = m.predict(np.array(norm_inputs))
    if log:
        probabilities = np.log(probabilities + 0.000001)  # for stability.
    return probabilities


# No need to have regularization. The dataset is really big and the model really small.
def get_model(time_len, num_classes):
    left = Sequential()
    left.add(LSTM(32, batch_input_shape=[None, time_len, num_classes]))
    left.add(Dense(32, name='Dense_after_LSTM'))

    right = Sequential()
    right.add(Dense(32, name='Dense_Time', batch_input_shape=[None, time_len]))

    mf = Sequential()
    mf.add(Merge([left, right], mode='concat'))
    mf.add(Dense(32, name='Dense_classifier'))
    mf.add(Dense(num_classes, activation='softmax'))

    print(mf.summary())
    return mf
