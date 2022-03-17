# run `pip install discord.py` to install discord.py
# run `pip install python-dotenv` to install dotenv
import os
import discord
from dotenv import load_dotenv

# Keeps your bot's token private
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

intents = discord.Intents.default()
intents.members = True
bot = discord.Client(intents=intents)


@bot.event
async def on_ready():
    # Check to make sure that the bot is online
    print("Bot is Online.")


@bot.event
async def on_member_join(member):
    # Gets the guild that the member is in
    guild = bot.get_guild(member.guild.id)

    # if the server has a guild system channel - message will send there. 
    # Otherwise it is set to the "general" channel.
    if guild.system_channel:
        channel = guild.system_channel
    else:
        channel = discord.utils.get(guild.channels, name="general")

    # Message that will be sent to the user
    await channel.send(f"Hey {member.mention}, welcome to **{guild.name}** :heart_eyes::smiley:")

bot.run(TOKEN)