import discord

# Replace with your bot token obtained from Discord Developer Portal
bot_token = "MTIyMzM3MzI4MDgyNDY1NTkwMg.GVt4lm._afQ4VWVLvNaRHVkdrCwUWUWMrELZiNBrPdVrc"

# Intents for your bot
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

# Data structure to store to-do items and their completion status (True/False)
# Consider using a database for persistence in larger projects
to_do_list = {}

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')

@client.event
async def on_message(message):
    if message.author == client.user:
        return  # Ignore messages from the bot itself

    prefix = "!"  # Customize the command prefix here (e.g., "todo!")

    # Check for greetings
    if any(word in message.content.lower() for word in ["hi", "hello"]):
        await message.channel.send("Hello! I'm a to-do list bot. You can use the following commands:\n"
                                "!add: Add tasks to your to-do list.\n"
                                "!done: Mark tasks as completed.\n"
                                "!list: View your to-do list and progress.")
        return  # Exit the function after sending the response

    # Command to add multiple tasks
    if message.content.startswith(f"{prefix}add"):
        tasks = message.content.split(maxsplit=1)[1].strip()
        added_tasks = 0
        for task in tasks.splitlines():
            if task.lower() != "done":
                to_do_list[task] = False
                added_tasks += 1
        await message.channel.send(f"Added {added_tasks} tasks to your to-do list!")

    # Command to mark tasks as done
    elif message.content.startswith(f"{prefix}done"):
        numbers = message.content.split(maxsplit=1)[1].strip().split()
        marked_tasks = 0
        for number in numbers:
            try:
                index = int(number) - 1  # Convert to 0-based index
                task = list(to_do_list.keys())[index]
                if task in to_do_list:
                    to_do_list[task] = True
                    marked_tasks += 1
                    await message.channel.send(f"Marked '{task}' as done!")
                else:
                    await message.channel.send(f"Task number {number} not found in your list.")
            except (ValueError, IndexError):
                await message.channel.send(f"Invalid task number: {number}")
        if marked_tasks > 0:
            await update_progress(to_do_list, message.channel)  # Update progress after marking done

    # Command to display to-do list and progress
    elif message.content.startswith(f"{prefix}list"):
        await view_list(message.channel)

async def update_progress(todo_list, channel):
    """Calculates and sends a message with the current progress."""
    completed = sum(value for value in todo_list.values())
    total = len(todo_list)
    progress = (completed / total) * 100
    await channel.send(f"Progress: {progress:.2f}% ({completed}/{total} tasks completed)")

async def view_list(channel):
    """Displays the to-do list and progress in the channel."""
    if not to_do_list:
        await channel.send("Your to-do list is empty.")
        return
    completed_tasks = sum(1 for task in to_do_list.values() if task)
    total_tasks = len(to_do_list)
    progress = (completed_tasks / total_tasks) * 100
    message_content = "**To-Do List:**\n"
    for i, (task, done) in enumerate(to_do_list.items(), start=1):
        status = "✅" if done else "❌"
        message_content += f"{status} {task}\n"
    message_content += f"\nProgress: {progress:.2f}% ({completed_tasks}/{total_tasks})"
    await channel.send(message_content)

client.run(bot_token)