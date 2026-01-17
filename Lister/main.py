import discord
from discord.ext import commands
import json
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

FILE_PATH = "lists.json"
bot_token=os.getenv("bot_token")
# Load existing lists or initialize an empty dictionary
try:
    with open(FILE_PATH, "r") as file:
        lists = json.load(file)
except (json.JSONDecodeError, FileNotFoundError):
    lists = {}


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")


@bot.command(name="create")
async def create_list(ctx, name):
    if name not in lists:
        lists[name] = {"tasks": [], "message": None}
        await ctx.send(f"List `{name}` created!")
        # Save lists to a file after adding a new task
        await save_lists(ctx)

    else:
        await ctx.send(f"A list with the name `{name}` already exists!")


@bot.command(name="add")
async def add_task(ctx, name, *, task):
    if name in lists:
        lists[name]["tasks"].append(task)

        if "message" in lists[name] and lists[name]["message"]:
            await update_message(name)
        else:
            channel = ctx.channel
            tasks = "\n".join(lists[name]["tasks"])
            list_content = f"**{name}**\n{tasks}"
            message = await channel.send(list_content)
            lists[name]["message"] = (channel.id, message.id)

        await ctx.send(f"Task added to the list `{name}`!")
        # Save lists to a file after adding a new task
        await save_lists(ctx)

    else:
        await ctx.send(f"List `{name}` not found! Create it using !create command.")


@bot.command(name="complete")
async def complete_task(ctx, name, task_number: int):
    task_number -= 1
    if name in lists and 0 <= task_number < len(lists[name]["tasks"]):
        task_to_complete = lists[name]["tasks"][task_number]
        lists[name]["tasks"][task_number] = f'~~{lists[name]["tasks"][task_number]}~~'
        await update_message(name)
        await ctx.send(
            f"`{task_number}. {task_to_complete}` marked as completed in the list `{name}`!"
        )
        # Save lists to a file after adding a new task
        await save_lists(ctx)

    else:
        await ctx.send(f"List `{name}` not found or invalid task number!")


async def update_message(name):
    channel_id, message_id = lists[name]["message"]
    channel = bot.get_channel(channel_id)
    message = await channel.fetch_message(message_id)

    tasks = "\n".join(
        [f"{i + 1}. {task}" for i, task in enumerate(lists[name]["tasks"])]
    )
    updated_content = f"**{name}**\n{tasks}"

    await message.edit(content=updated_content)
    lists[name]["message"] = (channel.id, message.id)


@bot.command(name="remove")
async def remove_task(ctx, name, task_number: int):
    task_number -= 1
    if name in lists and 0 <= task_number < len(lists[name]["tasks"]):
        task_to_remove = lists[name]["tasks"][task_number]
        del lists[name]["tasks"][task_number]
        await update_message(name)
        await ctx.send(
            f"`{task_number + 1}. {task_to_remove}`  removed from the list `{name}`!"
        )
        # Save lists to a file after adding a new task
        await save_lists(ctx)

    else:
        await ctx.send(f"List `{name}` not found or invalid task number!")


@bot.command(name="lists")
async def view_lists(ctx):
    list = "\n".join([f"{i + 1}. {name}" for i, name in enumerate(lists.keys())])
    await ctx.send(f"Available Lists:\n{list}")


@bot.command(name="delete")
async def delete_list(ctx, name):
    if name in lists:
        del lists[name]
        await ctx.send(f"List `{name}` deleted!")
        # Save Lists to a file after adding a new task
        await save_lists(ctx)

    else:
        await ctx.send(f"List `{name}` not found!")


@bot.command(name="clear")
async def clear_list(ctx, name):
    if name in lists:
        lists[name]["tasks"] = []
        await update_message(name)
        await ctx.send(f"List `{name}` cleared!")
        # Save Lists to a file after adding a new task
        await save_lists(ctx)
    else:
        await ctx.send(f"List `{name}` not found!")


@bot.command(name="show")
async def show_list(ctx, name):
    if name in lists:
        if "message" in lists[name] and lists[name]["message"]:
            channel_id, message_id = lists[name]["message"]
            channel = bot.get_channel(channel_id)

            if channel:
                try:
                    message = await channel.fetch_message(message_id)
                    tasks = "\n".join(
                        [
                            f"{i + 1}. {task}"
                            for i, task in enumerate(lists[name]["tasks"])
                        ]
                    )
                    list_content = f"**{name}**\n{tasks}"
                    await ctx.send(list_content)

                except discord.NotFound:
                    await ctx.send("Message not found. Maybe it was deleted.")
            else:
                await ctx.send("Channel not found.")
        else:
            await ctx.send("No message associated with the list.")
    else:
        await ctx.send(f"List `{name}` not found.")


class CustomHelpCommand(commands.DefaultHelpCommand):
    async def send_bot_help(self, mapping):
        help_message = (
            "**!create <name>** - Creates a new list with the given name.\n"
            "**!add <name> <task>** - Adds a task to the specified list.\n"
            "**!complete <name> <task_number>** - Marks a task as completed in the specified list.\n"
            "**!lists** - Displays the names of all available lists.\n"
            "**!delete <name>** - Deletes the specified list.\n"
            "**!clear <name>** - Clears all tasks from the specified list.\n"
            "**!show <name>** - Shows the tasks of the specified list.\n"
            "**!remove <name> <task_number>** - Removes a task from the specified list.\n"
            "**!help** - Displays this help message.\n"
            "**!save_lists** - Saves the current state of lists.\n"
        )
        await self.get_destination().send(help_message)


bot.help_command = CustomHelpCommand()


# Add a command to save the lists before shutting down the bot
@bot.command(name="save_lists")
async def save_lists(ctx=None):
    # Save todo_lists to a file
    with open(FILE_PATH, "w") as file:
        json.dump(lists, file)

    # if ctx:
    #     await ctx.send("Todo lists saved successfully!")


# Ensure the bot saves the lists when it is stopped
@bot.event
async def on_disconnect():
    with open(FILE_PATH, "w") as file:
        json.dump(lists, file)


bot.run(bot_token)
