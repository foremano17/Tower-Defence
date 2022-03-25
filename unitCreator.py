from pygame.draw import line
import Images
import config
import pygame
import os
import importlib
import Anim

WIDTH, HEIGHT = int(900*config.size), int(450*config.size)
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
FPS =  30
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



class Unit:
    def __init__(self, info={}, smallProfPic=pygame.Surface((50,50)), largeProfPic=pygame.Surface((50,50)), idleAnim=[], attackAnim=[], update=None, summonAnim=[], code=None):
        self.smallProfPic = smallProfPic
        self.largeProfPic = largeProfPic
        self.idleAnim = idleAnim
        self.attackAnim = attackAnim
        self.update = update
        self.summonAnim = summonAnim
        self.code = code
        self.info = info


class Enemy(Unit):
    enemies = []

    def __init__(self, info={}, smallProfPic=pygame.Surface((50,50)), largeProfPic=pygame.Surface((50,50)), idleAnim=[], attackAnim=[], update=None, summonAnim=[], code=None, walkingAnims={"up":[], "down":[], "left":[], "right":[]}, deathAnim=[], attack=None, summon=None, death=None, damaged=None):
        self.walkingAnims = walkingAnims
        self.deathAnim = deathAnim
        self.update = update
        self.attack = attack
        self.summon = summon
        self.death = death
        self.damaged = damaged
        self.type = "Enemy"
        
        super().__init__(info, smallProfPic, largeProfPic, idleAnim, attackAnim, update, summonAnim, code)

    @classmethod
    def Create(self, info={}, smallProfPic=pygame.Surface((50,50)), largeProfPic=pygame.Surface((50,50)), idleAnim=[], attackAnim=[], update=None, summonAnim=[], code=None, walkingAnims={"up":[], "down":[], "left":[], "right":[]}, deathAnim=[], attack=None, summon=None, death=None, damaged=None):
        Enemy.enemies.append( Enemy(info, smallProfPic, largeProfPic, idleAnim, attackAnim, update, summonAnim, code, walkingAnims, deathAnim, attack, summon, death, damaged) )

        return Enemy.enemies[-1]


class Tower(Unit):
    towers = []

    def __init__(self, info={}, smallProfPic=pygame.Surface((50,50)), largeProfPic=pygame.Surface((50,50)), idleAnim=[], attackAnim=[], update=None, summonAnim=[], code=None, despawnAnim=[], despawn=None, ability=None):
        self.despawn = despawn
        self.despawnAnim = despawnAnim
        self.ability = ability
        self.type = "Tower"
        
        super().__init__(info, smallProfPic, largeProfPic, idleAnim, attackAnim, update, summonAnim, code)

    @classmethod
    def Create(self, info={}, smallProfPic=pygame.Surface((50,50)), largeProfPic=pygame.Surface((50,50)), idleAnim=[], attackAnim=[], update=None, summonAnim=[], code=None, despawnAnim=[], despawn=None, ability=None):
        Enemy.enemies.append( Tower(info, smallProfPic, largeProfPic, idleAnim, attackAnim, update, summonAnim, code, despawnAnim, despawn, ability) )

        return Tower.towers[-1]


