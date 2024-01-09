from events.hooks import PreEvent
from players.entity import Player
from weapons.dictionary import WeaponDictionary

import math

weapon_instances = WeaponDictionary()

@PreEvent('weapon_fire')
def weapon_fire_pre(event):
    player = Player.from_userid(event['userid'])
    if (player.velocity.z == 0):
    	return
    if (math.sqrt(player.velocity.x*player.velocity.x+player.velocity.y*player.velocity.y)) < 220:
    	return
    # Get the weapon the player is firing.
    weapon = weapon_instances.from_inthandle(player.active_weapon_handle)
    # Store the weapon instance for later use (in weapon_fire_post()).
    player.fired_weapon = weapon

    weapon.set_network_property_float('m_fAccuracyPenalty', 0.0)

