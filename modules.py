#'Module name':{Stats,'Materials':{materials}, 'Class':class, 'Type':type}
modules={
  'Solar Panel':{'EnergyRegen':0.1,'Materials':{'Silicon':10, 'Iron':5},'Class':'Production','Type':'Energy'},
  'Basic Collector':{'CollectEnergy':5, 'CollectAmount':1,'CollectEnergyReduce':0.99,'Materials':{'Space Rock':50, 'Iron':5, 'Silicon':5}, 'Class':'Production', 'Type':'Physical'}, 
  'Metal Armor':{'DamageReduced':0.95, 'Materials':{'Space Rock':50, 'Iron':20},'Class':'Defense', 'Type':'Physical'}, 
  'Rusty Detector':{'AsteroidChance':100, 'Rare':1, 'Materials':{'Silicon':10, 'Iron':5, 'Silver':1},'Class':'System', 'Type':'Energy'}, 
  'Small Energy Storage':{'MaxEnergy':10, 'Materials':{'Space Rock':50, 'Gold':1, 'Silicon':10},'Class':'Storage', 'Type':'Energy'}, 
  'Laser Gun':{'Damage':1,'EnergyUse':5,'Cooldown':0,'Materials':{'Space Rock':20, 'Iron':10, 'Silver':1},'Class':'Attack', 'Type':'Energy'},
  'Anti-Radar Cloaking':{'Evade':0.99,'RougeChance':100,'Materials':{'Silicon':10, 'Iron':20, 'Silver':5},'Class':'System', 'Type':'Energy'},
  'Refined Collector':{'CollectEnergy':12, 'CollectAmount':3,'CollectEnergyReduce':0.95,'Materials':{'Space Rock':75, 'Iron':15, 'Silicon':15, 'Gold':1},'Class':'Production', 'Type':'Physical'},
  'Small Cooling System':{'TravelEnergy':0.95,'CooldownReduce':0.95, 'CollectEnergyReduce':0.95,'AttackReduce':0.95,'Materials':{'Ice':50, 'Iron':10, 'Silver':5},'Class':'System', 'Type':'Physical'},
  'Laser Detector':{'AsteroidChance':200, 'Rare':3,'Special':'A better detector to help you search for starships. Use `cs search [energy/ percent energy]` to search for starships', 'Materials':{'Silicon':25, 'Iron':15, 'Silver':5,'Diamond':1},'Class':'System', 'Type':'Energy'},
  'Medium Energy Storage':{'MaxEnergy':25, 'Materials':{'Space Rock':75, 'Gold':3, 'Silicon':20},'Class':'Storage', 'Type':'Energy'},
  'Energy Blaster':{'Damage':5, 'EnergyUse':15,'Cooldown':3,'EnergyRegen':-0.2, 'Materials':{'Space Rock':50, 'Silver':10, 'Amethyst':1},'Class':'Attack', 'Type':'Energy'},
  'Combustion Engine':{'Special':'Turn space rocks into energy. Use `cs combust [energy/rocks/all] [unit]`','Materials':{'Space Rock':100, 'Silicon':25,'Iron':25, 'Silver':5,'Gold':5},'Class':'Production', 'Type':'Physical'},
  'Force Field':{'MaxEnergy':-10, 'DamageReduced':0.75, 'Materials':{'Silicon':50, 'Gold':10, 'Diamond':5},'Class':'Defense', 'Type':'Energy'},
  'Evasive Maneuvers':{'Evade':0.9, 'EnergyRegen':-0.1, 'Materials':{'Silver':25, 'Gold':15, 'Diamond':3},'Class':'System', 'Type':'Energy'},
  'Better Solar Panels':{'EnergyRegen':0.5, 'Materials':{'Silicon':50, 'Silver':10, 'Diamond':5},'Class':'Production', 'Type':'Energy'},
  'SpaceNet':{'EnergyRegen':-0.2,'Special':'Connect to SpaceNet to access a lot of new stuff. Unlocks `cs market`,  *TraderLocator*, *AdvancedNavigator*, etc.', 'Materials':{'Diamond':5, 'Amethyst':1},'Class':'System', 'Type':'Energy'},
  'Large Energy Storage':{'MaxEnergy':75, 'Materials':{'Space Rock':150, 'Gold':10, 'Silicon':75, 'Diamond':1},'Class':'Storage', 'Type':'Energy'},
  'Improved Cooling System':{'TravelEnergy':0.8,'CooldownReduce':0.8, 'CollectEnergyReduce':0.8,'AttackReduce':0.8,'Materials':{'Ice':150, 'Iron':25, 'Silver':15, 'Diamond':1},'Class':'System', 'Type':'Energy'},
  'Armor Piercer':{'Damage':7, 'EnergyUse':25,'Cooldown':1,'CritChance':0.1,'Materials':{'Space Rock':150, 'Silver':10,'Iron':50, 'Silicon':75, 'Titanium':1},'Class':'Attack', 'Type':'Physical'},
  'Efficient Collector':{'CollectEnergy':20, 'CollectAmount':5,'CollectEnergyReduce':0.90,'Materials':{'Space Rock':125, 'Iron':25, 'Silicon':25, 'Gold':5, 'Diamond':1},'Class':'Production', 'Type':'Physical'},
  'TradeLocator':{'Special':'Connect to SpaceNet to locate nearby traders. Increased chance to find a trader starship with `search`','Materials':{'Iron':50, 'Silicon':50, 'Gold':10, 'Diamond':1},'Class':'System', 'Type':'Energy'},
  'AdvancedNavigator':{'Special':'Connect to SpaceNet to finally know your coordinates relative to SpaceNet. Unlocks `cs coords` and `cs travel c [x] [y] [z]`','Materials':{'Iron':50, 'Silicon':50, 'Gold':10, 'Amethyst':1},'Class':'System', 'Type':'Energy'},
  'StarForge':{'Special':'Harness the power of stars (?)','Materials':{'Silicon':250,'Iron':100, 'Silver':50, 'Diamond':25,'Amethyst':10,'Titanium':2,'Uranium':1}},
  'Nuclear Strike':{'Damage':15, 'EnergyUse':50,'Cooldown':5,'CritChance':0.5,'EnergyRegen':-0.5,'Materials':{'Iron':100, 'Silver':25, 'Titanium':1, 'Uranium':5},'Class':'Attack', 'Type':'Physical'},
  'Nuclear Reactor':{'EnergyRegen':5, 'Materials':{'Iron':100, 'Titanium':5, 'Uranium':5},'Class':'Production', 'Type':'Physical'},
  'Titanium Armor':{'DamageReduced':0.5, 'Materials':{'Iron':250, 'Titanium':10},'Class':'Defense', 'Type':'Physical'},
  'Detection and Evasion':{'Evade':0.75,'Rare':10, 'EnergyRegen':-0.5, 'Materials':{'Silver':75, 'Diamond':15, 'Amethyst':10},'Class':'System', 'Type':'Energy'}}
