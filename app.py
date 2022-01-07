#!/usr/bin/env python
# coding: utf-8

# In[1]:


from flask import Flask, render_template, jsonify, request
import chatbot_response


# In[ ]:


app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html', **locals())

@app.route('/chatbot', methods=["GET", "POST"])
def chatbotResponse():

    if request.method == 'POST':
        the_question = request.form.get('question')

        response = chatbot_response.chatbot_response(the_question)

    return jsonify({"response": response })

if __name__ == '__main__':
    app.run()


# In[ ]:




