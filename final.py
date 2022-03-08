import getopt
import json
import sys
import time
from tinydb import TinyDB, Query
from urllib.request import urlopen


def main():
    userName = ''
    repoName = ''
    try: 
        params, args = getopt.getopt(sys.argv[1:], "u:r:")
        for p, pa in params:
            if p == '-u':
                userName = pa
            if p == '-r':
                repoName = pa
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
    db = TinyDB('gabrys.json')

    repoTable = db.table("REPO")
    userTable = db.table("USER")
    otherTable = db.table("OTHER")

    repoTable.insert({'RepoName': repo})
    userTable.insert({'UserName': user})

    api = urlopen(f"https://api.github.com/repos/{user}/{repo}/commits")
    print(type(api))
    print(api)
    commits = json.loads(api.readline())
    for commit in commits: 
        sha = commit['sha']
        otherTable.insert({'sha': sha})
        committer = commit["commit"]["committer"]
        message = commit['commit']['message']
        otherTable.insert({'committer': committer, 'message': message})
        time.sleep(0.1)
        print(f"\nrepo: {repo} \nsha: {sha} \nmessage: {message} \ncommitter: {committer}")
        
if __name__ == "__main__":
    main()


# def instruction():



#def dbConfig(user, repo):
    # db = TinyDB('test8.json')

    # repoTable = db.table("REPOS")
    # userTable = db.table("USERS")

    # repoTable.insert({'RepoName': repo})
    # userTable.insert({'UserName': user})



# otherTable.insert({'sha': sha})
# check = db.search(otherTable == f'{sha}')
# print(db)
# if check in db:
#     print("chuj")
# else:
#     exit()
# print(check)
# print(type(check))
# # if check == False:
