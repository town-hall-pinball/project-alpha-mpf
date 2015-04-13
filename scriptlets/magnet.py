# The MIT License (MIT)

# Copyright (c) 2013-2015 Brian Madden and Gabe Knuth

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from mpf.system.scriptlet import Scriptlet

class Assist(Scriptlet):

    mapping = {
        "s_magnet_left": "c_magnet_left",
        "s_magnet_center": "c_magnet_center",
        "s_magnet_right": "c_magnet_right"
    }

    def on_load(self):
        self.machine.events.add_handler("ball_started", self.start)
        self.machine.events.add_handler("ball_ending", self.stop)

    def start(self, *args, **kwargs):
        for switch_name in self.mapping:
            self.machine.switch_controller.add_switch_handler(switch_name,
                    self.activate, state=1, return_info=True)
            self.machine.switch_controller.add_switch_handler(switch_name,
                    self.deactivate, state=0, return_info=True)

    def stop(self, *args, **kwargs):
        for switch_name in self.mapping:
            self.machine.switch_controller.remove_switch_handler(switch_name,
                    self.activate, state=1)
            self.machine.switch_controller.remove_switch_handler(switch_name,
                    self.deactivate, state=0)

    def activate(self, switch_name, **kwargs):
        coil_name = self.mapping[switch_name]
        print "ON", switch_name, self.machine.coils[coil_name], kwargs
        self.machine.coils[coil_name].pwm(1, 1)

    def deactivate(self, switch_name, **kwargs):
        print "OFF", switch_name
        coil_name = self.mapping[switch_name]
        self.machine.coils[coil_name].disable()




