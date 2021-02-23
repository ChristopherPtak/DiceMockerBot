#!/bin/env python3

import os
import random

import discord


class RollStatus:
    IGNORE_ROLL = 0
    LOW_ROLL    = 1
    CRIT_FAIL   = 2


class DiceMockerClient(discord.Client):

    async def on_ready(self):
        print('Started DiceMockerClient')

    async def on_message(self, message):

        if message.author.name == 'DiceParser':
            roll = self._parse_DiceParser(message.content)
        elif message.author.name == 'Avrae.avrae':
            roll = self._parse_Avrae(message.content)
        else:
            # Ignore all messages not from a Dice bot
            return

        if roll != RollStatus.IGNORE_ROLL:
            await self._mock_reply(roll, message.channel.send)

    def _parse_DiceParser(self, content):

        value_line = content.split('\n')[1]
        final_value = int(value_line.split()[1])

        # TODO: Implement a calculation of these quantities
        min_possible_value = 0
        max_possible_value = 1

        if max_possible_value == min_possible_value:
            # Ignore trivial rolls like a d0 or d1
            return RollStatus.IGNORE_ROLL

        if final_value == min_possible_value:
            return RollStatus.CRIT_FAIL
        if final_value <= max_possible_value * 0.25:
            # Anything below 25% of the max is considered a low roll
            return RollStatus.LOW_ROLL
        else:
            # All other rolls should be ignored
            return RollStatus.IGNORE_ROLL

    def _parse_Avrae(self, content):
        # TODO: Implement this function
        return RollStatus.IGNORE_ROLL

    async def _mock_reply(self, roll, send):

        if roll == RollStatus.LOW_ROLL:

            # Create a random taunt from these choices
            laugh = random.choice(['haha', 'lol', 'lmao', '😂'])
            insult = random.choice(['loser', 'idiot', 'fool'])

            if random.random() < 0.33:
                await send(laugh)
            else:
                await send(laugh + ' ' + insult)

        elif roll == RollStatus.CRIT_FAIL:

            # Send a tutorial link when someone crit fails
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

