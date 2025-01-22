# Discord AI Chat Bot

A Discord bot that integrates with Ollama to provide AI chat capabilities using the Deepseek model family.

## Overview

This project implements a Discord bot that can interact with users through direct messages and server channels while leveraging Ollama's API to generate AI responses using various Deepseek models.

## Prerequisites

- Python 3.x
- Discord Bot Token
- Ollama server setup with authentication

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Unix
   # or
   .\venv\Scripts\activate  # For Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Create a `.env` file in the root directory with the following variables:

```plaintext
DISCORD_TOKEN=your_discord_token
USERNAME=ollama_username
PASSWORD=ollama_password
HOST=ollama_host
PORT=ollama_port
```

## Project Structure

### Config Module

```python
MODEL = {
    "deepseek": {
        "1.5b": "deepseek-r1:1.5b",
        "7b": "deepseek-r1",
        "8b": "deepseek-r1:8b",
        "14b": "deepseek-r1:14b",
        "32b": "deepseek-r1:32b",
    }
}
```

Defines available Deepseek models and handles authentication configuration for the Ollama client.

### Discord Bot

```python
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
```

Implements a Discord bot that:
- Logs when the bot is ready
- Handles both direct messages and server messages
- Responds to basic commands (e.g., `$hello`)

### Main Module

```python
def pull_model(ollama: Client, model: str) -> None:
    model_pulled: bool = _is_model_pulled(ollama, model)
    if not model_pulled:
        ollama.pull(model)

def _is_model_pulled(ollama: Client, model: str) -> bool:
    response: ListResponse = ollama.list()
    return model in response.models

def chat(ollama: Client, model: str, messages: list[dict]) -> ChatResponse: 
    response: ChatResponse = ollama.chat(model, messages)
    return response
```

Provides core functionality for:
- Pulling AI models from Ollama
- Checking model availability
- Handling chat interactions with the AI model

## Features

- Multiple Deepseek model support (1.5B to 32B parameters)
- Secure authentication with Ollama API
- Discord message logging for both DMs and server messages
- Easy model management and chat interaction

## Usage

1. Ensure your environment variables are set
2. Run the bot:
   ```bash
   python bot.py
   ```

## Security

The project implements basic authentication for Ollama API access and stores sensitive information in environment variables for security.

## Dependencies

- discord.py - Discord API wrapper
- ollama - Ollama API client
- python-dotenv - Environment variable management
- audioop-lts - Audio processing support

## Contributing

Feel free to submit issues and pull requests to improve the functionality of this bot.
