from discord.ext.commands import Cog
from discord.errors import Forbidden

from ..db import db

class Welcome(Cog):
  def __init__(self, bot):
    self.bot = bot

  @Cog.listener()
  async def on_ready(self):
    if not self.bot.ready:
      self.welcome_channel = self.bot.get_channel(1286209238808399883) # Welcome Text Channel
      self.goodbye_channel = self.bot.get_channel(1317133240955306004) # Goodbye Text Channel
      self.bot.cogs_ready.ready_up("welcome")
  
  @Cog.listener()
  async def on_member_join(self, member):
    db.execute("INSERT INTO exp (UserID) VALUES (?)", member.id)
    await self.welcome_channel.send(f"Welcome {member.mention} to **{member.guild.name}**! Head over to <#1066416009197662341> to say hi!")

    try:
      await member.send(f"Welcome to **{member.guild.name}**! Enjoy your stay!")

    except Forbidden:
      pass

    await member.add_roles(*(member.guild.get_role(id_) for id_ in (1286206402917957673)))

  @Cog.listener()
  async def on_member_remove(self, member):
    db.execute("DELETE FROM exp WHERE UserID = ?", member.id)
    await self.goodbye_channel.send(f"{member.display_name} has left **{member.guild.name}**.")


async def setup(bot):
  await bot.add_cog(Welcome(bot))