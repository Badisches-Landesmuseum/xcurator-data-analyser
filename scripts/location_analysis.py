import logging
import os
import pickle
import json
import pandas as pd
from collections import Counter

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import mpl_toolkits

import sys


class LocationAnalyser:

    # Beispiel:
    # 'ort': [{'typ': 'Fundort/Herkunft', 'term': 'Bad Säckingen', 'lon': '7.94612', 'lat': '47.55371'}],
    # 'ort': [{'typ': 'Münzstätte', 'term': 'Lyon'}],

    def __init__(self):

        self.no_loc = 0
        self.no_lon_lat = 0
        self.no_standort = 0

        self.list_loc = []
        self.type_loc = []
        self.list_standort = []
        self.lat_long_type = []
        self.long_lat_list = []

        self.all_types = []

    def evaluate_location(self, objects):
        for object in objects["records"]:
            has_loc = False
            if 'ort' in object.keys():
                if object['ort'] != 'nicht ausgestellt':
                    self.list_loc.append(object['ort'])
                    for element in object['ort']:
                        if 'lon' in element.keys():
                            has_loc = True
                            self.lat_long_type.append(element['typ'])
                            self.long_lat_list.append([element['lon'], element['lat']])
                        self.all_types.append(element['typ'])

                    if not has_loc:
                        self.no_lon_lat += 1

                else:
                    self.no_loc += 1
            else:
                self.no_loc += 1

        for object in objects["records"]:
            if 'standort' in object.keys():
                if object['standort'] != 'nicht ausgestellt':
                    self.list_standort.append(object['standort'])
                else:
                    self.no_standort += 1
            else:
                self.no_standort += 1

        print('Results of location analysis:')
        print('The give collection has ' + str(len(objects["records"])) + ' objects.')
        print('From those ' + str(self.no_loc) + ' have no associated location field.')
        print('From those the whole collection ' + str(
            self.no_lon_lat) + ' have no long or lat information.')
        print('There are ' + str(self.no_standort) + ' objects who have no standort field.')

        print('###')
        print('The field "Ort" has ' + str(len(list(set(self.all_types)))) + ' different types.')
        print('Namely: ' + str(list(set(self.all_types))))
        print('One object can have multiple location attributes. Therefore we have ' + str(
            len(self.all_types)) + ' total locations.')

        print('###')
        print('For the whole collection the types of location are distributed as followed: ')
        print(Counter(self.all_types).keys())
        print(Counter(self.all_types).values())

        print(
            'For the locations that have long ant lat coordinates the types of location are distributed as followed: ')
        print(Counter(self.lat_long_type).keys())
        print(Counter(self.lat_long_type).values())


if __name__ == '__main__':
    # You can choose if you want to analyse the expodb or just the Katalog
    # with open('../resources/objects/katalog.json') as f:
    #   objects = json.load(f)
    with open('../resources/objects/expodb.json') as f:
        objects = json.load(f)
    location_analyser = LocationAnalyser()
    location_analyser.evaluate_location(objects=objects)
