import pygame
import heapq
import math

# Constants
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 30, 30
CELL_SIZE = WIDTH // COLS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)

# Initialize Pygame
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pathfinding Visualization")

# Font for displaying algorithm name
font = pygame.font.SysFont("Arial", 20)

# Node class
class Node:
    def __init__(self, row, col):
        self.row, self.col = row, col
        self.g = float('inf')  # Cost from start node (for Dijkstra and A*)
        self.h = 0  # Heuristic (for GBFS and A*)
        self.f = float('inf')  # f = g + h (for A*)
        self.parent = None
        self.is_obstacle = False

    def __lt__(self, other):
        return self.f < other.f  # For heapq priority queue

# Grid setup
def reset_grid():
    global grid, start, end
    grid = [[Node(r, c) for c in range(COLS)] for r in range(ROWS)]
    start, end = None, None

reset_grid()

def heuristic(node1, node2):
    return math.sqrt((node1.row - node2.row)**2 + (node1.col - node2.col)**2)

def get_neighbors(node):
    neighbors = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        r, c = node.row + dr, node.col + dc
        if 0 <= r < ROWS and 0 <= c < COLS and not grid[r][c].is_obstacle:
            neighbors.append(grid[r][c])
    return neighbors

def dijkstra():
    global start, end
    if not start or not end:
        return

    for row in grid:
        for node in row:
            node.g = float('inf')
            node.f = float('inf')
            node.parent = None

    start.g = 0
    start.f = 0
    open_list = []
    heapq.heappush(open_list, start)

    visited = set()

    while open_list:
        current = heapq.heappop(open_list)

        if current in visited:
            continue
        visited.add(current)

        if current != start and current != end:
            pygame.draw.rect(win, (255, 255, 0), (current.col * CELL_SIZE, current.row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.display.update()
            pygame.time.delay(20)

        if current == end:
            reconstruct_path(current)
            return

        for neighbor in get_neighbors(current):
            temp_g = current.g + 1
            if temp_g < neighbor.g:
                neighbor.g = temp_g
                neighbor.f = neighbor.g
                neighbor.parent = current
                heapq.heappush(open_list, neighbor)

                if neighbor != start and neighbor != end:
                    pygame.draw.rect(win, (0, 255, 255), (neighbor.col * CELL_SIZE, neighbor.row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                    pygame.display.update()
                    pygame.time.delay(10)

def greedy_best_first_search():
    global start, end
    if not start or not end:
        return

    for row in grid:
        for node in row:
            node.g = float('inf')
            node.f = float('inf')
            node.parent = None

    start.g = 0
    start.f = heuristic(start, end)
    open_list = []
    heapq.heappush(open_list, start)

    visited = set()

    while open_list:
        current = heapq.heappop(open_list)

        if current in visited:
            continue
        visited.add(current)

        if current != start and current != end:
            pygame.draw.rect(win, (255, 255, 0), (current.col * CELL_SIZE, current.row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.display.update()
            pygame.time.delay(20)

        if current == end:
            reconstruct_path(current)
            return

        for neighbor in get_neighbors(current):
            temp_f = heuristic(neighbor, end)
            if temp_f < neighbor.f:
                neighbor.f = temp_f
                neighbor.parent = current
                heapq.heappush(open_list, neighbor)

                if neighbor != start and neighbor != end:
                    pygame.draw.rect(win, (0, 255, 255), (neighbor.col * CELL_SIZE, neighbor.row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                    pygame.display.update()
                    pygame.time.delay(10)

def a_star():
    global start, end
    if not start or not end:
        return

    for row in grid:
        for node in row:
            node.g = float('inf')
            node.f = float('inf')
            node.parent = None

    open_list = []
    heapq.heappush(open_list, start)
    start.g = 0
    start.f = heuristic(start, end)

    visited = set()

    while open_list:
        current = heapq.heappop(open_list)

        if current in visited:
            continue
        visited.add(current)

        if current != start and current != end:
            pygame.draw.rect(win, (255, 255, 0), (current.col * CELL_SIZE, current.row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.display.update()
            pygame.time.delay(20)

        if current == end:
            reconstruct_path(current)
            return

        for neighbor in get_neighbors(current):
            temp_g = current.g + 1
            if temp_g < neighbor.g:
                neighbor.g = temp_g
                neighbor.h = heuristic(neighbor, end)
                neighbor.f = neighbor.g + neighbor.h
                neighbor.parent = current
                heapq.heappush(open_list, neighbor)

                if neighbor != start and neighbor != end:
                    pygame.draw.rect(win, (0, 255, 255), (neighbor.col * CELL_SIZE, neighbor.row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                    pygame.display.update()
                    pygame.time.delay(10)

def reconstruct_path(node):
    while node:
        pygame.draw.rect(win, GREEN, (node.col * CELL_SIZE, node.row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.display.update()
        pygame.time.delay(50)
        node = node.parent

def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            color = BLACK if grid[row][col].is_obstacle else WHITE
            pygame.draw.rect(win, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(win, GRAY, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
    if start:
        pygame.draw.rect(win, RED, (start.col * CELL_SIZE, start.row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    if end:
        pygame.draw.rect(win, BLUE, (end.col * CELL_SIZE, end.row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_algorithm_name(algorithm_name):
    text = font.render(f"Algorithm: {algorithm_name}", True, BLACK)
    win.blit(text, (10, 10))

def main():
    global start, end
    algorithm = 'A*'  # Default algorithm
    running = True
    prev_cell = None
    while running:
        win.fill(WHITE)
        draw_grid()
        draw_algorithm_name(algorithm)  # Display the algorithm name
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            mouse_pressed = pygame.mouse.get_pressed()
            if mouse_pressed[0]:  # Left click
                x, y = pygame.mouse.get_pos()
                row, col = y // CELL_SIZE, x // CELL_SIZE
                cell = (row, col)
                if cell != prev_cell:
                    if not start:
                        start = grid[row][col]
                    elif not end:
                        end = grid[row][col]
                    else:
                        grid[row][col].is_obstacle = not grid[row][col].is_obstacle
                    prev_cell = cell
            else:
                prev_cell = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if algorithm == 'A*':
                        a_star()
                    elif algorithm == 'Dijkstra':
                        dijkstra()
                    elif algorithm == 'Greedy':
                        greedy_best_first_search()
                if event.key == pygame.K_r:  # Reset grid on 'R' key
                    reset_grid()
                if event.key == pygame.K_1:  # Switch to A* algorithm
                    algorithm = 'A*'
                if event.key == pygame.K_2:  # Switch to Dijkstra algorithm
                    algorithm = 'Dijkstra'
                if event.key == pygame.K_3:  # Switch to Greedy Best-First Search
                    algorithm = 'Greedy'

    pygame.quit()

if __name__ == "__main__":
    main()
