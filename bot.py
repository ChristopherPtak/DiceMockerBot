#!/bin/env python3

# Standard library imports
import os
import sqlite3

# Import discord API
import discord


##
## A client class for this specific discord bot.
##
## Extends discord.Client and overrides event handlers.
## This template also creates a data directory and a database connection for
## bot-specific data. For example, a bot may need to remember which users it
## has interacted with, or keep settings for how to behave on each server.
##

class DiscordBotClient(discord.Client):

    def __init__(self):

        # Call discord.Client constructor
        super().__init__()

        # Create data directory if it does not exist
        if not os.path.isdir('data'):
            os.mkdir('data')

        # Create or open a database for bot data
        self.database = sqlite3.connect('data/bot.db')


    ##
    ## Example event handlers
    ##

    # Event handler for bot startup
    async def on_ready(self):
        print('Ready!')

    # Event handler for a text-channel message
    async def on_message(self, message):
        print('Saw message: {}'.format(message.content))


# Read the token from a file
token = open('token.txt', 'r').read()

# Run the bot
client = DiscordBotClient()
client.run(token)