class TextBox:
    allBoxes = []

    cursorBlinkCount = 0


    FPS = 30

    @classmethod
    def init(self, FPS=30):
        TextBox.FPS = FPS

    def __init__(self, x=0, y=0, colour=(240, 240, 240), contents="", width=None, yPadding=3, font=pygame.font.Font("Assets/Fonts/RobotoMono.ttf", 8), fontColour=(0,0,0), xOffsetText=0, yOffsetText=0, outlineColour=(20,20,20), charLimit=None, lines=1, linePadding=2, locked=False):
        self.x = x
        self.y = y
        self.colour = colour
        self.contents = contents
        self.width = width
        self.yPadding = yPadding
        self.linePadding = linePadding
        self.font = font
        self.fontColour = fontColour
        self.selected = False
        self.selectedCol = 0
        self.selectedRow = 0
        self.xOffsetText = xOffsetText
        self.yOffsetText = yOffsetText
        self.outlineColour = outlineColour
        self.charLimit = charLimit
        self.lines = lines
        self.textHeight = font.render("M", 1, (0,0,0)).get_height()
        self.textWidth = font.render("M", 1, (0,0,0)).get_width()
        self.locked = locked


        if width == None and len(contents) > 0:
            longestLine = ""

            for line in contents:
                if len(line) > len(longestLine):
                    longestLine = line

            self.width = font.render(longestLine, 1, (0,0,0)).get_width() + xOffsetText*2

        elif width == None:
            self.width = 100


        self.height = font.render("M", 1, (0,0,0)).get_height()*lines + 2*yPadding + (lines-1)*linePadding


        if contents == None:
            self.contents = [""]

        while len(contents) > lines:
            contents.remove(contents[-1])

        if charLimit == None:
            maxLetterSize = font.render("M", 1, (0,0,0)).get_width()

            self.charLimit = self.width // maxLetterSize

        
        TextBox.allBoxes.append(self)

    @classmethod
    def Left(self):
        box = TextBox.GetSelectedBox()

        if box != None and box.selectedCol > 0:
            box.selectedCol -= 1
            TextBox.cursorBlinkCount = 0

    @classmethod
    def Right(self):
        box = TextBox.GetSelectedBox()

        if box != None and box.selectedCol < len(box.contents[box.selectedRow]):
            box.selectedCol += 1
            TextBox.cursorBlinkCount = 0

    @classmethod
    def Up(self):
        box = TextBox.GetSelectedBox()

        if box != None and box.selectedRow > 0:
            box.selectedRow -= 1
            TextBox.cursorBlinkCount = 0

            if box.selectedCol > len(box.contents[box.selectedRow]):
                box.selectedCol = len(box.contents[box.selectedRow])

    @classmethod
    def Down(self):
        box = TextBox.GetSelectedBox()

        if box != None and box.selectedRow < len(box.contents)-1:
            box.selectedRow += 1
            TextBox.cursorBlinkCount = 0

            if box.selectedCol > len(box.contents[box.selectedRow]):
                box.selectedCol = len(box.contents[box.selectedRow])

    @classmethod
    def AddLine(self):
        box = TextBox.GetSelectedBox()

        if len(box.contents) < box.lines:
            copyContents = []
            
            for i, line in enumerate(box.contents):
                copyContents.append(line)

                if i == box.selectedRow:
                    copyContents.append("")
            
            box.contents = copyContents
            TextBox.Down()

    @classmethod
    def Type(self, charicter):
        box = TextBox.GetSelectedBox()

        if len(box.contents[box.selectedRow]) < box.charLimit:
            beforeCursor = box.contents[box.selectedRow][:box.selectedCol]
            afterCursor = box.contents[box.selectedRow][box.selectedCol:]

            amendedText = beforeCursor + charicter + afterCursor

            box.contents[box.selectedRow] = amendedText

            TextBox.Right()

    @classmethod
    def Delete(self):
        box = TextBox.GetSelectedBox()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LCTRL] and keys[pygame.K_LSHIFT]:
            for i in range(box.lines):
                box.contents[i] = ""

            box.selectedCol = 0
            box.selectedRow = 0

            return

        elif box.selectedCol == 0 and box.selectedRow != 0:
            prevLineLength = len(box.contents[box.selectedRow-1])

            if prevLineLength + len(box.contents[box.selectedRow]) <= box.charLimit:
                box.contents[box.selectedRow-1] += box.contents[box.selectedRow]

                box.contents.pop(box.selectedRow)

                TextBox.Up()

                box.selectedCol = prevLineLength

                return

        if keys[pygame.K_LCTRL]:
            words = box.contents[box.selectedRow].split(" ")
            words.remove(words[-1])

            amendedText = ""
            for word in words:
                amendedText += f"{word} "

            amendedText = amendedText[:-1]

            box.selectedCol = len(amendedText)

        else:
            box = TextBox.GetSelectedBox()

            beforeCursor = box.contents[box.selectedRow][:box.selectedCol]
            afterCursor = box.contents[box.selectedRow][box.selectedCol:]

            amendedText = beforeCursor[:-1] + afterCursor

            TextBox.Left()


        box.contents[box.selectedRow] = amendedText

    @classmethod
    def Draw(self):
        for b in TextBox.allBoxes:
            pygame.draw.rect(WIN, b.colour, (b.x, b.y, b.width, b.height))

            for i, line in enumerate(b.contents):
                text = b.font.render(line, 1, b.fontColour)
                WIN.blit(text, (b.x + b.xOffsetText, b.y + b.yPadding + i*(b.textHeight + b.linePadding)))

                if b.selected:
                    pygame.draw.rect(WIN, (20,100,230), (b.x-int(2*config.size), b.y-int(2*config.size), b.width+int(4*config.size), b.height+int(4*config.size)), int(2*config.size), int(2*config.size))

                    if TextBox.cursorBlinkCount < 0.5 and b.selectedRow == i:
                        beforeCursor = line[0:b.selectedCol]

                        xOffset = b.font.render(beforeCursor, 1, (0,0,0)).get_width()
                        yOffset = (b.textHeight + b.linePadding) * i

                        pygame.draw.rect(WIN, (20,20,20), (b.x + xOffset + b.xOffsetText, b.y + yOffset + int(3*config.size), int(2*config.size), b.textHeight))

                else:
                    pygame.draw.rect(WIN, b.outlineColour, (b.x, b.y, b.width, b.height), int(1*config.size), int(1*config.size))

    @classmethod
    def SelectBox(self, box):
        if box != None and not box.locked:
            for b in TextBox.allBoxes:
                if b is box:
                    b.selected = True

                    b.selectedCol = len(b.contents[-1])
                    b.selectedRow = len(b.contents)-1
                
                else:
                    b.selected = False

        else:
            for b in TextBox.allBoxes:
                b.selected = False

    @classmethod
    def GetSelectedBox(self):
        for b in TextBox.allBoxes:
            if b.selected:
                return b

    @classmethod
    def Reload(self):
        TextBox.allBoxes = []

    @classmethod
    def Update(self):
        TextBox.cursorBlinkCount += 1 / self.FPS

        if TextBox.cursorBlinkCount > 1:
            TextBox.cursorBlinkCount = 0

    @classmethod
    def LogEvent(self, event):
        mouseX = pygame.mouse.get_pos()[0]
        mouseY = pygame.mouse.get_pos()[1]

        if event.type == pygame.KEYDOWN:
            if TextBox.GetSelectedBox() != None:
                if event.key == pygame.K_LEFT:
                    TextBox.Left()

                elif event.key == pygame.K_RIGHT:
                    TextBox.Right()

                elif event.key == pygame.K_UP:
                    TextBox.Up()

                elif event.key == pygame.K_DOWN:
                    TextBox.Down()

                elif event.key == pygame.K_RETURN:
                    TextBox.AddLine()

                elif event.key == pygame.K_BACKSPACE:
                    TextBox.Delete()

                elif len(event.unicode) > 0:
                    TextBox.Type(event.unicode)


        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:

                boxClicked = False

                for b in TextBox.allBoxes:
                    x = b.x
                    y = b.y
                    width = b.width
                    height = b.height

                    if mouseX >= x and mouseX <= x+width:
                        if mouseY >= y and mouseY <= y+height:
                            TextBox.SelectBox(b)

                            TextBox.cursorBlinkCount = 0

                            boxClicked = True

                if not boxClicked:
                    TextBox.SelectBox(None)

