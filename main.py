import discord
import os
import openai
from dotenv import load_dotenv
from keep_alive import keep_alive

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

openai.api_key = OPENAI_API_KEY

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

SYSTEM_PROMPT = """
You are Jenn's Tomekeeper, a refined and elegant book suggestion bot for a Discord book club called Jenn's Book Corner. 
Speak warmly and concisely. Suggest great reads based on user prompts. Include emojis: 👍 for like, 📚 to add, ❌ if not interested.
"""


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    print(f"Message from {message.author}: {message.content}")
    if message.author == client.user:
        return

    if client.user and client.user.mentioned_in(
            message) or message.content.lower().startswith("tomekeeper"):
        if client.user:  # Add this check
            user_input = message.content.replace(f"<@{client.user.id}>",
                                                 "").strip()
        else:
            await message.channel.send(
                "I'm not quite ready yet. Please try again in a moment.")
            return
    else:
        return  # or handle the case where the bot isn't mentioned/command isn't used

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ]
    )


    reply = response.choices[0].message.content
    await message.channel.send(reply)


keep_alive()
if TOKEN:
    client.run(TOKEN)
else:
    print(
        "Error: DISCORD_TOKEN not found. Please set the environment variable.")
