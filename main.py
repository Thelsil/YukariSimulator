from src.Analysis import analyseStability
from src.Simulation import Simulation, Side

print('Notations (1) - Positions: 12345, Y: Yukari, F: Front, M: Middle, B: Back, X: Any.')
print('Notations (2) - P(1 -5): Position (from  1 to 5), AR: Attack Range, TPB: TP Boost')
print('Format: (case index) - (positions) = (position TP boosted) / (conditions) \n')

simulObj = Simulation()

# The full team defender team doesnt matter if the case is stable.
defenderTeam = ['Miyako']
simulObj.setDefenderTeam(defenderTeam)

#####################################
#       YUKARI POSITION 1 CASES     #
#####################################

#-----------------------------------------------------------
print('CASE 1A - YXXXX = P4')

# Execute the simulation.
simulObj.setAttackerTeam(['Yukari','Monika','Ninon','Illya','Saren'])
simulObj.execute()

TPBoostedUnit = simulObj.getHighestTPUnit(Side.ATTACKER)
assert TPBoostedUnit.name == "Illya"


#####################################
#       YUKARI POSITION 2 CASES     #
#####################################

#-----------------------------------------------------------
print('CASE 2A - XYMBB = P4 / P4 AR < 809')

simulObj.setAttackerTeam(['Miyako','Yukari','Monika','Suzuna','Kyoka'])
simulObj.execute()
TPBoostedUnit = simulObj.getHighestTPUnit(Side.ATTACKER)

assert TPBoostedUnit.name == 'Suzuna'

#-----------------------------------------------------------
print('CASE 2B - XYBBB = P5 / P1 TPB < P3 TPB or P1* AR < 189')

# When P1* AR < 189
simulObj.setAttackerTeam(['Nozomi','Yukari','Suzuna','Shiori','Kyoka'])
simulObj.execute()
TPBoostedUnit = simulObj.getHighestTPUnit(Side.ATTACKER)

assert TPBoostedUnit.name == 'Kyoka'

# When Pos 1 TP < Pos 3 TP
simulObj.setAttackerTeam(['Shizuru','Yukari','Suzuna','Shiori','Kyoka'],[0,0,10,0,0])
simulObj.execute()
TPBoostedUnit = simulObj.getHighestTPUnit(Side.ATTACKER)

assert TPBoostedUnit.name == 'Kyoka'

#-----------------------------------------------------------
print('CASE 2C - XYBBB = P4 / P1 TPB ≥ P3 TPB & P1 AR > 200 & P4 AR < 809')

simulObj.setAttackerTeam(['Shizuru','Yukari','Suzuna','Shiori','Yuki'],[10,0,0,0,0])
simulObj.execute()
TPBoostedUnit = simulObj.getHighestTPUnit(Side.ATTACKER)

assert TPBoostedUnit.name == 'Shiori'


#####################################
#       YUKARI POSITION 3 CASES     #
#####################################

#-----------------------------------------------------------
print('CASE 3A - XXYMX = P4 / P5 AR < 809')

simulObj.setAttackerTeam(['Miyako','Kuka','Yukari','Illya','Mitsuki'])
simulObj.execute()
TPBoostedUnit = simulObj.getHighestTPUnit(Side.ATTACKER)

assert TPBoostedUnit.name == 'Illya'

#-----------------------------------------------------------
print('CASE 3B - XXYBB = P3 / P4 AR > 628')

simulObj.setAttackerTeam(['Miyako','Shizuru','Yukari','Maho','Kyoka'])
simulObj.execute()
TPBoostedUnit = simulObj.getHighestTPUnit(Side.ATTACKER)

assert TPBoostedUnit.name == 'Yukari'

#####################################
#       YUKARI POSITION 4 CASES     #
#####################################

#-----------------------------------------------------------
print('CASE 4A - XXXYM = P4 / P3 TPB ≤ P1 TPB & P3 TPB ≤ P2 TPB or P4 AR < 201.')

simulObj.setAttackerTeam(['Miyako','Kuka','Shizuru','Yukari','Illya'])
simulObj.execute()
TPBoostedUnit = simulObj.getHighestTPUnit(Side.ATTACKER)

assert TPBoostedUnit.name == 'Yukari'

simulObj.setAttackerTeam(['Miyako','Kuka','Jun','Yukari','Illya'],[0,0,10,0,0])
simulObj.execute()
TPBoostedUnit = simulObj.getHighestTPUnit(Side.ATTACKER)

assert TPBoostedUnit.name == 'Yukari'

#-----------------------------------------------------------
print('CASE 4B - XXXYM = P5 / P3 TPB > P1 TPB & P3 TPB > P2 TPB & P4 AR > 204.')

simulObj.setAttackerTeam(['Miyako','Kuka','Shizuru','Yukari','Illya'],[0,0,10,0,0])
simulObj.execute()
TPBoostedUnit = simulObj.getHighestTPUnit(Side.ATTACKER)

assert TPBoostedUnit.name == 'Illya'

#-----------------------------------------------------------
print('CASE 4C - FFFYB = P3 / P3 AR < 201')

simulObj.setAttackerTeam(['Miyako','Kuka','Tsumugi','Yukari','Maho'])
simulObj.execute()
TPBoostedUnit = simulObj.getHighestTPUnit(Side.ATTACKER)

assert TPBoostedUnit.name == 'Tsumugi'

#-----------------------------------------------------------
print('CASE 4D - XXXYB = P4 / P3 AR > 204')

simulObj.setAttackerTeam(['Miyako','Kuka','Shizuru','Yukari','Maho'])
simulObj.execute()
TPBoostedUnit = simulObj.getHighestTPUnit(Side.ATTACKER)

assert TPBoostedUnit.name == 'Yukari'

#####################################
#       YUKARI POSITION 5 CASES     #
#####################################

#-----------------------------------------------------------
print('CASE 5A - FFFFY = P4 / P4 AR < 197 & P3 TPB ≤ P1 TPB & P3 TPB ≤ P2 TPB')

simulObj.setAttackerTeam(['Jun','Nozomi','Matsuri','Tsumugi','Yukari'],[10,10,0,0,0])
simulObj.execute()
TPBoostedUnit = simulObj.getHighestTPUnit(Side.ATTACKER)

assert TPBoostedUnit.name == 'Tsumugi'

#-----------------------------------------------------------
print('CASE 5B - XXXXY = P5 / P4 AR > 200 or P3 TPB > P1 TPB & P3 TPB > P2 TPB')

simulObj.setAttackerTeam(['Jun','Nozomi','Matsuri','Shizuru','Yukari'],[10,10,0,0,0])
simulObj.execute()
TPBoostedUnit = simulObj.getHighestTPUnit(Side.ATTACKER)

assert TPBoostedUnit.name == 'Yukari'

simulObj.setAttackerTeam(['Jun','Nozomi','Matsuri','Tsumugi','Yukari'],[0,0,10,0,0])
simulObj.execute()
TPBoostedUnit = simulObj.getHighestTPUnit(Side.ATTACKER)

assert TPBoostedUnit.name == 'Yukari'

print('* Not fully stable if Lima (but very, very edge cases).')