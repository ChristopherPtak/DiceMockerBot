#!/bin/env python3


##
## DiceMockerBot
## (C) 2021 Christopher Ptak
##
## A Discord bot that makes fun of low D&D rolls
##


import os
import random
import re

import discord


class RollStatus:
    IGNORE_ROLL = 0
    LOW_ROLL    = 1
    CRIT_FAIL   = 2


class DiceMockerClient(discord.Client):

    async def on_ready(self):
        print('Started DiceMockerClient')

    ##
    ## React to a message send in a public discord channel.
    ## Check to see if the message was sent by one of the supported dice bots,
    ## and if so parse the message and respond appropriately.
    ##
    async def on_message(self, message):

        if message.author.name == 'DiceParser':
            (roll, minval, maxval) = self._parse_DiceParser(message.content)
        elif message.author.name == 'Avrae':
            (roll, minval, maxval) = self._parse_Avrae(message.content)
        else:
            # Ignore all messages not from a Dice bot
            return

        status = self._judge_roll(roll, minval, maxval)
        if status != RollStatus.IGNORE_ROLL:
            await self._mock_reply(status, message.channel.send)

    ## The below functions are the individual parsers for the outputs of the
    ## various dice bots. All return a 3-tuple of the actual value of the
    ## roll, the minimum value that could have been rolled, and the maximum
    ## possible value.

    def _parse_DiceParser(self, content):

        roll = None
        minval = None
        maxval = None

        for line in content.split('\n'):
            tokens = line.split()
            if len(tokens) == 2 and tokens[0] == '#':
                roll = int(tokens[1])
            elif len(tokens) > 0 and tokens[0].startswith('Details'):

                # Get everything after 'Details:['
                expression = tokens[0][9:]

                minval = 0
                maxval = 0

                # TODO: Come up with a more sophisticated parser

                for token in re.split('[+-]', expression):

                    match = re.fullmatch('[0-9]+', token)
                    if match is not None:
                        minval += int(match.group(0))
                        maxval += int(match.group(0))
                        continue

                    match = re.fullmatch('d([0-9]+)', token)
                    if match is not None:
                        minval += 1
                        maxval += int(match.group(1))
                        continue

                    match = re.fullmatch('([0-9]+)d([0-9]+)', token)
                    if match is not None:
                        minval += int(match.group(1))
                        maxval += int(match.group(1)) * int(match.group(2))
                        continue

                    raise ValueError('Unrecognized token \'' + token
                                     + '\' in DiceParser output')

        if None in [roll, minval, maxval]:
            raise ValueError('Unable to find all parts of DiceParser output')

        return (roll, minval, maxval)

    def _parse_Avrae(self, content):

        roll = None
        minval = None
        maxval = None

        for line in content.split('\n'):
            tokens = line.split()
            if len(tokens) == 2 and tokens[0] == '**Total**:':
                roll = int(tokens[1])
            elif len(tokens) > 0 and tokens[0] == '**Result**:':

                # Get everything after '**Result**:'
                expression = line[12:]

                minval = 0
                maxval = 0

                # TODO: Come up with a more sophisticated parser
                # TODO: Reduce code duplication with the above method

                for token in re.split('[+-]', expression):

                    stoken = token.strip()

                    match = re.fullmatch('[0-9]+', stoken)
                    if match is not None:
                        minval += int(match.group(0))
                        maxval += int(match.group(0))
                        continue

                    match = re.fullmatch('([0-9]+)d([0-9]+) \\(.*\\)', stoken)
                    if match is not None:
                        minval += int(match.group(1))
                        maxval += int(match.group(1)) * int(match.group(2))
                        continue

                    raise ValueError('Unrecognized token \'' + token
                                     + '\' in Avrae output')

        if None in [roll, minval, maxval]:
            raise ValueError('Unable to find all parts of Avrae output')

        return (roll, minval, maxval)

    ##
    ## Categorize a roll based on the three parameters from the parsers.
    ## Returns either IGNORE_ROLL, LOW_ROLL, or CRIT_FAIL.
    ##
    def _judge_roll(self, roll, minval, maxval):

        if (maxval - minval) < 3:
            # Ignore trivial rolls
            return RollStatus.IGNORE_ROLL

        if roll == minval:
            return RollStatus.CRIT_FAIL
        if roll < maxval * 0.25:
            # Anything below 25% of the max is considered a low roll
            return RollStatus.LOW_ROLL
        else:
            # All other rolls should be ignored
            return RollStatus.IGNORE_ROLL

    ##
    ## Given a category of reply and a callback function to send a message,
    ## choose an appropriate taunt and send it using the callback function.
    ##
    async def _mock_reply(self, status, send):

        if status == RollStatus.CRIT_FAIL and random.random() < 0.25:

            # Have a 25% chance to send a tutorial link on a crit fail
            embed = discord.Embed(url='https://dnd.wizards.com/get-started',
                                  title='D&D for Beginners',
                                  description=('New to Dungeons & Dragons? ' +
                                               'We\'ll walk you through '    +
                                               'options that introduce and ' +
                                               'teach the game, and help '   +
                                               'get you started!'))

            await send('Maybe this will help you', embed=embed)

        else:

            # Create a random taunt from these choices
            laugh = random.choice(['haha', 'lol', 'lmao', '😂'])
            insult = random.choice(['loser', 'idiot', 'fool'])

            # 33% chance to just send a laugh but not an insult
            if random.random() < 0.33:
                await send(laugh)
            else:
                await send(laugh + ' ' + insult)


token = open('token.txt', 'r').read()

client = DiceMockerClient()
client.run(token)

