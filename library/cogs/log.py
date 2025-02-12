from datetime import datetime

from discord import Embed
from discord.ext.commands import Cog

class Log(Cog):
  def __init__(self, bot):
    self.bot = bot

  @Cog.listener()
  async def on_ready(self):
    if not self.bot.ready:
      self.log_channel = self.bot.get_channel(1317130812298362920) # Mod-Logs Text Channel
      self.bot.cogs_ready.ready_up("log")

  @Cog.listener()
  async def on_user_update(self, before, after):
    if before.name != after.name:
      embed = Embed(title="Name change",
                    color=self.log_channel.guild.get_member(after.id).color,
                    timestamp=datetime.utcnow())
      
      fields = [("Before", before.name, False),
                ("After", after.name, False)]
      
      for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)

      await self.log_channel.send(embed=embed)
    
    if before.display_avatar != after.display_avatar:
      embed = Embed(title="Avatar change",
              description="New image is below, old to the right",
              color=self.log_channel.guild.get_member(after.id).color,
              timestamp=datetime.utcnow())
      
      embed.set_thumbnail(url=before.display_avatar)
      embed.set_image(url=after.display_avatar)

      await self.log_channel.send(embed=embed)

    if before.discriminator != after.discriminator:
      embed = Embed(title="Discriminator change",
                    color=self.log_channel.guild.get_member(after.id).color,
                    timestamp=datetime.utcnow())
      
      fields = [("Before", before.discriminator, False),
                ("After", after.discriminator, False)]
      
      for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)

      await self.log_channel.send(embed=embed)

  @Cog.listener()
  async def on_member_update(self, before, after):
    if before.display_name != after.display_name:
      embed = Embed(title="Nickname change",
                    description=after.display_name,
                    color=after.color,
                    timestamp=datetime.utcnow())
      
      embed.set_thumbnail(url=after.display_avatar)
      
      fields = [("Before", before.display_name, False),
                ("After", after.display_name, False)]
      
      for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)

      await self.log_channel.send(embed=embed)

    elif before.roles != after.roles:
      embed = Embed(title="Role updates",
                    description=after.display_name,
                    color=after.color,
                    timestamp=datetime.utcnow())
      
      embed.set_thumbnail(url=after.display_avatar)
      
      fields = [("Before", ", ".join([r.mention for r in before.roles]), False),
                ("After", ", ".join([r.mention for r in after.roles]), False)]
      
      for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)

      await self.log_channel.send(embed=embed)

  @Cog.listener()
  async def on_message_edit(self, before, after):
    if not after.author.bot:
      if before.content != after.content:
        embed = Embed(title="Message edit",
                      description=f"Edited by {after.author.display_name}.",
                      color=after.author.color,
                      timestamp=datetime.utcnow())
        
        fields = [("Member", before.author, False),
                  ("Before", before.content, False),
                  ("After", after.content, False)]
        
        for name, value, inline in fields:
          embed.add_field(name=name, value=value, inline=inline)

        await self.log_channel.send(embed=embed)

  @Cog.listener()
  async def on_message_delete(self, message):
    if not message.author.bot:
      if (message.content not in ["jr", "1", "lr", "0", "js", "3", "ls", "2"]
          and "!echo" not in message.content[0:5]):
        embed = Embed(title="Message deletion",
                      description=f"Deleted by {message.author.display_name}.",
                      color=message.author.color,
                      timestamp=datetime.utcnow())
        
        if len(message.content) > 0:
          embed.add_field(name="**Deleted message**", value=message.content, inline=False)
        if any([hasattr(a, "width") for a in message.attachments]):
          url = [a for a in message.attachments if(hasattr(a, "width"))][0].url
          embed.add_field(name="**Deleted attachment**", value="", inline=False)
          embed.set_image(url=url)

        await self.log_channel.send(embed=embed)

async def setup(bot):
  await bot.add_cog(Log(bot))
      