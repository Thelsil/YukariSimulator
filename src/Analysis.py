from src.CONSTANTS import CONSTANTS as CST
from src.Simulation import Simulation, Side
from src.Unit import unitsRange

# This function can be used to analyse stability of Yukari TP boost.
# It is an advanced features that is a bit harder to use than the basic simulator functions.
# It takes as input an unit list ("unitList"). Optionally, the TP boost list can be given, otherwise
# it is initialized to 0 for each units. This function return a boolean value (or a list of boolean, see below),
# True if the case is stable and False if not stable.

# The primary goal of this function is to search TP boost cases for all possible front unit combination
# in the enemy team (+ case when Lima is pos 1).
# Example of a simple use case : analyseStability(['Miyako','Kuka','Shizuru','Yukari','Illya'])

# It is possible to enter one of the "Directive" listed below instead of an unit name:
# "F" = FRONT - Note: Lima is excluded from the FRONT units due to her special behaviour.
# "M" = MIDDLE
# "B" = BACK
# "X" = ANY
# "V" = VARIABLE - Note: "variableValues" input need to be defined
# "Y" = YUKARI
# Example 1: analyseStability(['F','Kuka','Shizuru','Y','Illya']) search all stability condition for all front units
# at position 1 behind position 2 (Kuka) , with Yukari in position 4.
# Example 2: analyseStability(['Miyako','F','Shizuru','Y','M']) search all stability condition for all front units
# between Miyako and Shizuru AND all middle units behind Yukari (Yukari is position 4).

# Finally, it is possible to set an unit with variable attack range. The stability conditions will be checked for all
# "variableValues" entered, and return a list of boolean.
# Example: analyseStability(['Miyako','Kuka','V','Yukari','Maho'],None,range(195,205)) search stability conditions when
# the attack range of unit at position 3 is equals to 195, 196 (...), and 204.

def analyseStability(unitList, TPBoostList = None, variableValues = None):

    # By default TP boost list is initialize at zero.
    if TPBoostList == None:
        TPBoostList = [0]*len(unitList)

    # Check if Yukari is present in the given unit list.
    if "Y" in unitList:
        unitList = [CST.YUKARI_NAME if u == "Y" else u for u in unitList]
    elif "Yukari" not in unitList:
        raise RuntimeError('Yukari unit (or "Y" directive) need to be set in the unit list.')

    # Create simulation object.
    simulObj = Simulation()

    # If no variable directive inputted, then simply run one stability check simulation.
    if variableValues == None:

        if "V" in unitList:
            raise RuntimeError('Values must be inputted if the directive "V" is used in the provided unit list.')

        return checkStability_recursive(simulObj,unitList,TPBoostList,0)

    else: # otherwise, run simulation for each variable values.

        if "V" not in unitList:
            raise RuntimeError('Directive "V" must be set in the unit list if variable values are provided.')

        # Change the directive "V" by the dummit unit defined in CONSTANT.py
        unitVarPosition = 0
        for u in unitList:
            if u == "V":
                unitList[unitVarPosition]= CST.VARIABLE_UNIT_NAME
                break
            unitVarPosition += 1

        isStable_list = []
        for v in variableValues:
            unitsRange[CST.VARIABLE_UNIT_NAME] = v
            isStable_list.append(checkStability_recursive(simulObj,unitList,TPBoostList,0))

        # Print results if verbose constant is enabled.
        if CST.STABILITY_ANALYSIS_VERBOSE:

            for idx in range(len(variableValues)):
                if isStable_list[idx]:
                    print("P" + str(unitVarPosition+1) + " AR = " + str(variableValues[idx]) + " is stable.")
                else:
                    print("P" + str(unitVarPosition+1) + " AR = " + str(variableValues[idx]) + " is not stable.")

        return isStable_list

def checkStability_recursive(simulObj,unitList,TPBoostList,startIndex):

    numberUnits = len(unitList)
    positionIndex = None
    for idx in range(startIndex,numberUnits):
        if len(unitList[idx]) == 1:
            positionIndex = idx
            break

    # If no unit directive found, just return
    # the stability check result on the opposite team positions.
    if positionIndex  == None:
        simulObj.setAttackerTeam(unitList,TPBoostList)
        return checkStability_oppositeTeam(simulObj)

    unitDirective = unitList[positionIndex]

    # Default values if "X" or anything else.
    lowestAttackRange = CST.FRONT_ATTACK_RANGE[0]
    highestAttackRange = CST.BACK_ATTACK_RANGE[1]

    if unitDirective == "F":
        lowestAttackRange = CST.FRONT_ATTACK_RANGE[0]
        highestAttackRange = CST.FRONT_ATTACK_RANGE[1]


    if unitDirective == "M":
        lowestAttackRange = CST.MIDDLE_ATTACK_RANGE[0]
        highestAttackRange = CST.MIDDLE_ATTACK_RANGE[1]

    if unitDirective == "B":
        lowestAttackRange = CST.BACK_ATTACK_RANGE[0]
        highestAttackRange = CST.BACK_ATTACK_RANGE[1]

    # Check if the unit just before has higher ranges than the lowest one considered before.
    if positionIndex > 0:
        attackRange_toCompare = unitsRange[unitList[positionIndex-1]]
        if attackRange_toCompare > lowestAttackRange:
            lowestAttackRange = attackRange_toCompare

    # Check if the unit just before has higher ranges than the lowest one considered before.
    attackRange_toCompare =  CST.BACK_ATTACK_RANGE[1]
    if positionIndex < numberUnits-1:
        idx = positionIndex+1
        if len(unitList[idx]) == 1:

            if unitList[idx] == "F":
                attackRange_toCompare = CST.FRONT_ATTACK_RANGE[1]

            if unitList[idx] == "M":
                attackRange_toCompare = CST.MIDDLE_ATTACK_RANGE[1]

            if unitList[idx] == "B":
                attackRange_toCompare = CST.BACK_ATTACK_RANGE[1]
        else:
            attackRange_toCompare = unitsRange[unitList[idx]]

    if highestAttackRange > attackRange_toCompare:
        highestAttackRange = attackRange_toCompare

    unitListToCheck = [item for item in unitsRange.keys() if (lowestAttackRange < unitsRange[item]) &
                                                           (unitsRange[item] < highestAttackRange)]


    # Check stability.
    isStable = True
    for u in unitListToCheck:

        newUnitList = unitList.copy()
        newUnitList[positionIndex] = u
        isStable = checkStability_recursive(simulObj,newUnitList,TPBoostList,positionIndex+1)
        if not isStable:
            break

    return isStable


# Check stability with respect to the opposite team.
def checkStability_oppositeTeam(simulObj):

        allUnit_dict = unitsRange.copy()
        del allUnit_dict['Lima']
        for id in range(5):
            del allUnit_dict['Dummy' + str(id+1)]

        simulObj.setDefenderTeam(["Miyako"])
        simulObj.execute()
        refName = simulObj.getHighestTPUnit(Side.ATTACKER).name
        isStable = True
        for k in allUnit_dict.keys():

            # Simulate with one unit (no lima).
            simulObj.setDefenderTeam([k])
            simulObj.execute()
            name = simulObj.getHighestTPUnit(Side.ATTACKER).name
            if name != refName:
                isStable = False
                break

            # Simulate again with Lima + a second unit (no lima).
            simulObj.setDefenderTeam(['Lima', k])
            simulObj.execute()
            name = simulObj.getHighestTPUnit(Side.ATTACKER).name
            if name != refName:
                isStable = False
                break

        return isStable
