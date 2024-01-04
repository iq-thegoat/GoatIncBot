import discord
from discord import app_commands
from discord.ext import commands , tasks
from modules.DB.db import Dbstruct,BotDb
from modules.Config.config import combos_channel,authorized_role,guild_id,logs
from sqlalchemy.orm import Session
from modules.auth.helper import create_embed
import datetime

global session

session:Session = BotDb().session

class AuthTasks(commands.Cog):
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

        self.check_for_users.start()
    def cog_unload(self) -> None:
        self.check_for_users.stop()

    @tasks.loop(seconds=1)
    async def check_for_users(self):
        user_obj:Dbstruct.users = session.query(Dbstruct.users).filter(Dbstruct.users.end_sub < datetime.datetime.now()).first()
        if user_obj:
            id = user.id
            session.delete(user_obj)
            server = self.bot.get_guild(guild_id)
            user:discord.Member = server.get_member(id)
            role = server.get_role(authorized_role)
            await user.remove_roles(role)
            embed = await create_embed(title="user sub finished",content=f"user:{user.id},user_struct:{user_obj}")
            logs_channel = server.get_channel(logs)
            await logs_channel.send(embed=embed)
            session.commit()
        else:
            pass

async def setup(bot):
    """
    Setup function for adding the Dorrar cog to the bot.

    Args:
        bot (commands.Bot): The Discord bot instance.

    Returns:
        None
    """
    await bot.add_cog(AuthTasks(bot=bot))