import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
from collections import defaultdict
import asyncio

# Replace with your bot token and channel IDs
BOT_TOKEN = "MTMxOTY0MTU0NzYwMzQ0MzcyMw.G3qGWv.yiAu_mxuoF9o35X56QgZC2KRlgNm7kd7xQSvsI"
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
intents.guilds = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Maintain thread counters
daily_thread_count = defaultdict(
    lambda: defaultdict(int))  # {date: {channel_name: count}}

MESSAGES_DATE = datetime.now() - timedelta(days=2)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await check_auction_channels()
    print("Processing complete. Shutting down...")
    await bot.close()  # Log out and terminate the bot


@tasks.loop(minutes=15)  # Adjust frequency as needed
async def check_auction_channels():
    today = datetime.now().strftime("%m/%d/%Y")
    for channel_name, channel_id in CHANNELS.items():
        channel = bot.get_channel(channel_id)
        if not channel:
            print(f"Channel {channel_name} not found.")
            continue

        async for message in channel.history(limit=100, after=MESSAGES_DATE):  # Adjust the message limit as needed
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


# Initial thread message


@bot.command()
async def manual_check(ctx):
    """Command to trigger a manual check"""
    await check_auction_channels()


# Run the bot
bot.run(BOT_TOKEN)
