from classes.Sprites import Sprites
import pygame
import json
from entities.Goomba import Goomba
from entities.Koopa import Koopa
from classes.Tile import Tile
from entities.Coin import Coin

class Level():
    def __init__(self,screen):
        self.sprites = Sprites()
        self.screen = screen
        self.level = None
        self.entityList = []
        self.loadLevel("Level1-1.json")

    def loadLevel(self,levelname):
        with open("./levels/{}".format(levelname)) as jsonData:
            levelx=[]
            levely = []
            data = json.load(jsonData)
            for layer in data['level']['layers']:
                for y in range(layer['ranges']['y'][0],layer['ranges']['y'][1]):
                    levelx = []
                    for x in range(layer['ranges']['x'][0],layer['ranges']['x'][1]):
                        if(layer['spritename'] == 'sky'):
                            levelx.append(Tile(self.sprites.spriteCollection.get(layer['spritename']),None))
                        else:
                            levelx.append(Tile(self.sprites.spriteCollection.get(layer['spritename']),pygame.Rect(x*32,(y-1)*32,32,32)))
                    levely.append(levelx)
            self.level = levely
            for obj in data['level']['objects']:
                for position in obj['positions']:
                    if(obj['name'] == "bush"):
                        self.addBushSprite(position[0],position[1])
                    elif(obj['name'] == "cloud"):
                        self.addCloudSprite(position[0],position[1])
                    elif(obj['name'] == "randomBox"):
                        self.addRandomBox(position[0],position[1])
                    elif(obj['name'] == "pipe"):
                        self.addPipeSprite(position[0],position[1],position[2])
                    elif(obj['name'] == "coin"):
                        self.addCoin(position[0],position[1])
                    else:
                        self.level[position[1]][position[0]] = Tile(self.sprites.spriteCollection.get(obj['name']),pygame.Rect(position[0]*32,position[1]*32,32,32))
            for entity in data['level']['entities']:
                if entity['name'] == "Goomba":
                    for postion in entity['pos']:
                        self.addGoomba(postion[0],postion[1])
                elif entity['name'] == "Koopa":
                    for postion in entity['pos']:
                        self.addKoopa(postion[0],postion[1])

    def updateEntities(self,cam):
        for entity in self.entityList:
            entity.update(cam)
            if(entity.alive == None):
                self.entityList.remove(entity)

    def drawLevel(self,camera):
        try:
            for y in range(0,15):
                for x in range(0-int(camera.pos.x+1),20-int(camera.pos.x-1)):
                    if self.level[y][x].sprite.redrawBackground:
                        self.screen.blit(self.sprites.spriteCollection.get("sky").image,((x+camera.pos.x)*32,y*32))
                    self.level[y][x].sprite.drawSprite(x+camera.pos.x,y,self.screen)
                    #self.level[y][x].drawRect(self.screen)
            self.updateEntities(camera)
        except IndexError:
            return

    def addCloudSprite(self,x,y):
        try:
            for yOff in range(0,2):
                for xOff in range(0,3):
                    self.level[y+yOff][x+xOff] = Tile(
                        self.sprites.spriteCollection.get("cloud{}_{}".format(yOff+1,xOff+1)),
                        None
                    )
        except IndexError:
            return

    def addPipeSprite(self,x,y,length=2):
        try:
            #add Pipe Head
            self.level[y][x] = Tile(self.sprites.spriteCollection.get("pipeL"),pygame.Rect(x*32,y*32,32,32))
            self.level[y][x+1] = Tile(self.sprites.spriteCollection.get("pipeR"),pygame.Rect((x+1)*32,y*32,32,32))
            #add pipe Body
            for i in range(1,length+20):
                self.level[y+i][x] = Tile(self.sprites.spriteCollection.get("pipe2L"),pygame.Rect(x*32,(y+i)*32,32,32))
                self.level[y+i][x+1] = Tile(self.sprites.spriteCollection.get("pipe2R"),pygame.Rect((x+1)*32,(y+i)*32,32,32))
        except IndexError:
            return

    def addBushSprite(self,x,y):
        try:
            self.level[y][x] = Tile(self.sprites.spriteCollection.get("bush_1"),None)
            self.level[y][x+1] = Tile(self.sprites.spriteCollection.get("bush_2"),None)
            self.level[y][x+2] = Tile(self.sprites.spriteCollection.get("bush_3"),None)
        except IndexError:
            return

    def addRandomBox(self,x,y):
            self.level[y][x] = Tile(
                self.sprites.spriteCollection.get("randomBox"),
                pygame.Rect(x*32,y*32,32,32)
            )

    def addCoin(self,x,y):
        self.entityList.append(
            Coin(self.screen,self.sprites.spriteCollection,x,y)
        )

    def addGoomba(self,x,y):
        self.entityList.append(
            Goomba(self.screen,self.sprites.spriteCollection,x,y,self.level)
        )

    def addKoopa(self,x,y):
        
        self.entityList.append(
            Koopa(self.screen,self.sprites.spriteCollection,x,y,self.level)
        )