########## Create Item Frame Shops by jgierer12 ###########
# for Purple_
# Creates Shops from Item Frames using Block 36. Watch http://youtu.be/wyTDHd5xTPE for more information & explanation!

########## VERSION 1.1 ###########
# fix bug #5 (CreateItemFrameShops)
# update video link


from pymclevel import TAG_List
from pymclevel import TAG_Byte
from pymclevel import TAG_Int
from pymclevel import TAG_Compound
from pymclevel import TAG_Short
from pymclevel import TAG_Double
from pymclevel import TAG_String
from pymclevel import TAG_Int_Array
from pymclevel import TAG_Float
from pymclevel import TAG_Long
import math


# List of old and new IDs copied from http://www.minecraftforum.net/topic/1994759-new-item-id-system/
IDs = [
	("0", "minecraft:air"),
	("1", "minecraft:stone"),
	("2", "minecraft:grass"),
	("3", "minecraft:dirt"),
	("4", "minecraft:cobblestone"),
	("5", "minecraft:planks"),
	("6", "minecraft:sapling"),
	("7", "minecraft:bedrock"),
	("8", "minecraft:flowing_water"),
	("9", "minecraft:water"),
	("10", "minecraft:flowing_lava"),
	("11", "minecraft:lava"),
	("12", "minecraft:sand"),
	("13", "minecraft:gravel"),
	("14", "minecraft:gold_ore"),
	("15", "minecraft:iron_ore"),
	("16", "minecraft:coal_ore"),
	("17", "minecraft:log"),
	("18", "minecraft:leaves"),
	("19", "minecraft:sponge"),
	("20", "minecraft:glass"),
	("21", "minecraft:lapis_ore"),
	("22", "minecraft:lapis_block"),
	("23", "minecraft:dispenser"),
	("24", "minecraft:sandstone"),
	("25", "minecraft:noteblock"),
	("26", "minecraft:bed"),
	("27", "minecraft:golden_rail"),
	("28", "minecraft:detector_rail"),
	("29", "minecraft:sticky_piston"),
	("30", "minecraft:web"),
	("31", "minecraft:tallgrass"),
	("32", "minecraft:deadbush"),
	("33", "minecraft:piston"),
	("34", "minecraft:piston_head"),
	("35", "minecraft:wool"),
	("36", "minecraft:piston_extension"),
	("37", "minecraft:yellow_flower"),
	("38", "minecraft:red_flower"),
	("39", "minecraft:brown_mushroom"),
	("40", "minecraft:red_mushroom"),
	("41", "minecraft:gold_block"),
	("42", "minecraft:iron_block"),
	("43", "minecraft:double_stone_slab"),
	("44", "minecraft:stone_slab"),
	("45", "minecraft:brick_block"),
	("46", "minecraft:tnt"),
	("47", "minecraft:bookshelf"),
	("48", "minecraft:mossy_cobblestone"),
	("49", "minecraft:obsidian"),
	("50", "minecraft:torch"),
	("51", "minecraft:fire"),
	("52", "minecraft:mob_spawner"),
	("53", "minecraft:oak_stairs"),
	("54", "minecraft:chest"),
	("55", "minecraft:redstone_wire"),
	("56", "minecraft:diamond_ore"),
	("57", "minecraft:diamond_block"),
	("58", "minecraft:crafting_table"),
	("59", "minecraft:wheat"),
	("60", "minecraft:farmland"),
	("61", "minecraft:furnace"),
	("62", "minecraft:lit_furnace"),
	("63", "minecraft:standing_sign"),
	("64", "minecraft:wooden_door"),
	("65", "minecraft:ladder"),
	("66", "minecraft:rail"),
	("67", "minecraft:stone_stairs"),
	("68", "minecraft:wall_sign"),
	("69", "minecraft:lever"),
	("70", "minecraft:stone_pressure_plate"),
	("71", "minecraft:iron_door"),
	("72", "minecraft:wooden_pressure_plate"),
	("73", "minecraft:redstone_ore"),
	("74", "minecraft:lit_redstone_ore"),
	("75", "minecraft:unlit_redstone_torch"),
	("76", "minecraft:redstone_torch"),
	("77", "minecraft:stone_button"),
	("78", "minecraft:snow_layer"),
	("79", "minecraft:ice"),
	("80", "minecraft:snow"),
	("81", "minecraft:cactus"),
	("82", "minecraft:clay"),
	("83", "minecraft:reeds"),
	("84", "minecraft:jukebox"),
	("85", "minecraft:fence"),
	("86", "minecraft:pumpkin"),
	("87", "minecraft:netherrack"),
	("88", "minecraft:soul_sand"),
	("89", "minecraft:glowstone"),
	("90", "minecraft:portal"),
	("91", "minecraft:lit_pumpkin"),
	("92", "minecraft:cake"),
	("93", "minecraft:unpowered_repeater"),
	("94", "minecraft:powered_repeater"),
	("95", "minecraft:chest_locked_aprilfools_super_old_legacy_we_should_not_even_have_this"),
	("96", "minecraft:trapdoor"),
	("97", "minecraft:monster_egg"),
	("98", "minecraft:stonebrick"),
	("99", "minecraft:brown_mushroom_block"),
	("100", "minecraft:red_mushroom_block"),
	("101", "minecraft:iron_bars"),
	("102", "minecraft:glass_pane"),
	("103", "minecraft:melon_block"),
	("104", "minecraft:pumpkin_stem"),
	("105", "minecraft:melon_stem"),
	("106", "minecraft:vine"),
	("107", "minecraft:fence_gate"),
	("108", "minecraft:brick_stairs"),
	("109", "minecraft:stone_brick_stairs"),
	("110", "minecraft:mycelium"),
	("111", "minecraft:waterlily"),
	("112", "minecraft:nether_brick"),
	("113", "minecraft:nether_brick_fence"),
	("114", "minecraft:nether_brick_stairs"),
	("115", "minecraft:nether_wart"),
	("116", "minecraft:enchanting_table"),
	("117", "minecraft:brewing_stand"),
	("118", "minecraft:cauldron"),
	("119", "minecraft:end_portal"),
	("120", "minecraft:end_portal_frame"),
	("121", "minecraft:end_stone"),
	("122", "minecraft:dragon_egg"),
	("123", "minecraft:redstone_lamp"),
	("124", "minecraft:lit_redstone_lamp"),
	("125", "minecraft:double_wooden_slab"),
	("126", "minecraft:wooden_slab"),
	("127", "minecraft:cocoa"),
	("128", "minecraft:sandstone_stairs"),
	("129", "minecraft:emerald_ore"),
	("130", "minecraft:ender_chest"),
	("131", "minecraft:tripwire_hook"),
	("132", "minecraft:tripwire"),
	("133", "minecraft:emerald_block"),
	("134", "minecraft:spruce_stairs"),
	("135", "minecraft:birch_stairs"),
	("136", "minecraft:jungle_stairs"),
	("137", "minecraft:command_block"),
	("138", "minecraft:beacon"),
	("139", "minecraft:cobblestone_wall"),
	("140", "minecraft:flower_pot"),
	("141", "minecraft:carrots"),
	("142", "minecraft:potatoes"),
	("143", "minecraft:wooden_button"),
	("144", "minecraft:skull"),
	("145", "minecraft:anvil"),
	("146", "minecraft:trapped_chest"),
	("147", "minecraft:light_weighted_pressure_plate"),
	("148", "minecraft:heavy_weighted_pressure_plate"),
	("149", "minecraft:unpowered_comparator"),
	("150", "minecraft:powered_comparator"),
	("151", "minecraft:daylight_detector"),
	("152", "minecraft:redstone_block"),
	("153", "minecraft:quartz_ore"),
	("154", "minecraft:hopper"),
	("155", "minecraft:quartz_block"),
	("156", "minecraft:quartz_stairs"),
	("157", "minecraft:activator_rail"),
	("158", "minecraft:dropper"),
	("159", "minecraft:stained_hardened_clay"),
	("170", "minecraft:hay_block"),
	("171", "minecraft:carpet"),
	("172", "minecraft:hardened_clay"),
	("173", "minecraft:coal_block"),
	("174", "minecraft:packed_ice"),
	("175", "minecraft:double_plant"),

	("256", "minecraft:iron_shovel"),
	("257", "minecraft:iron_pickaxe"),
	("258", "minecraft:iron_axe"),
	("259", "minecraft:flint_and_steel"),
	("260", "minecraft:apple"),
	("261", "minecraft:bow"),
	("262", "minecraft:arrow"),
	("263", "minecraft:coal"),
	("264", "minecraft:diamond"),
	("265", "minecraft:iron_ingot"),
	("266", "minecraft:gold_ingot"),
	("267", "minecraft:iron_sword"),
	("268", "minecraft:wooden_sword"),
	("269", "minecraft:wooden_shovel"),
	("270", "minecraft:wooden_pickaxe"),
	("271", "minecraft:wooden_axe"),
	("272", "minecraft:stone_sword"),
	("273", "minecraft:stone_shovel"),
	("274", "minecraft:stone_pickaxe"),
	("275", "minecraft:stone_axe"),
	("276", "minecraft:diamond_sword"),
	("277", "minecraft:diamond_shovel"),
	("278", "minecraft:diamond_pickaxe"),
	("279", "minecraft:diamond_axe"),
	("280", "minecraft:stick"),
	("281", "minecraft:bowl"),
	("282", "minecraft:mushroom_stew"),
	("283", "minecraft:golden_sword"),
	("284", "minecraft:golden_shovel"),
	("285", "minecraft:golden_pickaxe"),
	("286", "minecraft:golden_axe"),
	("287", "minecraft:string"),
	("288", "minecraft:feather"),
	("289", "minecraft:gunpowder"),
	("290", "minecraft:wooden_hoe"),
	("291", "minecraft:stone_hoe"),
	("292", "minecraft:iron_hoe"),
	("293", "minecraft:diamond_hoe"),
	("294", "minecraft:golden_hoe"),
	("295", "minecraft:wheat_seeds"),
	("296", "minecraft:wheat"),
	("297", "minecraft:bread"),
	("298", "minecraft:leather_helmet"),
	("299", "minecraft:leather_chestplate"),
	("300", "minecraft:leather_leggings"),
	("301", "minecraft:leather_boots"),
	("302", "minecraft:chainmail_helmet"),
	("303", "minecraft:chainmail_chestplate"),
	("304", "minecraft:chainmail_leggings"),
	("305", "minecraft:chainmail_boots"),
	("306", "minecraft:iron_helmet"),
	("307", "minecraft:iron_chestplate"),
	("308", "minecraft:iron_leggings"),
	("309", "minecraft:iron_boots"),
	("310", "minecraft:diamond_helmet"),
	("311", "minecraft:diamond_chestplate"),
	("312", "minecraft:diamond_leggings"),
	("313", "minecraft:diamond_boots"),
	("314", "minecraft:golden_helmet"),
	("315", "minecraft:golden_chestplate"),
	("316", "minecraft:golden_leggings"),
	("317", "minecraft:golden_boots"),
	("318", "minecraft:flint"),
	("319", "minecraft:porkchop"),
	("320", "minecraft:cooked_porkchop"),
	("321", "minecraft:painting"),
	("322", "minecraft:golden_apple"),
	("323", "minecraft:sign"),
	("324", "minecraft:wooden_door"),
	("325", "minecraft:bucket"),
	("326", "minecraft:water_bucket"),
	("327", "minecraft:lava_bucket"),
	("328", "minecraft:minecart"),
	("329", "minecraft:saddle"),
	("330", "minecraft:iron_door"),
	("331", "minecraft:redstone"),
	("332", "minecraft:snowball"),
	("333", "minecraft:boat"),
	("334", "minecraft:leather"),
	("335", "minecraft:milk_bucket"),
	("336", "minecraft:brick"),
	("337", "minecraft:clay_ball"),
	("338", "minecraft:reeds"),
	("339", "minecraft:paper"),
	("340", "minecraft:book"),
	("341", "minecraft:slime_ball"),
	("342", "minecraft:chest_minecart"),
	("343", "minecraft:furnace_minecart"),
	("344", "minecraft:egg"),
	("345", "minecraft:compass"),
	("346", "minecraft:fishing_rod"),
	("347", "minecraft:clock"),
	("348", "minecraft:glowstone_dust"),
	("349", "minecraft:fish"),
	("350", "minecraft:cooked_fished"),
	("351", "minecraft:dye"),
	("352", "minecraft:bone"),
	("353", "minecraft:sugar"),
	("354", "minecraft:cake"),
	("355", "minecraft:bed"),
	("356", "minecraft:repeater"),
	("357", "minecraft:cookie"),
	("358", "minecraft:filled_map"),
	("359", "minecraft:shears"),
	("360", "minecraft:melon"),
	("361", "minecraft:pumpkin_seeds"),
	("362", "minecraft:melon_seeds"),
	("363", "minecraft:beef"),
	("364", "minecraft:cooked_beef"),
	("365", "minecraft:chicken"),
	("366", "minecraft:cooked_chicken"),
	("367", "minecraft:rotten_flesh"),
	("368", "minecraft:ender_pearl"),
	("369", "minecraft:blaze_rod"),
	("370", "minecraft:ghast_tear"),
	("371", "minecraft:gold_nugget"),
	("372", "minecraft:nether_wart"),
	("373", "minecraft:potion"),
	("374", "minecraft:glass_bottle"),
	("375", "minecraft:spider_eye"),
	("376", "minecraft:fermented_spider_eye"),
	("377", "minecraft:blaze_powder"),
	("378", "minecraft:magma_cream"),
	("379", "minecraft:brewing_stand"),
	("380", "minecraft:cauldron"),
	("381", "minecraft:ender_eye"),
	("382", "minecraft:speckled_melon"),
	("383", "minecraft:spawn_egg"),
	("384", "minecraft:experience_bottle"),
	("385", "minecraft:fire_charge"),
	("386", "minecraft:writable_book"),
	("387", "minecraft:written_book"),
	("388", "minecraft:emerald"),
	("389", "minecraft:item_frame"),
	("390", "minecraft:flower_pot"),
	("391", "minecraft:carrot"),
	("392", "minecraft:potato"),
	("393", "minecraft:baked_potato"),
	("394", "minecraft:poisonous_potato"),
	("395", "minecraft:map"),
	("396", "minecraft:golden_carrot"),
	("397", "minecraft:skull"),
	("398", "minecraft:carrot_on_a_stick"),
	("399", "minecraft:nether_star"),
	("400", "minecraft:pumpkin_pie"),
	("401", "minecraft:fireworks"),
	("402", "minecraft:firework_charge"),
	("403", "minecraft:enchanted_book"),
	("404", "minecraft:comparator"),
	("405", "minecraft:netherbrick"),
	("406", "minecraft:quartz"),
	("407", "minecraft:tnt_minecart"),
	("408", "minecraft:hopper_minecart"),
	("417", "minecraft:iron_horse_armor"),
	("418", "minecraft:golden_horse_armor"),
	("419", "minecraft:diamond_horse_armor"),
	("420", "minecraft:lead"),
	("421", "minecraft:name_tag"),
	("422", "minecraft:command_block_minecart"),
	("2256", "minecraft:record_13"),
	("2257", "minecraft:record_cat"),
	("2258", "minecraft:record_blocks"),
	("2259", "minecraft:record_chirp"),
	("2260", "minecraft:record_far"),
	("2261", "minecraft:record_mall"),
	("2262", "minecraft:record_mellohi"),
	("2263", "minecraft:record_stal"),
	("2264", "minecraft:record_strad"),
	("2265", "minecraft:record_ward"),
	("2266", "minecraft:record_11"),
	("2267", "minecraft:record_wait"),
]

