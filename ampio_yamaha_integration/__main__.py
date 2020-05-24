from __version__ import __version__
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Control a Yamaha MusicCast device')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)
    parser.add_argument('-d', '--device', action='store', required=True,
        help='hostname or IP address of the MusicCast device', dest='host')
    parser.add_argument('-z', '--zone', action='store', default='main',
        help='zone on which to execute all actions', dest='zone')
    parser.add_argument('-a', '--action', action='extend', required=True, nargs='+',
        help='one or more actions to execute',
        choices=[
            'volume_up',
            'volume_down',
            'next',
            'previous',
        ])
    
    
    args = parser.parse_args()

