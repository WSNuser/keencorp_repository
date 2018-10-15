import csv
import datetime
import os
import sys

sys.path.insert(0, os.path.abspath(".."))
import core.keencorp_api

api = core.keencorp_api.keencorp_api("admin@enron_ind", "k33nc0rp", "https://api.keencorp.com")

counter = 0
with open("/media/mark/DataDisk/Projects/datasets/Enron/enron.csv", "rb") as rf:
    reader = csv.reader(rf, delimiter=',', quotechar='"')
    for row in reader:
        dt = row[1]
        sender = row[2]
        if "@enron" in sender.lower():
            cont = row[3]
            try:
                msg = core.keencorp_func.force_to_unicode(cont)
                # msg = core.keencorp_func.removeForwards(keencorp_func.removeHTML(msg))
                msg = core.keencorp_func.removeHTML(msg)
                remove_char = "~`@#$%^&*()_+-={}[]:\"\\|<>/\n\r\t"
                for i in remove_char:
                    msg = msg.replace(i, "")
                msg = msg.replace('&nbsp;', ' ').replace('&amp;', ' ').replace('&quot;', ' ')
                while '  ' in msg:
                    msg = msg.replace('  ', ' ')
                # msg = core.keencorp_func.removeSignature(msg)
                msg = msg.strip()
                if len(msg) > 20:

                    print msg.encode("utf-8")

                    dt = datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
                    ms_gram = {
                        "message": {
                            "timestamp": core.keencorp_func.timeToEpoch(dt),
                            "ner": False,
                            "body": msg
                        }
                    }

                    lang = api.detect_language(ms_gram["message"])
                    ms_gram["message"]["language_iso"] = lang["language_iso"]

                    ner = api.anonimize_message(ms_gram["message"])
                    ms_gram["message"]["ner"] = True
                    ms_gram["message"]["body"] = ner["body"]
                    ms_gram["message"]["diagnostics"] = True

                    score = api.calculate_score(ms_gram["message"])
                    print score
                    raw_input("press enter to continue...")


            except Exception, e:
                print "Processing of email message failed: " + str(e)
                continue