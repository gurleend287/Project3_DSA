from node import Node
from sklearn.metrics.pairwise import cosine_similarity
from collections import deque
import csv
import os


class Graph:
    def __init__(self, threshold_map):
        self.adj_list = {}
        self.threshold_map = threshold_map
        self.size=0; 
        self.num = 0
    
    # helper function
    # returns similarity score used to determine if two nodes should be connected
    def find_similarity(self, node1: Node, node2: Node):
        features1 = [node1.danceability, node1.energy, node1.valence, node1.tempo]
        features2 = [node2.danceability, node2.energy, node2.valence, node2.tempo]
        
        # reshape
        features1 = [features1]
        features2 = [features2]
        
        return cosine_similarity(features1, features2)[0][0]
    
    # add edge between nodes if similarity score theshold is met
    # similary score is weight of edge
    def add_edge(self, node1: Node, node2: Node):
        # avoid adding edge from a node to itself
        if node1.track_id.strip().lower() == node2.track_id.strip().lower():
            return
        
        sim_score = self.find_similarity(node1, node2)
        # getting high similarity scores for most nodes
        # 0.9999995 is good threshold for sparse graph - obtained through trial and error
        if sim_score >= 0.9999995:
            key1 = (node1.track_id, node1)
            key2 = (node2.track_id, node2)
            self.adj_list[key1].append((key2, sim_score))
            self.adj_list[key2].append((key1, sim_score))
    
    # add node to graph based on mood theshold criteria and connect edges
    def add_node(self, node: Node, cols: list[str]):
        for col in cols:
            if getattr(node, col) < self.threshold_map[col][0] or getattr(node, col) > self.threshold_map[col][1]:
                return # node not added
        
        key = (node.track_id, node)
        if node.track_id not in self.adj_list:
            self.adj_list[key] = []
        self.size += 1 #update the size of graph

    # depth first traversal
    def dfs(self, start: Node, visited=None, out_file="dfs.csv"):
        if visited is None:
            visited = set()

        visited.add(start.track_id)

        # create new csv file with the following:
        # track_id, popularity, duration_ms, danceability, energy, loudness, intrumentalness, valence, tempo, track_genre
        with open(out_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([start.track_id, start.popularity, start.duration_ms, start.danceability,
                             start.energy, start.loudness, start.instrumentalness, start.valence, start.tempo, start.track_genre])

        for neighbor, _ in self.adj_list.get((start.track_id, start), []):
            neighbor_node = neighbor[1]
            if neighbor_node.track_id not in visited:
                self.dfs(neighbor_node, visited)

    # breath first traversal    
    def bfs(self, start: Node, out_file="bfs.csv"):
        visited = set() # stored in a set to have once only 
        queue = deque([start])

        # remove existing file
        if os.path.exists("bfs.csv"):
            os.remove("bfs.csv")
        
        while queue:
            start = queue.popleft()
            
            if start.track_id not in visited:
                visited.add(start.track_id)

                # write data to csv file
                with open(out_file, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([start.track_id, start.popularity, start.duration_ms, start.danceability,
                                     start.energy, start.loudness, start.instrumentalness, start.valence, start.tempo, start.track_genre])
                
                for neighbor, _ in self.adj_list[(start.track_id, start)]:
                    queue.append(neighbor[1])
         # prints out in bfs order            
        for track_id in visited:
                node = next((node for key, node in self.adj_list.keys() if key == track_id), None)
                if node:
                    bfs_vector.append(node)
        return bfs_vector

    def bfs_print(self, start_node: Node):
        bfs_vector = self.bfs(start_node)
        for song in bfs_vector:
            print(f"{song.track_name} - {song.artists}")
