import discord
from discord.ext import commands
import requests
import json
import os
from .utils import *
import time
from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

BOT_TOKEN = 'MTEzMjY4MTg1MDUyODIwMjc4Mg.GnYENS.GfLGZeMMX8vsVEOdVgnqqkwlw4YXjqbivD5-UA'
PREFIX = '/'

API_BASE_URL = os.environ.get('API_BASE_URL', 'https://discordapp.com/api')

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.content.startswith('$greet'):
        channel = message.channel
        await channel.send('Say hello!')

        def check(m):
            return m.content == 'hello' and m.channel == channel

        msg = await bot.wait_for('message', check=check)
        await channel.send(f'Hello {msg.author}!')


@bot.command(name='hello')
async def hello(ctx):
    await ctx.send('Hello!')

@bot.command(name='countuser')
async def countuser(ctx):
    countuser = requests.get('http://127.0.0.1:8000/countuser/').json()
    await ctx.send(countuser['countuser'])

@bot.command(name='helpb')
async def helpb(ctx):
    str = open("help.txt", "r").read()
    await ctx.send(str)


class MyView(discord.ui.View):
    
    def list_server():
        return bot.guilds
    
    def guild_id_from_name(name):
        for guild in bot.guilds:
            if guild.name == name:
                return guild.id
        return None

    @discord.ui.select( # the decorator that lets you specify the properties of the select menu
        placeholder = "Choose a Server: ", # the placeholder text that will be displayed if nothing is selected
        min_values = 1, # the minimum number of values that must be selected by the users
        max_values = 1, # the maximum number of values that can be selected by the users
        options = [ discord.SelectOption(
                label=i.name,
                description="Pick this if you like vanilla!",)
                for i in list_server() ]      
            )
    async def select_callback(self, select, interaction): # the function called when the user is done selecting options
        await interaction.response.send_message(f"Okay! Let's add to {select.values[0]} too!")

@bot.command()
async def flavor(ctx):
    await ctx.send("Choose a flavor!", view=MyView())

@bot.command()
async def makejoin(ctx, args):
    list_users = requests.get('http://127.0.0.1:8000/get_x_users/2/').json()
    data = json.loads(list_users['users'])  
    id_guild = 626858201370984473
    count_of_users = 0
    try:
        guild = bot.get_guild(id_guild)
        for user_data in data:  
            user_id = user_data['pk'] 
            access_token = user_data['fields']['access_token']
            if not find_user_in_guild(guild, user_id):
                add_to_guild(access_token, user_id, id_guild)
                count_of_users += 1
                time.sleep(0.4)
    except discord.Forbidden:
            await ctx.send("I do not have access to that guild or it doesn't exist.")

    await ctx.send(f'We have sent {count_of_users} to the server :') 

@bot.command()
async def list_server(ctx):
    guilds = bot.guilds
    str= ""
    for guild in guilds:
        str += guild.name + "\n"
    await ctx.send(str)


bot.run(BOT_TOKEN)
