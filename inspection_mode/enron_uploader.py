import csv
import datetime
import os
import sys

sys.path.insert(0, os.path.abspath(".."))
import core.keencorp_func
import core.keen_uploader

uploader = core.keen_uploader.initialize("admin@test_organization", "k33nc0rp", nr_uploaders=15)

with open("D:\Projects\enron\enron_messages.tsv","rU") as rf:
    reader = csv.reader(rf, delimiter='\t')
    for row in reader:
        if len(row) > 3:
            if "@enron" in row[2]:
                try:
                    msg = core.keencorp_func.force_to_unicode(row[4])
                    msg = core.keencorp_func.removeHTML(msg)
                    msg = core.keencorp_func.removeForwards(msg)

                    msg = msg.replace('&nbsp;', ' ').replace('&amp;', ' ').replace('&quot;', ' ')
                    while '  ' in msg:
                        msg = msg.replace('  ', ' ')
                    msg = core.keencorp_func.removeSignature(msg)
                    msg = msg.strip()
                    if len(msg) > 20:

                        dt = datetime.datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S")
                        ms_gram = {
                            "message": {
                                "timestamp": core.keencorp_func.timeToEpoch(dt),
                                "ner": False,
                                "body": msg
                            },
                            "identity": {
                                "labels": ['All'] + ["MailAddress:"+row[2]]
                            }
                        }
                        # print ms_gram
                        core.keen_uploader.uploadMessage(ms_gram)

                except Exception, e:
                    print "Processing of email message failed: " + str(e)
                    continue

report = core.keen_uploader.finalize()
print report