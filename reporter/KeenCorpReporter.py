# -*- coding: utf-8 -*-
from __future__ import division

import datetime
import json
import os
import sys

sys.path.insert(0, os.path.abspath(".."))
import core.keencorp_func
import core.keencorp_api


"""KeenCorpReport class for making requests to the KeenCorp API and write a number of JSON files for further inspection.
 
Example:
kcr = KeenCorpReporter.KeenCorpReporter(credentials)
kcr.generate()

"""

class KeenCorpReporter:
    """The KeenCorpReporter class generates files based on passed parameters.

    """

    def __init__(self, credentials):
        """Initialization of the class with passed credentials.

        Args:
            credentials (dict): a dictionary holding "api_access" with a username and password and additional optional
             parameters.
        """

        self.credentials = credentials
        self.identity = self.credentials["api_access"]["username"].split("@")[1]
        self.api = core.keencorp_api.keencorp_api(
            self.credentials["api_access"]["username"],
            self.credentials["api_access"]["password"], "https://api.keencorp.com")

        if "no_smoothing" in self.credentials:
            self.no_smoothing = self.credentials["no_smoothing"]
        else:
            self.no_smoothing = False

        if "external_smoothing" in self.credentials:
            self.external_smoothing = self.credentials["external_smoothing"]
        else:
            self.external_smoothing = False

    def generate(self, start_date="2018-01-01T00:00:00", to_date=datetime.datetime.now().isoformat().split(".")[0], supergroups=None, report_config=None):
        """Generate the report files .

        Args:
            start_date Optional([str]): A starting date as a string in the format YYYY-MM-DDTHH:MM:SS
            to_date Optional([str]): A end date as a string in the format YYYY-MM-DDTHH:MM:SS
            supergroups (Optional([dict]): A dictionary with supergroups (not yet implemented).
            report_config Optional([list]): A list of list with supergroups which should be in a report together.
        """

        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S")
        to_date = datetime.datetime.strptime(to_date, "%Y-%m-%dT%H:%M:%S")

        supergroups = self.api.request_super_groups()

        clusters = {}
        for sg in supergroups["supergroups"].keys():
            if not sg.split(":")[0] in clusters:
                clusters[sg.split(":")[0]] = []
            clusters[sg.split(":")[0]].append(sg)

        if report_config == None:
            report_config = []
            for i in sorted(clusters.keys()):
                report_config.append(sorted(clusters[i]))
        else:
            request_supergroups = {"supergroups": {}}
            for line in report_config:
                for item in line:
                    request_supergroups["supergroups"][item] = supergroups["supergroups"][item]
            supergroups = request_supergroups

        if self.external_smoothing:
            results = {"scores": {}}
            for x in supergroups["supergroups"].keys():
                my_res = self.api.request_smoothed_scores({x: supergroups["supergroups"][x]},
                                                 core.keencorp_func.timeToEpoch(start_date),
                                                 core.keencorp_func.timeToEpoch(to_date))
                results["scores"][x] = my_res["scores"][x]

        else:
            results = {"scores": {}}
            for x in supergroups["supergroups"].keys():
                print {x: supergroups["supergroups"][x]}
                my_res = self.api.request_scores({'all':['all']},
                                                 core.keencorp_func.timeToEpoch(start_date),
                                                 core.keencorp_func.timeToEpoch(to_date),
                                                 no_smoothing=self.no_smoothing)

                results["scores"][x] = my_res["scores"][x]
                print my_res

        stats = {
            "overall_messages_processed": 0,
            "clusters": {}
        }

        for i in report_config:
            for group in i:
                stats["clusters"][group] = {"total_messages": 0,
                                                 "details": {"total_counted": 0}}

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