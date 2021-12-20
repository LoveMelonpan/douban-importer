import pandas as pd
import json
import request
from request import Cookie

class FileReader():

    def __init__(self,file):
        self.file = file

    def read(self):
        pass


class XlsxReader(FileReader):

    def __init__(self,file):
        super().__init__(file)
        try:
            f = pd.ExcelFile(file)
            self.sheets = f.sheet_names
        except FileNotFoundError:
            raise Exception("no such xlsx file.")

    #dict[sheet_name] = list
    def read(self)->dict:
        data = {}

        for sheet in self.sheets:
            list = []
            df = pd.read_excel(self.file,sheet_name=sheet)
            for _, row in df.iterrows():
                list.append(row)
            data[sheet] = list
        return data


class JsonReader(FileReader):
    def __init__(self,file):
        super().__init__(file)

    def read(self)->list[dict]:
        with open(self.file,'r') as f:
            data = json.load(f)
            f.close()
            return data


def parseJsonFormatCookies(jsonList)->list:
    cookies = []

    for cookieDict in jsonList:
        try:
            cookie = request.Cookie(cookieDict["name"], cookieDict["value"], cookieDict["domain"], cookieDict["path"])
            cookies.append(cookie)
        except KeyError as e:
            raise(e)

    return cookies


# convert entrys to object Doubanentry for a specific sheet
def convertExcelDataToDoubanEntrys(sheetName:str,rows:dict)->list:
    entrys = []

    for row in rows:
        title = row["标题"]
        introduce = row["简介"]
        link = row["链接"]
        rating = row["豆瓣评分"]
        createTime = row["创建时间"]
        star = row["我的评分"]
        tag = row["标签"]
        comment = row["评论"]

        #type handle
        if pd.isna(star):
            star = ""
        else:
            star = str(int(star))
        if pd.isna(tag):
            tag = ""
        if pd.isna(comment):
            comment=""

        entry = request.DoubanEntry(type_ = sheetName, title=title, introduce=introduce, rating=rating, link=link, createTime=createTime, star=star, tag= tag, comment=comment)
        entrys.append(entry)

    return entrys

def getDoubanEntrysFromExcel(file:str)->list:
    reader = XlsxReader(file)
    rows = reader.read()

    entrys = []

    for sheetName in rows.keys():
        sheetEntrys = convertExcelDataToDoubanEntrys(sheetName,rows[sheetName])
        entrys.extend(sheetEntrys)

    return entrys
