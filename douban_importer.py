import requests
import reader
import request

def readCookies(file):
    r = reader.JsonReader(file)
    data =  r.read()
    cookies = reader.parseJsonFormatCookies(data)
    return cookies

def main():
    entrys = reader.getDoubanEntrysFromExcel("data.xlsx")
    cookies = readCookies("cookie.json")

    for entry in entrys:
        req = request.PostRequest(entry=entry, cookies=cookies)
        request.postDoubanRequest(req)

if __name__ =="__main__":
    main()