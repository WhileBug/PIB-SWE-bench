from PIBBench.pibbench.agent_frontend import AgentFrontend
from PIBBench.pibbench.repository import InstanceRepo
from PIBBench.pibbench.utils import load_dataset
import json

def pred_json_generate(instance_id, model_patch, model_name, pred_json_filename):
    pred_dict = {
        "instance_id": instance_id,
        "model_patch": model_patch,
        "model_name_or_path": model_name
    }
    with open(pred_json_filename, "w+") as f:
        json.dump(pred_dict, f)

def evaluate_pipeline(pred_path, bench_path, log_dir, testbed):
    evaluate_command = f'''
    python run_evaluation.py \
    --predictions_path {pred_path} \
    --swe_bench_tasks {bench_path} \
    --log_dir {log_dir} \
    --testbed {testbed}
    '''

def generate_pred_patches_pipeline(agent_name="SWE-Agent"):
    agent_frontend = AgentFrontend(agent_type=agent_name)
    test_df = load_dataset(
        "/Users/whilebug/Desktop/Projects/PIB-SWE-bench/PIBBench/original_data/train-00000-of-00001.parquet")
    for key, instance_info in test_df.iterrows():
        repo_name = instance_info["repo"]
        instance_id = instance_info["instance_id"]
        base_commit = instance_info["base_commit"]
        problem_statement = instance_info["problem_statement"]
        placeholder_patch = instance_info["placeholder_patch"]
        repo_path = "tmp/" + instance_id
        instance_repo = InstanceRepo(
            instance_id=instance_id,
            repo_path=repo_path,
            repo_name=repo_name,
            base_commit=base_commit,
            placeholder_patch=placeholder_patch
        )
        instance_repo.clone_repo()
        instance_repo.placeholder_add()

        issue_path = instance_id + ".md"
        with open(issue_path, "w+") as f:
            f.write(problem_statement)
        agent_frontend.call_agent(
            repo_path=repo_path,
            issue_path=issue_path
        )
        agent_frontend.collect_patch(
            target_patch_path=instance_id + ".patch",
            issue_name=instance_id
        )
        with open(instance_id+".patch", "r") as f:
            model_patch = f.read()
        pred_json_generate(
            instance_id=instance_id,
            model_patch=model_patch,
            model_name=agent_name,
            pred_json_filename=instance_id+".json"
        )
        evaluate_pipeline(
            pred_path=instance_id+".json",
            bench_path=instance_id+".json",
            log_dir=instance_id+".json",
            testbed=instance_id+".json"
        )

