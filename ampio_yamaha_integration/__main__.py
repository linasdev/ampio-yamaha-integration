from . import __version__
from . import yamaha
from argparse import ArgumentParser
from pyamaha import Device, Zone
from requests.exceptions import ConnectionError
from sys import stderr

def main():
    parser = ArgumentParser(description="Controls a Yamaha MusicCast device")
    parser.add_argument("-v", "--version", action="version", version="Ampio Yamaha Integration " + __version__)
    parser.add_argument("-d", "--device", action="store", required=True,
        help="target device's IP address or hostname", dest="host")
    parser.add_argument("-z", "--zone", action="store", default="main",
        help="target zone", dest="zone")
    parser.add_argument("-a", "--action", action="extend", required=True, nargs="+",
        dest="actions", help="one or more actions to execute",
        choices=[
            "volume_up",
            "volume_down",
            "radio_next",
            "radio_previous",
        ])

    args = parser.parse_args()

    device = Device(args.host)

    try:
        device.request(Zone.get_status(args.zone))
    except ConnectionError:
        print("Can't connect to host.", file=stderr)
    except AssertionError:
        print("Invalid zone specified.", file=stderr)
    else:
        for action in args.actions:
            getattr(yamaha, action)(device, args)

main()
