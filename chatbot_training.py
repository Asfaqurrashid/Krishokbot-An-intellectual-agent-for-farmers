#!/usr/bin/env python
# coding: utf-8

# In[13]:


import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
from nltk.corpus import stopwords
import json
import pickle
import tensorflow as tf
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD
import random


# In[14]:


words = []
classes = []
documents = []
ignore_words = ['?', '!']
data_file = open('intents.json', encoding = 'utf8').read()
intents = json.loads(data_file)


# In[15]:


for intent in intents['intents']:
    for pattern in intent['patterns']:
        w = nltk.word_tokenize(pattern)
        words.extend(w)
        documents.append((w, intent['tag']))
    if intent['tag'] not in classes:
        classes.append(intent['tag'])


# In[16]:


words = [word for word in words if word.isalpha()]
stop_words = set(stopwords.words('english'))
words = [w for w in words if not w in stop_words]
words = [lemmatizer.lemmatize(w.lower(), pos = 'v') for w in words if w not in ignore_words]
words = [word for word in words if len(word)>1]
words = sorted(list(set(words)))
classes = sorted(list(set(classes)))
pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('labels.pkl', 'wb'))


# In[17]:


training = []
output_empty = [0]*len(classes)
for doc in documents:
    bag = []
    pattern_words = doc[0]
    pattern_words = [lemmatizer.lemmatize(word.lower(), pos = 'v') for word in pattern_words]
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1
    training.append([bag, output_row])
random.shuffle(training)
training = np.array(training, dtype = object)
train_x = list(training[:,0])
train_y = list(training[:,1])


# In[18]:


model = Sequential()
model.add(Dense(128, input_shape = (len(train_x[0]),), activation = 'relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation = 'relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation = 'softmax'))
sgd = SGD(lr = 0.01, decay = 1e-6, momentum = 0.9, nesterov = True)
model.compile(loss = 'categorical_crossentropy', optimizer = sgd, metrics = ['accuracy'])
hist = model.fit(np.array(train_x), np.array(train_y), epochs = 600, batch_size = 5, verbose = 1)
model.save('model.h5', hist)


# In[ ]:





# In[ ]:




