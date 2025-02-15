#  Copyright (c) 2022-2023 SergSel2006 (Sergey Selivanov).
#
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.

import gettext
import traceback

import shared
from discord.ext import commands


_ = gettext.gettext


class Settings(commands.Cog):
    description = _("Configurations for bot")

    def __init__(self, bot):
        self.bot = bot

    settings_attrs = {
        "name": _("config"),
        "usage": _("<subcommand>"),
        "brief": _("changes settings. use `help config` for details."),
        "description": _(
            "Changes bots configurations. Available subcommands:"
            "\n  trigger <enable/disable>"
            "\n  react <enable/disable>"
        )
    }

    @commands.command(**settings_attrs)
    @shared.can_manage_server()
    async def config(self, ctx, mode, *options):
        lang = shared.load_server_language(ctx.guild.id)
        _ = lang.gettext
        config = shared.find_server_config(ctx.guild.id)
        mode = mode.lower()
        try:
            if mode == "trigger":
                if options[0].lower() == "enable":
                    config["everyonetrigger"] = True
                else:
                    config["everyonetrigger"] = False
            elif mode == "react":
                if options[0].lower() == "enable":
                    config["react_to_pizza"] = True
                else:
                    config["react_to_pizza"] = False
            else:
                raise NotImplementedError(
                    "Configuration mode {0} Not Implemented".format(mode)
                )
            shared.dump_server_config(ctx.guild.id, config)
        except Exception as e:
            await ctx.send(
                _(
                    "Oops! Something went wrong! If this happens too often,"
                    " send basic information about"
                    " what you've done and this code: {0} to issue tracker"
                ).format(ctx.guild.id)
            )
            exc_info = ''.join(traceback.format_exception(e))
            shared.printe(
                "While configuring {0}, error occurred and ignored."
                "\n{1}".format(ctx.guild.id, exc_info)
            )


async def setup(bot):
    await bot.add_cog(Settings(bot))
