import discord
from discord import app_commands
from discord.ext import commands , tasks
import io
from sqlalchemy.orm import Session
from uuid import uuid4
from modules.DB.db import Dbstruct,BotDb
from modules.Config.config import combos_channel,authorized_role,guild_id,logs
from modules.auth.helper import end_date_calc,create_embed
session:Session = BotDb().session

class Auth(commands.Cog):
    """
    A Discord cog for searching and displaying Hadiths.

    Attributes:
        bot (discord.Client): The Discord bot instance.
    """
    def __init__(self,bot:discord.Client):
        self.bot = bot

    @commands.has_permissions(administrator=True)
    @app_commands.command(name="key_gen")
    @app_commands.describe(
    sub="subscription type")
    @app_commands.choices(
        sub=[
            app_commands.Choice(name="1 day",value=1),
            app_commands.Choice(name="3 days",value=3),
            app_commands.Choice(name="1 week",value=7),
            app_commands.Choice(name="2 weeks",value=14),
            app_commands.Choice(name="1 month",value=30),
            app_commands.Choice(name="3 month",value=90),
        ]
    )
    
    async def authorize(self,interaction:discord.Interaction,sub:app_commands.Choice[int]):
        await interaction.response.defer()
        key = str(uuid4())
        new_key = Dbstruct.keys(str(key),sub=str(sub.name))
        session.add(new_key)
        session.commit()
        embed = discord.Embed(color=discord.Color.green())
        embed.add_field(name="key 🔓",value=f"```{key}```")
        embed.add_field(name="subscription_type 🎟️",value=str(sub.name))
        await interaction.followup.send(embed=embed,ephemeral=True)        
    
    @app_commands.command(name="claim")
    @app_commands.describe(key="authentication_key open a ticket to claim one")
    async def claim(self,interaction:discord.Interaction,key:str):
        await interaction.response.defer()
        
        server = self.bot.get_guild(guild_id)
        role   = server.get_role(authorized_role)
        if session.query(Dbstruct.users).filter(Dbstruct.users.id == interaction.user.id).first():
            embed = await create_embed(title="You are already registered",content="You are already registered as a premium member",color=discord.Color.yellow())
            if not role in interaction.user.roles:
                await interaction.user.add_roles(role)
            await interaction.followup.send(embed=embed)
            return 0 

        key_obj:Dbstruct.keys = session.query(Dbstruct.keys).filter(Dbstruct.keys.key == key).filter(Dbstruct.keys.claimed_by == None).first()
        if key_obj:
            print(key_obj)
            user_id = interaction.user.id
            key_obj.claimed_by = user_id
            new_user = Dbstruct.users(id=user_id,sub=key_obj.sub,end_sub=end_date_calc(key_obj.sub))
            session.add(new_user)
            user = interaction.user
            await user.add_roles(role)
            embed = await create_embed(title="Success",content=f"Congrats you got {key_obj.sub} of HQ private combos :partying_face:",color=discord.Color.green())
            try:
                session.commit()
            except:
                return 0 
            await interaction.followup.send(embed=embed)
        else:
            embed = await create_embed(title="Bad Key :sob:",content="invalid key, please open a ticket if you have bought this key",color=discord.Color.red())
            await interaction.followup.send(embed=embed)

    @app_commands.command(name="delete_sub")
    @app_commands.describe(user="the user you want to delete his sub",reason="why do you want to delete his sub")
    @commands.has_permissions(administrator=True)
    async def delete_sub(self,interaction:discord.Interaction,user:discord.Member,reason:str):
        await interaction.response.defer()
        user_obj = session.query(Dbstruct.users).filter(Dbstruct.users.id == user.id).first()
        if user_obj:
            server = self.bot.get_guild(guild_id)
            member = server.get_member(user.id)
            role = server.get_role(authorized_role)
            await member.remove_roles(role)
            session.delete(user_obj)
            session.commit()
            logs_channel = server.get_channel(logs)
            embed = await create_embed(title=f"removed {user.name} Successfully",content=f"deleted {user.name} because {reason}",color=discord.Color.green())
            await interaction.followup.send(embed=embed)
            await logs_channel.send(embed=embed)
        else:
            embed = await create_embed(title="user is not premium member",content="user is not even a premium member to remove him!",color=discord.Color.red())
            await interaction.followup.send(embed=embed)


async def setup(bot:commands.bot):
    """
    Setup function for adding the Auth cog to the bot.

    Args:
        bot (commands.Bot): The Discord bot instance.

    Returns:
        None
    """
    await bot.add_cog(Auth(bot=bot))