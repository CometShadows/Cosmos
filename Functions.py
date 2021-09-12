import modules
import random
import datetime as dt
import math
import discord


#calculates true stats by multiplying base stats with startship boost
def StatsCal(data, value):
  stats=0
  if modules.stats[value]:
    stats=1
  keys_list = list(data['Modules'])
  if value=='CollectEnergy':
    stats=0
    for x in keys_list:
      if value in modules.modules[x]:
        stats=stats=stats+(modules.modules[x][value])*data['Modules'][x][1]
    for x in keys_list:
      if 'CollectEnergyReduce' in modules.modules[x]:
        stats=stats=stats*((1-(1-modules.modules[x]['CollectEnergyReduce'])*(data['Modules'][x][0]/100))**data['Modules'][x][1])
  else:
    for x in keys_list:
      if value in modules.modules[x]:
        if modules.stats[value]:
          if modules.modules[x][value]<1:
            stats=stats*((1-(1-modules.modules[x][value])*(data['Modules'][x][0]/100))**data['Modules'][x][1])
          else:
            stats=stats*(((modules.modules[x][value]-1)*(data['Modules'][x][0]/100)+1)**data['Modules'][x][1])
        else:
          stats=stats+(modules.modules[x][value]*data['Modules'][x][0]/100)*data['Modules'][x][1]
  if value in modules.starships[data['Starship']]:
    return round(stats*(modules.starships[data['Starship']][value]**data['StarshipLvl']),2)
  else:
    return round(stats,2)

#Pass in the stat 'Rare' to give a random rarity
def Collect(chance):
  common=5000+round(810*chance)
  uncommon=1000+round(270*chance)
  rare=250+round(90*chance)
  epic=50+round(30*chance)
  legendary=10+round(10*chance)
  mythic=1+round(2*chance)
  Sum=common+uncommon+rare+epic+legendary+mythic
  item=random.randint(1,Sum)
  if item<common:
    return 'common'
  elif item<common+uncommon:
    return 'uncommon'
  elif item<common+uncommon+rare:
    return 'rare'
  elif item<common+uncommon+rare+epic:
    return 'epic'
  elif item<common+uncommon+rare+epic+legendary:
    return 'legendary'
  else:
    return 'mythical'

#Input coords return the zone
def Zone(coords):
  r=coords[0]**2+coords[1]**2+coords[2]**2
  r=math.sqrt(r)
  keys_list = list(modules.zonevalue)
  values = modules.zonevalue.values()
  values_list = list(values)
  x=0
  while r>values_list[x]:
    x=x+1
  return keys_list[x]

#Input player data output the regened energy
def EnergySet(data):
  seconds=dt.datetime.utcnow()-data['Var']['time']
  regened=seconds.total_seconds()*StatsCal(data, 'EnergyRegen')
  energy=data['Var']['energy']+regened
  if energy>StatsCal(data, 'MaxEnergy'):
    energy=StatsCal(data, 'MaxEnergy')
  return round(energy,2)

def cap(word):
  words=word.split(' ')
  ans=''
  for x in words:
    if x !='and':
      ans=ans + x.capitalize() +' '
    else:
      ans=ans+x.lower()+' '
  ans=ans.strip()
  return ans