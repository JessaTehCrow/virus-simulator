from PIL import Image
import cprint
import os
import random

def img_size(img_dir):
    class img_class():
        def __init__(self,width,height):
            self.width = width
            self.height = height

    img = Image.open(img_dir)
    img = img.size
    return img_class(img[0],img[1])

def get_nodes(amount,img,irange=10,speed=5,rec_min=300,rec_max=1200):
    class node():
        def __init__(self,x,y,motion,range,max,infected=False):
            self.range = range
            self.x = x
            self.y = y
            self.motion = motion
            self.maxx = max[0]
            self.maxy = max[1]

            self.last_spread = 0
            self.when_infected = 0
            self.health = random.randint(0,6)
            self.died = False
            self.recover_time = random.randint(rec_min,rec_max)
            self.recovered = False
            self.infected = infected

        def move(self):
            self.x += self.motion[0]
            self.y += self.motion[1]

            if self.x < 0 or self.x > self.maxx:
                self.motion[0] *= -1

            if self.y < 0 or self.y > self.maxy:
                self.motion[1] *= -1

        def infect(self,frame):
            if not self.recovered:
                self.infected = True
                self.when_infected = frame

        def recover(self):
            self.recovered = True
            self.infected = False

        def die(self):
            self.died = True
            self.infected = False
            self.recovered = False
            self.motion = [0,0]

        def spread(self,nodes,frame):
            if frame%10 == 0:
                for x in nodes:
                    if x.infected or x.recovered or x.died:
                        continue

                    offx = x.x - self.x 
                    offy = x.y - self.y

                    offx = offx * -1 if offx < 0 else offx
                    offy = offy * -1 if offy < 0 else offy

                    distance = offx + offy

                    if distance <= self.range and self.health != 0:
                        if random.randint(1,self.health) == 1:
                            x.infect(frame)

        def update(self,nodes,frame):
            self.spread(nodes,frame)

            if frame >= self.recover_time:
                if random.randint(0,5) == 1 or self.health == 1:
                    self.die()
                else:
                    self.recover()

    locs = []
    nodes = []
    infected = 00
    for x in range(amount):
        while True:
            loc = [random.randint(0,img[0]),random.randint(0,img[1])]
            if loc in locs:
                continue
            else:
                isinfected = False
                if infected < 2:
                    if random.randint(0,amount) == 1 or x == amount -1:
                        isinfected = True
                        infected += 1

                locs.append(loc)
                new_node = node(loc[0],loc[1],[random.uniform(speed*-1,speed),random.uniform(speed*-1,speed)],irange,[img[0],img[1]],infected=isinfected)
                nodes.append(new_node)
                break

    return nodes