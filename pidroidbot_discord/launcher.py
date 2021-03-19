import asyncio
import gettext
import logging
import os
from sys import argv

from pidroidbot_discord.modules.config import get_config
from discord.ext import commands


# load config
config = get_config()
log = logging.getLogger("launcher")
# TODO : gérer numéro de versions
VERSION = "1.0.0"
log.info("*" * 60)
log.info(f" START bot-markdown-discord {VERSION} ".center(60, "*"))
log.info("*" * 60)

# i18n
gettext.install(
    "bot_markdown_discord",
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(argv[0]))), "locales"),
)
_ = gettext.gettext

bot = commands.Bot(command_prefix=config["bot"]["prefix"])


@bot.event
async def on_ready():
    log.info(f"Logged as [{bot.user.name}] with ID [{bot.user.id}]")
    await asyncio.sleep(1)
    # inventaire des serveurs auquel le bot est invité
    if config["debug"]["what_i_see"]:
        try:
            log.debug(_("Servers' list :"))
            for server in bot.guilds:
                log.debug(_("- Server {servername}").format(servername=server.name))
                log.debug(_("\t- Chans"))
                for channel in server.channels:
                    log.debug(f"\t\t{channel.id} - {channel.name}")

                log.debug(_("\t- Roles"))
                for role in server.roles:
                    log.debug(f"\t\t {role.id} - {role.name}")
        except Exception as e:
            log.error(e, exc_info=True)


def main():

    log.info("Initialization")

    try:
        log.info("Load extensions...")
        for extension in [
            f.replace(".py", "")
            for f in os.listdir("cogs")
            if os.path.isfile(os.path.join("cogs", f))
        ]:
            try:
                if extension not in config["cogs"]["list_ignore"]:
                    log.info("\t" + extension)
                    bot.load_extension("cogs" + "." + extension)
            except Exception as e:
                log.error(f'Failed to load extension "{extension}". \n', exc_info=True)

        bot.run(config["bot"]["token"])
    finally:
        pass
        # bot.db.close()

    # print("Hello world")
    # print(config)
