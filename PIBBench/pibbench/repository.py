import git
import os
from git import Repo
import shutil
import subprocess
from PIBBench.pibbench.utils import insert_placeholder

def apply_patch(repo_path, patch_path):
    print("repo_path, ", repo_path, "patch path", patch_path)
    # Change to the repository directory
    subprocess.run(['cd', repo_path], check=True, shell=True)

    # Apply the patch
    result = subprocess.run(['git', 'apply', patch_path], capture_output=True, text=True)

    if result.returncode == 0:
        print("Patch applied successfully.")
    else:
        print("Failed to apply patch:")
        print(result.stderr)

class InstanceRepo:
    def __init__(self, instance_id, repo_path, repo_name, base_commit, file2line, base_repo_path):
        self.instance_id = instance_id
        self.repo_path = repo_path
        self.repo_name = repo_name
        self.base_commit = base_commit
        self.file2line = file2line

        self.base_repo_path = base_repo_path

    def copy_base(self):
        if os.path.exists(self.base_repo_path):
            pass
        else:
            shutil.copytree(self.repo_path, self.base_repo_path)

    def clone_repo_base(
            self
    ):
        if os.path.exists(self.base_repo_path):
            print("repo:", self.base_repo_path, "already cloned")
        else:
            repo_url = "https://github.com/" + self.repo_name
            repo = git.Repo.clone_from(repo_url, self.base_repo_path)
            repo.git.checkout(self.base_commit)

    def copy_repo_from_base(
            self
    ):
        if os.path.exists(self.repo_path):
            pass
        else:
            shutil.copytree(self.base_repo_path, self.repo_path)

    def clone_repo(
            self
    ):
        if os.path.exists(self.repo_path):
            pass
            #print("repo:", self.repo_path, "already cloned")
        else:
            repo_url = "https://github.com/"+self.repo_name
            repo = git.Repo.clone_from(repo_url, self.repo_path)
            repo.git.checkout(self.base_commit)
            #self.copy_base()

    def apply_patch_path(self, patch_path):
        print(self.repo_path, "!!!!!!!!!!")
        repo = git.Repo(self.repo_path)
        if repo.is_dirty():
            raise Exception("Uncommited changes")
        patch_path = os.path.abspath(patch_path)
        try:
            #repo.git.apply(patch_path)
            #with open(patch_path, 'r') as file:
            #    patch_content = file.read()
            #repo.git.execute(['git', 'apply'], input=patch_path)
            #result = subprocess.run(['git', 'apply', patch_path], cwd=self.repo_path, capture_output=True, text=True)
            apply_patch(self.repo_path, patch_path)
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
        placeholder_patch_string = insert_placeholder(self.repo_path, self.file2line)
        self.apply_patch_string(placeholder_patch_string)
        self.git_commit_all_changes(commit_message="Commit placeholder")

    def base_placeholder_add(self):
        placeholder_patch_string = insert_placeholder(self.base_repo_path, self.file2line)
        self.apply_patch_string(placeholder_patch_string)
        self.git_commit_all_changes(commit_message="Commit placeholder")

    def placeholder_prompt_inject(
            self,
            inject_prompt
    ):
        import os

        def replace_placeholder_in_file(file_path, placeholder, new_string):
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            if placeholder in content:
                new_content = content.replace(placeholder, new_string)
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(new_content)
                print(f"Replaced in: {file_path}")

        def traverse_and_replace(directory, placeholder, new_string):
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if file.endswith('.py'):  # 可以根据文件类型进行过滤
                        file_path = os.path.join(root, file)
                        replace_placeholder_in_file(file_path, placeholder, new_string)
                        #print(f"Replaced in: {file_path}")

        # 使用方法
        directory = self.repo_path  # 仓库的路径
        placeholder = '[PLACEHOLDER]'
        new_string = inject_prompt

        traverse_and_replace(directory, placeholder, new_string)
