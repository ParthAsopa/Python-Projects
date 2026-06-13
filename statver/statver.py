import discord
from discord.ext import tasks
import psutil
import os
import datetime
from dotenv import load_dotenv

# Load the environment variables from the hidden .env file
load_dotenv()

# Securely pull configuration into the script
TOKEN = os.getenv('STATVER_DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('STATVER_CHANNEL_ID')) 
STORAGE_PATH = os.getenv('STATVER_STORAGE_PATH')
SERVER_MANAGER_ID = int(os.getenv('SERVER_MANAGER_ID'))

class StatverBot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.status_message = None
        self.bat_message=None
        self.case_20=False
        self.case_15=False

    async def setup_hook(self):
        self.update_dashboard.start()

    async def on_ready(self):
        print(f'Logged in as {self.user} - Statver Telemetry Online')

    async def get_battery(self):
        try:
            with open('/sys/class/power_supply/BAT0/capacity', 'r') as f:
                cap = f.read().strip()
            with open('/sys/class/power_supply/BAT0/status', 'r') as f:
                status = f.read().strip()

            channel = self.get_channel(CHANNEL_ID)
            # If we don't have a channel reference, bail out gracefully
            if not channel:
                return f"{cap}% [{status}]"

            cap_int = int(cap)
            if cap_int <= 20 and status == "Discharging":
                message = f"<@{SERVER_MANAGER_ID}> Battery low!! Only {cap}% left!!"

                # Handle specific one-off alerts and avoid double-sends
                if cap_int == 20:
                    if not self.case_20:
                        if self.bat_message:
                            try:
                                await self.bat_message.delete()
                            except Exception:
                                pass
                        self.bat_message = await channel.send(message)
                        self.case_20 = True
                elif cap_int == 15:
                    if not self.case_15:
                        if self.bat_message:
                            try:
                                await self.bat_message.delete()
                            except Exception:
                                pass
                        self.bat_message = await channel.send(message)
                        self.case_15 = True
                elif cap_int <= 10:
                    if self.bat_message:
                        try:
                            await self.bat_message.delete()
                        except Exception:
                            pass
                    self.bat_message = await channel.send(message)
            else:
                if self.bat_message:
                    try:
                        await self.bat_message.delete()
                    except Exception:
                        pass
                self.bat_message = None
                self.case_20 = False
                self.case_15 = False

            return f"{cap}% [{status}]"
        except FileNotFoundError:
            return "Battery data unavailable"

    def get_temperature(self):
        try:
            with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
                temp_c = int(f.read().strip()) / 1000
            return f"{temp_c:.1f}°C"
        except FileNotFoundError:
            return "N/A"

    @tasks.loop(minutes=2)
    async def update_dashboard(self):
        channel = self.get_channel(CHANNEL_ID)
        if not channel:
            print("Error: Statver could not find the specified Discord channel.")
            return

        # System Metrics
        ram = psutil.virtual_memory()
        cpu = psutil.cpu_percent(interval=1)
        
        # Calculate Exact Uptime
        boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.datetime.now() - boot_time
        uptime_str = str(uptime).split('.')[0]  # Formats neatly to Hours:Minutes:Seconds
        
        # Storage Metrics
        try:
            disk = psutil.disk_usage(STORAGE_PATH)
            free_gb = disk.free / (1024**3)
            total_gb = disk.total / (1024**3)
            storage_str = f"{free_gb:.1f} GB Free of {total_gb:.1f} GB"
        except FileNotFoundError:
            storage_str = f"Path '{STORAGE_PATH}' not found."

        # Build Statver Discord Embed
        embed = discord.Embed(
            title="🟢 Statver Live Telemetry", 
            color=0x00ff00,
            timestamp=discord.utils.utcnow()  # Injects the exact local refresh time
        )
        embed.add_field(name="System Uptime", value=uptime_str, inline=False)
        embed.add_field(name="CPU Usage", value=f"{cpu}%", inline=True)
        embed.add_field(name="RAM Usage", value=f"{ram.percent}%", inline=True)
        embed.add_field(name="Temperature", value=self.get_temperature(), inline=True)
        embed.add_field(name="Cloud Storage", value=storage_str, inline=False)
        embed.add_field(name="Power Supply", value=await self.get_battery(), inline=False)
        embed.set_footer(text="Statver Heartbeat")

        # Edit existing message or send a new one
        if self.status_message:
            try:
                await self.status_message.edit(embed=embed)
            except discord.NotFound:
                self.status_message = await channel.send(embed=embed)
        else:
            await channel.purge(limit=5)
            self.status_message = await channel.send(embed=embed)

    @update_dashboard.before_loop
    async def before_update(self):
        await self.wait_until_ready()

# Initialize and run the Statver client
statver_client = StatverBot()
statver_client.run(TOKEN)
