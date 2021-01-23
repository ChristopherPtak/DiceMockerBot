
# DiscordBotTemplate

A simple template for creating Discord bots.

## About

Discord bots are simple to make, but they still involve a small amount of
boilerplate code for logging into Discord and keeping persistent data between
different servers and executions of the bot. This template provides a minimal
base with a token-reading mechanism and a database to facilitate making simple
Discord bots.

## Usage

You probably want to fork this repository and modify the code in order to
create your own bot. After you have done that, the steps to run the bot are as
follows:

1. Install all prerequisites. You will need a working Python implementation
   and the `discord` package, which can be installed with
   `pip3 install --user discord`. It is recommended that you install the
   discord module as a non-privileged user, possibly one created to run the
   bot. All other modules are part of the Python standard library.

2. Create a bot account at the
   [Discord Applications page](https://discord.com/developers/applications).

3. From the bot account page, use the provided link to add the bot to your
   server. You may want to create a test server to run the bot before
   releasing it into the wild.

4. After setting the appropriate permissions, get the token you have created
   for the bot and place it in the file `token.txt`.

Now you can run the bot using `python3 bot.py`. Check to make sure the bot has
logged into your server, and enjoy!

