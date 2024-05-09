import json

def load_Project_JSON():
    #---- loads all the information stored in the json in the proper format to show all the projects ----
    with open("./information/Projects.json") as Projects:
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


def makeitpretty(searchList):
    result = ""
    if len(searchList) %3 == 0:
        number_of_div = len(searchList) // 3 
        print("equal to 3 ")
    else:
        number_of_div = int(len(searchList) // 3)
    split_searchList = [searchList[i:i+3] for i in range(0, len(searchList), 3)]
    while number_of_div > 0: 
        for x in split_searchList:
            result = result + '''<div class="row">'''
            #print("x", x)
            if len(x) == 3:
                for y in x:
                    result = result + ('''
            <div class="col-md-4">
                <div class="card">
                    <div class="card-header">%s</div>
                    <img src="..." class="card-img-top" alt="...">
                
                    <div class="card-body">
                    <h5 class="card-title">%s</h5>
                    <p class="card-text">%s</p>
                    <a href="%s" class="btn btn-primary">See the Project</a>
                    </div>
                </div>
            </div>''' %(y.get("Name"), y.get("Name"), y.get("information"), y.get("Link")))
            result = result + '''</div>'''
        # create div 
        number_of_div -= 1
    if number_of_div == 0:
        for x in split_searchList:
            if len(x) != 3:
                result = result + '''<div class="row">'''
                for y in x: 
                    result = result + ('''
                    <div class="col-md-4">
                        <div class="card">
                            <div class="card-header">%s</div>
                            <img src="..." class="card-img-top" alt="...">
                        
                            <div class="card-body">
                            <h5 class="card-title">%s</h5>
                            <p class="card-text">%s</p>
                            <a href="%s" class="btn btn-primary">See the Project</a>
                            </div>
                        </div>
                    </div>''' %(y.get("Name"), y.get("Name"), y.get("information"), y.get("Link")))
                result = result + '''</div>'''
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