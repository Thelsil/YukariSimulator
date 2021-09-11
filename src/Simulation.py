import math
from enum import Enum, auto

from src.CONSTANTS import CONSTANTS
from src.Unit import Lima, Yukari, Unit, unitsRange
from src.quickSort import quickSort


class Simulation:
    def __init__(self, attackerNameList = None, defenderNameList = None):

        # Public attributes.
        self.attackerTeam = []
        self.defenderTeam = []

        # Private attrubtes.
        self.__frameCount   = 0
        self.__simulEndFlag = False

        # Instanciate all attacker units.
        if attackerNameList:
            self.setAttackerTeam(attackerNameList)

        # Instanciate all defender units.
        if defenderNameList:
            self.setDefenderTeam(defenderNameList)


    def setTeam(self, unitList, side, TPBoostList=None):

        if side == Side.ATTACKER:
            self.setAttackerTeam(unitList, TPBoostList)
            return

        if side == Side.DEFENDER:
            self.setDefenderTeam(unitList, TPBoostList)
            return

        raise RuntimeError("Unknown team side input. Must be either 'Side.ATTACKER' or 'Side.DEFENDER'.")


    # Set the attacker team by giving the name of all units in a list
    def setAttackerTeam(self, unitList, TPBoostList=None):

        numberAttackers = len(unitList)

        if not TPBoostList:
            TPBoostList = [0] * numberAttackers

        # Instanciate all attacker units.
        self.attackerTeam = []
        for u in range(numberAttackers):
            unitObj = self.__instanciateUnit(unitList[u], TPBoostList[u])
            self.attackerTeam.append(unitObj)

        self.attackerTeam.sort(key=lambda unit: unit.attackRange)

    # Set the defender team by giving the name of all units in a list
    def setDefenderTeam(self, unitList, TPBoostList=None):

        numberDefenders = len(unitList)

        if not TPBoostList:
            TPBoostList = [0] * numberDefenders

        # Instanciate all defender units.
        self.defenderTeam = []
        for u in range(numberDefenders):
            unitObj = self.__instanciateUnit(unitList[u], TPBoostList[u])
            self.defenderTeam.append(unitObj)

        self.defenderTeam.sort(key=lambda unit: unit.attackRange)

    def reset(self):

        self.__frameCount = 0
        self.__simulEndFlag = False

        # Set attacker team initial positions.
        orderCount = 1
        for unit in self.attackerTeam:
            unit.reset()
            if unit.name == CONSTANTS.LIMA_NAME:
                unit.position = -CONSTANTS.INIT_LIMA_POSITION  # TODO: find the real start position of Lima...
            else:
                unit.position = -(CONSTANTS.INIT_START_POSITION + CONSTANTS.INIT_DISTANCE * orderCount)
            orderCount += 1

        # Set defender team initial positions.
        orderCount = 0
        for unit in self.defenderTeam:
            unit.reset()
            if unit.name == CONSTANTS.LIMA_NAME:
                unit.position = CONSTANTS.INIT_LIMA_POSITION  # TODO: find the real start position of Lima...
            else:
                unit.position = CONSTANTS.INIT_START_POSITION + CONSTANTS.INIT_DISTANCE * orderCount
            orderCount += 1

    def execute(self):


        # Reset simulation.
        self.reset()

        while not self.__simulEndFlag:

            # Update attack side.
            for unit in self.attackerTeam:
                unit.update(self.attackerTeam,self.defenderTeam)

            # Update defender side.
            for unit in self.defenderTeam:
                unit.update(self.defenderTeam,self.attackerTeam)

            self.__updateSimulState()

    def getTeam(self, side):
        if side == Side.ATTACKER:
            return self.attackerTeam
        else:
            return self.defenderTeam

    def setTPBoost(self, TPBoostList, side):
        team = self.getTeam(side)
        i = 0
        for tp in TPBoostList:
            team[i].TPBoost = tp
            i += 1

    def analysisStability(self,limaFlag: bool = False):

        savedDefenseTeam = self.defenderTeam
        unitTPStats_dict = {}

        allUnit_dict = unitsRange.copy()
        del allUnit_dict['Lima']
        for id in range(5):
            del allUnit_dict['Dummy' + str(id+1)]


        unitCount = 0
        for k in allUnit_dict.keys():

            if limaFlag:
                self.setDefenderTeam(['Lima',k])
            else:
                self.setDefenderTeam([k])

            self.execute()
            name = self.getHighestTPUnit(Side.ATTACKER).name

            if name in unitTPStats_dict.keys():
                unitTPStats_dict[name] += 1
            else:
                unitTPStats_dict[name] = 1
            unitCount += 1


        self.defenderTeam = savedDefenseTeam
        return unitTPStats_dict

    def getHighestTPUnit(self,side):
        team = self.getTeam(side)
        return max(team, key=lambda u: u.TPValue)

    def getUnit(self, unitName, side):
        team = self.getTeam(side)
        return next((unit for unit in team if unit.name == unitName), None)

    def getUnitsInRangeOf(self, unitName, side):

        team = self.getTeam(-side)
        unit = self.getUnit(unitName, side)
        return list([u for u in team if unit.isInRange(u)])


    def __instanciateUnit(self,name, TPBoost = None):
        if name == CONSTANTS.LIMA_NAME:
            return Lima(TPBoost)

        if name == CONSTANTS.YUKARI_NAME:
            return Yukari(TPBoost)

        return Unit(name,TPBoost)

    def __updateSimulState(self):

        # Increase frame counter.
        self.__frameCount += 1

        # The simulation stop if all units have finished their actions.
        attackersFinished = all(unit.isActionFinished() for unit in self.attackerTeam)
        defendersFinished = all(unit.isActionFinished() for unit in self.defenderTeam)

        if attackersFinished and defendersFinished:
            self.__simulEndFlag = True
        else:
            self.__simulEndFlag = False


class Side(int, Enum):
    ATTACKER = 1
    DEFENDER = -1


def shift(seq, n):
    return seq[n:] + seq[:n]
