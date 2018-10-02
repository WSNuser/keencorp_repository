# -*- coding: utf-8 -*-
from __future__ import division
import os
import sys
import datetime
import json

sys.path.insert(0, os.path.abspath(".."))
import core.keencorp_func
import core.keencorp_api

"""The procedure starts the steps necessary to 

"""

class KeenCorpReporter:

    def __init__(self, credentials):

        # Global variables
        self.credentials = credentials
        self.identity = self.credentials["api_access"]["username"].split("@")[1]
        self.api = core.keencorp_api.keencorp_api(self.credentials["api_access"]["username"], self.credentials["api_access"]["password"], "https://api.keencorp.com")
        if "no_smoothing" in self.credentials:
            self.no_smoothing = self.credentials["no_smoothing"]
        else:
            self.no_smoothing = False
        if "external_smoothing" in self.credentials:
            self.external_smoothing = self.credentials["external_smoothing"]
        else:
            self.external_smoothing = False

    def generate(self, start_date="2018-01-01T00:00:00", to_date=datetime.datetime.now().isoformat().split(".")[0], supergroups=None, report_config=None):

        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S")
        to_date = datetime.datetime.strptime(to_date, "%Y-%m-%dT%H:%M:%S")

        if report_config == None and supergroups == None:
            supergroups = self.api.request_super_groups()
            clusters = {}
            report_config = []
            for sg in supergroups["supergroups"].keys():
                if not sg.split(":")[0] in clusters:
                    clusters[sg.split(":")[0]] = []
                clusters[sg.split(":")[0]].append(sg)
            for i in sorted(clusters.keys()):
                report_config.append(sorted(clusters[i]))

            if self.external_smoothing:
                results = self.api.request_smoothed_scores(supergroups["supergroups"], core.keencorp_func.timeToEpoch(start_date), core.keencorp_func.timeToEpoch(to_date))
            else:
                results = self.api.request_scores(supergroups["supergroups"],
                                                  core.keencorp_func.timeToEpoch(start_date),
                                                  core.keencorp_func.timeToEpoch(to_date), no_smoothing=self.no_smoothing)
        stats = {
            "overall_messages_processed": 0,
            "clusters": {}
        }

        for i in report_config:
            for group in i:
                stats["clusters"][group] = {"total_messages": 0,
                                                 "details": {"total_counted": 0}}

        # Create Standard
        result = {
            "account_name": self.identity,
            "description": "Automatically generated report for: " + str(self.identity) + " from: " +
                           start_date.isoformat().split("T")[0] + " to: "
                           + to_date.isoformat().split("T")[0] + "<br /> Report generated at: " +
                           datetime.datetime.now().isoformat().split("T")[0],
            "moodmetrix": [],
            "heatmap": []
        }

        for config in report_config:
            this_mm = {
                "data": {"amounts": {}, "ebi": {}, "comments": {}},
                "options": {},
                "description": "Showing Moodmetrix for cluster: " + str(config[0].split(":")[0] + "<br /> Amount stats:")}

            for group in config:

                this_mm["data"]["amounts"][group] = []
                this_mm["data"]["ebi"][group] = []
                stats["clusters"][group]["details"] = {"total_counted": 0}

                if group in results["scores"]:
                    for date in results["scores"][group]:

                        stats["clusters"][group]["details"]["total_counted"] += date["amount"]
                        dt = datetime.datetime.fromtimestamp(date["date"])

                        if not "Y"+str(dt.year) in stats["clusters"][group]["details"]:
                            stats["clusters"][group]["details"]["Y"+str(dt.year)] = 0
                        if not "M"+str(dt.month) in stats["clusters"][group]["details"]:
                            stats["clusters"][group]["details"]["M" + str(dt.month)] = 0
                        if not "W"+str(datetime.date(dt.year, dt.month, dt.day).isocalendar()[1]) in stats["clusters"][group]["details"]:
                            stats["clusters"][group]["details"]["W"+str(datetime.date(dt.year, dt.month, dt.day).isocalendar()[1])] = 0
                        stats["clusters"][group]["details"]["Y" + str(dt.year)] += date["amount"]
                        stats["clusters"][group]["details"]["M" + str(dt.month)] += date["amount"]
                        stats["clusters"][group]["details"]["W" + str(datetime.date(dt.year, dt.month, dt.day).isocalendar()[1])] += date["amount"]

                        date_epoch_milisecond = date["date"] * 1000
                        this_mm["data"]["amounts"][group].append([date_epoch_milisecond, date["amount"]])
                        this_mm["data"]["ebi"][group].append([date_epoch_milisecond, date["score"]])

                    this_mm["description"] += "<br /><b>" + group + "</b>" + "<br />"
                    this_mm["description"] += "Year stats: <br />"
                    for i in sorted([x for x in stats["clusters"][group]["details"] if "Y" in x]):
                        this_mm["description"] += i + ": " + str(stats["clusters"][group]["details"][i]) + ", "
                    this_mm["description"] += "<br />Month stats: <br />"
                    for i in sorted([x for x in stats["clusters"][group]["details"] if "M" in x]):
                        this_mm["description"] += i + ": " + str(stats["clusters"][group]["details"][i]) + ", "
                    this_mm["description"] += "<br />Week stats: <br />"
                    for i in sorted([x for x in stats["clusters"][group]["details"] if "W" in x]):
                        this_mm["description"] += i + ": " + str(stats["clusters"][group]["details"][i]) + ", "

            result["moodmetrix"].append(this_mm)

            with open(os.path.join("json", self.identity + "_"+str(config[0].split(":")[0])+".json"), "wb") as wf:
                wf.write(json.dumps(this_mm))

        with open(os.path.join("json", self.identity + ".json"), "wb") as wf:
            wf.write(json.dumps(result))