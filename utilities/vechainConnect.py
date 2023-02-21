import string
import os
import random
import discord
import asyncio
import time
from utilities.vechainEnergyClient import vechainEnergyClient
from utilities.discordUtil import DiscordUtil

venergy = vechainEnergyClient()
disutil = DiscordUtil()

TIMEOUT = 90


class VechainConnect:
    async def connect(self, interaction: discord.Interaction):
        baseuri = os.getenv('VECHAIN_ENERGY_BASE_URL')
        sessionid = ''.join(random.choice(string.ascii_letters) for i in range(36)[2:])
        state = ''.join(random.choice(string.ascii_letters) for i in range(36)[2:])
        await venergy.start_session(session_id=sessionid, state=state)
        redirect = f"https://{baseuri}/session/{sessionid}"
        authurl = f"https://{baseuri}/oauth2/authorize?state={state}&scope=identity%20profile&redirect_uri={redirect}"
        embed = discord.Embed()
        embed.description = f"please click [here]({authurl}) to identify yourself."
        await disutil.interactionResponse(interaction=interaction, embed=embed, ephemeral=True)

        return sessionid

    async def waitforuserauth(self, sessionid: str):
        timeout = TIMEOUT
        while True:
            await asyncio.sleep(1)
            status = await venergy.get_session(sessionid=sessionid)
            if 'access_token' in status or 'error' in status:
                return status

            if --timeout == 0:
                break
        return

    async def getuserdata(self, token_type, access_token):
        return await venergy.get_user_info(token_type=token_type, access_token=access_token)

    async def editresponse(selfs, interaction: discord.Interaction, description: str):
        embed = discord.Embed()
        embed.description = description
        await interaction.edit_original_response(content=None, embed=embed)
