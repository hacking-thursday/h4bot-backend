#-*- coding: utf-8 -*-

success = {
    "status": "success"
}

welcome = {
    "messages": [
        {"text": "Welcome to our store!"},
        {"text": "How can I help you?"} ]}

def attendee(attendee):
  return { "messages": [ {"text": u"今天有來的朋友：\n" + "\n".join(attendee)} ] }