displayName = "Create Item Frame Shops"

inputs = (
	("Step 1: Select the item frames", "label"),
	("Step 2: Select the area where the Command Blocks are generated", "label"),
	("", "label"),
	("Step: ", ("I", "II")),
	("/give selector (\"//x\" etc. will be converted to position of the item frame): ", ("string", "value=@p[//x,//y,//z]")),
)

########## Fast data access ##########
from pymclevel import ChunkNotPresent
GlobalChunkCache = {}
GlobalLevel = None

def getChunk(x, z):
	global GlobalChunkCache
	global GlobalLevel
	chunkCoords = (x>>4, z>>4)
	if chunkCoords not in GlobalChunkCache:
		try:
			GlobalChunkCache[chunkCoords] = GlobalLevel.getChunk(x>>4, z>>4)
		except ChunkNotPresent:
			return None

	return GlobalChunkCache[chunkCoords]

def blockAt(x, y, z):
	chunk = getChunk(x, z)
	if chunk == None:
		return 0
	return chunk.Blocks[x%16][z%16][y]

def dataAt(x, y, z):
	chunk = getChunk(x, z)
	if chunk == None:
		return 0
	return chunk.Data[x%16][z%16][y]

def tileEntityAt(x, y, z):
	chunk = getChunk(x, z)
	if chunk == None:
		return 0
	return chunk.tileEntityAt(x, y, z)

