import discord
from discord.ext import commands
import io

@commands.command(aliases=['fd', "format_data"])
async def format_data_command(ctx):
    if not ctx.message.attachments:
        await ctx.send("Please attach a `.txt` file with the command.")
        return

    # Get the attached file
    attachment = ctx.message.attachments[0]
    if not attachment.filename.endswith('.txt'):
        await ctx.send("Only `.txt` files are supported.")
        return

    # Read the content of the file
    file_content = await attachment.read()
    input_data = file_content.decode('utf-8')

    # Define the format_data function
    def format_data(input_data):
        words_to_remove = [":generalist:", ":ninja:", ":healer:", ":warrior:"]
        words_to_replace = {
            ":Worn:": "<:Pristine:830383264572243978>",
            ":Great:": "<:Pristine:830383264572243978>",
            ":Pristine:": "<:Pristine:830383264572243978>",
            ":Good:": "<:Pristine:830383264572243978>",
            ":Scarred:": "<:Pristine:830383264572243978>"
        }
        placeholder = "<TEMP_PLACEHOLDER>"

        formatted_output = ""
        for line in input_data.split("\n"):
            if "discord.com" in line:
                formatted_output += f"\n{line}\n\n"
            elif line.strip():
                for word in words_to_remove:
                    line = line.replace(word, "")
                for key in words_to_replace.keys():
                    line = line.replace(key, placeholder)
                line = line.replace(placeholder, words_to_replace[":Pristine:"])
                formatted_output += line + "\n"

        return formatted_output.strip()

    # Format the input data
    formatted_output = format_data(input_data)

    # Create a file-like object for the output
    output_file = io.BytesIO(formatted_output.encode('utf-8'))
    output_file.name = "formatted_output.txt"

    # Send the output file
    await ctx.send("Here is the formatted output:", file=discord.File(output_file))

# Add the command to the bot
