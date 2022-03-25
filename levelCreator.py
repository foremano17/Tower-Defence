import pygame
import os
import random

from pygame.constants import *

import tile
import config
import Images
import Level

pygame.font.init()

WIDTH, HEIGHT = int(950*config.size), int(450*config.size)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 50
clock = pygame.time.Clock()


def GetImage(type, size=None, relativeSize=None):
    if relativeSize == None:
        if size == None:
            return Images.SPRITES[type.lower()]
        else:
            return pygame.transform.scale(Images.SPRITES[type.lower()], (int(size[0]*config.size), int(size[1]*config.size)))

    else:
        return pygame.transform.scale(Images.SPRITES[type.lower()], (int(relativeSize[0]*config.size*Images.SPRITES[type.lower()].get_width()), int(relativeSize[1]*config.size*Images.SPRITES[type.lower()].get_height())))

pygame.display.set_caption("Level Creator")
pygame.display.set_icon(GetImage("LevelEditorIcon", (37, 37)))


#Loading levels into memory
levels = []

for i in range(len(os.listdir("Levels"))):
    level = open(f"Levels/Level{i+1}.lvl", "r")
    data = level.readlines()

    while len(data) < 3:
        data.append("")

    for line in range(len(data)):
        for l in data[line]:
            if l == "\n":
                data[line] = data[line][:-1]

    # Name
    name = data[0]

    # Tiles
    tiles = [[""]]
    for c in data[1]:
        if c == ",":
            tiles[-1].append("")
        elif c == "/":
            tiles.append([""])
        else:
            tiles[-1][-1] += c

    levTiles = []

    for y in range(9):
        for x in range(16):
            levTiles.append(tile.Tile(xGrid=x, yGrid=y, img=GetImage(tiles[y][x], (config.gridSize, config.gridSize)), tile=tiles[y][x]))

    # Path Positions
    allPos = []
    for pos in data[2].split(";"):
        splitPos = pos.split(",")
        if pos != "":
            allPos.append((int(splitPos[0]), int(splitPos[1])))

    # Description
    description = data[3]

    # brief
    brief = data[4]

    strDiff = data[5]
    if strDiff == "beginner":
        diff = Level.beginner
    elif strDiff == "easy":
        diff = Level.easy
    elif strDiff == "medium":
        diff = Level.medium
    elif strDiff == "hard":
        diff = Level.hard
    elif strDiff == "titanic":
        diff = Level.titanic

    waves = int(data[6])

    level.close()

    levels.append(Level.Level(name=name, index=i, tiles=levTiles, pathpos=allPos, difficulty=diff, waves=waves, desc=description, brief=brief))



#Title Page
def TitlePage():
    def RedrawWindow():
        pygame.draw.rect(WIN, (15,15,15), (0,0,WIDTH,HEIGHT))

        titleFont = pygame.font.SysFont("comicsans", int(85*config.size))
        title = titleFont.render("Level Creator!", 1, (245, 45, 45))
        WIN.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//3 - title.get_height()//2))

        subtitleFont = pygame.font.SysFont("comicsans", int(50*config.size))
        subtitle = subtitleFont.render("Press x to continue", 1, (240, 240, 240))
        WIN.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, HEIGHT//1.9 - subtitle.get_height()//2))

        pygame.display.update()

    #Game Loop
    while True:
        clock.tick(FPS)

        RedrawWindow()

        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if keys[pygame.K_x]:
                LevelSelection()


