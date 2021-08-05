from models import Room, Relay
import json
import os




eight_relays = {40:False, 38:False, 37:False, 36:False, 35:False, 33:False, 29:False, 31:False}

single_channel_room = Room()
eight_channel_room = Room()
single_channel = Relay(pin=11)
eight_channel = [Relay(pin=num) for num in eight_relays]


single_channel_room.add_relays(single_channel)
print('adding relay')
eight_channel_room.add_relays(eight_channel)
eight_channel_room.save()
print('saving room')

single_channel_room.save('./single_room_config.pickle')
print('saving room')
