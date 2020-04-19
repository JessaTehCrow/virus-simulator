import pygame
import time
import utils
import graph

pygame.init()

#############################################
### ==---==--==    SETTINGS    ==--==--== ###
#############################################
nodes = 800             #Amount of nodes in final simulation
speed = 1.5             #Max speed of nodes
infection_range = 20    #Range of infection around infected nodes
width = 900             #Image width   
height = 900            #Image height
rec_time_min = 300      #Recover time for node to either die / recover
rec_time_max = 2400     #Recover time for node to either die / recover
#############################################
### ==---==--==    SETTINGS    ==--==--== ###
#############################################

tot = nodes
nodes = utils.get_nodes(nodes,[width,height],speed=speed,irange=infection_range,rec_max=rec_time_max,rec_min=rec_time_min)

screen = pygame.display.set_mode([width,height])
pygame.display.set_caption("Realtime")

frame = 0
data = []

running = True
while running:
    frame += 1
    screen.fill([0,0,0])

    if frame % 10 == 0:
        data.append([])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        pass

    for x in nodes:
        if frame % 10 == 0:
            data[int(frame/10)-1].append([x.infected,x.recovered,x.died])
        x.move()

        if x.infected:
            pygame.draw.circle(screen,(255,0,0),[int(x.x),int(x.y)],2)
            x.update(nodes,frame)
        elif x.recovered:
            pygame.draw.circle(screen,(100,100,100),[int(x.x),int(x.y)],2)
        elif x.died:
            pygame.draw.circle(screen,(0,0,255),[int(x.x),int(x.y)],2)
        else:
            pygame.draw.circle(screen,(255,255,255),[int(x.x),int(x.y)],2)

    pygame.display.flip()
    pygame.time.wait(10)

print("Generating graph...")
final = graph.make_graph(data,healthy=tot)
graph.base_graph(final,tot)