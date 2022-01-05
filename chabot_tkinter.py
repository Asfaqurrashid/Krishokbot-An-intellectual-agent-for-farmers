#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tkinter
from tkinter import *
import import_ipynb
import chatbot_response


# In[2]:


def send():
    msg = str(EntryBox.get("1.0", 'end - 1c').strip())
    EntryBox.delete("0.0", END)
    if msg != '':
        Chatlog.config(state = NORMAL)
        Chatlog.insert(END, "You: " + msg + '\n\n')
        Chatlog.config(foreground = "#442265", font = ("Verdana", 12 ))
        res = str(chatbot_response.chatbot_response(msg))
        Chatlog.insert(END, "Bot: " + res + '\n\n')
        Chatlog.config(state = DISABLED)
        Chatlog.yview(END)


# In[3]:


base = Tk()
base.title("Chatbot")
base.geometry("400x500")
base.resizable(width = False, height = False)


# In[4]:


Chatlog = Text(base, bd = 0, bg = "white", height = "8", width = "50", font = "Arial")
Chatlog.config(state = DISABLED)


# In[5]:


scrollbar = Scrollbar(base, command = Chatlog.yview, cursor = "heart")
Chatlog['yscrollcommand'] = scrollbar.set


# In[6]:


sendButton = Button(base, font = ("Verdana", 12, 'bold'), text = "Send", width = 12, height = 5, bd = 0, bg = "#32de97", activebackground = "#3c9d9b", fg = "#ffffff", command = send)


# In[7]:


EntryBox = Text(base, bd = 0, bg = "white", width = "29", height = "5", font = "Arial")


# In[8]:


scrollbar.place(x = 376, y = 6, height = 386)
Chatlog.place(x = 6, y = 6, height = 386, width = 370)
EntryBox.place(x = 128, y = 401, height = 90, width = 265)
sendButton.place(x = 6, y = 401, height = 90)


# In[9]:


base.mainloop()


# In[ ]:





# In[ ]:




