import discord
import os
import datetime as dt
import datetime
import asyncio
from replit import db

import Functions
import modules as md
import randomevent as re
import random
import math
import Battle
import market
import Crystals as c

from discord.ext import commands, tasks
from dotenv import load_dotenv
from itertools import cycle
from flask import Flask
from threading import Thread

#Just connecting to server
app = Flask('')


@app.route('/')
def main():
    return "Your Bot Is Ready"


def run():
    app.run(host="0.0.0.0", port=8000)


def keep_alive():
    server = Thread(target=run)
    server.start()


load_dotenv()
bot = commands.Bot(command_prefix='cs ')
bot.remove_command('help')
client=discord.Client()
status = cycle(['Cosmos', 'cs help', 'cs start', 'cs guide'])


@bot.event
async def on_ready():
    change_status.start()
    print("Your bot is ready")


@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))

#Main stuff starts here
starships = [
    'Comet', 'Aurora', 'Nightmare', 'Starlight', 'Destroyer', 'Defender',
    'Brilliance'
]

#A list of all the premade blueprints
moduleIndex = list(md.modules)



#Random events called before travelling, collecting, searching
async def events(Id, ctx, bot):
  #Getting player data from database
  v = eval(db[Id])
  #Determines if a random event occurs and returns result (including battle)
  result = await re.randomevent(v, ctx, bot)
  #Determines if the original action will be skipped because of the event
  event = True
  #Radiation damage in Radiance zone
  if Functions.Zone(v['Var']['pos'])=='Radiance':
    if random.randint(0,1)==0:
      mod=random.sample(list(v['Modules']),1)
      v['Modules'][mod[0]][0]-=random.randint(75,125)/100
  #Returns 0 if no events
  if result[0] == 0:
      event = False
      
  #Returns 1 in the 0th index if asteroid
  elif result[0] == 1:
    #Gets data again because it is changed in randomevent function
    v = eval(db[Id])
    #Index 1 gives what modules and by what percent they are damaged
    if result[1] == {}:
      await ctx.send(
            'You were in an asteroid rain but you evaded all the asteroids. Impressive.'
        )
    else:
      rewind=False
      activated=[]
      try:
        equipped=c.SearchEnchant(v['Equip'], v['Crystals'], 'Rewind')
        if 'Core' in equipped:
          probability=int(math.log(100,equipped['Core']+1)*200)
          if random.randint(0,probability)<100:
            result[1]={}
            rewind=True
        else:
          for x in equipped:
            probability=int(math.log(100,equipped[x]+1)*200)
            if random.randint(0,probability)<100:
              rewind=True
              activated.append(x)
      except:
        pass
      keys_list = list(result[1])
      for x in keys_list:
        if md.modules[x]['Class'] in activated:
          pass
        else:
          v['Modules'][x][0] -= result[1][x]
          if v['Modules'][x][0] < 25:
            v['Modules'][x][0] = 25
      if rewind:
        await ctx.send('You got hit by some asteroid buy your rewind crystal was activated')
      else:
        await ctx.send(
          'You got hit by some asteroids. Better check the damage.')
  #Rouge spaceship
  elif result[0] == 2:
    v = eval(db[Id])
    #If battle is won rewards will be returned (length will be 3)
    if len(result) == 2:
      #No modules damaged
      if result[1] == {}:
        pass
      else:
        #Damaging the modules
        keys_list = list(result[1])
        for x in keys_list:
          v['Modules'][x][0] -= result[1][x]
          if v['Modules'][x][0] < 25:
            v['Modules'][x][0] = 25
    else:
      if result[1] == {}:
        pass
      else:
        for x in keys_list:
          v['Modules'][x][0] -= result[1][x]
          if v['Modules'][x][0] < 25:
            v['Modules'][x][0] = 25
      #Printing out the materials won
      materials = '**Items salvaged**: \n'
      keys_list = list(result[2])
      for x in keys_list:
        multiply=random.randint(2,5)
        if x in v['Inv']:
          v['Inv'][x] += result[2][x]*multiply
        else:
          v['Inv'][x] = result[2][x]*multiply
        materials = materials + '**' + x + '**: ' + str(result[2][x]*multiply) + '\n'
      embed = discord.Embed(title=ctx.message.author.name + " has won the battle", description = materials, color = discord.Color.blue())
      await ctx.send(embed=embed)
  #Get free loot
  elif result[0] == 3:
    v = eval(db[Id])
    await ctx.send('You found an abandon starship and dismantled it')
    materials = ''
    keys_list = list(result[1])
    for x in keys_list:
      if x in v['Inv']:
        v['Inv'][x] += result[1][x]
      else:
        v['Inv'][x] = 1
      materials = materials + '**' + x + '**: ' + str(result[1][x]) + '\n'
    embed = discord.Embed(title="Items obtained",
                          description=materials,
                          color=discord.Color.blue())
    await ctx.send(embed=embed)
  #Find a trader (all the stuff is done in the trader function)
  elif result[0] == 4:
    v = eval(db[Id])
  #Saving the changed data
  db[Id] = str(v)
  return event
#Admin commands
@bot.command(name='admin')
async def Admin(ctx, action, password):
  Id = str(ctx.message.author.id)
  v = eval(db[Id])
  #Really don't use this or ill be very pissed
  if action=='reset':
    if password=='Cosmological':
      for x in db.keys():
        if x != 'Market':
          del db[x]
      await ctx.send('Reset finish')
  if action=='supply':
    if password=='Infinity':
      
      for x in md.material_list:
        v['Inv'][x]=1000
      db[Id]=str(v)
      await ctx.send('Supply sent')
  if action=='data':
    if password=='View':
      embed = discord.Embed(title="Viewing data",description="",color=discord.Color.blue())
      embed.add_field(name="id "+str(Id),value=db[Id],inline=False)
      print(v)



#The market command (obviously)
#Optional argument 'select' is for deleting or selecting a trade (pass in the trade id)
@bot.command(name='market', aliases=['m'])
async def Market(ctx, Action='blank', select='-1'):
  #Just saving the id into a variable
  Id = str(ctx.message.author.id)
  v = eval(db[Id])
  #m={'give':{},'get':{},'id':0}
  #db['Market']=str(m)

  #No space net 
  if 'SpaceNet' not in v['Modules']:
    await ctx.send('You are not linked to SpaceNet')
  #No space net connection outside first 3 zones
  elif not (Functions.Zone(v['Var']['pos']) == 'Alpha' or Functions.Zone(v['Var']['pos']) == 'Beta' or Functions.Zone(v['Var']['pos']) == 'Wasteland'):
    await ctx.send('Your SpaceNet was unable to connect')
  #No action
  elif Action == 'blank':
    await ctx.send(
          '**You didn\'s choose an action\nAction:** \n- `add` to add a trade\n- `search` to search for trades\n- `listed` to see your listed trades\n- `delete [id]` to delete a listed trade\n- `select[id]` to select a trade\n- `inbox` to view and get you profit'
      )
  #Rest is pretty obvious
  elif Action == 'search':
    await market.search(ctx, bot)
  elif Action == 'add':
    await market.add(ctx, bot)
  elif Action == 'listed':
    await market.listing(ctx, bot)
  elif Action == 'delete':
    await market.delete(ctx, bot, select)
  elif Action == 'select':
    await market.select(ctx, bot, select)
  elif Action == 'inbox':
    await market.inbox(ctx)
  else:
    await ctx.send(
          '**You didn\'s choose an action\nAction:** \n- `add` to add a trade\n- `search` to search for trades\n- `listed` to see your listed trades\n- `delete [id]` to delete a listed trade\n- `select[id]` to select a trade\n- `inbox` to view and get you profit'
      )

#Just the guide message
@bot.command(name='guide', aliases=['g'])
async def help(ctx):
  Id = str(ctx.message.author.id)
  v=eval(db[Id])
  embed = discord.Embed(
      title="Guide to the Cosmos",
      description=
      "Get materials, improve your starship, discover secrets, and fight bosses!\nTo start use `cs start`",
      color=discord.Color.blue())
  embed.add_field(
      name="**Crafting and Upgrades**",
      value=
      "`cs collect`: Get materials with your collector (Uses energy). Some materials are only found in specific zones\n`cs inventory`: View your materials\n`cs craft [item]`: Craft modules or items to improve your starship stats \n`cs upgrade`: Upgrade your starship for higher starship boost and more module slots \n`cs dismantle [item]`: Dismantle modules you don't want and get back some materials\n`cs repair [item]`: Repair your damaged modules so it can run at max efficiency\n`cs recipes`: View your unlocked recipes. You can unlock recipes through leveling up your starship or finding special blueprints\n`cs info [item]` View the materials needed to craft the item, its stats, and its special abilities",
      inline=False)
  embed.add_field(
      name="**Stats for Nerds**",
      value=
      "`cs starship`: The basic information of your starship\n`cs stats`: View your stats\n`cs modules`: View your modules and check if they are at max efficiency\n`cs energy`: View your energy stats",
      inline=False)
  embed.add_field(
      name="**Travel and Exploration**",
      value=
      "`cs explore [distance/% energy used]`: Travel in a random direction away from your current zone for a chance to discover a new zone (type % behind a value to use % amount of energy)\n`cs travel [zone]`: Travel to a discovered zone (Uses energy)\n`cs zones`: View all your discovered zones",
      inline=False)
  if 'Laser Detector' in v['Modules']:
    embed.add_field(
      name="**Combat**",
      value=
      "Use your weapons to fight rouge starships and get some loot.\n`cs search`: Search for other starships for a chance for loot (Requires *Laser Detector* and uses energy)",
      inline=False)
  embed.add_field(
      name="**Random Events**",
      value=
      "The cosmos is unpredictable. Watch out for random events (Chances are based on secret stats)",
      inline=False)
  if 'SpaceNet' in v['Modules']:
    embed.add_field(
      name="**Market**",
      value=
      "`cs market`:You can offer and accept trades with real players",
      inline=False)
  if 'StarForge' in v['Modules']:
    embed.add_field(
      name="**Star Crystals**",
      value=
      "Star crystals can provide powerful boosts to your stats when equipped. Fuse your crystals to create crystals of immense powers. Search for crystals or grow them to find new powers.",
      inline=False)
  embed.add_field(
      name="**Free stuff**",
      value=
      "`cs crates`: Get a free crate every hour. You can also choose the type and level up the crate to get more and better materials.",
      inline=False)
  embed.add_field(
      name="**Others**",
      value=
      "Some commands will only be unlocked after crafting a specific module. Those commands will be updated into the guide after you unlock them",
      inline=False)

  await ctx.send(embed=embed)


#Registers your ID into the database
@bot.command(name='start')
async def pick(ctx, starship='none'):
    Id = str(ctx.message.author.id)
    #When your ID is already in the database
    if Id in db.keys():
      await ctx.send('You have already chosen a starship')
    elif starship=='none':
      embed = discord.Embed(
      title="Welcome to the Cosmos",
      description=
      "Choose a starship to get started by using the `cs start [starship]` command",
      color=discord.Color.blue())
      embed.add_field(name="**Comet**",
                      value="Uses less energy when traveling or exploring",
                      inline=False)
      embed.add_field(name="**Aurora**",
                      value="Faster energy regeneration",
                      inline=False)
      embed.add_field(name="**Nightmare**",
                      value="Higher chance of evading attack",
                      inline=False)
      embed.add_field(name="**Starlight**",
                      value="Bonus energy storage",
                      inline=False)
      embed.add_field(name="**Destroyer**",
                      value="More attack damage",
                      inline=False)
      embed.add_field(name="**Defender**",
                      value="More damage reduced",
                      inline=False)
      embed.add_field(name="**Brilliance**",
                      value="Higher chance for rare materials",
                      inline=False)
      await ctx.send(embed=embed)
    #There is no such starship
    elif starships.count(starship[0].upper()+starship[1:].lower()) == 0:
      await ctx.send('That is not a starship type (use `cs start` to view starship types)')
    #All the default stuff
    else:
      value = {}
      value['Starship'] = starship[0].upper()+starship[1:].lower()
      value['Modules'] = {
          'Solar Panel': [100, 1],
          'Basic Collector': [100, 1],
          'Metal Armor': [100, 1],
          'Rusty Detector': [100, 1],
          'Small Energy Storage': [100, 1],
          'Laser Gun': [100, 1]
      }
      value['Unlocked'] = [
          'Solar Panel', 'Basic Collector', 'Metal Armor', 'Rusty Detector',
          'Small Energy Storage', 'Laser Gun'
      ]
      value['StarshipLvl'] = 1
      value['Var'] = {
          'time': dt.datetime.utcnow(),
          'energy': Functions.StatsCal(value, 'MaxEnergy'),
          'pos': [0, 0, 0]
      }
      value['Inv'] = {}
      value['Zones'] = ['Alpha']
      value['Cooldown'] = [dt.datetime.utcnow(), dt.datetime.utcnow(), dt.datetime.utcnow(),dt.datetime.utcnow()]
      value['CooldownN'] = [0,0,0,0]
      db[Id] = str(value)
      await ctx.send('You have chosen the starship ' + starship + '. Check out `cs guide` to know what to do')
#For hourly
@bot.command(name='crate', aliases=['crates'])
async def crates(ctx, action='collect'):
  Id = str(ctx.message.author.id)
  v = eval(db[Id])
  action=action.lower()
  if 'Crates' not in v:
    v['Crates']=[1,0,'Rocky',dt.datetime.utcnow()]
    if 'Iron' in v['Inv']:
      v['Inv']['Iron']+=15
    else:
      v['Inv']['Iron']=15
    if 'Silicon' in v['Inv']:
      v['Inv']['Silicon']+=25
    else:
      v['Inv']['Silicon']=25
    if 'Space Rock' in v['Inv']:
      v['Inv']['Space Rock']+=50
    else:
      v['Inv']['Space Rock']=50
    if 'Silver' in v['Inv']:
      v['Inv']['Silver']+=5
    else:
      v['Inv']['Silver']=5
    if 'Gold' in v['Inv']:
      v['Inv']['Gold']+=2
    else:
      v['Inv']['Gold']=2
    embed = discord.Embed(title=ctx.message.author.name + "\'s Starter Crate",description='Every hour you can collect a supply crate sent from a mysterious source. You can also use `cs crate upgrade` to get more materials and other type of crates to choose from. Use `cs crate edit` to change crates.', color=discord.Color.blue())
    embed.add_field(name="Items recieved", value='**Space Rock**: 50 \n **Silicon**: 25 \n **Iron**: 15 \n **Silver**: 5 \n **Gold**: 1 ', inline=False)
    await ctx.send(embed=embed)
    v['Crates'][1]+=1
  elif action=='collect':
    seconds=dt.datetime.utcnow()-v['Crates'][3]
    seconds=seconds.total_seconds()
    if seconds>=3600:
      v['Crates'][3]=dt.datetime.utcnow()
      embed = discord.Embed(title=ctx.message.author.name + "\'s "+v['Crates'][2]+" Crate",description='', color=discord.Color.blue())
      v['Crates'][1]+=1
      streak=v['Crates'][1]
      level=v['Crates'][0]
      types=v['Crates'][2]
      embed.add_field(name="Stats", value='**Type**: '+types+'\n**Level**: '+str(level)+'\n**Streak**: '+str(streak), inline=False)
      recieved={}
      upper=int((level*5)*100*(1+streak/100))
      lower=int(upper*0.75)
      if v['Crates'][2]=='Rocky': 
        number=int(5*random.randint(lower,upper)/100)
        if 'Space Rock' in v['Inv']:
          v['Inv']['Space Rock']+=number
        else:
          v['Inv']['Space Rock']=number
        recieved['Space Rock']=number
        number=int(random.randint(lower,upper)/100)
        if 'Silicon' in v['Inv']:
          v['Inv']['Silicon']+=number
        else:
          v['Inv']['Silicon']=number
        recieved['Silicon']=number
        number=int(random.randint(lower,upper)/100)
        if 'Iron' in v['Inv']:
          v['Inv']['Iron']+=number
        else:
          v['Inv']['Iron']=number
        recieved['Iron']=number
      if v['Crates'][2]=='Icy': 
        number=int(10*random.randint(lower,upper)/100)
        if 'Space Rock' in v['Inv']:
          v['Inv']['Space Rock']+=number
        else:
          v['Inv']['Space Rock']=number
        recieved['Space Rock']=number
        number=int(5*random.randint(lower,upper)/100)
        if 'Ice' in v['Inv']:
          v['Inv']['Ice']+=number
        else:
          v['Inv']['Ice']=number
        recieved['Ice']=number
        number=int(0.05*random.randint(lower,upper)/100)
        if 'Diamond' in v['Inv']:
          v['Inv']['Diamond']+=number
        else:
          v['Inv']['Diamond']=number
        recieved['Diamond']=number
      if v['Crates'][2]=='Metallic': 
        number=int(2*random.randint(lower,upper)/100)
        if 'Iron' in v['Inv']:
          v['Inv']['Iron']+=number
        else:
          v['Inv']['Iron']=number
        recieved['Iron']=number
        number=int(1*random.randint(lower,upper)/100)
        if 'Silver' in v['Inv']:
          v['Inv']['Silver']+=number
        else:
          v['Inv']['Silver']=number
        recieved['Silver']=number
        number=int(0.5*random.randint(lower,upper)/100)
        if 'Gold' in v['Inv']:
          v['Inv']['Gold']+=number
        else:
          v['Inv']['Gold']=number
        recieved['Gold']=number
        number=int(0.001*random.randint(lower,upper)/100)
        if 'Titanium' in v['Inv']:
          v['Inv']['Titanium']+=number
        else:
          v['Inv']['Titanium']=number
        recieved['Titanium']=number
      if v['Crates'][2]=='Shiny': 
        number=int(5*random.randint(lower,upper)/100)
        if 'Silicon' in v['Inv']:
          v['Inv']['Silicon']+=number
        else:
          v['Inv']['Silicon']=number
        recieved['Silicon']=number
        number=int(0.05*random.randint(lower,upper)/100)
        if 'Diamond' in v['Inv']:
          v['Inv']['Diamond']+=number
        else:
          v['Inv']['Diamond']=number
        recieved['Diamond']=number
        number=int(0.005*random.randint(lower,upper)/100)
        if 'Amethyst' in v['Inv']:
          v['Inv']['Amethyst']+=number
        else:
          v['Inv']['Amethyst']=number
        recieved['Amethyst']=number
      if v['Crates'][2]=='Unbreakable': 
        number=int(0.1*random.randint(lower,upper)/100)
        if 'Diamond' in v['Inv']:
          v['Inv']['Diamond']+=number
        else:
          v['Inv']['Diamond']=number
        recieved['Diamond']=number
        number=int(0.005*random.randint(lower,upper)/100)
        if 'Titanium' in v['Inv']:
          v['Inv']['Titanium']+=number
        else:
          v['Inv']['Titanium']=number
        recieved['Titanium']=number
      if v['Crates'][2]=='Radiant': 
        number=int(0.01*random.randint(lower,upper)/100)
        if 'Amethyst' in v['Inv']:
          v['Inv']['Amethyst']+=number
        else:
          v['Inv']['Amethyst']=number
        recieved['Amethyst']=number
        number=int(0.005*random.randint(lower,upper)/100)
        if 'Titanium' in v['Inv']:
          v['Inv']['Titanium']+=number
        else:
          v['Inv']['Titanium']=number
        recieved['Titanium']=number
        number=int(0.002*random.randint(lower,upper)/100)
        if 'Uranium' in v['Inv']:
          v['Inv']['Uranium']+=number
        else:
          v['Inv']['Uranium']=number
        recieved['Uranium']=number
      send=''
      for x in recieved:
        if recieved[x]!=0:
          send=send+'**'+x+'**: '+str(recieved[x])+'\n'
      if send=='':
        send='The crate is empty. Unlucky you.'
      embed.add_field(name="Items recieved", value=send, inline=False)
      await ctx.send(embed=embed)
    else:
      embed = discord.Embed(title=ctx.message.author.name + "\'s "+v['Crates'][2]+" Crate",description='Your crate is currently on its way', color=discord.Color.blue())
      seconds=int(3600-seconds)
      minutes=seconds//60
      sec=seconds%60
      embed.add_field(name="**Time left**", value='**'+str(minutes)+'** minutes **'+str(sec)+'** seconds', inline=False)
      streak=v['Crates'][1]
      level=v['Crates'][0]
      types=v['Crates'][2]
      embed.add_field(name="Stats", value='**Type**: '+types+'\n**Level**: '+str(level)+'\n**Streak**: '+str(streak), inline=False)
      await ctx.send(embed=embed)
  elif action=='upgrade' or action=='up':
    items={'Space Rock':100, 'Ice':100, 'Silicon':75, 'Iron':75}
    level=v['Crates'][0]
    if level>=2:
      items['Silver']=50
      items['Gold']=25
    if level>=3:
      items['Diamond']=10
    if level>=4:
      items['Amethyst']=5
    if level>=5:
      items['Titanium']=1
    if level>=6:
      items['Uranium']=1
    for x in items:
      items[x]=items[x]*level
    enough=True
    try:
      for x in items:
          if v['Inv'][x] < items[x]:
            enough = False
    #Can't find the material in list
    except:
      enough = False
    #Enough materials
    if enough == True:
      await ctx.send('Are you sure you want to upgrade ur crates. This will cause a new crate to be send and the old crate destroyed [y/n]')
      try:
        msg = await bot.wait_for("message", timeout=30.0,check=lambda message: message.author == ctx.author)
      except asyncio.TimeoutError:
        await ctx.send('Upgrade cancelled')
      else:
        msg=msg.content
        msg=msg.lower()
        if msg=='y' or msg=='Y' or msg=='yes':
      #Subtracting the materials from inv
          for x in items:
            v['Inv'][x] -= items[x]
          #Upping the level
          v['Crates'][0]+=1
          v['Crates'][3]=dt.datetime.utcnow()
          embed = discord.Embed(title="Upgrade success",description="Your crates are now level " + str(v['Crates'][0]))
          #Calculating the next cost
          cost = ''
          items={'Space Rock':100, 'Ice':100, 'Silicon':75, 'Iron':75}
          level=v['Crates'][0]
          if level>=2:
            items['Silver']=50
            items['Gold']=25
          if level>=3:
            items['Diamond']=10
          if level>=4:
            items['Amethyst']=5
          if level>=5:
            items['Titanium']=1
          if level>=6:
            items['Uranium']=1
          for x in items:
            items[x]=items[x]*level
          for x in items:
            cost = cost + x + ': ' + str(items[x]) + '\n'
          embed.add_field(name="**Next upgrade cost**", value=cost, inline=False)
          await ctx.send(embed=embed)
        else:
          await ctx.send('Upgrade cancelled')
    else:
      embed = discord.Embed(title="Not enough materials", description="Your crates are currently level " + str(level))
      #Telling the cost of the current upgrade
      cost = ''
      for x in items:
        cost = cost + x + ': ' + str(items[x]) + '\n'
      embed.add_field(name="**Next upgrade cost**", value=cost, inline=False)
      await ctx.send(embed=embed)
  elif action=='edit' or action=='e':
    level=v['Crates'][0]
    types=v['Crates'][2]
    crates=md.crates[:level]
    send=''
    count=0
    for x in crates:
      send=send+'`id '+str(count)+'` '+x+'\n'
      count=count+1
    send=send+'`cancel` Cancel editing'
    embed = discord.Embed(title="Editting crates", description="Your crates are currently level " + str(level)+' '+types+' crates')
    embed.add_field(name="**Available Crates**", value=send, inline=False)
    embed.set_footer(text='Type in the id number to select')
    await ctx.send(embed=embed)
    try:
      msg = await bot.wait_for("message", timeout=30.0,check=lambda message: message.author == ctx.author)
    except asyncio.TimeoutError:
      await ctx.send('Edit cancel')
    else:
      msg=msg.content
      msg=msg.lower()
      proceed=False
      if msg.isnumeric():
        msg=int(msg)
        if msg<count:
          if crates[msg]!=types:
            proceed=True
            chosen=crates[msg]
          else:
            await ctx.send('Your current crate is already '+types)
    if proceed:
      await ctx.send('Are you sure you want to change your '+types+' crates to '+chosen+' crates? A new crate will be sent and the old crate will be destroyed. [y/n]')
      try:
        msg = await bot.wait_for("message", timeout=30.0,check=lambda message: message.author == ctx.author)
      except asyncio.TimeoutError:
        await ctx.send('Edit cancel')
      else:
        msg=msg.content
        msg=msg.lower()
        if msg=='y' or 'Y':
          v['Crates'][2]=chosen
          v['Crates'][3]=dt.datetime.utcnow()
          await ctx.send('Edit success')
        else:
          proceed=False
    if not proceed:
      await ctx.send('Edit cancelled')
        
  db[Id]=str(v)
