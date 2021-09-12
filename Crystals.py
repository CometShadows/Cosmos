import random
import Functions
import modules as md
import discord
import asyncio
import datetime as dt
import datetime
from replit import db

def NewCrystal(rarity):
  enchant={}
  if rarity=='starter':
    crystallist=list(md.crystals)
    c=random.randint(0,len(crystallist)-1)
    while md.crystals[crystallist[c]][0]=='Special':
      c=random.randint(0,len(crystallist)-1)
    enchant[crystallist[c]]=1
  return enchant
def SearchEnchant(equipped,crystals,enchant):
  enchants={}
  count=0
  for x in equipped.values():
    if x!='none':
      if enchant in crystals[x]['Enchantments']:
        enchants[list(equipped)[count]]=crystals[x]['Enchantments'][enchant]
  return enchants
