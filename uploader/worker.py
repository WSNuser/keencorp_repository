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

# credentials = {
#  "connector": {"type": "GMailAPI",
#                    "parameters": {
#                        "deligation": {
#                            "type": "service_account",
#                           "project_id": "server-wide-deligation",
#                           "private_key_id": "bed0a46082b5f334a655823db57bc5a93f4d3b47",
#                           "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQChZXh5J8rib7XD\nm5HtlQiATV0yl3XVJlf7ZRfhq0auBC6he+ZGblMP42fB9kO7O/Jqf6hL5FZn8tEt\nzTqEuOaW6IaMoXePxHMNHeqYH5cfEYpUh8L1xt4VpjSrqdPm6B+Of/ISBSZHNG0c\nhHXxi64j0j1yFOzmQY0DkksNw4d1AIr4sdSpz8MXksqa4+14of25orPKNmjyA4Mb\nD1bMbasz6Yt3FC9cK4ily4OjbFc/DOXRL4QACv0AIbkhGGLRdn01K/BjGlZg4WL2\nnWDkJwYx/9yVtVoQs5nRVZVlu3L9bjsn2HrYLO5Kme8KEKbSgCyIT+ftg/4+K0vw\np/Mc7btxAgMBAAECggEAAvsnUwGPp0gN8Ot+Mge3LPuA1a7jf8jiBiQzYTkzKIKu\nQ9BQjAt8oEYAhB4i2SH908bA2ooAqJHdGD36rznlFHN+DLnsxeyIfX0IeL/YoDvI\nNNB/IuAF+RtlTKhp4BF4h77IP1n1/4mx3D18GjaMxF+dP+6wA37Bdofst/fdGCWf\nZendQHAero5UlyE0kc41DKWgf/CBZS4h9Hfj8ImKGSxco87RiYHENRNndCAj06hB\nvE3dCTbPiwUgcNIfxSt+vO8npmGMLZBcxCGNbH1HHpteNtneQBb9Dhae4/mVxSu9\nUx3uINdfTdbdOXg9Az2g6GwVKpxT+RevOpv11c83+wKBgQDXg0izADoHFRvyTjdZ\nXRZY/V/SRTrhwjTCtOdjPjLRupGkfiRiSfVRhGxehzsSu+8nXpJyz/0oOFEr3IS0\n5XJixwXlXHD7uVKOt0my5LOSTZn1vYHlc70huY7BzWXgm/qSw/qeBZ8k+WLIMAAS\nCOnxmOIx+qpQwYFSmCXH8XG3lwKBgQC/t4ygK8eeeHgVNwpUPMul0tpFiWwteo+Y\naE24diAReNK1Id4Ru/fjaqB8qGLDwxJzyAgcfFN13ErnKMDPzYGjRk6GNQpOeH6U\nsrqpBOgrD4sOBz0Oec5cy5sN1p8Cn7s+4/irRy/AY+VmcAOUKE0hpv9nV4RusYBZ\ngiFtTpRGNwKBgDU3ZuFEog+Tp9X6eHJpqRYKYvnyPGr44LxfnW+FMVlWn5Yly+g1\naQ1bDMN+0xh6LcDj+ne9Yj7nQSv6hQ6CRe+cQ5lybTfLeFZjbiBtluX+oZDr3cKC\nBObqAhVbGdgPzB0npaAVtUmVB051g97wMoyE+v3qbtoIHl390f6AYVs7AoGAem5B\nA9hxdiYAqauokPryIkdw1I9Z4gEuymlxmKb2+7Fo/ftO0Yx0VWq2amUuDU357q6D\nX42VzuKLgutnlkzqyNYRN2uP1WTlkRhCU8WqbjVS2/aLaz8mJeRwdHnmuco/zX3Q\nQ7EGMZqZ2L0Xy/mgqCj5WYluLTJ1gLO1nRRdZCkCgYAGsjVSCmOAyKXop1E4eLKX\nSCuxh75vtIdcw0ZBiMFjv43NUewxBool+FOFuweKcwSbEquEgQR48s5rdjhnMFGQ\nhxAhvhdj15zyB0nxeuZgb91iTv/26y4EgkhI1JpTLqZDToLvkjIOh0h1DTOZOhn3\nhSUWTJKIU0dMvG6rqRmTNA==\n-----END PRIVATE KEY-----\n",
#                           "client_email": "keencorp@server-wide-deligation.iam.gserviceaccount.com",
#                           "client_id": "103859637496094451378",
#                           "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#                           "token_uri": "https://oauth2.googleapis.com/token",
#                           "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#                           "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/keencorp%40server-wide-deligation.iam.gserviceaccount.com"
#                         }
#                    }
#                    },
#      "uploader": {"username": "test@test_organization", "password": "k33nc0rp"},
#  }
# kcw = KeenCorpUploader.KeenCorpUploader('ai-applied', credentials)
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
