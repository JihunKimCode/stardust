# Path Finding Simulation
We implemented the pathfinding algorithms in Python using Pygame to visually demonstrate how it finds the optimal path. The algorithm then calculates and displays the most optimal path from start to finish.

## Controls
* The first cell you click is marked in blue and indicates starting point.
* The second cell you click is marked in red and indicates destination.
* After deciding starting point and destination, you click cells to build obstacles which indicates black. Click again to remove obstacle. You can drag to build multiple obstacles.
* Press `1`, `2`, or `3` to select A*, Dijkstra's, or Greedy Best-First Search pathfinding algorithm.
* Press `r` to clear everything
* Press `spacebar` to start pathfinding

## Colors
* Black: Obstacles
* Red: Starting point
* Blue: Destination
* Green: Optimal Path
* Yellow: Node being explored
* Cyan: Node being added to open list

# Reference
https://theory.stanford.edu/~amitp/GameProgramming/AStarComparison.html