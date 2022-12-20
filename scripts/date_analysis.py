import logging
import os
import pickle
import json
import pandas as pd

import sys


class DateAnalyser:

    # Beispiele:
    # {'term': 'Römische Kaiserzeit (31/27 v. Chr.-395)', 'beginn': '-31', 'ende': '395'}
    # {'term': '71', 'beginn': '71', 'ende': '71'}
    # {'term': 'Mittlere römische Kaiserzeit (69-192)', 'beginn': '69', 'ende': '192'}
    # {'term': 'Merowingerzeit', 'beginn': '400', 'ende': '751'}
    # [{'term': 'Zhou-Dynastie'}]
    # {'term': '21. Jh.', 'beginn': '2000', 'ende': '2099'}]
    # {'term': '3.-5. Jh.', 'beginn': '200', 'ende': '499'}
    # {'term': '22.08.1992', 'beginn': '1992', 'ende': '1992'}
    # {'term': 'August 1992', 'beginn': '1992', 'ende': '1992'}}

    def __init__(self):
        self.no_date_counter = 0
        self.no_begin_or_end = 0

        self.list_dates = []
        self.begin_and_end_list = []
        self.begin_and_end_list_objects = []
        self.no_begin_end_datierung = []
        self.multiple_begin_and_end = []
        self.term_one_year = []
        self.no_date_objects = []

        self.counter_100000 = 0
        self.counter_10000 = 0
        self.counter_5000 = 0
        self.counter_2000 = 0
        self.counter_0 = 0
        self.counter_over_100 = 0
        self.counter_under_100 = 0
        self.counter_one_year = 0

        self.longer_two = 0
        self.day_note = 0

        self.oldest = 2022.0
        self.under_5000 = 0

    def set_rough_time(self, time: float) -> None:
        if time < -100000:
            self.counter_100000 += 1
        if time < -10000:
            self.counter_10000 += 1
        if time < -5000:
            self.counter_5000 += 1
        if time < -2000:
            self.counter_2000 += 1
        if time < 0:
            self.counter_0 += 1

    def evaluate_date(self, objects):
        for object in objects["records"]:
            if 'datierung' in object.keys():
                self.list_dates.append(object['datierung'])
                counter_date = 0
                for index, date_entry in enumerate(object['datierung']):

                    if 'beginn' in date_entry.keys():

                        self.set_rough_time(float(date_entry['beginn']))

                        counter_date += 1

                        if counter_date == 1:
                            self.begin_and_end_list.append([date_entry['beginn'], date_entry['ende']])
                            self.begin_and_end_list_objects.append(object)
                            if float(date_entry['ende']) - float(date_entry['beginn']) == 0:
                                self.term_one_year.append(date_entry['term'])
                        elif counter_date >= 2:
                            self.multiple_begin_and_end.append(object)

                if counter_date == 0 and index == len(object['datierung']) - 1:
                    self.no_begin_end_datierung.append(object)
                    self.no_begin_or_end += 1

            else:
                self.no_date_objects.append(object)
                self.no_date_counter += 1

        # Check for span of dates
        for element in self.begin_and_end_list:
            start = float(element[0])
            end = float(element[1])
            if start >= 0:
                if end - start > 100:
                    self.counter_over_100 += 1
                else:
                    self.counter_under_100 += 1
                    if end - start == 0:
                        self.counter_one_year += 1
            else:
                if (start * -1) - (end * -1) > 100:
                    self.counter_over_100 += 1
                else:
                    self.counter_under_100 += 1
                    if (start * -1) - (end * -1) == 0:
                        self.counter_one_year += 1

        # check for if the term of the one year is on month level
        for term in self.term_one_year:
            if len(term.split(' ')) >= 2:
                self.longer_two += 1

        # check for if the term of the one year is on day level
        for term in self.term_one_year:
            if len(term.split('.')) >= 3:
                self.day_note += 1

        # check for oldest and older -5000
        for element in self.list_dates:
            if 'beginn' in element[0].keys():
                if float(element[0]['beginn']) < self.oldest:
                    self.oldest = float(element[0]['beginn'])

                if float(element[0]['beginn']) <= -5000:
                    self.under_5000 += 1

        print('Results of Date analysis:')
        print('The give collection has ' + str(len(objects["records"])) + ' objects.')
        print('From those ' + str(len(self.multiple_begin_and_end)) + ' have multiple available begin and end dates.')
        print('From those ' + str(
            len(self.no_begin_end_datierung)) + ' have no available begin and end dates but have a field "datierung".')
        print('There are ' + str(self.no_date_counter) + ' do not have the field "datierung".')
        print('That means ' + str(
            len(self.begin_and_end_list)) + ' have an available begin and end dates within the "datierung" field.')
        print('###')
        print('The oldest object is from: ' + str(self.oldest) + ' and there are ' + str(
            self.under_5000) + ' objects older than 5000 years BC.')
        print('The collection contains ' + str(self.counter_100000) + ' objects older than 100000 B.C.')
        print('The collection contains ' + str(self.counter_10000) + ' objects older than 10000 B.C.')
        print('The collection contains ' + str(self.counter_5000) + ' objects older than 5000 B.C.')
        print('The collection contains ' + str(self.counter_2000) + ' objects older than 2000 B.C.')
        print('The collection contains ' + str(self.counter_0) + ' objects older than year 0.')
        print('###')
        print('There are ' + str(self.counter_over_100) + ' wich are dated to a span of over 100 years.')
        print('There are ' + str(self.counter_under_100) + ' wich are dated to a span of under 100 years.')
        print('There are ' + str(self.counter_one_year) + ' wich are dated to exactly one year.')
        print('For the one year objects ' + str(self.longer_two) + ' could be broken down to the month and ' + str(
            self.day_note) + ' to an exact day')


if __name__ == '__main__':
    # You can choose if you want to analyse the expodb or just the Katalog
    with open('../resources/objects/katalog.json') as f:
        objects = json.load(f)
    #with open('../resources/objects/expodb.json') as f:
     #   objects = json.load(f)
    date_analyser = DateAnalyser()
    date_analyser.evaluate_date(objects=objects)
