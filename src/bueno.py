"""
import os
import sys


import yaml
import pandas as pd
import semver

from datetime import datetime
import time

import dependency
import point
import db_manager
import directories_manager
import scripts_manager
import git_manager

with open('../config.yaml') as config_file:
    config = yaml.full_load(config_file)
    vulnerable_versions_csv = pd.read_csv(config['vulnerable_versions_csv'], sep=';', dtype={"id": int})
    token = config['token']
    org = config['org']
    bucket = config['bucket']
    client = config['client']
    csv_file = config['csv_file']

current_directory = os.getcwd()
new_vulnerabilities = []
last_commit_vulnerabilities = []
vulnerabilities_log = []
kept_vulnerabilities = []
revoked_vulnerabilities = []
total_commit_vulnerabilities = []
no_duplicated_vulnerabilities = []
severity_records = []
manager = db_manager
write_api = manager.open_connection(client, token)



def cleaner(version_to_clean):
    dependency_version_cleaned = version_to_clean.replace(" ", "")
    dependency_version_cleaned = dependency_version_cleaned.replace("^", "")
    dependency_version_cleaned = dependency_version_cleaned.replace("~", "")
    return dependency_version_cleaned


def version_in_range(vulnerable_range, version):
    range_cleaned = cleaner(vulnerable_range)

    if ">=" in vulnerable_range:  # true if result -1 or 0
        range_cleaned = range_cleaned.replace(">=", "")
        result = semver.compare(range_cleaned, version)
        if result is -1 or 0:
            return True
    elif "<=" in vulnerable_range:  # true if result 1 or 0
        range_cleaned = range_cleaned.replace("<=", "")
        result = semver.compare(range_cleaned, version)
        if result is 1 or 0:
            return True
    elif ">" in vulnerable_range:  # true if result -1
        range_cleaned = range_cleaned.replace(">", "")
        result = semver.compare(range_cleaned, version)
        if result is -1:
            return True
    elif "<" in vulnerable_range:  # true if result 1
        range_cleaned = range_cleaned.replace("<", "")
        result = semver.compare(range_cleaned, version)
        if result is 1:
            return True
    elif "=" in vulnerable_range:  # true if result 0
        range_cleaned = range_cleaned.replace("=", "")

    result = semver.compare(range_cleaned, version)
    if result is 0:
        return True
    return False


def is_vulnerable(dependency_version, vulnerable_range):
    if "," in vulnerable_range:
        return version_in_range(vulnerable_range.split(',')[0], dependency_version) and version_in_range(
            vulnerable_range.split(',')[1], dependency_version)
    else:
        return version_in_range(vulnerable_range, dependency_version)



def get_dependency(line):
    # in case that the dependency name starts with @, we should remove '@' and add it after spliting.
    if line.startswith("@"):
        line = line[1:]
        return dependency.Dependency("@" + line.split("@")[0], line.split("@")[1].replace("extraneous", ""), "?")
    else:
        return dependency.Dependency(line.split("@")[0], line.split("@")[1].replace("extraneous", ""), "?")


def set_dependencies_and_vulnerabilities(file_path, pattern_1, pattern_2, pattern_3, pattern_4, pattern_5, pattern_6):
    dependencies_set = []
    dependencies_set.clear()
    try:
        with open('../output/' + file_path) as file:
            if "npm" in file_path:
                file_content = file.readlines()[1:]
            else:
                file_content = file.readlines()
            file_content = [x.strip() for x in file_content]
            last = file_content[-2]
            for line in file_content:
                previous_len = len(dependencies_set)
                if line.startswith(pattern_1):
                    dependencies_set.append(get_dependency(line.split(pattern_1, 1)[1]))
                elif line.startswith(pattern_2):
                    dependencies_set.append(get_dependency(line.split(pattern_2, 1)[1]))
                elif line.startswith(pattern_3):
                    dependencies_set.append(get_dependency(line.split(pattern_3, 1)[1]))
                elif line.startswith(pattern_6):
                    dependencies_set.append(get_dependency(line.split(pattern_6, 1)[1]))
                elif line is last and line.startswith(pattern_4):
                    dependencies_set.append(get_dependency(line.split(pattern_4, 1)[1]))
                elif line is last and line.startswith(pattern_5):
                    dependencies_set.append(get_dependency(line.split(pattern_5, 1)[1]))
                if previous_len < len(dependencies_set):
                    set_new_vulnerability(dependencies_set[-1])
        file.close()
    except:
        pass
    return len(dependencies_set)


def set_npm_and_yarn_dependencies():
    last_commit_vulnerabilities.clear()
    for vul in total_commit_vulnerabilities:
        last_commit_vulnerabilities.append(vul)

    total_commit_vulnerabilities.clear()
    kept_vulnerabilities.clear()
    new_vulnerabilities.clear()
    revoked_vulnerabilities.clear()

    npm = set_dependencies_and_vulnerabilities('npm_dependencies.txt', "└── UNMET DEPENDENCY ", "├── UNMET DEPENDENCY "
                                               , "├── ", "└── ", "└── UNMET DEPENDENCY ", "├─┬ UNMET DEPENDENCY ")

    yarn = set_dependencies_and_vulnerabilities('yarn_dependencies.txt', "└─  UNMET DEPENDENCY ", "├─ UNMET DEPENDENCY "
                                                , "├─ ", "└─  ", "└─  UNMET DEPENDENCY ", "├─┬ UNMET DEPENDENCY ")

    return npm + yarn


def set_new_vulnerability(current_dependency):
    try:
        vulnerability_position = 0
        dependency_version = current_dependency.version
        dependency_version_clean = cleaner(dependency_version)

        if semver.VersionInfo.isvalid(dependency_version_clean):
            matched_vulnerable_version_ranges = vulnerable_versions_csv.loc[
                vulnerable_versions_csv['name'] == current_dependency.library_name, "vulnerableVersionRange"].to_numpy()

            matched_vulnerable_ids = vulnerable_versions_csv.loc[
                vulnerable_versions_csv['name'] == current_dependency.library_name, "id"].to_numpy()

            matched_severity_levels = vulnerable_versions_csv.loc[
                vulnerable_versions_csv['name'] == current_dependency.library_name, "severity"].to_numpy()

            for vulnerable_version_range in matched_vulnerable_version_ranges:
                vulnerability_id = matched_vulnerable_ids[vulnerability_position]
                if is_vulnerable(dependency_version_clean,
                                 vulnerable_version_range) and vulnerability_id not in no_duplicated_vulnerabilities:
                    if vulnerability_id not in vulnerabilities_log:
                        if vulnerability_id not in last_commit_vulnerabilities:
                            new_vulnerabilities.append(vulnerability_id)
                    elif vulnerability_id in last_commit_vulnerabilities:
                        kept_vulnerabilities.append(vulnerability_id)
                    if vulnerability_id in vulnerabilities_log and vulnerability_id not in last_commit_vulnerabilities:
                        revoked_vulnerabilities.append(vulnerability_id)
                    if vulnerability_id not in vulnerabilities_log:
                        vulnerabilities_log.append(vulnerability_id)
                    no_duplicated_vulnerabilities.append(vulnerability_id)
                    severity_records.append(str(matched_severity_levels[vulnerability_position]))

            for vul_id in new_vulnerabilities:
                if vul_id not in total_commit_vulnerabilities:
                    total_commit_vulnerabilities.append(vul_id)

            for vul_id in kept_vulnerabilities:
                if vul_id not in total_commit_vulnerabilities:
                    total_commit_vulnerabilities.append(vul_id)

            for vul_id in revoked_vulnerabilities:
                if vul_id not in total_commit_vulnerabilities:
                    total_commit_vulnerabilities.append(vul_id)

    except:
        error = sys.exc_info()[0]
        error_details = sys.exc_info()[1]
        print("Error: \n%s" % error)
        print("Error: \n%s" % error_details)




def main():

    print("\n~~ INFO:Reading repositories presented in '" + csv_file + "' ...")
    repos_csv = pd.read_csv(csv_file, sep=';', dtype={"lib_id": int})

    for i in range(repos_csv.shape[0]):
        try:
            prev_commit = 0
            github_url = repos_csv['github_link'][i]
            repo_owner = github_url.split('/')[3]
            repo_name = github_url.split('/')[4]
            print("Registro general: " + str(vulnerabilities_log))
            vulnerabilities_log.clear()
            directories_manager.new_output_folder()
            total_commit_vulnerabilities.clear()


            print("------------------------------------------------------------------")
            print("~~ INFO:Analyzing evolution of vulnerable dependencies from '" + repo_owner + "/" + repo_name + "'")

            repo = git_manager.clone_repo(repo_name, repo_owner, current_directory)


            # Iterate over each commit
            for commit in list(repo.iter_commits()):  # if we want the 1000 first -> (repo.iter_commits('master', max_count=1000)
                print("\n       * Commit: '" + commit.hexsha)
                severity_records.clear()
                has_config_file = "False"
                if prev_commit is 0 or git_manager.diff_in_dependencies(commit, prev_commit):
                    no_duplicated_vulnerabilities.clear()

                    # Download configuration files.
                    has_package_file = directories_manager.download_file(repo, commit.hexsha, 'package.json')
                    directories_manager.download_file(repo, commit.hexsha, 'package-lock.json')
                    directories_manager.download_file(repo, commit.hexsha, 'npm-shrinkwrap.json')
                    has_yarn_dependencies = directories_manager.download_file(repo, commit.hexsha, 'yarn.lock')

                    if has_package_file:
                        scripts_manager.collect_npm_dependencies()

                    if has_yarn_dependencies:
                        scripts_manager.collect_yarn_dependencies()

                    for file in ["../output/package.json", "../output/yarn.lock", "../output/package-lock.json",
                                 "../output/package-lock.json"]:
                        directories_manager.remove_file(file)

                    fixed_vulnerabilities = len(total_commit_vulnerabilities)

                    total_commit_dependencies = set_npm_and_yarn_dependencies()

                    #print("Last commit: " + str(last_commit_vulnerabilities))
                    #print("Total current commit:" + str(total_commit_vulnerabilities))
                    #print("New vulnerabilities " + str(new_vulnerabilities))
                    #print("Revoked vuln:" + str(revoked_vulnerabilities))

                    if len(last_commit_vulnerabilities) > 0:
                        fixed_vulnerabilities = fixed_vulnerabilities - len(kept_vulnerabilities)

                    if fixed_vulnerabilities < 0:
                        fixed_vulnerabilities = 0

                    if directories_manager.download_file(repo, commit.hexsha, ".github/dependabot.yml"):
                        has_config_file = "True"

                    p = point.Point(repos_csv['lib_id'][i]
                                    , int(round(time.mktime(datetime.strptime(commit.committed_datetime.strftime('%Y-%m-%d %H:%M:%S') ,'%Y-%m-%d %H:%M:%S').timetuple())))
                                    , commit.hexsha
                                    , commit.author
                                    , repo_name
                                    , repo_owner
                                    , total_commit_dependencies
                                    , len(new_vulnerabilities)
                                    , fixed_vulnerabilities
                                    , len(revoked_vulnerabilities)
                                    , len(kept_vulnerabilities)
                                    , len(total_commit_vulnerabilities)
                                    , severity_records.count("4")
                                    , severity_records.count("3")
                                    , severity_records.count("2")
                                    , severity_records.count("1")
                                    , has_config_file)
                    print(p)
                    print("         ~~ INFO:Writing point into '" + bucket + "' ...")
                    db_manager.write_point(p.repo_id
                                , p.commited_date
                                , p.commit_hexsha
                                , p.commit_author
                                , p.repo_name
                                , p.repo_owner
                                , p.total_commit_dependencies
                                , p.new_vulnerabilities
                                , p.fixed_vulnerabilities
                                , p.revoked_vulnerabilities
                                , p.kept_vulnerabilities
                                , p.total_vulnerabilities
                                , p.critical_severity
                                , p.high_severity
                                , p.moderate_severity
                                , p.low_severity
                                , p.has_config_file
                                , write_api
                                , bucket
                                , org)
                    prev_commit = commit

                else:
                    print("         ~~ INFO:Dependencies have not changed. ")


        except:
            error = sys.exc_info()[0]
            error_details = sys.exc_info()[1]
            print("Error: \n%s" % error)
            print("Error: \n%s" % error_details)


if __name__ == "__main__":
    main()

"""