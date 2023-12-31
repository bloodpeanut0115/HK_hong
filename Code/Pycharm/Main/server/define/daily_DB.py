import json
import traceback
from datetime import datetime, timedelta
from glob import glob

import pymysql
from tqdm import tqdm


class DailyDB:
    ### init 설정
    def __init__(self, DB_USERNAME, DB_HOST, DB_PASSWORD, DB_NAME,
                 Area_Dict, Whole_List, Daily_FolderPath):
        self.DB_USERNAME = DB_USERNAME
        self.DB_HOST = DB_HOST
        self.DB_PASSWORD = DB_PASSWORD
        self.DB_NAME = DB_NAME
        self.Area_Dict = Area_Dict
        self.Whole_List = Whole_List
        self.Daily_FolderPath = Daily_FolderPath

    def DailyData(self):

        try:
            for data in tqdm(glob(self.Daily_FolderPath + "*.json"), desc='Daily DB INSERT'):
                Table = data.split('_')[-1].split('.')[0]
                day = data.split('_')[-2].split('\\')[-1]

                if Table in self.Whole_List:
                    day = (datetime.strptime(day, '%y%m%d') - timedelta(days=1)).strftime('%Y%m%d')

                    if Table == '농산물거래량':
                        table = 'wholesale_quantity'
                        name = '거래량(kg)'
                    else:
                        table = 'wholesale_price'
                        name = '가격(원/kg)'

                    db = pymysql.Connect(host=self.DB_HOST,
                                         user=self.DB_USERNAME,  # db 계정
                                         password=self.DB_PASSWORD,  # db 비밀 번호
                                         database=self.DB_NAME)  # 접속 하고자 하는 db 명
                    ## DB 작업
                    with db:
                        with db.cursor() as cur:
                            cur.execute("SELECT * FROM {} WHERE date = {}".format(table, str(day)))
                            if not cur.fetchall():
                                with open(data, 'r', encoding='utf-8') as f:
                                    Data_Json = json.load(f)
                                cur.execute("SHOW columns FROM {}".format(table))

                                col_Text = ''
                                for cnt, column in enumerate(cur.fetchall()):
                                    if cnt == 0:
                                        col_Text += column[0]
                                    else:
                                        col_Text = col_Text + "," + column[0]

                                for num in Data_Json.keys():
                                    Row_Dict = Data_Json[num]

                                    # DB 쿼리문
                                    query = """INSERT INTO {} ({}) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                                                                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                            """.format(table, col_Text)
                                    Result_Text = (
                                        Row_Dict['date'], Row_Dict['콩_' + name], Row_Dict['고구마_' + name],
                                        Row_Dict['감자_' + name], Row_Dict['배추_' + name], Row_Dict['양배추_' + name],
                                        Row_Dict['시금치_' + name], Row_Dict['상추_' + name], Row_Dict['얼갈이배추_' + name],
                                        Row_Dict['수박_' + name], Row_Dict['참외_' + name], Row_Dict['오이_' + name],
                                        Row_Dict['호박_' + name], Row_Dict['토마토_' + name], Row_Dict['딸기_' + name],
                                        Row_Dict['무_' + name], Row_Dict['당근_' + name], Row_Dict['열무_' + name],
                                        Row_Dict['건고추_' + name], Row_Dict['풋고추_' + name], Row_Dict['양파_' + name],
                                        Row_Dict['대파_' + name], Row_Dict['쪽파_' + name], Row_Dict['생강_' + name],
                                        Row_Dict['미나리_' + name], Row_Dict['깻잎_' + name], Row_Dict['피망(단고추)_' + name],
                                        Row_Dict['파프리카_' + name], Row_Dict['방울토마토_' + name], Row_Dict['참깨_' + name],
                                        Row_Dict['땅콩_' + name], Row_Dict['느타리버섯_' + name], Row_Dict['새송이_' + name],
                                        Row_Dict['팽이버섯_' + name], Row_Dict['호두_' + name], Row_Dict['사과_' + name],
                                        Row_Dict['배_' + name], Row_Dict['복숭아_' + name], Row_Dict['포도_' + name],
                                        Row_Dict['감귤_' + name], Row_Dict['단감_' + name], Row_Dict['바나나_' + name],
                                        Row_Dict['참다래(키위)_' + name], Row_Dict['파인애플_' + name], Row_Dict['오렌지_' + name],
                                        Row_Dict['레몬_' + name], Row_Dict['체리_' + name], Row_Dict['망고_' + name])
                                    cur.execute(query, Result_Text)
                                    db.commit()
                            cur.close()


                else:
                    day = (datetime.strptime(day, '%Y%m%d') - timedelta(days=1)).strftime('%Y%m%d')
                    Total_List = []
                    Total_List.append(day)

                    db = pymysql.Connect(host=self.DB_HOST,
                                         user=self.DB_USERNAME,  # db 계정
                                         password=self.DB_PASSWORD,  # db 비밀 번호
                                         database=self.DB_NAME)  # 접속 하고자 하는 db 명
                    ## DB 작업
                    with db:
                        with db.cursor() as cur:
                            cur.execute(
                                "SELECT * FROM {}_retail WHERE date = {}".format(self.Area_Dict[Table], str(day)))
                            if not cur.fetchall():
                                with open(data, 'r', encoding='utf-8') as f:
                                    Data_Json = json.load(f)
                                for data_List in Data_Json['Result']:
                                    for price in data_List.values():
                                        Total_List.append(price[0])
                                        Total_List.append(price[1])
                                cur.execute("SHOW columns FROM {}_retail".format(self.Area_Dict[Table]))

                                col_Text = ''
                                for cnt, column in enumerate(cur.fetchall()):
                                    if cnt == 0:
                                        col_Text += column[0]
                                    else:
                                        col_Text = col_Text + "," + column[0]

                                # DB 쿼리문
                                query = "INSERT INTO {}_retail ({}) VALUES {}".format(self.Area_Dict[Table], col_Text,
                                                                                      tuple(Total_List))
                                cur.execute(query)
                                db.commit()
                            cur.close()
            return 'Daily_DB Finish'

        except Exception as e:
            message = traceback.format_exc()
            return message
