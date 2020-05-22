import os
import requests
from revised import *
import json

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

full = get_all()
s1 = get_episodes(full,1)
s2 = get_episodes(full,2)
s3 = get_episodes(full,3)
s4 = get_episodes(full,4)
s5 = get_episodes(full,5)
s6 = get_episodes(full,6)
s7 = get_episodes(full,7)
s8 = get_episodes(full,8)
s9 = get_episodes(full,9)
seasons = [s1,s2,s3,s4,s5,s6,s7,s8,s9]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/plot", methods=["POST"])
def plot():
    speakers = json.loads(request.form.get('speakers'))
    twc = json.loads(request.form.get('total_word_count'))
    tlc = json.loads(request.form.get('total_line_count'))
    wf = json.loads(request.form.get('word_frequency'))
    if wf:
        word = request.form.get('word')
    else:
        word = False
    seas = json.loads(request.form.get('seasons'))
    percent = json.loads(request.form.get('percent'))
    # print('**********')
    # print(percent)
    episodes = []
    for i in range(0,9):
        if seas[i]:
            episodes += seasons[i]
    x_axis_labels, speakers_data = generate_plot_data(speakers, episodes, total_word_count=twc, total_line_count=tlc, word_frequency=word, percent=percent)
    return jsonify({"success": True, "xLabels":x_axis_labels, "data":speakers_data})
