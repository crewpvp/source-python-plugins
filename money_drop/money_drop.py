from engines.precache import Model
from players.entity import Player
from mathlib import Vector, QAngle
from entities.entity import Entity
from entities.hooks import EntityCondition, EntityPreHook
from entities.constants import CollisionGroup, SolidFlags
from memory import make_object
from events import Event

import random 

money_ents = set()
model_path = 'models/props/cs_assault/money.mdl'

@Event('round_start')
def _round_start(game_event):
	money_ents.clear()

@Event('player_death')
def player_death(event):
	player =  Player.from_userid(event['userid'])
	for i in range(3):
		money = Entity.create('prop_physics')
		money.model = Model(model_path)
		money.origin = player.origin
		money.origin.z += 50
		angle = QAngle()
		QAngle.random(angle,0, 360)
		money.angles = angle
		money.spawn()

		money.collision_group = CollisionGroup.DEBRIS_TRIGGER
		money.solid_flags = SolidFlags.TRIGGER
		money.teleport(velocity=Vector(random.randint(-100,100),random.randint(-100,100),100) + (player.velocity*Vector(1,1,0)))
		money_ents.add(money.index)

@EntityPreHook(EntityCondition.equals_entity_classname('prop_physics'),"start_touch")
def on_pickup(stack_data):
	entity = make_object(Entity, stack_data[0])
	if entity.classname != 'prop_physics':
		return
	if entity.model.path.lower() != model_path:
		return
	other = make_object(Entity, stack_data[1])
	if not other.is_player():
		return
	player = make_object(Player, stack_data[1])
	if player.dead or player.team < 2 or player.cash >= 16000:
		return
	try:
		money_ents.remove(entity.index)
	except:
		return
	entity.remove()
	player.cash+=100