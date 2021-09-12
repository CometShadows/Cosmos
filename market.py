import discord
import asyncio
from replit import db
import random
import datetime
import modules
import Functions as f

def read(id,trade,self):
  send='`id '+id+'` '
  tradelist=list(trade)
  if self==True:
    item1=tradelist[0]
    item2=tradelist[1]
  else:
    item1=tradelist[1]
    item2=tradelist[0]
  send=send+str(trade[item1])+' **'+item1+'** for '+str(trade[item2])+' **'+item2+'**'
  return send
async def add(ctx,bot):
  Id=str(ctx.message.author.id)
  v=eval(db[Id])
  m=eval(db['Market'])
  trade=True
  tradeinfo={}
  while trade==True:
    exit=False
    await ctx.send('Which material do you wish to offer (Type `cancel` at anytime to cancel)')
    try:
      msg = await bot.wait_for("message", timeout=30.0,check=lambda message: message.author == ctx.author)
    except asyncio.TimeoutError:
      await ctx.send('The system shut down after idling for too long. Trade cancelled')
      trade=False
    else:
      msg=msg.content
      msg=f.cap(msg)
      if msg in modules.material_list:
        exit=True
        tradeinfo[msg]=0
      elif msg=='Cancel':
        trade=False
        await ctx.send('Trade cancelled')
      else:
        await ctx.send('Material not found')
    if exit==True:
      break
  while trade==True:
    exit=False
    tradeinfolist=list(tradeinfo)
    item=tradeinfolist[0]
    await ctx.send('How much of '+ item+' do you wish to offer (Type `cancel` at anytime to cancel)')
    try:
      msg = await bot.wait_for("message", timeout=30.0,check=lambda message: message.author == ctx.author)
    except asyncio.TimeoutError:
      await ctx.send('The system shut down after idling for too long. Trade cancelled')
      trade=False
    else:
      msg=msg.content
      if msg.isnumeric():
        msg=int(msg)
        if msg>0:
          if v['Inv'][item]>= msg:
            tradeinfo[item]=msg
            exit=True
          else:
            await ctx.send('Are you trying to scam someone? You only have '+str(v['Inv'][item])+' '+item)
        elif msg==0:
          await ctx.send('You can\'t trade nothing')
        else:
          await ctx.send('Why are you trying to trade negative things. Be positive')
        
      elif msg=='cancel':
        trade=False
        await ctx.send('Trade cancelled')
      else:
        await ctx.send('Input invalid')
    if exit==True:
      break
  while trade==True:
    exit=False
    await ctx.send('Which material do you want (Type `cancel` at anytime to cancel)')
    try:
      msg = await bot.wait_for("message", timeout=30.0,check=lambda message: message.author == ctx.author)
    except asyncio.TimeoutError:
      await ctx.send('The system shut down after idling for too long. Trade cancelled')
      trade=False
    else:
      msg=msg.content
      msg=f.cap(msg)
      if msg in modules.material_list:
        exit=True
        tradeinfo[msg]=0
      elif msg=='Cancel':
        trade=False
        await ctx.send('Trade cancelled')
      else:
        await ctx.send('Material not found')
    if exit==True:
      break
  while trade==True:
    exit=False
    tradeinfolist=list(tradeinfo)
    item=tradeinfolist[1]
    await ctx.send('How much of '+ item+' do you want (Type `cancel` at anytime to cancel)')
    try:
      msg = await bot.wait_for("message", timeout=30.0,check=lambda message: message.author == ctx.author)
    except asyncio.TimeoutError:
      await ctx.send('The system shut down after idling for too long. Trade cancelled')
      trade=False
    else:
      msg=msg.content
      if msg.isnumeric():
        msg=int(msg)
        if msg>=0:
          tradeinfo[item]=msg
          exit=True
        else:
          await ctx.send('Be nice. Stop trying to scam people')
      elif msg=='cancel':
        trade=False
        await ctx.send('Trade cancelled')
      else:
        await ctx.send('Input invalid')
    if exit==True:
      break
  if trade==True:
    tradeinfolist=list(tradeinfo)
    get=tradeinfolist[1]
    give=tradeinfolist[0]
    await ctx.send('Are you sure you want '+str(tradeinfo[get])+' '+get+' for '+str(tradeinfo[give])+' '+give+'. [y/n]')
    try:
      msg = await bot.wait_for("message", timeout=30.0,check=lambda message: message.author == ctx.author)
    except asyncio.TimeoutError:
      await ctx.send('The system shut down after idling for too long. Trade cancelled')
      trade=False
    else:
      msg=msg.content
      if msg=='y' or msg=='Y':
        v['Inv'][give]-=tradeinfo[give]
        v['Market'][str(m['id'])]=tradeinfo
        tradeinfo['user']=str(ctx.message.author.id)

        if get not in m['give']:
          m['give'][get]={}
        if give in m['give'][get]:
          m['give'][get][give][str(m['id'])]=tradeinfo
        else:
          m['give'][get][give]={str(m['id']):tradeinfo}
        if give not in m['get']:
          m['get'][give]={}
        if get in m['get'][give]:
          m['get'][give][get][str(m['id'])]=tradeinfo
        else:
          m['get'][give][get]={str(m['id']):tradeinfo}
        m['id']+=1
        await ctx.send('Trade successfully listed. Check you inbox to see your accepted trades')
        
      elif msg=='n' or msg=='N':
        trade=False
        await ctx.send('Trade cancelled')
      else:
        await ctx.send('Wtf are you doing? Answer `y` or `n`')
  db[Id]=str(v)
  db['Market']=str(m)