TextBox.init(FPS=FPS)


def SelectionWindow():
    global units

    def RedrawWindow():
        pygame.draw.rect(WIN, (15, 15, 15), (0,0,WIDTH,HEIGHT))

        index = 0
        for u in units:
            WIN.blit(u.largeProfPic, (WIDTH//(4/4**(index%3) + 1) - u.largeProfPic.get_width()//2, int(30*config.size) + (index//3)*int(240*config.size) + int(scrollCount*50*config.size)))

            index += 1

        pygame.display.update()


    def GetUnits():
        allUnits = []

        for folder in os.listdir("Units"):
            for unit in os.listdir(f"Units/{folder}"):
                fileData = open(f"Units/{folder}/{unit}/info.txt", "r")

                lines = fileData.readlines()

                allInfo = {}
                for line in lines:
                    if line is not lines[-1]:
                        allInfo[line.split(":")[0]] = line.split(":")[1][:-1]
                    else:
                        allInfo[line.split(":")[0]] = line.split(":")[1]

                fileData.close()

                smallProfPic = pygame.image.load(os.path.join(f"Units/{folder}/{unit}/smallProfPic.png"))
                smallProfPic = pygame.transform.scale(smallProfPic, (int(100*config.size), int(100*config.size)))

                largeProfPic = pygame.image.load(os.path.join(f"Units/{folder}/{unit}/largeProfPic.png"))
                largeProfPic = pygame.transform.scale(largeProfPic, (int(200*config.size), int(200*config.size)))

                idleAnim = []
                for frame in os.listdir(f"Units/{folder}/{unit}/idleAnim"):
                    idleAnim.append(f"Units/{folder}/{unit}/idleAnim/{frame}")

                attackAnim = []
                for frame in os.listdir(f"Units/{folder}/{unit}/attackAnim"):
                    attackAnim.append(f"Units/{folder}/{unit}/attackAnim/{frame}")

                summonAnim = []
                for frame in os.listdir(f"Units/{folder}/{unit}/attackAnim"):
                    summonAnim.append(f"Units/{folder}/{unit}/attackAnim/{frame}")

                walkingAnims = {}
                for direction in os.listdir(f"Units/{folder}/{unit}/walkingAnims"):

                    currentAnim = []
                    for frame in os.listdir(f"Units/{folder}/{unit}/walkingAnims/{direction}"):
                        currentAnim.append(pygame.image.load(os.path.join(f"Units/{folder}/{unit}/walkingAnims/{direction}/{frame}")))

                    walkingAnims[direction] = currentAnim

                code = importlib.import_module(f"Units.{folder}.{unit}.code")



                if folder == "Enemies":
                    deathAnim = []
                    for frame in os.listdir(f"Units/{folder}/{unit}/deathAnim"):
                        deathAnim.append(f"Units/{folder}/{unit}/deathAnim/{frame}")

                    allUnits.append( Enemy.Create(info=allInfo, smallProfPic=smallProfPic, largeProfPic=largeProfPic, idleAnim=idleAnim, attackAnim=attackAnim, update=code.Update, summonAnim=summonAnim, code=code, walkingAnims=walkingAnims, deathAnim=deathAnim, attack=code.Attack, summon=code.Summon, death=code.Death, damaged=code.Damaged) )
                
                elif folder == "Towers":
                    despawnAnim = []
                    for frame in os.listdir(f"Units/{folder}/{unit}/despawnAnim"):
                        despawnAnim.append(f"Units/{folder}/{unit}/despawnAnim/{frame}")

                    allUnits.append( Tower.Create(info=allInfo, smallProfPic=smallProfPic, largeProfPic=largeProfPic, idleAnim=idleAnim, attackAnim=attackAnim, update=code.Update, summonAnim=summonAnim, code=code, despawnAnim=despawnAnim, despawn=code.Despawn, ability=code.Ability) )


        return allUnits

    units = GetUnits()

    scrollCount = 0

    while True:
        clock.tick(FPS)

        RedrawWindow()
        
        mouseX = pygame.mouse.get_pos()[0]
        mouseY = pygame.mouse.get_pos()[1]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    index = 0
                    for u in units:
                        x = WIDTH//(4/4**(index%3) + 1) - u.largeProfPic.get_width()//2
                        y = int(30*config.size) + (index//3)*int(240*config.size) + int(scrollCount*50*config.size)
                        width = u.largeProfPic.get_width()
                        height = u.largeProfPic.get_height()

                        if mouseX >= x and mouseX <= x+width:
                            if mouseY >= y and mouseY <= y+height:
                                EditWindow(u)

                        index += 1



                elif event.button == 4 and scrollCount < 0:
                    scrollCount += 1

                elif event.button == 5:
                    scrollCount -= 1
                

def AnimationWindow(unit, animName):
    def RedrawWindow():
        pygame.draw.rect(WIN, (100, 100, 100), (0,0,WIDTH,HEIGHT))
        pygame.draw.rect(WIN, (200, 200, 200), (int(2*config.size), int(2*config.size), WIDTH-int(4*config.size), HEIGHT-int(4*config.size)), 0, int(2*config.size))


        for i, f in enumerate(anim.frames):
            xOffset = i % 3 * int(90*config.size)
            yOffset = i // 3 * int(90*config.size)

            if selectedFrame[0] == f:
                pygame.draw.rect(WIN, (235, 255, 15), (int(10*config.size) + xOffset, int(170*config.size) + yOffset + scrollCount*SCROLL_BUFF, int(85*config.size), int(85*config.size)))
                pygame.draw.rect(WIN, (235*0.5, 255*0.5, 15*0.5), (int(10*config.size) + xOffset, int(170*config.size) + yOffset + scrollCount*SCROLL_BUFF, int(85*config.size), int(85*config.size)), 2, 2)

            pygame.draw.rect(WIN, (10, 10, 10), (int(15*config.size) + xOffset, int(175*config.size) + yOffset + scrollCount*SCROLL_BUFF, int(75*config.size), int(75*config.size)), int(2*config.size), int(2*config.size))


            frame = pygame.image.load(os.path.join(f))

            if frame.get_height() > frame.get_width():
                sizeMultiplyer = int(71*config.size) / frame.get_height()

            else:
                sizeMultiplyer = int(71*config.size) /frame.get_width()

            frame = pygame.transform.scale(frame, (int(frame.get_width() * sizeMultiplyer), int(frame.get_height() * sizeMultiplyer)))

            WIN.blit(frame, (int(15*config.size) + xOffset - frame.get_width()//2  + int(75*config.size/2), int(175*config.size) + yOffset + scrollCount*SCROLL_BUFF - frame.get_height()//2 + int(75*config.size/2)))

        xOffset = 0
        yOffset = 0

        if len(anim.frames) > 0:
            xOffset = (i+1) % 3 * int(90*config.size)
            yOffset = (i+1) // 3 * int(90*config.size)

        pygame.draw.rect(WIN, (35, 35, 35), (int(15*config.size) + xOffset, int(175*config.size) + yOffset + scrollCount*SCROLL_BUFF, int(75*config.size), int(75*config.size)), 0, int(2*config.size))
        pygame.draw.rect(WIN, (5, 5, 5), (int(15*config.size) + xOffset, int(175*config.size) + yOffset + scrollCount*SCROLL_BUFF, int(75*config.size), int(75*config.size)), int(2*config.size), int(2*config.size))
        
        plusFont = pygame.font.Font("Assets/Fonts/RobotoSlab.ttf", (50))
        plusImg = plusFont.render("+", 1, (245, 245, 245))

        WIN.blit(plusImg, (int(15*config.size) + xOffset + int(75*config.size)//2 - plusImg.get_width()//2, int(175*config.size) + yOffset + int(70*config.size)//2 - plusImg.get_height()//2 + scrollCount*SCROLL_BUFF))



        pygame.draw.rect(WIN, (200, 200, 200), (int(2*config.size), int(2*config.size), WIDTH-int(4*config.size), int(165*config.size)), 0, int(2*config.size))
        
        pygame.draw.rect(WIN, (100, 100, 100), (0, 0, WIDTH, int(2*config.size)))
        pygame.draw.rect(WIN, (100, 100, 100), (0, HEIGHT-int(2*config.size), WIDTH, int(4*config.size)))


        symbolFont = pygame.font.Font("Assets/Fonts/RobotoSlab.ttf", (70))

        #Next
        pygame.draw.rect(WIN, (30, 30, 30), (int(280*config.size), int(175*config.size), int(70*config.size), int(75*config.size)), 0, int(2*config.size))
        pygame.draw.rect(WIN, (160, 160, 160), (int(282*config.size), int(177*config.size), int(66*config.size), int(71*config.size)), 0, int(2*config.size))

        nextImg = symbolFont.render(">", 1, (245, 245, 245))

        WIN.blit(nextImg, (int(280*config.size) + int(70*config.size)//2 - nextImg.get_width()//2, int(175*config.size) + int(75*config.size)//2.35 - nextImg.get_height()//2))

        #Last
        pygame.draw.rect(WIN, (30, 30, 30), (int(280*config.size), int(265*config.size), int(70*config.size), int(75*config.size)), 0, int(2*config.size))
        pygame.draw.rect(WIN, (160, 160, 160), (int(282*config.size), int(267*config.size), int(66*config.size), int(71*config.size)), 0, int(2*config.size))
        
        lastImg = symbolFont.render("<", 1, (245, 245, 245))

        WIN.blit(lastImg, (int(280*config.size) + int(70*config.size)//2 - lastImg.get_width()//2, int(265*config.size) + int(75*config.size)//2.35 - lastImg.get_height()//2))
        
        #Play / Pause ▶
        pygame.draw.rect(WIN, (30, 30, 30), (int(280*config.size), int(355*config.size), int(70*config.size), int(75*config.size)), 0, int(2*config.size))
        pygame.draw.rect(WIN, (160, 160, 160), (int(282*config.size), int(357*config.size), int(66*config.size), int(71*config.size)), 0, int(2*config.size))

        if animPlaying:
            playImg = symbolFont.render("...", 1, (245, 245, 245))

            WIN.blit(playImg, (int(280*config.size) + int(70*config.size)//2 - playImg.get_width()//2, int(355*config.size) + int(75*config.size)//2.05 - playImg.get_height()//2))

        else:
            pauseImg = symbolFont.render("| |", 1, (245, 245, 245))

            WIN.blit(pauseImg, (int(280*config.size) + int(70*config.size)//2 - pauseImg.get_width()//2, int(355*config.size) + int(75*config.size)//2.3 - pauseImg.get_height()//2))


        pygame.draw.rect(WIN, (25, 25, 25), (WIDTH//2 + int(14*config.size), int(8*config.size), WIDTH//2 - int(14*config.size)*2, WIDTH//2 - int(14*config.size)*2))
        pygame.draw.rect(WIN, (245, 245, 245), (WIDTH//2 + int(16*config.size), int(10*config.size), WIDTH//2 - int(16*config.size)*2, WIDTH//2 - int(16*config.size)*2))

        framePreview = pygame.image.load(os.path.join(selectedFrame[0]))

        if len(anim.frames) > 0:
            if frame.get_height() > frame.get_width():
                sizeMultiplyer = (WIDTH//2 - int(16*config.size)*2) / framePreview.get_height()

            else:
                sizeMultiplyer = (WIDTH//2 - int(16*config.size)*2) /framePreview.get_width()

            framePreview = pygame.transform.scale(framePreview, (int(framePreview.get_width() * sizeMultiplyer), int(framePreview.get_height() * sizeMultiplyer)))  

            WIN.blit(framePreview, (WIDTH//2 + int(14*config.size) + (WIDTH//2 - int(14*config.size)*2)/2 - framePreview.get_width()//2, int(8*config.size) + (WIDTH//2 - int(14*config.size)*2)/2 - framePreview.get_height()//2))


        TextBox.Draw();

        labelFont = pygame.font.Font("Assets/Fonts/RobotoMono.ttf", int(11*config.size))
        speedText = labelFont.render("Speed:", 1, (5, 5, 5))
        WIN.blit(speedText, (int(18*config.size), int(66*config.size)))

        pygame.display.update()


    TextBox.Reload()


    nameFont = pygame.font.Font("Assets/Fonts/RobotoMono.ttf", int(10*config.size))
    unitNameBox = TextBox(x=int(13*config.size), y=int(10*config.size), contents=[unit.info["Name"]], xOffsetText=int(5*config.size), font=nameFont, locked=True)

    animFont = pygame.font.Font("Assets/Fonts/RobotoMono.ttf", int(18*config.size))
    animNameBox = TextBox(x=int(18*config.size), y=int(33*config.size), contents=[animName], xOffsetText=int(5*config.size), font=animFont, locked=True)

    animSpeedBox = TextBox(x=int(18*config.size), y=int(80*config.size), contents=[unit.info[f"{animName}Speed"]], xOffsetText=int(5*config.size), font=animFont, width=int(32*config.size))


    if animName == "Idle":
        allFrames = unit.idleAnim

    elif animName == "Summon":
        allFrames = unit.summonAnim

    elif animName == "Attack":
        allFrames = unit.attackAnim

    elif animName == "Death":
        allFrames = unit.deathAnim

    elif animName == "Walking":
        pass #########################################################################################

    anim = Anim.Anim(frames=allFrames, name=animName)

    selectedFrame = [anim.frames[0], 0]

    animCounter = 0

    animPlaying = False


    scrollCount = 0
    SCROLL_BUFF = int(25*config.size)


    while True:
        clock.tick(FPS)

        RedrawWindow()

        TextBox.Update()

        if animPlaying:
            animCounter += 1

            try:
                if animCounter >= FPS / int(animSpeedBox.contents[0]):
                    animCounter = 0

                    newFrameNum = selectedFrame[1] + 1

                    if newFrameNum >= len(anim.frames) - 1:
                        newFrameNum -= len(anim.frames) - 1

                    selectedFrame = [anim.frames[newFrameNum], newFrameNum]

            except:
                if animCounter >= FPS / int(unit.info[f"{animName}Speed"]):
                    animCounter = 0

                    newFrameNum = selectedFrame[1] + 1

                    if newFrameNum >= len(anim.frames):
                        newFrameNum -= len(anim.frames)

                    selectedFrame = [anim.frames[newFrameNum], newFrameNum]

        mouseX = pygame.mouse.get_pos()[0]
        mouseY = pygame.mouse.get_pos()[1]

        for event in pygame.event.get():

            TextBox.LogEvent(event)

            if event.type == pygame.DROPFILE and (event.file[-3:] == "png" or event.file[-3:] == "jpg"):

                xOffset = len(anim.frames) % 3 * int(90*config.size)
                yOffset = len(anim.frames) // 3 * int(90*config.size)

                x = int(15*config.size) + xOffset
                y = int(175*config.size) + yOffset + scrollCount*SCROLL_BUFF
                w = int(75*config.size)
                h = int(75*config.size)

                if mouseX >= x and mouseX <= x + w:
                    if mouseY >= y and mouseY <= y + h:
                        anim.frames.append(event.file)

                        selectedFrame = [event.file, len(anim.frames)-1]

            if event.type == pygame.QUIT:
                EditWindow(unit)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4 and scrollCount < 0:
                    scrollCount += 1

                elif event.button == 5:
                    scrollCount -= 1

                elif event.button == 2:
                    for i, f in enumerate(anim.frames):
                        xOffset = i % 3 * int(90*config.size)
                        yOffset = i // 3 * int(90*config.size)

                        x = int(15*config.size) + xOffset
                        y = int(175*config.size) + yOffset + scrollCount*SCROLL_BUFF
                        w = int(75*config.size)
                        h = int(75*config.size)

                        if mouseX >= x and mouseX <= x + w:
                            if mouseY >= y and mouseY <= y + h:
                                anim.frames.pop(i)

                                if len(anim.frames) > 0:
                                    selectedFrame = [anim.frames[0], 0]

                elif event.button == 1:
                    for i, f in enumerate(anim.frames):
                        xOffset = i % 3 * int(90*config.size)
                        yOffset = i // 3 * int(90*config.size)

                        x = int(15*config.size) + xOffset
                        y = int(175*config.size) + yOffset + scrollCount*SCROLL_BUFF
                        w = int(75*config.size)
                        h = int(75*config.size)

                        if mouseX >= x and mouseX <= x + w:
                            if mouseY >= y and mouseY <= y + h:
                                selectedFrame = [f, i]

                    if len(anim.frames) > 0:
                        x, y, w, h = int(280*config.size), int(175*config.size), int(70*config.size), int(75*config.size)

                        if mouseX >= x and mouseX <= x + w:
                            if mouseY >= y and mouseY <= y + h:
                                animCounter = 0

                                newFrameNum = selectedFrame[1] + 1

                                if newFrameNum >= len(anim.frames):
                                    newFrameNum -= len(anim.frames)

                                selectedFrame = [anim.frames[newFrameNum], newFrameNum]


                        x, y, w, h = int(280*config.size), int(265*config.size), int(70*config.size), int(75*config.size)

                        if mouseX >= x and mouseX <= x + w:
                            if mouseY >= y and mouseY <= y + h:
                                animCounter = 0

                                newFrameNum = selectedFrame[1] - 1

                                if newFrameNum < 0:
                                    newFrameNum += len(anim.frames)

                                selectedFrame = [anim.frames[newFrameNum], newFrameNum]


                        x, y, w, h = int(280*config.size), int(355*config.size), int(70*config.size), int(75*config.size)

                        if mouseX >= x and mouseX <= x + w:
                            if mouseY >= y and mouseY <= y + h:
                                animPlaying = not animPlaying



def EditWindow(unit):
    global WIDTH, HEIGHT
    global WIN

    def RedrawWindow():
        pygame.draw.rect(WIN, (100, 100, 100), (0,0,WIDTH,HEIGHT))
        pygame.draw.rect(WIN, (200, 200, 200), (int(2*config.size),int(2*config.size),WIDTH-int(4*config.size),HEIGHT-int(4*config.size)), 0, int(2*config.size))

        labelFontLarge = pygame.font.Font("Assets/Fonts/RobotoSlab.ttf", int(14*config.size))
        labelFontSmall = pygame.font.Font("Assets/Fonts/RobotoSlab.ttf", int(9.5*config.size))

        # Profile pics
        WIN.blit(unit.largeProfPic, (int(25*config.size), int(20*config.size)))
        pygame.draw.rect(WIN, (70, 70, 70), (int(24*config.size), int(19*config.size), int(202*config.size), int(202*config.size)), int(2*config.size))
        WIN.blit(unit.smallProfPic, (int(235*config.size), int(20*config.size)))
        pygame.draw.rect(WIN, (70, 70, 70), (int(234*config.size), int(19*config.size), int(102*config.size), int(102*config.size)), int(2*config.size))

        # Name
        nameLabelText = labelFontLarge.render("Name:", 1, (5, 5, 5))
        WIN.blit(nameLabelText, (int(20*config.size), int(223*config.size)))

        # Desc
        descLabelText = labelFontLarge.render("Description:", 1, (5, 5, 5))
        WIN.blit(descLabelText, (int(20*config.size), int(265.5*config.size)))

        # Speed
        descLabelText = labelFontLarge.render("Speed:", 1, (5, 5, 5))
        WIN.blit(descLabelText, (int(20*config.size), int(397*config.size)))

        # HP
        descLabelText = labelFontLarge.render("HP:", 1, (5, 5, 5))
        WIN.blit(descLabelText, (int(125*config.size), int(397*config.size)))

        # Idle Animation
        idleLabelText1 = labelFontSmall.render("Idle", 1, (5, 5, 5))
        idleLabelText2 = labelFontSmall.render("Animation:", 1, (5, 5, 5))
        WIN.blit(idleLabelText1, (int(233*config.size), int(122*config.size)))
        WIN.blit(idleLabelText2, (int(233*config.size), int(132*config.size)))

        WIN.blit(GetImage("Folder", relativeSize=(0.5, 0.5)), (int(238*config.size), int(149*config.size)))

        # Summon Animation
        summonLabelText1 = labelFontSmall.render("Summon", 1, (5, 5, 5))
        summonLabelText2 = labelFontSmall.render("Animation:", 1, (5, 5, 5))
        WIN.blit(summonLabelText1, (int(297*config.size), int(122*config.size)))
        WIN.blit(summonLabelText2, (int(297*config.size), int(132*config.size)))

        WIN.blit(GetImage("Folder", relativeSize=(0.5, 0.5)), (int(302*config.size), int(149*config.size)))

        # Attack Animation
        attackLabelText1 = labelFontSmall.render("Attack", 1, (5, 5, 5))
        attackLabelText2 = labelFontSmall.render("Animation:", 1, (5, 5, 5))
        WIN.blit(attackLabelText1, (int(233*config.size), int(182*config.size)))
        WIN.blit(attackLabelText2, (int(233*config.size), int(192*config.size)))

        WIN.blit(GetImage("Folder", relativeSize=(0.5, 0.5)), (int(238*config.size), int(209*config.size)))

        # Death Animation
        deathLabelText1 = labelFontSmall.render("Death", 1, (5, 5, 5))
        deathLabelText2 = labelFontSmall.render("Animation:", 1, (5, 5, 5))
        WIN.blit(deathLabelText1, (int(297*config.size), int(182*config.size)))
        WIN.blit(deathLabelText2, (int(297*config.size), int(192*config.size)))

        WIN.blit(GetImage("Folder", relativeSize=(0.5, 0.5)), (int(302*config.size), int(209*config.size)))

        # Walking Animations
        walkingLabelText = labelFontSmall.render("Walking Animations:", 1, (5, 5, 5))
        WIN.blit(walkingLabelText, (int(233*config.size), int(242*config.size)))

        WIN.blit(GetImage("Folder", relativeSize=(0.5, 0.5)), (int(245*config.size), int(259*config.size)))
        WIN.blit(GetImage("Folder", relativeSize=(0.5, 0.5)), (int(245*config.size), int(299*config.size)))
        WIN.blit(GetImage("Folder", relativeSize=(0.5, 0.5)), (int(292*config.size), int(259*config.size)))
        WIN.blit(GetImage("Folder", relativeSize=(0.5, 0.5)), (int(292*config.size), int(299*config.size)))


        TextBox.Draw()

        pygame.display.update()

# Towers:  name, desc, idleAnim, attackAnim, summonAnim, radius, range, price, despawnAnim

    WIDTH, HEIGHT = int(360*config.size), int(450*config.size)
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))

    newSmallImgPath = None
    newLargeImgPath = None


    TextBox.Reload()


    textboxFontLarge = pygame.font.Font("Assets/Fonts/RobotoMono.ttf", int(17*config.size))
    textboxFontSmall = pygame.font.Font("Assets/Fonts/RobotoMono.ttf", int(11*config.size))

    nameBox = TextBox(
        x=int(18*config.size), 
        y=int(240*config.size), 
        contents=[unit.info["Name"]],
        width=int(200*config.size), 
        yPadding=int(2*config.size), 
        font=textboxFontLarge,
        xOffsetText=int(5*config.size),
        lines=1
    )

    descBox = TextBox(
        x=int(18*config.size), 
        y=int(282.5*config.size), 
        contents=unit.info["Desc"].split(";"),
        width=int(200*config.size), 
        yPadding=int(2*config.size), 
        font=textboxFontSmall,
        xOffsetText=int(5*config.size),
        lines=7
    )

    speedBox = TextBox(
        x=int(18*config.size), 
        y=int(414*config.size), 
        contents=[str(unit.info["Speed"])],
        width=int(95*config.size), 
        yPadding=int(2*config.size), 
        font=textboxFontLarge,
        xOffsetText=int(5*config.size),
        lines=1
    )

    hpBox = TextBox(
        x=int(123*config.size), 
        y=int(414*config.size), 
        contents=[str(unit.info["Health"])],
        width=int(95*config.size), 
        yPadding=int(2*config.size), 
        font=textboxFontLarge,
        xOffsetText=int(5*config.size),
        lines=1
    )


    while True:
        clock.tick(FPS)

        RedrawWindow()

        TextBox.Update()


        mouseX = pygame.mouse.get_pos()[0]
        mouseY = pygame.mouse.get_pos()[1]
        
        for event in pygame.event.get():

            TextBox.LogEvent(event)


            if event.type == pygame.QUIT:
                exit()


            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:

                    x = int(238*config.size)
                    y = int(149*config.size)
                    w = GetImage("Folder", relativeSize=(0.5, 0.5)).get_width()
                    h = GetImage("Folder", relativeSize=(0.5, 0.5)).get_height()

                    if mouseX > x and mouseX < x + w:
                        if mouseY > y and mouseY < y + h:
                            AnimationWindow(unit, "Idle")


                    x = int(302*config.size)
                    y = int(149*config.size)
                    w = GetImage("Folder", relativeSize=(0.5, 0.5)).get_width()
                    h = GetImage("Folder", relativeSize=(0.5, 0.5)).get_height()

                    if mouseX > x and mouseX < x + w:
                        if mouseY > y and mouseY < y + h:
                            AnimationWindow(unit, "Summon")


                    x = int(238*config.size)
                    y = int(209*config.size)
                    w = GetImage("Folder", relativeSize=(0.5, 0.5)).get_width()
                    h = GetImage("Folder", relativeSize=(0.5, 0.5)).get_height()

                    if mouseX > x and mouseX < x + w:
                        if mouseY > y and mouseY < y + h:
                            AnimationWindow(unit, "Attack")


                    x = int(302*config.size)
                    y = int(209*config.size)
                    w = GetImage("Folder", relativeSize=(0.5, 0.5)).get_width()
                    h = GetImage("Folder", relativeSize=(0.5, 0.5)).get_height()

                    if mouseX > x and mouseX < x + w:
                        if mouseY > y and mouseY < y + h:
                            AnimationWindow(unit, "Death")
                            

                    x = int(245*config.size)
                    y = int(259*config.size)
                    w = GetImage("Folder", relativeSize=(0.5, 0.5)).get_width() + int(47*config.size)
                    h = GetImage("Folder", relativeSize=(0.5, 0.5)).get_height() + int(40*config.size)

                    if mouseX > x and mouseX < x + w:
                        if mouseY > y and mouseY < y + h:
                            AnimationWindow(unit, "Walking")



            
            if event.type == pygame.DROPFILE and (event.file[-3:] == "png" or event.file[-3:] == "jpg"):
                x = int(24*config.size)
                y = int(19*config.size)
                width = int(202*config.size)
                height = int(202*config.size)

                if mouseX >= x and mouseX <= x+width:
                    if mouseY >= y and mouseY <= y+height:
                        unit.largeProfPic = pygame.transform.scale(pygame.image.load(os.path.join(event.file)), (int(200*config.size), int(200*config.size)))
                        newLargeImgPath = event.file

                x = int(234*config.size)
                y = int(19*config.size)
                width = int(102*config.size)
                height = int(102*config.size)

                if mouseX >= x and mouseX <= x+width:
                    if mouseY >= y and mouseY <= y+height:
                        unit.smallProfPic = pygame.transform.scale(pygame.image.load(os.path.join(event.file)), (int(100*config.size), int(100*config.size)))
                        newSmallImgPath = event.file


SelectionWindow()