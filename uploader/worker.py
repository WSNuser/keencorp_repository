import KeenCorpUploader

# credentials = {
#  "connector": {"type": "Office365API",
#                    "parameters": {
#                        "username": "",
#                        "password": ""
#                    }
#                    },
#      "uploader": {"username": "uploader@keencorp", "password": ""},
#  }
# kcw = KeenCorpUploader.KeenCorpUploader('keencorp', credentials)
# print kcw.process()



credentials = {
 "connector": {"type": "file",
                   "parameters": {
                       "filename": "D:\Projects\enron\enron_messages.tsv"
                   }
                   },
     "uploader": {"username": "admin@enron_exp", "password": "k33nc0rp"},
 }
kcw = KeenCorpUploader.KeenCorpUploader('enron', credentials)
print kcw.process()
