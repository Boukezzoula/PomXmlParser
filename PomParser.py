import csv
from pydriller import Repository
import xml.etree.ElementTree as etree


changedLines_list = []
namespaces = {'xmlns' : 'http://maven.apache.org/POM/4.0.0'}
#class represent the changed lines

class changedLine:
    def __init__(self, CommitHash, CommitDate, ChangeType, groupId, artifactId, version, NbrAddedLines,NbrDeletedLines,NbrModifiedFiles):
        self.CommitHash = CommitHash
        self.CommitDate = CommitDate
        self.ChangeType = ChangeType
        self.groupId = groupId
        self.artifactId = artifactId
        self.version = version
        self.NbrAddedLines = NbrAddedLines
        self.NbrDeletedLines = NbrDeletedLines
        self.NbrModifiedFiles = NbrModifiedFiles


for commit in Repository('https://github.com/huisunan/epic4j').traverse_commits():
    for m in commit.modified_files:
        if m.filename == "pom.xml":
            print(commit.hash)
            print(type(m.source_code))  # <class 'str'>
            if m.source_code is not None:
                tree = etree.fromstring(bytes(m.source_code,'utf-8'))
                deps = tree.findall(".//xmlns:dependency", namespaces=namespaces)
                for d in deps:
                    groupId = d.find("xmlns:groupId", namespaces=namespaces).text
                    artifactId = d.find("xmlns:artifactId", namespaces=namespaces).text
                    version = d.find("xmlns:version", namespaces=namespaces)
                    try:
                        if version is not None:  # The variable
                             change = changedLine(commit.hash, commit.committer_date, m.change_type.name,
                                                  groupId,artifactId,version.text, commit.insertions, commit.deletions, commit.files)
                             changedLines_list.append(change)
                        else:
                             change = changedLine(commit.hash, commit.committer_date, m.change_type.name,
                                             groupId, artifactId, "None", commit.insertions,
                                             commit.deletions, commit.files)
                             changedLines_list.append(change)
                    except NameError:
                        print("This variable is not defined")
            else:
                print("Ouuupppps is None")





with open('result.csv', 'w', newline='') as f:

    # fieldnames lists the headers for the csv.
    w = csv.DictWriter(f, fieldnames=vars(changedLines_list[0]))
    w.writeheader()
    for change in changedLines_list:
        # Build a dictionary of the member names and values...
        w.writerow({'CommitHash': change.CommitHash, 'CommitDate': change.CommitDate, 'ChangeType': change.ChangeType, 'groupId': change.groupId,'artifactId':change.artifactId,'version':change.version})