#Classes
classes=['System', 'Production', 'Attack', 'Defense', 'Storage']


#'Stat name': Stacks by multiplying [True] or addition [False]
stats={'EnergyRegen':False, 'TravelEnergy':True, 'Evade':True, 'MaxEnergy':False, 'DamageReduced':True, 'Rare':False, 'CollectEnergy':True, 'AsteroidChance':False, 'Damage':False, 'RougeChance':False, 'CollectAmount':False, 'AttackReduce':True, 'CooldownReduce':True}
#The boosts of starships
starships={'Comet':{'TravelEnergy':0.95},'Nightmare':{'Evade':0.95},'Aurora':{'EnergyRegen':1.05},'Starlight':{'MaxEnergy':1.1},'Defender':{'DamageReduced':0.95}, 'Brilliance':{'Rare':1.1}, 'Destroyer':{'Damage':1.01}}

#Loot-table of zones

zone={'Alpha':{'common':['Space Rock'],'uncommon':['Iron','Silicon','Silicon'],'rare':['Gold'],'epic':['Diamond'],'legendary':['Diamond'],'mythical':['Stardust']},'Beta':{'common':['Space Rock','Ice'],'uncommon':['Iron','Iron', 'Silicon'],'rare':['Silver'],'epic':['Diamond'],'legendary':['Diamond'],'mythical':['Stardust']},'Wasteland':{'common':['Space Rock','Space Rock','Ice'],'uncommon':['Space Rock','Space Rock','Silicon'],'rare':['Iron'],'epic':['Silver'],'legendary':['Diamond'],'mythical':['Stardust']}, 'Sparkle':{'common':['Space Rock','Space Rock', 'Silicon'],'uncommon':['Silicon','Silicon','Iron'],'rare':['Iron','Iron','Silver'],'epic':['Silver','Silver','Silver','Gold'],'legendary':['Diamond','Diamond','Amethyst'],'mythical':['Stardust']},'Gamma':{'common':['Space Rock','Space Rock','Space Rock','Ice','Ice', 'Iron'],'uncommon':['Silver'],'rare':['Gold'],'epic':['Diamond'],'legendary':['Diamond','Diamond','Diamond','Titanium'],'mythical':['Stardust']},'Radiance':{'common':['Space Rock','Space Rock','Space Rock', 'Silicon'],'uncommon':['Iron'],'rare':['Gold'],'epic':['Diamond'],'legendary':['Diamond','Diamond','Diamond','Amethyst','Titanium','Uranium'],'mythical':['Stardust']}}

