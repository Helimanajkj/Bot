import discord
from discord.ext import commands
from datetime import timedelta
import os
from dotenv import load_dotenv
from keep_alive import keep_alive

# Load environment variables from .env file
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

MUTE_DURATION_SECONDS = 12 * 60 * 60  # 12 ώρες
PRIVATE_CHANNEL_NAME = "🔒private"


@bot.event
async def on_ready():
    print(f"🤖 Bot is online ως {bot.user}")


@bot.event
async def on_message(message):
    # Αγνοούμε τα μηνύματα από bots
    if message.author.bot:
        return

    # Αγνοούμε διαχειριστές
    if message.author.guild_permissions.administrator:
        return

    # Αν το μήνυμα περιέχει invite link
    if "discord.gg/" in message.content.lower():
        try:
            # Διαγραφή μηνύματος
            await message.delete()

            duration = timedelta(seconds=MUTE_DURATION_SECONDS)
            await message.author.timeout(duration,
                                         reason="Invite link detected")

            print(f"⏳ Timeout applied to {message.author}")

            # Βρες το κανάλι που θα στείλεις το μήνυμα
            private_channel = discord.utils.get(message.guild.text_channels,
                                                name=PRIVATE_CHANNEL_NAME)
            if private_channel:
                await private_channel.send(
                    f"⛔ {message.author.mention} έστειλε invite link και έχει timeout για 12 ώρες."
                )
            else:
                print(f"❌ Δεν βρέθηκε το κανάλι {PRIVATE_CHANNEL_NAME}")

        except discord.Forbidden:
            print("❌ Δεν έχω δικαιώματα για timeout αυτού του μέλους.")
        except Exception as e:
            print(f"❌ Σφάλμα κατά το timeout: {e}")

    await bot.process_commands(message)


if __name__ == "__main__":
    token = os.environ.get("TOKEN")
    if not token:
        print("❌ Δεν βρέθηκε το TOKEN στο περιβάλλον! Βάλε το στο .env")
    else:
        keep_alive()
        bot.run(token)
