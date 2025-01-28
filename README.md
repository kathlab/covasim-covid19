# Covasim-Covid19 Project
Dockerized Covasim environment with Visual Studio Code support.

Build docker image (Linux x86_64):
---

```
docker build -f Dockerfile -t local/covasimcovid19:latest .
```

Open project in VS Code
---

1. Open VS Code workspace
2. (optional) Add ports forwarding of 8888 and 8889 in VS Code (for Juypter Notebook web app)
3. Dev Containers: Reopen in Container
4. (optional) Install necessary VS Code extensions

Run experiment
---

This project was built to run on a slurm HPC cluster. But you can run experiments on a single local machine as follows:

Experiment settings:
- __EXPERIMENT__: 0-1330
- __POPULATION_SIZE__: Size of the popluation used as a Covasim simulation parameter.
- __Experiments/experiment_setup.csv__: Parameters used in Covasim (each line is an experiment setup)

```
env SLURM_ARRAY_TASK_ID=[EXPERIMENT_INDEX] python3 python/run.py /workspaces/covasim-covid19/ [POPULATION_SIZE]
```

Example: Run experiments 0-1330 with a population size of 5000.

```
for EXPERIMENT in $(seq 0 1330); do
env SLURM_ARRAY_TASK_ID=${EXPERIMENT} python3 python/run.py /workspaces/covasim-covid19/ 70000
done
```

Experiment results
---

The results are saved in these folders: Experiments/[__POPULATION_SIZE__]k/[__EXPERIMENT__]_[__SIMULATION_PARAMETERS__]/
