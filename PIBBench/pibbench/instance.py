from PIBBench.pibbench.repository import InstanceRepo

class Instance:
    def __init__(self, instance_id, repo_path, repo_name, base_commit, file2line, home_path, attack_method):
        self.instance_id = instance_id
        self.repo_path = repo_path
        self.repo_name = repo_name
        self.base_commit = base_commit
        self.file2line = file2line
        self.instance_repo = InstanceRepo(
            instance_id,
            repo_path,
            repo_name,
            base_commit,
            file2line,
            base_repo_path = home_path+"/"+instance_id+"-base"
        )

        self.attack_method = attack_method
        self.task_id = self.instance_id+"-"+self.attack_method

        #self.full_repo_path = home_path+"/"+self.instance_id
        self.issue_path = home_path+"/"+self.task_id+".md"
        self.pred_patch_path = home_path+"/"+self.task_id+".patch"
        self.pred_json_path = home_path + "/" + self.task_id + ".json"
        self.log_dir_path = home_path + "/" + self.task_id+"-log"
        self.test_bed_path = home_path + "/" + self.task_id + "-test_bed"
        self.pred_traj_path = home_path+"/"+self.task_id+".traj"