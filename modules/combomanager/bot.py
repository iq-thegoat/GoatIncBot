import discord
from discord import app_commands
from discord.ext import commands , tasks
from modules.DB.db import Dbstruct,BotDb
from modules.Config.config import combos_channel,authorized_role,guild_id
import io
from sqlalchemy.orm import Session
session:Session = BotDb().session


class ComboBot(commands.Cog):
    """
    A Discord cog for searching and displaying Hadiths.

    Attributes:
        bot (discord.Client): The Discord bot instance.
    """

    def __init__(self, bot: discord.Client):
        """
        Initialize the Dorrar cog.

        Args:
            bot (discord.Client): The Discord bot instance.
        """
        self.bot = bot
        self.check_for_combos.start()

    def cog_unload(self) -> None:
        self.check_for_combos.stop()

    @tasks.loop(seconds=3)
    async def check_for_combos(self):
        combo:Dbstruct.combos = session.query(Dbstruct.combos).filter(Dbstruct.combos.uploaded == False).first()
        if combo:
            file = io.BytesIO(combo.file)
            channel = self.bot.get_channel(combos_channel)
            server = self.bot.get_guild(guild_id)
            role   = server.get_role(authorized_role)
            await channel.send(f"{combo.target} {role.mention}",file=discord.File(file,f"GOATINC_COMBO_{combo.id}.txt"))
            combo.uploaded = True
            session.commit()


    @tasks.loop(minutes=(60*12))
    async def db_backup(self):
        time.sleep(5)
        try:
            channel = self.bot.get_channel(db_backup_channel)
            await channel.send(file=discord.File("database.db"))
        except Exception as e:
            ic("Error uploading backup:", e)

async def setup(bot):
    """
    Setup function for adding the Dorrar cog to the bot.

    Args:
        bot (commands.Bot): The Discord bot instance.

    Returns:
        None
    """
    await bot.add_cog(ComboBot(bot=bot))