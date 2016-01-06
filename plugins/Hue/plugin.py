from plugins.BasePlugin import BasePlugin
from phue import Bridge
import math
import logging
from time import sleep
from subprocess import Popen
from hue_helper import ColorHelper

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
        self.chelper = ColorHelper()

    def flash(self,color_1,color_2,ntimes=10,interval=0.2):
        #store the old states
        old_colors = {}
        for l in self.bridge.lights:
            old_colors[l] = (l.xy,l.brightness)
        #flash a bunch
        for x in range (ntimes):
            self.set_color(rgb=color_1, brightness=254)
            sleep(interval)
            self.set_color(rgb=color_2, brightness=254)
            sleep(interval)
        #reset to old states
        for l in self.bridge.lights:
            l.xy = old_colors[l][0]
            l.brightness = old_colors[l][1]

    def set_color(self,rgb=None,xy=None,brightness=None):
        for l in self.bridge.lights:
            l.transitiontime = 1
            if brightness:
                if brightness == 0:
                    l.on = False
                else:
                    l.on = True
                    l.brightness = brightness
            if rgb:
                if rgb == (0,0,0):
                    l.on = False
                else:
                    l.on = True
                    l.xy = self._RGBtoXY(rgb[0],rgb[1],rgb[2])
            elif xy:
                l.xy = xy



    def _enhancecolor(self,normalized):
        if normalized > 0.04045:
            return math.pow( (normalized + 0.055) / (1.0 + 0.055), 2.4)
        else:
            return normalized / 12.92

    def _XYtoRGB(self,xy,brightness):
        return self.chelper.getRGBFromXYAndBrightness(x, y, bri=1)

    def _RGBtoXY(self,r, g, b):
        return self.chelper.getXYPointFromRGB(r, g, b)

REQUIRED_VOTES = 2
class HuePlugin(BasePlugin):
    def __init__(self, twitchy):
        super(HuePlugin, self).__init__(twitchy)
        self.mods = []
        self.registerCommand('hue', self.hueHandler) # respond when '!hello' is at beginning of message
        self.registerCommand('2spoopy', self.flashVote)
        self.registerCommand('brighter', self.brighterVote)
        self.registerCommand('darker', self.darkerVote)
        self.registerCommand('help', self.helpHandler)
        self.hue = Hue("192.168.1.211")
        self.votes = {}
        self.darkerVotes = {}
        self.brighterVotes = {}
        self.flashVotes = {}

    def brighterVote(self,user,commandArg):
        if not user['nick'] in self.brighterVotes:
            self.brighterVotes[user['nick']] = 1
        if len(self.brighterVotes) > 5:
            self.sendMessage("The light has returned! Praise the sun!")
            current_brightness = self.hue.bridge.lights[2].brightness
            self.hue.set_color(brightness=min(254,current_brightness+50))
            self.brighterVotes = {}
            self.darkerVotes = {}
        else:
            #self.sendMessage("The sun draws nearer")
            pass

    def darkerVote(self,user,commandArg):
        if not user['nick'] in self.brighterVotes:
            self.darkerVotes[user['nick']] = 1
        if len(self.darkerVotes) > 5:
            self.sendMessage("Darkness falls across the land... well shit")
            current_brightness = self.hue.bridge.lights[2].brightness
            self.hue.set_color(brightness=max(0,current_brightness-50))
            self.darkerVotes = {}
            self.brighterVotes = {}
        else:
            #self.sendMessage("The darkness swells")
            pass

    def doLightning(self):
        old_colors = {}
        for l in self.hue.bridge.lights:
            old_colors[l] = (l.xy,l.brightness,l.on)
        fast_full_white = {"transitiontime":1,"on":True,"xy":self.hue._RGBtoXY(1, 1, 1),'bri':254}
        fast_half_white = {"transitiontime":1,"on":True,"xy":self.hue._RGBtoXY(1, 1, 1),'bri':124}
        fast_min_white = {"transitiontime":1,"on":True,"xy":self.hue._RGBtoXY(1, 1, 1),'bri':124}
        off_fast = {"transitiontime":1,"on":False}
        self.hue.bridge.set_light([1,2,3],off_fast)
        sleep(1)
        p = Popen(['afplay','plugins/Hue/thunder.mp3'])
        sleep(0.3)
        self.hue.bridge.set_light([1,2,3],fast_full_white)
        sleep(0.3)
        self.hue.bridge.set_light([1,2,3],fast_min_white)
        sleep(0.1)
        self.hue.bridge.set_light([1,2,3],off_fast)
        sleep(0.1)
        self.hue.bridge.set_light([1,2,3],fast_min_white)
        sleep(0.1)
        self.hue.bridge.set_light([1,2,3],fast_full_white)
        sleep(0.1)
        self.hue.bridge.set_light([1,2,3],off_fast)
        sleep(3)
        #reset to old states
        for l in self.hue.bridge.lights:
            l.on = old_colors[l][2]
            l.xy = old_colors[l][0]
            l.brightness = old_colors[l][1]

    def flashVote(self,user,commandArg):
        if not user['nick'] in self.flashVotes:
            self.flashVotes[user['nick']] = 1
        if len(self.flashVotes) >= 5:
            self.sendMessage("SHITTTTT")
            self.doLightning()
            self.flashVotes = {}
        else:
            #self.sendMessage("Your intent has been registered...")
            pass

    def helpHandler(self, user, commandArg):
        if user["user-type"] == "mod":
            self.sendMessage("Commands are :")
            self.sendMessage("[!darker] , vote to make the room darker and more scary")
            self.sendMessage("[!brighter] , vote to make the room brighter and less scary")
            self.sendMessage("[!hue R G B] , vote to set current lighting color")
            self.sendMessage("[!2spoopy] , vote to strike us with lightning")

    def hueHandler(self, user, commandArg):
        rgb = (int(commandArg[1]),int(commandArg[2]),int(commandArg[3]))
        if user["user-type"] == "mod":
            self.sendMessage("Moderator override! Lights changed!")
            self.hue.set_color(rgb)
            self.votes = {}
            return
        return
        if rgb in self.votes:
            if not user['nick'] in self.votes[rgb]:
                self.votes[rgb].append(user['nick'])
        else:
            self.votes[rgb] = [user['nick']]
        if len(self.votes[rgb]) >= REQUIRED_VOTES:
            self.sendMessage("We have enough votes! Lights changing color wooo!! 2spoopy4me!")
            self.hue.set_color(rgb)
            self.votes = {}
        else:
            self.sendMessage("Vote registered! %i more votes to change to this color!" %(REQUIRED_VOTES-len(self.votes[xy])))

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
