''''
BasePlugin.py
Twitchy project

Copyright (c) 2013 Matthew McNamara
BSD 2-Clause License
http://opensource.org/licenses/BSD-2-Clause
'''

class BasePlugin(object):
    def __init__(self, twitchy):
        self.twitchy = twitchy

    def registerCommand(self, command, handler):
        self.twitchy.registerCommand(command, handler)

    def registerTrigger(self, trigger, handler):
        self.twitchy.registerTrigger(trigger, handler)

    def registerForJoinPartNotifications(self, handler):
        self.twitchy.registerForJoinPartNotifications(handler)

    def registerForModNotifications(self, handler):
        self.twitchy.registerForModNotifications(handler)

    def sendMessage(self, message):
        self.twitchy.sendMessage(message)