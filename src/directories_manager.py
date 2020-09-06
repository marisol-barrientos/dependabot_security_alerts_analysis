import shutil
from os import path
import os

from src import scripts_manager


def download_file(repo, commit_hexsha, file_name):
    """ To Download file if it is presented in a repository commit.

    :param repo: Repository name that contains the commit.
    :type repo: str

    :param commit_hexsha: Commit where the file is searched.
    :type commit_hexsha: str

    :param file_name: Name of the file to download.
    :type file_name: str

    :return: It returns 'True' if file exists in the commit and it can be downloaded, if not it returns 'False'.
    :rtype: Repo
    """
    try:
        repo.git.checkout(commit_hexsha, file_name)
        if path.exists("../cloned_git/" + file_name):
            return True
        return False
    except:
        # print("         INFO: It doesn't contain '" + file_name + "'")
        return False
        pass


def remove_file(file_directory):
    """ To remove file.

    :param file_directory: Path where is the wanted to be delete file.
    :type file_directory: str
    """
    try:
        os.remove(file_directory)
    except:
        pass


def new_cloned_git_folder():
    """ It deletes 'cloned git' folder, if possible.
    It generates a new 'cloned git' folder.

    :param file_directory: Path where is the wanted to be delete file.
    :type file_directory: str
    """
    try:
        shutil.rmtree("../cloned_git")
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
    os.mkdir("../cloned_git")


def first_level_dependencies_tree(repo, commit):
    """ It downloads 'package.json', 'package-lock.json' and 'npm-shrinkwrap.json',
    'yarn.lock' is possible. If'package.json' was downloaded, it will generate the
    first level npm dependencies tree. If 'yarn.lock' was downloaded, it will create
    the first level yarn dependencies tree.

     :param repo: Repository that contains the commit that it is being analyzed.
     :type repo: Repo

     :param commit: Commit which dependencies first level tree is being built.
     :type commit: Commit
     """
    has_package_file = download_file(repo, commit.hexsha, 'package.json')
    download_file(repo, commit.hexsha, 'package-lock.json')
    download_file(repo, commit.hexsha, 'npm-shrinkwrap.json')
    has_yarn_dependencies = download_file(repo, commit.hexsha, 'yarn.lock')

    if has_package_file:
        scripts_manager.collect_npm_dependencies()

    if has_yarn_dependencies:
        scripts_manager.collect_yarn_dependencies()

    for file in ["../cloned_git/package.json", "../cloned_git/yarn.lock", "../cloned_git/package-lock.json",
                 "../cloned_git/package-lock.json"]:
        remove_file(file)