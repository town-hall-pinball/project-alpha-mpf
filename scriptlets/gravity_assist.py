# Copyright (c) 2014 - 2015 townhallpinball.org
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

from mpf.system.scriptlet import Scriptlet

class GravityAssist(Scriptlet):

    spinner_base = 1000
    orbit_little_score = 100
    orbit_big_score = 100000

    def on_load(self):
        self.machine.events.add_handler("ball_started", self.start)
        self.machine.events.add_handler("ball_ending", self.stop)

    def start(self, *args, **kwargs):
        self.machine.events.add_handler("shot_orbit_inner", self.inner_orbit)
        self.machine.events.add_handler("shot_spinner", self.spinner)
        self.machine.game.player.spinner_multiplier = 1

    def stop(self, *args, **kwargs):
        self.machine.events.remove_handler("shot_orbit_inner", self.inner_orbit)
        self.machine.events.remove_handler("shot_spinner", self.spinner)

    def inner_orbit(self, *args, **kwargs):
        if self.machine.game.player.spinner_multiplier < 10:
            self.machine.game.player.score += self.orbit_little_score
            self.machine.game.player.spinner_multiplier += 1
            self.machine.events.post("gravity_assist",
                    multiplier=self.machine.game.player.spinner_multiplier)
        else:
            self.machine.game.player.score += self.orbit_big_score
            self.machine.events.post("gravity_assist_max",
                    score=self.orbit_big_score)

    def spinner(self, *args, **kwargs):
        mult = self.machine.game.player.spinner_multiplier
        self.machine.game.player.score += self.spinner_base * mult



