from git import Repo

def diff_in_dependencies(current_commit, previous_commit):
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
    print("\n~~ INFO:Cloning '" + owner + "/" + name + ".git' into '" + directory[:-3] + "output'")

    return Repo.clone_from(
        url="https://github.com/" + owner + "/" + name,
        to_path="../output",
        no_checkout=True
    )
