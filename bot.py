#!/bin/env python3

import os
import random

import discord


class RollStatus:
    NORMAL_ROLL = 0
    LOW_ROLL    = 1
    CRIT_FAIL   = 2


class DiceMockerClient(discord.Client):

    async def on_ready(self):
        print('Started DiceMockerClient')

    async def on_message(self, message):

        if message.author.name == 'DiceParser':
            roll = self._parse_DiceParser(message.content)
        else:
            # Ignore all messages not from a Dice bot
            return

        if roll != RollStatus.NORMAL_ROLL:
            await self._mock_reply(roll, message.channel.send)

    def _parse_DiceParser(self, content):

        roll_line = content.split('\n')[1]
        actual_roll_value = int(roll_line.split()[1])

        if actual_roll_value == 1:
            return RollStatus.CRIT_FAIL
        if actual_roll_value <= 5:
            # Consider anything below 5 "low"
            # TODO: Replace with percentage of maximum
            return RollStatus.LOW_ROLL
        else:
            return RollStatus.NORMAL_ROLL

    async def _mock_reply(self, roll, send):

        if roll == RollStatus.LOW_ROLL:

            laugh = random.choice(['haha', 'lol', 'lmao', '😂'])
            insult = random.choice(['loser', 'idiot', 'fool'])

            if random.random() < 0.33:
                await send(laugh)
            else:
                await send(laugh + ' ' + insult)

        elif roll == RollStatus.CRIT_FAIL:

            embed = discord.Embed(url='https://dnd.wizards.com/get-started',
                                  title='D&D for Beginners',
                                  description=('New to Dungeons & Dragons? ' +
                                               'We\'ll walk you through '    +
                                               'options that introduce and ' +
                                               'teach the game, and help '   +
                                               'get you started!'))

            await send('Maybe this will help you', embed=embed)


token = open('token.txt', 'r').read()

client = DiceMockerClient()
client.run(token)

