from config import DB_USERNAME, DB_PASSWORD, DB_HOST, DB_NAME, Root_Path, Area_Dict, Whole_List, Daily_FolderPath
from server.define.daily_DB import DailyDB
from server.prophet.parameter import W_Parameter_Dict, R_Parameter_Dict
from server.prophet.prophet_code import MyProphet

DailyDB = DailyDB(DB_USERNAME, DB_HOST, DB_PASSWORD, DB_NAME, Area_Dict, Whole_List, Daily_FolderPath)

MyProphet = MyProphet(DB_USERNAME, DB_HOST, DB_PASSWORD, DB_NAME, W_Parameter_Dict, R_Parameter_Dict, Root_Path)

Daily_Check = DailyDB.DailyData()
print(Daily_Check)

Daily_Wholesale = MyProphet.Wholesale()
print(Daily_Wholesale)
Daily_Retail = MyProphet.Retail()
print(Daily_Retail)
