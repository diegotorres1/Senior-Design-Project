# Author : Diego Torres
# Description : App for control system called by Main
# Date of Modification : 3/2/2018

# Libraries
from video_send import video_send
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-svip',default = '192.168.0.13',type = str, dest = 'server_ip',help = 'server_ip string')
    parser.add_argument('-svp',default='8000',type = int, dest = 'server_port',help='server port integer')
    parser.add_argument('-vp',default = '8006',type = int, dest = 'video_port',help='video port integer')
    parser.add_argument('-sp',default = '8005',type = int, dest = 'sensor_port',help='sensor port integer')

    args = parser.parse_args()
    vs = video_send(args.server_ip, args.video_port)
    vs.capture()

if __name__ == '__main__':
    main()
    print('client')
