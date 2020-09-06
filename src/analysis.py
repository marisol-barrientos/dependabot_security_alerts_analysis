import os
import sys

import yaml
import pandas as pd


from datetime import datetime
import time

from src import db_manager, git_manager, helpers, dependencies_manager, directories_manager, point

with open('../config.yaml') as config_file:
    config = yaml.full_load(config_file)
    vulnerable_versions_csv = pd.read_csv(config['vulnerable_versions_csv'], sep=';', dtype={"id": int})
    repos_csv_to_read = config['repos_csv_to_read']
    token = config['token']
    org = config['org']
    bucket = config['bucket']
    client = config['client']


current_directory = os.getcwd()
manager = db_manager
write_api = manager.open_connection(client, token)


def main():

    print("\n~~ INFO:Reading repositories presented in '" + repos_csv_to_read + "' ...")
    repos_csv = pd.read_csv(repos_csv_to_read, sep=';', dtype={"lib_id": int})

    for i in range(repos_csv.shape[0]):
        try:
            github_url = repos_csv['github_link'][i]
            repo_owner = github_url.split('/')[3]
            repo_name = github_url.split('/')[4]
            previous_commit = 0
            helpers.prepare_repo_environment()
            print("------------------------------------------------------------------")
            print("~~ INFO:Analyzing evolution of vulnerable dependencies from '" + repo_owner + "/" + repo_name + "'")

            repo = git_manager.clone_repo(repo_name, repo_owner, current_directory)

            # Iterate over each commit
            for commit in list(repo.iter_commits()):  # if we want the 1000 first -> (repo.iter_commits('master', max_count=1000)

                has_config_file = "False"
                print("\n       * Commit: '" + commit.hexsha + "'")
                if previous_commit is 0 or git_manager.diff_in_dependencies(commit, previous_commit):
                    has_config_file = helpers.prepare_commit_environment(repo, commit)

                    fixed_vulnerabilities = len(dependencies_manager.total_commit_vulnerabilities)
                    total_commit_dependencies = dependencies_manager.set_npm_and_yarn_dependencies()
                    if len(dependencies_manager.last_commit_vulnerabilities) > 0:
                        fixed_vulnerabilities = fixed_vulnerabilities - len(dependencies_manager.kept_vulnerabilities)
                    if fixed_vulnerabilities < 0:
                        fixed_vulnerabilities = 0
                    if directories_manager.download_file(repo, commit.hexsha, ".github/dependabot.yml"):
                        has_config_file = "True"

                    db_manager.record_point(point.Point(repos_csv['lib_id'][i]
                                            , int(round(time.mktime(datetime.strptime(commit.committed_datetime.strftime('%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S').timetuple())))
                                            , commit.hexsha
                                            , commit.author
                                            , repo_name
                                            , repo_owner
                                            , total_commit_dependencies
                                            , len(dependencies_manager.new_vulnerabilities)
                                            , fixed_vulnerabilities
                                            , len(dependencies_manager.revoked_vulnerabilities)
                                            , len(dependencies_manager.kept_vulnerabilities)
                                            , len(dependencies_manager.total_commit_vulnerabilities)
                                            , dependencies_manager.severity_records.count("4")
                                            , dependencies_manager.severity_records.count("3")
                                            , dependencies_manager.severity_records.count("2")
                                            , dependencies_manager.severity_records.count("1")
                                            , has_config_file)
                                            , write_api
                                            , bucket
                                            , org)

                    previous_commit = commit

                else:
                    print("         ~~ INFO:Dependencies have not changed. ")



        except:
            error = sys.exc_info()[0]
            error_details = sys.exc_info()[1]
            print("Error: \n%s" % error)
            print("Error: \n%s" % error_details)


if __name__ == "__main__":
    main()