#The command search (this is one hell of a chunk)
#Pass in how much energy will be used (can use % to indicate a percentage)
#Default is 100%
@bot.command(name='search')
async def search(ctx, energy='100%'):
  #Getting data
  Id = str(ctx.message.author.id)
  v = eval(db[Id])
  #Adding the regen of energy
  v['Var']['energy'] = Functions.EnergySet(v)
  v['Var']['time'] = dt.datetime.utcnow()
  #Saving
  db[Id] = str(v)
  #Checking if you have a laser detector
  if 'Laser Detector' in v['Modules']:
    #Checking if it is a percent and converting
    if energy[-1] == '%':
      #To prevent idiots to do over 100%
      if int(energy[:-1])>100:
        enough = False
        await ctx.send('Are you an idiot?')
      else:
        energy = float(energy[:-1]) * v['Var']['energy'] / 100
        enough = True
    else:
      if float(energy) > v['Var']['energy']:
        enough = False
        await ctx.send('You don\'t have enough energy')
      else:
        enough = True
    #Converting string to float
    energy = float(energy)
    #Checking enough energy
    if enough == True:
      #Calls event
      event = await events(Id, ctx, bot)
      #Re-retrieving the data
      v = eval(db[Id])
      if event == False:
        used = 0   #Used energy
        success = False
        find = False
        #Repeating until all the energy allocated is used up
        while energy > 1:
          used = used + 1
          energy = energy - 1
          zone = Functions.Zone(v['Var']['pos'])
          #Calculating the chance of finding something using the zone and the stat 'Rare'(Rare-chance)
          chance = round(25 / (Functions.StatsCal(v, 'Rare') * md.zoneevents[zone][1]))
          #Found something
          if random.randint(0, chance) == 0:
            #Higher chance to find trader with TradeLocator
            if 'TradeLocator' in v['Modules']:
              t=10
            else:
              t=25
            #A 10% chance to find free loot
            if random.randint(0, 10) == 0:
              #To indicate loop exited because of loot found
              find = True 
              await ctx.send('You found an abandon starship and dismantled it')
              materials = ''
              #List of zones
              keys_list = list(md.zone)
              #Getting the loot by inputting the loottable of the zone
              treasure = re.treasure(v,
              keys_list.index(Functions.Zone(v['Var']['pos'])))
              keys_list = list(treasure)
              for x in keys_list:
                if x in v['Inv']:
                    v['Inv'][x] += treasure[x]
                else:
                    v['Inv'][x] = 1
                materials = materials + '**' + x + '**: ' + str(treasure[x]) + '\n'
              embed = discord.Embed(title="Items obtained", description=materials,
              color=discord.Color.blue())
              await ctx.send(embed=embed)
            #Chance of finding a trader
            elif random.randint(1, t) == 1:
              #Running the trader function
              await re.trader(ctx, bot)
              find = True
              v = eval(db[Id])
            else:
              #Doig the battle things
              success = True   #Indicates theres a battle
              keys_list = list(md.zone)
              result = await Battle.rouge(ctx, v,
              keys_list.index(Functions.Zone(v['Var']['pos'])), bot, True, used)
              v = eval(db[Id])
              damage = result[1]
              if result[0] == True:
                treasures = re.treasure(v,keys_list.index(Functions.Zone(v['Var']['pos'])))
          if success == True or find == True:
            break
        #Doing module damage after battle
        if success:
          if result[0] == False:
            if result[1] == {}:
              pass
            else:
              keys_list = list(result[1])
              for x in keys_list:
                v['Modules'][x][0] -= result[1][x]
                if v['Modules'][x][0] < 25:
                  v['Modules'][x][0] = 25
          else:
            if result[1] == {}:
              pass
            else:
              keys_list = list(result[1])
              for x in keys_list:
                v['Modules'][x][0] -= result[1][x]
                if v['Modules'][x][0] < 25:
                  v['Modules'][x][0] = 25
            materials = '**Items salvaged**: \n'
            keys_list = list(treasures)
            for x in keys_list:
              if x in v['Inv']:
                v['Inv'][x] += treasures[x]
              else:
                v['Inv'][x] = 1
              materials = materials + '**' + x + '**: ' + str(treasures[x]) + '\n'
            embed = discord.Embed(title=ctx.message.author.name + " has won the battle", description=materials,color=discord.Color.blue())
            await ctx.send(embed=embed)
        #Show that you found nothing
        elif find == False:
          await ctx.send('You used up ' + str(used) + ' energy but you didn\'t find any starships')
        v['Var']['energy'] -= used
        db[Id] = str(v)
  #This is for no laser detector remember?
  else:
    await ctx.send(
          'Your detector sucks too much to do that. Get the *Laser Detector* to search for some starships')

#Just a dashboard for some stat commands
@bot.command(name='starship')
async def starship(ctx):
  Id = str(ctx.message.author.id)
  v = eval(db[Id])
  #Calculating average efficiency
  keys_list = list(v['Modules'])
  total = 0
  count = 0
  for x in keys_list:
    for y in range(0, v['Modules'][x][1]):
      total += v['Modules'][x][0]
      count = count + 1
  total = round(total / count, 2)
  #The rest of the stuff
  embed = discord.Embed(title=ctx.message.author.name + '\'s Starship',description="Starship Type: " + v['Starship'] + '\nStarship Efficiency: ' + str(total) + '%',color=discord.Color.blue())
  embed.add_field(name="`cs stats`", value='Used to check your starship stats', inline=False)
  embed.add_field(name="`cs energy`", value='Used to check the current energy you have', inline=False)
  embed.add_field(name="`cs inv`", value='Used to check what materials you have', inline=False)
  embed.add_field(name="`cs modules`", value='Used to check what modules you have', inline=False)
  db[Id] = str(v)
  await ctx.send(embed=embed)

#The collect command
@bot.command(name='collect', aliases=['c'])
async def collect(ctx):
  #Getting data
  Id = str(ctx.message.author.id)
  v = eval(db[Id])
  #Doing the energy thing
  v['Var']['energy'] = Functions.EnergySet(v)
  v['Var']['time'] = dt.datetime.utcnow()
  #Saving it
  db[Id] = str(v)
  
  
  #If there is enough energy for collection
  if v['Var']['energy'] >= Functions.StatsCal(v, 'CollectEnergy'):
    cooldown=False
    seconds=dt.datetime.utcnow()-v['Cooldown'][0]
    seconds=seconds.total_seconds()
    if seconds < v['CooldownN'][0]:
      await ctx.send(f"You collector is overheating. Wait for a bit ok?", delete_after=5)
      cooldown=True
    else:
      v['Cooldown'][0]=dt.datetime.utcnow()
      v['CooldownN'][0]=random.randint(3,10)
    if cooldown==False:
      #Call events
      event = await events(Id, ctx, bot)
      #Getting data
      v = eval(db[Id])
      if event == False:
        #How much stuff u can get
        collectamount = round(Functions.StatsCal(v, 'CollectAmount'))
        #So at least if ur collector is bust u can still get stuff
        if collectamount == 0:
          collectamount = 1
        collected = {}
        #Determine each item found
        for x in range(0, collectamount):
          #Determine rarity base on the stat 'Rare' (rare-chance)
          rarity = Functions.Collect(Functions.StatsCal(v, 'Rare'))
          zone = Functions.Zone(v['Var']['pos'])
          #Choose a random item(number) from the loottable of that zone base on the rarity
          items = random.randint(0, len(md.zone[zone][rarity]) - 1)
          #This is the real item
          item = md.zone[zone][rarity][items]
          if item in v['Inv']:
            v['Inv'][item] += 1
          else:
            v['Inv'][item] = 1
          if item in collected:
            collected[item] += 1
          else:
            collected[item] = 1
        #Subtracting the energy
        v['Var']['energy'] -= Functions.StatsCal(v, 'CollectEnergy')
        #Telling the player what they god
        send = ''
        collectedlist = list(collected)
        for x in collectedlist:
          send = send + '**' + x + '**: ' + str(collected[x]) + '\n'
        embed = discord.Embed(title=ctx.message.author.name + "\'s items found", description=send,color = discord.Color.blue())
        await ctx.send(embed=embed)
    #Not having enough energy dumbass
  else:
    await ctx.send(
        'Not enough energy. You can check your energy with `cs energy`.')
    #Save
  db[Id] = str(v)


#Display some energy stats  
@bot.command(name='energy', aliases=['e'])
async def energy(ctx):
  #Getting data
  Id = str(ctx.message.author.id)
  v = eval(db[Id])
  #Energy thing
  v['Var']['energy'] = Functions.EnergySet(v)
  v['Var']['time'] = dt.datetime.utcnow()
  #Calculating stuff
  percent = round( v['Var']['energy'] / Functions.StatsCal(v, 'MaxEnergy') * 100, 2)
  #The stuff sent
  embed = discord.Embed(title=ctx.message.author.name + '\'s starship is ' + str(percent) + "% Charged", description="Your starship's max energy is " + str(Functions.StatsCal(v, 'MaxEnergy')), color=discord.Color.blue())
  embed.add_field(name="**Current Energy**", value=str(v['Var']['energy']), inline=False)
  embed.add_field(name="**Energy Regeneration**",value=str(Functions.StatsCal(v, 'EnergyRegen')) + ' per second', inline=False)
  db[Id] = str(v)
  await ctx.send(embed=embed)

#Checking inventory
@bot.command(name='inv', aliases=['inventory', 'i'])
async def inv(ctx):
  #Getting data
  Id = str(ctx.message.author.id)
  v = eval(db[Id])
  #Getting the values
  materials=md.material_list
  values = v['Inv'].values()
  inv = ''
  #If inventory is empty
  if len(values) == 0:
    inv = 'Your inventory is empty. Use `cs collect` to get materials.'
  else:
    for x in materials:
      if x in v['Inv']:
        inv = inv + '**' + x + '**: ' + str(v['Inv'][x]) + '\n'
  embed = discord.Embed(title=ctx.message.author.name + "\'s inventory",description=inv, color=discord.Color.blue())
  await ctx.send(embed=embed)
  db[Id] = str(v)

#Just stats
@bot.command(name='stats')
async def stats(ctx):
  Id = str(ctx.message.author.id)
  v = eval(db[Id])
  embed = discord.Embed(title="Your starship stats",description= "Craft more modules or upgrade your starship to improve your stats",color=discord.Color.blue())
  embed.add_field(name="**Starship Level**",value='Level ' + str(v['StarshipLvl']),inline=False)
  embed.add_field(name="**Energy Capacity**",value=str(Functions.StatsCal(v, 'MaxEnergy')),inline=False)
  embed.add_field(name="**Energy Regeneration**",value=str(Functions.StatsCal(v, 'EnergyRegen')) +' per second', inline=False)
  embed.add_field(name="**Travel Efficiency**",value=str(Functions.StatsCal(v, 'TravelEnergy')) + ' energy per unit travelled', inline=False)
  embed.add_field(name="**Collection Energy**",value=str(Functions.StatsCal(v, 'CollectEnergy')) + ' energy per collect', inline=False)
  embed.add_field(name="**Collection Amount**",value=str(round(Functions.StatsCal(v, 'CollectAmount'))) + ' items per collect', inline=False)
  embed.add_field(name="**Better Material**",value=str(round(Functions.StatsCal(v, 'Rare'))) +' better materials', inline=False)
  embed.add_field(name="**Damage Reduced**", value=str(round(Functions.StatsCal(v, 'DamageReduced') * 100)) + '%', inline=False)
  embed.add_field(name="**Attack Energy Reduce**",value=str(Functions.StatsCal(v, 'AttackReduce') * 100) + '%', inline=False)
  embed.add_field(name="**Evade Chance**", value=str(100 - Functions.StatsCal(v, 'Evade') * 100) + '%',inline=False)
  embed.add_field(name="**Cooldown Reduction**", value=str(Functions.StatsCal(v, 'CooldownReduce') * 100) + '%',inline=False)
  await ctx.send(embed=embed)
  db[Id] = str(v)

#Check the zone
@bot.command(name='zones', aliases=['zone', 'z', 'coords'])
async def zones(ctx):
  Id = str(ctx.message.author.id)
  v = eval(db[Id])
  embed = discord.Embed(title=ctx.message.author.name + "\'s current zone is " + Functions.Zone(v['Var']['pos']), description= "Use `cs explore [distance/ %energy]` to discover new zones", color=discord.Color.blue())
  zones = ''
  for x in v['Zones']:
    zones = zones + x + '\n'
  if 'AdvancedNavigator' in v['Modules']:
    embed.add_field(name="**Current position**",value=[round(v['Var']['pos'][0],2),round(v['Var']['pos'][1],2),round(v['Var']['pos'][2],2)], inline=False)
  embed.add_field(name="**Your discovered zones**",value=zones, inline=False)
  await ctx.send(embed=embed)
  db[Id] = str(v)

#Check your module and their damage level
@bot.command(name='modules', aliases=['mod', 'mods'])
async def modulescheck(ctx, page='1'):
  Id = str(ctx.message.author.id)
  v = eval(db[Id])
  keys_list = list(v['Modules'])
  moduleCount = 0
  if page.isnumeric():
    page=int(page)
  for x in keys_list:
    moduleCount = moduleCount + v['Modules'][x][1]
  embed = discord.Embed(title=ctx.message.author.name + ' \'s modules',description="**Your max modules is " + str(10 + v['StarshipLvl'] * 5) + '**\n' + "You currently have " + str(moduleCount), color=discord.Color.blue())
  modules = ''
  valid=True
  if len(keys_list)>=x*20:
    keys_list=keys_list[(x-1)*20:(x*20)]
  elif len(keys_list)<=(x-1)*20:
    await ctx.send('You don\'t have that many modules')
    valid=False
  else:
    keys_list=keys_list[(x-1)*20:]
  if valid:
    for x in keys_list:
      modules = modules + '`id ' + str(
        moduleIndex.index(x)) + '` **' + x + '**' + ' x' + str(v['Modules'][x][1]) + ' at ' + str(round(v['Modules'][x][0])) + '% efficiency' + '\n'
    embed.add_field(name="**Your modules**", value=modules, inline=False)
    embed.set_footer(text='Use cs modules [page no.] to view other module pages')
    await ctx.send(embed=embed)
  db[Id] = str(v)

#Upgrade the ship
@bot.command(name='upgrade', aliases=['up'])
async def upgrade(ctx):
  #Getting data
  Id = str(ctx.message.author.id)
  v = eval(db[Id])
  #The material thing 
  keys_list = list(md.starshipUp[v['Starship']])
  #Scaling thing
  r = v['StarshipLvl']**2.5
  enough = True
  #Testing if there is enough materials
  try:
    for x in keys_list:
      if round(md.starshipUp[v['Starship']][x] * r) > 0:
        if v['Inv'][x] < round(md.starshipUp[v['Starship']][x] * r):
          enough = False
  #Can't find the material in list
  except:
    enough = False
  #Enough materials
  if enough == True:
    #Subtracting the materials from inv
    for x in keys_list:
      if round(md.starshipUp[v['Starship']][x] * r) > 0:
        v['Inv'][x] -= round(md.starshipUp[v['Starship']][x] * r)
    #Upping the level
    v['StarshipLvl'] += 1
    embed = discord.Embed(title="Upgrade success",description="Your starship is now level " + str(v['StarshipLvl']))
    #Calculating the next cost
    cost = ''
    r = v['StarshipLvl']**2.5
    for x in keys_list:
      cost = cost + x + ': ' + str(
        round(md.starshipUp[v['Starship']][x] * r)) + '\n'
    embed.add_field(name="**Next upgrade cost**", value=cost, inline=False)
    lvl = v['StarshipLvl']
    #Unlocking premade modules
    if lvl == 2:
      v['Unlocked'].append('Anti-Radar Cloaking')
      v['Unlocked'].append('Refined Collector')
      v['Unlocked'].append('Small Cooling System')
      v['Unlocked'].append('Laser Detector')
      v['Unlocked'].append('Medium Energy Storage')
    if lvl == 3:
      v['Unlocked'].append('Energy Blaster')
      v['Unlocked'].append('Combustion Engine')
      v['Unlocked'].append('Force Field')
      v['Unlocked'].append('Evasive Maneuvers')
      v['Unlocked'].append('Better Solar Panels')
    if lvl == 4:
      v['Unlocked'].append('SpaceNet')
      v['Unlocked'].append('Large Energy Storage')
      v['Unlocked'].append('Improved Cooling System')
      v['Unlocked'].append('Armor Piercer')
      v['Unlocked'].append('Efficient Collector')
    if lvl == 5:
      v['Unlocked'].append('StarForge')
      v['Unlocked'].append('Nuclear Strike')
      v['Unlocked'].append('Nuclear Reactor')
      v['Unlocked'].append('Titanium Armor')
      v['Unlocked'].append('Detection and Evasion')
  else:
    embed = discord.Embed(title="Not enough materials", description="Your starship is currently level " + str(v['StarshipLvl']))
    #Telling the cost of the current upgrade
    cost = ''
    for x in keys_list:
      cost = cost + x + ': ' + str(round(md.starshipUp[v['Starship']][x] * r)) + '\n'
    embed.add_field(name="**Next upgrade cost**", value=cost, inline=False)
  await ctx.send(embed=embed)
  #Saving
  db[Id] = str(v)

#Salvagin modules
@bot.command(name='dismantle')
async def dismantle(ctx, item, item2='none', item3='none',item4='none'):
  #Getting data
  Id = str(ctx.message.author.id)
  v = eval(db[Id])
  #Checking if specified by id
  if item.isnumeric():
    try:
      item = moduleIndex[int(item)]
    except:
      pass
  else:
    if item2!='none':
      item=item+' '+item2
    if item3!='none':
      item=item+' '+item3
    if item4!='none':
      item=item+' '+item4
  item=Functions.cap(item)
  if item=='Spacenet':
    item='SpaceNet'
  if item=='Tradelocator':
    item='TradeLocator'
  if item=='Advancednavigator':
    item='AdvancedNavigator'
  elif item=='Starforge':
    item='StarForge'
  #Getting list of modules
  keys_list = list(md.modules[item])
  #Set up
  valid = True
  haveModule = False
  #Checking if you actually have the module
  try:
    if v['Modules'][item][1] > 0:
      haveModule = True
  except:
    pass
  if haveModule:
    #Checking if the module is essential
    if 'EnergyRegen' in md.modules[item]:
      if Functions.StatsCal(v, 'EnergyRegen') <= md.modules[item]['EnergyRegen']:
        valid = False
    if 'MaxEnergy' in md.modules[item]:
      if Functions.StatsCal(v, 'MaxEnergy') <= md.modules[item]['MaxEnergy']:
        valid = False
    if 'CollectAmount' in md.modules[item]:
      if Functions.StatsCal(v, 'CollectAmount') <= md.modules[item]['CollectAmount']:
        valid = False
    if 'Rare' in md.modules[item]:
      if Functions.StatsCal(v, 'Rare') <= md.modules[item]['Rare']:
        valid = False
    if valid:
      cooldown=False
      seconds=dt.datetime.utcnow()-v['Cooldown'][1]
      seconds=seconds.total_seconds()
      if seconds<v['CooldownN'][1]:
        await ctx.send(f"Your crafter is running its cleaning sequence", delete_after=5)
        cooldown=True
      else:
        v['Cooldown'][1]=dt.datetime.utcnow()
        v['CooldownN'][1]=random.randint(5,10)
      if cooldown==False:
        #Deleting the module
        v['Modules'][item][1] -= 1
        if v['Modules'][item][1] == 0:
          v['Modules'].pop(item)
        #Giving the materials
        materials = md.modules[item]['Materials']
        keys_list = list(materials)
        items = {}
        send = '**Items salvaged**\n'
        for x in keys_list:
          #Materials are random btw
          amount = round((random.randint(0, 100) / 100) * materials[x])
          items[x] = amount
          v['Inv'][x] += amount
          send = send + '**' + x + '**: ' + str(amount) + '\n'
        embed = discord.Embed(title="Dismantle success", description=send)
        await ctx.send(embed=embed)
    #The module is essential
    else:
      await ctx.send('You can\'t dismantle that')
  #You dont have this module
  else:
    await ctx.send('You do not have this module')
  db[Id] = str(v)

#Crafting yay
@bot.command(name='craft')
async def craft(ctx, item, item2='none', item3='none', item4='none'):
  #Same thing
  Id = str(ctx.message.author.id)
  v = eval(db[Id])
  if item.isnumeric():
    try:
      item = moduleIndex[int(item)]
    except:
      pass
  else:
    if item2!='none':
      item=item+' '+item2
    if item3!='none':
      item=item+' '+item3
    if item4!='none':
      item=item+' '+item4
  item=Functions.cap(item)
  if item=='Spacenet':
    item='SpaceNet'
  if item=='Tradelocator':
    item='TradeLocator'
  if item=='Advancednavigator':
    item='AdvancedNavigator'
  elif item=='Starforge':
    item='StarForge'
  keys_list = list(v['Modules'])
  keys_list = list(v['Modules'])
  moduleCount = 0
  #Counting how much modules you currently have
  for x in keys_list:
    moduleCount = moduleCount + v['Modules'][x][1]
  #If ur maxed
  if moduleCount >= v['StarshipLvl'] * 5 + 10:
    await ctx.send(
        'Your modules are maxed. Use `cs upgrade` to get more slots or `cs dismantle [module]` to free up a slot'
    )
  elif item in v['Unlocked']:
    keys_list = list(md.modules[item]['Materials'])
    #Checking if you have enough material
    enough = True
    try:
      for x in keys_list:
        if v['Inv'][x] < md.modules[item]['Materials'][x]:
          enough = False
    except:
      enough = False
    valid = True
    #The module use up too much energy regen
    if 'EnergyRegen' in md.modules[item]:
      if Functions.StatsCal(v, 'EnergyRegen') + md.modules[item]['EnergyRegen'] * 2 <= 0:
        valid = False
        reason = 'Your starship will run out of energy if you craft that idiot'
    #The module use up too much max energy
    if 'MaxEnergy' in md.modules[item]:
      if Functions.StatsCal(v, 'MaxEnergy') + md.modules[item]['MaxEnergy'] <= 0:
        reason = 'That module takes up too much max energy'
        valid = False
    if enough == True and valid == True:
      cooldown=False
      seconds=dt.datetime.utcnow()-v['Cooldown'][1]
      seconds=seconds.total_seconds()
      if seconds<v['CooldownN'][1]:
        await ctx.send(f"Your crafter is running its cleaning sequence", delete_after=5)
        cooldown=True
      else:
        v['Cooldown'][1]=dt.datetime.utcnow()
        v['CooldownN'][1]=random.randint(5,15)
      if cooldown==False:
      #Subtracting all the materials used
        for x in keys_list:
          v['Inv'][x] = v['Inv'][x] - md.modules[item]['Materials'][x]
        await ctx.send('You have successfully crafted a ' + item)
        #If you already have this module
        if item in v['Modules']:
          #Second space net glitch
          if item == 'SpaceNet':
            await ctx.send(
                  'After crafting the second SpaceNet (Why would you even want to do that), the second SpaceNet flashed the numbers 19 18 13 then crashed. Guess you wasted those diamonds and amethyst.'
              )
          else:
            v['Modules'][item][1] += 1
        #Fist time unlocks
        else:
          v['Modules'][item] = [100, 1]
          if item == 'SpaceNet':
            v['Unlocked'].append('TradeLocator')
            v['Unlocked'].append('AdvancedNavigator')
            v['Market'] = {}
            await ctx.send('Connected to SpaceNet')
          if item == 'StarForge':
            v['Equip']={'Production':'none', 'Attack': 'none', 'Defense':'none', 'System': 'none', 'Storage':'none', 'Core':'none'}
            v['Crystals']={'Count':1}
            v['Crystals']['1']={'Frequency':1,'Equip':'none'}
            v['Crystals']['1']['Enchantments']=c.NewCrystal('starter')
            v['Crystals']['1']['Type']=md.crystals[list(v['Crystals']['1']['Enchantments'])[0]][0]
            await ctx.send('Congratulations, you can now harness the power of stars. Here\'s a star crystal to help you get started. Use `cs crystal` to view your crystal')
            v['Crystals']['Count']+=1
    else:
      if enough == False:
        keys_list = list(md.modules[item]['Materials'])
        send = ''
        for x in keys_list:
          try:
            send = send + '**' + x + '**: ' + str(
            v['Inv'][x]) + '/' + str(md.modules[item]['Materials'][x]) + '\n'
          except:
            send = send + '**' + x + '**: 0/' + str(md.modules[item]['Materials'][x]) + '\n'
        embed = discord.Embed(title="Not enough materials", description=send,color=discord.Color.blue())
        await ctx.send(embed=embed)
      else:
        await ctx.send(reason)
  else:
    await ctx.send('Module not found')
  db[Id] = str(v)

#Repair
@bot.command(name='repair')
async def repair(ctx, item, item2='none', item3='none',item4='none'):
  Id = str(ctx.message.author.id)
  v = eval(db[Id])
  if item.isnumeric():
    try:
      item = moduleIndex[int(item)]
    except:
      pass
  else:
    if item2!='none':
      item=item+' '+item2
    if item3!='none':
      item=item+' '+item3
    if item4!='none':
      item=item+' '+item4
  item=Functions.cap(item)
  if item=='Spacenet':
    item='SpaceNet'
  if item=='Tradelocator':
    item='TradeLocator'
  if item=='Advancednavigator':
    item='AdvancedNavigator'
  elif item=='Starforge':
    item='StarForge'
  if item in v['Modules']:
    if v['Modules'][item][0] == 100:
      await ctx.send('This module is fully functional')
    else:
      enough = True
      items_list = {}
      sent = ''
      material_list = list(md.modules[item]['Materials'])
      percent = (100 - v['Modules'][item][0]) / 100
      for x in material_list:
        neededItem = round(md.modules[item]['Materials'][x] * (percent * 1.5 + 0.1))
        if neededItem > 0:
          items_list[x] = neededItem
          sent = sent + '**' + x + '**: ' + str(neededItem) + '\n'
          try:
            if v['Inv'][x] < neededItem:
              enough = False
          except:
            enough = False
    if enough == True:
      cooldown=False
      seconds=dt.datetime.utcnow()-v['Cooldown'][1]
      seconds=seconds.total_seconds()
      if seconds<v['CooldownN'][1]:
        await ctx.send(f"Your crafter is running its cleaning sequence", delete_after=5)
        cooldown=True
      else:
        v['Cooldown'][1]=dt.datetime.utcnow()
        v['CooldownN'][1]=random.randint(5,25)
      if cooldown==False:
        for x in items_list:
          v['Inv'][x] = v['Inv'][x] - items_list[x]
        embed = discord.Embed(title="Success", description='**Materials used**: \n' + sent,color=discord.Color.blue())
        await ctx.send(embed=embed)
        if item in v['Modules']:
          v['Modules'][item][0] = 100
    else:
      embed = discord.Embed(title="Not enough materials", description='**Materials needed**: \n' + sent, color=discord.Color.blue())
      await ctx.send(embed=embed)
  else:
    await ctx.send('Module not found')
  db[Id] = str(v)

#Recipes pages
@bot.command(name='recipes')
async def recipes(ctx, page=1):
  Id = str(ctx.message.author.id)
  v = eval(db[Id])
  embed = discord.Embed(title="Unlocked Recipes", description="Use `cs info [module]` to know more about a module", color=discord.Color.blue())
  modules = ''
  if (page - 1) * 20 > len(v['Unlocked']):
    await ctx.send('Imagine thinking that you have that much recipes lmao')
  else:
    if page * 20 > len(v['Unlocked']):
      setmax = len(v['Unlocked'])
    else:
      setmax = page * 20
    for x in v['Unlocked'][(page - 1) * 20:setmax]:
      modules = modules + '`id ' + str(moduleIndex.index(x)) + '` ' + x + '\n'
    embed.add_field(name="**Modules**", value=modules, inline=False)
    embed.set_footer(text='Use cs recipes [page no.] to view other recipe pages')
    await ctx.send(embed=embed)
  db[Id] = str(v)

