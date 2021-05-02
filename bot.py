import discord, os, json, datetime, random
from time import time
from platform import system
from math import *

# TODO LIST
# Ability to produce cocaine/meth...
# Sell the drugs (Qucksell + NPC + Player market)
# Police
# Player transfer items/money

# !!! Use .pop('key') !!!

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as ' + str(self.user))

    def nice_number(self, num):
        final = ""
        indx = 0
        for char in str(num)[::-1]:
            indx += 1
            if indx % 3 != 0:
                final += char
            else:
                final += char+" "
        final = final[::-1]
        if final.startswith(" "):
            final = final[1:]
        return final

    def startup(self):
        self.prefix = "."
        self.currency = "$"
        self.databasePath = os.path.join(os.getcwd(), "database.json")
        self.database = self.loadDB()
        self.fullName = {"pot":":potted_plant: Flower Pot", "led":":bulb: LED Lamp", "hid":":bulb: HID Lamp", "dryer":":control_knobs: Electric Dryer", "ruderalis":":seedling: Ruderalis seeds", "indica":":seedling: Indica seeds", "microscope":":microscope: Microscope", "meth":":cloud: Crystal Meth Powder", "cocaine":":cloud: Cocaine Powder", "heroin":":cloud: Heroin Powder", "amp":":cloud: Amphetamine Powder"}
        self.drugName = {"wetweed":":shamrock: Wet Weed", "weed":":herb: Weed", "meth":":cloud: Crystal Meth", "cocaine":":cloud: Cocaine", "heroin":":cloud: Herion", "amp":":cloud: Amphetamine"}
        self.description = {"pot":"A flower pot, used to grow weed. (id => `pot`)", "led":"Cheap and not power efficient lamp. (750W) (id => `led`)", "hid":"High quality and power efficient lamp. (500W) (id => `hid`)", "dryer":"A better way to dry weed, gives you 20% more weed. (id => `dryer`)", "ruderalis":"Avarage seeds, fast growth, 20g per plant. (id => `ruderalis`)", "indica":"Grat seeds, slow growth, 30g per plant. (id => `indica`)", "microscope":"Used to analyze drugs. (id => `microscope`)", "meth":"1g powder ==> 4g crystal meth (id => `meth`)", "cocaine":"1g powder ==> 3g cocaine (id => `cocaine`)", "heroin":"1g powder ==> 4g herion (id => `heroin`)", "amp":"1g powder ==> 5g amphetamine (id => `amp`/`amphetamine`)"}
        self.drugDescription = {"wetweed":"You need to dry wet weed to turn it into sellable weed", "weed":"The green stuff", "meth":"White powder with good effects", "cocaine":"The most expensive drug", "heroin":"The more serious drug", "amp":"So you wanna be fast?"}
        self.drugLvls = {"1":["weed", "amp"], "10":["lsd", "meth"], "25":["cocaine", "heroin"]}
        self.prices = {"pot":30, "led":150, "hid":1000, "dryer":2500, "ruderalis":12, "indica":20, "microscope":2000, "meth":30, "cocaine":50, "heroin":20, "amp":20}
        self.buildings = {
            "house":[
                {"type":"Small appartment", "name":"Starter appartment", "size":2, "electricity":0.4, "price":30000, "id":"smallappartment"},
                {"type":"Medium appartment", "name":"Friends place", "size":5, "electricity":0.35, "price":80000, "id":"mediumappartment"},
                {"type":"Large appartment", "name":"A more luxurious appartment", "size":10, "electricity":0.35, "price":150000, "id":"largeappartment"},
                {"type":"Small house", "name":"Grandma's small house", "size":25, "electricity":0.4, "price":200000, "id":"smallhouse"},
                {"type":"Medium house", "name":"Avarge house", "size":35, "electricity":0.35, "price":300000, "id":"mediumhouse"},
                {"type":"Large house", "name":"Nice and big house", "size":65, "electricity":0.3, "price":500000, "id":"largehouse"},
                {"type":"Medium mansion", "name":"A fucking mansion!", "size":80, "electricity":0.35, "price":1000000, "id":"mediummansion"},
                {"type":"Large mansion", "name":"Now this is just flex...", "size":110, "electricity":0.3, "price":2500000, "id":"largemansion"}],
            "warehouse":[
                {"type":"Mini warehouse", "name":"Friend's garage", "size":5, "electricity":0.2, "price":20000, "id":"miniwarehouse"},
                {"type":"Small warehouse", "name":"Abadoned warehouse", "size":20, "electricity":0.2, "price":100000, "id":"smallwarehouse"},
                {"type":"Medium warehouse", "name":"A regular warehouse", "size":100, "electricity":0.15, "price":750000, "id":"mediumwarehouse"},
                {"type":"Large warehouse", "name":"A nice big place to grow stuff", "size":250, "electricity":0.15, "price":1500000, "id":"largewarehouse"},
                {"type":"Mega warehouse", "name":"Now this is a warehouse!", "size":500, "electricity":0.15, "price":4000000, "id":"megawarehouse"}],
            "lab":[
                {"type":"Small lab", "name":"Friend's kitchen", "size":4, "electricity":0.35, "price":15000, "id":"smalllab"},
                {"type":"Medium lab", "name":"Normal chemical lab", "size":10, "electricity":0.3, "price":75000, "id":"mediumlab"},
                {"type":"Large lab", "name":"Modern lab", "size":25, "electricity":0.3, "price":250000, "id":"largelab"},
                {"type":"XL lab", "name":"This is sience!", "size":75, "electricity":0.25, "price":1000000, "id":"xllab"}]}
        self.starterHouse = self.buildings["house"][0]
        self.buildingDB = {}
        for buildingType in self.buildings:
            for building in self.buildings[buildingType]:
                building["btype"] = buildingType
                self.buildingDB[building["id"]] = building
        self.electricityMultiplayer = 1.5
        print("BOT IS READY")

    def loadDB(self):
        if not os.path.exists(self.databasePath):
            print("Database not found, creating a new one...")
            database = {"user":{}}
            f = open(self.databasePath, 'w')
            f.write(json.dumps(database, sort_keys=True, indent=4))
            f.close()
        else:
            f = open(self.databasePath, 'r')
            database = json.loads(f.read())
            f.close()
        return database

    def saveDB(self):
        f = open(self.databasePath, 'w')
        f.write(json.dumps(self.database, sort_keys=True, indent=4))
        f.close()

    async def on_message(self, message):
        if message.author == client.user:
            return
        if message.content.startswith(self.prefix):
            t = time()
            if str(message.author.id) not in self.database["user"]:
                await message.channel.send("Hey "+message.author.name+", I see that you are new aroud here. If you want to learn some tips and tricks check this out `"+self.prefix+"help`")
                self.database["user"][str(message.author.id)] = {"name":message.author.name, "balance":1000, "house":self.starterHouse, "warehouse":None, "lab":None, "upgrades":{"lab":None}, "inventory":{"items":{}, "drugs":{"pure":{}, "mixes":[]}}, "lvl":1, "job":None, "lastJob":0, "growing":[], "electricity":0, "lastBill":round(time())}
            if self.database["user"][str(message.author.id)]["lastBill"]+86400 < time():
                self.database["user"][str(message.author.id)]["balance"] -= self.database["user"][str(message.author.id)]["electricity"]*self.electricityMultiplayer
                self.database["user"][str(message.author.id)]["electricity"] = 0
                self.database["user"][str(message.author.id)]["lastBill"] = round(time())
            command = message.content.lower()[len(self.prefix):].split(" ")
            if command[0] == "ping":
                await command.channel.send("Pong!")
            elif command[0] == "help":
                if len(command) != 2:
                    embed = discord.Embed(title="Dark Dealer Help Menu", description="Here is a simple help menu", color=discord.Color.light_gray())
                    embed.add_field(name=":video_game: Basic game info", value="`"+self.prefix+"help info`", inline=True)
                    embed.add_field(name=":gear: List of commands", value="`"+self.prefix+"help commands`", inline=True)
                else:
                    if command[1] == "info":
                        embed = discord.Embed(title="Dark Dealer Info", description="Some informations about the game", color=discord.Color.light_gray())
                        embed.add_field(name=":satellite: Basic Info", value="This is a drug dealing game, you start by selling marijuana (weed) and amphetamine (speed), they both sell at 10$ per gram. There is a whole market changing the avarage value so it can change (not more than 2$ per gram)", inline=False)
                        embed.add_field(name=":electric_plug: Power", value="Yes, there is electricity in this game (you need to pay your bills). Some equipment (lamps, labs...) have a electricity consumption (in watts), you pay the bill automaticly each 24hours IRL. And yes you can go into negatives, so be careful how much money you have and what you can and cant afford...")
                        embed.add_field(name=":police_officer: Police", value="While trying to make deals and make as much profit as possible there are these stupid pigs, that want to put you behind bars, so be careful when selling with 'qucksell'. Also ist not recommended to live where you grow, you can be easly swatted and put behind bars. `What happens to you when the police catches you?` Its not as drastic as IRL, but you will get a cooldown depending on what type of drug you were selling/buing/producing and the amount, ex. if you grow around 100 grams of weed in your appartment and you get swatted, your coolding is going to be around 1day. Just dont live where you grow weed and you should be fine...", inline=False)
                        embed.add_field(name=":herb: Growing Weed", value="So the first step in making money, growing the green stuff. You can grow weed anywhere, but not in your lab. Each house/appartment/warehouse has a different size (capacity) of the amount of plants you can grow there, biger house => more plants => more money. Firstly you need a regular flower pot, its easy to get, but you need to buy it from the online weed shop, then you need to get a lamp (better lamp => less power cusumtion + faster weed growth) and you need to get the actual seeds (from the weed shop too), finaly you need to start growing them (this will take 1day and 6hours with the cheapest lighting). Be careful where you live and where you grow your weed, you attract more police attention and can be swatted anytime.", inline=False)
                        embed.add_field(name=":mag_right: Producing Powder Drugs", value="To produce powder drugs, firstly you need a lab starting from 15k. Then you need some powder to produce the drug from. Lastly you need to produce the drug this takes 2 IRL days without any upgrades. You can list all upgrades with the command `"+self.prefix+"upgrades <BUILDING>` then buy them with the command `"+self.prefix+"upgrade <BUILDING> <UPGRADE_LVL>`", inline=False)
                        embed.add_field(name=":dollar: Selling Drugs", value="So, selling the good stuff isn't that hard as it seems, BUT the police might be interested in participating in the deal aswell so be careful who and how you sell it to... There are 3 ways of selling drugs:\n 1. Qucksell - qucksell is the easiest and fastest method of selling drugs, but you dont make as much money here and also police are interested in investigating quicksells.\n 2. Market - On the market there are 2 ways of selling stuff: 1. Market making - you will create an player only or NPC only or both offer, it will take time before an NPC or an another player buys it (pricing will make a big difference here) 2. Market taking - You will see that some NPC's or other players are willing to buy a certain drug at certain price, you can easly fill the order and quckly finish the trade, but you will pay a 'Market taker fee' this is 5% of your profit, but there is NO police attetion when using the market.\n 3. Gang - Lastly selling to a gang is realy profitalbe sometimes, but realy risky...", inline=False)
                    elif command[1] in ["commands", "cmds"]:
                        embed = discord.Embed(title="Dark Dealer Commands", description="`balance`, `shops`, `shop`, `buy`, `market`", color=discord.Color.light_gray())
                        embed.set_footer(text="Use "+self.prefix+" before each command!")
                await message.channel.send(embed=embed)
            elif command[0] in ["balance", "bal", "money"]:
                user = str(message.author.id)
                name = message.author.name
                if len(command) == 2 and len(message.mentions) >= 1:
                    user = str(message.mentions[0].id)
                    name = message.mentions[0].name
                if user in self.database["user"]:
                    bal = self.nice_number(self.database["user"][user]["balance"])
                    if "." in bal:
                        bal = self.nice_number(int(bal.split(".")[0].replace(" ", "")))
                        self.database["user"][user]["balance"] = round(self.database["user"][user]["balance"])
                else:
                    bal = 0
                embed = discord.Embed(title=name+"'s balance", description="Balance: "+self.currency+" "+str(bal), color=discord.Color.green())
                await message.channel.send(embed=embed)
            elif command[0] in ["info", "profile"]:
                user = str(message.author.id)
                name = message.author.name
                avatar = message.author.avatar_url
                if len(command) == 2 and len(message.mentions) >= 1:
                    if str(message.mentions[0].id) in self.database["user"]:
                        user = str(message.mentions[0].id)
                        name = message.mentions[0].name
                        avatar = message.mentions[0].avatar_url
                embed = discord.Embed(color=discord.Color.blue())
                embed.set_author(name=name+"'s profile", icon_url=str(avatar).replace("size=1024", "size=256"))
                embed.add_field(name='Level', value=str(self.database["user"][user]["lvl"]), inline=True)
                embed.add_field(name='Balance', value=self.currency+" "+self.nice_number(self.database["user"][user]["balance"]), inline=True)
                embed.add_field(name='Inventory', value="Player has `"+str(len(self.database["user"][user]["inventory"]["items"]))+"` different items in his inventory", inline=False)
                if self.database["user"][user]["job"] != None:
                    embed.add_field(name='Employment', value="Player is working as a "+str(self.database["user"][user]["job"]), inline=False)
                await message.channel.send(embed=embed)
            elif command[0] in ["jobs", "joblist"]:
                embed = discord.Embed(title="Job List", color=discord.Color.blue())
                embed.add_field(name=':window: Window Cleaner', value="500 "+self.currency+" per clean | cooldown: 8hours (id => `windowcleaner`)", inline=False)
                embed.add_field(name=':desktop: YouTuber', value="400 "+self.currency+" per video | cooldown: 6hours (id => `youtuber`)", inline=False)
                embed.set_footer(text="You can apply to a job with the command `"+self.prefix+"job <JOB_ID>`")
                await message.channel.send(embed=embed)
            elif command[0] == "job":
                if len(command) != 2:
                    await message.channel.send("Please use => `"+self.prefix+"job <JOB_ID>`")
                elif command[1] == "unemploy":
                    if self.database["user"][str(message.author.id)]["job"] != None:
                        self.database["user"][str(message.author.id)]["job"] = None
                        self.database["user"][str(message.author.id)]["lastJob"] = 0
                        await message.channel.send("You are not employed anymore")
                    else:
                        await message.channel.send("You are not employed")
                elif self.database["user"][str(message.author.id)]["job"] != None:
                    await message.channel.send("You are already working as a "+self.database["user"][str(message.author.id)]["job"]+", use `"+self.prefix+"job unemploy` to leave your current job")
                else:
                    if command[1] in ["windowcleaner", "youtuber"]:
                        self.database["user"][str(message.author.id)]["job"] = command[1]
                        self.database["user"][str(message.author.id)]["lastJob"] = time()
                        await message.channel.send("You are now working as a "+command[1])
                    else:
                        await message.channel.send("Job with ID `"+command[1]+"` does not exist, use `"+self.prefix+"jobs` to list all available jobs and their IDs")
            elif command[0] == "work":
                job = self.database["user"][str(message.author.id)]["job"]
                if job != None:
                    if job == "youtuber":
                        reward = 400
                        cooldown = 21600
                    elif job == "windowcleaner":
                        reward = 500
                        cooldown = 28800
                    if self.database["user"][str(message.author.id)]["lastJob"]+cooldown < time():
                        await message.channel.send(message.author.mention+" You have worked your shift and you earned "+self.nice_number(reward)+" "+self.currency)
                        self.database["user"][str(message.author.id)]["balance"] += reward
                        self.database["user"][str(message.author.id)]["lastJob"] = time()
                    else:
                        remaining = str(datetime.timedelta(seconds=round((self.database["user"][str(message.author.id)]["lastJob"]+cooldown)-time()))).split(":")
                        for i in range(len(remaining)):
                            if remaining[i].startswith("0") and len(remaining[i]) != 1:
                                remaining[i] = remaining[i][1:]
                        await message.channel.send(message.author.mention+" You have to wait **"+remaining[0]+" hours "+remaining[1]+" minutes "+remaining[2]+" seconds"+"** before you can work")
                else:
                    await message.channel.send(message.author.mention+" You are not employed, you can employ using `"+self.prefix+"job <JOB_ID>`")
            elif command[0] == "shops":
                embed = discord.Embed(title="Shop List", color=discord.Color.dark_grey())
                embed.add_field(name=":potted_plant: Smoky", value="Everyting that your weed growing needs. (id => `smoky`/`weed`)", inline=False)
                embed.add_field(name=":scientist: Science Needs", value="We sell high quality lab equpment. (id => `science`/`lab`)", inline=False)
                embed.add_field(name=":mag_right: Power of Powder", value="We sell powder that can be turned into large amounts of powder drugs. (id => `powder`)", inline=False)
                embed.add_field(name=":house: PrimeLocation", value="We sell great appartments, warehouses, labs... (id => `location`/`buildings`/`properties`)", inline=False)
                embed.set_footer(text="You can visit any shop with "+self.prefix+"shop <SHOP_ID>")
                await message.channel.send(embed=embed)
            elif command[0] == "shop":
                if len(command) == 2 or len(command) == 3:
                    if command[1] in ["smoky", "weed"]:
                        embed = discord.Embed(title=":potted_plant: Smoky", color=discord.Color.green())
                        embed.set_thumbnail(url="https://image.freepik.com/free-vector/green-neon-sign-marijuana-leaves-cannabis-logo_1268-14217.jpg")
                        embed.add_field(name=":seedling: Ruderalis seeds - "+str(self.prices["ruderalis"])+" "+self.currency, value="Avarage seeds, fast growth, 20g per plant. (id => `ruderalis`)", inline=False)
                        embed.add_field(name=":seedling: Indica seeds - "+str(self.prices["indica"])+" "+self.currency, value="Grat seeds, slow growth, 30g per plant. (id => `indica`)", inline=False)
                        embed.add_field(name=":potted_plant: Flower Pot - "+str(self.prices["pot"])+" "+self.currency, value="Needed to grow weed. (id => `pot`)", inline=False)
                        embed.add_field(name=":bulb: LED Lamp - "+str(self.prices["led"])+" "+self.currency, value="Cheap and not power efficient lamp. (750W) (id => `led`)", inline=False)
                        embed.add_field(name=":bulb: HID Lamp - "+str(self.prices["hid"])+" "+self.currency, value="High quality and power efficient lamp. (500W) (id => `hid`)", inline=False)
                        embed.add_field(name=":control_knobs: Electric Dryer - "+str(self.prices["dryer"])+" "+self.currency, value="A better way to dry weed, gives you 20% more weed (id => `dryer`)", inline=False)
                        embed.set_footer(text="You can buy stuff with "+self.prefix+"buy <ITEM_ID>")
                        await message.channel.send(embed=embed)
                    elif command[1] in ["science", "lab"]:
                        embed = discord.Embed(title=":scientist: Science Needs", color=discord.Color.blue())
                        embed.set_thumbnail(url="https://static.wixstatic.com/media/975a90_19cac9b1df2c4257a14a33569f274dea~mv2.png/v1/fill/w_164,h_190,al_c,q_85,usm_0.66_1.00_0.01/975a90_19cac9b1df2c4257a14a33569f274dea~mv2.webp")
                        embed.add_field(name=":microscope: Microscope - "+str(self.prices["microscope"])+" "+self.currency, value="Used to analyze drugs. (id => `microscope`)", inline=False)
                        embed.set_footer(text="You can buy stuff with "+self.prefix+"buy <ITEM_ID>")
                        await message.channel.send(embed=embed)
                    elif command[1] == "powder":
                        embed = discord.Embed(title=":mag_right: Power of Powder", description="You need a lab to turn powder to the real drug.", color=discord.Color.dark_gray())
                        embed.set_thumbnail(url="https://media.istockphoto.com/vectors/explosion-of-blue-powder-vector-id1081303692?k=6&m=1081303692&s=612x612&w=0&h=qv00YeAwnCRs6_Z4HfRf7IbWlJ6yZgt9xYbBWb0fnpE=")
                        embed.add_field(name=":cloud: Cocaine Powder - "+str(self.prices["cocaine"])+" "+self.currency, value="1g powder ==> 3g cocaine (id => `cocaine`)", inline=False)
                        embed.add_field(name=":cloud: Crystal Meth Powder - "+str(self.prices["meth"])+" "+self.currency, value="1g powder ==> 4g crystal meth (id => `meth`)", inline=False)
                        embed.add_field(name=":cloud: Amphetamine Powder - "+str(self.prices["amp"])+" "+self.currency, value="1g powder ==> 5g amphetamine (id => `amp`/`amphetamine`)", inline=False)
                        embed.add_field(name=":cloud: Heroin Powder - "+str(self.prices["pot"])+" "+self.currency, value="1g powder ==> 4g herion (id => `heroin`)", inline=False)
                        embed.set_footer(text="You can buy stuff with "+self.prefix+"buy <ITEM_ID> <AMOUNT (optional)>")
                        await message.channel.send(embed=embed)
                    elif command[1] in ["location", "building", "buildings", "houses", "properties", "property", "prime", "primelocation"]:
                        embed = discord.Embed(title=":house: PrimeLocation", color=discord.Color.gold())
                        embed.set_thumbnail(url="https://media.istockphoto.com/vectors/house-abstract-sign-design-vector-linear-style-vector-id1131184921?k=6&m=1131184921&s=612x612&w=0&h=X5MCxDEER4QrVvE2olwd-ZZuVAa-NFKzKGRgupestQ8=")
                        if len(command) <= 2:
                            embed.description = "Welcome to PrimeLocation, please use `"+self.prefix+"shop primelocation <BUILDING_TYPE>` a building type is a `house`/`warehouse`/`lab`\n\n\nTip: you don't need to use the whole `primelocation` thing, you can just use `prime` or `houses`..."
                        else:
                            if command[2] in ["house", "houses", "appartment", "appartments"]:
                                for building in self.buildings["house"]:
                                    embed.add_field(name=":house: **"+building["type"]+"**", value=building["name"]+" (id => `"+building["id"]+"`)\nElectricity: "+str(building["electricity"])+" "+self.currency+" | Grow space: "+str(building["size"])+" plants | Price: "+self.nice_number(building["price"])+" "+self.currency, inline=False)
                            elif command[2] in ["warehouse", "warehouses"]:
                                for building in self.buildings["warehouse"]:
                                    embed.add_field(name=":hotel: **"+building["type"]+"**", value=building["name"]+" (id => `"+building["id"]+"`)\nElectricity: "+str(building["electricity"])+" "+self.currency+" | Grow space: "+str(building["size"])+" plants | Price: "+self.nice_number(building["price"])+" "+self.currency, inline=False)
                            elif command[2] in ["lab", "labs", "laboratory", "laboratories"]:
                                for building in self.buildings["lab"]:
                                    embed.add_field(name=":microscope: **"+building["type"]+"**", value=building["name"]+" (id => `"+building["id"]+"`)\nElectricity: "+str(building["electricity"])+" "+self.currency+" | Production capacity: "+str(building["size"])+" | Price: "+self.nice_number(building["price"])+" "+self.currency, inline=False)
                        embed.set_footer(text="You can buy a building with "+self.prefix+"buy <BUILDING_ID>")
                        await message.channel.send(embed=embed)
                    else:
                        await message.channel.send(message.author.mention+" There is no shop with that ID, use `"+self.prefix+"shops` to view all available shops")
                else:
                    await message.channel.send(message.author.mention+" Please use `"+self.prefix+"shop <SHOP_ID>` or use `"+self.prefix+"shops` to view all available shops")
            elif command[0] == "buy":
                if len(command) < 2 or len(command) > 3:
                    await message.channel.send(message.author.mention+" Please use `"+self.prefix+"buy <ITEM_ID> <AMOUNT (optional)>`")
                else:
                    user = str(message.author.id)
                    if command[1] in self.prices:
                        if self.database["user"][user]["lvl"] < 10:
                            if command[1] in self.drugLvls["10"]:
                                await message.channel.send(message.author.mention+" You need lvl 10+ to unlock "+command[1])
                                return
                            elif command[1] in self.drugLvls["25"]:
                                await message.channel.send(message.author.mention+" You need lvl 25+ to unlock "+command[1])
                                return
                        elif self.database["user"][user]["lvl"] < 25:
                            if command[1] in self.drugLvls["25"]:
                                await message.channel.send(message.author.mention+" You need lvl 25+ to unlock "+command[1])
                                return
                        price = self.prices[command[1]]
                        amount = 1
                        if len(command) == 3:
                            try:
                                amount = int(command[2])
                            except:
                                await message.channel.send(message.author.mention+" Please specify a valid amount `"+self.prefix+"buy <ITEM_ID> <AMOUNT (optional)>`")
                                return
                            price = self.prices[command[1]]*amount
                        if self.database["user"][user]["balance"]-price >= 0:
                            self.database["user"][user]["balance"] -= price
                            if command[1] not in self.database["user"][user]["inventory"]["items"]:
                                self.database["user"][user]["inventory"]["items"][command[1]] = amount
                            else:
                                self.database["user"][user]["inventory"]["items"][command[1]] += amount
                            await message.channel.send(message.author.mention+" You bought **"+str(amount)+"x "+command[1]+"**")
                        else:
                            await message.channel.send(message.author.mention+" You can't afford to buy that :joy:")
                    elif command[1] in self.buildingDB:
                        building = self.buildingDB[command[1]]
                        if self.database["user"][user]["balance"]-building["price"] >= 0:
                            self.database["user"][user]["balance"] -= building["price"]
                            self.database["user"][user][building["btype"]] = building
                            await message.channel.send(message.author.mention+" You got yourself a new "+building["btype"]+"!")
                        else:
                            await message.channel.send(message.author.mention+" You can't afford to buy that :joy:")
                    else:
                        await message.channel.send(message.author.mention+" That item/building does not exist, use `.shop <SHOP_ID>` to see all available items and buildings")
            elif command[0] in ["inv", "inventory", "items"]:
                user = str(message.author.id)
                name = message.author.name
                page = 1
                if len(message.mentions) > 0:
                    user = str(message.mention[0].id)
                    name = message.mentions[0].name
                    if len(command) > 2:
                        try:
                            page = int(command[2])
                        except:
                            page = 1
                elif len(command) > 1:
                    try:
                        page = int(command[1])
                    except:
                        page = 1
                pages = [[]]
                if len(self.database["user"][user]["inventory"]["items"]) > 0:
                    for item in self.database["user"][user]["inventory"]["items"]:
                        if len(pages[-1]) < 5:
                            pages[-1].append(("**"+self.fullName[item]+"** ─ "+str(self.database["user"][user]["inventory"]["items"][item]), self.description[item]))
                        else:
                            pages.append([("**"+self.fullName[item]+"** ─ "+str(self.database["user"][user]["inventory"]["items"][item]), self.description[item])])
                if page > len(pages):
                    await message.channel.send(message.author.mention+" Sorry, but you only have `"+str(len(pages))+"` pages")
                elif pages[page-1] == []:
                    await message.channel.send(message.author.mention+" Your inventory is empty")
                else:
                    embed = discord.Embed(title=name+"'s Inventory", color=discord.Color.blue())
                    for item in pages[page-1]:
                        embed.add_field(name=item[0], value=item[1], inline=False)
                    await message.channel.send(embed=embed)
            elif command[0] in ["drugs", "druglist"]: # TODO Mixes
                user = str(message.author.id)
                name = message.author.name
                page = 1
                if len(message.mentions) > 0:
                    user = str(message.mention[0].id)
                    name = message.mentions[0].name
                    if len(command) > 2:
                        try:
                            page = int(command[2])
                        except:
                            page = 1
                elif len(command) > 1:
                    try:
                        page = int(command[1])
                    except:
                        page = 1
                pages = [[]]
                if len(self.database["user"][user]["inventory"]["drugs"]["pure"]) > 0:
                    for drug in self.database["user"][user]["inventory"]["drugs"]["pure"]:
                        if len(pages[-1]) < 5:
                            pages[-1].append(("**"+self.drugName[drug]+"** ─ "+str(self.database["user"][user]["inventory"]["drugs"]["pure"][drug])+" grams", self.drugDescription[drug]))
                        else:
                            pages.append([("**"+self.drugName[drug]+"** ─ "+str(self.database["user"][user]["inventory"]["drugs"]["pure"][drug])+" grams", self.drugDescription[drug])])
                if len(self.database["user"][user]["inventory"]["drugs"]["mixes"]) > 0:
                    for drug in self.database["user"][user]["inventory"]["drugs"]["mixes"]:
                        if len(pages[-1]) < 5:
                            pages[-1].append(("**"+self.drugName[drug]+"** ─ "+str(self.database["user"][user]["inventory"]["drugs"]["mixes"][drug])+" grams", self.drugDescription[drug]))
                        else:
                            pages.append([("**"+self.fuldrugNamelName[drug]+"** ─ "+str(self.database["user"][user]["inventory"]["drugs"]["mixes"][drug])+" grams", self.drugDescription[drug])])
                if page > len(pages):
                    await message.channel.send(message.author.mention+" Sorry, but you only have `"+str(len(pages))+"` pages")
                elif pages[page-1] == []:
                    await message.channel.send(message.author.mention+" Your drug inventory is empty")
                else:
                    embed = discord.Embed(title=name+"'s Drugs", color=discord.Color.red())
                    for drug in pages[page-1]:
                        embed.add_field(name=drug[0], value=drug[1], inline=False)
                    await message.channel.send(embed=embed)
            elif command[0] in ["buildings", "houses", "houselist", "homelist"]:
                user = str(message.author.id)
                name = str(message.author.name)
                if len(message.mentions) > 0:
                    user = str(message.mentions[0].id)
                    name = str(message.mentions[0].name)
                embed = discord.Embed(title=name+"'s Buildings", description="List of owned buildings", color=discord.Color.gold())
                if self.database["user"][user]["house"] != None:
                    building = self.database["user"][user]["house"]
                    embed.add_field(name=":house: House: **"+building["type"]+"**", value=building["name"]+"\nElectricity: "+str(building["electricity"])+" "+self.currency+" | Grow space: "+str(building["size"])+" plants | Price: "+self.nice_number(building["price"])+" "+self.currency, inline=False)
                if self.database["user"][user]["warehouse"] != None:
                    building = self.database["user"][user]["warehouse"]
                    embed.add_field(name=":hotel: Warehouse: **"+building["type"]+"**", value=building["name"]+"\nElectricity: "+str(building["electricity"])+" "+self.currency+" | Grow space: "+str(building["size"])+" plants | Price: "+self.nice_number(building["price"])+" "+self.currency, inline=False)
                if self.database["user"][user]["lab"] != None:
                    building = self.database["user"][user]["lab"]
                    embed.add_field(name=":microscope: Lab: **"+building["type"]+"**", value=building["name"]+"\nElectricity: "+str(building["electricity"])+" "+self.currency+" | Production capacity: "+str(building["size"])+" | Price: "+self.nice_number(building["price"])+" "+self.currency, inline=False)
                await message.channel.send(embed=embed)
            elif command[0] == "grow":
                user = str(message.author.id)
                name = str(message.author.name)
                target = 1
                if len(message.mentions) > 0:
                    user = str(message.mentions[0].id)
                    name = str(message.mentions[0].name)
                    target = 2
                if (len(command) >= 3 and len(message.mentions) > 0) or (len(command) >= 2 and len(message.mentions) == 0):
                    embed = discord.Embed(title="Grow Menu", color=discord.Color.green())
                    embed.set_thumbnail(url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fpsdlearning.com%2Fwp-content%2Fuploads%2F2017%2F09%2FCannabis-logo.jpg&f=1&nofb=1")
                    if command[target] == "info":
                        capacity = self.database["user"][user]["house"]["size"]
                        if self.database["user"][user]["warehouse"] != None:
                            capacity += self.database["user"][user]["warehouse"]["size"]
                        growing, grown = 0, 0
                        topTime = 0
                        for plant in self.database["user"][user]["growing"]:
                            if plant["growTime"] < time():
                                grown += 1
                            else:
                                if plant["growTime"] < topTime or (topTime == 0 and time() < plant["growTime"]):
                                    topTime = plant["growTime"]
                                growing += 1
                        destTime = 0
                        if topTime != 0:
                            destTime = topTime-time()
                        remaining = str(datetime.timedelta(seconds=round(destTime))).split(":")
                        for i in range(len(remaining)):
                            if remaining[i].startswith("0") and len(remaining[i]) != 1:
                                remaining[i] = remaining[i][1:]
                        embed.add_field(name=":potted_plant: **Currently Growing**", value="Growing `"+str(growing)+"` out of `"+str(capacity)+"` plants", inline=False)
                        embed.add_field(name=":potted_plant: **Top Growing**", value="You need to wait about "+remaining[0]+" hours and "+remaining[1]+" minutes before your next plant grows", inline=False)
                        embed.add_field(name=":potted_plant: **Harvestable**", value="There are `"+str(grown)+"` harvestable plants", inline=False)
                        await message.channel.send(embed=embed)
                    elif command[target] == "grow":
                        if len(command) == target+3 or len(command) == target+4:
                            amount = 1
                            if len(command) == target+4:
                                try:
                                    amount = int(command[target+3])
                                except:
                                    await message.channel.send(message.author.mention+" That's not a valid number")
                                    return
                            if command[target+1] in ["ruderalis", "indica"]:
                                if command[target+2] in ["house", "warehouse"]:
                                    if self.database["user"][user][command[target+2]] != None:
                                        capacity = self.database["user"][user][command[target+2]]["size"]
                                        if capacity-len(self.database["user"][user]["growing"]) >= amount:
                                            lamps = []
                                            lamp = None
                                            pots = 0
                                            pot = False
                                            for plant in self.database["user"][user]["growing"]:
                                                lamps.append(plant["lamp"])
                                                pots += 1
                                            if "hid" in self.database["user"][user]["inventory"]["items"]:
                                                if self.database["user"][user]["inventory"]["items"]["hid"] > lamps.count("hid"):
                                                    lamp = "hid"
                                            if lamp == None:
                                                if "led" in self.database["user"][user]["inventory"]["items"]:
                                                    if self.database["user"][user]["inventory"]["items"]["led"] > lamps.count("led"):
                                                        lamp = "led"
                                            if "pot" in self.database["user"][user]["inventory"]["items"]:
                                                if self.database["user"][user]["inventory"]["items"]["pot"] > pots:
                                                    pot = True
                                            if lamp != None:
                                                if pot:
                                                    speed = 1
                                                    watts = 1000
                                                    seedTime = 108000
                                                    if lamp == "hid":
                                                        speed = 1.5
                                                        watts = 400
                                                    if command[target+1] == "ruderalis":
                                                        seedTime = 72000
                                                    growTime = seedTime/speed
                                                    self.database["user"][user]["growing"].append({"seeds":command[target+1], "growTime":round(time()+growTime)})
                                                    self.database["user"][user]["electricity"] += round((watts/1000)*(growTime/60/60))
                                                    remaining = str(datetime.timedelta(seconds=growTime)).split(":")
                                                    for i in range(len(remaining)):
                                                        if remaining[i].startswith("0") and len(remaining[i]) != 1:
                                                            remaining[i] = remaining[i][1:]
                                                    await message.channel.send(message.author.mention+" You planted a "+command[target+1]+" seed with a "+lamp+" lamp, it will take **"+remaining[0]+" hours "+remaining[1]+" minutes** to grow")
                                                else:
                                                    await message.channel.send(message.author.mention+" You don't have enough pots to grow more weed")
                                            else:
                                                await message.channel.send(message.author.mention+" You don't have enough lamps to grow more weed")
                                        else:
                                            await message.channel.send(message.author.mention+" You don't have enough space to grow more weed")
                                    else:
                                        await message.channel.send(message.author.mention+" You don't own a "+command[target+2])
                                else:
                                    await message.channel.send(message.author.mention+" Please specify a valid place to grow the weed in (`house`/`warehouse`)")
                            else:
                                await message.channel.send(message.author.mention+" There are no seeds named `"+command[target+1]+"`")
                        else:
                            await message.channel.send(message.author.mention+" Please use `"+self.prefix+"grow grow <SEED_ID> <HOUSE/WAREHOUSE> <AMOUNT (optional)>`")
                    elif command[target] == "harvest":
                        user = str(message.author.id)
                        name = str(message.author.name)
                        packageSize = 0
                        collectedPlants = []
                        for plant in self.database["user"][user]["growing"]:
                            if plant["growTime"] < time():
                                if plant["seeds"] == "indica":
                                    packageSize += 30
                                else:
                                    packageSize += 20
                                collectedPlants.append(plant)
                        for plant in collectedPlants:
                            del self.database["user"][user]["growing"][self.database["user"][user]["growing"].index(plant)]
                        if packageSize > 0:
                            if "weed" in self.database["user"][user]["inventory"]["drugs"]["pure"]:
                                self.database["user"][user]["inventory"]["drugs"]["pure"]["wetweed"] += packageSize
                            else:
                                self.database["user"][user]["inventory"]["drugs"]["pure"]["wetweed"] = packageSize
                            await message.channel.send(message.author.mention+" You collected "+str(packageSize)+" grams of wet weed")
                        else:
                            await message.channel.send(message.author.mention+" Your weed hasn't fully grown yet")
                    elif command[target] == "dry":
                        dryer = False
                        if "dryer" in self.database["user"][user]["inventory"]["items"]:
                            if self.database["user"][user]["inventory"]["items"]["dryer"] > 0:
                                dryer = True
                        if "wetweed" in self.database["user"][user]["inventory"]["drugs"]["pure"]:
                            if self.database["user"][user]["inventory"]["drugs"]["pure"]["wetweed"] > 0:
                                weed = self.database["user"][user]["inventory"]["drugs"]["pure"]["wetweed"]
                                base = self.database["user"][user]["inventory"]["drugs"]["pure"]["wetweed"]
                                bonus = 0
                                if dryer:
                                    self.database["user"][user]["electricity"] += 10
                                    bonus = round(weed/5)
                                    weed += bonus
                                if "weed" in self.database["user"][user]["inventory"]["drugs"]["pure"]:
                                    self.database["user"][user]["inventory"]["drugs"]["pure"]["weed"] += weed
                                else:
                                    self.database["user"][user]["inventory"]["drugs"]["pure"]["weed"] = weed
                                self.database["user"][user]["inventory"]["drugs"]["pure"].pop("wetweed")
                                await message.channel.send(message.author.mention+" You dryed `"+str(base)+"` grams of weed into `"+str(weed)+"` grams with `"+str(bonus)+"` bonus grams (dryer)")
                            else:
                                await message.channel.send(message.channel.mention+" You don't have any wet weed to dry")
                        else:
                            await message.channel.send(message.channel.mention+" You don't have any wet weed to dry")
                    else:
                        await message.channel.send(message.author.mention+" Please use `"+self.prefix+"grow <@USER (optional)> <ACTION>`\nGrow actions: *info*/*grow*/*harvest*/*dry*")
                else:
                    await message.channel.send(message.author.mention+" Please use `"+self.prefix+"grow <@USER (optional)> <ACTION>`\nGrow actions: *info*/*grow*/*harvest*/*dry*")
            elif command[0] in ["electricity", "bill", "bills", "tax", "taxes", "elec"]:
                user = str(message.author.id)
                name = str(message.author.name)
                if len(message.mentions) > 0:
                    user = str(message.mentions[0].id)
                    name = str(message.mentions[0].name)
                remaining = str(datetime.timedelta(seconds=(self.database["user"][user]["lastBill"]+86400)-round(time()))).split(":")
                for i in range(len(remaining)):
                    if remaining[i].startswith("0") and len(remaining[i]) != 1:
                        remaining[i] = remaining[i][1:]
                embed = discord.Embed(title=name+"'s Electricity Bills", description="Next bill will be automaticly payed in "+remaining[0]+" hours "+remaining[1]+" minutes", color=discord.Color.from_rgb(93, 109, 126))
                embed.add_field(name=":electric_plug: Estimated Payment", value=self.nice_number(round(self.database["user"][user]["electricity"]*self.electricityMultiplayer))+" "+self.currency)
                await message.channel.send(embed=embed)
            elif command[0] == "levelup":
                user = str(message.author.id)
                if len(command) == 2:
                    if command[1] == "confirm":
                        cost = 2000*self.database["user"][user]["lvl"]*self.database["user"][user]["lvl"]
                        if self.database["user"][user]["balance"]-cost > 0:
                            self.database["user"][user]["balance"] -= cost
                            self.database["user"][user]["lvl"] += 1
                            await message.channel.send(message.author.mention+" You are now lvl "+self.database["user"][user]["lvl"])
                        else:
                            await message.channel.send(message.author.mention+" You need `"+str(0-(self.database["user"][user]["balance"]-cost))+" "+self.currency+"` more to level up")
                else:
                    embed = discord.Embed(title="Level "+str(self.database["user"][user]["lvl"]+1)+" Requirements", color=discord.Color.blue())
                    embed.add_field(name="**Current Level**", value="You are currently level "+str(self.database["user"][user]["lvl"]), inline=False)
                    embed.add_field(name="**Level Up**", value="You need `"+str(2000*self.database["user"][user]["lvl"]*self.database["user"][user]["lvl"])+" "+self.currency+"`", inline=False)
                    embed.add_field(name="**Confirm Level Up**", value="Use `"+self.prefix+"levelup confirm` to confirm your level up", inline=False)
                    await message.channel.send(embed=embed)
            elif command[0] in ["prod", "produce", "lab"]:
                pass

if __name__ == "__main__":
    client = MyClient()
    client.startup()
    token = ""
    if token == "":
        if str(system()).lower() == "windows":
            path = "C:\\Users\\lukas\\Documents\\PythonStuff\\Discord\\darkDealerToken.tk"
        else:
            path = "/Library/DarkDealer/token.tk"
        f = open(path, 'r')
        token = f.read()
        f.close()
    client.run(token, bot=True)
    client.saveDB()