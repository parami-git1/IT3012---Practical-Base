# agent.py
from collections import deque
import heapq
import random



class GreedyGridAgent:
    """A simple agent that tries to move around systematically to clear the grid."""

    def __init__(self):
        self.actions_pool = ['Up', 'Down', 'Left', 'Right']

    def sense_and_act(self, percept: dict) -> str:
        # If standing directly on food, or just wander / move towards coordinates
        pos = percept['agent_pos']
        # Simple heuristic or fallback random sweep
        return random.choice(self.actions_pool)



class SimpleReflexAgent:
    """A Simple Reflex Agent using Condition-Action Rules (No Memory)."""

    def __init__(self):
        pass  # Strictly NO memory or state tracking

    def sense_and_act(self, percept: dict) -> str:
        # Condition-Action Rules (IF-THEN logic)
        if percept.get('food_here'):
            return 'Stay'  # Eat food
        elif percept.get('wall_ahead'):
            return 'Left'  # Turn/move left if blocked by a wall
        else:
            return 'Up'    # Default movement forward

    
class ModelBasedAgent:
     """A Model-Based Agent that maintains internal memory to escape loops."""

     def __init__(self):
        self.visited_cells = set()  # Internal State: Memory of visited locations
        self.last_action = None

     def sense_and_act(self, percept: dict) -> str:
        current_pos = tuple(percept.get('agent_pos', (0, 0)))        
        # 1. Update Transition & Sensor Model
        self.visited_cells.add(current_pos)
        
        # 2. Query Memory and Condition-Action Rules
        if percept.get('food_here'):
            action = 'Stay'
        elif percept.get('wall_ahead'):
            # Check options using memory to avoid loop
            if self.last_action == 'Left':
                action = 'Right'
            elif self.last_action == 'Right':
                action = 'Down'
            else:
                action = 'Left'
        else:
            action = 'Up'

        self.last_action = action
        return action

    # Meka agent.py file eke pahalinma (anthimata) danna

class SearchAgent:
    """A Goal-Based/Planning Agent that uses offline simulation (search) to find a path."""

    def __init__(self):
        # Step 1.3.1: Add empty list for plan and config string for active_algo[cite: 2]
        self.plan = [] 
        self.active_algo = 'BFS' 

    def sense_and_act(self, percept: dict) -> str:
        # Step 1.3.2: Check if self.plan is empty[cite: 2]
        if not self.plan: 
            all_food = percept['all_food']
            if not all_food:
                return 'Stay'
            
            start_pos = tuple(percept['agent_pos'])
            
            # Step 1.3.3: Find the closest food pellet[cite: 2]
            closest_food = min(all_food, key=lambda f: abs(f[0]-start_pos[0]) + abs(f[1]-start_pos[1]))
            goal_pos = tuple(closest_food)
            
            walls = percept['walls']
            grid_size = percept['grid_size']

            # Step 1.3.3: Execute the search method matching self.active_algo[cite: 2]
            if self.active_algo == 'BFS':
                self.plan = self.bfs_search(start_pos, goal_pos, walls, grid_size)
            elif self.active_algo == 'DFS':
                self.plan = self.dfs_search(start_pos, goal_pos, walls, grid_size)
            elif self.active_algo == 'UCS':
                self.plan = self.ucs_search(start_pos, goal_pos, walls, grid_size)

            if not self.plan:
                return 'Stay'

        # Step 1.3.4: Return the first action from the plan[cite: 2]
        return self.plan.pop(0) 

    def get_successors(self, state, walls, grid_size):
        """Helper to get valid next states and actions"""
        successors = []
        x, y = state
        width, height = grid_size
        moves = {'Up': (x, y + 1), 'Down': (x, y - 1), 'Left': (x - 1, y), 'Right': (x + 1, y)}
        
        for action, (nx, ny) in moves.items():
            if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in walls:
                successors.append((action, (nx, ny), 1)) # cost is 1 per step
        return successors

    def bfs_search(self, start, goal, walls, grid_size):
        # Step 1.2.3: BFS using a FIFO queue (deque.popleft())[cite: 2]
        frontier = deque([(start, [])])
        # Step 1.2.6: Maintain a reached set to convert to Graph Search and prevent infinite loops[cite: 2]
        reached = {start} 
        
        while frontier:
            current_state, path = frontier.popleft()
            
            if current_state == goal:
                return path
                
            for action, next_state, cost in self.get_successors(current_state, walls, grid_size):
                if next_state not in reached:
                    reached.add(next_state)
                    frontier.append((next_state, path + [action]))
        return []

    def dfs_search(self, start, goal, walls, grid_size):
        # Step 1.2.4: DFS using a LIFO stack (list.pop())[cite: 2]
        frontier = [(start, [])]
        # Step 1.2.6: Reached set for DFS[cite: 2]
        reached = {start} 
        
        while frontier:
            current_state, path = frontier.pop()
            
            if current_state == goal:
                return path
                
            for action, next_state, cost in self.get_successors(current_state, walls, grid_size):
                if next_state not in reached:
                    reached.add(next_state)
                    frontier.append((next_state, path + [action]))
        return []

    def ucs_search(self, start, goal, walls, grid_size):
        # Step 1.2.5: UCS using a Priority Queue (heapq.heappop())[cite: 2]
        frontier = []
        heapq.heappush(frontier, (0, start, []))
        # Step 1.2.6: Reached set for UCS, tracking minimum cost g(n)[cite: 2]
        reached = {start: 0} 
        
        while frontier:
            current_cost, current_state, path = heapq.heappop(frontier)
            
            if current_state == goal:
                return path
                
            for action, next_state, step_cost in self.get_successors(current_state, walls, grid_size):
                new_cost = current_cost + step_cost
                if next_state not in reached or new_cost < reached[next_state]:
                    reached[next_state] = new_cost
                    heapq.heappush(frontier, (new_cost, next_state, path + [action]))
        return []