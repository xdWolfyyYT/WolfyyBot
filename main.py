import discord
from discord.ext import commands
import random
import json
import os
import praw
import datetime
import time
import asyncio
from discord.utils import get
import youtube_dl


rps_choices = [1,2,3]

TOKEN = 'NzM5ODc0OTkyMDM2MjQ5NzMx.Xyg0SA.sDN3TEbBfQKDM8MzypS3PFg0d-o'
BOT_PREFIX = 'w!'

bot = commands.Bot(command_prefix=BOT_PREFIX)

client = commands.Bot(command_prefix="w!")

@client.event
async def on_ready():
	await client.change_presence(status = discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name = 'Prefix: w! | Moderating'))
	print("Wolfyy Bot is Online and Ready!")


@client.command()
async def balance(ctx):
    await open_account(ctx.author)
    users = await get_bank_data()
    user = ctx.author
    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]['bank']

    embed = discord.Embed(title = f"{ctx.author.name}'s balance", color = discord.Colour.from_rgb(54, 151, 255))
    embed.add_field(name = "Wallet balance", value = wallet_amt, inline = False)
    embed.add_field(name = "Bank balance", value = bank_amt, inline = False)
    await ctx.send(embed = embed)

async def open_account(user):

    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users [str(user.id)]["bank"] = 0
    
    with open("mainbank.json", "w") as f:
        json.dump(users,f)
    return True

async def get_bank_data():
    with open("mainbank.json", "r+") as f:
        users = json.load(f)
    return users

async def update_bank(user,change = 0,mode = "wallet"):
    users = await get_bank_data()

    users[str(user.id)][mode] += change

    with open("mainbank.json","w") as f:
        json.dump(users, f)

    bal = [users[str(user.id)]["wallet"],users[str(user.id)]["bank"]]
    return bal

