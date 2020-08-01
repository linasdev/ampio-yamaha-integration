from pyamaha import Zone
from requests.exceptions import ConnectionError
import sys

def volume_up(dev, args):
    dev.request(Zone.set_volume(args.zone, 'up', None))

def volume_down(dev, args):
    dev.request(Zone.set_volume(args.zone, 'down', None))

def radio_next(dev, args):
    (host, zone) = args.host, args.zone
    print("Radio next! To host '" + host + "' and zone '" + zone + "'")

def radio_previous(dev, args):
    (host, zone) = args.host, args.zone
    print("Radio previous! To host '" + host + "' and zone '" + zone + "'")
