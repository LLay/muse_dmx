from __future__ import division
from __future__ import absolute_import
import requests
import random
import colorsys
import re

# Primary interface for an Aurora light
# For instructions or bug reports, please visit
# https://github.com/software-2/nanoleaf


class Aurora(object):
    def __init__(self, ip_address, auth_token):
        self.baseUrl = u"http://" + ip_address + u":16021/api/v1/" + auth_token + u"/"
        self.ip_address = ip_address
        self.auth_token = auth_token

    def __repr__(self):
        return u"<Aurora(" + self.ip_address + u")>"

    def __put(self, endpoint, data):
        url = self.baseUrl + endpoint
        try:
            r = requests.put(url, json=data)
        except requests.exceptions.RequestException, e:
            print e
            return
        return self.__check_for_errors(r)

    def __get(self, endpoint = u""):
        url = self.baseUrl + endpoint
        try:
            r = requests.get(url)
        except requests.exceptions.RequestException, e:
            print e
            return
        return self.__check_for_errors(r)

    def __delete(self, endpoint = u""):
        url = self.baseUrl + endpoint
        try:
            r = requests.delete(url)
        except requests.exceptions.RequestException, e:
            print e
            return
        return self.__check_for_errors(r)

    def __check_for_errors(self, r):
        if r.status_code == 200:
            if r.text == u"":  # BUG: Delete User returns 200, not 204 like it should, as of firmware 1.5.0
                return None
            return r.json()
        elif r.status_code == 204:
            return None
        elif r.status_code == 403:
            print u"Error 400: Bad request! (" + self.ip_address + u")"
        elif r.status_code == 401:
            print u"Error 401: Not authorized! This is an invalid token for this Aurora (" + self.ip_address + u")"
        elif r.status_code == 404:
            print u"Error 404: Resource not found! (" + self.ip_address + u")"
        elif r.status_code == 422:
            print u"Error 422: Unprocessible Entity (" + self.ip_address + u")"
        elif r.status_code == 500:
            print u"Error 500: Internal Server Error (" + self.ip_address + u")"
        else:
            print u"ERROR! UNKNOWN ERROR " + unicode(r.status_code) + u". Please post an issue on the GitHub page: https://github.com/software-2/nanoleaf/issues"
        return None

    ###########################################
    # General functionality methods
    ###########################################

    @property
    def info(self):
        u"""Returns the full Aurora Info request.

        Useful for debugging since it's just a fat dump."""
        return self.__get()

    @property
    def color_mode(self):
        u"""Returns the current color mode."""
        return self.__get(u"state/colorMode")

    def identify(self):
        u"""Briefly flash the panels on and off"""
        self.__put(u"identify", {})

    @property
    def firmware(self):
        u"""Returns the firmware version of the device"""
        return self.__get(u"firmwareVersion")

    @property
    def model(self):
        u"""Returns the model number of the device. (Always returns 'NL22')"""
        return self.__get(u"model")

    @property
    def serial_number(self):
        u"""Returns the serial number of the device"""
        return self.__get(u"serialNo")

    def delete_user(self):
        u"""CAUTION: Revokes your auth token from the device."""
        self.__delete()

    ###########################################
    # On / Off methods
    ###########################################

    @property
    def on(self):
        u"""Returns True if the device is on, False if it's off"""
        return self.__get(u"state/on/value")

    @on.setter
    def on(self, value):
        u"""Turns the device on/off. True = on, False = off"""
        data = {u"on": value}
        self.__put(u"state", data)

    @property
    def off(self):
        u"""Returns True if the device is off, False if it's on"""
        return not self.on

    @off.setter
    def off(self, value):
        u"""Turns the device on/off. True = off, False = on"""
        self.on = not value

    def on_toggle(self):
        u"""Switches the on/off state of the device"""
        self.on = not self.on

    ###########################################
    # Brightness methods
    ###########################################

    @property
    def brightness(self):
        u"""Returns the brightness of the device (0-100)"""
        return self.__get(u"state/brightness/value")

    @brightness.setter
    def brightness(self, level):
        u"""Sets the brightness to the given level (0-100)"""
        data = {u"brightness": {u"value": level}}
        self.__put(u"state", data)

    @property
    def brightness_min(self):
        u"""Returns the minimum brightness possible. (This always returns 0)"""
        return self.__get(u"state/brightness/min")

    @property
    def brightness_max(self):
        u"""Returns the maximum brightness possible. (This always returns 100)"""
        return self.__get(u"state/brightness/max")

    def brightness_raise(self, level):
        u"""Raise the brightness of the device by a relative amount (negative lowers brightness)"""
        data = {u"brightness": {u"increment": level}}
        self.__put(u"state", data)

    def brightness_lower(self, level):
        u"""Lower the brightness of the device by a relative amount (negative raises brightness)"""
        self.brightness_raise(-level)

    ###########################################
    # Hue methods
    ###########################################

    @property
    def hue(self):
        u"""Returns the hue of the device (0-360)"""
        return self.__get(u"state/hue/value")

    @hue.setter
    def hue(self, level):
        u"""Sets the hue to the given level (0-360)"""
        data = {u"hue": {u"value": level}}
        self.__put(u"state", data)

    @property
    def hue_min(self):
        u"""Returns the minimum hue possible. (This always returns 0)"""
        return self.__get(u"state/hue/min")

    @property
    def hue_max(self):
        u"""Returns the maximum hue possible. (This always returns 360)"""
        return self.__get(u"state/hue/max")

    def hue_raise(self, level):
        u"""Raise the hue of the device by a relative amount (negative lowers hue)"""
        data = {u"hue": {u"increment": level}}
        self.__put(u"state", data)

    def hue_lower(self, level):
        u"""Lower the hue of the device by a relative amount (negative raises hue)"""
        self.hue_raise(-level)

    ###########################################
    # Saturation methods
    ###########################################

    @property
    def saturation(self):
        u"""Returns the saturation of the device (0-100)"""
        return self.__get(u"state/sat/value")

    @saturation.setter
    def saturation(self, level):
        u"""Sets the saturation to the given level (0-100)"""
        data = {u"sat": {u"value": level}}
        self.__put(u"state", data)

    @property
    def saturation_min(self):
        u"""Returns the minimum saturation possible. (This always returns 0)"""
        return self.__get(u"state/sat/min")

    @property
    def saturation_max(self):
        u"""Returns the maximum saturation possible. (This always returns 100)"""
        return self.__get(u"state/sat/max")

    def saturation_raise(self, level):
        u"""Raise the saturation of the device by a relative amount (negative lowers saturation)"""
        data = {u"sat": {u"increment": level}}
        self.__put(u"state", data)

    def saturation_lower(self, level):
        u"""Lower the saturation of the device by a relative amount (negative raises saturation)"""
        self.saturation_raise(-level)

    ###########################################
    # Color Temperature methods
    ###########################################

    @property
    def color_temperature(self):
        u"""Returns the color temperature of the device (0-100)"""
        return self.__get(u"state/ct/value")

    @color_temperature.setter
    def color_temperature(self, level):
        u"""Sets the color temperature to the given level (0-100)"""
        data = {u"ct": {u"value": level}}
        self.__put(u"state", data)

    @property
    def color_temperature_min(self):
        u"""Returns the minimum color temperature possible. (This always returns 1200)"""
        # return self.__get("state/ct/min")
        # BUG: Firmware 1.5.0 returns the wrong value.
        return 1200

    @property
    def color_temperature_max(self):
        u"""Returns the maximum color temperature possible. (This always returns 6500)"""
        # return self.__get("state/ct/max")
        # BUG: Firmware 1.5.0 returns the wrong value.
        return 6500

    def color_temperature_raise(self, level):
        u"""Raise the color temperature of the device by a relative amount (negative lowers color temperature)"""
        data = {u"ct": {u"increment": level}}
        self.__put(u"state", data)

    def color_temperature_lower(self, level):
        u"""Lower the color temperature of the device by a relative amount (negative raises color temperature)"""
        self.color_temperature_raise(-level)

    ###########################################
    # Color RGB/HSB methods
    ###########################################

    # TODO: Shame on all these magic numbers. SHAME.

    @property
    def rgb(self):
        u"""The color of the device, as represented by 0-255 RGB values"""
        hue = self.hue
        saturation = self.saturation
        brightness = self.brightness
        if hue is None or saturation is None or brightness is None:
            return None
        rgb = colorsys.hsv_to_rgb(hue / 360, saturation / 100, brightness / 100)
        return [int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)]

    @rgb.setter
    def rgb(self, color):
        u"""Set the color of the device, as represented by either a hex string or a list of 0-255 RGB values"""
        try:
            red, green, blue = color
        except ValueError:
            try:
                hexcolor = color
                reg_match = re.match(u"^([A-Fa-f0-9]{6})$", hexcolor)
                if reg_match:
                    red = int(hexcolor[:2], 16)
                    green = int(hexcolor[2:-2], 16)
                    blue = int(hexcolor[-2:], 16)
                else:
                    print u"Error: Color must be in valid hex format."
                    return
            except ValueError:
                print u"Error: Color must have one hex value or three 0-255 values."
                return
        if not 0 <= red <= 255:
            print u"Error: Red value out of range! (0-255)"
            return
        if not 0 <= green <= 255:
            print u"Error: Green value out of range! (0-255)"
            return
        if not 0 <= blue <= 255:
            print u"Error: Blue value out of range! (0-255)"
            return

        hsv = colorsys.rgb_to_hsv(red / 255, green / 255, blue / 255)
        hue = int(hsv[0] * 360)
        saturation = int(hsv[1] * 100)
        brightness = int(hsv[2] * 100)
        data = {u"hue": {u"value": hue}, u"sat": {u"value": saturation}, u"brightness": {u"value": brightness}}
        self.__put(u"state", data)

    ###########################################
    # Layout methods
    ###########################################

    @property
    def orientation(self):
        u"""Returns the orientation of the device (0-360)"""
        return self.__get(u"panelLayout/globalOrientation/value")

    @property
    def orientation_min(self):
        u"""Returns the minimum orientation possible. (This always returns 0)"""
        return self.__get(u"panelLayout/globalOrientation/min")

    @property
    def orientation_max(self):
        u"""Returns the maximum orientation possible. (This always returns 360)"""
        return self.__get(u"panelLayout/globalOrientation/max")

    @property
    def panel_count(self):
        u"""Returns the number of panels connected to the device"""
        return self.__get(u"panelLayout/layout/numPanels")

    @property
    def panel_length(self):
        u"""Returns the length of a single panel. (This always returns 150)"""
        return self.__get(u"panelLayout/layout/sideLength")

    @property
    def panel_positions(self):
        u"""Returns a list of all panels with their attributes represented in a dict.

        panelId - Unique identifier for this panel
        x - X-coordinate
        y - Y-coordinate
        o - Rotational orientation
        """
        return self.__get(u"panelLayout/layout/positionData")

    ###########################################
    # Effect methods
    ###########################################

    _reserved_effect_names = [u"*Static*", u"*Dynamic*", u"*Solid*"]

    @property
    def effect(self):
        u"""Returns the active effect"""
        return self.__get(u"effects/select")

    @effect.setter
    def effect(self, effect_name):
        u"""Sets the active effect to the name specified"""
        data = {u"select": effect_name}
        self.__put(u"effects", data)

    @property
    def effects_list(self):
        u"""Returns a list of all effects stored on the device"""
        return self.__get(u"effects/effectsList")

    def effect_random(self):
        u"""Sets the active effect to a new random effect stored on the device.

        Returns the name of the new effect."""
        effect_list = self.effects_list
        active_effect = self.effect
        if active_effect not in self._reserved_effect_names:
            effect_list.remove(self.effect)
        new_effect = random.choice(effect_list)
        self.effect = new_effect
        return new_effect

    def effect_set_raw(self, effect_data):
        u"""Sends a raw dict containing effect data to the device.

        The dict given must match the json structure specified in the API docs."""
        data = {u"write": effect_data}
        self.__put(u"effects", data)

    def effect_details(self, name):
        u"""Returns the dict containing details for the effect specified"""
        data = {u"write": {u"command": u"request",
                          u"animName": name}}
        return self.__put(u"effects", data)

    def effect_details_all(self):
        u"""Returns a dict containing details for all effects on the device"""
        data = {u"write": {u"command": u"requestAll"}}
        return self.__put(u"effects", data)

    def effect_delete(self, name):
        u"""Removed the specified effect from the device"""
        data = {u"write": {u"command": u"delete",
                          u"animName": name}}
        self.__put(u"effects", data)

    def effect_rename(self, old_name, new_name):
        u"""Renames the specified effect saved on the device to a new name"""
        data = {u"write": {u"command": u"rename",
                          u"animName": old_name,
                          u"newName": new_name}}
        self.__put(u"effects", data)