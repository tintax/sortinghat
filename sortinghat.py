import logging
from pathlib import Path

import click
import evdev
import toml


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


class SortingHat:
    """Controls the application logic."""

    def __init__(self, tags, audio_dir):
        self.tags = tags
        self.audio_dir = Path(audio_dir)
        
    def sort(self, tag):
        """Play sound for guest associated with supplied RFID tag.""" 
    
        audio_filename = self.tags["guests"].get(tag)
        if not audio_filename:
            logging.warning("tag '%s' not recognised", tag)
            return
            
        click.echo(self.audio_dir / audio_filename)


@click.command()
@click.argument("tags", type=click.File("r"))
@click.argument("audiofiles", type=click.Path(exists=True, file_okay=False))
@click.option("--log-level", default="WARNING")
def cli(tags, audiofiles, log_level):
    """Sorts wedding guests on to tables."""
    
    logging.basicConfig(level=log_level, format="%(message)s")
    
    hat = SortingHat(toml.load(tags), audiofiles)
    
    reader = Reader.find()
    for tag in reader.read_loop():
        logging.info("tag '%s' read", tag)
        hat.sort(tag)
