import datetime
from dateutil.relativedelta import relativedelta
import discord

def end_date_calc(sub_type:str):
    now = datetime.datetime.utcnow()
    if sub_type == "1 day":
        end_time = now + relativedelta(days=2)
        return end_time

    elif sub_type == "3 day":
        end_time = now + relativedelta(days=4)
        return end_time
        
    if sub_type == "1 week":
        end_time = now + relativedelta(days=8)
        return end_time

    if sub_type == "2 weeks":
        end_time = now + relativedelta(days=15)
        return end_time

    if sub_type == "1 month":
        end_time = now + relativedelta(days=31)
        return end_time

    if sub_type == "3 month":
        end_time = now + relativedelta(days=91)
        return end_time
        


async def create_embed(title: str, content: str, color: discord.Color):
    """
    Create and return a Discord embed with the specified title, content, and color.

    Args:
        title (str): The title of the embed.
        content (str): The content of the embed.
        color (discord.Color): The color of the embed.

    Returns:
        discord.Embed: The created embed.
    """
    embed = discord.Embed(title=title, color=color)
    embed.add_field(name=content, value="")
    embed.set_footer(text="if you think something is wrong, please open a ticket")
    return embed