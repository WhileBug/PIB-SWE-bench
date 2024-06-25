import git
import os
from git import Repo

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

    def git_commit_all_changes(self, commit_message):
        repo = Repo(self.repo_path)
        repo.git.add(all=True)
        repo.index.commit(commit_message)
        print(f"Committed all changes with message: '{commit_message}'")

    def placeholder_add(self):
        self.apply_patch_path(self.placeholder_patch)
        self.git_commit_all_changes(commit_message="Commit placeholder")

    def placeholder_prompt_inject(
            self,
            inject_prompt
    ):
        import os

        def replace_placeholder_in_file(file_path, placeholder, new_string):
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            new_content = content.replace(placeholder, new_string)

            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(new_content)

        def traverse_and_replace(directory, placeholder, new_string):
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if file.endswith('.txt'):  # 可以根据文件类型进行过滤
                        file_path = os.path.join(root, file)
                        replace_placeholder_in_file(file_path, placeholder, new_string)
                        print(f"Replaced in: {file_path}")

        # 使用方法
        directory = self.repo_path  # 仓库的路径
        placeholder = '[placeholder]'
        new_string = inject_prompt

        traverse_and_replace(directory, placeholder, new_string)
