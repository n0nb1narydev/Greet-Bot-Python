# run `pip install discord.py` to install discord.py
# run `pip install python-dotenv` to install dotenv
import os
import discord
from dotenv import load_dotenv
from models import initialize, Member, session
from sqlalchemy import func, desc
import csv

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
    await channel.send(f"Hey {member.mention}, welcome to the **{guild.name}**! Check your direct messages to verify your account.")

    # send direct message to new user
    await member.send(f"Welcome to the {guild.name}. In order to verify your account, we must make sure that you are a valid member. Please reply with your Treehouse email address.")


@bot.event
async def on_message(message):
    # if the message contains the "@" symbol and the channel type is a DM - Adds member to the database.
    if "@" in message.content and "private" in message.channel.type and message.author != bot.user:
        new_member = Member(username=message.author.name, email=message.content, techdegree="TBD", verified=False)
        session.add(new_member)
        session.commit()
        update_csv()
        await message.author.send("Thank you for your response. Your information has been added to our database. Please allow up to 3 business days for verification.")
    # if the user sends a message that does not contain an "@" symbol. May want to used Regex for email verification in the future.
    elif "private" in message.channel.type and message.author != bot.user:
        await message.author.send("Invalid email address. Please try again!")


def update_csv():
    data = "members.csv"
    titles = [
        'username',
        'email',
        'techdegree',
        "verified"
    ]
    
    with open(data, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile,fieldnames=titles)
        writer.writeheader()
        members = session.query(Member).all()
        for member in members:
            writer.writerow({
                'username': member.username,
                'email': member.email,
                'techdegree': member.techdegree,
                'verified': member.verified,
            })

        print("Your database has been updated and saved to a csv!")


initialize()
bot.run(TOKEN)
