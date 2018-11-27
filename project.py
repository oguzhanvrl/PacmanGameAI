# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 16:37:18 2018

@author: Dell
"""

import collections
import heapq



class GameField:
    def __init__(self , width , height , start , goal):
        self.width = width
        self.height = height
        self.walls = []
        self.start = start
        self.goal = goal
    
    def in_bounds(self , location):
        (x, y) = location
        return 0 <= x < self.width and 0 <= y < self.height
    
    def passable(self , location):
        return location not in self.walls
    
    def neighbours(self , location):
        x , y = location
        neighbour_list = [(x+1, y) , (x, y-1) , (x-1, y) , (x, y+1)]
        if (x + y) % 2 == 0: neighbour_list.reverse()
        neighbour_list = filter(self.in_bounds , neighbour_list)
        neighbour_list = filter(self.passable , neighbour_list)
        return neighbour_list
    
 
    
class PriorityField(GameField):
    def __init__(self , width , height , start , goal):
        super().__init__(width , height , start , goal)
        self.weights = {}
    
    def cost(self , from_node , to_node):
        return self.weights.get(to_node , 1)
    
    
    
class Stack:
     def __init__(self):
         self.items = []

     def is_empty(self):
         return len(self.items) == 0

     def put(self, item):
         self.items.append(item)

     def get(self):
         return self.items.pop()


     

class Queue:
    def __init__(self):
        self.items = collections.deque()
    
    def is_empty(self):
        return len(self.items) == 0
    
    def put(self, x):
        self.items.append(x)
    
    def get(self):
        return self.items.popleft()




class PriorityQueue:
    def __init__(self):
        self.items = []
    
    def is_empty(self):
        return len(self.items) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.items, (priority, item))
    
    def get(self):
        return heapq.heappop(self.items)[1]
  
    
    
def find_path(source_locs, start, goal):
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = source_locs[current]
    path.append(start)
    path.reverse()
    return path




def breadth_first_search(game_map,start,goal):# goal sadece hedefin index'i tutuyor algoritmaya etkisi yok
    search_queue = Queue()
    search_queue.put(start)
    source_locs = {}
    source_locs[start] = None
    
    while not search_queue.is_empty():
        current = search_queue.get()
        
        if current == goal:
            break
        
        for next in game_map.neighbours(current):
            if next not in source_locs:
                search_queue.put(next)
                source_locs[next] = current 
    return source_locs




def depth_first_search(game_map,start,goal):# goal sadece hedefin index'i tutuyor algoritmaya etkisi yok
    search_stack = Stack()
    search_stack.put(start)
    source_locs = {}
    source_locs[start] = None
    
    while not search_stack.is_empty():
        current = search_stack.get()
        
        if current == goal:
            break
        
        for next in game_map.neighbours(current):
            if next not in source_locs:
                search_stack.put(next)
                source_locs[next] = current 
    return source_locs



def uniform_cost_search(game_map , start , goal):
    priority_map=PriorityField(game_map.width,game_map.height,game_map.start,game_map.goal)
    priority_map.walls=game_map.walls
    search_queue = PriorityQueue()
    search_queue.put(start, 0)
    source_locs = {}
    cost = {}
    source_locs[start] = None
    cost[start] = 0
    
    while not search_queue.is_empty():
        current = search_queue.get()
        
        if current == goal:
            break
        
        for next in priority_map.neighbours(current):
            new_cost = cost[current] + priority_map.cost(current, next)
            if next not in cost or new_cost < cost[next]:
                cost[next] = new_cost
                priority = new_cost
                search_queue.put(next, priority)
                source_locs[next] = current
    path=find_path(source_locs,start,goal)
    return path , source_locs , cost






def heuristic_function(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)




def a_star_search(game_map, start, goal):
    search_queue = PriorityQueue()
    priority_map=PriorityField(game_map.width,game_map.height,game_map.start,game_map.goal)
    priority_map.walls=game_map.walls
    search_queue.put(start, 0)
    source_locs = {}
    cost = {}
    source_locs[start] = None
    cost[start] = 0
    
    while not search_queue.is_empty():
        current = search_queue.get()
        
        if current == goal:
            break
        
        for next in priority_map.neighbours(current):
            new_cost = cost[current] + priority_map.cost(current, next)
            if next not in cost or new_cost < cost[next]:
                cost[next] = new_cost
                priority = new_cost + heuristic_function(goal, next)
                search_queue.put(next, priority)
                source_locs[next] = current
    path=find_path(source_locs,start,goal)
    return path , source_locs , cost



def main_menu():
    choice=None
    choice=input("""Haritayi gormek icin 1 ,   bfs ile taranmis harita icin 2,     dfs 
              ile taranmis harita icin 3 ,      ucs maliyet,tarama ve yol haritalari icin 4 ,       a* 
              maliyet,tarama ve yol haritalari icin 5'e ,      cikis icin 0'a basiniz.""")
    choice = int(choice)
    if not choice == 0:
        if(choice==1):
            print("OYUN ALANI :")
            draw_field(field,choice)
        elif(choice==2):
            print("BFS HARITASI :")
            draw_field(field,choice,bfs_results)
        elif(choice==3):
            print("DFS HARITASI :")
            draw_field(field,choice,dfs_results)
        elif(choice==4):
            print("UCS HARITASI :")
            draw_field(field,41,ucs_results)
            print("UCS MALIYET HARITASI :")
            draw_field(field,42,ucs_costs)
            print("UCS YOL HARITASI :")
            draw_field(field,43,ucs_path)
        elif(choice==5):
            print("A* HARITASI :")
            draw_field(field,51,ast_results)
            print("A* MALIYET HARITASI :")
            draw_field(field,52,ast_costs)
            print("A* YOL HARITASI :")
            draw_field(field,53,ast_path)
        else:
            print("HATALI KOMUT GIRISI ! ")
        main_menu()
    else:
        print("CIKIS YAPILIYOR ...")
        
        


def draw_field(game_map,draw_type,*args): 
    results = {}
    costs = {}
    path = []
    map_type = 0
    if(draw_type == 2 or draw_type == 3 or draw_type == 41 or draw_type == 51):
        results = args[0]
        map_type = 1
    
    elif(draw_type == 42 or draw_type == 52):
        costs = args[0]
        map_type = 2
    
    elif(draw_type == 43 or draw_type == 53):
        path = args[0]
        map_type = 3
        
    for x in range (game_map.width):
        mapstring=''
        for y in range(game_map.height):
            if((x,y) in game_map.walls):
                mapstring +='X '
            elif((x,y) == game_map.start):
                mapstring+='S '
            elif((x,y) == game_map.goal):
                mapstring+='G '
            elif(map_type == 1 and (x,y) in results):              
                a,b=results[(x,y)]
                if(x>a): #aşağı gitmiş demek
                    mapstring+='v '
                elif(x<a): #yukarı gitmiş demek
                    mapstring+='^ '
                elif(y>a): #sola gitmiş demek
                    mapstring+='< '
                elif(y<a): #sağa gitmiş demek
                    mapstring+='> '
            elif(map_type == 2 and (x,y) in costs):
                c = costs[(x,y)]
                mapstring+= ( str(c)  + ' ')
            elif(map_type == 3 and (x,y) in path):
                mapstring +='**' #bu yolu tercih etmiş demek
                               
            else:
                mapstring+='. '
        print(mapstring)
 

              

starting_point=(8,8)    # başlangıç noktasının index'i
goal_point=(5,9)        # hedef noktasının index'i
field_walls=[(3,3),(3,4),(3,5)]     # oyundaki geçilemeyen duvarların indexleri
field=GameField(15,15,starting_point,goal_point)
field.walls=field_walls

bfs_results = breadth_first_search(field,field.start,field.goal)
dfs_results = depth_first_search(field,field.start,field.goal)
ucs_path,ucs_results,ucs_costs = uniform_cost_search(field,field.start,field.goal)
ast_path,ast_results,ast_costs = a_star_search(field,field.start,field.goal)


main_menu()
      
