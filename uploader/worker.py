import KeenCorpUploader

credentials = {
 "connector": {"type": "Office365API",
                   "parameters": {
                       "username": "",
                       "password": ""
                   }
                   },
     "uploader": {"username": "uploader@keencorp", "password": ""},
 }
kcw = KeenCorpUploader.KeenCorpUploader('keencorp', credentials)
print kcw.process()
