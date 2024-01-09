from mathlib import Vector
from memory import make_object

from engines.trace import TraceFilterSimple,TraceType

from listeners import OnPlayerRunCommand

from players.constants import PlayerButtons
from players.entity import Player
from players.dictionary import PlayerDictionary
from filters.players import PlayerIter

from weapons.constants import WeaponSlot
from weapons.manager import weapon_manager
from weapons.dictionary import WeaponDictionary
from filters.weapons import WeaponIter

import time

weapon_instances = WeaponDictionary()

class PlayerWeaponPickupCooldown(Player):
	def __init__(self, index, caching=True):
		super().__init__(index, caching)
		self.last_pickup = 0

	def can_pickup(self):
		if time.time() - self.last_pickup > 1:
			return True
		return False

	def try_pickup(self):
		eye_location = self.get_eye_location()
		trace = self.get_trace_ray(trace_filter=TraceFilterSimple(ignore=[player for player in PlayerIter()], trace_type=TraceType.WORLD_ONLY))
		if not trace.did_hit():
			return
		trace_origin = eye_location + Vector.normalized(trace.end_position-eye_location)*90

		target_weapon = None
		target_distance = 20
		for other in WeaponIter():
			other_distance=Vector.get_distance(other.origin,trace_origin)
			if other_distance < target_distance:
				target_distance = other_distance
				target_weapon = other
		if not target_weapon:
			return
		
		target_weapon_slot = weapon_manager[target_weapon.classname].slot

		active_weapon = weapon_instances.from_inthandle(self.active_weapon_handle)
		active_weapon_slot = weapon_manager[active_weapon.classname].slot
		if (target_weapon_slot == WeaponSlot.PRIMARY):
			if self.primary:
				self.drop_weapon(self.primary.pointer)
		elif (target_weapon_slot == WeaponSlot.SECONDARY):
			if self.secondary:
				self.drop_weapon(self.secondary.pointer)
		else:
			return
		self.last_pickup = time.time()

		target_weapon.teleport(self.origin)
		if active_weapon_slot == target_weapon_slot:
			self.delay(0,self.weapon_switch,[target_weapon,0])

player_instances = PlayerDictionary(PlayerWeaponPickupCooldown)

@OnPlayerRunCommand
def on_prop_use(player, usercmd):
	if (player.dead or player.team < 2):
		return
	if (not usercmd.buttons & PlayerButtons.USE):
		return
	player = player_instances[player.index]
	if player.can_pickup():
		player.try_pickup()
	
	
	