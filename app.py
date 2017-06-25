# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
import sqlite3
from flask import g

app = Flask(__name__)

@app.before_request
def before_request():
    g.db = sqlite3.connect("h4bot.db")

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

def get_user(id):
    cur = g.db.cursor()
    cur.execute("SELECT * FROM users WHERE user_id = %s" % id)

    user = cur.fetchone()

    return user[0] if user else None

def get_users():
    cur = g.db.cursor()

    cur.execute("SELECT user_id, first_name, last_name, profile_pic_url FROM users")
    users = cur.fetchall()

    return users

def add_user(id, first_name, last_name, profile_pic_url):
    g.db.execute("INSERT INTO users (user_id, first_name, last_name, profile_pic_url) VALUES (?, ?, ?, ?)", (id, first_name, last_name, profile_pic_url))
    g.db.commit()

@app.route('/nick', methods=['GET', 'POST'])
def nick():
    if request.method == 'POST':
        print request.form
        g.db.execute("INSERT INTO nick (user_id, nickname) VALUES (?, ?)", (request.form['messenger user id'], request.form['nick']))
        g.db.commit()

    return jsonify('')

@app.route('/checkin', methods=['GET', 'POST'])
def checkin():
    if request.method == 'POST':
        print request.form
        g.db.execute("INSERT INTO checkin (user_id) VALUES (?)", (request.form['messenger user id'],))
        g.db.commit()

        print get_user(request.form['messenger user id'])
        if not get_user(request.form['messenger user id']):
            add_user(request.form['messenger user id'], request.form['first name'], request.form['last name'], request.form['profile pic url'])

    return jsonify('')

@app.route('/attendee')
def attendee():
    attendee = []

    cur = g.db.cursor()
    cur.execute("SELECT DISTINCT checkin.user_id, users.*, n.* FROM checkin LEFT OUTER JOIN users ON users.user_id=checkin.user_id LEFT OUTER JOIN (SELECT MAX(nick.id), nick.* FROM nick GROUP BY nick.user_id) n ON checkin.user_id=n.user_id WHERE checkin.datetime LIKE '2017-05-18%'")
    _ = cur.fetchall()

    for a in _:
        attendee.append('%s (%s %s)' % (a[11], a[3], a[4]) if a[11] else '%s %s' % (a[3], a[4]))

    return jsonify({ "messages": [ {"text": u"今天有來的朋友：\n" + "\n".join(attendee)} ] })

@app.route('/users', methods=['GET', 'POST'])
def users():
    ret_users = []
    if request.method == 'POST':
        ## add users here
        print request.form
        if not get_user(request.form['messenger user id']):
            add_user(request.form['messenger user id'], request.form['first name'], request.form['last name'], request.form['profile pic url'])

        return jsonify('')

    else:
        users = get_users()
        for user in users:
            #/****************************************************************
            #   0           1          2           3
            # user_id, first_name, last_name, profile_pic_url
            #****************************************************************/
            full_name = user[1] + user[2]
            ret_users.append(full_name)
            print full_name

        return jsonify({ "messages": [ {"text": u"所有的朋友：\n" + "\n".join(ret_users)} ] })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