#Just info
@bot.command(name='info')
async def info(ctx, advance: str, item2='none', item3='none', item4='none'):
  Id = str(ctx.message.author.id)
  v = eval(db[Id])
  if advance.isnumeric():
    try:
      advance = moduleIndex[int(advance)]
    except:
      pass
  else:
    if item2!='none':
      advance=advance+' '+item2
    if item3!='none':
      advance=advance+' '+item3
    if item4!='none':
      advance=advance+' '+item4
  advance=Functions.cap(advance)
  if advance=='Spacenet':
    advance='SpaceNet'
  if advance=='Tradelocator':
    advance='TradeLocator'
  if advance=='Advancednavigator':
    advance='AdvancedNavigator'
  elif advance=='Starforge':
    advance='StarForge'

  if advance in v['Unlocked']:
    embed = discord.Embed(
        title=advance,
        description='Use `cs craft [module]` to craft the module',
        color=discord.Color.blue())
    material = ''
    keys_list = list(md.modules[advance]['Materials'])
    for x in keys_list:
        material = material + x + ': ' + str(
            md.modules[advance]['Materials'][x]) + '\n'
    embed.add_field(name="**Materials**", value=material, inline=False)
    stats = ''
    statsdict = md.modules[advance]
    if 'EnergyRegen' in statsdict:
      if statsdict['EnergyRegen'] > 0:
        stats = stats + 'Regenerate ' + str(statsdict['EnergyRegen']) + ' energy per second' + '\n'
      else:
        stats = stats + 'Uses ' + str(-statsdict['EnergyRegen']) + ' energy per second' + '\n'
    if 'TravelEnergy' in statsdict:
      stats = stats + 'Reduce ' + str(statsdict['TravelEnergy'] * 100) + '% energy when travelling' + '\n'
    if 'DamageReduced' in statsdict:
      stats = stats + 'Reduce damage to ' + str(statsdict['DamageReduced'] * 100) + '%' + '\n'
    if 'MaxEnergy' in statsdict:
      if statsdict['MaxEnergy'] > 0:
        stats = stats + 'Add ' + str(statsdict['MaxEnergy']) + ' max energy' + '\n'
      else:
        stats = stats + 'Takes up ' + str(-statsdict['MaxEnergy']) + ' max energy' + '\n'
    if 'Rare' in statsdict:
      stats = stats + 'Improve rarity by ' + str(statsdict['Rare']) + '\n'
    if 'CollectEnergy' in statsdict:
      stats = stats + 'Uses ' + str(statsdict['CollectEnergy']) + ' energy per collect' + '\n'
    if 'CollectEnergyReduce' in statsdict:
      stats = stats + 'Reduce ' + str(statsdict['CollectEnergyReduce'] * 100) + '% energy used when collecting' + '\n'
    if 'CollectAmount' in statsdict:
      stats = stats + 'Collects ' + str(statsdict['CollectAmount']) + ' items per collect' + '\n'
    if 'Evade' in statsdict:
      stats = stats + 'Adds ' + str(100 - statsdict['Evade'] * 100) + '% chance of evading an attack' + '\n'
    if 'Damage' in statsdict:
      stats = stats + 'Deals ' + str(statsdict['Damage']) + ' damage when used in combat' + '\n'
    if 'Cooldown' in statsdict:
      stats = stats + 'Takes ' + str(statsdict['Cooldown']) + ' rounds to recharge in combat' + '\n'
    if 'EnergyUse' in statsdict:
      stats = stats + 'Uses ' + str(statsdict['EnergyUse']) + ' energy in combat' + '\n'
    if 'CritChance' in statsdict:
      stats = stats + 'Has ' + str(statsdict['CritChance'] * 100) + ' % chance to deal extra damage' + '\n'
    if 'AttackReduce' in statsdict:
      stats = stats + 'Reduce attack energy use to ' + str(statsdict['AttackReduce'] * 100) + ' %' + '\n'
    if 'CooldownReduce' in statsdict:
      stats = stats + 'Reduce cooldown by ' + str(statsdict['CooldownReduce'] * 100) + ' %' + '\n'
    if stats == '':
      stats = 'None'
    embed.add_field(name='Stats', value=stats, inline=False)
    if 'Special' in statsdict:
      special = statsdict['Special']
    else:
      special = 'None'
    embed.add_field(name='Special', value=special, inline=False)
    await ctx.send(embed=embed)
  else:
    await ctx.send('Module not found')
  db[Id] = str(v)

#Exploration
@bot.command(name='explore', aliases=['ex'])
async def explore(ctx, distance='100%'):
  #Same old
  Id = str(ctx.message.author.id)
  v = eval(db[Id])
  position = v['Var']['pos']
  v['Var']['energy'] = Functions.EnergySet(v)
  v['Var']['time'] = dt.datetime.utcnow()
  energy = v['Var']['energy']
  invalid = False
  energyuse = Functions.StatsCal(v, 'TravelEnergy')
  #Checking if using percentage
  if distance[-1] == '%':
    distance = int(distance[:-1])
    if distance > 100 or distance <= 0:
      await ctx.send('A percentage should be between 0 and 100')
      invalid = True
    else:
      distance = (energy * distance) / (energyuse * 100)
  else:
    distance = int(distance)
    if distance * energyuse < energy:
      pass
    else:
      await ctx.send('Not enough energy')
      invalid = True
  db[Id] = str(v)
  #Enough energy
  if invalid == False:
    cooldown=False
    seconds=dt.datetime.utcnow()-v['Cooldown'][2]
    seconds=seconds.total_seconds()
    reduced = Functions.StatsCal(v, 'CooldownReduce')
    if seconds<v['CooldownN'][2]:
      await ctx.send(f"Your warp engine is cooling down", delete_after=5)
      cooldown=True
    else:
      v['Cooldown'][2]=dt.datetime.utcnow()
      v['CooldownN'][2]=random.randint(int(60*reduced),int(300*reduced))
    if cooldown==False:
    #Calling events
      event = await events(Id, ctx, bot)
      v = eval(db[Id])
      #Math ahead 
      if event == False:
        #Those are angles
        a = random.randint(0, 360)
        b = random.randint(0, 360)
        #Those are the destination coords
        x = math.cos(b) * math.cos(a) * distance + position[0]
        y = math.cos(b) * math.sin(a) * distance + position[1]
        z = math.sin(b) * distance + position[2]
        #If the direction picked is facing the origin
        while position[0]**2 + position[1]**2 + position[2]**2 > x**2 + y**2 + z**2:
          a = random.randint(0, 360)
          b = random.randint(0, 360)
          x = math.cos(b) * math.cos(a) * distance + position[0]
          y = math.cos(b) * math.sin(a) * distance + position[1]
          z = math.sin(b) * distance + position[2]
        #Telling the player stuff
        await ctx.send('Your starship moved ' + str(round(distance, 2)) + ' units')
        await ctx.send('Your starship used ' + str(round(distance * energyuse, 2)) + ' energy')
        if Functions.Zone([x, y, z]) in v['Zones']:
          if Functions.Zone([x, y, z]) != Functions.Zone(position):
            await ctx.send('You have entered the zone ' + Functions.Zone([x, y, z]))
        else:
          #If discover new zone put the zone into the found-zone list
          await ctx.send('You have discovered a new zone ' + Functions.Zone([x, y, z]))
          v['Zones'].append(Functions.Zone([x, y, z]))
        #Switching old coords for new coords
        v['Var']['pos'] = [x, y, z]
        #Subtracting energy
        v['Var']['energy'] = v['Var']['energy'] - round(distance * energyuse, 2)
  #Saving
  db[Id] = str(v)

#Explore cooldown


#Trading space rock for energy (Can specify using energy or number of space rock (2nd argument))
#Default of first argument is all (rocks)
@bot.command(name='combust')
async def combust(ctx, Input='all', unit='e'):
  Id = str(ctx.message.author.id)
  v = eval(db[Id])
  if 'Combustion Engine' in v['Modules']:
    energy = 0
    rocks = 0
    #Use up all the rocks
    if Input.lower() == 'all':
      rocks = v['Inv']['Space Rock']
      energy = round(rocks * (v['Modules']['Combustion Engine'][1]**0.5) / (1000 / v['Modules']['Combustion Engine'][0]), 2)
    #Just transfering units
    elif Input.isnumeric():
      Input = float(Input)
      invalid = False
      if Input < 0:
        invalid = True
      if unit == 'e':
        energy = Input
        rocks = energy * (1000 / v['Modules']['Combustion Engine'][0]) / (v['Modules']['Combustion Engine'][1]** 0.5)
      elif unit == 'r':
        rocks = int(Input)
        energy = round(rocks * (v['Modules']['Combustion Engine'][1]**0.5) / (1000 / v['Modules']['Combustion Engine'][0]), 2)
      else:
        invalid = True
        await ctx.send('Invalid arguement(s)')
    else:
      invalid = True
      await ctx.send('Invalid arguement(s)')
    if invalid == False:
      if rocks > v['Inv']['Space Rock']:
        invalid = True
        await ctx.send('Not enough rocks')
    if invalid == False:
      cooldown=False
      reduced = Functions.StatsCal(v, 'CooldownReduce')
      seconds=dt.datetime.utcnow()-v['Cooldown'][3]
      seconds=seconds.total_seconds()
      if seconds<v['CooldownN'][3]:
        await ctx.send(f"You combuster will overheat", delete_after=5)
        cooldown=True
      else:
        v['Cooldown'][3]=dt.datetime.utcnow()
        v['CooldownN'][3]=random.randint(int(120*reduced),int(180*reduced))
      if cooldown==False:
        #Getting energy data
        v['Var']['energy'] = Functions.EnergySet(v)
        v['Var']['time'] = dt.datetime.utcnow()
        #Adding energy/ subtracting rocks
        v['Var']['energy'] += energy
        v['Inv']['Space Rock'] -= rocks
        if v['Var']['energy'] > Functions.StatsCal(v, 'MaxEnergy'):
          v['Var']['energy'] = Functions.StatsCal(v, 'MaxEnergy')
        await ctx.send('Your combustion engine used ' + str(rocks) + ' rocks to create ' + str(energy) + ' energy.')
  else:
    await ctx.send('Craft the **Combustion Engine** to use this command')
  db[Id] = str(v)

