import requests,reader
import json
import logging
class Cookie():
    def __init__(self,name,value, domain = "",path = "/"):
        self.domain = domain
        self.name = name
        self.path = path
        self.value = value

    def __str__(self):
        return "=".join((self.name,self.path))

class DoubanEntry():
    def __init__(self,type_, title, introduce, rating, link, createTime, star, tag, comment):
        self.type_ = type_
        self.title = title
        self.introduce = introduce
        self.rating = rating
        self.link = link
        self.createTime = createTime
        self.star = star
        self.tag = tag
        self.comment = comment
    
    def __str__(self):
        return self.title

    #request header host
    def getHost(self):
        firstPartition = self.link.find("//")
        secondPartition = self.link.find(".com/")
        host = self.link[firstPartition+len("//"):secondPartition+len(".com")]
        return host

    #request header origin
    def getOrigin(self):
        partition = self.link.find("/subject")
        origin = self.link[:partition]
        return origin

    #request header referer
    def getReferer(self):
        return self.link

    #request post to it
    def getPost(self):
        partition = self.link.find(".com/")
        linkPrefix = self.link[:partition+len(".com/")]
        linkSuffix = self.link[partition+len(".com/"):]
        postUrl = linkPrefix + "j/" + linkSuffix +'interest'
        return postUrl
    
    #property "inerest" in post request form
    #看过=collect 想看=wish 在看=wish
    def getInterest(self):
        if self.type_[0] == "在":
            return "wish"
        elif self.type_[0]== "想":
            return "do"
        else:
            return "collect"

class PostRequest():
    def __init__(self, entry:DoubanEntry, cookies:list):
        self.data = entry
        self.url = entry.getPost()
        self.header = ""
        self.cookies = cookies
        self.payload = {}
        self.setHeader()
        self.setPayload()

    def setHeader(self):
        host = self.data.getHost()
        origin = self.data.getOrigin()
        referer = self.data.getReferer()
        cookies  = self.getPostCookieString()

        self.header = {
            'Accept':'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language': 'zh,en-US;q=0.9,en;q=0.8,zh-TW;q=0.7,zh-CN;q=0.6',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
            'Host':host,
            'Origin':origin,
            'Referer':referer,
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'X-Requested-With': 'XMLHttpRequest',
            'Cookie':cookies,
        }

    """
    request

    ck : cookie["jznd"]
    intetest :
    rating :
    foldCollect:
    tags :
    comment :
    """
    def setPayload(self):
        ck = getCookieValueInCookies(name="ck",cookies=self.cookies)
        interest = self.data.getInterest()
        star = self.data.star
        tags = self.data.tag
        comment = self.data.comment
        foldCollect = "F"
        self.payload = {
            'ck': ck,
            'interest': interest,
            'rating': star,
            'foldcollect': foldCollect,
            'tags': tags,
            'comment': comment,
        }

    def getPostCookieString(self):
        filterCookies = cookieFilterByDomain(url=self.url,cookies=self.cookies)
        str = getCookiesStr(cookies=filterCookies)
        return str

def getCookieValueInCookies(name:str,cookies:list):
    for cookie in cookies:
        if cookie.name == name:
            return cookie.value
    return ""

# list[request.Cookie] -> "cookie.name=cookie.value;"
def getCookiesStr(cookies:list)->str:
    """
    cookiesDict = {}
    for cookie in cookies:
        if cookie.name in cookiesDict.keys():
            cookiesDict[cookie.name] += "|" + cookie.value
        else:
            cookiesDict[cookie.name] = cookie.value 
    str = ""
    for key in cookiesDict.keys():
        str =str + "=".join((key, cookiesDict[key])) + "; "
    return str[:-1]
    """
    str =""
    for cookie in cookies:
        str = str + "=".join((cookie.name,cookie.value)) + "; "
    return str[:-2]

# filter cookies by domain,filter cookies for specfic url
def cookieFilterByDomain(url:str,cookies:list)->list:
    filterCookies = []
    for cookie in cookies:
        if cookie.domain == "":
            filterCookies.append(cookie)
        elif cookie.domain[0] == "." and cookie.domain[1:] in url:
            filterCookies.append(cookie)
        elif cookie.domain in url:
            filterCookies.append(cookie)
    return filterCookies

def postDoubanRequest(req:PostRequest):
    try:
        res = requests.post(url=req.url,data=req.payload,headers=req.header)
        if res.status_code != 200:
            logging.error("error request:", req.url)
            logging.error(res.status_code)
        else:
            print("success",req.url)
    except Exception as e:
        raise(e)