from pyamaha import Zone
from requests.exceptions import ConnectionError
import sys

def volume_up(dev, args):
    dev.request(Zone.set_volume(args.zone, 'up', None))

def volume_down(dev, args):
    dev.request(Zone.set_volume(args.zone, 'down', None))

def next(dev, args):
    (host, zone) = args.host, args.zone
    print("Next! To host '" + host + "' and zone '" + zone + "'")

def previous(dev, args):
    (host, zone) = args.host, args.zone
    print("Previous! To host '" + host + "' and zone '" + zone + "'")
