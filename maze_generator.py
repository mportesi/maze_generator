import numpy as np
import random
import os
from colorama import init, Fore
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import copy
import argparse

##### MAZE GENERATOR #####
# https://en.wikipedia.org/wiki/Maze_generation_algorithm
# generate a maze using numpy
# 
# Implemented algorithms:
# - Prim's 
# - depth-first

WALL = 0
CORRIDOR = 1

#################################################
#for debugging
init()
def print_maze(maze):
    for i in range(maze.shape[0]):
        for j in range(maze.shape[1]):
            if maze[i][j] == 1:
                print(Fore.WHITE, f'{maze[i][j]}', end="")
            else:
                print(Fore.RED, f'{maze[i][j]}', end="")
        print('\n')
#################################################


def new_maze(width, height):
    maze = np.full((height, width),WALL,int)
    return maze


def get_frontier_cells(cell, maze):
    frontier=[]
    if cell[0]<(maze.shape[0]-3):
        if maze[cell[0]+2][cell[1]] == WALL:
            frontier.append([cell[0]+2,cell[1]])
    if cell[0]>2:
        if maze[cell[0]-2][cell[1]] == WALL:
            frontier.append([cell[0]-2,cell[1]])
    if cell[1]<(maze.shape[1]-3):
        if maze[cell[0]][cell[1]+2] == WALL:
            frontier.append([cell[0],cell[1]+2])
    if cell[1]>2:
        if maze[cell[0]][cell[1]-2] == WALL:
            frontier.append([cell[0],cell[1]-2])
    return frontier

def get_connection(cell, maze):
    conn=[]
    if cell[0]<(maze.shape[0]-2):
        if maze[cell[0]+2][cell[1]] == CORRIDOR:
            conn.append([cell[0],cell[1],cell[0]+1, cell[1]])
    if cell[0]>1:
        if maze[cell[0]-2][cell[1]] == CORRIDOR:
            conn.append([cell[0],cell[1],cell[0]-1,cell[1]])
    if cell[1]<(maze.shape[1]-2):
        if maze[cell[0]][cell[1]+2] == CORRIDOR:
            conn.append([cell[0],cell[1],cell[0],cell[1]+1])
    if cell[1]>1:
        if maze[cell[0]][cell[1]-2] == CORRIDOR:
            conn.append([cell[0],cell[1],cell[0],cell[1]-1])
    return conn

#####
# Generate maze using Prim's algorithm
#####
def prim_maze(width, height):
    mazelist=[] # for animating
    maze = new_maze(width, height)
    for temp in range(10):
        mazelist.append(copy.deepcopy(maze))

    # select random starting point..
    start_h = int(random.random()*height)
    start_w = int(random.random()*width)
    # ..NOT on the edge of the maze!
    if start_h <= 2:
        start_h += 3
    if start_h >= height-3:
        start_h -= 3
    if start_w <= 2:
        start_w += 3
    if start_w >= width-3:
        start_w -= 3

    # the starting point become a path, and we add the frontiers
    maze[start_h][start_w] = CORRIDOR
    
    mazelist.append(copy.deepcopy(maze))
    frontiers = []
    frontiers.append([start_h-2, start_w])
    frontiers.append([start_h, start_w+2])
    frontiers.append([start_h+2, start_w])
    frontiers.append([start_h, start_w-2])

    # Frontiers of a cell are unvisited cells at distance + 1

    # while there are Frontiers in the list, pick a random one.
    # Then, pick a random connection to a visited cell in the frontier range
    #   1) Make the wall a passage and mark the unvisited cell as part of the maze.
    #   2) Add the frontiers of the cell to the frontiers list.
    # Remove the frontier from the list.
    while frontiers:
        rand_front =frontiers[random.randint(0, len(frontiers)-1)]
       
        front_connections =get_connection(rand_front,maze)
   
        if front_connections:
            rand_connection = front_connections[random.randint(0,len(front_connections)-1)]
            maze[rand_connection[0]][rand_connection[1]]=CORRIDOR
            maze[rand_connection[2]][rand_connection[3]]=CORRIDOR
            temp_front =  get_frontier_cells(rand_front, maze)
            for a in temp_front:
                if (a not in frontiers):
                    frontiers.append(a)
            temp_front.clear()
        front_connections.clear()
        frontiers.remove(rand_front)
        mazelist.append(copy.deepcopy(maze))
    return maze, mazelist

