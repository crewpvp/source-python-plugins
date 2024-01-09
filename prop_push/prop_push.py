from listeners import OnPlayerRunCommand
from players.constants import PlayerButtons
from mathlib import Vector

@OnPlayerRunCommand
def on_prop_use(player, usercmd):
	if (player.dead or player.team < 2):
		return
	if (not usercmd.buttons & PlayerButtons.USE):
		return
	target = player.view_entity
	if not target or not target.classname.startswith('prop_physics'):
		return
	if (Vector.get_distance(player.origin, target.origin)) > 130:
		return
	if (not usercmd.buttons & PlayerButtons.BACK):
		view_vector = Vector.normalized(target.origin - player.origin)
	else:
		view_vector = Vector.normalized(player.origin - target.origin)
	push_scale = 150/(target.physics_object.mass/20)
	velocity = view_vector*Vector(push_scale,push_scale,0)
	target.teleport(velocity=velocity)