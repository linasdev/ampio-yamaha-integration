def volume_up(args):
    (host, zone) = args.host, args.zone
    print("Volume up! To host '" + host + "' and zone '" + zone + "'")

def volume_down(args):
    (host, zone) = args.host, args.zone
    print("Volume down! To host '" + host + "' and zone '" + zone + "'")

def next(args):
    (host, zone) = args.host, args.zone
    print("Next! To host '" + host + "' and zone '" + zone + "'")

def previous(args):
    (host, zone) = args.host, args.zone
    print("Previous! To host '" + host + "' and zone '" + zone + "'")