def setBlockAt(x, y, z, block):
	chunk = getChunk(x, z)
	if chunk == None:
		return 0
	chunk.Blocks[x%16][z%16][y] = block

def setDataAt(x, y, z, data):
	chunk = getChunk(x, z)
	if chunk == None:
		return 0
	chunk.Data[x%16][z%16][y] = data

def tileEntityAt(x, y, z):
	chunk = getChunk(x, z)
	if chunk == None:
		return 0
	return chunk.tileEntityAt(x, y, z)

########## End fast data access ##########

def perform(level, box, options):
	global GlobalLevel
	GlobalLevel = level

	global itemFrames

	if options["Step: "] == "I":
		itemFrames = getItemFrames(level, box, options)
	else:
		if itemFrames:
			if box.maxx-box.minx < 5:
				raise Exception("The selection must be at least 5 blocks deep (x dimension)")
			elif box.maxz-box.minz < 5:
				raise Exception("The selection must be at least 5 blocks wide (z dimension)")

			createCommandBlocks(level, box, options)
		else:
			raise Exception("Please select the item frames first!")

def getItemFrames(level, box, options):
	itemFramesTemp = []

	for (chunk, slices, point) in level.getChunkSlices(box):

		for ent in chunk.Entities:
			x = int(ent["Pos"][0].value)
			y = int(ent["Pos"][1].value)
			z = int(ent["Pos"][2].value)

			entId = ent["id"].value

			if ent["Direction"].value == 0:
				displayX = ent["TileX"].value
				displayZ = ent["TileZ"].value+1
			elif ent["Direction"].value == 1:
				displayX = ent["TileX"].value-1
				displayZ = ent["TileZ"].value
			elif ent["Direction"].value == 2:
				displayX = ent["TileX"].value
				displayZ = ent["TileZ"].value-1
			else:
				displayX = ent["TileX"].value+1
				displayZ = ent["TileZ"].value

			itemId = ent["Item"]["id"].value
			itemData = ent["Item"]["Damage"].value

			if "tag" in ent["Item"]:
				itemTag = ent["Item"]["tag"].value
			else:
				itemTag = None

			if x >= box.minx and x < box.maxx and y >= box.miny and y < box.maxy and z >= box.minz and z < box.maxz and entId == "ItemFrame" and ent["Item"]:
				itemFramesTemp.append((displayX, y, displayZ, itemId, itemData, itemTag))

	return itemFramesTemp

