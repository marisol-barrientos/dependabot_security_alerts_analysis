#!/usr/bin/python
import uuid


class Point:
    """This is a conceptual class to represent each point present in the InfluxDB Bucket.

        :param repo_id: It represents the id of a repository.
        :type repo_id: int

        :param commited_date: It is the date when the commit was committed.
        :type commited_date: int

        :param commit_hexsha: It is the hexsha of a commit.
        :type commit_hexsha: int

        :param commit_author: It contains the committed author name.
        :type commit_author: int

        :param repo_name: It represents the name of a repository.
        :type repo_name: str

        :param repo_owner: It represents the owner's name of a repository.
        :type repo_owner: str

        :param total_commit_dependencies: It contains the total number of dependencies present in a commit.
        :type total_commit_dependencies: int

        :param new_vulnerabilities: It contains the total number new vulnerabilities that has been introduced in a commit.
        :type new_vulnerabilities: int

        :param fixed_vulnerabilities: It contains the total number fix vulnerabilities that has been removed in a commit.
        :type fixed_vulnerabilities: int

        :param revoked_vulnerabilities: It contains the total number revoked vulnerabilities that has been introduced in a commit. They were not in the previous commit but in other.
        :type revoked_vulnerabilities: int

        :param kept_vulnerabilities: It contains the total number of vulnerabilities that are kept in a commit. They were already presented in the previous commit.
        :type kept_vulnerabilities: int

        :param total_vulnerabilities: It contains the total number of vulnerabilities present in a commit.
        :type total_vulnerabilities: int

        :param critical_severity: It contains the total number of critical severity vulnerabilities present in a commit.
        :type critical_severity: int

        :param high_severity: It contains the total number of high severity vulnerabilities present in a commit.
        :type high_severity: int

        :param moderate_severity: It contains the total number of moderate severity vulnerabilities present in a commit.
        :type moderate_severity: int

        :param low_severity: It contains the total number of low severity vulnerabilities present in a commit.
        :type low_severity: int

        :param has_config_file: It indicates if in the commit it is present the Dependabot configuration file.
        :type has_config_file: bool
        """
    def __init__(self, repo_id, commited_date, commit_hexsha, commit_author, repo_name, repo_owner,
                 total_commit_dependencies, new_vulnerabilities, fixed_vulnerabilities, revoked_vulnerabilities, kept_vulnerabilities,
                 total_vulnerabilities, critical_severity, high_severity, moderate_severity, low_severity, has_config_file):
        """Constructor method
        """
        self.repo_id = repo_id
        self.commited_date = commited_date
        self.commit_hexsha = commit_hexsha
        self.commit_author = commit_author
        self.repo_name = repo_name
        self.repo_owner = repo_owner
        self.total_commit_dependencies = total_commit_dependencies
        self.new_vulnerabilities = new_vulnerabilities
        self.fixed_vulnerabilities = fixed_vulnerabilities
        self.revoked_vulnerabilities = revoked_vulnerabilities
        self.kept_vulnerabilities = kept_vulnerabilities
        self.total_vulnerabilities = total_vulnerabilities
        self.critical_severity = critical_severity
        self.high_severity = high_severity
        self.moderate_severity = moderate_severity
        self.low_severity = low_severity
        self.has_config_file = has_config_file


    def __str__(self):
        """To String method
        """
        return "         - Commited date:'" + str(self.commited_date) + "'" + \
               "\n         - Repository id: '" + str(self.repo_id) + "'" + \
               "\n         - Commit author: '" + str(self.commit_author) + "'" + \
               "\n         - Repo name: '" + self.repo_name + "'" + \
               "\n         - Repo owner: '" + self.repo_owner + "'" + \
               "\n         - Total number of dependencies: " + str(self.total_commit_dependencies) + \
               "\n         - New vulnerabilities: " + str(self.new_vulnerabilities) + \
               "\n         - Fixed vulnerabilities: " + str(self.fixed_vulnerabilities) + \
               "\n         - Revoked vulnerabilities: " + str(self.revoked_vulnerabilities) + \
               "\n         - Kept vulnerabilities: " + str(self.kept_vulnerabilities) + \
               "\n         - Total number of vulnerabilities: " + str(self.total_vulnerabilities) + \
               "\n         - Critical severity: " + str(self.critical_severity) + \
               "\n         - High severity: " + str(self.high_severity) + \
               "\n         - Moderate severity: " + str(self.moderate_severity) + \
               "\n         - Low severity: " + str(self.low_severity) + \
               "\n         - Dependabot configuration file: '" + str(self.has_config_file) + "'"
