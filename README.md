The PIPEMANIA project is an Artificial Intelligence assignment that focuses on solving instances of the classic puzzle game PIPEMANIA using search algorithms. In this game, a square grid contains pipe pieces that can be rotated. The objective is to connect a path from a source (S) to a sink (T) through properly aligned pipes.

Key Components:
State Representation:
Each state represents the current configuration of the board, where each tile's rotation determines how the pipes are connected.

Actions:
The only possible action is rotating a tile 90° clockwise. The solver explores different board configurations by rotating tiles.

Goal Test:
A state is a goal state if there's a valid path connecting the source to the sink through properly connected pipes.

Search Algorithm:
A generic search framework is used (e.g., Breadth-First Search), where states are expanded based on legal moves (rotations), and visited states are tracked to avoid cycles.

Instance Parser:
The solver reads instances from .txt files, where each character represents a pipe piece or empty space.

 Skills Applied:
State space modeling

Uninformed search (BFS)

Efficient state encoding and visited tracking

AI problem-solving strategies

