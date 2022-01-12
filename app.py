#!/usr/bin/env python
# coding: utf-8

# In[1]:


from flask import Flask, render_template, jsonify, request
import chatbot_response
import re
import json


app = Flask(__name__)

@app.route('/')
def index():
    return "hello_world"
    
@app.route('/chatbot', methods=["POST"])
def chatbotResponse():
    req_data = request.get_json()
    question = req_data['question']
    res = str(question)
    response = chatbot_response.chatbot_response(question)
    return jsonify({"response": str(res)})

if __name__ == '__main__':
    app.run()


# In[ ]:




