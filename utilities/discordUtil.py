import discord
import os


class DiscordUtil:
    async def interactionResponse(self, interaction, embed=None, content=None, ephemeral=False):
        await interaction.response.send_message(content=content, embed=embed, ephemeral=ephemeral)
