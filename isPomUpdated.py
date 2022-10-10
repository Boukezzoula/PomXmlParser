from collections import defaultdict
from urllib.request import urlopen
import xml.etree.ElementTree as etree
import csv
import requests

# Define the structure of the data
dependency_header = ['id', 'situation', 'groupId', 'artifactId', 'version']
dependencies_list = []


class Dependency:
    def __init__(self, id, situation, groupId, artifactId,version):
        self.id = id
        self.situation = situation
        self.version = version
        self.groupId = groupId
        self.artifactId = artifactId


maven_url = 'https://search.maven.org/solrsearch/select'
namespaces = {'xmlns' : 'http://maven.apache.org/POM/4.0.0'}

#raw github link to pom file
link = "https://raw.githubusercontent.com/vinayalodha/greenbot/master/pom.xml"


with urlopen(link) as response:
    tree = etree.parse(response)
    root = tree.getroot()

dependencies = root.find('{http://maven.apache.org/POM/4.0.0}dependencies')
for dep in dependencies:
    infoList = []
    for child in list(dep):
        print(child.tag, child.text)


deps = root.findall(".//xmlns:dependency", namespaces=namespaces)
currenId = 1

for d in deps:
    groupId = d.find("xmlns:groupId", namespaces=namespaces)
    artifactId = d.find("xmlns:artifactId", namespaces=namespaces)
    version = d.find("xmlns:version", namespaces=namespaces)
    try:
        if version is not None:  # The variable
            dependency = Dependency(currenId, 'current pom version', groupId.text, artifactId.text, version.text)
            dependencies_list.append(dependency)
            print("currenId: "+str(currenId)+" groupId: "+groupId.text+" artifactId: "+artifactId.text+" Version: "+version.text)
            params = dict(
                q="g:"+dependency.groupId+"+AND+a:"+dependency.artifactId,
                core="gav",
                rows=20,
                #wt='json'
            )
            resp = requests.get("https://search.maven.org/solrsearch/select?q=g:"+dependency.groupId+" AND a:"+dependency.artifactId+"&core=gav&rows=20")
            data = resp.json()  # Check the JSON Response Content documentation below
            if(data["response"]["numFound"] == 0):
                print("no results found")
            else:
                dependency = Dependency(currenId, 'latest pom version', data["response"]["docs"][0]["g"],
                                        data["response"]["docs"][0]["a"], data["response"]["docs"][0]["v"])
                dependencies_list.append(dependency)
        else:
            dependency = Dependency(currenId, 'current pom version', groupId.text, artifactId.text, "None")
            dependencies_list.append(dependency)
            print("currenId: "+str(currenId)+" groupId: "+groupId.text+" artifactId: "+artifactId.text+" Version: "+"None")
            respon = requests.get("https://search.maven.org/solrsearch/select?q=g:" + dependency.groupId + " AND a:" + dependency.artifactId + "&core=gav&rows=20")
            data = respon.json()  # Check the JSON Response Content documentation below
            if (data["response"]["numFound"] == 0):
                print("no results found")
            else:
                dependency = Dependency(currenId, 'latest pom version', data["response"]["docs"][0]["g"],
                                        data["response"]["docs"][0]["a"], data["response"]["docs"][0]["v"])
                dependencies_list.append(dependency)
    except NameError:
        print("This variable is not defined")
    currenId += 1

with open('out.csv', 'w', newline='') as f:

    # fieldnames lists the headers for the csv.
    w = csv.DictWriter(f, fieldnames=vars(dependencies_list[0]))
    w.writeheader()
    for dep in dependencies_list:
        # Build a dictionary of the member names and values...
        w.writerow({'id': dep.id, 'situation': dep.situation, 'groupId': dep.groupId, 'artifactId': dep.artifactId, 'version': dep.version})