async def listing(ctx, bot):
  id=str(ctx.message.author.id)
  v=eval(db[id])
  market=v['Market']
  print(eval(db['Market']))
  if market=={}:
    await ctx.send('You don\'t have any market listings yet. Use `cs market add` to add trades')
  else:
    send=''
    for x in market:
      send=send+read(x,market[x],True)+'\n'
    embed=discord.Embed(
      title=ctx.message.author.name+"\'s market listings", description=send, color=discord.Color.blue())
    await ctx.send(embed=embed)
async def delete(ctx, bot, select):
  id=str(ctx.message.author.id)
  v=eval(db[id])
  m=eval(db['Market'])
  market=v['Market']
  idlist=list(market)
  if select in idlist:
    trade=v['Market'][select]
    await ctx.send('Are you sure you want to delete the trade [y/n] \n'+read(select,trade,True))
    try:
      msg = await bot.wait_for("message", timeout=30.0,check=lambda message: message.author == ctx.author)
    except asyncio.TimeoutError:
      await ctx.send('Action cancelled')
    else:
      msg=msg.content
      if msg=='y' or msg=='Y':
        item1=list(trade)[0]
        item2=list(trade)[1]
        m['give'][item2][item1].pop(select)
        m['get'][item1][item2].pop(select)
        v['Inv'][item1]+=trade[item1]
        v['Market'].pop(select)
        await ctx.send('Trade successfully deleted')
        db[id]=str(v)
        db['Market']=str(m)
      else:
        await ctx.send('Trade cancelled')
  else:
    await ctx.send('Invalid id')
