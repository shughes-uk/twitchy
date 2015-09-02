from plugins.BasePlugin import BasePlugin
from phue import Bridge
import math
import logging
from time import sleep

class Device(object):
    def __init__(self):
        super(Device, self).__init__()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.current_color = (0,0,0)

    def set_color(self,color):
        raise Exception("Function not implemented , whoops")

    def flash(self,color_1,color_2,ntimes=10,interval=0.2):
        old_color = self.current_color
        for x in range (ntimes):
            self.set_color(color_1)
            sleep(interval)
            self.set_color(color_2)
            sleep(interval)
        self.set_color(old_color)

    def start(self):
        raise Exception("Function not implemented, whoops")

    def stop(self):
        raise Exception("Function not implemented, whoops")


class Hue(Device):
    def __init__(self,ip):
        super(Hue, self).__init__()
        self.logger = logging.getLogger("Hue")
        self.bridge = Bridge(ip)

    def set_color(self,rgb):
        self.current_color = rgb
        for l in self.bridge.lights:
            l.transitiontime = 1
            l.brightness = 254
            l.xy = self._RGBtoXY(rgb[0],rgb[1],rgb[2])


    def _enhancecolor(self,normalized):
        if normalized > 0.04045:
            return math.pow( (normalized + 0.055) / (1.0 + 0.055), 2.4)
        else:
            return normalized / 12.92

    def _RGBtoXY(self,r, g, b):
        rNorm = r / 255.0
        gNorm = g / 255.0
        bNorm = b / 255.0

        rFinal = self._enhancecolor(rNorm)
        gFinal = self._enhancecolor(gNorm)
        bFinal = self._enhancecolor(bNorm)

        X = rFinal * 0.649926 + gFinal * 0.103455 + bFinal * 0.197109
        Y = rFinal * 0.234327 + gFinal * 0.743075 + bFinal * 0.022598
        Z = rFinal * 0.000000 + gFinal * 0.053077 + bFinal * 1.035763

        if X + Y + Z == 0:
            return (0,0)
        else:
            xFinal = X / (X + Y + Z)
            yFinal = Y / (X + Y + Z)

            return (xFinal, yFinal)

REQUIRED_VOTES = 1
class HelloPlugin(BasePlugin):
	def __init__(self, twitchy):
		super(HelloPlugin, self).__init__(twitchy)
		self.mods = []
		self.registerCommand('hue', self.hueHandler) # respond when '!hello' is at beginning of message
		self.registerCommand('flash', self.flashHandler)
		self.registerForModNotifications(self.modGivenTaken)
		self.hue = Hue("192.168.1.211")
		#self.hue.start()
		self.votes = {}

	def flashHandler(self,user, commandArg):


		rgb1 = (int(commandArg[1]),int(commandArg[2]),int(commandArg[3]))
		rgb2 = (int(commandArg[4]),int(commandArg[5]),int(commandArg[6]))
		self.hue.flash(rgb1, rgb2, ntimes=10, interval=0.2)


	def hueHandler(self, user, commandArg):
		rgb = (int(commandArg[1]),int(commandArg[2]),int(commandArg[3]))
		if user["user-type"] == "mod":
			self.sendMessage("Moderator override! Lights changed!")
			self.hue.set_color(rgb)
			self.votes = {}
			return
		if rgb in self.votes:
			if not nick in self.votes[rgb]:
				self.votes[rgb].append(user)
		else:
			self.votes[rgb] = [user]
		if len(self.votes[rgb]) >= REQUIRED_VOTES:
			self.sendMessage("We have enough votes! Lights changing color wooo!! 2spoopy4me!")
			self.hue.set_color(rgb)
			self.votes = {}
		else:
			self.sendMessage("Vote registered! %i more votes to change to this color!" %(REQUIRED_VOTES-len(self.votes[xy])))


	def modGivenTaken(self, nick, modGiven):
		if modGiven:
			self.mods.append(nick)
		else:
			if nick in self.mods:
				self.mods.remove(nick)

	def _enhancecolor(self,normalized):
		if normalized > 0.04045:
			return math.pow( (normalized + 0.055) / (1.0 + 0.055), 2.4)
		else:
			return normalized / 12.92

	def _RGBtoXY(self,r, g, b):
		rNorm = r / 255.0
		gNorm = g / 255.0
		bNorm = b / 255.0

		rFinal = self._enhancecolor(rNorm)
		gFinal = self._enhancecolor(gNorm)
		bFinal = self._enhancecolor(bNorm)

		X = rFinal * 0.649926 + gFinal * 0.103455 + bFinal * 0.197109
		Y = rFinal * 0.234327 + gFinal * 0.743075 + bFinal * 0.022598
		Z = rFinal * 0.000000 + gFinal * 0.053077 + bFinal * 1.035763

		if X + Y + Z == 0:
			return (0,0)
		else:
			xFinal = X / (X + Y + Z)
			yFinal = Y / (X + Y + Z)

			return (xFinal, yFinal)
