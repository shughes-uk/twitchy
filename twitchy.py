import time
import imp
import os
<<<<<<< HEAD
import traceback
=======
>>>>>>> 2aee655cb4e97922c93c6c1525c6eac75263d628
import re
import inspect
from plugins.BasePlugin import BasePlugin
from twitchchat import twitch_chat
<<<<<<< HEAD
=======
import logging
import argparse
from yaml import load
logger = logging.getLogger('twitchy')

>>>>>>> 2aee655cb4e97922c93c6c1525c6eac75263d628
# Twitchy
# An IRC bot designed for Twitch.TV streams
#
# Please see the README for instructions on using Twitchy.
# It is released under the BSD license; the full license
# available in the LICENSE file.

<<<<<<< HEAD
# CONFIGURATION
Twitch_Username = 'Collectablecat'  # Twitch.TV username for the bot, must be a registered username!
Twitch_Password = 'oauth:7ps3sw9l3wn3rhljnmtlhlbm8oedas'  # OAuth for above Twitch.TV account, http://www.twitchapps.com/tmi/
Twitch_Channel = 'animaggus'  # Twitch.TV channel to connect to

# NOW DON'T TOUCH ANYTHING ELSE, UNLESS YOU KNOW WHAT YOU'RE DOING
=======
>>>>>>> 2aee655cb4e97922c93c6c1525c6eac75263d628

class Twitchy:

<<<<<<< HEAD

class Twitchy:

    def __init__(self):

        self.connected = False
        # Plugin system loosely based on blog post by lkjoel
        # http://lkubuntu.wordpress.com/2012/10/02/writing-a-python-plugin-api/
        self.twitch_chat = twitch_chat(Twitch_Username, Twitch_Password, [Twitch_Channel])
        self._pluginFolder = './plugins/'
        self._mainModule = 'plugin'
        self._plugins = []  # used for cleanup
        self.commands = []
        self.triggers = []
        self.joinPartHandlers = []
        self.modHandlers = []
        self.ignoredUsers = []
        self.loadedPluginNames = []
        self.spamMessages = ['codes4free.net', 'g2a.com/r/', 'prizescode.net']
        self.twitch_chat.subscribeChatMessage(self.handleIRCMessage)

    def kill(self):
        for p in self._plugins:
            p._kill()

    def start(self):
        self.twitch_chat.start()

    def loadPlugins(self):
        potentialPlugins = []
        allplugins = os.listdir(self._pluginFolder)
        for i in allplugins:
            location = os.path.join(self._pluginFolder, i)
            if not os.path.isdir(location) or not self._mainModule + ".py" in os.listdir(location):
                continue
            info = imp.find_module(self._mainModule, [location])
            potentialPlugins.append({"name": i, "info": info})

        print("Found plugin classes:")
        for i in potentialPlugins:
            try:
                plugin = imp.load_module(self._mainModule, *i["info"])
                pluginClasses = inspect.getmembers(plugin, inspect.isclass)
                for className, classObj in pluginClasses:
                    if className == "BasePlugin" or className in self.loadedPluginNames or not issubclass(classObj,
                                                                                                          BasePlugin):
                        continue  # Exclude BasePlugin & any classes that are not a subclass of it
                    print(className)
                    pluginInstance = classObj(self)
                    self._plugins.append(pluginInstance)
                    self.loadedPluginNames.append(className)
            except:
                print("Error loading plugin.")
                print(traceback.format_exc())

    def registerCommand(self, command, pluginFunction):
        self.commands.append({'regex': command, 'handler': pluginFunction})

    def registerTrigger(self, trigger, pluginFunction):
        self.triggers.append({'regex': trigger, 'handler': pluginFunction})

    def registerForJoinPartNotifications(self, pluginFunction):
        self.joinPartHandlers.append(pluginFunction)

    def registerForModNotifications(self, pluginFunction):
        self.modHandlers.append(pluginFunction)

    def handleIRCMessage(self, twitch_msg):
        print twitch_msg
        text = twitch_msg['message']
        user = twitch_msg['display-name'] or twitch_msg['username']
        for pluginDict in self.commands:
            if re.search('^!' + pluginDict['regex'], text, re.IGNORECASE):
                handler = pluginDict['handler']
                args = text.split(" ")
                handler(user, args)

        for pluginDict in self.triggers:
            if re.search('^' + pluginDict['regex'], text, re.IGNORECASE):
                handler = pluginDict['handler']
                handler(user, text)

    def stop(self):
        self.twitch_chat.stop()
        self.kill()

        # 'main'


if __name__ == "__main__":
    while True:
        twitchy = Twitchy()
        try:
            twitchy.start()
            while True:
                time.sleep(0.2)
        finally:
            twitchy.stop()
