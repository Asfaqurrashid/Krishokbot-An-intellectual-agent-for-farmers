#!/usr/bin/env python
# coding: utf-8

# In[1]:


from flask import Flask, render_template, jsonify, request
import chatbot_response
import re
import json
from googletrans import Translator


app = Flask(__name__)

@app.route('/')
def index():
    return "hello_world"
    
@app.route('/chatbot', methods=["POST"])
def chatbotResponse():
    question = request.json['question']
    translator = Translator()
    question = translator.translate(question, dest = 'en')
    response = chatbot_response.chatbot_response(question.text)
    response = translator.translate(response, dest = 'bn')
    return jsonify({"response": str(response.text)})

if __name__ == '__main__':
    app.run()


# In[ ]:




