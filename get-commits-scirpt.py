import getopt
import json
import sys
import time
from tinydb import TinyDB, Query
from urllib.request import urlopen


def instruction():
    print('''
    ________________________________________________________________
    HI! 
    This alpha version of script which saves repo of desired user to tinyDB, 
    Whenever you try to run script you need to provide parameters: -u username -r reponame
 
    Proper executing: ./yourScript.py -u JobbyJabber - Python-Exercises

    Since it's 0.1 version few things needs to fixed/added: 
    
    - There is a problem when providing exception for http error. Might show exception instead of crashing while URL dosen't exist.
    - It will be extended for branch parameter
    - Needs to fix dupes in DB. At the moment duplicates exists.  
    - Add comments

    Author GitID: @JobbyJabber
    ________________________________________________________________
    ''')

def main():
    instruction()
    userName = ''
    repoName = ''
    try: 
        params, args = getopt.getopt(sys.argv[1:], "u:r:")
        for p, pa in params:
            if p == '-u':
                userName = pa
            if p == '-r':
                repoName = pa
            else:
                instruction()
    except getopt.GetoptError as e: 
        print(str(e))
    checkParameters(userName, repoName)
    getCommits(userName, repoName)

def checkParameters(user, repo):
    if type(user) != str or len(user) <= 0:
        print("Please use -u then enter GitHub username ")
        sys.exit()
    if type(repo) != str or len(repo) <= 0:
        print("Please use -r then enter your repo ")
        sys.exit()


def getCommits(user, repo):
    db = TinyDB('bazaDanych.json')

    repoTable = db.table("REPO")
    userTable = db.table("USER")
    otherTable = db.table("OTHER")

    repoTable.insert({'RepoName': repo})
    userTable.insert({'UserName': user})

    api = urlopen(f"https://api.github.com/repos/{user}/{repo}/commits")

    commits = json.loads(api.readline())
    for commit in commits: 
        sha = commit['sha']
        otherTable.insert({'sha': sha})
        committer = commit["commit"]["committer"]
        message = commit['commit']['message']
        otherTable.insert({'committer': committer, 'message': message})
        time.sleep(0.1)
        print(f"\nrepo: {repo} \nsha: {sha} \nmessage: {message} \ncommitter: {committer}")
    otherTable.update 
        
if __name__ == "__main__":
    main()

