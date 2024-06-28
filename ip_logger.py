import os.path
import time
import pandas
import json
import requests
from credentials import *

def IPJsonInfo():
    serverCredentials = getJsonInformation()
    with open(os.path.join(serverCredentials.get("Server Files").get("baseDirectory"), serverCredentials.get("Server Files").get("ipLoggerInfo"))) as ipInfo:
        ipInfoJson = json.load(ipInfo)
    return ipInfoJson, serverCredentials.get("Server Files").get("baseDirectory")

def ip_logged(ip_addr, ip_addr2):
    ipInfoJson, baseDirectory = IPJsonInfo()
    location = os.path.join(baseDirectory, ipInfoJson.get("IP_txt_File"))
    if os.path.isfile(location):
        f = open(location, "r+")
        for x in f:
            list_x = x.split(":")
            print(list_x[0])
            print(ip_addr)
            print(ip_addr not in list_x[0])
            if ip_addr not in list_x[0] and str(ip_addr2) not in list_x[1].replace("\n", ""):
                f.write(ip_addr + ":" + str(ip_addr2)+"\n")
        f.close()
        print("here")
    else:
        f = open(location, "w")
        f.write(ip_addr + ":" + str(ip_addr2) +"\n")
        f.close()
        print("here2")

def get_pretty():
    ipInfoJson, baseDirectory = IPJsonInfo()
    location = os.path.join(baseDirectory, ipInfoJson.get("IP_txt_File"))
    biglist = []
    ipaddrlist = open(location, 'r').read()
    listiplist = ipaddrlist.split("\n")
    for x in listiplist:
        smalllist = x.split(":")
        print("Small", smalllist)
        if len(smalllist) > 1: 
            biglist.append(smalllist[1])
    setbiglist = set(biglist)
    bigstring = ""
    for x in setbiglist:
        bigstring += x +","
        get_IP_loc(x)
    print(bigstring)
    return setbiglist

def get_IP_loc(ipaddr):
    ipInfoJson, baseDirectory = IPJsonInfo()
    csv_location = os.path.join(baseDirectory, ipInfoJson.get("IP_CSV_File"))
    url = ipInfoJson.get("api_site")+ipaddr
    headers = {"accept":"application/json","content-type":"application/json"}
    time.sleep(10)
    r = requests.get(url=url, headers=headers)
    print(r.status_code)
    if r.status_code == 200:
        results = r.json()
        print("ip", ipaddr)
        if ipaddr is not None: 
            print("results", results)
            ip_addr_dataframe = getIPRequest(results, ipaddr)
            print(ip_addr_dataframe)
            if os.path.isfile(csv_location):
                csvFile_dataframe = pandas.read_csv(csv_location)
                csvFile_dataframe1 = pandas.concat([ip_addr_dataframe,csvFile_dataframe], axis=0)
                csvFile_dataframe1 = csvFile_dataframe1.reset_index(drop=True).drop_duplicates(keep="first", inplace=False)
                print(csvFile_dataframe1)
                csvFile_dataframe1.to_csv(csv_location, index=False, header=True)
                print("file exists")
            else:
                ip_addr_dataframe.to_csv(csv_location, index=False, header=True)
                print("file doesn't exist")

def getIPRequest(results, ip):
    ipInfoJson, baseDirectory = IPJsonInfo()
    lookupList = ipInfoJson.get("Look up")
    dictionaryValues = {}
    dictionaryValues.update({"IP":ip})
    columnslist = ["IP"]
    for x in lookupList:
        columnslist.append(x)
        dictionaryValues.update({x:results.get(x)})
    return pandas.DataFrame([dictionaryValues], columns=columnslist)

def blacklist(ipaddr):
    ipInfoJson, baseDirectory = IPJsonInfo()
    blacklist = os.path.join(baseDirectory, ipInfoJson.get("blacklist"))
    if os.path.isfile(blacklist):
        f = open(blacklist, "r+")
        for x in f:
            f.write(x + "\n")
        f.close()
        print("here")
    else:
        f = open(blacklist, "w")
        f.write(ipaddr +"\n")
        f.close()
        print("here2")
