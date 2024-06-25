# PIB-Bench: LLM Code Agent

## 0-Preinstall

You should have two repositories installation:

- PIB-SWE-bench (We modified from SWE-bench): 
```shell
git clone https://github.com/WhileBug/PIB-SWE-bench.git
cd PIB-SWE-bench
conda env create -f environment.yml
conda activate swe-bench
pip install flask
pip install pandas
pip install pyarrow
```
- SWE-Agent
```shell
git clone https://github.com/princeton-nlp/SWE-agent.git
```
And follow the instructions of SWE-agent.

## 1-Use
You can run the bench by
```shell
cd PIBBench
python main.py
```
Before that, you can modify the pibbench.pipeline.py, and edit the code in
```python
def evaluate_inject(traj_path):
    pass
```
The traj_path stores the traj files which describes all the actions/commands that the agent executes.