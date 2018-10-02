import KeenCorpReporter

credentials = {
   "api_access": {"username": "keencorp@keencorp", "password": "k33nc0rp"},
   "advanced_stats": True,
   "no_smoothing": True,
    "external_smoothing": True
}

kcr = KeenCorpReporter.KeenCorpReporter(credentials)
kcr.generate()