def createCommandBlocks(level, box, options):

	commands = []

	selector = options["/give selector (\"//x\" etc. will be converted to position of the item frame): "]

	for (frameX, frameY, frameZ, itemId, itemData, itemTag) in itemFrames:
		level.setBlockAt(frameX, frameY, frameZ, 36) # Block 36

		selectorSlashIndex = selector.find("//")

		while selectorSlashIndex >= 0:
			if selector[selectorSlashIndex+2] == "x":
				selector = selector[:selectorSlashIndex]+str(frameX)+selector[selectorSlashIndex+3:]
			elif selector[selectorSlashIndex+2] == "y":
				selector = selector[:selectorSlashIndex]+str(frameY)+selector[selectorSlashIndex+3:]
			elif selector[selectorSlashIndex+2] == "z":
				selector = selector[:selectorSlashIndex]+str(frameZ)+selector[selectorSlashIndex+3:]

			selectorSlashIndex = selector.find("//")

		testforblockCommand = "/testforblock "+str(frameX)+" "+str(frameY)+" "+str(frameZ)+" minecraft:piston_extension"
		setblockCommand = "/setblock "+str(frameX)+" "+str(frameY)+" "+str(frameZ)+" minecraft:piston_extension"
		giveCommand = "/give "+selector+" "+getNewID(itemId)+" 1 "+str(itemData)+" {"+tagCode(itemTag)+"}"

		commands.append((testforblockCommand, setblockCommand, giveCommand))

	i = 0

	x = box.minx
	y = box.miny
	z = box.minz

	level.setBlockAt(x, y+2, z, 159) # Block
	level.setBlockDataAt(x, y+2, z, 5) # Block Data
	chunk = getChunk(x, z)
	chunk.dirty = True

	rsLen = 0
	direction = True

	for (testforblockCommand, setblockCommand, giveCommand) in commands:
		newPos = getNewPos(x, y, z, box, level, rsLen, direction)
		x = newPos[0]
		y = newPos[1]
		z = newPos[2]

		rsLen = newPos[3]
		direction = newPos[4]

		level.setBlockAt(x, y+2, z, 55) # Redstone Dust

		level.setBlockAt(x, y+1, z, 137) # Command Block
		chunk = getChunk(x, z)
		commandBlock = cmdBlock(x, y+1, z, testforblockCommand)
		chunk.TileEntities.append(commandBlock)
		chunk.dirty = True

		level.setBlockAt(x+1, y+1, z, 149) # Comparator
		level.setBlockDataAt(x+1, y+1, z, 1) # Comparator Data

		level.setBlockAt(x+1, y, z, 159) # Block
		level.setBlockDataAt(x+1, y, z, 9) # Block Data
		chunk = getChunk(x+1, z)
		chunk.dirty = True

		level.setBlockAt(x+2, y+1, z, 159) # Block
		level.setBlockDataAt(x+2, y+1, z, 9) # Block Data
		chunk = getChunk(x+2, z)
		chunk.dirty = True

		level.setBlockAt(x+3, y, z, 137) # Command Block
		chunk = getChunk(x+3, z)
		commandBlock = cmdBlock(x+3, y, z, setblockCommand)
		chunk.TileEntities.append(commandBlock)
		chunk.dirty = True

		level.setBlockAt(x+3, y+1, z, 76) # Torch
		level.setBlockDataAt(x+3, y+1, z, 1) # Torch Data

		level.setBlockAt(x+4, y+1, z, 137) # Command Block
		chunk = getChunk(x+4, z)
		commandBlock = cmdBlock(x+4, y+1, z, giveCommand)
		chunk.TileEntities.append(commandBlock)
		chunk.dirty = True

		i = i+1


