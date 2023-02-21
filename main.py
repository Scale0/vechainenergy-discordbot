import os
import discord
from dotenv import load_dotenv
from discord import app_commands
from utilities.commandsUtil import CommandsUtil

# Load environment variables from a .env file
load_dotenv('.env')

# Initialize a new Discord bot client with all intents enabled
client = discord.Client(intents=discord.Intents.all())

# Create a new command tree that is synchronized with Discord's server
tree = app_commands.CommandTree(client)

# Instantiate an instance of CommandsUtil to handle the bot's commands
commands = CommandsUtil()


class BotClient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.synced = False

    # When the bot client is ready, print a message indicating that the command synchronization is starting
    # and then synchronize the command tree with Discord's server
    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            print(f'start syncing commands')
            await tree.sync()
            print(f'Done syncing commands')
            self.synced = True


# Define a new command named 'connect' with a description
# and associate it with the 'connect' method of the CommandsUtil class
@tree.command(name='connect', description='Please connect your Vechain Wallet')
async def connect(interaction: discord.Interaction):
    await commands.connect(interaction)


# Define a new command named 'disconnect' with a description
# and associate it with the 'disconnect' method of the CommandsUtil class
@tree.command(name='disconnect', description='Disconnect from current wallet')
async def disconnect(interaction: discord.Interaction):
    await commands.disconnect(interaction)


# Define a new command named 'whoami' with a description
# and associate it with the 'getprofile' method of the CommandsUtil class
@tree.command(name='whoami', description='check your current connected wallet')
async def getprofile(interaction: discord.Interaction):
    await commands.getprofile(interaction=interaction)


# Run the bot by passing in the Discord bot token from the environment variables
client.run(os.getenv('DISCORD_TOKEN'))
