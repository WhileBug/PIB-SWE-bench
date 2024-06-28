from PIBBench.pibbench.instance import Instance
import pandas as pd
from PIBBench.pibbench.utils import parse_patch, insert_placeholder

patch_df = pd.read_parquet(
    "/Users/whilebug/Desktop/Projects/PIB-SWE-bench/PIBBench/pibdataset/data/train-00000-of-00001.parquet"
)
print(patch_df.iloc[0]["placeholder_patch"])
instance_id = "DataDog__integrations-core-10093"
repo_path = "/Users/whilebug/Desktop/Projects/PIB-SWE-bench/PIBBench/tmp/DataDog__integrations-core-10093"
repo_name = "DataDog/integrations-core"
base_commit = "160cfef6e1118061fa66d333e8c2a572f5d0a815"
home_path = "/Users/whilebug/Desktop/Projects/PIB-SWE-bench/PIBBench/tmp"
patch = patch_df.iloc[0]["patch"]

with open("temp.patch", "w+") as f:
        f.write(patch)
modified_files = parse_patch("temp.patch")
insert_placeholder(
        repo_path=repo_path,
        files_lines=modified_files
)