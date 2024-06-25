from PIBBench.pibbench.agent_frontend import AgentFrontend
from PIBBench.pibbench.repository import InstanceRepo
from PIBBench.pibbench.utils import load_dataset
import json
from PIBBench.pibbench.instance import Instance
import os

def pred_json_generate(instance_id, model_patch, model_name, pred_json_filename):
    pred_dict = {
        "instance_id": instance_id,
        "model_patch": model_patch,
        "model_name_or_path": model_name
    }
    with open(pred_json_filename, "w+") as f:
        json.dump(pred_dict, f)

def evaluate_pass(pred_path, bench_path, log_dir, testbed):
    evaluate_command = f'''
    python run_evaluation.py \
    --predictions_path {pred_path} \
    --swe_bench_tasks {bench_path} \
    --log_dir {log_dir} \
    --testbed {testbed}
    '''

def evaluate_inject(traj_path):
    pass

def evaluate_one_instance(
        instance_info:dict,
        agent_frontend:AgentFrontend,
        bench_dataset_path:str,
        agent_name:str,
        inject_prompt:str=None
):
    repo_name = instance_info["repo"]
    instance_id = instance_info["instance_id"]
    base_commit = instance_info["base_commit"]
    problem_statement = instance_info["problem_statement"]
    placeholder_patch = instance_info["placeholder_patch"]
    repo_path = "tmp/" + instance_id
    instance = Instance(
        instance_id=instance_id,
        repo_path=repo_path,
        repo_name=repo_name,
        base_commit=base_commit,
        placeholder_patch=placeholder_patch,
        home_path="tmp"
    )

    instance.instance_repo.clone_repo()
    instance.instance_repo.placeholder_add()

    '''
    [TODO] For the prompt inject, please specify the inject_prompt when you need
    '''

    if inject_prompt is None:
        pass
    else:
        instance.instance_repo.placeholder_prompt_inject(inject_prompt=inject_prompt)

    with open(instance.issue_path, "w+") as f:
        f.write(problem_statement)
    agent_frontend.call_agent(
        repo_path=repo_path,
        issue_path=instance.issue_path
    )
    agent_frontend.collect_patch(
        target_patch_path=instance.pred_patch_path,
        issue_name=instance_id
    )
    agent_frontend.collect_traj(
        collected_traj_path=instance.pred_traj_path,
        issue_name=instance_id
    )

    with open(instance.pred_patch_path, "r") as f:
        model_patch = f.read()
    pred_json_generate(
        instance_id=instance_id,
        model_patch=model_patch,
        model_name=agent_name,
        pred_json_filename=instance.pred_json_path
    )


    '''
    Evaluate the fix is successful or not
    '''
    evaluate_pass(
        pred_path=instance_id + ".json",
        bench_path=bench_dataset_path,
        log_dir=instance.log_dir_path,
        testbed=instance.test_bed_path
    )
    '''
    [TODO] Please modify the evaluate_inject 
    '''
    evaluate_inject(
        traj_path=instance.pred_traj_path
    )

def generate_pred_patches_pipeline(agent_name="SWE-Agent", bench_dataset_path = "PIBBench/pibdataset"):
    agent_frontend = AgentFrontend(agent_type=agent_name)
    test_df = load_dataset(
        "/Users/whilebug/Desktop/Projects/PIB-SWE-bench/PIBBench/original_data/train-00000-of-00001.parquet")

    for key, instance_info in test_df.iterrows():
        evaluate_one_instance(instance_info, agent_frontend, bench_dataset_path, agent_name)
    os.system("pause")