import logging

import click
import evdev


class Reader:
    """Represents the USB RFID reader input device."""

    @classmethod
    def find(cls):
        """Find input device and return corresponding Reader."""
        
        for node in evdev.list_devices():
            device = evdev.InputDevice(node)
            logging.debug("scan %s -- %s", device.fn, device.name)
            if "rfid" in device.name.lower():
                logging.info("selected '%s' (%s)", device.fn, device.name)
                return cls(device)
                
        logging.error("unable to find reader")

    def __init__(self, input_device):
        self.device = input_device
            
    def read_loop(self):
        """Grab device (exclusively) and yield tags in endless loop."""
    
        tag = ""
        with self.device.grab_context():
            for event in self.device.read_loop():
                if event.type == evdev.ecodes.EV_KEY and event.value == 1:
                    key = evdev.ecodes.KEY[event.code]
                    if key == 'KEY_ENTER':
                        yield tag
                        tag = ""
                    else:
                        tag = tag + key.strip('KEY_')            


@click.command()
@click.option("--log-level", default="WARNING")
def cli(log_level):
    """Sorts wedding guests on to tables."""
    
    logging.basicConfig(level=log_level, format="%(message)s")
    
    reader = Reader.find()
    for tag in reader.read_loop():
        logging.info("tag '%s' read", tag)
