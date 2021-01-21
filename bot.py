#!/bin/env python3

import discord


class DiscordBotClient(discord.Client):

    def __init__(self):
        super().__init__()

    async def on_message(self, message):
        print('Saw message: {}'.format(message.content))


token = open('token.txt', 'r').read()
client = DiscordBotClient()
client.run(token)