async def search(ctx,bot):
  id=str(ctx.message.author.id)
  v=eval(db[id])
  m=eval(db['Market'])
  get=''
  give=''
  trade=True
  await ctx.send('Which material do you want (Type `none` if you don\'t want to specify or `cancel` to cancel)')
  try:
    msg = await bot.wait_for("message", timeout=30.0,check=lambda message: message.author == ctx.author)
  except asyncio.TimeoutError:
    await ctx.send('The system shut down after idling for too long. Search cancelled')
    trade=False
  else:
    msg=msg.content
    msg=f.cap(msg)
    if msg in modules.material_list or msg=='None':
      get=msg
    elif msg=='Cancel':
      await ctx.send('Search cancelled')
      trade=False
    else:
      await ctx.send('Invalid argument')
      trade=False
  if trade:
    await ctx.send('Which material are you willing to give (Type `none` if you don\'t want to specify or `cancel` to cancel)')
    try:
      msg = await bot.wait_for("message", timeout=30.0,check=lambda message: message.author == ctx.author)
    except asyncio.TimeoutError:
      await ctx.send('The system shut down after idling for too long. Search cancelled')
      trade=False
    else:
      msg=msg.content
      msg=f.cap(msg)
      if msg in modules.material_list or msg=='None':
        give=msg
      elif msg=='Cancel':
        await ctx.send('Search cancelled')
        trade=False
      else:
        await ctx.send('Invalid argument')
        trade=False
  if trade:
    result={}
    try:
      if get=='None':
        if give=='None':
          for x in m['give']:
            for y in m['give'][x]:
              result.update(m['give'][x][y])
        else:
          for x in m['give'][give]:
            result.update(m['give'][give][x])
      else:
        if give=='None':
          for x in m['get'][get]:
            result.update(m['get'][get][x])
        else:
          result.update(m['get'][get][give])
    except:
      pass

    resultlist=list(result)
    if len(resultlist)>20:
      resultlist=random.sample(resultlist,20)
    send=''
    for x in resultlist:
      send=send+read(x,result[x],False)
    if send=='':
      await ctx.send('No listings found')
    else:
      embed=discord.Embed(
      title=ctx.message.author.name+"\'s search results", description=send, color=discord.Color.blue())
      await ctx.send(embed=embed)
async def select(ctx,bot,selected):
  Id=str(ctx.message.author.id)
  v=eval(db[Id])
  m=eval(db['Market'])
  alltrades={}

  for x in m['give']:
    for y in m['give'][x]:
      alltrades.update(m['give'][x][y])
  if selected in alltrades:
    trade=alltrades[selected]
    give=list(trade)[1]
    get=list(trade)[0]
    if trade[give]>v['Inv'][give]:
      await ctx.send('You can\'t afford that')
    else:
      await ctx.send('Are you sure you want '+str(trade[get])+' **'+get+'** for '+str(trade[give])+' **'+give+'**? [y/n]')
      try:
        msg = await bot.wait_for("message", timeout=30.0,check=lambda message: message.author == ctx.author)
      except asyncio.TimeoutError:
        await ctx.send('The system shut down after idling for too long. Trade cancelled')
      else:
        msg=msg.content
        if msg=='Y' or msg=='y':
          if get in v['Inv']:
            v['Inv'][get]+=trade[get]
            v['Inv'][give]-=trade[give]
            recieverid=trade['user']
            recieverv=eval(db[recieverid])
            recieverv['Inv'][give]+=trade[give]
            if 'Profit' not in recieverv:
              recieverv['Profit']={}
            recieverv['Profit'].update(trade)
            recieverv['Market'].pop(selected)
            db[recieverid]=str(recieverv)
            m['give'][give][get].pop(selected)
            m['get'][get][give].pop(selected)
            db[id]=str(v)
            db['Market']=str(m)
        else:
          await ctx.send('Trade cancelled')
  else:
    await ctx.send('Trade not found')

async def inbox(ctx):
  id=str(ctx.message.author.id)
  v=eval(db[id])
  send=''
  if 'Profit' in v:
    for x in v['Profit']:
      send=send+read(x,v['Profit'][x],True)+'\n'
    v.pop('Profit')
  else:
    send='You don\'t have any new accepted trades'
  embed=discord.Embed(
      title=ctx.message.author.name+"\'s accepted trades", description=send, color=discord.Color.blue())
  await ctx.send(embed=embed)
  db[id]=str(v)