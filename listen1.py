# -*- coding: utf-8 -*-
"""
What does this do......!
"""

from __future__ import print_function
try:
    from queue import Empty
except:  # Py2.7
    from Queue import Empty

import soco
from pprint import pprint
from soco.events import event_listener

#pick a device at random
device = soco.discover().pop()
# device = soco.SoCo('192.168.1.64')

print (device.player_name)
sub = device.renderingControl.subscribe()
sub2 = device.avTransport.subscribe()

while True:
    try:
        event = sub.events.get(timeout=0.5)
        print('-------Render event----------')
        pprint (event.variables)
    except Empty:
        pass
    try:
        event = sub2.events.get(timeout=0.5)
        print('-------AVtransport event----------')
        print ('transport state: {}'.format(event.transport_state))
        #pprint (event.variables)

        if event.current_track_duration == '0:00:00':
            print ('>>Playing stream (eg radio)')
            print ('content:  {}'.format(event.current_track_meta_data.stream_content))
            print ('show:     {}'.format(event.current_track_meta_data.radio_show))
            print ('station:  {}'.format(event.enqueued_transport_uri_meta_data.title))
        elif event.current_track_duration == '':
            print ('>>Playing from line in')
            print ('not handled....yet')
        else:
            print ('>>Playing from queue')
            print ('Artist:      {}'.format(event.current_track_meta_data.creator))
            print ('Album:       {}'.format(event.current_track_meta_data.album))
            print ('Track:       {}'.format(event.current_track_meta_data.title))
            print ('Playlist:    {}'.format(event.enqueued_transport_uri_meta_data.title))
            print ('Track uri    {}'.format(event.current_track_uri))
            if event.next_track_meta_data:
                print ('next Artist: {}'.format(event.next_track_meta_data.creator))
                print ('next Album:  {}'.format(event.next_track_meta_data.album))
                print ('next Track:  {}'.format(event.next_track_meta_data.title))

    except Empty:
        pass

    except KeyboardInterrupt:
        sub.unsubscribe()
        sub2.unsubscribe()
        event_listener.stop()
        break
