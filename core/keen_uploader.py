# KeenCorp uploading component, (C) 2018, KeenCorp, bjakic@keencorp.com
# Use as follows:
#
# N.B: your_nr_of_uploaders, your_context and your_outfile are optional and should only be used if applicable
#
# import keen_uploader
# keen_uploader.initialize(your_username, your_password, your_nr_of_uploaders, your_context, your_outfile)
#
# << YOUR MESSAGE RETRIEVAL AND PREPARATION CODE >>
# for message in all_your_messages:
#       keen_uploader.uploadMessage( message )
#
# << YOUR RETRIEVAL IS COMPLETED >>
#
# keen_uploader.finalize()

version = 1.01

from multiprocessing import Queue
import time
import keencorp_api
import threading
import codecs, json

class uploader( threading.Thread ):
    def __init__(self, input_queue, output_queue, username, password, context):
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.api = keencorp_api.keencorp_api(username, password, "https://api.keencorp.com", context=context)
        self.die = False
        threading.Thread.__init__ ( self )

    def run(self):
        for item in iter(self.input_queue.get, 'STOP'):
            if not ("labels" in item["identity"]):
                item["identity"] = self.api.anonimize_identity(item["identity"])
            result = self.api.process_message(item)
            result["identity"] = {"labels": item["identity"]["labels"]}

            if "score" in result:
                result = {"identity": {"labels": item["identity"]["labels"]}, "message": {"timestamp":item["message"]["timestamp"], "score": result["score"]}}

            self.output_queue.put(result)

            if self.die==True:
                break

class output_dequeuer( threading.Thread ):

    def __init__(self, output_queue, uploader_control, outfile, log_object):
        self.output_queue = output_queue
        self.uploader_control = uploader_control
        self.die = False
        self.log_object = log_object

        if outfile!=None:
            self.outfile = codecs.open(outfile,"wb","utf8")
        else:
            self.outfile = None
        threading.Thread.__init__ ( self )

    def run(self):
        errors = 0
        for item in iter(self.output_queue.get, 'STOP'):
            uploader_control["output"] += 1
            for cluster in item["identity"]["labels"]:
                if not cluster in self.log_object:
                    self.log_object[cluster] = {"success": 0, "error": {}}

            if "description" in item:
                for cluster in item["identity"]["labels"]:
                    if not item["description"] in self.log_object[cluster]["error"]:
                        self.log_object[cluster]["error"][item["description"]] = 0
                    self.log_object[cluster]["error"][item["description"]] += 1
                errors += 1
                if not item["description"] in self.log_object["overall"]["error"]:
                    self.log_object["overall"]["error"][item["description"]] = 0
                self.log_object["overall"]["error"][item["description"]] += 1

            else:
                self.log_object["overall"]["success"] += 1
                for cluster in item["identity"]["labels"]:
                    self.log_object[cluster]["success"] += 1
                if self.outfile!=None:
                    self.outfile.write(json.dumps(item)+"\n")
            if self.die==True:
                break

            if uploader_control["output"] % 10000 == 0:
                print uploader_control["output"],"messages processed with",errors,"errors."

        print uploader_control["output"],"messages processed with",errors,"errors. Processing finished!"

        if self.outfile!=None:
            self.outfile.close()

uploader_control = {"uploaders": [], "input": 0, "output": 0, "nr_uploaders": 0, "max_buffer": 0}

input_queue = Queue()

output_queue = Queue()

log_object = {"overall": {"success": 0, "error": {}}}

def initialize(username, password, nr_uploaders=150, context=None, outfile=None):
    uploader_control["nr_uploaders"] = nr_uploaders
    uploader_control["max_buffer"] = nr_uploaders*4
    for n in range(nr_uploaders):
        uploader_control["uploaders"].append(uploader(input_queue, output_queue, username, password, context))
        uploader_control["uploaders"][-1].start()

    output_dequeuer(output_queue, uploader_control, outfile, log_object).start()

    print "Uploader created."

def uploadMessage(message):
    input_queue.put(message)
    uploader_control["input"] += 1
    while (uploader_control["input"] - uploader_control["output"]) > uploader_control["max_buffer"]:
        time.sleep(1)

def finalize():
    while (uploader_control["input"] - uploader_control["output"]) > 0:
            time.sleep(1)

    for n in range(uploader_control["nr_uploaders"]):
        uploader_control["uploaders"][n].die = True

    for n in range(uploader_control["nr_uploaders"]):
        input_queue.put("STOP")
    output_queue.put("STOP")

    time.sleep(3)
    print "Uploading completed."
    return log_object