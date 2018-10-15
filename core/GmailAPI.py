# -*- coding: utf-8 -*-
from __future__ import division

"""gmailapi class for making request to the Google GMail API.

The class is called with a server-wide deligation file and allows access to GMail accounts.

Example:
    gm = GMailAPI(<CONTENTS OF DELIAGTION FILE>)
    messages = oa.getMessages()

"""

import datetime
import base64
import email
import time
import httplib2
import sys
import os
from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.http import BatchHttpRequest

sys.path.insert(0, os.path.abspath(".."))
import core.parsemail

class GMailAPI:
    """The GMail api class allows various operations through the GMail API.

    """

    def __init__(self, deligation):
        """Initialization of the class with the content of a deligation file.

        Args:
            deligation (dict): JSON dictionary.
        """

        SCOPES = [
            'https://www.googleapis.com/auth/gmail.readonly',
        ]

        self.credentials = ServiceAccountCredentials.from_json_keyfile_dict(deligation, SCOPES)
        self.results = []
        self.last_check = ""
        self.account = ""

    def getMessages(self):
        """Helper function to return the gathered results

        Returns:
            results (list): A list of results
        """

        return self.results

    def list_messages(self, service, user, query=''):
        messages = []
        try:
            response = service.users().messages().list(userId=user, q=query).execute()
            messages = response['messages']

            while 'nextPageToken' in response:
                page_token = response['nextPageToken']
                response = service.users().messages().list(userId=user, q=query,
                                                           pageToken=page_token).execute()
                messages.extend(response['messages'])

            return messages
        except Exception, error:
            print 'An error occurred: %s' % error
            return messages

    def add_to_results(self, request, response, exception):
        if response:
            dt = time.mktime(self.last_check.timetuple())
            if int(dt * 1000) < int(response["internalDate"]):
                msg_str = base64.urlsafe_b64decode(response['raw'].encode('ASCII'))
                msg = email.message_from_string(msg_str)

                subject = core.parsemail.getmailheader(msg.get('Subject', ''))
                from_ = core.parsemail.getmailaddresses(msg, 'from')
                from_ = ('', '') if not from_ else from_[0]
                tos = core.parsemail.getmailaddresses(msg, 'to')
                # print tos
                # cc = parsemail.getmailaddresses(msg, 'cc')
                # bcc = parsemail.getmailaddresses(msg, 'bcc')

                receivers = [x[1] for x in tos]

                if self.account.split("@")[1] in ",".join(receivers) and \
                        from_[1] in self.account:

                    self.results.append({
                            u'datetime': datetime.datetime.fromtimestamp(int(response["internalDate"])/1000).isoformat(),
                            u'from': from_[1],
                            u'to': [x[1] for x in tos],
                            # u'cc': [],
                            # u'bcc': [],
                            u'subject': subject,
                            u'message': str(msg),
                        })
        else:
            print "Date Error: ",response

    def get_messages_linked_mailbox(self, account, last_check="2018-10-01T00:00:00"):
        self.results = []
        self.last_check = datetime.datetime.strptime(last_check, "%Y-%m-%dT%H:%M:%S")
        self.account = account

        delegated_credentials = self.credentials.create_delegated(account)
        http = delegated_credentials.authorize(httplib2.Http())
        service = discovery.build('gmail', 'v1', http=http)

        messages = self.list_messages(service, account, "!in:chats and after:" + self.last_check.isoformat().split("T")[0])

        batch = BatchHttpRequest()
        for msg in messages:
            batch.add(service.users().messages().get(userId=account, id=msg['id'], format="raw"),
                      callback=self.add_to_results)
        batch.execute()

    # def get_messages_linked_mailbox(self, account, last_check="1980-01-01T00:00:00"):
    #     """Method for iteratively requesting all messages from defined date for a deligated mailbox.
    #
    #     Args:
    #         account (str): email address of the deligated mailbox (access should be granted).
    #         last_check (Optional[str]): String of the last checked datetime, please note that this should be a string in
    #         the following format: "Y-%m-%dT%H:%M:%S", when not provided Unix Epoch is used.
    #
    #     Returns:
    #         status (bool): True if successful, False otherwise.
    #         message (str): Error message or 'Process completed successfully'.
    #         total_results (int): The total number of processed messages.
    #         last_check (str): String of the last checked datetime.
    #     """
    #
    #     message = "Process completed successfully"
    #     total_results = 0
    #     status = True
    #
    #     try:
    #         last_check = datetime.datetime.strptime(last_check, "%Y-%m-%dT%H:%M:%S")
    #         request_dt = last_check
    #     except Exception, e:
    #         status = False
    #         return status, "Could not convert argument last_check to datetime: " + str(e), total_results, last_check
    #
    #
    #
    #     #: Compose request.
    #     body = {
    #         "$select": ",".join(self.messageSelect),
    #         "$filter": "SentDateTime ge " + last_check.isoformat() + "Z",
    #         "$top": 250
    #     }
    #     results = []
    #
    #     #: Iterate while pagination results are available.
    #     while body != {}:
    #
    #         response = self.conn.get(url=self.base_link.replace("me", "users") + "/" + account + "/messages/?",
    #                                  params=body)
    #
    #         if response.status_code is 200:
    #             try:
    #                 json_reply = json.loads(response.text)
    #
    #                 if "@odata.nextLink" in json_reply:
    #                     #: If pagination results are available set next link to process.
    #                     next_link = urlparse.urlparse(json_reply["@odata.nextLink"])
    #                     body = urlparse.parse_qs(next_link.query)
    #                 else:
    #                     #: End of loop.
    #                     body = {}
    #
    #                 #: Iterate over received email items.
    #                 for item in json_reply["value"]:
    #
    #                     receivers = []
    #                     try:
    #                         for r in item["ToRecipients"]:
    #                             receivers.append(r["EmailAddress"]["Address"])
    #                         for r in item["CcRecipients"]:
    #                             receivers.append(r["EmailAddress"]["Address"])
    #                         for r in item["BccRecipients"]:
    #                             receivers.append(r["EmailAddress"]["Address"])
    #                     except Exception, e:
    #                         continue
    #                     try:
    #                         # Only internal mail
    #                         if account.split("@")[1] in ",".join(receivers) and \
    #                                 item["Sender"]["EmailAddress"]["Address"] in account:
    #                             total_results += 1
    #
    #                             #: Set new last_check
    #                             item_datetime = item["ReceivedDateTime"].split("Z")[0]
    #
    #                             if datetime.datetime.strptime(item_datetime, "%Y-%m-%dT%H:%M:%S") > last_check:
    #                                 last_check = datetime.datetime.strptime(item_datetime, "%Y-%m-%dT%H:%M:%S")
    #
    #                             #: Append email item to result list.
    #                             if datetime.datetime.strptime(item_datetime, "%Y-%m-%dT%H:%M:%S") > request_dt:
    #                                 results.append(item)
    #
    #                     except Exception, e:
    #                         continue
    #
    #             except Exception, e:
    #                 print "Error interpreting JSON: " + str(e)
    #                 body = {}
    #
    #         else:
    #             body = {}
    #             status = False
    #             message = "Error processing request: " + str(body) + ", HTTP_code was: " + str(response.status_code) + \
    #                       ", Response was: " + str(response.text)
    #
    #     self.conn.close()
    #     return status, message, results, last_check
