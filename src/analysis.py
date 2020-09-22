import os

import yaml
import pandas as pd

from datetime import datetime
import time

from src import db_manager
from src.db_manager import record_point
from src.db_point import InfluxPoint
from src.dependencies_manager import summary, critical_vulnerabilities, high_vulnerabilities, moderate_vulnerabilities, \
    low_vulnerabilities, set_npm_and_yarn_dependencies
from src.git_manager import clone_repo, diff_in_dependencies
from src.helpers import print_current_time, write_failed_repos_log, prepare_commit_environment, has_config_file, \
    prepare_repo_environment

with open('../config.yaml') as config_file:
    config = yaml.full_load(config_file)
    repos_csv_to_read = config['repos_csv_to_read']
    token = config['token']
    org = config['org']
    bucket = config['bucket']
    client = config['client']


current_directory = os.getcwd()



def main():
    try:
        print("\n~~ INFO:Reading repositories presented in '" + repos_csv_to_read + "' ...")
        repos_csv = pd.read_csv(repos_csv_to_read, sep=';', dtype={"id": int})

        # Iterate over each repository present in repos.csv
        for i in range(repos_csv.shape[0]):
            print_current_time("Started")
            github_url = repos_csv['github_link'][i]
            repo_owner = github_url.split('/')[3]
            repo_name = github_url.split('/')[4]
            previous_commit = 0
            prepare_repo_environment()
            print("------------------------------------------------------------------")
            print("~~ INFO:Analyzing evolution of vulnerable dependencies from '" + repo_owner + "/" + repo_name + "'")

            repo = clone_repo(repo_name, repo_owner, current_directory, repos_csv['id'][i])
            if repo is not False:
                flipped_commit_list = []
                for commit in list(repo.iter_commits()):
                    flipped_commit_list.insert(0, commit)
                # Iterate over each commit
                for commit in flipped_commit_list:  # if we want the 1000 first commits -> (repo.iter_commits('master', max_count=1000)

                    print("\n       * Commit: '" + commit.hexsha + "'")
                    if previous_commit is 0 or diff_in_dependencies(commit, previous_commit):
                        prepare_commit_environment(repo, commit)
                        # Vulnerabilities are collected and classified.
                        total_commit_dependencies = set_npm_and_yarn_dependencies()

                        record_point(InfluxPoint(
                                              repos_csv['id'][i]
                                            , int(round(time.mktime(datetime.strptime(commit.committed_datetime.strftime('%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S').timetuple())))
                                            , commit.hexsha
                                            , commit.author
                                            , repo_name
                                            , repo_owner
                                            , total_commit_dependencies
                                            , summary
                                            , critical_vulnerabilities
                                            , high_vulnerabilities
                                            , moderate_vulnerabilities
                                            , low_vulnerabilities
                                            , has_config_file(repo, commit)
                                            , commit.author.email
                                            , commit.message)
                                            , bucket
                                            , org)
                        previous_commit = commit
                    else:
                        print("         ~~ INFO:Dependencies have not changed. ")
                    print_current_time("Stopped")
    except:
        print_current_time("Failed")
        write_failed_repos_log(repos_csv['id'][i], github_url)
        pass


if __name__ == "__main__":
    main()