import os
import sys
from datetime import datetime

from src import dependencies_manager, directories_manager
from src.dependencies_manager import clear_dictionaries


def prepare_repo_environment():
    """ It clears 'total commit' and 'log' lists. It replaces the 'output' folder
    for a new one. After that the environment is ready for a new repository analysis.
        """
    clear_dictionaries()
    dependencies_manager.total_commit_vulnerabilities.clear()
    dependencies_manager.vulnerabilities_log.clear()
    dependencies_manager.historial_fixes.clear()
    directories_manager.new_cloned_git_folder()


def prepare_commit_environment(repo, commit):
    """ It clears 'severity records' and 'no duplicated vulnerabilities' lists.
    After that it generates the 'first level dependencies tree' to extract the
    dependencies presented on the current commit.

    :param repo: Repository to prepare.
    :type repo: Repo

    :param commit: Current commit.
    :type commit: Commit
    """

    dependencies_manager.severity_records.clear()
    dependencies_manager.no_duplicated_vulnerabilities.clear()
    directories_manager.first_level_dependencies_tree(repo, commit)
    return False


def has_config_file(repo, commit):
    """ It sees if Dependabot's configuration is presented on a specific repository and commit.

    :param repo: Repository where the commit is.
    :type repo: Repo

    :param commit: Commit where it is searched the Dependabot's configuration file.
    :type commit: Commit

    :return It returns 'True' if Dependabot's configuration file is presented. If not it will return 'False'.
    :rtype
    """
    if directories_manager.download_file(repo, commit.hexsha, ".github/dependabot.yml"):
        return True
    return False


def print_current_time():
    """ It prints current time.
    """
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    print("Started recording - " + current_time)


def write_failed_repos_log(repo_id, repo_url):
    with open('../output/failed_repos.txt', 'a') as f1:
        failed_repo = str(repo_id) + "-" + repo_url
        f1.write(failed_repo + os.linesep)

    error = sys.exc_info()[0]
    error_details = sys.exc_info()[1]
    print("Error: \n%s" % error)
    print("Error: \n%s" % error_details)
