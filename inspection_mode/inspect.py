import csv
import datetime
import os
import sys

sys.path.insert(0, os.path.abspath(".."))
import core.keencorp_api
import core.keencorp_func

api = core.keencorp_api.keencorp_api("admin@test_organization", "k33nc0rp", "https://api.keencorp.com")
counter = 0

print "This process processes the Enron dataset email for email and is expected to take a very long time, for " \
      "specific analyses please adapt the source file (enron_messages.tsv)."

with open("enron_messages_processed.tsv", "wb") as wf:
    writer = csv.writer(wf, delimiter="\t", quotechar='"')
    writer.writerow(["message_id",
                     "date",
                     "from_address",
                     "original_body",
                     "preprocessed_body",
                     "detected_lang",
                     "analysed_body",
                     "score",
                     "diagnostics"
                     ])

    with open("D:\Projects\enron\enron_messages.tsv","rU") as rf:
        reader = csv.reader(rf, delimiter='\t')
        for row in reader:
            if counter == 10000:
                print "Processed: " + str(counter) + " messages"
                break
            if len(row) > 3:
                if "@enron" in row[2]:
                    try:
                        msg = core.keencorp_func.force_to_unicode(row[4])
                        # msg = core.keencorp_func.removeHTML(msg)
                        msg = core.keencorp_func.removeForwards(msg)

                        for i in ['&nbsp;','&amp;','&quot;',"\n","\r","\t","&","=20"]:
                            msg = msg.replace(i, " ")
                        for i in "~`@#$%^&*()_+-={}[]:\"\\|<>/\n\r\t":
                            msg = msg.replace(i, "")
                        while '  ' in msg:
                            msg = msg.replace('  ', ' ')

                        msg = msg.replace("01,","'")
                        msg = core.keencorp_func.removeSignature(msg)
                        msg = msg.strip()
                        if len(msg) > 20:

                            dt = datetime.datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S")
                            ms_gram = {
                                "message": {
                                    "timestamp": core.keencorp_func.timeToEpoch(dt),
                                    "ner": False,
                                    "body": msg
                                }
                            }

                            lang = api.detect_language(ms_gram["message"])
                            if lang["language_iso"] == "eng":
                                ms_gram["message"]["language_iso"] = lang["language_iso"]
                                ner = api.anonimize_message(ms_gram["message"])
                                if "body" in ner:
                                    ms_gram["message"]["ner"] = True
                                    ms_gram["message"]["body"] = ner["body"]
                                    ms_gram["message"]["diagnostics"] = True
                                    score = api.calculate_score(ms_gram["message"])

                                    writer.writerow([row[0],
                                                     row[1],
                                                     row[2],
                                                     row[4],
                                                     msg,
                                                     lang["language_iso"],
                                                     str(ner["body"]),
                                                     score["score"],
                                                     score["diagnostics"]
                                                     ])
                                    counter += 1

                    except Exception, e:
                        print "Processing of email message failed: " + str(e)
                        continue
                    # raw_input("press enter to continue..")