#Travelling
#If first argument is 'coord' or 'c' checks for coordinate inputs in arguments 2~4
@bot.command(name='travel', aliases=['t'])
async def travel(ctx, zone='none', x='none',y='none',z='none'):
  Id = str(ctx.message.author.id)
  v = eval(db[Id])
  zone=Functions.cap(zone)
  if zone == Functions.Zone(v['Var']['pos']):
    await ctx.send('You are already in that zone')
  elif zone=='none':
    await ctx.send('Please specify a zone with `cs travel [zone]`')
  #Checking if zone valid
  elif zone in v['Zones']:
    db[Id] = str(v)
    reduced = Functions.StatsCal(v, 'CooldownReduce')
    cooldown=False
    seconds=dt.datetime.utcnow()-v['Cooldown'][2]
    seconds=seconds.total_seconds()
    if seconds<v['CooldownN'][2]:
      await ctx.send(f"Your warp engine is cooling down", delete_after=5)
      cooldown=True
    else:
      v['Cooldown'][2]=dt.datetime.utcnow()
      v['CooldownN'][2]=random.randint(int(120*reduced),int(300*reduced))
    if cooldown==False:
      v = eval(db[Id])
      #Call event
      event = await events(Id, ctx, bot)
      if event == False:
        #The usual stuff
        position = v['Var']['pos']
        v['Var']['energy'] = Functions.EnergySet(v)
        v['Var']['time'] = dt.datetime.utcnow()
        energy = v['Var']['energy']
        #Calculating the max distance
        energyuse = Functions.StatsCal(v, 'TravelEnergy')
        maxTravelDist = energy / Functions.StatsCal(v, 'TravelEnergy')
        #Calculating the ratio of y and z coords according to x
        a = position[1] / position[0]
        b = position[2] / position[0]
        r = md.zonevalue[zone]
        #Checking if you are travelling outwards
        #If you are the target will be set to the inner border of the zone
        if r > md.zonevalue[Functions.Zone(v['Var']['pos'])]:
          keys_list = list(md.zonevalue)
          values = md.zonevalue.values()
          values_list = list(values)
          r = values_list[keys_list.index(zone) - 1]
        #Getting the x coords on the line from origin the current position with distance r from origin
        x = math.sqrt((r**2) / (1 + a**2 + b**2))
        #Getting y and z back using the ratios
        y = x * a
        z = x * b
        #IF you start out positive ur coords should end up positive (etc.)
        if position[0] > 0:
          x = abs(x)
        else:
          x = -abs(x)
        if position[1] > 0:
          y = abs(y)
        else:
          y = -abs(y)
        if position[2] > 0:
          z = abs(z)
        else:
          z = -abs(z)
        #Calculating the difference in coords 
        xdiff = x - position[0]
        ydiff = y - position[1]
        zdiff = z - position[2]
        #Adding a tiny bit to the difference so you won't land exactly on the border (which causes some problems you dont want to know)
        if xdiff > 0:
          xdiff = xdiff + 1
        else:
          xdiff = xdiff - 1
        if ydiff > 0:
          ydiff = ydiff + 1
        else:
          ydiff = ydiff - 1
        if zdiff > 0:
          zdiff = zdiff + 1
        else:
          zdiff = zdiff - 1
        #Calculating the travel distance after the tweeks
        travelDist = math.sqrt(xdiff**2 + ydiff**2 + zdiff**2)
        success = True
        #If you dont have enough fuel, you will half way
        if travelDist > maxTravelDist:
          x = position[0] + (xdiff / travelDist) * maxTravelDist
          y = position[1] + (ydiff / travelDist) * maxTravelDist
          z = position[2] + (zdiff / travelDist) * maxTravelDist
          success = False   #Indicate you didnt reach destination
          travelDist = maxTravelDist
        #You have enough fuel
        else:
          x = position[0] + xdiff
          y = position[1] + ydiff
          z = position[2] + zdiff
        used = travelDist * energyuse
        if success:
          await ctx.send('You have reached the zone ' + zone)
        else:
          await ctx.send('You are on your way to the zone ' + zone + ' but you ran out of energy')
          if Functions.Zone(v['Var']['pos']) != Functions.Zone([x, y, z]):
            if Functions.Zone([x, y, z]) not in v['Zones']:
              await ctx.send('You must have missed a zone while exploring, since you are currently now in the newly discovered zone ' + Functions.Zone([x, y, z]))
              v['Zones'].append(Functions.Zone([x, y, z]))
            else:
              await ctx.send('You are currently in the zone ' + Functions.Zone([x, y, z]))
      await ctx.send('You travelled ' + str(round(travelDist, 2)) + ' units')
      await ctx.send('You used ' + str(round(used, 2)) + ' energy')
      v['Var']['pos'] = [x, y, z]
      v['Var']['energy'] = v['Var']['energy'] - used
  #Using coords
  elif zone=='Coords' or zone=='C' or zone=='Coord':
    if 'AdvancedNavigator' in v['Modules'] and 'SpaceNet' in v['Modules']:
      #Checking if some non mess up the input
      proceed=True
      if x[0]=='-':
        if x[1:].isnumeric():
          x=-int(x[1:])
      elif x.isnumeric():
        x=int(x)
      else:
        proceed=False
      if y[0]=='-':
        if x[1:].isnumeric():
          y=-int(y[1:])
      elif y.isnumeric():
        y=int(y)
      else:
        proceed=False
      if z[0]=='-':
        if z[1:].isnumeric():
          z=-int(z[1:])
      elif z.isnumeric():
        z=int(z)
      else:
        proceed=False
      if proceed:
        #Checking if your in range
        if (x**2+y**2+z**2)<=10000:
          reduced = Functions.StatsCal(v, 'CooldownReduce')
          cooldown=False
          seconds=dt.datetime.utcnow()-v['Cooldown'][2]
          seconds=seconds.total_seconds()
          if seconds<v['CooldownN'][2]:
            await ctx.send(f"Your warp engine is cooling down", delete_after=5)
            cooldown=True
          else:
            v['Cooldown'][2]=dt.datetime.utcnow()
            v['CooldownN'][2]=random.randint(int(180*reduced),int(450*reduced))
          if cooldown==False:
            db[Id] = str(v)
            #Calling event
            event = await events(Id, ctx, bot)
            v = eval(db[Id])
            if event == False:
              #Same thing
              position = v['Var']['pos']
              v['Var']['energy'] = Functions.EnergySet(v)
              v['Var']['time'] = dt.datetime.utcnow()
              energy = v['Var']['energy']
              energyuse = Functions.StatsCal(v, 'TravelEnergy')
              maxTravelDist = energy / Functions.StatsCal(v, 'TravelEnergy')
              current=v['Var']['pos']
              #Calculating distance
              xdiff=x-current[0]
              ydiff=y-current[1]
              zdiff=z-current[2]
              travelDist = math.sqrt(xdiff**2 + ydiff**2 + zdiff**2)
              success = True
              #Same thing (stop half way)
              if travelDist > maxTravelDist:
                  x = position[0] + (xdiff / travelDist) * maxTravelDist
                  y = position[1] + (ydiff / travelDist) * maxTravelDist
                  z = position[2] + (zdiff / travelDist) * maxTravelDist
                  success = False
                  travelDist = maxTravelDist
              used = travelDist * energyuse
              if success:
                await ctx.send('You have reached your destination')
              else:
                await ctx.send('You are on your way to you destination but you ran out of energy')
              await ctx.send('You travelled ' + str(round(travelDist, 2)) +
                            ' units')
              await ctx.send('You used ' + str(round(used, 2)) + ' energy')
              v['Var']['pos'] = [x, y, z]
              v['Var']['energy'] = v['Var']['energy'] - used
        else:
          await ctx.send('Position is outside SpaceNet range')
      else:
        await ctx.send('Correct usage of this command is `cs travel coords [x] [y] [z]`')
    else:
      await ctx.send('Connect to SpaceNet Navigation to use this command')
  else:
    await ctx.send('Zone not found')
  db[Id] = str(v)

#Crystal stuffs
@bot.command(name='crystals', aliases=['crystal'])
async def Crystal(ctx, action='view'):
  Id = str(ctx.message.author.id)
  v = eval(db[Id])
  if 'StarForge' in v['Modules']:
    if action=='view':
      crystals=v['Crystals']
      embed = discord.Embed(title=ctx.message.author.name + "\'s crystals",description='You currently have '+str(len(list(crystals)))+' crystals', color=discord.Color.blue())
      send=''
      count=1
      for x in crystals:
        if x!='Count':
          send=''
          send=send+'**Type**: '+v['Crystals'][x]['Type']+'\n'+'**Enchantments**: '+'\n'
          for y in v['Crystals'][x]['Enchantments']:
            send=send+y+' '+md.numerals[v['Crystals'][x]['Enchantments'][y]]+'\n'
          if count%2==0:
            inline=False
          else:
            inline=True
          embed.add_field(name="`id "+x+'`',value=send,inline=inline)
          count=count+1 
      await ctx.send(embed=embed)
#Just sending it to the bot token
bot.run(os.getenv('TOKEN'))