def LevelSelection():
    def RedrawWindow():
        pygame.draw.rect(WIN, (15,15,15), (0,0,WIDTH,HEIGHT))

        index = 1
        for l in levels:
            surf = pygame.Surface((int(800*config.size), int(550*config.size)))

            for t in l.tiles:
                surf.blit(t.img, (t.x, t.y))

            surfSize = 0.35
            surf = pygame.transform.scale(surf, (int(surf.get_width()*surfSize), int(surf.get_height()*surfSize)))

            if index%2 == 1:
                x = WIDTH//4 - surf.get_width()//2
            else:
                x = (WIDTH-WIDTH//4) - surf.get_width()//2

            y = ((HEIGHT//4 * ((index-1)//2+1)) - surf.get_height()//2) + int(120*config.size)*((index-1)//2)

            levelNameFont = pygame.font.Font("Assets/Fonts/Gosmicksans.ttf", int(25*config.size))
            levelName = levelNameFont.render(f"Level {l.index+1}", 1, (245,245,245))

            surf.blit(levelName, (surf.get_width()//2 - levelName.get_width()//2, surf.get_height()-int(95*config.size)*surfSize))

            WIN.blit(surf, (x, y + (scrollOffset*config.size)))

            index += 1

        index = 1
        for l in levels:
            if index%2 == 1:
                x = WIDTH//4 - int(400*config.size*0.35)
            else:
                x = (WIDTH-WIDTH//4) - int(400*config.size*0.35)

            y = ((HEIGHT//4 * ((index-1)//2+1)) - int(550*config.size*0.35)//2) + int(120*config.size)*((index-1)//2)

            index += 1

        pygame.display.update()

    scrollOffset = 0

    while True:
        clock.tick(FPS)

        RedrawWindow()

        key = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    scrollOffset += 50
                elif event.button == 5:
                    scrollOffset -= 50
                # 232
                if scrollOffset > 0:
                    scrollOffset = 0
                elif scrollOffset < -232 * ((len(levels)-1)//2):
                    scrollOffset = -232 * ((len(levels)-1)//2)

                if event.button == 1:
                    index = 1
                    for l in levels:
                        if index%2 == 1:
                            x = WIDTH//4 - int(800*config.size*0.35)//2
                        else:
                            x = (WIDTH-WIDTH//4) - int(800*config.size*0.35)//2

                        y = ((HEIGHT//4 * ((index-1)//2+1)) - int(550*config.size*0.35)//2) + int(120*config.size)*((index-1)//2)

                        mouseX = pygame.mouse.get_pos()[0]
                        mouseY = pygame.mouse.get_pos()[1]

                        if mouseX > x and mouseX < x + int(800*config.size*0.35):
                            if mouseY > y+scrollOffset*config.size and mouseY < y+scrollOffset*config.size + int(550*config.size*0.35):
                                LevelEditor(index)

                        index += 1

class Tab:
    def __init__(self, name):
        self.name = name
        self.contents = []

    def Add(self, tile):
        self.contents.append(tile)

grassTab = Tab("Grass")
stoneTab = Tab("Stone")
sandTab = Tab("Sand")
dirtTab = Tab("Dirt")
overlayTab = Tab("Overlay")

tabs = [
    grassTab,
    stoneTab,
    sandTab,
    dirtTab,
    overlayTab
]

class TileType:
    tiles = []

    def __init__(self, tile, tabs):
        self.img = GetImage(tile, (config.gridSize, config.gridSize))
        self.tile = tile
        self.tabs = tabs

        for tab in tabs:
            tab.Add(self)

    def GetTile(self, name=None, tile=None):
        for t in TileType.tiles:
            if (name != None and t.name == name) or (tile != None and self.tile == tile):
                return t

        return None

TileType("dirtGrassBorderB", [dirtTab,grassTab])
TileType("dirtGrassCornerBL", [dirtTab,grassTab])
TileType("grassDirtCircleBR", [grassTab,dirtTab])
TileType("grassDirtCircleBL", [grassTab,dirtTab])
TileType("dirtSandCornerBR", [dirtTab,sandTab])
TileType("dirtSandBorderB", [dirtTab,sandTab])
TileType("dirtSandBorderBL", [dirtTab,sandTab])
TileType("sandDirtCircleBR", [sandTab,dirtTab])
TileType("sandDirtCircleBL", [sandTab,dirtTab])
TileType("dirtStoneCornerBR", [dirtTab,stoneTab])
TileType("dirtStoneEndgeB", [dirtTab,stoneTab])
TileType("dirtStoneCornerBL", [dirtTab,stoneTab])
TileType("stoneDirtCircleBR", [stoneTab,dirtTab])
TileType("stoneDirtCircleBL", [stoneTab,dirtTab])
TileType("squareOverlay", [overlayTab])
TileType("editOverlay", [overlayTab])
TileType("exitOverlay", [overlayTab])
TileType("targetOverlay", [overlayTab])
TileType("darkShadowOverlay", [overlayTab])
TileType("darkBubblesOverlay", [overlayTab])
TileType("spikedDarkShadowOverlay", [overlayTab])
TileType("whiteStarOverlay", [overlayTab])
TileType("dirtGrassBorderR", [dirtTab,grassTab])
TileType("tallGrass", [grassTab])
TileType("dirtGrassBorderL", [dirtTab,grassTab])
TileType("grassDirtCircleTR", [grassTab,dirtTab])
TileType("grassDirtCircleTL", [grassTab,dirtTab])
TileType("dirtSandBorderR", [dirtTab,sandTab])
TileType("sand", [sandTab])
TileType("dirtSandBorderL", [dirtTab,sandTab])
TileType("sandDirtCircleTR", [sandTab,dirtTab])
TileType("sandDirtCircleTL", [sandTab,dirtTab])
TileType("dirtStoneBorderR", [dirtTab,stoneTab])
TileType("stone", [stoneTab])
TileType("dirtStoneBorderL", [dirtTab,stoneTab])
TileType("stoneDirtCircleTR", [stoneTab,dirtTab])
TileType("stoneDirtCircleTL", [stoneTab,dirtTab])
TileType("dirtGrassCornerTR", [dirtTab,grassTab])
TileType("dirtGrassBorderT", [dirtTab,grassTab])
TileType("dirtGrassCornerTL", [dirtTab,grassTab])
TileType("dirtGrassCircle", [dirtTab,grassTab])
TileType("dirt", [dirtTab])
TileType("dirtSandCornerTR", [dirtTab,sandTab])
TileType("dirtSandBorderT", [dirtTab,sandTab])
TileType("dirtSandCornerTL", [dirtTab,sandTab])
TileType("dirtSandCircle", [dirtTab,sandTab])
TileType("dirtStoneCornerTR", [dirtTab,stoneTab])
TileType("dirtStoneBorderT", [dirtTab,stoneTab])
TileType("dirtStoneCornerTL", [dirtTab,stoneTab])
TileType("dirtStoneCircle", [dirtTab,stoneTab])
TileType("grassDirtCornerBR", [grassTab,dirtTab])
TileType("grassDirtBorderB", [grassTab,dirtTab])
TileType("grassDirtCornerBL", [grassTab,dirtTab])
TileType("dirtGrassCircleBR", [dirtTab,grassTab])
TileType("dirtGrassCircleBL", [dirtTab,grassTab])
TileType("grassSandCornerBR", [grassTab,sandTab])
TileType("grassSandBorderB", [grassTab,sandTab])
TileType("grassSandCornerBL", [grassTab,sandTab])
TileType("sandGrassCircleBR", [sandTab,grassTab])
TileType("sandGrassCircleBL", [sandTab,grassTab])
TileType("grassStoneCornerBR", [grassTab,stoneTab])
TileType("grassStoneBorderB", [grassTab,stoneTab])
TileType("grassStoneCornerBL", [grassTab,stoneTab])
TileType("stoneGrassCircleBR", [stoneTab,grassTab])
TileType("stoneGrassCircleBL", [stoneTab,grassTab])
TileType("grassDirtBorderR", [grassTab,dirtTab])
TileType("grassDirtBorderL", [grassTab,dirtTab])
TileType("dirtGrassCircleTR", [dirtTab,grassTab])
TileType("dirtGrassCircleTL", [dirtTab,grassTab])
TileType("grassSandBorderR", [grassTab,sandTab])
TileType("grassSandBorderL", [grassTab,sandTab])
TileType("sandGrassCircleTR", [sandTab,grassTab])
TileType("sandGrassCircleTL", [sandTab,grassTab])
TileType("grassStoneBorderR", [grassTab,stoneTab])
TileType("grassStoneBorderL", [grassTab,stoneTab])
TileType("stoneGrassCircleTR", [stoneTab,grassTab])
TileType("stoneGrassCircleTL", [stoneTab,grassTab])
TileType("grassDirtCornerTR", [grassTab,dirtTab])
TileType("grassDirtBorderT", [grassTab,dirtTab])
TileType("grassDirtCornerTL", [grassTab,dirtTab])
TileType("grassDirtCircle", [grassTab,dirtTab])
TileType("grassSandCornerTR", [grassTab,sandTab])
TileType("grassSandBorderT", [grassTab,sandTab])
TileType("grassSandCornerTL", [grassTab,sandTab])
TileType("grassSandCircle", [grassTab,sandTab])
TileType("grass", [grassTab])
TileType("grassStoneCornerTR", [grassTab,stoneTab])
TileType("grassStoneBorderT", [grassTab,stoneTab])
TileType("grassStoneCornerTL", [grassTab,stoneTab])
TileType("grassStoneCircle", [grassTab,stoneTab])
TileType("bushBig", [overlayTab])
TileType("bushSmall", [overlayTab])
TileType("leafs", [overlayTab])
TileType("bushCircle", [overlayTab])
TileType("bushStar", [overlayTab])
TileType("rock1", [overlayTab])
TileType("rock2", [overlayTab])
TileType("rock3", [overlayTab])
TileType("sandGrassCornerBR", [sandTab,grassTab])
TileType("sandgrassBorderB", [sandTab,grassTab])
TileType("sandGrassCornerBL", [sandTab,grassTab])
TileType("grassSandCircleBR", [grassTab,sandTab])
TileType("grassSandCircleBL", [grassTab,sandTab])
TileType("sandDirtCornerBR", [sandTab,dirtTab])
TileType("sandDirtBorderB", [sandTab,dirtTab])
TileType("sandDirtCornerBL", [sandTab,dirtTab])
TileType("dirtSandCircleBR", [dirtTab,sandTab])
TileType("dirtSandCircleBL", [dirtTab,sandTab])
TileType("sandStoneCornerBR", [sandTab,stoneTab])
TileType("sandStoneBorderB", [sandTab,stoneTab])
TileType("sandStoneCornerBL", [sandTab,stoneTab])
TileType("stoneSandCircleBR", [stoneTab,sandTab])
TileType("stoneSandCircleBL", [stoneTab,sandTab])
TileType("sandGrassBorderR", [sandTab,grassTab])
TileType("sandGrassBorderL", [sandTab,grassTab])
TileType("grassSandCircleTR", [grassTab,sandTab])
TileType("grassSandCircleTL", [grassTab,sandTab])
TileType("sandDirtBorderR", [sandTab,dirtTab])
TileType("sandDirtBorderL", [sandTab,dirtTab])
TileType("dirtSandCircleTR", [dirtTab,sandTab])
TileType("dirtSandCircleTL", [dirtTab,sandTab])
TileType("sandStoneBorderR", [sandTab,stoneTab])
TileType("sandStoneBorderL", [sandTab,stoneTab])
TileType("stoneSandCircleTR", [stoneTab,sandTab])
TileType("stoneSandCircleTL", [stoneTab,sandTab])
TileType("grassStripeV", [grassTab])
TileType("dirtStripeV", [dirtTab])
TileType("stoneStripeV", [stoneTab])
TileType("sandStripeV", [sandTab])
TileType("stoneShape1", [stoneTab,overlayTab])
TileType("stoneShape2", [stoneTab,overlayTab])
TileType("stoneShape3", [stoneTab,overlayTab])
TileType("stoneShape4", [stoneTab,overlayTab])
TileType("sandGrassCornerTR", [sandTab,grassTab])
TileType("sandGrassBorderT", [sandTab,grassTab])
TileType("sandGrassCornerTL", [sandTab,grassTab])
TileType("sandGrassCircle", [sandTab,grassTab])
TileType("sandDirtCornerTR", [sandTab,dirtTab])
TileType("sandDirtBorderT", [sandTab,dirtTab])
TileType("sandDirtCornerTL", [sandTab,dirtTab])
TileType("sandDirtCircle", [sandTab,dirtTab])
TileType("sandStoneCornerTR", [sandTab,stoneTab])
TileType("sandStoneBorderT", [sandTab,stoneTab])
TileType("sandStoneCornerTL", [sandTab,stoneTab])
TileType("sandStoneCircle", [sandTab,stoneTab])
TileType("turretHead1", [overlayTab])
TileType("turretHead2", [overlayTab])
TileType("turretHead3", [overlayTab])
TileType("turretHead4", [overlayTab])
TileType("stoneGrassCornerBR", [stoneTab,grassTab])
TileType("stoneGrassBorderB", [stoneTab,grassTab])
TileType("stoneGrassCornerBL", [stoneTab,grassTab])
TileType("grassStoneCircleBR", [grassTab,stoneTab])
TileType("grassStoneCircleBL", [grassTab,stoneTab])
TileType("stoneDirtCornerBR", [stoneTab,dirtTab])
TileType("stoneDirtBorderB", [stoneTab,dirtTab])
TileType("stoneDirtCornerBL", [stoneTab,dirtTab])
TileType("dirtStoneCircleBR", [dirtTab,stoneTab])
TileType("dirtStoneCircleBL", [dirtTab,stoneTab])
TileType("stoneSandCornerBR", [stoneTab,sandTab])
TileType("stoneSandBorderB", [stoneTab,sandTab])
TileType("stoneSandCornerBL", [stoneTab,sandTab])
TileType("sandStoneCircleBR", [sandTab,stoneTab])
TileType("sandStoneCircleBL", [sandTab,stoneTab])
TileType("grassStripeH", [grassTab])
TileType("dirtStripeH", [dirtTab])
TileType("stoneStripeH", [stoneTab])
TileType("sandStripeH", [sandTab])
TileType("stoneShape5", [stoneTab,overlayTab])
TileType("stoneShape6", [stoneTab,overlayTab])
TileType("stoneShape7", [stoneTab,overlayTab])
TileType("stoneShape8", [stoneTab,overlayTab])
TileType("stoneGrassBorderR", [stoneTab,grassTab])
TileType("stoneGrassBorderL", [stoneTab,grassTab])
TileType("grassStoneCircleTR", [grassTab,stoneTab])
TileType("grassStoneCircleTL", [grassTab,stoneTab])
TileType("stoneDirtBorderR", [stoneTab,dirtTab])
TileType("stoneDirtBorderL", [stoneTab,dirtTab])
TileType("dirtStoneCircleTR", [dirtTab,stoneTab])
TileType("dirtStoneCircleTL", [dirtTab,stoneTab])
TileType("stoneSandBorderR", [stoneTab,sandTab])
TileType("stoneSandBorderL", [stoneTab,sandTab])
TileType("sandStoneCircleTR", [sandTab,stoneTab])
TileType("sandStoneCircleTL", [sandTab,stoneTab])
TileType("turretHead5", [overlayTab])
TileType("turretHead6", [overlayTab])
TileType("stoneGrassCornerTR", [stoneTab,grassTab])
TileType("stoneGrassBorderT", [stoneTab,grassTab])
TileType("stoneGrassCornerTL", [stoneTab,grassTab])
TileType("stoneGrassCircle", [stoneTab,grassTab])
TileType("stoneDirtCornerTR", [stoneTab,dirtTab])
TileType("stoneDirtBorderT", [stoneTab,dirtTab])
TileType("stoneDirtCornerTL", [stoneTab,dirtTab])
TileType("stoneDirtCircle", [stoneTab,dirtTab])
TileType("stoneSandCornerTR", [stoneTab,sandTab])
TileType("stoneSandBorderT", [stoneTab,sandTab])
TileType("stoneSandCornerTL", [stoneTab,sandTab])
TileType("stoneSandCircle", [stoneTab,sandTab])
TileType("tankBaseGreen", [overlayTab])
TileType("tankBaseWhite", [overlayTab])
TileType("turretHead7", [overlayTab])
TileType("turretHead8", [overlayTab])
TileType("plainShadow1", [overlayTab])
TileType("plainShadow2", [overlayTab])
TileType("fire1", [overlayTab])
TileType("fire2", [overlayTab])
TileType("fire3", [overlayTab])
TileType("fire4", [overlayTab])
TileType("dirtGrassCornerBR", [dirtTab, grassTab])

strToDiff = {
    "beginner":Level.beginner,
    "easy":Level.easy,
    "medium":Level.medium,
    "hard":Level.hard,
    "titanic":Level.titanic
}
        

def LevelEditor(levelIndex):
    global settingsChainging

    def GetLevel(offset=0, index=None):
        if index == None:
            return levels[levelIndex-1+offset]
        else:
            return levels[index+offset]

    def Save(board, levelIndex, name):
        global settingsChainging

        if diffText in ["beginner", "easy", "medium", "hard", "titanic"]:
            file = open(f"Levels/Level{levelIndex}.lvl", "w")
            file.write(name)
            file.close()

            lvl = "\n"

            index = 0
            for t in board:
                lvl += t.tile

                if index%16 == 15:
                    if t != board[-1]:
                        lvl += "/"
                else:
                    lvl += ","

                index += 1

            file = open(f"Levels/Level{levelIndex}.lvl", "a")
            file.write(lvl)
            file.close()

            path = "\n"
            for pos in GetLevel().pathpos:
                path += f"{pos[0]},{pos[1]}"

                if pos is not GetLevel().pathpos[-1]:
                    path += ";"

            file = open(f"Levels/Level{levelIndex}.lvl", "a")
            file.write(path)
            file.close()

            file = open(f"Levels/Level{levelIndex}.lvl", "a")
            file.write("\n" + descText)
            file.close()

            file = open(f"Levels/Level{levelIndex}.lvl", "a")
            file.write("\n" + briefText)
            file.close()

            file = open(f"Levels/Level{levelIndex}.lvl", "a")
            file.write("\n"+diffText)
            file.close()


            file = open(f"Levels/Level{levelIndex}.lvl", "a")
            file.write("\n"+wavesText)
            file.close()

        else:
            settingsChainging = True

    def DrawPointer(row=0, column=0, pos=(0,0), thickness=2, rawText="", font=pygame.font.SysFont("comicsans", int(20*config.size)), colour=(255,143,0), lineOffset=20, height=25):
        index = 0
        prePointerText = ""
        for line in GetBrokenText(rawText=rawText, font=font)[row]:
            for letter in line:
                if index < column:
                    prePointerText += letter
                
                index += 1

        text = font.render(prePointerText, 1, (0,0,0))

        pygame.draw.rect(WIN, colour, (int(pos[0]*config.size)+text.get_width(), int((pos[1]+lineOffset*row)*config.size), int(thickness*config.size), int(height*config.size)))

    def GetBrokenText(rawText="", font=pygame.font.SysFont("comicsans", int(20*config.size)), splitType="word"):
        brokenDesc = []
        for word in rawText.split(" "):
            if word != "":
                brokenDesc.append(word)

        brokenLines = [[]]
        lines = []
        while True:
            if len(brokenDesc) == 0:
                lineString = ""
                for word in brokenLines[-1]:
                    lineString += word
                lines.append(lineString)
                break

            if brokenDesc[0] == "BREAK":
                brokenDesc.pop(0)

                lineString = ""
                for word in brokenLines[-1]:
                    lineString += word
                lines.append(lineString)

                brokenLines.append([])
                continue

            brokenLines[-1].append(brokenDesc[0] + " ")

            lineString = ""
            for word in brokenLines[-1]:
                lineString += word
                    
            lineImg = font.render(lineString, 1, (255, 255, 255))
            if lineImg.get_width() >= int(340*config.size):
                brokenLines[-1].pop(-1)
                    
                lineString = ""
                for word in brokenLines[-1]:
                    lineString += word
                lines.append(lineString)

                brokenLines.append([])
            else:
                brokenDesc.pop(0)

        if splitType == "word":
            return brokenLines
        elif splitType == "line":
            brokenLinesCombined = []

            for x in brokenLines:
                brokenLinesCombined.append("")
                for y in x:
                    brokenLinesCombined[-1] += y

            return brokenLinesCombined


    def MultiLineText(rawText="", pos=(0,0), font=pygame.font.SysFont("comicsans", int(20*config.size)), lineOffset=20, colour=(30,30,30)):
        brokenDesc = []
        for word in rawText.split(" "):
            if word != "":
                brokenDesc.append(word)

        brokenLines = [[]]
        lines = []
        while True:
            if len(brokenDesc) == 0:
                lineString = ""
                for word in brokenLines[-1]:
                    lineString += word
                lines.append(lineString)
                break

            if brokenDesc[0] == "BREAK":
                brokenDesc.pop(0)

                lineString = ""
                for word in brokenLines[-1]:
                    lineString += word
                lines.append(lineString)

                brokenLines.append([])
                continue

            brokenLines[-1].append(brokenDesc[0] + " ")

            lineString = ""
            for word in brokenLines[-1]:
                lineString += word
                    
            lineImg = font.render(lineString, 1, (255, 255, 255))
            if lineImg.get_width() >= int(340*config.size):
                brokenLines[-1].pop(-1)
                    
                lineString = ""
                for word in brokenLines[-1]:
                    lineString += word
                lines.append(lineString)

                brokenLines.append([])
            else:
                brokenDesc.pop(0)

        lineIndex = 0
        for line in lines:
            text = font.render(line, 1, colour)
            WIN.blit(text, (int(pos[0]*config.size),int((pos[1]+lineOffset*lineIndex)*config.size)))

            lineIndex += 1

    def RedrawWindow():
        global textFont
        
        pygame.draw.rect(WIN, (15,15,15), (0,0,WIDTH,HEIGHT))

        pygame.draw.rect(WIN, (120,120,120), (0,int(HEIGHT-45*config.size),int(WIDTH-230*config.size),int(1*config.size)))
        pygame.draw.rect(WIN, (160,160,160), (0,int(HEIGHT-44*config.size),int(WIDTH-230*config.size),int(54*config.size)))

        WIN.blit(GetImage("save", (37, 37)), (int(3*config.size),int(HEIGHT-3*config.size-GetImage("save", (37, 37)).get_width())))
        WIN.blit(GetImage("exit", (37, 37)), (int(678*config.size), int(410*config.size)))
        WIN.blit(GetImage("settings", (37, 37)), (int(633*config.size), int(410*config.size)))
        if nameChainging:
            pygame.draw.rect(WIN, (20,200,20), (int(85*config.size), int(408*config.size),int(41*config.size), int(41*config.size)))
        WIN.blit(GetImage("nameLabel", (37, 37)), (int(87*config.size), int(410*config.size)))
        if drawing:
            pygame.draw.rect(WIN, (20,200,20), (int(43*config.size), int(408*config.size),int(41*config.size), int(41*config.size)))
        WIN.blit(GetImage("drawing", (37, 37)), (int(45*config.size), int(410*config.size)))
        
        pygame.draw.rect(WIN, (123,76,14), (int(720*config.size),0,int(1*config.size),HEIGHT))
        pygame.draw.rect(WIN, (163,116,44), (int(721*config.size),0,int(229*config.size),HEIGHT))

        contents = tabs[currentTab].contents
        index = 0
        for t in contents:
            x = int(749.5*config.size) + index%3*int(60*config.size)
            y = int(35*config.size) + index//3*int(60*config.size)

            if t == selectedTile:
                pygame.draw.rect(WIN, (242,231,10), (x-int(2*config.size),y-int(2*config.size)+int(scrollOffset*config.size),t.img.get_width()+int(4*config.size),t.img.get_height()+int(4*config.size)))

            WIN.blit(t.img, (x,y+int(scrollOffset*config.size)))

            index += 1

        pygame.draw.rect(WIN, (40,30,30), (int(720*config.size),0,int(230*config.size),int(30*config.size)))

        tabFont = pygame.font.SysFont("conicsans", int(30*config.size))
        tabTitle = tabFont.render(tabs[currentTab].name, 1, (240,240,240))
        WIN.blit(tabTitle, (int(725*config.size),int(7*config.size)))

        arrow = GetImage("arrowHead", (40,100))
        WIN.blit(arrow, (int(WIDTH-3*config.size-arrow.get_width()),HEIGHT//2-arrow.get_height()//2))
        arrow = pygame.transform.rotate(arrow, 180)
        WIN.blit(arrow, (int(723*config.size),HEIGHT//2-arrow.get_height()//2))

        surf = pygame.Surface((int(800*config.size), int(450*config.size)))

        for t in board:
            surf.blit(t.img, (t.x, t.y))

        surfSize = 0.9
        surf = pygame.transform.scale(surf, (int(surf.get_width()*surfSize), int(surf.get_height()*surfSize)))

        WIN.blit(surf, (0, 0))

        if settingsChainging:
            pygame.draw.rect(WIN, (153, 153, 153), (int(10*config.size),int(10*config.size),surf.get_width()-int(20*config.size),surf.get_height()-int(20*config.size)), 0, 3)
            pygame.draw.rect(WIN, (89, 89, 89), (int(10*config.size),int(10*config.size),surf.get_width()-int(20*config.size),surf.get_height()-int(20*config.size)), 3, 3)

            labelFont = pygame.font.SysFont("arialblack", int(16*config.size))
            textFont = pygame.font.SysFont("arialblack", int(18*config.size))

            # Difficulty
            label = labelFont.render("Difficulty:", 1, (40, 40, 40))
            WIN.blit(label, (int(20*config.size),int(25*config.size)))
            if diffText == "beginner" or diffText == "easy" or diffText == "medium" or diffText == "hard" or diffText == "titanic":
                pygame.draw.rect(WIN, (230, 230, 230), (int(18*config.size),int(50*config.size),int(280*config.size),int(30*config.size)), 0, 2)
            else:
                pygame.draw.rect(WIN, (230, 20, 20), (int(18*config.size),int(50*config.size),int(280*config.size),int(30*config.size)), 0, 2)
            if settingsBoxSelected == "diff":
                pygame.draw.rect(WIN, (245, 245, 0), (int(18*config.size),int(50*config.size),int(280*config.size),int(30*config.size)), 2, 2)
            text = textFont.render(diffText, 1, (30, 30, 30))
            WIN.blit(text, (int(24*config.size),int(50*config.size)))

            # Waves
            label = labelFont.render("Waves:", 1, (40, 40, 40))
            WIN.blit(label, (int(20*config.size),int(85*config.size)))
            pygame.draw.rect(WIN, (230, 230, 230), (int(18*config.size),int(110*config.size),int(280*config.size),int(30*config.size)), 0, 2)
            if settingsBoxSelected == "waves":
                pygame.draw.rect(WIN, (245, 245, 0), (int(18*config.size),int(110*config.size),int(280*config.size),int(30*config.size)), 2, 2)
            text = textFont.render(wavesText, 1, (30, 30, 30))
            WIN.blit(text, (int(24*config.size),int(110*config.size)))

            # Description
            label = labelFont.render("Level Description:", 1, (40, 40, 40))
            WIN.blit(label, (int(335*config.size),int(25*config.size)))
            pygame.draw.rect(WIN, (230, 230, 230), (int(333*config.size),int(50*config.size),int(350*config.size),int(150*config.size)), 0, 2)
            if settingsBoxSelected == "desc":
                pygame.draw.rect(WIN, (245, 245, 0), (int(333*config.size),int(50*config.size),int(350*config.size),int(150*config.size)), 2, 2)

            MultiLineText(rawText=descText, colour=(30,30,30), font=textFont, pos=(339,50), lineOffset=20)

            if settingsBoxSelected == "desc":
                DrawPointer(row=selectedLine, column=selectedColumn, pos=(337,52), thickness=2, rawText=descText, font=textFont, colour=((245, 131, 0)), lineOffset=20, height=25)

            # Briefing
            label = labelFont.render("Level Breifing:", 1, (40, 40, 40))
            WIN.blit(label, (int(335*config.size),int(205*config.size)))
            pygame.draw.rect(WIN, (230, 230, 230), (int(333*config.size),int(230*config.size),int(350*config.size),int(150*config.size)), 0, 2)
            if settingsBoxSelected == "brief":
                pygame.draw.rect(WIN, (245, 245, 0), (int(333*config.size),int(230*config.size),int(350*config.size),int(150*config.size)), 2, 2)
            
            MultiLineText(rawText=briefText, colour=(30,30,30), font=textFont, pos=(339,230), lineOffset=20)

            if settingsBoxSelected == "brief":
                DrawPointer(row=selectedLine, column=selectedColumn, pos=(337,232), thickness=2, rawText=briefText, font=textFont, colour=((245, 131, 0)), lineOffset=20, height=25)



        if drawing:
            for i in range(len(GetLevel().pathpos)-1):
                pygame.draw.line(WIN, (200,20,20), (GetLevel().pathpos[i]), (GetLevel().pathpos[i+1]), 2)

        if nameChainging:
            pygame.draw.rect(WIN, (220,220,220), (int(5*config.size),int(5*config.size),int(175*config.size),int(30*config.size)))
            pygame.draw.rect(WIN, (250,250,250), (int(6*config.size),int(6*config.size),int(173*config.size),int(28*config.size)))
            
            nameFont = pygame.font.SysFont("comicsans", 40)
            nameText = nameFont.render(levelName, 1, (10,10,10))
            WIN.blit(nameText, (int(9*config.size),int(9*config.size)))

        pygame.display.update()

    def CheckTileReplacements():
        for yI in range(9):
            for xI in range(16):
                x = xI*int(config.gridSize*config.size*0.9)
                y = yI*int(config.gridSize*config.size*0.9)

                mouseX = pygame.mouse.get_pos()[0]
                mouseY = pygame.mouse.get_pos()[1]

                if mouseX > x and mouseX < x + int(config.gridSize*config.size):
                    if mouseY > y and mouseY < y + int(config.gridSize*config.size):
                        board[yI*16+xI] = tile.Tile(xGrid=xI, yGrid=yI, img=selectedTile.img, tile=selectedTile.tile)
                        return

    for l in levels:
        if l.index == levelIndex-1:
            board = l.tiles

    currentTab = 0
    scrollOffset = 0
    selectedTile = None
    settingsBoxSelected = None
    levelName = GetLevel().name

    selectedLine = 0
    selectedColumn = 0

    global diffText
    global wavesText
    global descText
    global briefText

    diffText = GetLevel().GetStrDiff().lower()
    wavesText = str(GetLevel().waves)
    descText = GetLevel().desc
    briefText = GetLevel().brief

    drawing = False
    holding3 = False
    backspaceHeld = False
    nameChainging = False
    settingsChainging = False

    while True:
        clock.tick(FPS)

        RedrawWindow()

        if holding3 and selectedTile != None:
            CheckTileReplacements()

        key = pygame.key.get_pressed()

        if key[K_BACKSPACE] and drawing and len(GetLevel().pathpos) > 0 and not backspaceHeld:
            GetLevel().pathpos.pop(-1)
            backspaceHeld = True
        
        if not key[K_BACKSPACE]:
            backspaceHeld = False

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if nameChainging:
                    if event.key == pygame.K_BACKSPACE:
                        levelName = levelName[:-1]
                    elif event.key == pygame.K_RETURN:
                        nameChainging = False
                    else:
                        levelName += event.unicode

                    GetLevel().name = levelName
                
                elif settingsChainging:
                    def SetBox(value):
                        global diffText
                        global wavesText
                        global descText
                        global briefText

                        box = settingsBoxSelected
                        if box == "diff":
                            diffText = value
                        elif box == "waves":
                            wavesText = value
                        elif box == "desc":
                            descText = value
                        elif box == "brief":
                            briefText = value

                    def GetBox():
                        box = settingsBoxSelected
                        if box == "diff":
                            return diffText
                        elif box == "waves":
                            return wavesText
                        elif box == "desc":
                            return descText
                        elif box == "brief":
                            return briefText

                    def GetBoxList():
                        box = settingsBoxSelected
                        if box == "desc":
                            return descText
                        elif box == "brief":
                            return briefText
                            
                    if settingsBoxSelected != None:
                        if event.key == pygame.K_BACKSPACE:
                            if settingsBoxSelected == "desc" or settingsBoxSelected == "brief":
                                if selectedColumn == 0 and selectedLine != 0:
                                    count = 0
                                    index = 0
                                    for line in GetBrokenText(rawText=GetBox(), font=textFont, splitType="line"):
                                        if index < selectedLine:
                                            count += len(line) + 7
                                        index += 1

                                    count += selectedColumn
                                    SetBox(GetBox()[0:count-9] + GetBox()[count-1:])
                                    selectedLine -= 1 
                                    selectedColumn = len(GetBrokenText(rawText=GetBox(), font=textFont, splitType="line")[selectedLine])-1
                                    #selectedLine = len(GetBrokenText(rawText=GetBox(), font=textFont, splitType="line")[selectedLine])-1
                                else:
                                    if not (selectedLine == 0 and selectedColumn == 0):
                                        numLinesBefore = len(GetBrokenText(rawText=GetBox(), font=textFont, splitType="line"))
                                        
                                        count = 0
                                        index = 0
                                        for line in GetBrokenText(rawText=GetBox(), font=textFont, splitType="line"):
                                            if index < selectedLine:
                                                count += len(line)
                                                if GetBox()[count-1:count+6] == " BREAK ":
                                                    count += 6
                                            index += 1

                                        count += selectedColumn
                                        SetBox(GetBox()[0:count-1] + GetBox()[count:])

                                        selectedColumn -= 1

                                        chaingeInNumLines = len(GetBrokenText(rawText=GetBox(), font=textFont, splitType="line")) - numLinesBefore

                                        if chaingeInNumLines != 0:
                                            selectedLine += chaingeInNumLines
                                            selectedColumn = len(GetBrokenText(rawText=GetBox(), font=textFont, splitType="line")[-1])-1
                            
                            
                            elif settingsBoxSelected != "desc" and settingsBoxSelected != "brief":
                                SetBox(GetBox()[:-1])


                        elif event.key == pygame.K_UP and selectedLine != 0:
                            selectedLine -= 1
                            selectedColumn = len(GetBrokenText(rawText=GetBox(), font=textFont, splitType="line")[selectedLine])-1
                        elif event.key == pygame.K_DOWN and not (settingsBoxSelected == "diff" or settingsBoxSelected == "waves") and selectedLine != len(GetBrokenText(rawText=GetBox(), font=textFont, splitType="line"))-1:
                            selectedLine += 1
                            selectedColumn = len(GetBrokenText(rawText=GetBox(), font=textFont, splitType="line")[selectedLine])-1
                        elif event.key == pygame.K_LEFT and selectedColumn > 0:
                            selectedColumn -= 1
                        elif event.key == pygame.K_RIGHT and selectedColumn < len(GetBrokenText(rawText=GetBox(), font=textFont, splitType="line")[selectedLine])-1:
                            selectedColumn += 1
                        elif event.key == pygame.K_RETURN:
                            if not (settingsBoxSelected == "diff" or settingsBoxSelected == "waves") and selectedLine != len(GetBoxList())-1:
                                SetBox(GetBox()+" BREAK ")

                                selectedLine += 1
                                selectedColumn = 0
                        else:
                            if settingsBoxSelected != "desc" and settingsBoxSelected != "brief":
                                SetBox(GetBox() + event.unicode)

                            else:
                                numLinesBefore = len(GetBrokenText(rawText=GetBox(), font=textFont, splitType="line"))

                                count = 0
                                index = 0
                                for line in GetBrokenText(rawText=GetBox(), font=textFont, splitType="line"):
                                    if index < selectedLine:
                                        count += len(line)
                                        if GetBox()[count-1:count+6] == " BREAK ":
                                            count += 6
                                    index += 1

                                count += selectedColumn
                                SetBox(GetBox()[0:count] + event.unicode + GetBox()[count:])

                                chaingeInNumLines = len(GetBrokenText(rawText=GetBox(), font=textFont, splitType="line")) - numLinesBefore

                                if chaingeInNumLines != 0:
                                    selectedLine += chaingeInNumLines
                                    selectedColumn = len(GetBrokenText(rawText=GetBox(), font=textFont, splitType="line")[-1])-1
                                else:
                                    selectedColumn += len(event.unicode)


            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX = pygame.mouse.get_pos()[0]
                mouseY = pygame.mouse.get_pos()[1]

                if event.button == 1:
                    arrow = GetImage("arrowHead", (40, 100))
                    arrowClicked = False

                    # Left
                    x = int(723*config.size)
                    y = HEIGHT//2-arrow.get_height()//2
                    if mouseX >= x and mouseX <= x + arrow.get_width():
                        if mouseY >= y and mouseY <= y + arrow.get_height():
                            currentTab -= 1
                            scrollOffset = 0
                            arrowClicked = True

                    # Right
                    x = int(WIDTH-3*config.size-arrow.get_width())
                    y = HEIGHT//2-arrow.get_height()//2
                    if mouseX >= x and mouseX <= x + arrow.get_width():
                        if mouseY >= y and mouseY <= y + arrow.get_height():
                            currentTab += 1
                            scrollOffset = 0
                            arrowClicked = True


                    if not arrowClicked and not drawing:
                        contents = tabs[currentTab].contents
                        index = 0
                        for t in contents:
                            x = int(749.5*config.size) + index%3*int(60*config.size)
                            y = int(35*config.size) + index//3*int(60*config.size) + int(scrollOffset*config.size)

                            if mouseX > x and mouseX < x + t.img.get_width():
                                if mouseY > y and mouseY < y + t.img.get_height():
                                    selectedTile = t

                            index += 1

                    if selectedTile != None:
                        CheckTileReplacements()

                    
                    x = int(3*config.size)
                    y = int(HEIGHT-3*config.size-GetImage("save", (37, 37)).get_width())

                    if mouseX > x and mouseX < x + GetImage("save", (37, 37)).get_width():
                        if mouseY > y and mouseY < y + GetImage("save", (37, 37)).get_height():
                            Save(board, levelIndex, levelName)


                    x = int(678*config.size)
                    y = int(410*config.size)

                    if mouseX > x and mouseX < x + GetImage("exit", (37, 37)).get_width():
                        if mouseY > y and mouseY < y + GetImage("exit", (37, 37)).get_height():
                            LevelSelection()


                    x = int(633*config.size)
                    y = int(410*config.size)

                    if mouseX > x and mouseX < x + GetImage("settings", (37, 37)).get_width():
                        if mouseY > y and mouseY < y + GetImage("settings", (37, 37)).get_height():
                            settingsChainging = not settingsChainging
                            settingsBoxSelected = None


                    if settingsChainging:

                        if settingsBoxSelected != "diff":
                            x = int(18*config.size)
                            y = int(50*config.size)
                            if mouseX > x and mouseX < x + int(280*config.size):
                                if mouseY > y and mouseY < y + int(30*config.size):
                                    settingsBoxSelected = "diff"
                                    selectedLine = 0

                        if settingsBoxSelected != "waves":
                            x = int(18*config.size)
                            y = int(110*config.size)
                            if mouseX > x and mouseX < x + int(280*config.size):
                                if mouseY > y and mouseY < y + int(30*config.size):
                                    settingsBoxSelected = "waves"
                                    selectedLine = 0

                        if settingsBoxSelected != "desc":
                            x = int(333*config.size)
                            y = int(50*config.size)
                            if mouseX > x and mouseX < x + int(350*config.size):
                                if mouseY > y and mouseY < y + int(150*config.size):
                                    settingsBoxSelected = "desc"
                                    selectedLine = 0

                        if settingsBoxSelected != "brief":
                            x = int(333*config.size)
                            y = int(230*config.size)
                            if mouseX > x and mouseX < x + int(350*config.size):
                                if mouseY > y and mouseY < y + int(150*config.size):
                                    settingsBoxSelected = "brief"
                                    selectedLine = 0

                    
                    x = int(45*config.size)
                    y = int(410*config.size)

                    if mouseX > x and mouseX < x + int(37*config.size):
                        if mouseY > y and mouseY < y + int(37*config.size):
                            drawing = not drawing
                            selectedTile = None

                    if drawing:
                        if mouseX < int(800*config.size*0.9):
                            if mouseY < int(450*config.size*0.9):
                                if len(GetLevel().pathpos) == 0:
                                    left = mouseX
                                    right = int(800*config.size*0.9) - mouseX
                                    up = mouseY
                                    down = int(450*config.size*0.9) - mouseY

                                    if left < right and left < up and left < down:
                                        GetLevel().pathpos.append((0,mouseY))
                                    elif right < left and right < up and right < down:
                                        GetLevel().pathpos.append((int(800*config.size*0.9),mouseY))
                                    elif up < right and up < left and up < down:
                                        GetLevel().pathpos.append((mouseX,0))
                                    elif down < right and down < up and down < left:
                                        GetLevel().pathpos.append((mouseX,int(450*config.size*0.9)))

                                GetLevel().pathpos.append((mouseX,mouseY))

                    
                    x = int(87*config.size)
                    y = int(410*config.size)

                    if mouseX > x and mouseX < x + int(37*config.size):
                        if mouseY > y and mouseY < y + int(37*config.size):
                            nameChainging = not nameChainging


                if event.button == 3:
                    if drawing:
                        if mouseX < int(800*config.size*0.9):
                            if mouseY < int(450*config.size*0.9):
                                left = mouseX
                                right = int(800*config.size*0.9) - mouseX
                                up = mouseY
                                down = int(450*config.size*0.9) - mouseY

                                if left < right and left < up and left < down:
                                    GetLevel().pathpos.append((0,mouseY))
                                elif right < left and right < up and right < down:
                                    GetLevel().pathpos.append((int(800*config.size*0.9),mouseY))
                                elif up < right and up < left and up < down:
                                    GetLevel().pathpos.append((mouseX,0))
                                elif down < right and down < up and down < left:
                                    GetLevel().pathpos.append((mouseX,int(450*config.size*0.9)))


                if event.button == 3:
                    holding3 = True


                if currentTab >= len(tabs):
                    currentTab = 0
                elif currentTab < 0:
                    currentTab = len(tabs)-1

                if mouseX >= int(720*config.size):
                    if mouseY > 30:
                        if event.button == 4:
                            scrollOffset += 50
                        elif event.button == 5:
                            scrollOffset -= 50

                        if scrollOffset > 0:
                            scrollOffset = 0
                        if scrollOffset-int(35*config.size) + (len(tabs[currentTab].contents)-1)//3*int(60*config.size) < 0:
                            scrollOffset = -((len(tabs[currentTab].contents)-1)//3*int(60*config.size))

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    holding3 = False


def Game():
    def RedrawWindow():
        pygame.draw.rect(WIN, (15,15,15), (0,0,WIDTH,HEIGHT))

        #for t in tile.Tile.Tiles:
        #    t.Draw(WIN)

        pygame.display.update()

    #Game Loop
    while True:
        clock.tick(FPS)

        RedrawWindow()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()


#TitlePage()
LevelSelection()