@client.command()
async def withdraw(ctx,amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("**Please enter the amount to withdraw**")
        return
    
    bal = await update_bank(ctx.author)
    amount = int(amount)
    if amount>bal[1]:
        await ctx.send("**You don't have that much money!**")
        return
    if amount<0:
        await ctx.send('**Amount must be positive!**')
        return
    await update_bank(ctx.author,amount)
    await update_bank(ctx.author,-1*amount,"bank")
    await ctx.send(f"**You withdrew** {amount} **coins!**")

@client.command()
async def deposit(ctx,amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("**Please enter the amount to withdraw**")
        return

    bal = await update_bank(ctx.author)
    amount = int(amount)
    if amount>bal[1]:
        await ctx.send("**You don't have that much money!**")
        return
    if amount<0:
        await ctx.send('**Amount must be positive!**')
        return
    await update_bank(ctx.author,-1*amount)
    await update_bank(ctx.author,amount,"bank")
    await ctx.send(f"**You deposited** {amount} **coins!**")
    
@client.command()
async def send(ctx,member: discord.Member, amount = None):
    await open_account(ctx.author)
    await open_account(member)
    
    if amount == None:
        await ctx.send("**Please enter the amount to withdraw**")
        return

    bal = await update_bank(ctx.author)
    amount = int(amount)
    if amount>bal[0]:
        await ctx.send("**You don't have that much money!**")
        return
    if amount<0:
        await ctx.send('**Amount must be positive!**')
        return
    await update_bank(ctx.author,-1*amount, "bank")
    await update_bank(member,amount,"bank")
    await ctx.send(f"**You gave** {amount} **coins!**")


@client.command()
async def rob(ctx,member: discord.Member):
    await open_account(ctx.author)
    await open_account(member)

    bal = await update_bank(member)
    if bal[0]<100:
        await ctx.send("**It's not worth it!**")
        return

    earnings = random.randrange(0,bal[0])

    
    await update_bank(ctx.author,earnings)
    await update_bank(member,-1*earnings)
    await ctx.send(f"**You robbed and got** {earnings} **coins!**")

@client.command()
async def beg(ctx):
    await open_account(ctx.author)
    users = await get_bank_data()
    user = ctx.author
    earnings = random.randrange(101)

    await ctx.send(f"**Someone gave you** {earnings} **coins!**")

    users[str(user.id)]["wallet"] += earnings

    with open("mainbank.json","w") as f:
        json.dump(users,f)

reddit = praw.Reddit(client_id = 'nj9jdtBkdsZzNA',
                     client_secret = 'wGwIROgQVC1NSFb-_AjC4iQOZ5E',
                     user_agent = 'Windows 10:Wolfyy:v1.0.0 by /u/Cheezy_Nachos and /u/xdWolfyy_YT')

@client.command()
async def memes(ctx):
    sb = reddit.subreddit('memes').hot()
    post = random.randint(1,100)
    for i in range(0, post):
        submission = next(x for x in sb if not x.stickied)
    time_created = datetime.datetime.fromtimestamp(submission.created)
    embed = discord.Embed(title = submission.title,description = '**Posted by:** \n /u/' + str(submission.author) + '\n**Posted At:** \n' + str(time_created) + ' **UTC**', colour = discord.Colour.from_rgb(34, 137, 240))
    embed.set_image(url = submission.url)
    await ctx.send(embed = embed)
    
@client.command()
async def tihi(ctx):
    subreddit = reddit.subreddit('TIHI').hot()
    post = random.randint(1,100)
    for i in range(0, post):
        submission = next(x for x in subreddit if not x.stickied)
    time_created = datetime.datetime.fromtimestamp(submission.created)
    embed = discord.Embed(title = submission.title,description = '**Post by:** \n /u/' + str(submission.author) + '\n**Posted At:** \n' + str(time_created) + ' **UTC**', colour = discord.Colour.from_rgb(34, 137, 240))
    embed.set_image(url = submission.url)
    await ctx.send(embed = embed)
    
@client.command()
async def funny(ctx):
    subreddit = reddit.subreddit('funny').hot()
    post = random.randint(1,100)
    for i in range(0, post):
        submission = next(x for x in subreddit if not x.stickied)
    time_created = datetime.datetime.fromtimestamp(submission.created)
    embed = discord.Embed(title = submission.title,description = '**Post by:** \n /u/' + str(submission.author) + '\n   **Posted At:** \n' + str(time_created) + ' **UTC**', colour = discord.Colour.from_rgb(34, 137, 240))
    embed.set_image(url = submission.url)
    await ctx.send(embed = embed)

@client.command()
async def softwaregore(ctx):
    subreddit = reddit.subreddit('softwaregore').hot()
    post = random.randint(1,100)
    for i in range(0, post):
        submission = next(x for x in subreddit if not x.stickied)
    time_created = datetime.datetime.fromtimestamp(submission.created)
    embed = discord.Embed(title = submission.title,description = '**Post by:** \n /u/' + str(submission.author) + '\n   **Posted At:** \n' + str(time_created) + ' **UTC**', colour = discord.Colour.from_rgb(34, 137, 240))
    embed.set_image(url = submission.url)
    await ctx.send(embed = embed)

@client.command()
async def facepalm(ctx):
    subreddit = reddit.subreddit('facepalm').hot()
    post = random.randint(1,100)
    for i in range(0, post):
        submission = next(x for x in subreddit if not x.stickied)
    time_created = datetime.datetime.fromtimestamp(submission.created)
    embed = discord.Embed(title = submission.title,description = '**Post by:** \n /u/' + str(submission.author) + '\n   **Posted At:** \n' + str(time_created) + ' **UTC**', colour = discord.Colour.from_rgb(34, 137, 240))
    embed.set_image(url = submission.url)
    await ctx.send(embed = embed)
    
@client.command()
async def assholedesign(ctx):
    subreddit = reddit.subreddit('assholedesign').hot()
    post = random.randint(1,100)
    for i in range(0, post):
        submission = next(x for x in subreddit if not x.stickied)
    time_created = datetime.datetime.fromtimestamp(submission.created)
    embed = discord.Embed(title = submission.title,description = '**Post by:** \n /u/' + str(submission.author) + '\n   **Posted At:** \n' + str(time_created) + ' **UTC**', colour = discord.Colour.from_rgb(34, 137, 240))
    embed.set_image(url = submission.url)
    await ctx.send(embed = embed)
    
@client.command()
async def mildlyinteresting(ctx):
    subreddit = reddit.subreddit('mildlyinteresting').hot()
    post = random.randint(1,100)
    for i in range(0, post):
        submission = next(x for x in subreddit if not x.stickied)
    time_created = datetime.datetime.fromtimestamp(submission.created)
    embed = discord.Embed(title = submission.title,description = '**Post by:** \n /u/' + str(submission.author) + '\n   **Posted At:** \n' + str(time_created) + ' **UTC**', colour = discord.Colour.from_rgb(34, 137, 240))
    embed.set_image(url = submission.url)
    await ctx.send(embed = embed)
    



memes = [
'https://i.imgur.com/7H13IGa.jpeg',
'https://i.imgur.com/ZFaIys7.jpeg',
'https://i.imgur.com/Vp8cPxA.jpeg',
'https://i.imgur.com/Z3eByMq.jpeg',
'https://i.imgur.com/aEhjDSz.jpeg',
'https://i.imgur.com/RcSouWQ.jpeg',
'https://i.imgur.com/IkUoqSG.png',
'https://i.imgur.com/EATeBKw.jpeg',
'https://i.imgur.com/1p2v7pA.jpeg',
'https://i.imgur.com/O8NK4xG.jpeg',
'https://i.imgur.com/YYa5ilW.jpeg',
'https://i.imgur.com/k6E5ZEj.jpeg',
'https://i.imgur.com/oqVrqBe.jpeg',
'https://i.imgur.com/YrjB7Ey.jpeg',
'https://i.imgur.com/MUVZoEq.jpeg',
'https://i.imgur.com/WQcRP2G.jpeg',
'https://i.imgur.com/fxI9y1r.jpeg',
'https://i.imgur.com/Y9187ZZ.jpeg',
'https://i.imgur.com/FLQ7pEJ.jpeg',
'https://i.imgur.com/cmjt8d6.jpeg',
'https://i.imgur.com/aJiAFvy.jpeg',
'https://i.imgur.com/yS71Dfu.jpeg',
'https://i.imgur.com/HCKq3uH.jpeg',
'https://i.imgur.com/7SsBPd2.jpeg',
'https://i.imgur.com/aPmmXtr.jpeg',
'https://i.imgur.com/wi8dlYa.jpeg',
'https://i.imgur.com/95yJdU0.jpeg',
'https://i.imgur.com/Sc18aPH.jpeg',
'https://i.imgur.com/6BhLM0T.jpeg',
'https://i.imgur.com/ap5kbDo.jpeg',
'https://i.imgur.com/qcheI4P.jpeg',
'https://i.imgur.com/j3XGgY5.jpeg',
'https://i.imgur.com/7k9Laj6.jpeg',
'https://i.imgur.com/n9ZeJmf.jpeg']


@client.command()
async def oldmeme(ctx):
	embed = discord.Embed(title = "Here is your meme!", color = discord.Colour.from_rgb(54, 151, 255))
	random_memes = random.choice(memes)
	embed.set_image(url = random_memes)
	embed.set_footer(text = "Command used by "+ctx.author.name+" | Wolfyy Bot!")
	await ctx.send(embed=embed)


@client.command()
async def invite(ctx):
	embed = discord.Embed(title = "Thanks for using me! Here is how to invite me to another server.", description = "Here is the link where you can invite me! https://discord.com/api/oauth2/authorize?client_id=739874992036249731&permissions=8&scope=bot", color = discord.Colour.from_rgb(54, 151, 255))
	embed.set_footer(text = "Command used by "+ctx.author.name+" | Wolfyy Bot!")
	await ctx.send(embed=embed)

client.remove_command('help')

@client.command()
async def help(ctx):
	embed = discord.Embed(title = "Wolfyy Bot Help [ALPHA]", description = "[Please remember that our bot is still in the Alpha Stage. Because our bot is so good we need to have multiple help commands ;).", color = discord.Colour.from_rgb(54, 151, 255))
	embed.add_field(name = ":hammer: Moderation Help:", value = "w!helpModeration", inline = False)
	embed.add_field(name = ":gear: Other Features Help:", value = "w!helpOther", inline = False)
	embed.add_field(name = ":money_with_wings: Economy Commands:", value = "w!helpEconomy", inline = False)
	embed.add_field(name = ":desktop: Reddit Commands:", value = "w!helpReddit", inline = False)
	embed.add_field(name = ":video_game: Random Fun Commands:", value = "w!helpRandom", inline = False)
	embed.set_footer(text = "Command used by "+ctx.author.name+" | Wolfyy Bot!")
	await ctx.send(embed=embed)

@client.command()
async def helpRandom(ctx):
	embed = discord.Embed(title = ":video_game: Random Fun Commands!", description = "This is where you can get help with some random fun commands!", color = discord.Colour.from_rgb(54, 151, 255))
	embed.add_field(name = "Coin Flip Command", value = "w!coinflip", inline = False)
	embed.add_field(name = "Diceroll Command", value = "w!diceroll", inline = False)
	embed.add_field(name = "How Gay Command", value = "w!howgay (for yourself), w!howgayis <member> (for others)", inline = False)
	embed.add_field(name = "Guessing Game Command", value = "w!guessinggame", inline = False)
	embed.add_field(name = "Rock Paper Scissors Command", value = "w!rps", inline = False)
	embed.set_footer(text = "Command used by "+ctx.author.name+" | Wolfyy Bot!")
	await ctx.send(embed=embed)

@client.command()
async def helpOther(ctx):
    embed = discord.Embed(title = ":gear: Other Features Help", description = "This is where you can get help with other commands in this bot.", color = discord.Colour.from_rgb(54, 151, 255))
    embed.add_field(name = "Creator Of The Bot's YT Command", value = "w!creatorYT", inline = False)
    embed.add_field(name = "Who is? Command", value = "w!whois <member>", inline = False)
    embed.add_field(name = "Avatar Command", value = "w!avatar <member>", inline = False)
    embed.add_field(name = "Old Meme Command", value = "w!oldmeme", inline = False)
    embed.add_field(name = "Poll Command", value = "w!poll <poll question> (Permissions Needed: Manage Messages)", inline = False)
    embed.set_footer(text = "Command used by "+ctx.author.name+" | Wolfyy Bot!")
    await ctx.send(embed=embed)

@client.command()
async def suicide(ctx):
	await ctx.send("**You found the secret command! This command was made because the dev team is depressed! Also, you jumped off a building and survived! But, you landed on a pen that went into your eyeball and impaled 6 inches ;) into your brain. Have a great day.**x")

@client.command()
async def whois(ctx, member : discord.Member):
	memberjoin = member.joined_at
	embed = discord.Embed(title = member.name, description = member.mention, color = discord.Colour.from_rgb(54, 151, 255))
	embed.add_field(name = "ID", value = member.id, inline = True)
	embed.add_field(name = "Highest Role", value = member.top_role, inline = True)
	embed.add_field(name = "Status", value = str(member.status), inline = True)
	embed.add_field(name = "Activity", value = member.activity, inline = True)
	embed.add_field(name = "Join Date", value = memberjoin.strftime('%m/%d/%Y'), inline = True)
	embed.set_footer(text = "Command used by "+ctx.author.name+" | Wolfyy Bot!")
	embed.set_thumbnail(url = member.avatar_url)
	await ctx.send(embed=embed)

@client.command()
async def avatar(ctx, member : discord.Member):
	embed = discord.Embed(color = discord.Colour.from_rgb(54, 151, 255))
	embed.set_image(url = member.avatar_url)
	embed.set_footer(text = "Command used by "+ctx.author.name+" | Wolfyy Bot!")
	await ctx.send(embed=embed)

@client.command()
async def helpModeration(ctx):
	embed = discord.Embed(title = ":hammer: Moderation Commands:", description = "Here are our commands for Moderation!", color = discord.Colour.from_rgb(54, 151, 255))
	embed.add_field(name = "Clear Messages Command", value = ":clear <Ammount of messages deleted + 1> [Manage Messages Permissions Needed]", inline=False)
	embed.add_field(name = "Kick Member Command", value = ":kick <member> [Kick Members Permissions Needed]", inline = False)
	embed.add_field(name = "Ban / Unban Command", value = ":ban <member> <reason>, :unban <member> [Ban Members Permission Needed]", inline=False)
	embed.add_field(name = "Mute Command", value = ":mute <member> <reason>, :unmute <member> <reason> [Kick Members Permission Required]", inline = False)
	embed.set_footer(text = "Command used by "+ctx.author.name+" | Wolfyy Bot!")
	await ctx.send(embed=embed)

@client.command()
async def helpEconomy(ctx):
	embed = discord.Embed(title = ":money_with_wings: Economy Commands:", description = "Here are our commands for Memes! (More commands are coming to this section soon! E.g. Reddit search commands!)", color = discord.Colour.from_rgb(54, 151, 255))
	embed.add_field(name = "Balance Command", value = "w!balance", inline = False)
	embed.add_field(name = "Beg Command", value = "w!beg", inline = False)
	embed.add_field(name = "Deposit Command", value = "w!deposit <ammount>", inline = False)
	embed.add_field(name = "Withdraw Command", value = "w!withdraw <ammount>", inline = False)
	embed.add_field(name = "Send Command", value = "w!send <member> <ammount>", inline = False)
	embed.add_field(name = "Rob Command", value = "w!rob <member>", inline = False)
	embed.set_footer(text = "Command used by "+ctx.author.name+" | Wolfyy Bot!")
	await ctx.send(embed=embed)

@client.command()
async def helpReddit(ctx):
	embed = discord.Embed(title = ":desktop: Reddit Commands:", description = "Here are all of our commands for searching Reddit!", color = discord.Colour.from_rgb(54, 151, 255))
	embed.add_field(name = "r/memes Command", value = "w!memes", inline = True)
	embed.add_field(name = "r/tihi (Thanks I Hate It) Command", value = "w!tihi", inline = True)
	embed.add_field(name = "r/funny Command", value = "w!funny", inline = True)
	embed.add_field(name = "r/softwaregore Command", value = "w!softwaregore", inline = True)
	embed.add_field(name = "r/facepalm Command", value = "w!facepalm", inline = True)
	embed.add_field(name = "r/assholedesign Command", value = "w!assholedesign", inline = True)
	embed.add_field(name = "r/mildlyinteresting", value = "w!mildlyinteresting", inline = True)
	embed.set_footer(text = "Command used by "+ctx.author.name+" | Wolfyy Bot!")
	await ctx.send(embed=embed)

@client.command(aliases=['c'])
@commands.has_permissions(manage_messages = True)
async def clear(ctx,amount=2):
	await ctx.channel.purge(limit = amount)

@client.command(aliases=['k'])
@commands.has_permissions(kick_members = True)
async def kick(ctx,member : discord.Member,*,reason= "No Reason Provided"):
	embed = discord.Embed(title = f":hammer: {member.name} Has been kicked from the server.", description = f"Reason: {reason}", color = discord.Colour.from_rgb(54, 151, 255))
	embed2 = discord.Embed(title = f"You have been kicked from {ctx.guild.name}!", description = f"Reason: {reason} Banned By: {ctx.author.name}", color = discord.Colour.from_rgb(54, 151, 255))
	await ctx.send(embed=embed)
	await member.send(embed=embed2)
	await member.kick(reason=reason)

@client.command(aliases=['b'])
@commands.has_permissions(ban_members = True)
async def ban(ctx,member : discord.Member,*,reason= "No Reason Provided"):
	embed = discord.Embed(title = ":hammer: :lock: "+member.name+" Has Been Banned.", description = "Reason: "+reason, color = discord.Colour.from_rgb(54, 151, 255))
	embed.add_field(name = "User's ID:", value = member.id, inline = False)
	embed.set_footer(text = "Command used by "+ctx.author.name+" | Wolfyy Bot!")
	await ctx.send(embed = embed)
	await member.ban(reason=reason)

@client.command()
@commands.has_permissions(ban_members = True)
async def unban(ctx, *, member):
      banned_users = await ctx.guild.bans()
      member_name, member_discriminator = member.split('#')

      for ban_entry in banned_users:
          user = ban_entry.user

          if (user.name, user.discriminator) == (member_name, member_discriminator):
              await ctx.guild.unban(user)
      embed = discord.Embed(title = "Unban Successfull!", description = f"{user} has been unbanned by {ctx.author.name}.", color = discord.Colour.from_rgb(255,0,0))
      await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(kick_members=True)
async def mute(ctx, member:discord.Member,*,reason= "No Reason Provided."):
  await ctx.send(member.mention+" **Has been muted. Reason: **"+reason)
  while True:
    try:
      muted_give = discord.utils.get(ctx.guild.roles, name = 'muted')
      await member.add_roles(muted_give)
      break
    except AttributeError:
      muted = await ctx.guild.create_role(name = "muted")
      await ctx.message.channel.set_permissions(ctx.guild.get_role(muted.id), send_messages = False, reason=reason)

@client.command()
@commands.has_permissions(kick_members=True)
async def unmute(ctx, member : discord.Member):
	await ctx.send(member.mention+" **Has been unmuted.**")
	muted_remove = discord.utils.get(ctx.guild.roles, name = 'muted')
	await member.remove_roles(muted_remove)


@client.command()
async def coinflip(ctx):
    coinside = random.randint(0,1)
    await ctx.send('**Flipping a Coin...**')
    await asyncio.sleep(3)
    if coinside == 0:
        await ctx.send("You flipped **Heads**!")
    elif coinside == 1:
        await ctx.send("You flipped **Tails**")




@client.command()
async def diceroll(ctx):
    diceside = random.randint(1,6)
    await ctx.send('**Rolling Dice...**')
    await asyncio.sleep(3)
    await ctx.send('**You rolled a **' + str(diceside))



@client.command()
async def howgay(ctx):
    meter = random.randint(1,100)
    await ctx.send('You are ' + str(meter) + '% (percent) gay.')



@client.command()
async def howgayis(ctx, member:discord.Member):
    meter = random.randint(1,100)
    await ctx.send(str(member) + ' is ' + str(meter) + '% (percent) gay.')




@client.command()
async def guessinggame(ctx):
    amount = 1
    channel = ctx.message.channel
    tries = 0
    tries_left = 10
    await ctx.channel.purge(limit = amount)
    await ctx.send("Hi, " + str(ctx.author) + '!')
    await ctx.send("I am thinking of a number between 1 and 100, can you guess it? You get 10 tries.")
    def guessinginput(m):
         return m.author == ctx.message.author and m.content.isdigit()
    guessing_game_comps_number = random.randint(1,100)
    try:
        for x in range(10):
            guessing_input = await client.wait_for('message',check=guessinginput,timeout = 15)
            if int(guessing_input.content) == guessing_game_comps_number:
                await ctx.send("Congrats you have guessed my number!")
                await ctx.send ("You've taken " + str(tries) + " guesses to guess my number!")
                break
            elif int(guessing_input.content) < guessing_game_comps_number:
                await ctx.send("That's too low, aim higher!")
                tries = tries + 1
                tries_left = tries_left - 1
                await ctx.send("You have " + str(tries_left) + " tries left!")
            elif int(guessing_input.content) > guessing_game_comps_number:
                await ctx.send("Thats too high, aim lower!")
                tries = tries + 1
                tries_left = tries_left - 1
                await ctx.send("You have " + str(tries_left) + " tries left!")
        await ctx.send("The computer's number was: " + str(guessing_game_comps_number) + ".")
    except:
        await ctx.send("You timed out, please try again.")




@client.command()
async def rps(ctx):
    amount = 1
    await ctx.channel.purge(limit = amount)
    channel = ctx.message.channel
    comp_choice = random.choice(rps_choices)
    wins = 0
    loses = 0
    ties = 0
    await ctx.send('Hi, ' + str(ctx.author) + '! Welcome to Rock Paper Sciscors!')
    await ctx.send("Sometimes my answers are a little slow, please wait until I say 'What is your next move' before giving me your response.")
    await ctx.send("Do you choose rock, paper or sciscors?")
    def check(m):
        return m.content == 'rock' or 'paper' or 'scissors' and m.channel == channel
    try:
        for x in range(5):
            player_input = await client.wait_for('message', check=check, timeout = 15)
            if player_input.clean_content == "paper" and comp_choice == 1:
                await ctx.send("The computer chose rock. You win!")
                wins = wins + 1
                await ctx.send("You have won " + str(wins) + " game(s).")
                await ctx.send("What is your next move?")
            elif  player_input.clean_content == "scissors" and comp_choice == 1:
                await ctx.send("The computer chose rock. You lose.")
                loses = loses + 1
                await ctx.send("You have lost " + str(loses) + " game(s).")
                await ctx.send("What is your next move?")
            elif player_input.clean_content == "rock" and comp_choice == 1:
                await ctx.send("The computer chose rock. Tie Game!.")
                ties = ties + 1
                await ctx.send("You have tied " + str(ties) + " game(s).")
                await ctx.send("What is your next move?")
            elif player_input.clean_content == "scissors" and comp_choice == 2:
                await ctx.send("The computer chose paper. You Win!.")
                wins = wins + 1
                await ctx.send("You have won " + str(wins) + " game(s).")
                await ctx.send("What is your next move?")
            elif player_input.clean_content == "paper" and comp_choice == 2:
                await ctx.send("The computer chose paper. Tie Game!.")
                ties = ties + 1
                await ctx.send("You have tied " + str(ties) + " game(s).")
                await ctx.send("What is your next move?")
            elif player_input.clean_content == "rock" and comp_choice == 2:
                await ctx.send("The computer chose paper. You lose.")
                loses = loses + 1
                await ctx.send("You have lost " + str(loses) + " game(s).")
                await ctx.send("What is your next move?")
            elif player_input.clean_content == "scissors" and comp_choice == 3:
                await ctx.send("The computer chose scissors. Tie Game!.")
                ties = ties + 1
                await ctx.send("You have tied " + str(ties) + " game(s).")
                await ctx.send("What is your next move?")
            elif player_input.clean_content == "paper" and comp_choice == 3:
                await ctx.send("The computer chose scissors. You lose.")
                loses = loses + 1
                await ctx.send("You have lost " + str(loses) + " game(s).")
                await ctx.send("What is your next move?")
            elif player_input.clean_content == "rock" and comp_choice == 3:
                await ctx.send("The computer chose scissors. You Win!.")
                wins = wins + 1
                await ctx.send("You have won " + wins + " game(s).")
                await ctx.send("What is your next move?")
        await ctx.channel.purge(limit=amount)
        if loses > wins:
            await ctx.send("You have lost against the computer.")
        elif wins > loses:
            await ctx.send("You have won against the computer!")
        elif loses == wins:
            await ctx.send("You and the computer have tied.")
        await ctx.send("You have won " + str(wins) + " games, lost " + str(loses) + " games and tied " + str(ties) + " games.")   
    except: 
        await ctx.send("You timed out, please try again.")


@client.command()
@commands.has_permissions(manage_messages = True)
async def poll(ctx,*,question: str):
    ammount = 1
    await ctx.channel.purge(limit=ammount)
    embed = discord.Embed(title = f"{ctx.author.name} has created a poll!", description = f"{question}", color = discord.Colour.from_rgb(54, 151, 255))
    embed.set_footer(text = "Command used by "+ctx.author.name+" | Wolfyy Bot!")
    message = await ctx.send(embed=embed)
    await message.add_reaction("✔️")
    await message.add_reaction("❌")

@client.command()
#tickre stands for ticket reason.
async def ticket(ctx, tickre:str):
    embed = discord.Embed(title =f"Support Ticket System.", description = f"{ctx.author.name}, your ticket is being created!", color = discord.Colour.from_rgb(54,151,255))
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("✔️")




@client.event
async def on_command_error(ctx,error):
	if isinstance(error,commands.CheckFailure):
		embed = discord.Embed(title = "Sorry, you cannot use that command!", description = "You cannot use that command due to a lack of permissions. For help use `w!help` to see all commands! It will also show permissions needed to use them if any!", color = discord.Colour.from_rgb(54, 151, 255))
		embed.set_footer(text = "Wolfyy Bot Error: Member Doesn't Have Required Permissions!")
		await ctx.send(embed = embed)
	elif isinstance(error,commands.MissingRequiredArgument):
		embed2 = discord.Embed(title = "Sorry, You Are Missing The Required Argument!", description = "In non-coder terms it means you have missed out something from your command! The most common reason for this is you have forgotten the @member from a command! Use `w!help` to see commands and see wheather they need to have something after the command!", color = discord.Colour.from_rgb(54, 151, 255))
		embed2.set_footer(text = "Wolfyy Bot Error: Missing Required Arguments!")
		await ctx.send(embed=embed2)
	elif isinstance(error, commands.CommandNotFound):
		embed3 = discord.Embed(title = "Sorry, That is not a command!", description = "The message that you have entered is not a registered command in the Wolfyy Bot coding! To see all commands type `w!help` to see the commands I have!", color = discord.Colour.from_rgb(54, 151, 255))
		embed3.set_footer(text = "Wolfyy Bot Error: Command Not Found!")
		await ctx.send(embed=embed3)


client.run('NzM5ODc0OTkyMDM2MjQ5NzMx.Xyg0SA.sDN3TEbBfQKDM8MzypS3PFg0d-o')
