# -*- coding: utf-8 -*-
from __future__ import division

import cPickle
import datetime
import json
import logging
import os
import sys
import time

sys.path.insert(0, os.path.abspath(".."))
import core.keencorp_func
import core.keencorp_api


"""KeenCorpUploader class for sending data to the KeenCorp API.
 
Example:
kcu = KeenCorpUploader.KeenCorpUploader(credentials)
kcu.process()

"""

class KeenCorpUploader:
    """The KeenCorpUploader class upload messages to the KeenCorp API.

    """

    def __init__(self, identity, credentials):
        """Initialization of the class with passed credentials.

        Args:
            identity (str): A folder name from where to read basic configuration.
            credentials (dict): a dictionary holding "connector" with a parameters and "uploader" with parameters.
        """

        self.identity = identity
        default_last_check = "2018-01-01T00:00:00"
        storage_path = os.path.join('data_files', identity)

        if os.path.exists(storage_path):

            self.log_file = os.path.join(storage_path, 'worker.log')
            organization_data = os.path.join(storage_path, 'Checked_Wide_organization_data.xlsx')
            self.last_check_storage = os.path.join(storage_path, 'last_check.dump')
            self.report_stats = os.path.join(storage_path, 'report_stats.json')
            self.credentials = credentials

        else:
            raise Exception("Identity not found, please provide valid identity")

        if os.path.isfile(organization_data):
            self.group_listing = core.keencorp_func.read_xlsx(organization_data)

            if os.path.isfile(self.last_check_storage):
                with open(self.last_check_storage, "rb") as rf:
                    self.last_check_store = cPickle.load(rf)
            else:
                print "No storage found, using default starting date"
                self.last_check_store = {}
                for p in self.group_listing:
                    self.last_check_store[p] = default_last_check

        else:
            raise Exception("ERROR: Organization data could not be found/processed")

        self.uploader = core.keen_uploader.initialize(self.credentials["uploader"]["username"], self.credentials["uploader"]["password"], nr_uploaders=5)

    def process(self):
        """Start the upload procedure.

        Returns:
            report (dict): A dictionary with reporting info.
        """

        logging.basicConfig(format='%(asctime)s %(message)s', filename=self.log_file, level=logging.INFO)
        logging.info("Starting new cycle for identity: "+str(self.identity))
        logging.info("Attempting to process: "+str(len(self.group_listing.keys())) + " mailboxes")
        logging.info("Using connector type: "+str(self.credentials["connector"]["type"]))

        module = __import__(self.credentials["connector"]["type"])
        my_class = getattr(module, self.credentials["connector"]["type"])
        oa = my_class(self.credentials["connector"]["parameters"]["username"], self.credentials["connector"]["parameters"]["password"])

        log = {
            "overall": {
                "successful_accessed": 0,
                "unsuccessful_accessed": 0,
                "total": len(self.group_listing.keys())
            },
            "email_total": 0,
            "clusters": {}
        }
        local_log_object = {}

        m_counter = 0

        for linked_account in self.group_listing:
            m_counter += 1
            m_results = []

            print "Processing mailbox: " + str(linked_account) + " : " + str(m_counter) + "/" + str(len(self.group_listing.keys()))

            try:
                get_linked_message_status, get_linked_message, results, last_check = \
                    oa.get_messages_linked_mailbox(
                        linked_account, self.last_check_store[linked_account])
                if get_linked_message_status:
                    self.last_check_store[linked_account] = last_check.isoformat()
                    log["overall"]["successful_accessed"] += 1
                else:
                    log["overall"]["unsuccessful_accessed"] += 1
                    logging.info(
                        "ERROR processing of linked mailbox: " + linked_account + ": " + str(get_linked_message))

            except Exception, e:
                logging.info("ERROR processing of linked mailbox: " + linked_account + ": " + str(e) +
                             " retrying..")
                time.sleep(20)

                try:
                    get_linked_message_status, get_linked_message, results, last_check = \
                        oa.get_messages_linked_mailbox(
                            linked_account, self.last_check_store[linked_account])
                    if get_linked_message_status:
                        self.last_check_store[linked_account] = last_check.isoformat()
                        log["overall"]["successful_accessed"] += 1
                    else:
                        log["overall"]["unsuccessful_accessed"] += 1
                        logging.info("ERROR processing of linked mailbox: " + linked_account + ": " + str(get_linked_message))
                    m_results += results

                except Exception, e:
                    logging.info(
                        "ERROR processing of linked mailbox: " + linked_account + ": " + str(e))
                    log["overall"]["unsuccessful_accessed"] += 1
                    results = []
                    continue

            print "Collecting done, processing: " + str(len(results)) + " internal email messages"
            logging.info("Collecting done, found: " + str(len(results)) + " messages for mailbox: "+str(linked_account))
            for cluster in self.group_listing[linked_account]:
                if not cluster in local_log_object:
                    local_log_object[cluster] = {"total_messages_returned_from_api": 0, "error": {}}
                local_log_object[cluster]["total_messages_returned_from_api"] += len(results)

            for item in results:
                try:
                    msg = core.keencorp_func.force_to_unicode(item["Body"]["Content"])
                    msg = core.keencorp_func.removeForwards(core.keencorp_func.removeHTML(msg))
                    msg = msg.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').replace('&nbsp;',' ').replace('&amp;', ' ').replace('&quot;', ' ')
                    while '  ' in msg:
                        msg = msg.replace('  ', ' ')
                    msg = core.keencorp_func.removeSignature(msg)
                    msg = msg.strip()
                    if len(msg) > 20:
                        dt = datetime.datetime.strptime(item["ReceivedDateTime"].split("Z")[0], "%Y-%m-%dT%H:%M:%S")
                        ms_gram = {
                            "message": {
                                "timestamp": core.keencorp_func.timeToEpoch(dt),
                                "ner": False,
                                "body": msg.encode('ascii', 'ignore')
                            },
                            "identity": {
                                "labels": ['All'] + self.group_listing[linked_account]
                            }
                        }

                        core.keen_uploader.uploadMessage(ms_gram)
                        log["email_total"] += 1
                    else:
                        for cluster in self.group_listing[linked_account]:
                            if not "below size threshold" in local_log_object[cluster]["error"]:
                                local_log_object[cluster]["error"]["below size threshold"] = 0
                            local_log_object[cluster]["error"]["below size threshold"] += 1

                except Exception, e:
                    print "Processing of email message failed: " + str(e)
                    for cluster in self.group_listing[linked_account]:
                        if not str(e) in local_log_object[cluster]["error"]:
                            local_log_object[cluster]["error"][str(e)] = 0
                        local_log_object[cluster]["error"][str(e)] += 1
                    continue

        logging.info("Collecting email done, found: " + str(log["email_total"]) + " new messages, processed " + str(log["overall"]["successful_accessed"]) +
                     " mailboxes, found: "+str(log["overall"]["unsuccessful_accessed"]) + " errors.")

        report = core.keen_uploader.finalize()
        for cluster in local_log_object:
            if cluster in report:
                report[cluster]["error"].update(local_log_object[cluster]["error"])
                report[cluster]["total_messages_returned_from_api"] = local_log_object[cluster]["total_messages_returned_from_api"]
            else:
                report[cluster] = local_log_object[cluster]

        if self.last_check_store != {}:
            with open(self.last_check_storage, "wb") as wf:
                cPickle.dump(self.last_check_store, wf)
        with open(self.report_stats, "ab") as wf:
            wf.write(json.dumps(report)+"\n")
            
        return report
