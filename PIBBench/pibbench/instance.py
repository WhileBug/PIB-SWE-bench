from PIBBench.pibbench.repository import InstanceRepo

class Instance:
    def __init__(self, instance_id, repo_path, repo_name, base_commit, placeholder_patch, home_path):
        self.instance_id = instance_id
        self.repo_path = repo_path
        self.repo_name = repo_name
        self.base_commit = base_commit
        self.placeholder_patch = placeholder_patch
        self.instance_repo = InstanceRepo(instance_id, repo_path, repo_name, base_commit, placeholder_patch)

        self.repo_path = home_path+"/"+self.instance_id
        self.issue_path = home_path+"/"+self.instance_id+".md"
        self.pred_patch_path = home_path+"/"+self.instance_id+".patch"
        self.pred_json_path = home_path + "/" + self.instance_id + ".json"
        self.log_dir_path = home_path + "/" + self.instance_id+"-log"
        self.test_bed_path = home_path + "/" + self.instance_id + "-test_bed"