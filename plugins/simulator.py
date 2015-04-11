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

import logging

def preload_check(machine):
    return True

class Simulator(object):

    def __init__(self, machine):
        self.machine = machine
        self.log = logging.getLogger("Simulator")
        self.switches = self.machine.switch_controller
        self.events = self.machine.events

        self.valid = False
        self.running = False
        self.ball_devices = {}
        self.initial_balls = []
        self.total_count = 0
        self.tracking_count = 0
        self.playfield_switch = None
        self.drain_device = None

        self.events.add_handler('machine_init_phase_4', self._setup)

    def _setup(self):
        config = self.machine.config.get("Simulator", {})

        # Which ball devices should be managed?
        for device_name in config.get("ball_devices", []):
            device = self.machine.balldevices[device_name]
            if "drain" in device.tags:
                self.drain_device = device
            self.ball_devices[device_name] = device
        if len(self.ball_devices) == 0:
            self.log.warning("No ball devices to manage")
            return

        self.initial_balls = config.get("initial_balls", {})
        for count in self.initial_balls.values():
            self.total_count += count
        self.playfield_switch = config["playfield_switch"]
        self.events.add_handler("action_simulator_toggle", self.toggle)
        self.valid = True

    def start(self):
        if self.running or not self._can_start():
            return

        # Place balls in the initial starting positions
        self.log.info("Setting initial switch states")
        for device_name, count in self.initial_balls.items():
            self._put_ball(self.ball_devices[device_name], count)

        # Listen for all eject attempts in managed ball devices
        for name, device in self.ball_devices.items():
            event = "balldevice_{}_ball_eject_attempt".format(name)
            self.events.add_handler(event, self._move, name=name,
                    device=device)

        # Listen for drain requests
        self.events.add_handler("action_simulator_drain", self._drain)

        self.log.info("Started")
        self.events.post("simulator_start")
        self.running = True

    def stop(self):
        self._clear_balls()
        self.events.remove_handler(self._move)
        self.events.remove_handler(self._drain)

        self.log.info("Stopped")
        self.events.post("simulator_stop")
        self.running = False

    def toggle(self, **kwargs):
        if self.running:
            self.stop()
        else:
            self.start()

    def _can_start(self):
        if self.machine.physical_hw:
            self.log.warning("Not starting, connected to physical hardware")
            return False
        if not self.valid:
            self.log.warning("Not starting, configuration not valid")
            return False
        return True

    def _move(self, name, device, **kwargs):
        self._take_ball(device)

        if device.config["confirm_eject_type"] == "target":
            targets = device.config["eject_targets"]
            if len(targets) == 1:
                self._put_ball(targets[0])
                return
            elif len(targets) >= 1:
                self.log.info("Please manually place the ball")
                return
        self._free_ball()

    def _take_ball(self, device, count=1):
        for i in xrange(count):
            if self.tracking_count == 0:
                self.log.warning("Not enough balls when trying to take from %s",
                        device_name)
                return
            self.log.debug("Taking ball from device: %s", device.name)
            source_switch = None
            for switch in reversed(device.config["ball_switches"]):
                if switch.name == device.config["jam_switch"]:
                    self.log.debug("Ignoring jam switch: %s", switch.name)
                elif switch.state:
                    self.log.debug("Slot taken: %s", switch.name)
                    source_switch = switch
                    break
                else:
                    self.log.debug("Slot free: %s", switch.name)
            if not source_switch:
                self.log.warning("Device empty: %s", device.name)
                return
            self.log.info("Removing ball from device %s on switch %s",
                    device.name, source_switch)
            self.switches.process_switch(source_switch.name, state=0,
                    logical=True)
            self.tracking_count -= 1
            self._log_status()

    def _put_ball(self, device, count=1):
        for i in xrange(count):
            if self.tracking_count == self.total_count:
                self.log.warning("Too many balls when trying to add to %s",
                        device.name)
                return
            self.log.debug("Putting ball in device: %s", device.name)
            target_switch = None
            for switch in device.config["ball_switches"]:
                if switch.name == device.config["jam_switch"]:
                    self.log.debug("Ignoring jam switch: %s", switch.name)
                elif not switch.state:
                    self.log.debug("Slot free: %s", switch.name)
                    target_switch = switch
                    break
                else:
                    self.log.debug("Slot taken: %s", switch.name)
            if not target_switch:
                self.log.warning("Device full: %s", device.name)
                return
            self.log.info("Adding ball to device %s on switch %s", device.name,
                    target_switch)
            self.switches.process_switch(target_switch.name, state=1,
                    logical=True)
            self.tracking_count += 1
            self._log_status()

    def _free_ball(self):
        if self.tracking_count == 0:
            self.log.warning("Not enough balls when adding to playfield")
            return
        self.log.info("Adding ball to playfield")
        self.switches.process_switch(self.playfield_switch, state=1,
                logical=True)
        self.switches.process_switch(self.playfield_switch, state=0,
                logical=True)
        self._log_status()

    def _drain(self, **kwargs):
        if self.tracking_count == self.total_count:
            self.log.warning("No free balls to drain")
            return
        self._put_ball(self.drain_device)

    def _clear_balls(self):
        for device in self.ball_devices.values():
            for switch in device.config["ball_switches"]:
                if switch.state:
                    self.switches.process_switch(switch.name, state=0,
                            logical=True)
        self.tracking_count = 0

    def _log_status(self):
        self.log.debug("Tracking %d, total %d", self.tracking_count,
                self.total_count)




