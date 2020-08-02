from . import __version__
from . import yamaha
from argparse import ArgumentParser
from pyamaha import Device, Zone
from requests.exceptions import ConnectionError
from sys import stderr

def main():
    parser = ArgumentParser(description="Controls a Yamaha MusicCast device")
    parser.add_argument("-v", "--version", action="version", version="Ampio Yamaha Integration " + __version__)
    parser.add_argument("-z", "--zone", help="target zone (default: main)", action="store", default="main")
    parser.add_argument("host", help="target device's IP address or hostname", action="store")
    parser.add_argument("--volume-up", help="increase target device's volume by one step", action="count", default=0)
    parser.add_argument("--volume-down", help="decrease target device's volume by one step", action="count", default=0)
    parser.add_argument("--next", help="play next track / radio station (depends on input)", action="count", default=0)
    parser.add_argument("--prev", help="play previous track / radio station (depends on input)", action="count", default=0)
    parser.add_argument("--set-input", help="set input", action="append", default=[], dest="inputs", nargs=2)
    parser.add_argument("--set-playback", help="set playback", action="append", default=[], dest="playback")
    parser.add_argument("--set-power", help="set power", action="append", default=[], dest="power")
    parser.add_argument("--toggle-input", help="toggle between playing on the target input and power standby", action="append", default=[], dest="toggle", nargs=2)

    args = parser.parse_args()
    device = Device(args.host)

    try:
        device.request(Zone.get_status(args.zone))
    except ConnectionError:
        print("Can't connect to host.", file=stderr)
    except AssertionError:
        print("Invalid zone specified.", file=stderr)
    else:
        for _ in range(args.volume_up):
            yamaha.volume_up(device, args)

        for _ in range(args.volume_down):
            yamaha.volume_down(device, args)

        for _ in range(args.next):
            yamaha.next(device, args)

        for _ in range(args.prev):
            yamaha.prev(device, args)

        for [input, mode] in args.inputs:
            yamaha.set_input(device, args, input, mode)

        for playback in args.playback:
            yamaha.set_playback(device, args, playback)

        for power in args.power:
            yamaha.set_power(device, args, power)

        for [input, mode] in args.toggle:
            yamaha.toggle_input(device, args, input, mode)

main()
