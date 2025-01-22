# This example requires the 'message_content' intent.

import discord
from discord import Client, DMChannel, Intents, Message

from config import DISCORD_TOKEN

intents = Intents.default()
intents.message_content = True

client = Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message: Message):
    if message.author == client.user:
        return

    # Log private messages
    if isinstance(message.channel, DMChannel):
        print(f"Private message from {message.author}: {message.content}")
        
    # Log messages from servers (guilds)
    else:
        print(f"Message in {message.guild.name}#{message.channel.name} from {message.author}: {message.content}")

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(DISCORD_TOKEN)