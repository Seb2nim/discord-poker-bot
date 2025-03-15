import os
import traceback

import discord
import asyncio
from discord.ext import commands, tasks

from poker_game import PokerGame

# Récuperation du token du bot depuis les variables d'environement
TOKEN_BOT = os.environ['TOKEN_BOT']

# Définir les intentions du bot
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.members = True

class PokerBot(commands.Bot):
    """Bot personnalisé avec une instance de PokerGame."""
    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.game = PokerGame(self)  # Création de l'instance de PokerGame


bot = PokerBot(command_prefix="$", intents=intents)
client = discord.Client(intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")

@bot.event
async def on_command_error(ctx, error):
    """Gestionnaire global des erreurs des commandes."""
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Cette commande n'existe pas.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("⚠️ Il manque un argument à la commande.")
    elif isinstance(error, AttributeError):
        print(f"❌ Erreur : {error}")  # Affiche l'erreur dans la console
        error_traceback = "".join(traceback.format_exception(type(error), error, error.__traceback__))
        print(error_traceback)  # Affiche la trace complète dans la console
        await ctx.send("⚠️ Une erreur interne s'est produite.")
    else:
        print(f"🔴 Erreur inconnue : {error}")  # Affiche toute autre erreur
        error_traceback = "".join(traceback.format_exception(type(error), error, error.__traceback__))
        print(error_traceback)  # Affiche la trace complète dans la console
        await ctx.send("⚠️ Une erreur inattendue est survenue.")

# Chargement des extensions (Cog), approche asynchrone
async def load_extensions():
    await bot.load_extension("db_manager")
    await bot.load_extension("economy_manager")
    await bot.load_extension("bot_commands")

async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN_BOT)

# Démarrage du bot en async
asyncio.run(main())
