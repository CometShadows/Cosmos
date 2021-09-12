import Functions
import modules 
import random
import math
import Battle
from replit import db
import asyncio
import discord
import datetime as dt
import datetime

async def randomevent(data, ctx,bot):
  asteroidchance=round((Functions.StatsCal(data, 'AsteroidChance')+100)/modules.zoneevents[Functions.Zone(data['Var']['pos'])][0])
  rougechance=round(Functions.StatsCal(data, 'RougeChance')*2+500/modules.zoneevents[Functions.Zone(data['Var']['pos'])][1])
  treasurechance=round(300/(modules.zoneevents[Functions.Zone(data['Var']['pos'])][0]*math.sqrt(Functions.StatsCal(data, 'Rare'))))
  keys_list=list(modules.zonevalue)
  zone=keys_list.index(Functions.Zone(data['Var']['pos']))
  if random.randint(0,asteroidchance)==1:
    damage=asteroid(data, zone)
    value=1
    return [value, damage]
  elif random.randint(0, rougechance)==0:
    result=await Battle.rouge(ctx, data, zone, bot)
    damage=result[1]
    value=2
    if result[0]==True:
      treasures=treasure(data, zone)
      return [value,damage,treasures]
    else:
      return [value, damage]
  elif random.randint(0,treasurechance)==0:
    treasures=treasure(data, zone)
    value=3
    return [value, treasures]
  elif random.randint(0,rougechance*2)==0:
    await trader(ctx,bot)
    value=4
    return [value]
  else:
    value=0
    return [value]
def asteroid(data, zone):
  x=random.randint(1,2+zone)
  damage={}
  evade=1-Functions.StatsCal(data, 'Evade')*10000
  for i in range (0,x):
    if random.randint(0,10000)<evade:
      pass
    else:
      keys_list= list(data['Modules'])
      module=random.randint(0,len(keys_list)-1)
      damage[keys_list[module]]=random.randint(zone,round(zone**1.5+10))*Functions.StatsCal(data,'DamageReduced')
  return damage

def treasure(data,zone_index):
  keys_list=list(modules.zonevalue)
  loot=random.randint((1+zone_index)*2,(3+zone_index*5)*2)
  lootfound={}
  for x in range (0,loot):
    rarity=Functions.Collect(Functions.StatsCal(data, 'Rare'))
    zone=Functions.Zone(data['Var']['pos'])
    items=random.randint(0,len(modules.zone[zone][rarity])-1)
    item=modules.zone[zone][rarity][items]
    if item in lootfound:
      lootfound[item]+=1
    else:
      lootfound[item]=1
  return lootfound
async def trader(ctx,bot):
  
  tradesCount=random.randint(3,5)
  trades=[]
  v=eval(db[str(ctx.message.author.id)])
  zone=Functions.Zone(v['Var']['pos'])

  tradelist=modules.trades[zone]
  for x in range (0,tradesCount):
    items=random.sample(tradelist[0],2)
    
    random.shuffle(items)
    while trades.count(items)==1:
      items=random.sample(tradelist[0],2)
      random.shuffle(items)
    trades.append(items)
  convert=[]

  for x in range (0,tradesCount):
    item1=tradelist[0].index(trades[x][0])
    item2=tradelist[0].index(trades[x][1])

    if item1>item2:
      cost=1
      for y in range(item2,item1):
        cost=cost*random.randint(1,tradelist[1][y])
        
      multiply=random.randint(1,tradelist[2])
      listtrade={}
      listtrade[trades[x][0]]=1*multiply
      listtrade[trades[x][1]]=cost*multiply
      convert.append(listtrade)
    else:
      cost=1
      for y in range(item1,item2):
        cost=cost*random.randint(1,tradelist[1][y])
        
      multiply=random.randint(1,tradelist[2])
      listtrade={}
      
      listtrade[trades[x][0]]=cost*multiply
      listtrade[trades[x][1]]=1*multiply
      convert.append(listtrade)
  await ctx.send('You found a trader starship.')
  embed=discord.Embed(
  title=ctx.message.author.name+'\'s Trade', description="Choose a trade using its `id` or `cancel` to cancel. You can only choose one.", color=discord.Color.blue())
  send=''
  for x in range (0,tradesCount):
    itemlist=list(convert[x])
    send=send+'`id '+str(x)+'` **'+str(convert[x][itemlist[0]])+' '+itemlist[0]+'** for **'+str(convert[x][itemlist[1]])+' '+str(itemlist[1])+'**\n'
  send=send+'Or type `cancel` to cancel'
    
  embed.add_field(name='**Possible trades**:',value=send, inline=False)
  await ctx.send(embed=embed)
  while True:
    try:
      msg = await bot.wait_for("message", timeout=30.0,check=lambda message: message.author == ctx.author)
    except asyncio.TimeoutError:
      await ctx.send('You didn\'t answer anything. The trader was tired of waiting and left')
      Break=True
    else:
      msg=msg.content
      Break=False
      if msg=='cancel':
        Break=True
        await ctx.send('You told the trader you don\'t want anything.' )
      else:
        try:
          selected=convert[int(msg)]

          selectedlist=list(selected)
          item0=selectedlist[0]

          item1=selectedlist[1]

          if item0 in v['Inv']:
            if v['Inv'][item0]>=selected[item0]:
              v['Inv'][item0]-= selected[item0]
              if random.randint(1,100)==1:
                await ctx.send('You got scammed! The trader took ur stuff and fled')
              else:
                await ctx.send('You successfully traded with the trader and he left')
                if item1 in v['Inv']:
                  v['Inv'][item1]+=selected[item1]
                else:
                  v['Inv'][item1]=selected[item1]
              Break=True
            else:
              await ctx.send('Not enough materials')
          else:
            await ctx.send('Not enough materials')
        except:
          await ctx.send('That is not a trade')
    if Break:
      break
  db[str(ctx.message.author.id)]=str(v)
