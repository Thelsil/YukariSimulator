import math
from enum import Enum, auto

from src.CONSTANTS import CONSTANTS
from src.quickSort import quickSort


class Unit:
    def __init__(self, characterName: str, TPBoost: int = 0):

        if characterName not in unitsRange.keys():
            raise RuntimeError("Unit name '" + characterName + "'not found in the 'unitsRange' dictionary.")

        # Public attributes
        self.name = characterName
        self.position = 0
        self.attackRange = unitsRange[characterName]
        self.TPValue  = 0
        self.TPBoost  = TPBoost
        self.attackWidth = CONSTANTS.NORMAL_ATTACK_WIDTH


        # Protected attributes.
        self._moveStep = CONSTANTS.MOVE_STEP_START
        self._behaviour = eBehaviour.STARTING
        self.__frameCount = 0
        self._drawWeaponFrameCount = 0


    def __repr__(self):
        return repr((self.name, math.floor(self.position),  math.floor(self.TPValue),self.__frameCount))


    def reset(self):
        self.__frameCount = 0
        self.TPValue = 0
        self._drawWeaponFrameCount = 0
        self._behaviour = eBehaviour.STARTING

    def gainTP(self,value):
        self.TPValue += value * (1 + self.TPBoost / 100)
        if self.TPValue > CONSTANTS.CHARGED_TP_VALUE:
            self.TPValue = CONSTANTS.CHARGED_TP_VALUE

    def move(self, direction):
        self.position += self._moveStep * direction

    def isActionFinished(self):
        return self._behaviour is eBehaviour.FINISH

    def update(self, ownTeam, oppositeTeam):

        if self._behaviour is eBehaviour.FINISH:
            return

        self.__frameCount +=1

        if self._behaviour == eBehaviour.STARTING:
            self._startingBehaviour(oppositeTeam)
            self._drawWeaponFrameCount = 0
            return

        if self._behaviour == eBehaviour.DRAW_WEAPON:
            self._drawWeaponBehaviour()
            return

        if self._behaviour == eBehaviour.START_SKILL:
            self._startSkillBehaviour(ownTeam, oppositeTeam)
            self.gainTP(CONSTANTS.TP_GAIN_PER_ACTION)
            self._behaviour = eBehaviour.EXECUTE_SKILL
            return

        if self._behaviour == eBehaviour.EXECUTE_SKILL:
            self._executeSkillBehaviour(ownTeam, oppositeTeam)
            return



    def getDirection(self, unitObj):
        if unitObj.position - self.position > 0:
            return 1
        else:
            return -1

    def getDistance(self, unitObj):
        return abs(unitObj.position - self.position)

    def getEffectiveRange(self, unitObj):
        return self.attackRange + (unitObj.attackWidth + self.attackWidth) / 2


    def _startingBehaviour(self,oppositeTeam):

        closestUnit = self._findClosestTarget(oppositeTeam)
        self.move(self.getDirection(closestUnit))

        if self.isInRange(closestUnit):
            self._behaviour = eBehaviour.DRAW_WEAPON

    def _drawWeaponBehaviour(self):

        if self._drawWeaponFrameCount >= CONSTANTS.NUM_FRAME_DRAW_WEAPON:
            self._behaviour = eBehaviour.START_SKILL
        self._drawWeaponFrameCount += 1

    def _startSkillBehaviour(self, ownTeam,oppositeTeam):
        pass

    def _executeSkillBehaviour(self,ownTeam, oppositeTeam):
        self._behaviour = eBehaviour.FINISH

    def _findClosestTarget(self, team):

        # First, check if there are any unit in range.
        targetsList = list([u for u in team if self.isInRange(u)])

        # If no targets in range, set the whole team as potential target.
        if not targetsList:
            targetsList = team

        # Return the unit that has the minimum distance
        return min(targetsList, key=lambda u: self.getDistance(u))



    def isInRange(self, unitObj):

        distance = self.getDistance(unitObj)
        effectiveRange = self.getEffectiveRange(unitObj)

        if distance < effectiveRange:
            return True
        else:
            return False


