import csv
from pydriller import Repository


class changedLine:
    def __init__(self, CommitHash, CommitName, CommitDate, ChangeType, ChangeLine, ChangeValue):
        self.CommitHash = CommitHash
        self.CommitName = CommitName
        self.CommitDate = CommitDate
        self.ChangeType = ChangeType
        self.ChangeLine = ChangeLine
        self.ChangeValue = ChangeValue


changedLines_list = []
repo_url = 'https://github.com/gunnarmorling/quarkus-qute'
filename = repo_url.split("/")[-1]+'.csv'
print(filename)
for commit in Repository(repo_url).traverse_commits():
    for m in commit.modified_files:
        if m.filename == "pom.xml":
            for change in m.diff_parsed['added']:
                added_line = changedLine(commit.hash, commit.msg, commit.committer_date,"added",change[0],change[1])
                changedLines_list.append(added_line)
            for change in m.diff_parsed['deleted']:
                deleted_line = changedLine(commit.hash, commit.msg, commit.committer_date,"deleted",change[0],change[1])
                changedLines_list.append(deleted_line)

with open(filename, 'w', newline='') as f:

    w = csv.DictWriter(f, fieldnames=vars(changedLines_list[0]))
    w.writeheader()
    for change in changedLines_list:
        w.writerow({'CommitHash': change.CommitHash, 'CommitName':change.CommitName, 'CommitDate': change.CommitDate, 'ChangeType': change.ChangeType,
                    'ChangeLine': change.ChangeLine,'ChangeValue': change.ChangeValue})
