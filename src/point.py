#!/usr/bin/python
import uuid


class Point:

    def __init__(self, repo_id, commited_date, commit_hexsha, commit_author, repo_name, repo_owner,
                 total_commit_dependencies, new_vulnerabilities, fixed_vulnerabilities, revoked_vulnerabilities, kept_vulnerabilities,
                 total_vulnerabilities, critical_severity, high_severity, moderate_severity, low_severity, has_config_file):
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
