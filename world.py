import pygame
from pygame.locals import *
import sys
import numpy as np
from net import Net

## INIT pygame interface
img_size = (486, 426) #img size
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)
screen = pygame.display.set_mode((img_size[0] * 2, img_size[1] * 2))
imp = pygame.image.load("france.jpg").convert()
imp = pygame.transform.scale(imp, (img_size[0] * 2, img_size[1] * 2))
pygame.display.flip()
pygame.display.set_caption('Game')
empty = Color(0,0,0,0)
screen.blit(imp, (0, 0))
###
# init clock
clock = pygame.time.Clock()

# create net of nodes, taking in parameter the number of ants
net = Net(100)


# draw text depending on the mode
def draw_mode(net: Net, mode: int, computation_time: int):
    if mode == 0:
        text_surface = my_font.render(f'By clicking, place city where you want to pass through', False, (0, 0, 0))
        screen.blit(text_surface, (0, 0))
        if net.num_nodes <= 1:
            text_surface = my_font.render(f'Need more than 1 point placed', False, (0, 0, 0))
        else:
            text_surface = my_font.render(f'Press enter to compute', False, (0, 0, 0))
        screen.blit(text_surface, (0, 50))
    elif mode == 1:
        text_surface = my_font.render(f'Press enter to see best result', False, (0, 0, 0))
        screen.blit(text_surface, (0, 0))
        text_surface = my_font.render(f'computation time {computation_time}', False, (0, 0, 0))
        screen.blit(text_surface, (0, 25))
        text_surface = my_font.render(f'Press A or Z to modify cumputation time', False, (0, 0, 0))
        screen.blit(text_surface, (0, 50))
    elif mode == 2:
        text_surface = my_font.render(f'Press enter to reset map', False, (0, 0, 0))
        screen.blit(text_surface, (0, 0))

# draw text of mode and net on the screen
def draw(net: Net, mode: int, computation_time: int):
    draw_mode(net, mode, computation_time)
    surface = screen.convert_alpha()  # create surface that handle transparency
    for node in net.nodes:  # iter on node and draw them on surface
        pygame.draw.circle(surface, (0, 0, 255), node, 5)
    screen.blit(surface, (0,0))  #  draw surface on screen

    # in mode 1 connection between nodes are all show, but have an alpha value for their transparency
    if mode == 1:
        # iterate over 2d weights array
        for i in range(0, net.num_nodes):
            for j in range(0, net.num_nodes):
                # if nodes not the same, and connection not null and it's a connection never seen => True
                if (i != j and net.weights[i][j] != 0 and i > j):
                    alpha = int(net.weights[i][j] * 255 / np.max(net.weights))  # calculate transparency of connection
                    surface = screen.convert_alpha()  # create surface that handle transparency
                    pygame.draw.line(surface, (255, 0, 0, alpha), net.nodes[i], net.nodes[j], 3)  # draw line on it
                    screen.blit(surface, (0,0)) #draw it on screen
    # in mode 2 the best solution is shown
    if mode == 2 or mode == 1:
        # iterate over number of nodes
        for i in range(0, net.num_nodes + 1):
            idx1 = net.best_path[i % net.num_nodes]  # current idx node
            idx2 = net.best_path[(i + 1) % net.num_nodes]  # next idx
            pygame.draw.line(screen, (255, 0, 0, 1), net.nodes[idx1], net.nodes[idx2], 3)  # draw line

def run():
    running = True
    mode = 0
    computation_time = 5  # the greater the faster
    while running:
        ### event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            if event.type == pygame.KEYDOWN:
                #switch mode
                if event.key == pygame.K_RETURN:
                    if mode == 0 and net.num_nodes > 1:
                        net.set_net()
                        mode = 1
                        computation_time = 10
                    elif mode == 1:
                        mode = 2
                    elif mode == 2:
                        net.reset_net()
                        mode = 0
                if event.key == pygame.K_a:
                    computation_time += 5
                if event.key == pygame.K_z:
                    computation_time -= 5
                    if computation_time < 5:
                        computation_time = 5
            if mode == 0:
                if event.type == pygame.MOUSEBUTTONUP:
                    net.add_nodes(pygame.mouse.get_pos()) # add nodes to the net
        ###

        screen.blit(imp, (0, 0))  #draw france img
        if mode == 1:
            net.compute_net()  #calculate best path
        draw(net, mode, computation_time)
        pygame.display.update()
        if mode == 0:
            computation_time = 120
        clock.tick(computation_time)  # computation_time's time frame every second

run()