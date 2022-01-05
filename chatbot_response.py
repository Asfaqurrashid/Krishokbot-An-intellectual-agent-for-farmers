#!/usr/bin/env python
# coding: utf-8

# In[5]:


import time
import nltk
import json
import random
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model


# In[6]:


model = load_model('model.h5')


# In[7]:


intents = json.loads(open('intents.json', encoding = 'utf8').read())
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('labels.pkl', 'rb'))


# In[8]:


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower(), pos = 'v') for word in sentence_words]
    return sentence_words
def bow(sentence, words, show_details = True):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                bag[i] = 1
    return (np.array(bag))
def predict_class(sentence, model):
    p = bow(sentence, words, show_details = False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key = lambda x: x[1], reverse = True)
    return_list = []
    for r in results:
        return_list.append({"intent" : classes[r[0]], "Probability" : str(r[1])})
    return return_list
def getResponse(ints, intents_json):
    list_of_intents = intents_json['intents']
    if len(ints) == 0:
        for i in list_of_intents:
            if(i['tag'] == 'noanswer'):
                return random.choice(i['responses'])
    tag = ints[0]['intent']
    for i in list_of_intents:
        if (i['tag'] == tag):
            result = random.choice(i['responses'])
            break
    return result
def chatbot_response(text):
    ints = predict_class(text, model)
    res = getResponse(ints, intents)
    return res


# In[ ]:





# In[ ]:




