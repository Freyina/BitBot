"""
Nathan Meeks
Discord bot with button-based soundboard
"""

import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

import sound_paths as sp




# --- Load token ---
load_dotenv()
token = os.getenv("DISCORD_TOKEN")

# If not found, fall back to local .env file (for development)
if not token:
    load_dotenv()
    token = os.getenv("DISCORD_TOKEN")


# --- Config ---
ALLOWED_CHANNEL_ID = 763284891675656222


# --- Bot instance ---
intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='bit ', intents=intents)


# --- Soundboard buttons ---
class SoundButton(discord.ui.Button):
    def __init__(self, label, filename):
        super().__init__(label=label, style=discord.ButtonStyle.primary)
        self.filename = filename



    async def callback(self, interaction: discord.Interaction):
        vc = interaction.guild.voice_client
        if vc is None:
            await interaction.response.send_message("⚠️ Bot is not connected to a voice channel.", ephemeral=True)
            return

        file_path = sp.get_sound_path(self.filename)
        if not file_path:
            await interaction.response.send_message(f"❌ Sound '{self.filename}' not found.", ephemeral=True)
            return

        # Stop any current playback
        if vc.is_playing():
            vc.stop()

        source = discord.FFmpegPCMAudio(source=file_path)
        vc.play(source)
        await interaction.response.send_message(f"▶️ Playing **{self.filename}**", ephemeral=True)


# --- Pagination-enabled Soundboard ---
class SoundboardView(discord.ui.View):
    def __init__(self, sounds: list[str], page: int = 0):
        super().__init__(timeout=None)
        self.sounds = sounds
        self.page = page
        self.per_page = 25  # Discord limit (5 rows × 5 buttons)

        self.update_buttons()

    def update_buttons(self):
        self.clear_items()

        start = self.page * self.per_page
        end = start + self.per_page
        page_sounds = self.sounds[start:end]

        # Add sound buttons (auto-format labels)
        for sound in page_sounds:
            label = sound.replace("_", " ").title()
            self.add_item(SoundButton(label=label, filename=sound))

        # Pagination controls
        if self.page > 0:
            self.add_item(PrevPageButton(self.sounds, self.page - 1))
        if end < len(self.sounds):
            self.add_item(NextPageButton(self.sounds, self.page + 1))


class PrevPageButton(discord.ui.Button):
    def __init__(self, sounds, page):
        super().__init__(label="⬅️ Prev", style=discord.ButtonStyle.secondary)
        self.sounds = sounds
        self.page = page

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(
            content="🎵 Choose a sound:",
            view=SoundboardView(self.sounds, self.page)
        )


class NextPageButton(discord.ui.Button):
    def __init__(self, sounds, page):
        super().__init__(label="➡️ Next", style=discord.ButtonStyle.secondary)
        self.sounds = sounds
        self.page = page

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(
            content="🎵 Choose a sound:",
            view=SoundboardView(self.sounds, self.page)
        )


# --- Global check ---
@bot.check
async def globally_check_channel(ctx):
    if ctx.channel.id != ALLOWED_CHANNEL_ID:
        await ctx.send(f"Commands can only be used in <#{ALLOWED_CHANNEL_ID}>.")
        return False
    return True


# --- Events ---
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')



# If someone says hello
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('!hello'):
        await message.channel.send('Hello!')

    await bot.process_commands(message)

# --- Commands ---


# Join a channel
@bot.command(name='join')
async def join(ctx):
    if ctx.author.voice is None:
        await ctx.send("⚠️ You are not in a voice channel.")
        return
    
    channel = ctx.author.voice.channel
    await ctx.send(f"Connecting to {channel}...")
    await channel.connect()


# Leave a channel
@bot.command(name='leave')
async def leave(ctx):
    if ctx.voice_client is not None:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 Disconnected.")
    else:
        await ctx.send("⚠️ I'm not in a voice channel.")


# Play a sound
@bot.command(name='play')
async def play(ctx, filename: str):
    if ctx.voice_client is None:
        await ctx.send("⚠️ Bot is not connected to a voice channel.")
        return


    file_path = sp.get_sound_path(filename)
    if file_path is None:
        await ctx.send(f"❌ Sound '{filename}' not found.")
        return

    try:
        source = discord.FFmpegPCMAudio(source=file_path)

        def after_playing(error):
            if error:
                print(f'Player error: {error}')
            else:
                print(f'Finished playing {file_path}')

        ctx.voice_client.play(source, after=after_playing)

    except Exception as e:
        await ctx.send(f"Error playing audio: {e}")
        print(f"Error playing audio: {e}")


# Soundboard command
@bot.command(name="soundboard")
async def soundboard(ctx):
    sounds = sp.list_sounds()
    if not sounds:
        await ctx.send("⚠️ No sounds found!")
        return

    await ctx.send("🎵 Choose a sound:", view=SoundboardView(sounds))



# --- Run bot ---
bot.run(token)
