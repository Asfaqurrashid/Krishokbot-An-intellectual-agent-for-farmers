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
    translator = Translator()
    question = request.json['question']
    q1 = translator.translate(question, dest = 'en')
    q2 = q1.text
    r1 = chatbot_response.chatbot_response(q2)
    r2 = translator.translate(r1, dest = 'bn')
    response = r2.text
    return jsonify({"response": str(response)})

if __name__ == '__main__':
    app.run()


# In[ ]:




