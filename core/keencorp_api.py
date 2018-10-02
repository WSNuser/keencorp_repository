import json
import urllib
import urllib2

class keencorp_api:

    def __init__(self, username, password, api_endpoint="https://api.keencorp.com", context=None):
        self.api_endpoint = api_endpoint
        self.username = username
        self.password = password
        self.context = context
        self.session_id = None
        self.version = 1.3

    def __communicate(self, function, json_data):
        handler = urllib2.HTTPHandler()
        opener = urllib2.build_opener(handler)
        data = urllib.urlencode({"request": json.dumps(json_data)})
        req = urllib2.Request(self.api_endpoint+"/"+function , data=data)
        req.add_header('Content-Type', 'application/json')

        try:
            data = json.loads(opener.open(req).read())
            if ("success" in data) and (data["success"]):
                del data["success"]
                if ("session_id" in data) and (not (function=="login")):
                    del data["session_id"]
                return data
            else:
                if "description" in data:
                    print "API call error:", data["description"]
                else:
                    print "General API call error."
                if "log in" in data["description"]:
                    return None
                else:
                    return data
        except Exception, e:
            print "Fatal API call error: communication with API failed:",e
            return None

    def __callAPI(self, function, json_data):
        if self.session_id == None:
            auth_info = self.__communicate("login", {"username": self.username, "password": self.password, "context": self.context})
            if auth_info!=None:
                self.session_id = auth_info["session_id"]
            else:
                raise Exception('Authentication failed', 'Invalid credentials')

        json_data["session_id"] = self.session_id

        data = self.__communicate(function, json_data)
        if data==None:
            self.session_id = None
            return self.__callAPI(function, json_data)
        else:
            return data

    def detect_language(self, message):
        return self.__callAPI("detect_language", message)

    def anonimize_message(self, message):
        return self.__callAPI("anonimize_message", message)

    def anonimize_identity(self, identity):
        return self.__callAPI("anonimize_identity", identity)

    def calculate_score(self, message):
        return self.__callAPI("calculate_score", message)

    def store_score(self, item):
        return self.__callAPI("store_score", item)

    def process_message(self, item):
        return self.__callAPI("process_message", item)

    def remove_annotation(self, item):
        return self.__callAPI("remove_annotation", item)

    def request_scores(self, groups, from_epoch, to_epoch, supergroups=None, no_smoothing=False):
        if supergroups==None:
            return self.__callAPI("request_scores", {"groups": groups, "from": from_epoch, "to": to_epoch, "no_smoothing": no_smoothing})
        else:
            return self.__callAPI("request_scores", {"groups": groups, "from": from_epoch, "to": to_epoch, "supergroups": supergroups, "no_smoothing": no_smoothing})

    def request_scored_groups(self):
        return self.__callAPI("request_scored_groups", {})

    def update_supergroups(self, organization, supergroups):
        return self.__callAPI("update_supergroups", {"organization": organization, "supergroups": supergroups})

    def request_super_groups(self):
        return self.__callAPI("request_supergroups", {})
