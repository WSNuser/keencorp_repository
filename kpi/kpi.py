# -*- coding: utf-8 -*-
from __future__ import division

import datetime
import os
import sys

sys.path.insert(0, os.path.abspath(".."))
import core.keencorp_func
import core.keencorp_api

import csv

MESSAGE_LIMIT = 10

credentials = {"api_access": {"username": "enron@enron_alt", "password": "k33nc0rp"}}
identity = credentials["api_access"]["username"].split("@")[1]
api = core.keencorp_api.keencorp_api(
    credentials["api_access"]["username"],
    credentials["api_access"]["password"], "https://api.keencorp.com")

start_date = 0
to_date = datetime.datetime.strptime(datetime.datetime.now().isoformat().split(".")[0], "%Y-%m-%dT%H:%M:%S")

# Request supergroups
supergroups = api.request_super_groups()

# Request default scores
results = {"default_scores": {}, "smoothed_scores": {}, "raw_scores": {}}
for x in supergroups["supergroups"].keys():
    my_res = api.request_scores({x: supergroups["supergroups"][x]},
                                     0,
                                     core.keencorp_func.timeToEpoch(to_date))
    results["default_scores"][x] = my_res["scores"][x]

for x in supergroups["supergroups"].keys():
    my_res = api.request_smoothed_scores({x: supergroups["supergroups"][x]},
                                     0,
                                     core.keencorp_func.timeToEpoch(to_date))
    results["smoothed_scores"][x] = my_res["scores"][x]

for x in supergroups["supergroups"].keys():
    my_res = api.request_scores({x: supergroups["supergroups"][x]},
                                     0,
                                     core.keencorp_func.timeToEpoch(to_date),
                                    no_smoothing=True)
    results["raw_scores"][x] = my_res["scores"][x]


# Filter < 43 out
filtered_results = {"default_scores": {}, "smoothed_scores": {}, "raw_scores": {}}
for x in results["default_scores"]:
    filtered_results["default_scores"][x] = []
    filtered_results["smoothed_scores"][x] = []
    filtered_results["raw_scores"][x] = []

    for y in range(0, len(results["default_scores"][x])):
        if results["default_scores"][x][y]["amount"] >= MESSAGE_LIMIT:
            filtered_results["default_scores"][x].append(results["default_scores"][x][y])
            filtered_results["smoothed_scores"][x].append(results["smoothed_scores"][x][y])
            filtered_results["raw_scores"][x].append(results["raw_scores"][x][y])
        else:
            filtered_results["default_scores"][x].append({"date": results["default_scores"][x][y]["date"], "amount": None, "score": None})
            filtered_results["smoothed_scores"][x].append({"date": results["default_scores"][x][y]["date"], "amount": None, "score": None})
            filtered_results["raw_scores"][x].append({"date": results["default_scores"][x][y]["date"], "amount": None, "score": None})

fieldnames = ["date",
              "default_scores", "default_scores_normalized",
              "smoothed_scores", "smoothed_scores_normalized",
              "raw_scores", "raw_scores_normalized",
              "amount"
              ]

with open('scores.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=",", quotechar='"')
    writer.writerow(fieldnames)

    for i in filtered_results["default_scores"]:
        default_scores = [x["score"] for x in filtered_results["default_scores"][i] if x["score"] != None]
        smoothed_scores = [x["score"] for x in filtered_results["smoothed_scores"][i] if x["score"] != None]
        raw_scores = [x["score"]/x["amount"] for x in filtered_results["raw_scores"][i] if x["score"] != None]

        # default_scores_avg = sum(default_scores)/len(default_scores)
        # smoothed_scores_avg = sum(smoothed_scores) / len(smoothed_scores)
        # raw_scores_avg = sum(raw_scores) / len(raw_scores)

        default_scores_avg = max(default_scores)
        smoothed_scores_avg = max(smoothed_scores)
        raw_scores_avg = max(raw_scores)


        for j in range(0, len(filtered_results["default_scores"][i])):
            row = [datetime.datetime.fromtimestamp(filtered_results["default_scores"][i][j]["date"]).isoformat().split("T")[0], filtered_results["default_scores"][i][j]["score"]]

            if filtered_results["default_scores"][i][j]["score"] != None:
                row.append(round(((filtered_results["default_scores"][i][j]["score"]/default_scores_avg)*10)))
            else:
                row.append(None)
            row.append(filtered_results["smoothed_scores"][i][j]["score"])

            if filtered_results["smoothed_scores"][i][j]["score"] != None:
                row.append(round(((filtered_results["smoothed_scores"][i][j]["score"]/smoothed_scores_avg)*10)))
            else:
                row.append(None)

            if filtered_results["raw_scores"][i][j]["score"] != None:
                v =  round(filtered_results["raw_scores"][i][j]["score"]/filtered_results["raw_scores"][i][j]["amount"],2)
                row.append(v)
                row.append(round(((v / raw_scores_avg)*10)))
            else:
                row.append(None)
                row.append(None)
            row.append(filtered_results["raw_scores"][i][j]["amount"])
            writer.writerow(row)