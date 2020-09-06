import shutil
from os import path
import os

from src import scripts_manager


def download_file(repo, commit_hexsha, file_name):
    try:
        repo.git.checkout(commit_hexsha, file_name)
        if path.exists("../output/" + file_name):
            return True
        return False
    except:
        # print("         INFO: It doesn't contain '" + file_name + "'")
        return False
        pass


def remove_file(file_directory):
    try:
        os.remove(file_directory)
    except:
        pass


def new_output_folder():
    try:
        shutil.rmtree("../output")
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
    os.mkdir("../output")


def first_level_dependencies_tree(repo, commit):
    has_package_file = download_file(repo, commit.hexsha, 'package.json')
    download_file(repo, commit.hexsha, 'package-lock.json')
    download_file(repo, commit.hexsha, 'npm-shrinkwrap.json')
    has_yarn_dependencies = download_file(repo, commit.hexsha, 'yarn.lock')

    if has_package_file:
        scripts_manager.collect_npm_dependencies()

    if has_yarn_dependencies:
        scripts_manager.collect_yarn_dependencies()

    for file in ["../output/package.json", "../output/yarn.lock", "../output/package-lock.json",
                 "../output/package-lock.json"]:
        remove_file(file)