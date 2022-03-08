import getopt
import json
import sys
import time
from tinydb import TinyDB, Query, where
from urllib.request import urlopen


def instruction():
    print('''
    ________________________________________________________________
    HI! 
    Its script which saves repo of desired user to tinyDB, 
    Whenever you try to run script you need to provide parameters: -u username -r reponame
 
    Proper executing: ./yourScript.py -u JobbyJabber -r Python-Exercises -b branch
   
    - There is a problem when providing exception for http error. Might show exception instead of crashing while URL dosen't exist.

    Author GitID: @JobbyJabber
    ________________________________________________________________
    ''')

def main():
    instruction()
    userName = ''
    repoName = ''
    branchName = ''
    try: 
        params, args = getopt.getopt(sys.argv[1:], "u:r:b:")
        for p, pa in params:
            if p == '-u':
                userName = pa
            if p == '-r':
                repoName = pa
            if p == '-b':
                branchName = pa
            if p != '-b':
                branchName = "main"
            else:
                instruction()
    except getopt.GetoptError as e: 
        print(str(e))
    checkParameters(userName, repoName)
    getCommits(userName, repoName, branchName)

def checkParameters(user, repo):
    if type(user) != str or len(user) <= 0:
        print("Please use -u then enter GitHub username ")
        sys.exit()
    if type(repo) != str or len(repo) <= 0:
        print("Please use -r then enter your repo ")
        sys.exit()


def getCommits(user, repo, branch):
    db = TinyDB('bazaDanych14.json')

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

    api = urlopen(f"https://api.github.com/repos/{user}/{repo}/commits")

    commits = json.loads(api.readline())
    for commit in commits: 
        sha = commit['sha']
        q = Query()
        result = otherTable.search(q.sha == sha)
        if len(result) == 0:         
            otherTable.insert({'sha': sha})
            committer = commit["commit"]["committer"]
            message = commit['commit']['message']
            otherTable.insert({'committer': committer, 'message': message})
            time.sleep(0.1)
            print(f"\nrepo: {repo} \nbranch: {branch} \nsha: {sha} \nmessage: {message} \ncommitter: {committer}")

if __name__ == "__main__":
    main()

