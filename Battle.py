#Ill put the battling stuff here
import random
import Functions
import modules
import discord
import asyncio
import datetime as dt
import datetime
from replit import db

#The play attack sequence function (for simple battles)
async def attacksq(ctx,data,weapons,health,energy,maxenergy,bot):
  flee=False
  moves={}
  #Sending player the choices
  embed=discord.Embed(
  title=ctx.message.author.name+'\'s Attack', description="It is your turn to attack. Choose an move", color=discord.Color.blue())
  #List of weapons
  weapons_list=list(weapons)
  #Each weapon has [Cooldown, Damage, Energy use]
  for x in range (0,len(weapons_list)):
    moves[str(x)]=['Ready',round(modules.modules[weapons_list[x]]['Damage']*data['Modules'][weapons_list[x]][1]*data['Modules'][weapons_list[x]][0]/100,2),round(modules.modules[weapons_list[x]]['EnergyUse']*data['Modules'][weapons_list[x]][1]*Functions.StatsCal(data,'AttackReduce'))]
    #Apply Destroyer boost
    if data['Starship']=='Destroyer':
      moves[str(x)][1]=moves[str(x)][1]*(1.1**data['StarshipLvl'])
    #The information sent to player
    send='*Damage*: '+str(moves[str(x)][1])+'\n*Energy Use*: '+str(moves[str(x)][2])+'\n'
    if 'CritChance' in modules.modules[weapons_list[x]]:
      send=send+'*Critical Chance*: '+str(modules.modules[weapons_list[x]]['CritChance']*100)+'%\n'
      moves[str(x)].append(modules.modules[weapons_list[x]]['CritChance']*100)
    if weapons[weapons_list[x]]==0:
      send=send+'*Cooldown*: Ready'
    else:
      moves[str(x)][0]='Not'
      send=send+'*Cooldown*: '+str(weapons[weapons_list[x]])
    embed.add_field(name='`id '+str(x)+'`: '+weapons_list[x],value=send, inline=False)
  embed.add_field(name='`id '+str(len(weapons_list))+'`: Pass',value='Do nothing', inline=False)
  moves[str(len(weapons_list))]=['Pass']
  moves[str(len(weapons_list)+1)]=['Flee']
  embed.add_field(name='`id '+str(len(weapons_list)+1)+'`: Flee',value='Flee from battle', inline=False)
  embed.add_field(name='**Energy**:',value=str(round(energy,2))+'/'+str(maxenergy), inline=False)
  await ctx.send(embed=embed)
  while True:
    try:
      msg = await bot.wait_for("message", timeout=30.0,check=lambda message: message.author == ctx.author)
    except asyncio.TimeoutError:
      await ctx.send('Your starship fled because you didn\'t choose anything')
      Break=True
      flee=True
    else:
      msg=msg.content
      Break=False
      if msg in moves:
        if moves[msg][0]=='Not':
          await ctx.send('That weapon is cooling down. You don\'t want that to explode don\'t you')
        elif moves[msg][0]=='Pass':
          await ctx.send('You passed your turn')
          Break=True
        elif moves[msg][0]=='Flee':
          if random.randint(0,2)==1:
            await ctx.send('You tried to flee but was chased down')
          else:
            await ctx.send('You have succesfully fled the battle')
            flee=True
          Break=True
        elif moves[msg][2]>energy:
          await ctx.send('Not enough energy')
        else:
          if random.randint(0,100)==1:
            await ctx.send('The enemy evaded your attack')
          else:
            if len(moves[msg])==4:
              if random.randint(1,100)<=moves[msg][3]:
                health=health-moves[msg][1]*random.randint(125,200)/100
                await ctx.send('Critical attack')
              else:
                health=health-moves[msg][1]
                await ctx.send('Attack is successful')
            else:
              health=health-moves[msg][1]
              await ctx.send('Attack is successful')
          energy=energy-moves[msg][2]
          weapons[weapons_list[int(msg)]]=modules.modules[weapons_list[int(msg)]]['Cooldown']+1
          Break=True
    if Break==True and flee==False:
      regened=round(Functions.StatsCal(data,'EnergyRegen')*random.randint(7,13),2)
      if energy+regened>maxenergy:
        regened=maxenergy-energy
        energy=maxenergy
      else:
        energy=energy+regened
      await ctx.send('You have regenerated '+str(regened)+' energy')
      if energy==maxenergy:
        await ctx.send('Your energy is maxed')
      for x in weapons:
        weapons[x]-=1
        if weapons[x]<0:
          weapons[x]=0
    if Break==True:
      break
  return [energy,weapons,health,flee]
async def rouge(ctx, data, zone, bot, start=False, energyused=0):
  v=eval(db[str(ctx.message.author.id)])
  v['Var']['energy']=Functions.EnergySet(v)
  v['Var']['time']=dt.datetime.utcnow()
  health=random.randint((1+zone)*2, (1+zone*2)*5)
  damage={}
  evade=1-Functions.StatsCal(data, 'Evade')*10000
  keys_list= list(data['Modules'])
  win=False
  weapons={}
  for x in keys_list:
    if 'Damage' in modules.modules[x]:
      weapons[x]=0
  maxenergy=Functions.StatsCal(v, 'MaxEnergy')
  energy=v['Var']['energy']
  flee=False
  if start==True:
    await ctx.send('You found a starship after using '+str(energyused)+' energy')
    energy=energy-energyused
    attackinfo=await attacksq(ctx,data,weapons,health,energy,maxenergy,bot)
    energy=attackinfo[0]
    weapons=attackinfo[1]
    health=attackinfo[2]
    flee=attackinfo[3]

  else:
    await ctx.send('You were suddenly attacked by a rouge starship. Prepare for combat')
  while True:
    if health<=0:
      win=True
      break
    if flee==True:
      break
    if random.randint(0,10000)<evade:
      pass
      await ctx.send('You evaded the attack')
    else:
      keys_list= list(data['Modules'])
      module=random.randint(0,len(keys_list)-1)

      attack=round(random.randint(zone,round(zone**1.5+10))* Functions.StatsCal(data,'DamageReduced'),2)
      damage[keys_list[module]]=attack
      data['Modules'][keys_list[module]][0]-=attack
      await ctx.send('Your '+keys_list[module]+' was damaged by '+str(attack)+'%')
    if data['Modules'][keys_list[module]][0]<25:
      Id=str(ctx.message.author.id)
      v=eval(db[Id])
      v['Modules'][keys_list[module]][0]=25
      db[Id]=str[v]
      await ctx.send('Your '+keys_list[module]+'\'s health has dropped to dangerous levels. You were forced to flee.')
      break
    attackinfo=await attacksq(ctx,data,weapons,health,energy,maxenergy,bot)
    energy=attackinfo[0]
    weapons=attackinfo[1]
    health=attackinfo[2]
    flee=attackinfo[3]
  v=eval(db[str(ctx.message.author.id)])
  v['Var']['energy']=energy
  db[str(ctx.message.author.id)]=str(v)
  return [win,damage]
