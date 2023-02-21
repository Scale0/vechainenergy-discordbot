# Import necessary modules
from utilities.discordUtil import DiscordUtil
from utilities.vechainConnect import VechainConnect
import discord
import json
from types import SimpleNamespace

# Create instances of the VechainConnect and DiscordUtil classes
vechainConnect = VechainConnect()
util = DiscordUtil()

# Create an empty dictionary to store the logged in users
loggedInUsers = {}


# Define a class to contain various commands for the bot
class CommandsUtil:
    async def connect(self, interaction: discord.Interaction):
        # Connect to Vechain using the VechainConnect class
        session_id = await vechainConnect.connect(interaction=interaction)
        # Wait for user authentication using the VechainConnect class
        status = await vechainConnect.waitforuserauth(sessionid=session_id)

        # Check if authentication was successful and retrieve user data
        if 'access_token' in status and 'token_type' in status:
            status = json.loads(status, object_hook=lambda d: SimpleNamespace(**d))
            userdata_response = await vechainConnect.getuserdata(token_type=status.token_type,
                                                                 access_token=status.access_token)
            userdata = json.loads(userdata_response)

            # Store the user's address in the loggedInUsers dictionary
            loggedInUsers[interaction.user.id] = userdata['address']
            description = f"you are connected as [{userdata['address']}](https://explore.vechain.org/accounts/{userdata['address']})"

            # Update the response with the user's address
            await vechainConnect.editresponse(interaction=interaction, description=description)
            return

        # If authentication failed, display an error message
        description = 'Time is up, please try again'
        await vechainConnect.editresponse(interaction=interaction, description=description)

    async def disconnect(self, interaction: discord.Interaction):
        # Remove the user's ID from the loggedInUsers dictionary
        del loggedInUsers[interaction.user.id]

        # Display a message to the user indicating they have been logged out
        await util.interactionResponse(interaction=interaction, content="your logged out!", ephemeral=True)

    async def getprofile(self, interaction: discord.Interaction):
        # Get the user's address from the loggedInUsers dictionary based on their ID
        userdata = loggedInUsers[interaction.user.id]

        # Create a description of the user's address and display it in an embed
        description = f"your connected as [{userdata}](https://explore.vechain.org/accounts/{userdata})"
        embed = discord.Embed(description=description, color=discord.Colour.green())
        await util.interactionResponse(interaction=interaction, embed=embed, ephemeral=True)
