#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import networkx as nx
import covasim as cv
import numpy as np
import igraph as ig
from igraph import *
from scipy import stats
from pandas import DataFrame
import numpy as np
from igraph import Graph
from igraph import plot
from igraph import GraphBase
from igraph.clustering import*
from scipy import stats
import igraph
from igraph import Clustering
from igraph import VertexDendrogram
from igraph import VertexClustering
import pandas as pd
import networkx as nx

def normalize(matrix):
    return stats.zscore(matrix)


def graph3(x):
    test1 = np.array(x)
    graphx = Graph.Adjacency(test1.tolist(), mode='UNDIRECTED')
    graphx1= GraphBase.simplify(graphx,multiple=True, loops=True, combine_edges=None)
    return graphx1


def assortativity(x):
    coefficient_assortativity=GraphBase.assortativity_degree(x, directed=False)
    return coefficient_assortativity

def Shannon_entropy(distribution):
    entropia=stats.entropy(distribution)
    return entropia
def average_path_length(x):
    apl=GraphBase.average_path_length(x,directed=False, unconn=True)
    return apl

def calculate_betweenness(x):
    bc = np.mean(sorted(GraphBase.betweenness(x)))
    return bc

def calculate_closeness(x):
    cc=GraphBase.closeness(x)
    ##for i in cc:
     #   close= np.mean(i)
    #return close
    return np.mean(cc)

def diameter(x):
    d=GraphBase.diameter(x,directed=False)
    return d

def calculate_eigenvector(x):
    e=np.mean(sorted(GraphBase.eigenvector_centrality(x,directed=False)))
    return e

def hub_score(x):
    h=np.mean(sorted(GraphBase.hub_score(x,weights=None)))
    return h

#def independence_number(x):
 #   i=GraphBase.independence_number(x)
  #  return i

def knn(x):
    y= GraphBase.knn(x)
    for i in y:
        k= np.nanmean(sorted(i))
    return k

def calculate_pagerank(x):
    p=np.mean(Graph.pagerank(x, vertices=None, directed=True, damping=0.85))
    return p

def calculate_transitivity(x):
    t=GraphBase.transitivity_undirected(x)
    return t

#def modularity(x):
 #   m=GraphBase.modularity(x)
  #  return m

def calculate_mean_degree(x):
    t= np.mean(GraphBase.degree(x, mode='ALL', loops=True))
    return t

def second_moment(x):
    t=np.var(GraphBase.degree(x, mode='ALL', loops=True))
    return t

def entropy_degree_sequence(x):
    entropia=Shannon_entropy(sorted(GraphBase.degree(x, mode='ALL', loops=True)))
    return entropia

def Shannon_entropy(distribution):
    entropia=stats.entropy(distribution)
    return entropia


def complexidade(x):
   media_grau = np.mean(sorted(GraphBase.degree(x, mode='ALL', loops=True)))
   segundo_momento = np.var(sorted((GraphBase.degree(x, mode='ALL', loops=True))))
   return (segundo_momento / media_grau)
# np.seterr(divide='ignore')

def calculate_kcore(x):
    t=np.mean(Graph.coreness(x,mode='ALL'))
    return t

def nodal_eff(g):
    """
    This function calculates the nodal efficiency of a weighted graph object.
    Created by: Loukas Serafeim (seralouk), Nov 2017

    Args:
     g: A igraph Graph() object.
    Returns:
     The nodal efficiency of each node of the graph
    """

    sp = Graph.shortest_paths_dijkstra(g,weights = None)
    sp = np.asarray(sp)
    with np.errstate(divide='ignore'):
        temp = 1.0 / sp
    np.fill_diagonal(temp, 0)
    N = temp.shape[0]
    ne = ( 1.0 / (N - 1)) * np.apply_along_axis(sum, 0, temp)
    for i in ne:
        t=np.mean(sorted(ne))
    return t

def diversity(x):
    u=GraphBase.diversity(x, weights=None)
    return(np.mean(u))

def eccentricity(x):
    u=GraphBase.eccentricity(x)
    return np.mean(u)

def edge_conectivity(x):
    clusters    = x.clusters()
    giant       = clusters.giant() ## using the biggest component as an example, you can use the others here.
    #communities = giant.community_spinglass()
    t= GraphBase.edge_connectivity(giant)
    return t
def reciprocity(x):
    u= GraphBase.reciprocity(x,ignore_loops=True, mode="default")
    return u
def average_path_length(x):
    apl=GraphBase.average_path_length(x,directed=False, unconn=True)
    return apl

def tree_spaning(x):
    s=Graph.spanning_tree(x)
    return s

def community_fastgreedy(x):
    u= Graph.community_fastgreedy(x, weights=None)
    t= VertexDendrogram.as_clustering(u)
    return t

def community_infomap(x):
    u= Graph.community_infomap(x, edge_weights=None)

    return u



def community_leading_eigenvector(x):
    u= Graph.community_leading_eigenvector(x)
    return u

def community_label_propagation(x):
    u=Graph.community_label_propagation(x,weights=None)
    return u


def community_multilevel(x):
    u=Graph.community_multilevel(x, weights=None, return_levels=False)
    return u

def community_edge_betweenness(x):
 #   clusters    = x.clusters()
    clusters    = x.connected_components()
    giant       = clusters.giant() ## using the biggest component as an example, you can use the others here.
    #communities = giant.community_spinglass()
    #t= GraphBase.edge_connectivity(giant)
    u= Graph.community_edge_betweenness(giant, directed=False, weights=None)
    return u

def community_spinglass(x):
  #  clusters    = x.clusters()
    clusters    = x.connected_components()
    giant       = clusters.giant() ## using the biggest component as an example, you can use the others here.
    communities = giant.community_spinglass()

    #u=Graph.community_spinglass(x)
    #return u
    return communities

def community_walktrap(x):
   # clusters    = x.clusters()
    clusters    = x.connected_components()
    giant       = clusters.giant() ## using the biggest component as an example, you can use the others here.
    #communities = giant.community_spinglass()
    #t= GraphBase.edge_connectivity(giant)
    u= Graph.community_walktrap(giant, weights=None)
    
def compute_all_features(g):
    betweenness= calculate_betweenness(g)
    closeness= calculate_closeness(g)       
    eigenvector= calculate_eigenvector(g)
    transitivity= calculate_transitivity(g)
    pagerank= calculate_pagerank(g)
       
    mean_distribution_degree= calculate_mean_degree(g)
        
    kcore=calculate_kcore(g)

    list_final = [betweenness,closeness,eigenvector,transitivity,pagerank,mean_distribution_degree,kcore]
  #  list_final = [betweenness,eigenvector,transitivity,pagerank,mean_distribution_degree,kcore]
     
    return list_final
