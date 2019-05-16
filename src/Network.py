#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Simulate an Internet of things network, and send data on nodes to the server
# Author: Cody Lewis
# Date: 2019-05-16


import random
import time
from json.encoder import JSONEncoder

import requests

import Secrets
import Functions


ADMIN_DB_ADDR = f"http://{Secrets.DB_USERNAME}:{Secrets.DB_PASSWORD}@127.0.0.1:5984/sensors"
DB_ADDR = f"http://127.0.0.1:5984/sensors"
THING_TYPES = ["Themometer", "Acnemometer", "Smart Light", "Pulse Oximeter"]
JSONENCODER = JSONEncoder()


class Thing:
    '''
    A simulated thing in the network.
    '''
    def __init__(self, id_num=0, x_val=0, y_val=0, type_val="Thing"):
        self.__id = id_num
        self.__x = x_val
        self.__y = y_val
        self.__type = type_val
        self.__data = []
        self.rev = ""

    def get_type(self):
        return self.__type

    def get_id(self):
        return self.__id

    def get_json(self):
        '''
        Get a JSON style string from the values contained in this
        '''
        return JSONENCODER.encode(self.__get_vals())

    def __get_vals(self):
        '''
        Get a dictionary of the values in this
        '''
        return {
            "id": self.__id,
            "x": self.__x,
            "y": self.__y,
            "type": self.__type,
            "data": self.__data
        }

    def add_data(self, data):
        '''
        Add a row of data to this
        '''
        self.__data.append(data)

    def get_data_json(self):
        vals = self.__get_vals()
        vals["_rev"] = self.rev
        return JSONENCODER.encode(vals)


class Network:
    '''
    The simulated network.
    '''
    def __init__(self, total_nodes):
        requests.put(f"{ADMIN_DB_ADDR}")
        self.__nodes = []
        for i in range(total_nodes):
            new_thing = Thing(i, random.randint(0, 255), random.randint(0, 255), THING_TYPES[i % len(THING_TYPES)])
            request = requests.put(f"{DB_ADDR}/{new_thing.get_id()}", data=new_thing.get_json())
            new_thing.rev = request.json()["rev"]
            self.__nodes.append(new_thing)
            Functions.print_progress(i + 1, total_nodes, prefix=f"{i + 1}/{total_nodes} created")
        print()

    def run(self):
        '''
        Run the network infinitely.
        '''
        cur_time = 0, 0
        while True:
            # chosen_node = self.__nodes[random.randint(0, len(self.__nodes) - 1)]
            for node in self.__nodes:
                node_type = node.get_type()
                if node_type == "Themometer":
                    node.add_data({"time": cur_time, "temp": random.randint(15, 40)})
                elif node_type == "Acnemometer":
                    node.add_data({"time": cur_time, "speed": random.randint(0, 40), "pressure": random.randint(0, 20)})
                elif node_type == "Smart Light":
                    node.add_data({
                        "time": cur_time,
                        "status": random.sample(["On", "Off"], 1)[0],
                        "usage": random.uniform(0, 1)
                    })
                elif node_type == "Pulse Oximeter":
                    node.add_data({"time": cur_time, "rate": random.randint(50, 170)})
                request = requests.put(f"{DB_ADDR}/{node.get_id()}", data=node.get_data_json())
                node.rev = request.json()["rev"]
            print(f"\rAdded data for all nodes at time {cur_time}.", end="\r")
            time.sleep(1)
            cur_time += 1

    def cleanup(self):
        for index_node in enumerate(self.__nodes):
            ok = False
            while not ok:
                rev = requests.get(f"{DB_ADDR}/{index_node[1].get_id()}").json()["_rev"]
                request = requests.delete(f"{DB_ADDR}/{index_node[1].get_id()}?rev={rev}")
                ok = request.json()["ok"]
            Functions.print_progress(index_node[0] + 1, len(self.__nodes), prefix=f"{index_node[0] + 1}/{len(self.__nodes)} deleted")
        print()


if __name__ == '__main__':
    NUMBER_NODES = 10
    print(f"Creating a network with {NUMBER_NODES} nodes.")
    NETWORK = Network(NUMBER_NODES)
    try:
        print("Running the network...")
        NETWORK.run()
    except KeyboardInterrupt:
        print()
        print("Cleaning up...")
        NETWORK.cleanup()
        print("bye.")
