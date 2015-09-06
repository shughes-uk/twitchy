import time
import imp
import os
import traceback
import re
import inspect
from plugins.BasePlugin import BasePlugin
from twitchchat import twitch_chat
# Twitchy
# An IRC bot designed for Twitch.TV streams
#
# Please see the README for instructions on using Twitchy.
# It is released under the BSD license; the full license
# available in the LICENSE file.

# CONFIGURATION
Twitch_Username = 'Collectablecat'  # Twitch.TV username for the bot, must be a registered username!
Twitch_Password = 'nope'  # OAuth for above Twitch.TV account, http://www.twitchapps.com/tmi/
Twitch_Channel = 'animaggus'  # Twitch.TV channel to connect to

# NOW DON'T TOUCH ANYTHING ELSE, UNLESS YOU KNOW WHAT YOU'RE DOING

# If you do want to improve the code, though, feel free.
# I'd like if you then made a pull request on GitHub for everyone to
# benefit from the improved code, but you aren't required to do so.


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
