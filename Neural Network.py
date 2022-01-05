#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
from nltk.corpus import stopwords
import random
import numpy as np
import pickle
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.models import load_model


# In[2]:


data_file = open('intents.json', encoding = 'utf8').read()


# In[3]:


intents = json.loads(data_file)


# In[24]:


words = []
classes = []
documents = []
ignore_words = ['?', '!', '(', ')','.', ',']


# In[25]:


for intent in intents['intents']:
    print(intent['tag'])


# In[26]:


for intent in intents['intents']:
    for pattern in intent['patterns']:
        w = nltk.word_tokenize(pattern)
        words.extend(w)
        documents.append((w, intent['tag']))
    if intent['tag'] not in classes:
        classes.append(intent['tag'])


# In[27]:


words


# In[28]:


documents


# In[29]:


classes


# In[30]:


words = [word for word in words if word.isalpha()]
stop_words = set(stopwords.words('english'))
words = [w for w in words if not w in stop_words]
words = [lemmatizer.lemmatize(w.lower(), pos = 'v') for w in words if w not in ignore_words]
words = [word for word in words if len(word)>1]


# In[31]:


words


# In[32]:


words = sorted(list(set(words)))


# In[33]:


classes = sorted(list(set(classes)))


# In[34]:


words


# In[41]:


classes


# In[42]:


print(len(documents), "documents")


# In[43]:


print(len(classes), "classes", classes)


# In[44]:


print(len(words), "Unique Lemmatized words", words)


# In[45]:


training = []
output_empty = [0] * len(classes)
len(output_empty)


# In[46]:


output_empty


# In[47]:


for doc in documents:
    bag = []
    pattern_words = doc[0]
    print(doc)
    print(doc[0])


# In[48]:


for doc in documents:
    bag = []
    pattern_words = doc[0]
    pattern_words = [lemmatizer.lemmatize(word.lower(), pos = 'v') for word in pattern_words]
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1
    training.append([bag, output_row])


# In[49]:


print(bag)


# In[50]:


print(training)


# In[51]:


random.shuffle(training)


# In[52]:


training = np.array(training, dtype = object)


# In[53]:


print(training)


# In[54]:


print(len(training))


# In[55]:


train_x = list(training[:,0])


# In[56]:


train_y = list(training[:,1])


# In[57]:


print(train_x)


# In[58]:


print(train_y)


# In[59]:


print(train_x[0], " ", train_y[0])


# In[60]:


model = Sequential()
model.add(Dense(128, input_shape = (len(train_x[0]), ), activation = 'relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation = 'relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation = 'softmax'))


# In[61]:


sgd = SGD(lr = 0.01, decay = 1e-6, momentum = 0.9, nesterov = True)
model.compile(loss = 'categorical_crossentropy', optimizer = sgd, metrics = ['accuracy'])


# In[62]:


hist = model.fit(np.array(train_x), np.array(train_y), epochs = 600, batch_size = 5, verbose = 1)


# In[63]:


model.save('model.h5', hist)


# In[15]:


model = load_model('model.h5')


# In[16]:


intents = json.loads(open('intents.json', encoding = 'utf8').read())


# In[17]:


words = pickle.load(open("words.pkl", "rb"))


# In[18]:


classes = pickle.load(open("labels.pkl", "rb"))


# In[19]:


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower(), pos = 'v') for word in sentence_words]
    return sentence_words


# In[20]:


sentence = clean_up_sentence("Here we going again some direction")
sentence


# In[21]:


def bow(sentence, words, show_details = True):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]* len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                bag[i] = 1
    return (np.array(bag))


# In[22]:


def predict_class(sentence, model):
    p = bow(sentence, words, show_details = False)
    res = model.predict(np.array([p]))[0]
    print(res)
    ERROR_THRESHOLD = 0.1
    results = [[i,r] for i,r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key = lambda x: x[1], reverse = True)
    print(results)
    return_list = []
    for r in results:
        return_list.append({"intent" : classes[r[0]], "Probability" : str(r[1])})
    for i in return_list:
        print(i)
    return return_list
    


# In[23]:


def getResponse(ints, intents_json):
    list_of_intents = intents_json['intents']
    print(len(ints))
    if len(ints) == 0:
        for i in list_of_intents:
            if(i['tag'] == 'noanswer'):
                return random.choice(i['responses'])
    tag = ints[0]['intent']
    print(tag)
    for i in list_of_intents:
        if (i['tag'] == tag):
            result = random.choice(i['responses'])
            break
    return result


# In[24]:


def chatbot_response(text):
    ints = predict_class(text, model)
    res = getResponse(ints, intents)
    return res


# In[25]:


y = chatbot_response("rice plants are short, leaves are yellow")
y


# In[ ]:





# In[ ]:





# In[ ]:




