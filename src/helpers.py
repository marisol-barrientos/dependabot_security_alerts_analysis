from src import dependencies_manager, directories_manager


def prepare_repo_environment():
    """ It clears 'total commit' and 'log' lists. It replaces the 'output' folder
    for a new one. After that the environment is ready for a new repository analysis.
        """
    dependencies_manager.total_commit_vulnerabilities.clear()
    dependencies_manager.vulnerabilities_log.clear()
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