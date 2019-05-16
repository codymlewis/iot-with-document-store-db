#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from json.encoder import JSONEncoder
import requests

from flask import Flask, render_template
app = Flask(__name__)


DB_ADDR = f"http://127.0.0.1:5984/sensors"

JSONENCODER = JSONEncoder()

# NODE_DATA = get_node_data()


@app.route("/")
def home():
    return render_template('index.html', title="Map")


@app.route("/nodes/<node_id>")
def show_node(node_id):
    data = requests.get(f"{DB_ADDR}/{node_id}").json()
    return render_template('node.html', title=f"{node_id}", data=data)


@app.route("/node-data")
def get_node_data():
    data = requests.post(f"{DB_ADDR}/_find", data=JSONENCODER.encode({
        "selector": {
            "id": {
                "$gt": None
            }
        }
    }), headers={"Content-Type": "application/json"}).json()
    return JSONENCODER.encode(data)