class Lima(Unit):

    def __init__(self, TPBoost = 0):
        super().__init__("Lima", TPBoost)

        self.attackWidth = 0
        self._moveStep = CONSTANTS.MOVE_STEP_LIMA_CHARGE
        self.__skillTarget = None

    def _startingBehaviour(self,oppositeTeam):
        self.__skillTarget = None
        self._behaviour = eBehaviour.DRAW_WEAPON

    def _drawWeaponBehaviour(self):

        if self._drawWeaponFrameCount >= CONSTANTS.NUM_FRAME_LIMA_WAIT:
            self._behaviour = eBehaviour.START_SKILL
        self._drawWeaponFrameCount += 1

    def _startSkillBehaviour(self, ownTeam,oppositeTeam):
        self.__skillTarget = self._findClosestTarget(oppositeTeam)

    def _executeSkillBehaviour(self,ownTeam, oppositeTeam):
        self.move(self.getDirection(self.__skillTarget))

        if self.isInRange(self.__skillTarget):
            self._behaviour = eBehaviour.FINISH



class Yukari(Unit):

    def __init__(self, TPBoost = 0):
        super().__init__("Yukari", TPBoost)
        self.__skillTarget = None


    def _startSkillBehaviour(self, ownTeam,oppositeTeam):

        self.__skillTarget = quickSort(ownTeam, "TPValue", CONSTANTS.QUICK_SORT_VERBOSE)(0)

        if CONSTANTS.YUKARI_TP_SKILL_VERBOSE:
            print("Team state before Yukari TP boost skill: " + str(ownTeam))
            print("Unit TP boosted by Yukari: " + str(self.__skillTarget))

    def _executeSkillBehaviour(self,ownTeam, oppositeTeam):
        self.__skillTarget.gainTP(CONSTANTS.YUKARI_TP_GAIN_VALUE)
        self._behaviour = eBehaviour.FINISH

class eBehaviour(Enum):
    STARTING = auto()
    DRAW_WEAPON = auto()
    START_SKILL = auto()
    EXECUTE_SKILL = auto()
    FINISH = auto()

class ePosition(Enum):
    FRONT = 0
    MIDDLE = 299
    BACK = 599

unitsRange = {
    "Lima": 105,
    "Miyako": 125,
    "Kuka": 130,
    "Jun": 135,
    "Kaori": 145,
    "Pecorine": 155,
    "Nozomi": 160,
    "Makoto": 165,
    "Akino": 180,
    "Matsuri": 185,
    "Tsumugi": 195,
    "Hiyori": 200,
    "Misogi": 205,
    "Ayane": 210,
    "Tamaki": 215,
    "Tomo": 220,
    "S.Tamaki": 225,
    "Eriko": 230,
    "S.Pecorine": 235,
    "Kurumi": 240,
    "Djeeta": 245,
    "Rei": 250,
    "Shizuru": 285,
    "Mimi": 360,
    "Shinobu":365,
    "Mahiru": 395,
    "Yukari": 405,
    "Monika": 410,
    "Ninon": 415,
    "Mifuyu": 420,
    "Illya": 425,
    "Saren": 430,
    "H.Shinobu":440,
    "Anna": 440,
    "S.Miyufu": 495,
    "Kokkoro": 500,
    "S.Kokkoro": 535,
    "Rin": 550,
    "Mitsuki": 565,
    "Akari": 570,
    "Yori": 575,
    "Arisa": 625,
    "Rino": 700,
    "Suzuna": 705,
    "Shiori": 710,
    "Io": 715,
    "Suzume": 720,
    "Misato": 735,
    "Karyl": 750,
    "Hatsune": 755,
    "Misaki": 760,
    "S.Suzume": 775,
    "S.Karyl": 780,
    "Aoi": 785,
    "Chika": 790,
    "Maho": 795,
    "Yui": 800,
    "Yuki": 805,
    "Kyoka": 810,
    "Dummy1":0,
    "Dummy2":0,
    "Dummy3":0,
    "Dummy4":0,
    "Dummy5":0,
    "Reserved":0}
