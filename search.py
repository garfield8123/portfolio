import json
from credentials import *

def load_Project_JSON(version = ""):
    serverCredentials = getJsonInformation()
    #---- loads all the information stored in the json in the proper format to show all the projects ----
    if version == "site":
        with open(os.path.join(serverCredentials.get("Server Files").get("baseDirectory"), serverCredentials.get("Server Files").get("Site-Template"))) as siteTemplate:
            LoadProjects = json.load(siteTemplate)
    else:
        with open(os.path.join(serverCredentials.get("Server Files").get("baseDirectory"), serverCredentials.get("Server Files").get("Projects"))) as Projects:
            LoadProjects = json.load(Projects)

    return LoadProjects

def search(SearchBox):
    searchList = load_Project_JSON()
    queredList = []
    #---- Finds similiar name or tags for search box ----
    for x in searchList.get("Projects"):
        if SearchBox.lower() in x.get("Name").lower():
            queredList.append(x)
        elif SearchBox.lower() in [y.lower() for y in x.get("tag")]:
            queredList.append(x)
        elif SearchBox.lower() in x.get("information"):
            queredList.append(x)
        else:
            continue
    return queredList

def makeprettytags(Project):
    siteTemplate = load_Project_JSON("site")
    tagstyle = siteTemplate.get("Tag")
    tagStylestart = siteTemplate.get("Tag start")
    tagStyleend = siteTemplate.get("Tag end")
    taglist = Project.get("tag")
    result = tagStylestart
    for x in taglist:
        result = result + tagstyle.replace("%name", x)
    result = result + tagStyleend
    return result

def makeitpretty(searchList):
    siteTemplate = load_Project_JSON("site")
    result = ""
    if len(searchList) %3 == 0:
        number_of_div = len(searchList) // 3 
        print("equal to 3 ")
    else:
        number_of_div = len(searchList) // 3
    split_searchList = [searchList[i:i+3] for i in range(0, len(searchList), 3)]
    
    while number_of_div > 0: 
        for x in split_searchList:
            
            result = result + siteTemplate.get("Project start")
            #print("x", x)
            if len(x) == 3:
                for y in x:
                    projectstyle = siteTemplate.get("Project")
                    projectstyle = projectstyle.replace("%tag", makeprettytags(y))
                    projectstyle = projectstyle.replace('%title', y.get("Name"))
                    projectstyle = projectstyle.replace('%info', y.get("information"))
                    projectstyle = projectstyle.replace('%link', y.get("Link"))
                    result = result + projectstyle
                split_searchList.remove(x)
            result = result + siteTemplate.get("Project end")
        # create div 
        number_of_div -= 1
    if number_of_div == 0:
        for x in split_searchList:
            if len(x) != 3:
                result = result + siteTemplate.get("Project start")
                for y in x: 
                    projectstyle = siteTemplate.get("Project")
                    projectstyle = projectstyle.replace('%tag', makeprettytags(y))
                    projectstyle = projectstyle.replace('%title', y.get("Name"))
                    projectstyle = projectstyle.replace('%info', y.get("information"))
                    projectstyle = projectstyle.replace('%link', y.get("Link"))
                    result = result + projectstyle
                result = result + siteTemplate.get("Project end")
    return result
    

def template_dict(searchlist=None):
    load_projects = load_Project_JSON()
    if searchlist is None:
        result = makeitpretty(load_projects.get("Projects"))
    else:
        result = makeitpretty(searchlist)
    return {"ProjectList": result}

def getInformation_from_list(searchList):
    for x in searchList:
        print(x.get("Name"))
        print(x.get("Link"))
        print(x.get("information"))
        print(x.get("tag"))


