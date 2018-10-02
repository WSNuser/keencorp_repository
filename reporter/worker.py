import KeenCorpWorker
import KeenCorpReporter
import json

credentials = {
 "connector": {"type": "Office365API",
                   "parameters": {
                       "username": "mmooij@keencorp.com",
                       "password": "Fay54365"
                   }
                   },
     "uploader": {"username": "uploader@keencorp", "password": "k33nc0rp"},
 }
kcw = KeenCorpWorker.KeenCorpWorker('keencorp', credentials)
print kcw.process()

##
##d = kcw.generateONA()
##with open('keencorp_ona.json',"wb") as wf:
##    wf.write(json.dumps(d))


# del credentials
# del kcw
##
##credentials = {
##    "api_access": {"username": "mark@keencorp", "password": "h+mA2nAz"},
##    "advanced_stats": True
##}
##
##kcr = KeenCorpReporter.KeenCorpReporter('keencorp', credentials)
##kcr.generate()

##credentials = {
## "connector": {"type": "Office365API",
##                   "parameters": {
##                       "username": "svcKeenCorp_P@vwe.nl",
##                       "password": "vbgDWLfc5"
##                   }
##                   },
##     "uploader": {"username": "mark@vwe", "password": "h+mA2nAz"},
## }
##kcw = KeenCorpWorker.KeenCorpWorker('vwe', credentials)
##kcw.process()
##
##credentials = {
##    "api_access": {"username": "mark@vwe", "password": "h+mA2nAz"},
##    "advanced_stats": True
##}
##
##kcr = KeenCorpReporter.KeenCorpReporter('vwe', credentials)
##kcr.generate()

# credentials = {
#     "api_access": {"username": "mark@vwe", "password": "h+mA2nAz"},
#     "advanced_stats": True
# }
#
# kcr = KeenCorpReporter.KeenCorpReporter('vwe', credentials)
# report_config = [
#     ['All','Shared:All:Shared'],
#     ['All','Business Support:Overig','Business Support:Overig:Shared','Business Support:IT Beheer','Business Support:IT Beheer:Shared'],
#     ['All','Dienstjaren:10 of meer','Dienstjaren:1 tot minder dan 2','Dienstjaren:2 tot minder dan 5','Dienstjaren:5 tot minder dan 10','Dienstjaren:minder dan 1'],
#     ['All','Geslacht:Man','Geslacht:Vrouw'],
#     ['All','IT:Beheer','IT:Beheer:Shared','IT:Ontwikkeling'],
#     ['All','Innovatie Verbetering:Innovatie','Innovatie Verbetering:Verbetering'],
#     ['All','DSI:Non-sales'],
#     ['All','Leeftijd:20 tm 29','Leeftijd:30 tm 39','Leeftijd:40 tm 49','Leeftijd:50 tm 59'],
#     ['All','MT:MK','MT:MT'],
#     ['All','MijnVWE:Non-sales','MijnVWE:Sales','MijnVWE:Sales:Shared'],
#     ['All','Ranking:Non-performer','Ranking:Performer'],
#     ['All','Remarketing:ADAM','Remarketing:ADAM:Shared','Remarketing:HHW','Remarketing:HHW:Shared'],
#     ['All','Remarketing Klantenteam:ADAM','Remarketing Klantenteam:HHW'],
#     ['All','Salarisschaal:1 12','Salarisschaal:13 14','Salarisschaal:15 16','Salarisschaal:17'],
#     ['All','Sales KCC:KCC','Sales KCC:KCC:Shared','Sales KCC:Sales','Sales KCC Sales:Shared']
# ]
# kcr.generate(start_date="2018-01-01T00:00:00", to_date="2018-08-29T00:00:00", supergroups=[], report_config=report_config)
credentials = {
    "api_access": {"username": "mark@mizuho-retro", "password": "h+mA2nAz"},
    "advanced_stats": True
}

