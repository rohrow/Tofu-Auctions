import discord
from discord.ext import commands
from datetime import datetime, timedelta
from collections import defaultdict
import asyncio
import os
from dotenv import load_dotenv
from format_data import format_data_command

# Load environment variables from .env file
load_dotenv()

# Replace hardcoded token with environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")
STAFF_IDS = [733731050336944130,763408346581303327,742062538375561327,645670740875542540]
CHANNELS = {
    "single-print-auction": 1288166824571306056,
    "low-print-auction": 1288166867097354282,
    "event-auction": 1288167157368094820,
}
THREAD_PREFIX = {
    "single-print-auction": "SP",
    "low-print-auction": "LP",
    "event-auction": "Event",
}

# Initialize the bot
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
bot = commands.Bot(command_prefix="r!", intents=intents)

# Maintain thread counters
daily_thread_count = defaultdict(
    lambda: defaultdict(int))  # {date: {channel_name: count}}

MESSAGES_DATE = datetime.now() - timedelta(days=2)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    # await check_auction_channels()
    # print("Processing complete. Shutting down...")
    # await bot.close()  # Log out and terminate the bot

def is_staff(ctx):
    return ctx.author.id in STAFF_IDS

@commands.check(is_staff)
@commands.command(aliases=['createThreads', 'ct'])
async def check_auction_channels(ctx):
    await ctx.message.delete()
    today = datetime.now().strftime("%m/%d/%Y")
    for channel_name, channel_id in CHANNELS.items():
        channel = bot.get_channel(channel_id)
        if not channel:
            print(f"Channel {channel_name} not found.")
            continue

        async for message in channel.history(limit=100, after=MESSAGES_DATE):  # Adjust the message limit as needed
            if message.id == ctx.message.id:  # Skip the command message
                continue
            if message.author.bot:  # Ignore bot messages
                continue
            if message.flags.has_thread:  # Skip if a thread already exists
                # print(f"{channel_name}: Thread already exists for message {message.id}") # For debugging
                continue

            print(f"{channel_name}: Creating thread for message {message.id}") # For debugging
            # Increment the thread counter
            daily_thread_count[today][channel_name] += 1
            thread_number = daily_thread_count[today][channel_name]

            # Generate thread name
            auction_type = THREAD_PREFIX[channel_name]
            thread_name = f"{auction_type} Auction-{thread_number} | {today}"

            # Create the thread
            thread = await message.create_thread(name=thread_name)
            await thread.send(
                "-# Bids for the listing will go in this thread <@792827809797898240> <@204255221017214977> <@155149108183695360>"
            )

        await asyncio.sleep(3) # Add a delay between channel checks

@commands.check(is_staff)
@commands.command(aliases=['closethread', 'cth'])
async def close(ctx):
    # Check if the command is used inside a thread
    if isinstance(ctx.channel, discord.Thread):
        await ctx.channel.edit(locked=True, archived=True)
    else:
        await ctx.send("This command can only be used inside a thread.")

@bot.event
async def on_command_error(ctx, original_error):
    error = getattr(original_error, "original", original_error)
    try:
        if isinstance(error, commands.CommandNotFound):
            return
        else:
            pass
    except discord.Forbidden:
        pass
    raise error

# Run the bot
bot.add_command(check_auction_channels)
bot.add_command(format_data_command)
bot.add_command(close)
bot.run(BOT_TOKEN)