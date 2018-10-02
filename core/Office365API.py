# -*- coding: utf-8 -*-
from __future__ import division

"""office365api class for making request to the MS Office365 mail API.
(https://msdn.microsoft.com/en-us/office/office365/api/mail-rest-operations)

The class is called with login credentials and is able to retrieve messages and move messages. Office365 api allows
access to Exchange Online | Office 365 | Hotmail.com | Live.com | MSN.com | Outlook.com | Passport.com.

Example:
    oa = Office365(mmooij@keencorp.com, "myPasswWord")
    messages = oa.getMessages()

"""

import json
import urlparse
import datetime
import base64
import requests


class Office365API:
    """The office365 api class allows various operations through the office365api.

    """

    def __init__(self, login, password):
        """Initialization of the class with Office365 login and password.

        Args:
            login (str): microsoft account login.
             password (str): account password.
        """

        self.conn = requests.Session()

        self.conn.headers = {
            'Authorization': 'Basic ' + base64.b64encode(login + ":" + password),
            'Content-Type': 'application/json'
        }

        #: Set the version of the office365 api to be used.
        # version = "v1.0"
        version = "beta"

        self.base_link = "https://outlook.office365.com/api/" + version + "/me"

        #: List of selected parameters used in the getMessage method.
        self.messageSelect = [

            u'From',
            u'BccRecipients',
            u'Body',
            u'CcRecipients',
            u'Sender',
            u'ReceivedDateTime',
            u'ToRecipients',
            # u'Id',
            # u'Subject'
        ]

    def get_messages_linked_mailbox(self, account, last_check="1980-01-01T00:00:00"):
        """Method for iteratively requesting all messages from defined date for a shared mailbox.

        Args:
            account (str): email address of the linked account (access should be granted).
            groups (list): List of groups the sending users is a part of.
            last_check (Optional[str]): String of the last checked datetime, please note that this should be a string in
            the following format: "Y-%m-%dT%H:%M:%S", when not provided Unix Epoch is used.

        Returns:
            status (bool): True if successful, False otherwise.
            message (str): Error message or 'Process completed successfully'.
            total_results (int): The total number of processed messages.
            last_check (str): String of the last checked datetime.
        """

        message = "Process completed successfully"
        total_results = 0
        status = True

        try:
            last_check = datetime.datetime.strptime(last_check, "%Y-%m-%dT%H:%M:%S")
            request_dt = last_check
        except Exception, e:
            status = False
            return status, "Could not convert argument last_check to datetime: " + str(e), total_results, last_check

        #: Compose request.
        body = {
            "$select": ",".join(self.messageSelect),
            "$filter": "SentDateTime ge " + last_check.isoformat() + "Z",
            "$top": 250
        }
        results = []

        #: Iterate while pagination results are available.
        while body != {}:

            response = self.conn.get(url=self.base_link.replace("me", "users") + "/" + account + "/messages/?",
                                     params=body)

            if response.status_code is 200:
                try:
                    json_reply = json.loads(response.text)

                    if "@odata.nextLink" in json_reply:
                        #: If pagination results are available set next link to process.
                        next_link = urlparse.urlparse(json_reply["@odata.nextLink"])
                        body = urlparse.parse_qs(next_link.query)
                    else:
                        #: End of loop.
                        body = {}

                    #: Iterate over received email items.
                    for item in json_reply["value"]:

                        receivers = []
                        try:
                            for r in item["ToRecipients"]:
                                receivers.append(r["EmailAddress"]["Address"])
                            for r in item["CcRecipients"]:
                                receivers.append(r["EmailAddress"]["Address"])
                            for r in item["BccRecipients"]:
                                receivers.append(r["EmailAddress"]["Address"])
                        except Exception, e:
                            continue
                        try:
                            # Only internal mail
                            if account.split("@")[1] in ",".join(receivers) and \
                                    item["Sender"]["EmailAddress"]["Address"] in account:
                                total_results += 1

                                #: Set new last_check
                                item_datetime = item["ReceivedDateTime"].split("Z")[0]

                                if datetime.datetime.strptime(item_datetime, "%Y-%m-%dT%H:%M:%S") > last_check:
                                    last_check = datetime.datetime.strptime(item_datetime, "%Y-%m-%dT%H:%M:%S")

                                #: Append email item to result list.
                                if datetime.datetime.strptime(item_datetime, "%Y-%m-%dT%H:%M:%S") > request_dt:
                                    results.append(item)

                        except Exception, e:
                            continue

                except Exception, e:
                    print "Error interpreting JSON: " + str(e)
                    body = {}

            else:
                body = {}
                status = False
                message = "Error processing request: " + str(body) + ", HTTP_code was: " + str(response.status_code) + \
                          ", Response was: " + str(response.text)

        self.conn.close()
        return status, message, results, last_check