kcr = KeenCorpReporter.KeenCorpReporter('mizuho', credentials)
report_config = [
    ['All','Manager:Manager_No','Manager:Manager_Yes'],
    # ['All','Area:Daiba','Area:Hakusan','Area:Higashishinjuku','Area:Kitashinjuku','Area:Nakameguro','Area:Nishikasai','Area:Ohtemachi','Area:Osaka','Area:Shibuya','Area:Shinagawa','Area:Shinmachi','Area:Takagicho','Area:Takebashi','Area:Tama','Area:Uchisaiwaicho'],
    # ['All','BusinessSupport:BusinessSupport_Business_Support','BusinessSupport:BusinessSupport_Rest'],
    # ['All','Gender:Female','Gender:Male'],
    # ['All','Headdivision:BackOffice','Headdivision:Banking_Systems_Group','Headdivision:Consulting_Group','Headdivision:Enterprise_ITG','Headdivision:Group_ITG','Headdivision:Platform_Services_Group','Headdivision:Solution_Group'],
    # ['All','JobFamily:Delivery','JobFamily:Develop','JobFamily:Sales','JobFamily:Strategy','JobFamily:Support'],
    # ['All','LargeBuilding:Large_Building','LargeBuilding:Small_Building'],
    # ['All','Level:Level_1','Level:Level_2','Level:Level_3','Level:Level_4','Level:Level_5','Level:Level_6','Level:Level_7'],
    # ['All','ManagementGroup:ManagementGroup_Middle_Management','ManagementGroup:ManagementGroup_Rest','ManagementGroup:ManagementGroup_Top_Management'],
    # ['All','ManagementLevel:ManagementLevel_1','ManagementLevel:ManagementLevel_2','ManagementLevel:ManagementLevel_3','ManagementLevel:ManagementLevel_4'],
    # ['All',"Headdivision:Platform_Services_Group","Headdivision:Enterprise_ITG","Headdivision:Banking_Systems_Group","Headdivision:Consulting_Group","Headdivision:Group_ITG","Headdivision:BackOffice","Headdivision:Solution_Group"]
    # ['All','Division:Project_Risk_Examination_Division', 'Division:Group_IT_Division_1', 'Division:IT_Infrastructure_Systems_Sector_Division_4', 'Division:IT_Infrastructure_Systems_Sector_Division_3', 'Division:IT_Infrastructure_Systems_Sector_Division_2', 'Division:IT_Infrastructure_Systems_Sector_Division_1', 'Division:International_System_Division_SEIBI_Promotion_PT', 'Division:Enterprise_Division_6', 'Division:Accounting_Systems_Sector_2', 'Division:Enterprise_Division_5', 'Division:Enterprise_Division_4', 'Division:Group_IT_Division_3', 'Division:Group_IT_Division_2', 'Division:Enterprise_Division_1', 'Division:Group_IT_Division_4', 'Division:Enterprise_Division_3', 'Division:Enterprise_Division_2', 'Division:Banking_System_Quality_Management_Division', 'Division:Settlement_and_Channel_Systems_Sector_Division_1', 'Division:Environment_and_Energy_Division_2', 'Division:Information_and_Communication_Research_Division', 'Division:Environment_and_Energy_Division_1', 'Division:Platform_Services_Business_Promotion_Division', 'Division:Solution_Business_Division', 'Division:Information_Systems_Sector_Division_1', 'Division:Information_Systems_Sector_Division_2', 'Division:Information_Systems_Sector_Division_3', 'Division:Platform_Services_Division_3', 'Division:Platform_Services_Division_2', 'Division:Platform_Services_Division_1', 'Division:Consulting_Business_Promotion_Division', 'Division:Project_Team_for_Promoting_Cross-sectional_Development_of_the_Banking_Systems', 'Division:Internal_Audit_Division', 'Division:Risk_Management_Division', 'Division:Business_Process_Improvement_Division', 'Division:Banking_System_Business_Administration_Division', 'Division:Human_Resources_Division', 'Division:Data_Processing_Office', 'Division:Enterprises_Business_Promotion_Division', 'Division:Card_Business_Division', 'Division:Procurement_Management_Division', 'Division:Corporate_Planning_Division', 'Division:Settlement_and_Channel_Systems_Sector_Division_4', 'Division:Settlement_and_Channel_Systems_Sector_Division_2', 'Division:Settlement_and_Channel_Systems_Sector_Division_3', 'Division:Innovation_&_Strategy_Division', 'Division:Science_Solutions_Division', 'Division:Accounting_Systems_Sector_1_Division_2', 'Division:Accounting_Systems_Sector_1_Division_3', 'Division:Accounting_Systems_Sector_1_Division_1', 'Division:Accounting_Systems_Sector_1_Division_4', 'Division:Accounting_Systems_Sector_1_Division_5', 'Division:Management_&_IT_Consulting_Division', 'Division:Business_Management_Division', 'Division:Global_Systems_Sector_Division_2', 'Division:Global_Systems_Sector_Division_3', 'Division:Global_Systems_Sector_Division_1', 'Division:Solution_Division_3', 'Division:Solution_Division_2', 'Division:Solution_Division_1', 'Division:Solution_Division_5', 'Division:Solution_Division_4', 'Division:Group_Coordination_Division', 'Division:Accounting_Systems_Sector_2_Division_3', 'Division:Accounting_Systems_Sector_2_Division_2', 'Division:Accounting_Systems_Sector_2_Division_1', 'Division:Accounting_Systems_Sector_2_Division_4', 'Division:Advanced_Financial_Technology_Division', 'Division:Advanced_Information_Techonologies_Division', 'Division:Social_Policy_Consulting_Division', 'Division:Operations_and_IT_Administration_Division', 'Division:Market_and_Risk_Management_Systems_Sector_Division_1', 'Division:Market_and_Risk_Management_Systems_Sector_Division_3', 'Division:Market_and_Risk_Management_Systems_Sector_Division_2', 'Division:Market_and_Risk_Management_Systems_Sector_Division_4'],
    # ['All','Sales:Sales_Rest', 'Sales:Sales_Sales'],
    # ['All','Develop_Develop:Develop_Develop', 'Develop_Develop:Develop_Rest']
]
#
kcr.generate(start_date="2018-01-09T00:00:00", to_date="2018-04-30T00:00:00", supergroups=[], report_config=report_config)
