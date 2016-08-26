import matplotlib.pyplot as plt
import numpy as np

# In[14]:

np.random.seed(42)
xs = np.array(np.linspace(0, 2, 10000))
f = np.exp(-xs)
# plt.plot(xs, f)
# plt.show()

# In[15]:

CUTOFF_SPEED = 0.3

# In[16]:

# For example if we have 0.9, we want the network to understand that:
# exp(-x) = 0.9
# x = -log(0.9) => 0.105
# cutoff is 0.3. So x_cutoff = 1.203
# result = 1.203 - 0.105 = 1.098
# Function to approximate is then:
# INPUT: 0.9, F(X) = log(X) - log(0.3)


# In[17]:

x_inputs = np.random.uniform(low=0, high=-np.log(0.3), size=(1000,))
inputs = np.exp(-x_inputs)


# plt.plot(inputs)


# In[18]:

def f(x):
    return np.log(x) - np.log(CUTOFF_SPEED)


# In[19]:

outputs = f(inputs)
# plt.plot(outputs)

# In[ ]:

from keras.models import Sequential
from keras.layers.core import Dense

model = Sequential()
model.add(Dense(10, input_shape=(1,), activation='sigmoid'))
model.add(Dense(10, activation='sigmoid'))
model.add(Dense(1, activation='sigmoid'))

model.summary()
model.compile(loss='mse', optimizer='sgd')

# In[ ]:

train_loss = []
for epoch in range(10):
    model.fit(inputs, outputs,
              batch_size=1, nb_epoch=10,
              verbose=1, validation_data=(inputs, outputs))
    train_loss.append(model.evaluate(inputs, outputs))

# In[ ]:

plt.plot(train_loss)
