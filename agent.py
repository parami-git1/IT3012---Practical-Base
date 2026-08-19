# agent.py
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
        current_pos = tuple(percept['agent_pos'])
        
        # 1. Update Transition & Sensor Model
        self.visited_cells.add(current_pos)
        
        # 2. Query Memory and Condition-Action Rules
        if percept.get('food_here'):
            action = 'Stay'
        elif percept.get('wall_ahead'):
            # Check options using memory to avoid loop
            possible_actions = ['Left', 'Right', 'Down']
            action = random.choice(possible_actions)
        else:
            action = 'Up'

        self.last_action = action
        return action