#!/usr/bin/env python
# coding: utf-8

from datetime import datetime
from igraph import *
from igraph.clustering import *
from modules.Module_complex_network import *
from pandas import DataFrame
from scipy import stats
import concurrent.futures
import covasim as cv
import igraph as ig
import networkx as nx
import numpy as np
import os
import pandas as pd
import psutil
import psutil
import resource
import sys
# import threading
import time
import yappi as yi
import multiprocessing

#### process args

if len(sys.argv) < 2:
    print("please provide all mandatory args!")
    print("run_experiment OUTPUT_DIR/ POPULATION_SIZE")
    quit()

print(sys.argv)

#### experiment base setup

experiment = {
    'experiment_base_dir': sys.argv[1],
    'pop_size': sys.argv[2],
    'slurm_task_id': os.getenv('SLURM_ARRAY_TASK_ID'),
    'experiment_date_time': datetime.now().strftime("%Y-%m-%d_%H%M%S")
}

print(experiment)

#### Simulation

def simplify_graph(g):
    g = ig.Graph.TupleList(g.edges(), directed=False)  # Changed 'ig' to 'ig.Graph' here
    g1 = ig.GraphBase.simplify(g, multiple=True, loops=True, combine_edges=None)  # Changed 'GraphBase.simplify' to 'ig.GraphBase.simplify' here
    return g1

# Function to get all people
def get_all_people(people):
    return people.uid

# Function to simulate and save results
def simulate_and_save_results(s_val, c_val, w_val, _pop_size):
    pars = dict(
        pop_size=_pop_size,
        # pop_infected=_pop_size * 0.25, # prior setting
        pop_infected=_pop_size * 0.045,  # updated 2024-05-14
        beta=0.01825,  # Calibrate overall transmission to this setting
        rel_severe_prob=0.6558,
        rel_crit_prob=0.9404,
        pop_type='hybrid',
        location='germany',
        rand_seed=0,
        n_days=100
    )
    
    interventions1 = cv.clip_edges([1], [s_val], layers=['s'])
    interventions2 = cv.clip_edges([1], [c_val], layers=['c'])
    interventions3 = cv.clip_edges([1], [w_val], layers=['w'])

    sim = cv.Sim(pars=pars, interventions=[interventions1, interventions2, interventions3])
    sim.run()
    G_nx = sim.people.contacts.to_graph()
    G = simplify_graph(G_nx)

    list_final = compute_all_features(G)
    # Create Multisim with 5 seeds
    sim.initialize()
    sim = cv.Sim(pars=pars, interventions=[interventions1, interventions2, interventions3])
    msim = cv.MultiSim(sim, n_runs=5)
    msim.run()

    # Get the average results from Multisim
    msim.reduce()
    #avg_sim = msim.results.average()  # Change this line to access the average results
    infected = msim.results['n_infectious'].values
    critical = msim.results['n_critical'].values
    severe = msim.results['n_severe'].values
     
    index = [(s_val, c_val, w_val)]
    list_final.extend(index)
    list_final.append(infected)
    list_final.append(critical)
    list_final.append(severe)
    return list_final

def simulate_and_save_results_wrapper(args):
    s_val, c_val, w_val = args
    result = simulate_and_save_results(s_val, c_val, w_val)
    return result

# HPC specific
# load simulation data by using slurm_task_id as an index on the list 
def load_experiment_csv():
    # Load the CSV file into a DataFrame
    df = pd.read_csv(experiment['experiment_base_dir'] + "/Experiments/experiment_setup.csv")

    # Get a row by its index
    row_index = int(experiment['slurm_task_id'])
    row = df.iloc[row_index]

    return row.iloc[0], row.iloc[1], row.iloc[2]

#### main function
    
def run():
    # load simulation parameters from experiment list
    s_val, c_val, w_val = load_experiment_csv()

    # setup output directory
    output_folder = experiment['experiment_base_dir'] + "Experiments/" + experiment['pop_size'] + 'k' + "/" + experiment['slurm_task_id'] + '_' + str(s_val) + '_' + str(c_val) + '_' + str(w_val)
    os.makedirs(output_folder, exist_ok=True)

    # run simulation
    results = simulate_and_save_results(float(s_val), float(c_val), float(w_val), int(experiment['pop_size']))

    # preprocess the list to convert tuples and arrays to strings
    preprocessed_list = []
    for item in results:
        if isinstance(item, tuple):
            preprocessed_list.append(str(item))  # Convert tuple to string
        elif isinstance(item, np.ndarray):
            preprocessed_list.append(np.array2string(item))  # Convert array to string
        else:
            preprocessed_list.append(item)

    # create DataFrame with results
    df = pd.DataFrame([preprocessed_list], columns=['BC', 'CC', 'EC', 'ClC', 'PR', 'D', 'KC', 'Index', 'Infected-time', 'Critical-time', 'Severe-time'])
    print(df)

    df.to_csv(os.path.join(output_folder, "measures_results.csv"),
        index=None, header=['BC', 'CC', 'EC', 'ClC', 'PR', 'D', 'KC', 'Index', 'Infected-time', 'Critical-time', 'Severe-time'])

#########

run()