=======
    def __init__(self, username, password, channels):

        self.connected = False
        # Plugin system loosely based on blog post by lkjoel
        # http://lkubuntu.wordpress.com/2012/10/02/writing-a-python-plugin-api/
        self.twitch_chat = twitch_chat(username, password, channels)
        self._pluginFolder = './plugins/'
        self._mainModule = 'plugin'
        self._plugins = []  # used for cleanup
        self.commands = []
        self.triggers = []
        self.joinPartHandlers = []
        self.modHandlers = []
        self.ignoredUsers = []
        self.loadedPluginNames = []
        self.spamMessages = ['codes4free.net', 'g2a.com/r/', 'prizescode.net']
        self.twitch_chat.subscribeChatMessage(self.handleIRCMessage)
        self.loadPlugins()

    def kill(self):
        for p in self._plugins:
            p._kill()

    def start(self):
        self.twitch_chat.start()

    def loadPlugins(self):
        potentialPlugins = []
        allplugins = os.listdir(self._pluginFolder)
        for i in allplugins:
            location = os.path.join(self._pluginFolder, i)
            if not os.path.isdir(location) or not self._mainModule + ".py" in os.listdir(location):
                continue
            info = imp.find_module(self._mainModule, [location])
            potentialPlugins.append({"name": i, "info": info})

        logger.info("Found plugin classes:")
        for i in potentialPlugins:
            try:
                plugin = imp.load_module(self._mainModule, *i["info"])
                pluginClasses = inspect.getmembers(plugin, inspect.isclass)
                for className, classObj in pluginClasses:
                    if className == "BasePlugin" or className in self.loadedPluginNames or not issubclass(
                            classObj, BasePlugin):
                        continue  # Exclude BasePlugin & any classes that are not a subclass of it
                    logger.info(className)
                    pluginInstance = classObj(self)
                    self._plugins.append(pluginInstance)
                    self.loadedPluginNames.append(className)
            except:
                logger.exception("Error loading plugin.")

    def registerCommand(self, command, pluginFunction):
        self.commands.append({'regex': command, 'handler': pluginFunction})

    def registerTrigger(self, trigger, pluginFunction):
        self.triggers.append({'regex': trigger, 'handler': pluginFunction})

    def registerForJoinPartNotifications(self, pluginFunction):
        self.joinPartHandlers.append(pluginFunction)

    def registerForModNotifications(self, pluginFunction):
        self.modHandlers.append(pluginFunction)

    def handleIRCMessage(self, twitch_msg):
        text = twitch_msg['message']
        user = twitch_msg['display-name'] or twitch_msg['username']
        for pluginDict in self.commands:
            if re.search('^!' + pluginDict['regex'], text, re.IGNORECASE):
                handler = pluginDict['handler']
                args = text.split(" ")
                handler(user, args, twitch_msg)

        for pluginDict in self.triggers:
            if re.search('^' + pluginDict['regex'], text, re.IGNORECASE):
                handler = pluginDict['handler']
                handler(user, text, twitch_msg)

    def send_message(self, message, channel):
        self.twitch_chat.send_message(channel, message)

    def stop(self):
        self.twitch_chat.stop()
        self.kill()


def get_config():
    logger.info('Loading configuration from config.txt')
    config = None
    if os.path.isfile('config.txt'):
        config = load(open('config.txt', 'r'))
        required_settings = ['twitch_username', 'twitch_oauth', 'twitch_channels']
        for setting in required_settings:
            if setting not in config:
                msg = '{} not present in config.txt, put it there! check config_example.txt!'.format(setting)
                logger.critical(msg)
                return None
    else:
        logger.critical('config.txt doesn\'t exist, please create it, refer to config_example.txt for reference')
        return None
    logger.info('Configuration loaded')
    return config


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test", help="Subscribe to featured channels to aid testing", action="store_true")
    parser.add_argument('-d',
                        '--debug',
                        help="Enable debugging statements",
                        action="store_const",
                        dest="loglevel",
                        const=logging.DEBUG,
                        default=logging.INFO,)
    args = parser.parse_args()

    logging.basicConfig(level=args.loglevel,
                        format='%(asctime)s.%(msecs)d %(levelname)s %(name)s : %(message)s',
                        datefmt='%H:%M:%S')
    config = get_config()
    if config:
        while True:
            twitchy = Twitchy(config['twitch_username'], config['twitch_oauth'], config['twitch_channels'])
            try:
                twitchy.start()
                while True:
                    time.sleep(0.2)
            finally:
                twitchy.stop()
    else:
        logging.critical("Failed to load configuration file.. exiting")
>>>>>>> 2aee655cb4e97922c93c6c1525c6eac75263d628
