#!/bin/env python3

import os
import discord


class DiceMockerClient(discord.Client):

    async def on_ready(self):
        print('Started DiceMockerClient')

    async def on_message(self, message):

        if message.author.name != 'DiceParser':
            return

        lines = message.content.split('\n')
        roll_value = int(lines[1].split()[1])

        if roll_value <= 2:
            await message.channel.send('lmao loser')


token = open('token.txt', 'r').read()

client = DiceMockerClient()
client.run(token)