#####
# Generate maze using randomized depth first search algorithm
#####
def get_neighbours_with_connection(cell, maze):
    frontier=[]
    if cell[0]<(maze.shape[0]-3):
        if maze[cell[0]+2][cell[1]] == WALL:
            frontier.append([cell[0]+2,cell[1], cell[0]+1, cell[1]])
    if cell[0]>2:
        if maze[cell[0]-2][cell[1]] == WALL:
            frontier.append([cell[0]-2,cell[1],cell[0]-1, cell[1]])
    if cell[1]<(maze.shape[1]-3):
        if maze[cell[0]][cell[1]+2] == WALL:
            frontier.append([cell[0],cell[1]+2, cell[0], cell[1]+1])
    if cell[1]>2:
        if maze[cell[0]][cell[1]-2] == WALL:
            frontier.append([cell[0],cell[1]-2, cell[0], cell[1]-1])
    return frontier

def depth_first_maze(width, height):
    mazelist=[] # for animating
    back_stack=[]
    maze = new_maze(width, height)
    for temp in range(10):
        mazelist.append(copy.deepcopy(maze))

    # select random starting point.. 1-N, 2-S, 3-WE, 4_E
    face = int(random.randint(1,4))
    start_h = 1
    start_w = 1
    if face == 1:
        start_w = int(random.random()*width)
    if face == 2:
        start_h = height-1
        start_w = int(random.random()*width)
    if face == 3:
        start_h = int(random.random()*height)
    if face == 4:
        start_w = width-1
        start_h= int(random.random()*height)

    maze[start_h][start_w] = CORRIDOR
    back_stack.append([start_h, start_w])
    mazelist.append(copy.deepcopy(maze))

    neighbours=[]
    
    while back_stack:
        temp_neigh = get_neighbours_with_connection(back_stack[-1], maze)
        if len(temp_neigh) == 0:
            back_stack.pop()
        else:
            rand_neigh = temp_neigh[random.randint(0,len(temp_neigh)-1)]
            back_stack.append([rand_neigh[0], rand_neigh[1]])
            maze[rand_neigh[0]][rand_neigh[1]]=CORRIDOR
            maze[rand_neigh[2]][rand_neigh[3]]=CORRIDOR
            mazelist.append(copy.deepcopy(maze))
    return maze, mazelist

# TO-DO
# def create_entrance_exit(maze):

def main(algo):
    mazelist =[]
    imagelist=[]
    if algo == "prim":
        newmaze, mazelist = prim_maze(50,40)
    elif algo == "depth":
        newmaze, mazelist = depth_first_maze(50,40)
    else:
        newmaze, mazelist = prim_maze(50,40)

    # save image of the maze
    plt.imshow(newmaze,cmap='gray')
    os.makedirs('mazes/image', exist_ok=True)
    plt.imsave('mazes/image/sample'+".png",newmaze, dpi=1200, cmap='gray')

    # create animation of the maze
    fig = plt.figure(dpi=150, constrained_layout = True)
    fig.patch.set_facecolor('black')

    plt.axis("off")
    counter=0
    movie_image_step = len(mazelist) // 200
    if movie_image_step == 0:
        movie_image_step = 1
    for i in mazelist:
        if counter%movie_image_step==0:
            imagelist.append((plt.imshow(i, cmap='gray'),))
        counter+=1

    for aa in range(40):
        imagelist.append((plt.imshow(newmaze, cmap='gray'),))
    im_ani = animation.ArtistAnimation(
        fig, imagelist, interval=45, repeat_delay=3000, blit=False
    )
    os.makedirs('mazes/video', exist_ok=True)
    im_ani.save(('mazes/video/sample.gif'))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Maze generator. By default, produce a maze using Prim's algorithm."
    )
    parser.add_argument(
        "-a", type=str, default="prim", help="algorithm to use."
    )    
    args = parser.parse_args()
    main(args.a)