import KeenCorpReporter

"""Worker function to run the Reporter module which uses KeenCorpReporter to request data from the KeenCorp API and
write a number of JSON files for further inspection, the module is initialized with the default KeenCorp credentials as
an example. 
"""

credentials = {
   "api_access": {"username": "enron@enron_alt", "password": "k33nc0rp"},
   "advanced_stats": True,
 }

# Example call to run with standard parameters
# kcr = KeenCorpReporter.KeenCorpReporter(credentials)
# kcr.generate()

# credentials = {
#    "api_access": {"username": "keencorp@keencorp", "password": "k33nc0rp"},
#    "advanced_stats": True,
#    "no_smoothing": True,
#     "external_smoothing": True
# }
# #
# # Example call to run with external smoothing and a defined from and to date
kcr = KeenCorpReporter.KeenCorpReporter(credentials)
kcr.generate(start_date="1990-01-01T00:00:00", to_date="2018-06-01T00:00:00")

# credentials = {
#    "api_access": {"username": "keencorp@keencorp", "password": "k33nc0rp"},
#    "advanced_stats": False,
#    }
#
# Example call to run with a pre-defined report-config, please make sure the first item of the list is unique (it's used
# for naming)
# kcr = KeenCorpReporter.KeenCorpReporter(credentials)
# report_config = [
#     ['Gender:F','Gender:M','All'],
#     ['Age:<40', 'Age:>40', 'All']
# ]
# kcr.generate(report_config=report_config)
