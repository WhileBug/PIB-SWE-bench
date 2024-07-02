import git

repo_url = "https://github.com/DataDog/integrations-core.git"
base_repo_path= "/Users/whilebug/Desktop/Projects/PIB-SWE-bench/PIBBench/tmp/DataDog__integrations-core-1013-base"
git.Repo.clone_from(repo_url, base_repo_path)