from pyamaha import Zone, NetUSB
from sys import stderr
from re import search

def volume_up(dev, args):
    res = dev.request(Zone.set_volume(args.zone, 'up', None))
    if res.status_code != 200 or res.json()["response_code"] != 0:
        print("Can't increase device volume.", file=stderr)

def volume_down(dev, args):
    res = dev.request(Zone.set_volume(args.zone, 'down', None))
    if res.status_code != 200 or res.json()["response_code"] != 0:
        print("Can't decrease device volume.", file=stderr)

def radio_next(dev, args):
    res = dev.request(Zone.get_status(args.zone))
    if res.status_code != 200 or res.json()["response_code"] != 0:
        print("Can't play next radio station (can't get device status).", file=stderr)
        return

    if res.json()["input"] != "net_radio":
        print("Can't play next radio station (input is not 'net_radio').", file=stderr)
        return

    list_info = get_radio_list_info(dev)
    if list_info == None:
        print("Can't play next radio station (can't get list info).", file=stderr)
        return

    while list_info != ["Radio", "Podcasts"] and list_info != None:
        if not set_radio_list_control(dev, args.zone, "return", 0):
            print("Can't play next radio station (can't set list control).", file=stderr)
            return

        list_info = get_radio_list_info(dev)
        if list_info == None:
            print("Can't play next radio station (can't get list info).", file=stderr)
            return

    if not set_radio_list_control(dev, args.zone, "select", 0):
        print("Can't play next radio station (can't set list control).", file=stderr)
        return

    list_info = get_radio_list_info(dev)
    if list_info == None:
        print("Can't play next radio station (can't get list info).", file=stderr)
        return

    if not set_radio_list_control(dev, args.zone, "select", 0):
        print("Can't play next radio station (can't set list control).", file=stderr)
        return

    list_info = get_radio_list_info(dev)
    if list_info == None:
        print("Can't play next radio station (can't get list info).", file=stderr)
        return

    res = dev.request(NetUSB.get_play_info())
    if res.status_code != 200 or res.json()["response_code"] != 0:
        print("Can't play next radio station (can't get play info).", file=stderr)
        return

    current_station = search(r"(^.+) \(", res.json()["artist"]).groups()[0]
    new_station = 0

    try:
        new_station = list_info.index(current_station) + 1
    except ValueError:
        pass

    new_station %= len(list_info)

    if not set_radio_list_control(dev, args.zone, "play", new_station):
        print("Can't play next radio station (can't set list control).", file=stderr)
        return
    

def radio_prev(dev, args):
    res = dev.request(Zone.get_status(args.zone))
    if res.status_code != 200 or res.json()["response_code"] != 0:
        print("Can't play previous radio station (can't get device status).", file=stderr)
        return

    if res.json()["input"] != "net_radio":
        print("Can't play previous radio station (input is not 'net_radio').", file=stderr)
        return

    list_info = get_radio_list_info(dev)
    if list_info == None:
        print("Can't play previous radio station (can't get list info).", file=stderr)
        return

    while list_info != ["Radio", "Podcasts"] and list_info != None:
        if not set_radio_list_control(dev, args.zone, "return", 0):
            print("Can't play previous radio station (can't set list control).", file=stderr)
            return

        list_info = get_radio_list_info(dev)
        if list_info == None:
            print("Can't play previous radio station (can't get list info).", file=stderr)
            return

    if not set_radio_list_control(dev, args.zone, "select", 0):
        print("Can't play previous radio station (can't set list control).", file=stderr)
        return

    list_info = get_radio_list_info(dev)
    if list_info == None:
        print("Can't play previous radio station (can't get list info).", file=stderr)
        return

    if not set_radio_list_control(dev, args.zone, "select", 0):
        print("Can't play previous radio station (can't set list control).", file=stderr)
        return

    list_info = get_radio_list_info(dev)
    if list_info == None:
        print("Can't play previous radio station (can't get list info).", file=stderr)
        return

    res = dev.request(NetUSB.get_play_info())
    if res.status_code != 200 or res.json()["response_code"] != 0:
        print("Can't play previous radio station (can't get play info).", file=stderr)
        return

    current_station = search(r"(^.+) \(", res.json()["artist"]).groups()[0]
    new_station = 0

    try:
        new_station = list_info.index(current_station) - 1
    except ValueError:
        pass

    new_station %= len(list_info)

    if not set_radio_list_control(dev, args.zone, "play", new_station):
        print("Can't play previous radio station (can't set list control).", file=stderr)
        return

def get_radio_list_info(dev, index=0):
    res = dev.request(NetUSB.get_list_info("net_radio", index, 8, "en", "main"))
    if res.status_code != 200 or res.json()["response_code"] != 0:
        return None

    list_info = list(map(lambda item: item["text"],  res.json()["list_info"]))

    if res.json()["max_line"] - index >= 8:
        next_list_info = get_radio_list_info(dev, index + 8)
        if next_list_info == None:
            return None
        
        list_info += next_list_info

    return list_info

def set_radio_list_control(dev, zone, type, index):
    res = dev.request(NetUSB.set_list_control("main", type, index, zone))
    if res.status_code != 200 or res.json()["response_code"] != 0:
        return False

    return True
