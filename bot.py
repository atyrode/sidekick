# This example requires the 'message_content' intent.

import re

import discord
from discord import (ButtonStyle, Client, DMChannel, Intents, Message,
                     app_commands)
from discord.ui import Button, View

from config import DISCORD_TOKEN, MODEL, WHITELISTED_USER_IDS, ollama
from main import chat


class AskBot(Client):
    def __init__(self):
        super().__init__(intents=Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # This copies the global commands over to your guild.
        await self.tree.sync()

client = AskBot()

@client.tree.command(name="ask", description="Ask the AI a question using the default 7B model")
async def ask(interaction: discord.Interaction, question: str):
    await handle_ask_command(interaction, "7b", question)

@client.tree.command(name="ask-7b", description="Ask the AI a question using the 7B model")
async def ask_7b(interaction: discord.Interaction, question: str):
    await handle_ask_command(interaction, "7b", question)

@client.tree.command(name="ask-14b", description="Ask the AI a question using the 14B model")
async def ask_14b(interaction: discord.Interaction, question: str):
    await handle_ask_command(interaction, "14b", question)

async def handle_ask_command(interaction: discord.Interaction, model_size: str, question: str) -> None:
    if interaction.user.id not in WHITELISTED_USER_IDS:
        await interaction.response.send_message("Sorry, you don't have permission to use this command.", ephemeral=True)
        return

    if not question:
        await interaction.response.send_message("Please include a question!", ephemeral=True)
        return

    try:
        model = MODEL["deepseek"][model_size]
    except KeyError:
        await interaction.response.send_message(
            f"Invalid model size. Available sizes: {', '.join(MODEL['deepseek'].keys())}", 
            ephemeral=True
        )
        return

    # Defer the response since it might take more than 3 seconds
    await interaction.response.defer()

    try:
        response = chat(ollama, model, [{
            'role': 'system',
            'content': '''You are a concise assistant in a Discord chat. Keep your responses very brief (1-2 sentences max).'''
        }, {
            'role': 'user',
            'content': question,
        }])
        
        content = response.message.content
        thoughts = ""
        actual_response = content

        if '<think>' in content and '</think>' in content:
            parts = content.split('</think>')
            thoughts = parts[0].replace('<think>', '').strip()
            actual_response = parts[1].strip()
        
        view = View()
        view.add_item(ThoughtsButton(thoughts if thoughts else "No thoughts recorded."))
        
        reply = f"**Using model: {model}**\n\n{actual_response}"
        await interaction.followup.send(reply, view=view)
    except Exception as e:
        await interaction.followup.send(f"Sorry, something went wrong: {str(e)}")

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

class ThoughtsButton(Button):
    def __init__(self, thoughts: str):
        super().__init__(label="Show AI Thoughts", style=ButtonStyle.secondary)
        self.thoughts = thoughts

    async def callback(self, interaction):
        await interaction.response.send_message(
            f"**AI's Thoughts:**\n{self.thoughts}", 
            ephemeral=True  # Only visible to the user who clicked
        )

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

    # Handle different ask commands
    if message.content.startswith('$ask-'):
        model_size = message.content[5:].split(' ')[0]
        await handle_ask_command(message, model_size)
    elif message.content.startswith('$ask'):
        await handle_ask_command(message)
    elif message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(DISCORD_TOKEN)