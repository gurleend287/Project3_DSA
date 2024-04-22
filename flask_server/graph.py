from node import Node
from sklearn.metrics.pairwise import cosine_similarity
from collections import deque


class Graph:
    def __init__(self, threshold_map):
        self.adj_list = {}
        self.threshold_map = threshold_map
        self.size=0; 
    
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
        sim_score = self.find_similarity(node1, node2)
        # print(sim_score)
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
        self.size+=1 #update the size of graph
    
    #traverse depth first (code sourced from powerpoint 8a)
    def dfs_traversal(self, start_node: Node):
        dfs_vector= [] #store the nodes traversal order here

        # broken code, revisit later
        # visited = set() #stores visited nodes 
        # stack = [start_node] #keep the order of nodes to visit

        # #start off with the source node 
        # visited.add(start_node.track_id)
        
        # while stack:
        #     #u=stack[-1] #check top of the stack
        #     #dfs_vector.append(u)
        #     u=stack.pop()
        #     dfs_vector.append(u)
        #     print(u)
        
        #     neighbors = self.adj_list[(u)]

        #     for x in neighbors:
        #         if x not in visited:
        #             visited.add(x[1])
        #             stack.append(x)

        visited = set() # stored in a set to have once only 
        stack = [start_node] # stack is primary structure for dfs 
        
        while stack:
            current_node = stack.pop()
            
            if current_node.track_id not in visited:
                visited.add(current_node.track_id)
                
                for neighbor, _ in self.adj_list[(current_node.track_id, current_node)]:
                    stack.append(neighbor[1])

         # prints out in dfs order            
        for track_id in visited:
                node = next((node for key, node in self.adj_list.keys() if key == track_id), None)
                if node:
                    dfs_vector.append(node)

        return dfs_vector
        
    def dfs_print(self, start_node: Node):
        dfs_vector= self.dfs_traversal(start_node)
        for song in dfs_vector:
             print(f"{song.track_name} - {song.artists}")

     # searches through nodes using bfs algorithm     
    def bfs(self, start_node: Node):
        bfs_vector = []
        visited = set() # stored in a set to have once only 
        queue = deque([start_node])
        
        while queue:
            current_node = queue.popleft()
            
            if current_node.track_id not in visited:
                visited.add(current_node.track_id)
                
                for neighbor, _ in self.adj_list[(current_node.track_id, current_node)]:
                    queue.append(neighbor[1])
         # prints out in bfs order            
        for track_id in visited:
                node = next((node for key, node in self.adj_list.keys() if key == track_id), None)
                if node:
                    bfs_vector.append(node)
        return bfs_vector
        
    def bfs_print(self, start_node: Node):
        bfs_vector = self.bfs_traversal(start_node)
        for song in bfs_vector:
            print(f"{song.track_name} - {song.artists}")

    
