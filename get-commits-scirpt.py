import argparse
import json
from tinydb import TinyDB, Query, where
from urllib.request import urlopen
from urllib.error import URLError

def main():

    parser = argparse.ArgumentParser(description="Process some")

    parser.add_argument('userName', metavar="u", type=str, help='Git UserName')
    parser.add_argument('repoName', metavar="r", type=str, help='Git RepoName')
    parser.add_argument('branchName', metavar="b", type=str, help='Git BranchName')
    
    args = parser.parse_args()
    userName = args.userName
    repoName = args.repoName
    branchName = args.branchName 
    getCommits(userName, repoName, branchName)

    

def getCommits(user, repo, branch):

    try:
        api = urlopen(f"https://api.github.com/repos/{user}/{repo}/commits?sha={branch}")
    except URLError as Error:
        print("Such address doesnt exist")
        exit()   

    db = TinyDB('bazaDanych3.json')

    repoTable = db.table("REPO")
    userTable = db.table("USER")
    branchTable = db.table("BRANCH")
    otherTable = db.table("OTHER")

    w = Query()

    result1 = repoTable.search(w.RepoName == repo)
    result2 = userTable.search(w.UserName == user)
    result3 = branchTable.search(w.BranchName == branch)

    if len(result1) == 0:    
        repoTable.insert({'RepoName': repo})
    if len(result2) == 0:         
        userTable.insert({'UserName': user})
    if len(result3) == 0: 
        branchTable.insert({'BranchName': branch})

    commits = json.loads(api.readline()) 

    for commit in commits: 
        sha = commit['sha']
        q = Query()
        result = otherTable.search(q.sha == sha)
        if len(result) == 0: 
            committer = commit["commit"]["committer"]  
            message = commit['commit']['message']
            otherTable.insert({'RepoName': repo, 'BranchName': branch, 'UserName': user, 'sha': sha, 'message': message, 'committer': committer })
            print(f"\nrepo: {repo} \nbranch: {branch} \nsha: {sha} \nmessage: {message} \ncommitter: {committer} ")
            
if __name__ == "__main__":
    main()

