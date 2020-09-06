import dependencies_manager
import directories_manager


def prepare_repo_environment():
    dependencies_manager.total_commit_vulnerabilities.clear()
    dependencies_manager.vulnerabilities_log.clear()
    directories_manager.new_output_folder()

def prepare_commit_environment(repo, commit):
    dependencies_manager.severity_records.clear()
    dependencies_manager.no_duplicated_vulnerabilities.clear()
    directories_manager.first_level_dependencies_tree(repo, commit)
    return False