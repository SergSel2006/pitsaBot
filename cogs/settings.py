import os
import pathlib

import yaml
from discord.ext import commands

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader as Loader
try:
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Dumper as Dumper


def can_manage_channels():
    async def predicate(ctx):
        perms = ctx.author.top_role.permissions
        return perms.manage_channels or perms.administrator
    
    return commands.check(predicate)


class SettingsCog(commands.Cog, name="настроики сервера"):
    """Изменяет всяческие настроики сервера."""
    def __init__(self, bot, cwd: pathlib.Path):
        self.bot = bot
        self.cwd = cwd
    
    @commands.Command
    @can_manage_channels()
    async def prefix(self, ctx, prefix):
        """Меняет префикс"""
        with open(
                pathlib.Path(
                        "data", "servers_config", str(ctx.guild.id),
                        "config.yml"
                        ),
                "r"
                ) as config:
            if prefix:
                config = yaml.load(config, Loader)
                config["prefix"] = prefix
                with open(
                        pathlib.Path(
                                "data", "servers_config", str(ctx.guild.id),
                                "config.yml"
                                ),
                        "w"
                        ) as config_raw:
                    yaml.dump(config, config_raw, Dumper)
                await ctx.send("Префикс успешно сменён!")
            else:
                await ctx.send("Укажите префикс!")
    
    @commands.Command
    @can_manage_channels()
    async def change_modlog_channel(self, ctx):
        """(де)Активирует modlog на указанном канале."""
        if not "disable" in ctx.message.content:
            with open(
                    pathlib.Path(
                            "data", "servers_config", str(ctx.guild.id),
                            "config.yml"
                            ),
                    "r"
                    ) as config:
                channel = ctx.message.channel_mentions[0]
                config = yaml.load(config, Loader)
                if not config["modlog"]["enabled"]:
                    config["modlog"]["enabled"] = True
                config["modlog"]["channel"] = channel.id
                with open(
                        pathlib.Path(
                            "data", "servers_config", str(ctx.guild.id),
                            "config.yml"
                            ),
                        "w"
                        ) as config_raw:
                    yaml.dump(config, config_raw, Dumper)
                    await ctx.send("Модлог активирован")

        else:
            with open(
                    pathlib.Path(
                        "data", "servers_config", str(ctx.guild.id),
                        "config.yml"
                        ),
                    "r"
                    ) as config:
                config = yaml.load(config, Loader)
                if config["modlog"]["enabled"]:
                    config["modlog"]["enabled"] = False
                with open(
                        pathlib.Path(
                            "data", "servers_config", str(ctx.guild.id),
                            "config.yml"
                            ),
                        "w"
                        ) as config_raw:
                    yaml.dump(config, config_raw, Dumper)
                    await ctx.send("Модлог деактивирован")


def setup(bot):
    bot.add_cog(SettingsCog(bot, pathlib.Path(os.getcwd())))
