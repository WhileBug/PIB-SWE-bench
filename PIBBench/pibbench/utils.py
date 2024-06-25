import re
import pandas as pd

def load_dataset(parquet_name):
    return pd.read_parquet(parquet_name)

def parse_patch(patch_file):
    # Regular expressions to match patch lines
    file_regex = re.compile(r'^diff --git a/(.+\.py) b/\1')
    hunk_header_regex = re.compile(r'^@@ -(\d+),\d+ \+(\d+),\d+ @@')

    modified_files = {}

    with open(patch_file, 'r') as file:
        lines = file.readlines()

    current_file = None
    current_hunk_start = None

    for line in lines:
        file_match = file_regex.match(line)
        if file_match:
            current_file = file_match.group(1)
            modified_files[current_file] = set()
            continue

        if current_file:
            hunk_match = hunk_header_regex.match(line)
            if hunk_match:
                current_hunk_start = int(hunk_match.group(2))
                continue

            if current_hunk_start is not None:
                if line.startswith('+') and not line.startswith('+++'):
                    modified_files[current_file].add(current_hunk_start)
                if not line.startswith('-'):
                    current_hunk_start += 1

    return modified_files

def generate_placeholder_patch(modified_files):
    patch_lines = []
    for file, lines in modified_files.items():
        lines = sorted(lines)
        if lines:
            patch_lines.append(f'diff --git a/{file} b/{file}')
            patch_lines.append(f'--- a/{file}')
            patch_lines.append(f'+++ b/{file}')
            line=lines[0]
            patch_lines.append(f'@@ -{line},0 +{line},1 @@')
            patch_lines.append(f'+# [PLACEHOLDER]')
    return '\n'.join(patch_lines)