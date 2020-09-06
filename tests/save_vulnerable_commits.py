import os
import subprocess
import sys
import shutil

from git import Repo, Commit
from github import Github, Commit


# To create a Github instance:

g = Github("114408de7ed1d183a922ce284c30b3cdf7a36100")
repo_owner = "mcansh"
repo_name = "blog"

def set_npm_dependencies():
    print("seting npm")
    #subprocess.call(['sh', './test.sh'])
    subprocess.call(['sh', '../scripts/npm_dependencies.sh'])
    #subprocess.Popen(["../scripts/npm_dependencies.sh"], stdin=subprocess.PIPE)


def set_yarn_dependencies():
    print("seting yarn")
    subprocess.call(['sh', '../scripts/yarn_dependencies.sh'])
    #subprocess.Popen(["../scripts/yarn_dependencies.sh"], stdin=subprocess.PIPE)

try:
    # descomentar para parsear el .csv, meter en una funcion
    repo = Repo.clone_from(
        url="https://github.com/" + repo_owner + "/" + repo_name,
        to_path="/output/1",
        no_checkout=True
    )

    #repo = Repo("/home/ms28/PycharmProjects/measure_dependabot/output/1")

    print("----------------------------------------------------------------------------------------------------------------------------------------")
    print("  Repository: '" + repo_name + "'  -  Owner: '" + repo_owner + "'  ")
    print("----------------------------------------------------------------------------------------------------------------------------------------")

    for commit in list(repo.iter_commits('master', max_count=1000)): # list(repo.iter_commits()) if we want all

        print("\n     - Commit: '" + commit.hexsha)
        
         # ver si tienen vulnerabilidades,
        # nuevas_vulnerabilidades viejas_vulnerabilidades

        has_package = False
        has_package_lock = False
        has_npm_shrinkwrap = False
        has_yarn_dependencies = False

        try:
            repo.git.checkout(commit.hexsha, 'package.json')
            has_package = True
        except:
            print("         It doesn't contain 'package.json'")
            pass
        
        try:
            repo.git.checkout(commit.hexsha, 'package-lock.json')
            has_package_lock = True
        except:
            print("         It doesn't contain 'package-lock.json'")
            pass

        try:
            repo.git.checkout(commit.hexsha, 'npm-shrinkwrap.json')
            has_npm_shrinkwrap = True
        except:
            print("         It doesn't contain 'npm-shrinkwrap.json'")
            pass

        try:
            repo.git.checkout(commit.hexsha, 'yarn.lock')
            has_yarn_dependencies = True
        except:
            print("         It doesn't contain 'yarn.lock'")
            pass

        if has_package:
            set_npm_dependencies()
            os.remove("/output/1/package.json")

        if has_yarn_dependencies:
            set_yarn_dependencies()
            os.remove("/output/1/yarn.lock")

        if has_package_lock:
            os.remove("/output/1/package-lock.json")

        if has_npm_shrinkwrap:
            os.remove("/output/1/npm-shrinkwrap.json")
      

       # shellscript = subprocess.Popen(["../scripts/remove_old_data.sh"], stdin=subprocess.PIPE)


        # guardamos en influDB
        # commit.author.login contains dependabot
        # nuevo_id - repo_name - repo_owner - sha_commit - timestamp - dependencies 20 - nueva_vulnerable - vieja-vulnerable - añadir fixed y revoked - author del commit
        # ejemplo:
        # e23rnjnwjfnejn - shadows - nicolai - cijji23jd -2019-12-232 - 20 - 3 - 0
        # e23rnjnwjfnejn - shadows - nicolai - cijji23jd -2019-12-232 - 20 - 1 - 3
        # e23rnjnwjfnejn - shadows - nicolai - cijji23jd -2019-12-232 - 20 - 0 - 3 (si viejas vulnerabilidades es menor que la suma de nuevas y viejas eso significa que hay un arreglo)
        # e23rnjnwjfnejn - shadows - nicolai - cijji23jd -2019-12-232 - 20 - 0 - 4 (si viejas vulnerabilidades es mayor que la suma de nuevas y viejas del anterios, significa que la
        # vulnerabilidad ha vuelto)
        # el arreglo o revocar no es acumulativo, solo se indica en el commit que sucedió, es igual a la diferencia de los valores

except :
    e = sys.exc_info()[0]
    print("Error: \n%s" % e)



    #print(package_content)
   # if package_content is None:
    #    print("hola")
       #
        #shellscript = subprocess.Popen(["../scripts/yarn_dependencies.sh"], stdin=subprocess.PIPE)

    #print(package_content.decoded_content.decode())

    #subprocess.run(['sudo','sh', '../scripts/yarn_dependencies.sh'])
    #os.system("cd .. | cd input | npm install | npm list --depth 0 --silent > set_npm_dependencies.txt")


""""
    with open('randomazied_input.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if (i != 1):
                lib_name.append(row[0])
                git_project_id.append(row[1])
                github_link.append(row[2])
            else:
                i = -1

    for git_it in git_project_id:
        problem = 0
        i = i + 1
        repo = git.Repo.clone_from(
            url=github_link[i],
            to_path="/home/ms28/Desktop/TFG/repos/repoTest/" + git_project_id[i],
            no_checkout=True
        )
        try:
            commits = list(repo.iter_commits("master"))
        except git.GitCommandError:
            print("Repository: " + git_project_id[i] + " can not be downloaded")
            problem = 1
            
            """