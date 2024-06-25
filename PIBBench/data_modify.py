import pandas as pd
from pibbench.utils import parse_patch, generate_placeholder_patch

dev_path = "original_data/dev-00000-of-00001.parquet"
test_path = "original_data/test-00000-of-00001.parquet"
train_path = "original_data/train-00000-of-00001.parquet"

dev_df = pd.read_parquet(dev_path)
test_df = pd.read_parquet(test_path)
train_df = pd.read_parquet(train_path)

def generate_placeholders(parse_df, csv_name, parquet_name):
    placeholder_patches = []
    instance_num = 0
    for instance_idx, instance_map in parse_df.iterrows():
        instance_num += 1
        patch = instance_map["patch"]
        with open("temp.patch", "w+") as f:
            f.write(patch)
        modified_files = parse_patch("temp.patch")
        placeholder_patch = generate_placeholder_patch(modified_files)
        placeholder_patches.append(placeholder_patch)
    parse_df["placeholder_patch"] = placeholder_patches
    parse_df.to_parquet(parquet_name)

generate_placeholders(dev_df, "data/dev.csv", "data/dev-00000-of-00001.parquet")
generate_placeholders(test_df, "data/test.csv", "data/test-00000-of-00001.parquet")
generate_placeholders(train_df, "data/train.csv", "data/train-00000-of-00001.parquet")