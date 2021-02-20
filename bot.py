#!/bin/env python3

import os
import random

import discord


class DiceMockerClient(discord.Client):

    insult_list = [ 'lmao'
                  , 'lmao idiot'
                  , 'lmao loser'
                  , 'haha'
                  , 'haha idiot'
                  , 'haha loser'
                  , 'lol'
                  , 'lol idiot'
                  , 'lol loser'
                  , 'nice one'
                  , 'nice one BUDDY'
                  , 'ladies and gentlemen, we have a winner'
                  ]

    async def on_ready(self):
        print('Started DiceMockerClient')

    async def on_message(self, message):

        if message.author.name != 'DiceParser':
            return

        lines = message.content.split('\n')
        actual_roll_value = int(lines[1].split()[1])

        if actual_roll_value <= 2:
            insult = random.choice(DiceMockerClient.insult_list)
            await message.channel.send(insult)


token = open('token.txt', 'r').read()

client = DiceMockerClient()
client.run(token)

