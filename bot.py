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
    ## TODO: Add logging functionality to bot
    ##
    async def on_message(self, message):

        if message.content.strip() == '!mock':
            await self._mock_reply(RollStatus.LOW_ROLL, message.channel.send)

        if message.author.name == 'DiceParser':
            roll = self._parse_DiceParser(message)
        elif message.author.name == 'Avrae':
            roll = self._parse_Avrae(message)
        else:
            # Ignore all other messages not from a Dice bot
            return

        if roll is None:
            return

        (val, minval, maxval) = roll

        status = self._judge_roll(val, minval, maxval)
        if status != RollStatus.IGNORE_ROLL:
            await self._mock_reply(status, message.channel.send)

    ## The below functions are the individual parsers for the outputs of the
    ## various dice bots. All return a 3-tuple of the actual value of the
    ## roll, the minimum value that could have been rolled, and the maximum
    ## possible value.

    ##
    ## Message parser for the DiceParser bot
    ##
    ## TODO: Come up with a more sophisticated parser
    ## TODO: Add some sort of check for errors or log them?
    ##
    def _parse_DiceParser(self, message):

        content = message.content

        val = None
        minval = None
        maxval = None

        for line in content.split('\n'):
            tokens = line.split()
            if len(tokens) == 2 and tokens[0] == '#':
                val = int(tokens[1])
            elif len(tokens) > 0 and tokens[0].startswith('Details'):

                # Get everything after 'Details:['
                expression = tokens[0][9:]

                minval = 0
                maxval = 0

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

        if None in [val, minval, maxval]:
            # This is probably a DiceParser error message
            return

        return (val, minval, maxval)

    ##
    ## Message parser for the Avrae bot
    ##
    ## TODO: Come up with a more sophisticated parser
    ## TODO: Reduce code duplication with the parser for DiceParser
    ##
    def _parse_Avrae(self, message):
        if len(message.embeds) > 0:
            # Ignore other embeds if there are more than 1
            return self._parse_Avrae_character(message.embeds[0])
        else:
            return self._parse_Avrae_generic(message.content)

    def _parse_Avrae_character(self, embed):

        tokens = embed.description.split('=')

        if len(tokens) != 2:
            # Ignore message if the embed does not contain a roll
            return

        # Remove excess chars from the tokens
        expression = tokens[0].strip()
        total = tokens[1].strip()[1:-1]

        return self._parse_Avrae_expression(expression, total)

    def _parse_Avrae_generic(self, content):

        expression = None
        total = None

        for line in content.split('\n'):
            tokens = line.split()
            if len(tokens) == 2 and tokens[0] == '**Total**:':
                total = tokens[1]
            elif len(tokens) > 0 and tokens[0] == '**Result**:':
                # Get everything after '**Result**:'
                expression = line[12:]

        if None in [expression, total]:
            # This is not an error because Avrae has
            # outputs other than dice rolls
            return

        return self._parse_Avrae_expression(expression, total)

    def _parse_Avrae_expression(self, expression, total):

        val = int(total.strip())

        minval = 0
        maxval = 0


        for token in re.split('[+-]', expression.strip()):

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

        return (val, minval, maxval)

    ##
    ## Categorize a roll based on the three parameters from the parsers.
    ## Returns either IGNORE_ROLL, LOW_ROLL, or CRIT_FAIL.
    ##
    def _judge_roll(self, val, minval, maxval):

        if (maxval - minval) < 3:
            # Ignore trivial rolls
            return RollStatus.IGNORE_ROLL

        if val == minval:
            return RollStatus.CRIT_FAIL
        if val < maxval * 0.25:
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

