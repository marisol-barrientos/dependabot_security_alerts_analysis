import semver

import sys
import pandas as pd

from src import dependency

new_vulnerabilities = []
last_commit_vulnerabilities = []
vulnerabilities_log = []
kept_vulnerabilities = []
revoked_vulnerabilities = []
total_commit_vulnerabilities = []
no_duplicated_vulnerabilities = []
severity_records = []
vulnerable_versions_csv = pd.read_csv("../input/vulnerable_versions.csv", sep=';', dtype={"id": int})


def cleaner(version_to_clean):
    """It cleans a dependency version, removing spaces, '^' and '~'.
    Semver does not read version strings that contain those unwanted characters.

    :param version_to_clean: Dependency version to clean.
    :type version_to_clean: str

    :return: Dependency version cleaned.
    :rtype: str
    """
    dependency_version_cleaned = version_to_clean.replace(" ", "")
    dependency_version_cleaned = dependency_version_cleaned.replace("^", "")
    dependency_version_cleaned = dependency_version_cleaned.replace("~", "")
    return dependency_version_cleaned


def version_in_range(vulnerable_range, version):
    """It calculates if a version is within range.

    :param vulnerable_range: It represents the range.
    :type vulnerable_range: str

    :param version: It represents the dependency version.
    :type version: str

    :return: It return 'True' if version is within range, if not it returns 'False'.
    :rtype: bool
    """
    range_cleaned = cleaner(vulnerable_range)

    if ">=" in vulnerable_range:
        range_cleaned = range_cleaned.replace(">=", "")
        result = semver.compare(range_cleaned, version)
        if result is -1 or 0:
            return True
    elif "<=" in vulnerable_range:
        range_cleaned = range_cleaned.replace("<=", "")
        result = semver.compare(range_cleaned, version)
        if result is 1 or 0:
            return True
    elif ">" in vulnerable_range:
        range_cleaned = range_cleaned.replace(">", "")
        result = semver.compare(range_cleaned, version)
        if result is -1:
            return True
    elif "<" in vulnerable_range:
        range_cleaned = range_cleaned.replace("<", "")
        result = semver.compare(range_cleaned, version)
        if result is 1:
            return True
    elif "=" in vulnerable_range:
        range_cleaned = range_cleaned.replace("=", "")

    result = semver.compare(range_cleaned, version)
    if result is 0:
        return True
    return False


def is_vulnerable(dependency_version, vulnerable_range):
    """It analyzes if a dependency version is vulnerable.

    :param dependency_version: It represents the dependency version.
    :type dependency_version: str

    :param vulnerable_range: It represents the vulnerable range.
    :type vulnerable_range: str

    :return: It returns 'True' if version is within range, if not it returns 'False'.
    :rtype: bool
    """
    if "," in vulnerable_range:
        return version_in_range(vulnerable_range.split(',')[0], dependency_version) and version_in_range(
            vulnerable_range.split(',')[1], dependency_version)
    else:
        return version_in_range(vulnerable_range, dependency_version)


def get_dependency(line):
    """It returns the dependency present in a line.

    :param line: Line where the dependency is searched.
    :type line: str

    :return: It returns the dependency present in a line.
    :rtype: Dependency
    """
    # in case that the dependency name starts with @, we should remove '@' and add it after spliting.
    if line.startswith("@"):
        line = line[1:]
        return dependency.Dependency("@" + line.split("@")[0], line.split("@")[1].replace("extraneous", ""))
    else:
        return dependency.Dependency(line.split("@")[0], line.split("@")[1].replace("extraneous", ""))


def set_dependencies_and_vulnerabilities(file_path, pattern_1, pattern_2, pattern_3, pattern_4, pattern_5, pattern_6):
    """It returns the total number of dependencies presented in a commit. If one of those dependencies
    contains a vulnerability it will be set into vulnerable dependencies list.

    :param file_path: Path of npm vulnerable library versions file.
    :type file_path: str

    :param pattern_1: Possible pattern of first level dependency.
    :type pattern_1: str

    :param pattern_2: Possible pattern of first level dependency.
    :type pattern_2: str

    :param pattern_3: Possible pattern of first level dependency.
    :type pattern_3: str

    :param pattern_4: Possible pattern of first level dependency.
    :type pattern_4: str

    :param pattern_5: Possible pattern of first level dependency.
    :type pattern_5: str

    :param pattern_6: Possible pattern of first level dependency.
    :type pattern_6: str


    :return: It returns the total number of dependencies presented in a commit.
    :rtype: int
    """
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
    """It safe last commit vulnerabilities and record the new dependencies and vulnerabilities.

    :return: It returns the total number of npm and yarn dependencies.
    :rtype: int
    """
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
    """If the current dependency is vulnerable, it will be classified as new, revoked or kept.
    At the end the dependencies log is updated adding the current dependency.

     :param current_dependency: Dependency to classify.
     :type current_dependency: Dependency

     """
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