def getNewID(oldID):
	newID = ""

	for (intID, strID) in IDs:
		if intID == str(oldID):
			newID = strID

	if newID == "":
		newID = str(oldID)

	return newID

def cmdBlock(x, y, z, command):
	control = TAG_Compound()
	control["id"] = TAG_String("Control")
	control["Command"] = TAG_String(command)
	control["x"] = TAG_Int(x)
	control["y"] = TAG_Int(y)
	control["z"] = TAG_Int(z)

	return control

def getNewPos(x, y, z, box, level, rsLen, direction):
	rsLen = rsLen+1

	if direction == True:

		if z < box.maxz-3:
			z = z+1

			if rsLen >= 15:
				rsLen = 0

				level.setBlockAt(x, y+1, z, 159) # Block
				level.setBlockDataAt(x, y+1, z, 9) # Block Data

				level.setBlockAt(x, y+2, z, 93) # Repeater
				level.setBlockDataAt(x, y+2, z, 2) # Repeater Data
				chunk = getChunk(x, z)
				chunk.dirty = True

				z = z+1

		else:
			direction = False

			rsLen = 2

			level.setBlockAt(x, y+1, z+1, 159) # Block
			level.setBlockDataAt(x, y+1, z+1, 9) # Block Data

			level.setBlockAt(x, y+2, z+1, 93) # Repeater
			level.setBlockDataAt(x, y+2, z+1, 2) # Repeater Data

			level.setBlockAt(x, y+3, z+1, 159) # Block
			level.setBlockDataAt(x, y+3, z+1, 9) # Block Data

			level.setBlockAt(x, y+4, z+1, 55) # Redstone Dust
			chunk = getChunk(x, z+1)
			chunk.dirty = True

			level.setBlockAt(x, y+2, z+2, 159) # Block
			level.setBlockDataAt(x, y+2, z+2, 9) # Block Data

			level.setBlockAt(x, y+3, z+2, 55) # Redstone Dust
			chunk = getChunk(x, z+2)
			chunk.dirty = True

			y = y+3

	else:

		if z > box.minz+3:
			z = z-1

			if rsLen >= 15:
				rsLen = 0

				level.setBlockAt(x, y+1, z, 159) # Block
				level.setBlockDataAt(x, y+1, z, 9) # Block Data

				level.setBlockAt(x, y+2, z, 93) # Repeater
				level.setBlockDataAt(x, y+2, z, 0) # Repeater Data
				chunk = getChunk(x, z)
				chunk.dirty = True

				z = z-1

		else:
			direction = True

			rsLen = 2

			level.setBlockAt(x, y+1, z-1, 159) # Block
			level.setBlockDataAt(x, y+1, z-1, 9) # Block Data

			level.setBlockAt(x, y+2, z-1, 93) # Repeater
			level.setBlockDataAt(x, y+2, z-1, 0) # Repeater Data

			level.setBlockAt(x, y+3, z-1, 159) # Block
			level.setBlockDataAt(x, y+3, z-1, 9) # Block Data

			level.setBlockAt(x, y+4, z-1, 55) # Redstone Dust
			chunk = getChunk(x, z-1)
			chunk.dirty = True

			level.setBlockAt(x, y+2, z-2, 159) # Block
			level.setBlockDataAt(x, y+2, z-2, 9) # Block Data

			level.setBlockAt(x, y+3, z-2, 55) # Redstone Dust
			chunk = getChunk(x, z-2)
			chunk.dirty = True

			y = y+3

	if y+3 > box.maxy:
		raise Exception("The selection must be higher (y dimension)")

	return (x, y, z, rsLen, direction)

def tagCode(nbt):
	if nbt == None:
		return ""

	elif type(nbt) is TAG_Compound:
		tags = []
		for subTag in nbt.value:
			tags.append(tagCode(subTag))
		if nbt.name:
			return nbt.name+":{"+"".join(tags)+"},"
		else:
			return "{"+"".join(tags)+"},"

	elif type(nbt) is TAG_List:
		tags = []
		for subTag in nbt.value:
			tags.append(tagCode(subTag))

		if nbt.name:
			return nbt.name+":["+"".join(tags)+"],"

		else:
			return "["+"".join(tags)+"],"

	else:
		if nbt.name:
			return nbt.name+":"+str(nbt.value)+","

		else:
			return str(nbt.value)+","