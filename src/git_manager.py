from git import Repo


def diff_in_dependencies(current_commit, previous_commit):
    """ It compares the current commit with the previous. To check if'package.json',
    'package-lock.json', 'npm-shrinkwrap.json' or 'yarn.lock' were changed.

    :param current_commit: Current commit.
    :type current_commit: Commit

    :param previous_commit: Previous commit.
    :type previous_commit: Commit

    :return: It returns 'True' if 'package.json', 'package-lock.json', 'npm-shrinkwrap.json' or 'yarn.lock' was modified in the current commit, if not it will return 'False'.
    :rtype: bool
    """
    diff_index = previous_commit.diff(current_commit)
    for diff in diff_index:
        if "package.json" in {diff.b_path} or "package.json" in {diff.a_path}:
            return True
        if "package-lock.json" in {diff.b_path} or "package-lock.json" in {diff.a_path}:
            return True
        if "npm-shrinkwrap.json" in {diff.b_path} or "npm-shrinkwrap.json" in {diff.a_path}:
            return True
        if "yarn.lock" in {diff.b_path} or "yarn.lock" in {diff.a_path}:
            return True
    return False


def clone_repo(name, owner, directory):
    """ To clone repository into '/cloned_git'

    :param name: Repository name.
    :type name: str

    :param owner: Repository owner.
    :type owner: str

    :param directory: Directory were the repository is cloned.
    :type directory: str

    :return: It returns an instance of the cloned repository.
    :rtype: Repo
    """
    print("\n~~ INFO:Cloning '" + owner + "/" + name + ".git' into '" + directory[:-3] + "cloned_git'")

    return Repo.clone_from(
        url="https://github.com/" + owner + "/" + name,
        to_path="../cloned_git",
        no_checkout=True
    )
