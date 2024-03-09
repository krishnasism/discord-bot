import discord
from discord import Client, Message
from discord.abc import MessageableChannel
import os
import random

intents = discord.Intents.default()
intents.message_content = True

client: Client = discord.Client(intents=intents)

jokes: list[tuple[str, str]] = [
    ("Why don't skeletons fight each other?", "They don't have the guts."),
    ("What's a vampire's favorite fruit?", "A blood orange."),
    ("Why don't scientists trust atoms?", "Because they make up everything."),
    ("What did one hat say to the other?", "You stay here, I'll go on ahead."),
    ("Why did the tomato turn red?", "Because it saw the salad dressing!"),
    ("What do you call fake spaghetti?", "An impasta."),
    ("Why did the scarecrow win an award?", "Because he was outstanding in his field."),
    ("What do you call a bear with no teeth?", "A gummy bear."),
    ("What do you get when you cross a snowman and a vampire?", "Frostbite."),
    ("Why did the bicycle fall over?", "Because it was two-tired."),
]

banned_words: list[str] = [
    "bad",
    "words",
]

bad_users: list[str] = [
    "user",
]

bad_message: str = "F!@#@!#"

channels: set[MessageableChannel] = set()


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message: Message):
    channels.add(message.channel)
    if message.author == client.user:
        return

    if message.content.startswith("$hello"):
        if any(bad_user in str(message.author).lower() for bad_user in bad_users):
            await message.channel.send(bad_message)
            return
        await message.channel.send(f"Hello! {message.author}")

    if message.content.startswith("$tell me a joke"):
        joke = random.choice(jokes)
        joke_line = joke[0] + "\n" + joke[1]
        await message.channel.send(joke_line)

    if any(banned_word in message.content.lower() for banned_word in banned_words):
        await message.channel.send(
            "Insulting others will get you reported to the foo bar."
        )


if __name__ == "__main__":
    with open(".env", "r") as env:
        lines = env.readlines()
        for line in lines:
            os.environ[line.split("=")[0]] = line.split("=")[1]
    token = os.getenv("TOKEN")
    if not token:
        exit(1)
    client.run(token)