#The range of zones
zonevalue={'Alpha':10, 'Beta':30, 'Wasteland':100,'Sparkle':110,'Gamma':250,'Radiance':400, 'Void':750}
#The weight of events in each zone
zoneevents={'Alpha':[1,0.5,1], 'Beta':[1.5,1,1], 'Wasteland':[5,1,0.5], 'Sparkle':[1,3,2], 'Gamma':[3,2,1], 'Radiance':[1,0.5,3], 'Void':[2,0.5,1]}
#Material base factor of each starship
starshipUp={'Comet':{'Space Rock':25.4, 'Silicon':10.31, 'Iron':5.19, 'Ice':50.45, 'Silver':1.2, 'Gold':0.32, 'Diamond':0.12, 'Amethyst':0.03,'Stardust':0.01},'Aurora':{'Space Rock':25.12, 'Silicon':5.2, 'Iron':5.7, 'Silver':2.03, 'Gold':0.52, 'Diamond':0.19, 'Amethyst':0.06, 'Stardust':0.01},'Nightmare':{'Space Rock':30.21, 'Silicon':10.14, 'Iron':2.7, 'Silver':2.83, 'Gold':0.22, 'Diamond':0.183,'Titanium':0.017, 'Stardust':0.01},'Starlight':{'Space Rock':30.46, 'Silicon':20.34, 'Iron':5.7, 'Silver':1.11, 'Gold':0.41, 'Diamond':0.09,'Amethyst':0.014, 'Stardust':0.01},'Destroyer':{'Space Rock':25.44, 'Silicon':9.76, 'Iron':9.87, 'Silver':0.8, 'Diamond':0.17,'Amethyst':0.023,'Titanium':0.012, 'Stardust':0.01},'Defender':{'Space Rock':50.46, 'Silicon':5.24, 'Iron':9.87, 'Silver':0.92, 'Gold':0.28, 'Diamond':0.17,'Titanium':0.04, 'Stardust':0.01},'Brilliance':{'Space Rock':15.46, 'Silicon':15.24, 'Ice':5.41, 'Iron':4.87, 'Silver':1.08, 'Gold':0.58, 'Diamond':0.21,'Amethyst':0.02, 'Stardust':0.01}}
#Trade rates of each zone
trades={'Alpha':[['Space Rock','Silicon','Iron','Gold','Diamond'],[10,2,10,10],5],'Beta':[['Space Rock','Ice','Silicon','Iron','Silver','Diamond'],[2,5,2,5,20],7],'Wasteland':[['Space Rock','Ice','Silicon','Iron','Silver','Diamond'],[2,10,2,10,20],10],'Sparkle':[['Silicon','Iron','Silver','Gold','Diamond','Amethyst'],[2,5,2,7,2],10],'Gamma':[['Ice','Silicon','Iron','Silver','Gold','Diamond','Titanium'],[10,2,5,2,10,5],15],'Radiance':[['Silicon','Iron','Silver','Diamond','Titanium','Uranium'],[10,3,15,3,2],17],'Void':[['Space Rock','Iron','Silver','Diamond','Titanium'],[25,2,10,3],5]}

#Just the materials in the game
material_list=['Space Rock','Ice','Silicon','Iron', 'Silver', 'Gold','Diamond','Amethyst','Titanium','Uranium', 'Stardust']

#Crystal types and cost
crystals={'Rewind':['Spacetime'],'Freeze':['Spacetime'], 'Speedup':['Spacetime'],'Foresight':['Spacetime'],'Warp':['Spacetime'], 'Glitch':['Spacetime'],'Powered':['Energy'], 'Supercharged':['Energy'], 'Efficiency':['Energy'], 'Synchronized':['Energy', 'Special'], 'Stun':['Energy'], 'Uncertainty':['Energy'], 'Capacity':['Energy'], 'Unstable':['Energy'],'Duplicate':['Matter'], 'Simplify':['Matter'], 'Boosted':['Matter'], 'Reinforced':['Matter'], 'Unbreaking':['Matter', 'Special'], 'Complement':['Matter', 'Special'],' Crystallized':['Matter', 'Special']}

#Crate list
crates=['Rocky', 'Icy', 'Metallic', 'Shiny', 'Unbreakable', 'Radiant']

#Roman numberals
numerals=['0','I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X']