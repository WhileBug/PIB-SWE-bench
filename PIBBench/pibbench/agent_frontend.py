import requests
import json
import os
import shutil

class AgentFrontend:
    def __init__(
            self,
            agent_type="SWE-Agent",
            model_name="gpt4",#="azure:gpt4",
            agent_path:str="/Users/whilebug/Desktop/Projects/SWE-agent",
            username:str="whilebug"
    ):
        self.agent_type = agent_type
        self.model_name = model_name

        if self.agent_type == "SWE-Agent":
            self.swe_agent_url = 'http://127.0.0.1:5000/run_swe'
            self.swe_config = {}
            self.swe_config["folder_config"] = self.swe_folder_config(
                agent_path=agent_path,
                username=username
            )


    def swe_folder_config(
        self,
        agent_path:str="/Users/whilebug/Desktop/Projects/SWE-agent",
        username:str="whilebug"
    ):
        TRAJ_PATH = agent_path+"/trajectories/"+username+"/"
        TRAJ_PREFIX = self.model_name.replace(":", "-")+"__"
        TRAJ_SUFFIX = "__default_from_url__t-0.00__p-0.95__c-3.00__install-1"
        folder_config = {
            "path": TRAJ_PATH,
            "prefix": TRAJ_PREFIX,
            "suffix": TRAJ_SUFFIX
        }
        return folder_config

    def call_open_devin(self, repo_path, issue_path):
        pass

    def call_swe_agent(self, repo_path, issue_path):
        # 定义发送到接口的数据
        data = {
            "model_name": self.model_name,
            "repo_path": repo_path,
            "data_path": issue_path,
            "config_file": "config/default_from_url.yaml"
        }
        json_data = json.dumps(data)
        response = requests.post(self.swe_agent_url, json=json_data)
        print("Status Code:", response.status_code)
        print("Response Body:", response.json())
        return response.json()

    def call_agent(self, repo_path, issue_path):
        if self.agent_type == "SWE-Agent":
            self.call_swe_agent(repo_path=repo_path, issue_path=issue_path)
        elif self.agent_type == "OpenDevin":
            self.call_open_devin(repo_path=repo_path, issue_path=issue_path)

    def collect_patch(
        self,
        target_patch_path,
        issue_name
    ):
        patch_folder_path = self.swe_config["folder_config"]["path"] + self.swe_config["folder_config"]["prefix"] + issue_name + self.swe_config["folder_config"]["suffix"] + "/patches"
        all_patches = os.listdir(patch_folder_path)
        patch_files = [file for file in all_patches if file.endswith('.patch')]
        agent_patch_path = patch_folder_path + "/" + patch_files[0]
        shutil.copy(agent_patch_path, target_patch_path)
        print(issue_name, "patch collected.")

    def judge_finish(
            self,
            issue_name
    ):
        fix_path = self.swe_config["folder_config"]["path"] + self.swe_config["folder_config"]["prefix"] + issue_name + \
        self.swe_config["folder_config"]["suffix"]
        if os.path.exists(fix_path):
            return True
        else:
            return False

    def collect_traj(
        self,
        collected_traj_path,
        issue_name
    ):
        traj_folder_path = self.swe_config["folder_config"]["path"] + self.swe_config["folder_config"]["prefix"] + issue_name + self.swe_config["folder_config"]["suffix"]
        all_trajs = os.listdir(traj_folder_path)
        traj_files = [file for file in all_trajs if file.endswith('.traj')]
        agent_traj_path = traj_folder_path + "/" + traj_files[0]
        shutil.copy(agent_traj_path, collected_traj_path)
        print(issue_name, "traj collected.")