import pygame
import config

beginner = 0
easy = 1
medium = 2
hard = 3
titanic = 4

class Level:
    def __init__(self, name=None, tiles=None, pathpos=None, index=None, desc=None, brief=None, waves=0, difficulty=None):
        self.name = name
        self.tiles = tiles
        self.pathpos = pathpos
        self.index = index
        self.desc = desc
        self.brief = brief
        self.diff = difficulty
        self.waves = waves

        self.difficulty = difficulty

        if waves == 0:
            if difficulty == beginner:
                self.waves = 10
            elif difficulty == easy:
                self.waves = 25
            elif difficulty == medium:
                self.waves = 40
            elif difficulty == hard:
                self.waves = 60
            elif difficulty == titanic:
                self.waves = 100

    def GetStrDiff(self):
        ans = None

        if self.difficulty == beginner:
            ans = "Beginner"
        elif self.difficulty == easy:
            ans = "Easy"
        elif self.difficulty == medium:
            ans = "Medium"
        elif self.difficulty == hard:
            ans = "Hard"
        elif self.difficulty == titanic:
            ans = "Titanic"

        return ans

    def GetDiffFromStr(self, diff):
        ans = None

        if diff == "Beginner":
            ans = beginner
        elif diff == "Easy":
            ans = easy
        elif diff == "Medium":
            ans = medium
        elif diff == "Hard":
            ans = hard
        elif diff == "Titanic":
            ans = titanic

        return ans

    def GetImg(self, size=1):
        surf = pygame.Surface((int(800*config.size*size), int(450*config.size*size)))

        for t in self.tiles:
            surf.blit(pygame.transform.scale(t.img, (int(t.img.get_width()*size), int(t.img.get_height()*size))), (int(t.x*size), int(t.y*size)))

        return surf