import pygame
import os

import tile
import config
import Images
import Level

WIDTH, HEIGHT = int(800*config.size), int(450*config.size)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 50
clock = pygame.time.Clock()

pygame.font.init()


def GetImage(type, size=None, relativeSize=None):
    if relativeSize == None:
        if size == None:
            return Images.SPRITES[type.lower()]
        else:
            return pygame.transform.scale(Images.SPRITES[type.lower()], (int(size[0]*config.size), int(size[1]*config.size)))

    else:
        return pygame.transform.scale(Images.SPRITES[type.lower()], (int(relativeSize[0]*config.size*Images.SPRITES[type.lower()].get_width()), int(relativeSize[1]*config.size*Images.SPRITES[type.lower()].get_height())))

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

    # Brief
    brief = data[4]

    # Diff
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

    # Waves
    waves = int(data[6])

    level.close()

    levels.append(Level.Level(name=name, index=i, tiles=levTiles, pathpos=allPos, difficulty=diff, waves=waves, desc=description, brief=brief))


pygame.display.set_caption("PANDA Tower Defence")
pygame.display.set_icon(GetImage("pandaIcon", (37,37)))


# Main Menu
def MainMenu():
    def RedrawWindow():
        pygame.draw.rect(WIN, (200,20,20), (0,0,WIDTH,HEIGHT))
        pygame.draw.rect(WIN, (10,130,10), (int(5*config.size),int(5*config.size),WIDTH-int(10*config.size),HEIGHT-int(10*config.size)), 0, int(6*config.size))
        pygame.draw.rect(WIN, (20,180,20), (int(6*config.size),int(6*config.size),WIDTH-int(12*config.size),HEIGHT-int(12*config.size)), 0, int(10*config.size))
        
        titleFont = pygame.font.Font("Assets/Fonts/Pamit.ttf", int(55*config.size))
        titleText = titleFont.render("Ancient Tower Defence", 1, (12, 10, 12))
        WIN.blit(titleText, (WIDTH//2-titleText.get_width()//2, HEIGHT//4-titleText.get_height()//2))

        campaignButton = GetImage("campaignB", (192,48))
        WIN.blit(campaignButton, (WIDTH//2-campaignButton.get_width()//2, HEIGHT//1.5-campaignButton.get_height()//2))

        pygame.display.update()

    #Game Loop
    while True:
        clock.tick(FPS)

        RedrawWindow()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX = pygame.mouse.get_pos()[0]
                mouseY = pygame.mouse.get_pos()[1]

                if event.button == 1:
                    campaignButton = GetImage("campaignB", (192, 48))
                    x = WIDTH//2-campaignButton.get_width()//2
                    y = HEIGHT//1.5-campaignButton.get_height()//2
                    
                    if mouseX > x and mouseX < x + campaignButton.get_width():
                        if mouseY > y and mouseY < y + campaignButton.get_height():
                            LevelSelection()


# Level Selection
def LevelSelection():
    def RedrawWindow():
        global boardImg
        
        pygame.draw.rect(WIN, (50, 20, 0), (0,0,WIDTH,HEIGHT))
        pygame.draw.rect(WIN, (102, 41, 0), (0,0,WIDTH,HEIGHT), 0, int(7*config.size))

        rounding = int(10*config.size)

        # Campain Mission
        x = int(5*config.size)
        y = int(5*config.size)
        xW = WIDTH//3*2-int(5*config.size)
        yW = HEIGHT-int(10*config.size)
        pygame.draw.rect(WIN, (0, 0, 30), (x,y,xW,yW), False, rounding)
        pygame.draw.rect(WIN, (0, 0, 15), (x,y,xW,yW), 2, rounding)

        # Past Campain Missions
        x = WIDTH//3*2+int(4*config.size)
        y = int(5*config.size)
        xW = WIDTH//3-int(8*config.size)
        yW = HEIGHT//2.2-int(10*config.size)
        pygame.draw.rect(WIN, (0, 0, 20), (x,y,xW,yW), False, rounding)
        pygame.draw.rect(WIN, (0, 0, 10), (x,y,xW,yW), 2, rounding)

        levelTitleFontSmall = pygame.font.Font("Assets/Fonts/Gosmicksans.ttf", int(14*config.size))
        levelSubtextFontSmall = pygame.font.Font("Assets/Fonts/AsapItalic.ttf", int(9*config.size))
        
        levelTitleFontLarge = pygame.font.Font("Assets/Fonts/AsapItalic.ttf", int(30*config.size))
        levelSubtextFontLarge = pygame.font.Font("Assets/Fonts/AsapItalic.ttf", int(12*config.size))
        levelSubtextBFontLarge = pygame.font.Font("Assets/Fonts/AsapItalic.ttf", int(14*config.size))


        index = 0
        for l in levels:
            if index >= levelScroll and index < levelScroll + 3:
                ## Level Selection
                levelYOffset = (index-levelScroll)*int(64*config.size)

                if selectedLevel == l:
                    pygame.draw.rect(WIN, (12, 12, 45), (x+int(2*config.size), y+int(5*config.size)+levelYOffset, xW-int(2*config.size), int(53*config.size)), 0, int(5*config.size))

                # Board
                size = 0.085
                boardImg = l.GetImg()
                boardImg = pygame.transform.scale(l.GetImg(), (int(boardImg.get_width()*size), int(boardImg.get_height()*size)))

                pygame.draw.rect(WIN, (0, 0, 0), (x+int(4*config.size), y+int(8*config.size)+levelYOffset, boardImg.get_width()+int(2*config.size), boardImg.get_height()+int(((100*size)+2)*config.size)))
                WIN.blit(boardImg, (x+int(5*config.size), y+int(9*config.size)+levelYOffset))
                pygame.draw.rect(WIN, (160, 50, 0), (x+int(5*config.size), y+int(9*config.size)+boardImg.get_height()+levelYOffset, boardImg.get_width(), int(100*size*config.size)))

                # Title
                levelNameTextSmall = levelTitleFontSmall.render(l.name, 1, (255, 255, 255))
                WIN.blit(levelNameTextSmall, (x+int(12*config.size)+boardImg.get_width(), y+int(11*config.size)+levelYOffset))

                # Difficulty
                levelDiffTextSmall = levelSubtextFontSmall.render(f"Difficulty: {l.GetStrDiff()}", 1, (255, 255, 255))
                WIN.blit(levelDiffTextSmall, (x+int(14*config.size)+boardImg.get_width(), y+int(27*config.size)+levelYOffset))

                # Waves
                levelWaveTextSmall = levelSubtextFontSmall.render(f"Wave: 0/{l.waves}", 1, (255, 255, 255))
                WIN.blit(levelWaveTextSmall, (x+int(14*config.size)+boardImg.get_width(), y+int(35*config.size)+levelYOffset))

                # Seperation Line
                pygame.draw.rect(WIN, (5, 5, 40), (x+int(6*config.size), y+int(15*config.size)+boardImg.get_height()+int(100*size*config.size)+levelYOffset, xW-int(12*config.size), int(2*config.size)), 0, int(10*config.size))

            if l == selectedLevel:
                ## Level Detail
                # Title
                levelNameTextLarge = levelTitleFontLarge.render(l.name, 1, (255, 234, 248))
                WIN.blit(levelNameTextLarge, (int(23*config.size),int(28*config.size)))

                def DisplayMultiLine(fullBox, font, pos=(0,0), linePadding=10, width=int(200*config.size)):
                    brokenBox = []
                    for word in fullBox.split(" "):
                        if word != "":
                            brokenBox.append(word)

                    brokenLines = [[]]
                    lines = []
                    while True:
                        if len(brokenBox) == 0:
                            lineString = ""
                            for word in brokenLines[-1]:
                                lineString += word
                            lines.append(lineString)
                            break

                        if brokenBox[0] == "BREAK":
                            brokenBox.pop(0)

                            lineString = ""
                            for word in brokenLines[-1]:
                                lineString += word
                            lines.append(lineString)

                            brokenLines.append([])
                            continue

                        brokenLines[-1].append(brokenBox[0] + " ")

                        lineString = ""
                        for word in brokenLines[-1]:
                            lineString += word
                        
                        lineImg = levelSubtextFontLarge.render(lineString, 1, (255, 255, 255))
                        if lineImg.get_width() >= width:
                            brokenLines[-1].pop(-1)
                            
                            lineString = ""
                            for word in brokenLines[-1]:
                                lineString += word
                            lines.append(lineString)

                            brokenLines.append([])
                        else:
                            brokenBox.pop(0)

                    lineIndex = 0
                    for line in lines:
                        levelDescTextLarge = font.render(line, 1, (255, 255, 255))
                        WIN.blit(levelDescTextLarge, (pos[0], pos[1]+lineIndex*linePadding))

                        lineIndex += 1

                # Description
                DisplayMultiLine(l.desc, levelSubtextFontLarge, (int(21*config.size),int(61*config.size)), int(15*config.size), int(255*config.size)) 

                # Brief
                DisplayMultiLine(l.brief, levelSubtextBFontLarge, (int(250*config.size),int(210*config.size)), int(20*config.size), int(230*config.size)) 

                # Board
                size = 0.3
                boardImg = l.GetImg()
                boardImg = pygame.transform.scale(l.GetImg(), (int(boardImg.get_width()*size), int(boardImg.get_height()*size)))

                pygame.draw.rect(WIN, (0, 0, 0), (int(277*config.size), int(27*config.size), boardImg.get_width()+int(2*config.size), boardImg.get_height()+int(((100*size)+2)*config.size)))
                WIN.blit(boardImg, (int(278*config.size), int(28*config.size)))
                pygame.draw.rect(WIN, (160, 50, 0), (int(278*config.size), int(28*config.size)+boardImg.get_height(), boardImg.get_width(), int(100*size*config.size)))

                # Dustin
                WIN.blit(GetImage("dustinPogPet", (230,230)), (int(6*config.size), int(214*config.size)))

            index += 1

        # Achevements and progress
        x = WIDTH//3*2+int(4*config.size)
        y = HEIGHT//2.2
        xW = WIDTH//3-int(8*config.size)
        yW = HEIGHT//1.8-int(8*config.size)
        pygame.draw.rect(WIN, (0, 0, 20), (x,y,xW,yW), False, rounding)
        pygame.draw.rect(WIN, (0, 0, 10), (x,y,xW,yW), 2, rounding)


        mouseX = pygame.mouse.get_pos()[0]
        mouseY = pygame.mouse.get_pos()[1]

        x = int(278*config.size)
        y = int(28*config.size)
        xW = (selectedLevel.GetImg().get_width()+int(2*config.size))*0.3
        yW = (selectedLevel.GetImg().get_height()+int(2*config.size))*0.3
                    
        if mouseX > x and mouseX < x + xW:
            if mouseY > y and mouseY < y + yW:
                s = pygame.Surface((selectedLevel.GetImg().get_width()*0.3, (selectedLevel.GetImg().get_height())*0.3))
                s.set_alpha(50)
                s.fill((220,240,180))
                WIN.blit(s, (int(278*config.size), int(28*config.size)))

        
        pygame.display.update()


    levelScroll = 0

    selectedLevel = levels[0]

    #Game Loop
    while True:
        clock.tick(FPS)

        RedrawWindow()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX = pygame.mouse.get_pos()[0]
                mouseY = pygame.mouse.get_pos()[1]
                
                x = WIDTH//3*2+int(4*config.size)
                y = int(5*config.size)
                xW = WIDTH//3-int(8*config.size)
                yW = HEIGHT//2.2-int(10*config.size)
                if mouseX > x and mouseX < x + xW:
                    if mouseY > y and mouseY < y + yW:
                        if event.button == 4 and levelScroll > 0:
                            levelScroll -= 1
                        elif event.button == 5 and levelScroll < len(levels)-3:
                            levelScroll += 1

                if event.button == 1:
                    x = int(278*config.size)
                    y = int(28*config.size)
                    xW = (selectedLevel.GetImg().get_width()+int(2*config.size))*0.3
                    yW = (selectedLevel.GetImg().get_height()+int(2*config.size))*0.3
                    
                    if mouseX > x and mouseX < x + xW:
                        if mouseY > y and mouseY < y + yW:
                            Game(selectedLevel)
                    
                    index = 0
                    for l in levels:
                        if index >= levelScroll and index < levelScroll + 3:
                            levelYOffset = (index-levelScroll)*int(64*config.size)

                            panelX = WIDTH//3*2+int(4*config.size)
                            panelY = 0

                            x = panelX+int(2*config.size)
                            y = panelY+int(5*config.size)+levelYOffset
                            xW = xW-int(2*config.size)
                            yW = int(64*config.size)
                            if mouseX > x and mouseX < x + xW:
                                if mouseY > y and mouseY < y + yW:
                                    selectedLevel = l

                        index += 1



def Game(lev):
    def RedrawWindow():

        # General Structure
        WIN.blit(lev.GetImg(0.8), (0,0))

        SizeConstant = 0.5562

        WIN.blit(GetImage("GameSidebar", relativeSize=(SizeConstant+0.004, SizeConstant+0.004)), (lev.GetImg(0.8).get_width(), 0))
        WIN.blit(GetImage("BottomBoard", relativeSize=(SizeConstant, SizeConstant)), (0, lev.GetImg(0.8).get_height()))

        # Tower Type Buttons
        ButtonImg = GetImage("TypeButton", relativeSize=(SizeConstant, SizeConstant))

        WIN.blit(ButtonImg, (int(3.5*config.size), lev.GetImg(0.8).get_height() + int(5*config.size)))
        WIN.blit(ButtonImg, (int(3.5*config.size), lev.GetImg(0.8).get_height() + int(26*config.size)))
        WIN.blit(ButtonImg, (int(3.5*config.size), lev.GetImg(0.8).get_height() + int(47*config.size)))
        WIN.blit(ButtonImg, (int(3.5*config.size), lev.GetImg(0.8).get_height() + int(68*config.size)))

        TypeFont = pygame.font.Font("Assets/Fonts/SegoePrintItalic.ttf", int(15*config.size))

        textImage = TypeFont.render("Primery", 1, (2, 2, 2))
        textImage = pygame.transform.scale(textImage, (textImage.get_width(), int(textImage.get_height()*0.8)))
        x = int(3.5*config.size) + (ButtonImg.get_width()//2 - textImage.get_width()//2)
        y = lev.GetImg(0.8).get_height() + int(5*config.size)  + (ButtonImg.get_height()//2 - textImage.get_height()//1.77)
        WIN.blit(textImage, (x, y))
        
        textImage = TypeFont.render("Militery", 1, (2, 2, 2))
        textImage = pygame.transform.scale(textImage, (textImage.get_width(), int(textImage.get_height()*0.8)))
        x = int(3.5*config.size) + (ButtonImg.get_width()//2 - textImage.get_width()//2)
        y = lev.GetImg(0.8).get_height() + int(26*config.size)  + (ButtonImg.get_height()//2 - textImage.get_height()//1.77)
        WIN.blit(textImage, (x, y))

        textImage = TypeFont.render("Magical", 1, (2, 2, 2))
        textImage = pygame.transform.scale(textImage, (textImage.get_width(), int(textImage.get_height()*0.8)))
        x = int(3.5*config.size) + (ButtonImg.get_width()//2 - textImage.get_width()//2)
        y = lev.GetImg(0.8).get_height() + int(47*config.size)  + (ButtonImg.get_height()//2 - textImage.get_height()//1.77)
        WIN.blit(textImage, (x, y))

        textImage = TypeFont.render("Support", 1, (2, 2, 2))
        textImage = pygame.transform.scale(textImage, (textImage.get_width(), int(textImage.get_height()*0.8)))
        x = int(3.5*config.size) + (ButtonImg.get_width()//2 - textImage.get_width()//2)
        y = lev.GetImg(0.8).get_height() + int(68*config.size)  + (ButtonImg.get_height()//2 - textImage.get_height()//1.77)
        WIN.blit(textImage, (x, y))

        # Tower Profile Images
        ProfileImg = GetImage("TowerProfile", relativeSize=(SizeConstant, SizeConstant))

        for i in range(0, 7): 
            x = int(105*config.size + i*100)
            y = (HEIGHT-lev.GetImg(0.8).get_height())//2 - ProfileImg.get_height()//2  + lev.GetImg(0.8).get_height()
            WIN.blit(ProfileImg, (x, y))

        # Play/Pause Buttons
        PlayImg = GetImage("PlayButton", relativeSize=(SizeConstant, SizeConstant))
        PauseImg = GetImage("PauseButton", relativeSize=(SizeConstant, SizeConstant))

        WIN.blit(PlayImg, (int(662*config.size), int(380*config.size)))
        WIN.blit(PauseImg, (int(726*config.size), int(380*config.size)))

        # Speed Button
        SpeedImg = GetImage("EmptyButton", relativeSize=(SizeConstant * 0.8, SizeConstant * 0.8))
        WIN.blit(SpeedImg, (int(589*config.size), int(7*config.size)))

        SpeedFont = pygame.font.Font("Assets/Fonts/SubscribeRegular.ttf", int(26*config.size))
        TextImg = SpeedFont.render("3X", 1, (32, 236, 31))
        WIN.blit(TextImg, (int(597*config.size), int(19*config.size)))

        pygame.display.update()

    while True:
        clock.tick(FPS)

        RedrawWindow()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()



MainMenu()