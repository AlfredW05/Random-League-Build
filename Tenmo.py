import os
import discord
from discord.ext import commands
import json
import random

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.members = True

ITEMS_FILE = "D:/Python projects/Tenmo/items.json"
TOKEN = "MTIwMDc4MDY3MzM1NTYxNjM3OQ.GLOdqm.aSCl_j-bowdNARLxQUUWaoCGXu3gGzfAjlb5wI"  # Replace with your actual bot token
IMAGES_FOLDER = "D:/Python projects/Tenmo/League champs folder"  # Update this path
RUNES_FOLDER = "D:/Python projects/Tenmo/Runes"  # Path to your "Runes" folder


def read_token(file_name):
    with open(file_name, 'r') as token_file:
        return token_file.read().strip()

TOKEN_FILE = 'D:\Python projects\Tenmo\TenmoToken.txt'
TOKEN = read_token(TOKEN_FILE)


# Load the item list from the JSON file
with open(ITEMS_FILE, "r") as items_file:
    item_data = json.load(items_file)

item_list = item_data["items"]

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user.name}")

# Function to get a random image from a specified folder
def get_random_image(folder_path, file_extension=".jpg"):
    image_files = [f for f in os.listdir(folder_path) if f.endswith(file_extension)]
    if not image_files:
        print(f"No {file_extension} images found in the folder.")
        return None
    random_image_filename = random.choice(image_files)
    image_name = os.path.splitext(random_image_filename)[0]
    return {"name": image_name, "path": os.path.join(folder_path, random_image_filename)}

@bot.command(name="Random", aliases=["random", "RANDOM"])
async def random_build(ctx):
    champion_image = get_random_image(IMAGES_FOLDER)
    rune_image = get_random_image(RUNES_FOLDER, file_extension=".png")  # Assuming your rune images are .png
    if champion_image and rune_image:
        # Shuffle the item list to randomize the order
        random.shuffle(item_list)
        
        # Remove duplicate items while preserving the original order
        unique_items = []
        for item in item_list:
            if item not in unique_items:
                unique_items.append(item)

        # Initialize a counter for "no type" items
        no_type_counter = 1
        
        # Initialize the list of random items
        random_items = []

        # Inside the loop that selects random items
        while len(random_items) < 6:
            # Select a random item from the list
            random_item = random.choice(unique_items)
            
            # If the item has no type, assign a unique identifier
            if not random_item.get("type"):
                random_item["type"] = f"No Type {no_type_counter}"
                no_type_counter += 1
            
            # Add the selected item to the random_items list
            random_items.append(random_item)
            unique_items.remove(random_item)

        # Construct the embed
        embed = discord.Embed(
            title="Random Champion Build",
            color=discord.Color.green()  # Customize the color as needed
        )

        # Set the champion name as the embed title in the top left
        embed.title = champion_image['name']

        # Set the champion image within the embed
        embed.set_image(url=f"attachment://{champion_image['name']}.jpg")

        # Set the rune image within the embed as a thumbnail
        embed.set_thumbnail(url=f"attachment://{rune_image['name']}.png")

        # Add the random items in a row below, excluding the type
        item_list_str = "\n".join([item['name'] for item in random_items])
        embed.add_field(name="Random Items", value=item_list_str)

        # Send the embed with both champion and rune images
        files = [
            discord.File(champion_image['path'], filename=f"{champion_image['name']}.jpg"),
            discord.File(rune_image['path'], filename=f"{rune_image['name']}.png")
        ]
        await ctx.send(embed=embed, files=files)
    else:
        await ctx.send("Failed to fetch champion or rune information.")

bot.run(TOKEN)
