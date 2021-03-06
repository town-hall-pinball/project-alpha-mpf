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

class Assist(Scriptlet):

    magnets = {
        "s_magnet_left": "c_magnet_left",
        "s_magnet_center": "c_magnet_center",
        "s_magnet_right": "c_magnet_right"
    }

    def on_load(self):
        self.machine.events.add_handler("ball_started", self.start)
        self.machine.events.add_handler("ball_ending", self.stop)

    def start(self, *args, **kwargs):
        for switch, coil in self.magnets.items():
            self.machine.platform.set_hw_rule(
                switch,
                "active",
                coil,
                coil_action_ms=-1,
                pwm_on=1,
                pwm_off=1
            )
            self.machine.platform.set_hw_rule(
                switch,
                "inactive",
                coil,
                coil_action_ms=0
            )

    def stop(self, *args, **kwargs):
        for switch in self.magnets:
            self.machine.platform.clear_hw_rule(switch)



