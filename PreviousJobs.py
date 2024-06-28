import json
from credentials import *

def load_Project_JSON(version = ""):
    serverCredentials = getJsonInformation()
    #---- loads all the information stored in the json in the proper format to show all the projects ----
    if version == "site":
        with open(os.path.join(serverCredentials.get("Server Files").get("baseDirectory"), serverCredentials.get("Server Files").get("Site-Template"))) as siteTemplate:
            LoadProjects = json.load(siteTemplate)
    else:
        with open(os.path.join(serverCredentials.get("Server Files").get("baseDirectory"), serverCredentials.get("Server Files").get("previousJobs"))) as Projects:
            LoadProjects = json.load(Projects)

    return LoadProjects


def MakeJobs():
    jobs = load_Project_JSON()
    sitetemplate = load_Project_JSON("site")
    result = sitetemplate.get("Carosel Start")
    listjobs = jobs.get("Jobs")
    if len(listjobs) >= 0:
        first = sitetemplate.get("Carosel First")
        first = first.replace("%logoSource", listjobs[0].get("Logo"))
        first = first.replace("%CompanyName", listjobs[0].get("Company"))
        first = first.replace("%EmploymentTitle", listjobs[0].get("Position"))
        first = first.replace("%Date", listjobs[0].get("Employment_Time"))
        result = result + first
    for x in range(1, len(listjobs)):
        rest = sitetemplate.get("Carosel")
        rest = rest.replace("%logoSource", listjobs[x].get("Logo"))
        rest = rest.replace("%CompanyName", listjobs[x].get("Company"))
        rest = rest.replace("%EmploymentTitle", listjobs[x].get("Position"))
        rest = rest.replace("%Date", listjobs[x].get("Employment_Time"))
        result = result + rest
    result = result + sitetemplate.get("Carosel End") 
    return {"carousel":result}

