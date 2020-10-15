from datetime import datetime


class InfluxPoint:
    """Conceptual class to represent each point present in a InfluxDB bucket.

        :param repo_id: Id of a repository.
        :type repo_id: int

        :param commited_date: Date when the commit was committed.
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

        :param summary: It contains a dictionary with the following keys: 'new_vulnerabilities', 'fixed_vulnerabilities', 'removed_vulnerabilities', 'revoked_fixed_vulnerabilities', 'revoked_removed_vulnerabilities', 'kept_vulnerabilities' and 'total'. The values are the total number of vulnerabilities that correspond to those types.
        :type summary: Dictionary of lists.

        :param critical_severity: It contains a dictionary with the following keys: 'new_vulnerabilities', 'fixed_vulnerabilities', 'removed_vulnerabilities', 'revoked_fixed_vulnerabilities', 'revoked_removed_vulnerabilities', 'kept_vulnerabilities' and 'total'. The values are critical severity vulnerabilities corresponding to those types.
        :type critical_severity: Dictionary of lists.

        :param high_severity: It contains a dictionary with the following keys: 'new_vulnerabilities', 'fixed_vulnerabilities', 'removed_vulnerabilities', 'revoked_fixed_vulnerabilities', 'revoked_removed_vulnerabilities', 'kept_vulnerabilities' and 'total'. The values are high severity vulnerabilities corresponding to those types.
        :type high_severity: Dictionary of lists.

        :param moderate_severity: It contains a dictionary with the following keys: 'new_vulnerabilities', 'fixed_vulnerabilities', 'removed_vulnerabilities', 'revoked_fixed_vulnerabilities', 'revoked_removed_vulnerabilities', 'kept_vulnerabilities' and 'total'. The values are moderate severity vulnerabilities corresponding to those types.
        :type moderate_severity: Dictionary of lists.

        :param low_severity: It contains a dictionary with the following keys: 'new_vulnerabilities', 'fixed_vulnerabilities', 'removed_vulnerabilities', 'revoked_fixed_vulnerabilities', 'revoked_removed_vulnerabilities', 'kept_vulnerabilities' and 'total'. The values are low severity vulnerabilities corresponding to those types.
        :type low_severity: int

        :param has_config_file: It indicates if in the commit it is present the Dependabot configuration file.
        :type has_config_file: bool

        :param email: It contains the email of the commit author.
        :type email: str

        :param commit_message: It contains the commit message.
        :type commit_message: str
        """

    def __init__(self
                     , repo_id
                     , commited_date
                     , commit_hexsha
                     , commit_author
                     , repo_name
                     , repo_owner
                     , total_commit_dependencies
                     , summary
                     , critical_severity
                     , high_severity
                     , moderate_severity
                     , low_severity
                     , has_config_file
                     , email
                     , commit_message):
        """Constructor method
        """
        self.repo_id = repo_id
        self.commited_date = commited_date
        self.commit_hexsha = commit_hexsha
        self.commit_author = commit_author
        self.repo_name = repo_name
        self.repo_owner = repo_owner
        self.total_commit_dependencies = total_commit_dependencies
        self.summary = summary
        self.critical_severity = critical_severity
        self.high_severity = high_severity
        self.moderate_severity = moderate_severity
        self.low_severity = low_severity
        self.has_config_file = has_config_file
        self.email = email
        self.commit_message = commit_message


    def __str__(self):
        """To String method
        """
        return "         - Commited date:'" + datetime.utcfromtimestamp(self.commited_date).strftime('%Y-%m-%d %H:%M:%S') + "'" + \
               "\n         - Repository id: '" + str(self.repo_id) + "'" + \
               "\n         - Commit author: '" + str(self.commit_author) + "'" + \
               "\n         - Repo name: '" + self.repo_name + "'" + \
               "\n         - Repo owner: '" + self.repo_owner + "'" + \
               "\n         - Total number of dependencies: " + str(self.total_commit_dependencies) 
              # "\n         - Dependabot configuration file: '" + str(self.has_config_file) + "'" + \
              # "\n         - Email address: '" + str(self.email) + "'" + \
              # "\n         - Commit message: '" + self.commit_message.title() + \
              # "\n         - Total number of vulnerabilities: " + str(self.summary) + \
              # "\n         - Critical severity: " + str(self.critical_severity) + \
              # "\n         - High severity: " + str(self.high_severity) + \
              #  "\n         - Moderate severity: " + str(self.moderate_severity) + \
              #  "\n         - Low severity: " + str(self.low_severity)
