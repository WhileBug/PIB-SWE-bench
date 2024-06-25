import git
import os

class InstanceRepo:
    def __init__(self, instance_id, repo_path, repo_name, base_commit, placeholder_patch):
        self.instance_id = instance_id
        self.repo_path = repo_path
        self.repo_name = repo_name
        self.base_commit = base_commit
        self.placeholder_patch = placeholder_patch

    def clone_repo(
            self
    ):
        if os.path.exists(self.repo_path):
            print("repo:", self.repo_path, "already cloned")
        else:
            repo_url = "https://github.com/"+self.repo_name
            repo = git.Repo.clone_from(repo_url, self.repo_path)
            repo.git.checkout(self.base_commit)

    def apply_patch_path(self, patch_path):
        repo = git.Repo(self.repo_path)
        if repo.is_dirty():
            raise Exception("Uncommited changes")
        patch_path = os.path.abspath(patch_path)
        try:
            repo.git.apply(patch_path)
        except Exception as e:
            print(e)
        return 0

    def apply_patch_string(self, patch_str):

        patch_path = "temp_patch.patch"
        with open(patch_path, "w+") as f:
            f.write(patch_str)

        repo = git.Repo(self.repo_path)
        if repo.is_dirty():
            raise Exception("Uncommited changes")
        patch_path = os.path.abspath(patch_path)
        try:
            repo.git.apply(patch_path)
        except Exception as e:
            print(e)
        return 0

    def placeholder_add(self):
        self.apply_patch_path(self.placeholder_patch)