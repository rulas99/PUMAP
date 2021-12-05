from dash_apps.auxiliar_functions.here_api import hereRequestRoutes
from dash_apps.auxiliar_functions.mongo import getDataFromMongo

from networkx import Graph, dijkstra_path
from scipy.spatial import cKDTree
from numpy import array, linalg
from pandas import DataFrame

edges = DataFrame(getDataFromMongo('routes','edges'))
nodes = DataFrame(getDataFromMongo('routes','nodes'))

def creat_route_graph(nodes,edges):
	edges = edges[edges.Origen.isin(nodes.Nombre)]
	edges = edges[edges.Destino.isin(nodes.Nombre)]
	G = Graph()

	for row in nodes.itertuples():
		G.add_node(row.Nombre,pos=(row.lon,row.lat))

	edgesW = []
	for row in edges.itertuples():
		edgesW.append((row.Origen,row.Destino,row.Distancia))

	G.add_weighted_edges_from(edgesW)
	nodes0 = [x for  x in G.nodes() if G.degree(x) < 1]

	G.remove_nodes_from(nodes0)

	return G

G = creat_route_graph(nodes,edges)

def findNearest(pt,nodes):
    nB = array([(x,y) for x,y in zip(nodes.lon,nodes.lat)])
    btree = cKDTree(nB)

    dist, idx = btree.query(pt, k=1)

    return idx, dist*(109*1000)


def getRoute_graph(ori,dest):
    try:
        path = dijkstra_path(G,ori,dest)

        line = []
        for i in path:
            pt = nodes[nodes.Nombre==i].copy()
            line.append([pt.lat.iloc[0],pt.lon.iloc[0]])
            del pt

        return line
    
    except:
        return []

def get_hibryd_route(ubi, dest):
    idxO,distO = findNearest([ubi[1],ubi[0]],nodes)
    cveO,latO,lonO=nodes.iloc[idxO][['Nombre','lat','lon']]
    
    idxD,distD = findNearest([dest[1],dest[0]],nodes)
    cveD,latD,lonD = nodes.iloc[idxD][['Nombre','lat','lon']]
    
    pth = []
    if distO>50:
    	print('***'*6,' API al inicio ','***'*6)
    	pth += hereRequestRoutes(ubi,[latO,lonO])

    pth += getRoute_graph(cveO,cveD)
    print('***'*6,' Nodo Inicial: ',cveO,'***'*6)
    print('***'*6,' Nodo Final: ',cveD,'***'*6)
    
    if distD>50:
    	print('***'*6,' API al final ','***'*6)
    	pth += hereRequestRoutes([latD,lonD],dest)
        
        
    return pth


def poly_distance(pth):
    dist = round(sum([linalg.norm(array(pth[i])-array(pth[i+1])) for i in range(len(pth)) if i<len(pth)-1])*(109*1000))
    return int(dist), int(round((dist/.90)/60))

opcD = {'princi':[19.33119605, -99.18459609],
        'anexo':[19.32722693, -99.1827927],
        'mC':[19.33531763, -99.1807629],
        'mU':[19.32458997, -99.17433434],
        'mb':[19.32363581, -99.18857883]}

