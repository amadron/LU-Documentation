# Client reference tables

[Client overview](./README.md) | [Networking](./Client%20Networking.md) | [Server contract](./Server%20Contract.md)

Numeric values that come up when reading packet captures, client logs, or server code. Names and
numbers follow DarkflameServer's enums at revision `8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4`,
which match the final client. Usage counts come from the 2011 content data.

## Packet IDs

The message ID is the 4-byte field after the service in the
[application header](./Client%20Networking.md#application-header).

### Client → server

| Service | ID | Message |
| --- | ---: | --- |
| `COMMON` (0) | 0 | `VERSION_CONFIRM` (also sent by the server) |
| `COMMON` (0) | 1 | `DISCONNECT_NOTIFY` (server → client) |
| `AUTH` (1) | 0 | `LOGIN_REQUEST` |
| `WORLD` (4) | 1 | `VALIDATION` |
| `WORLD` (4) | 2 | `CHARACTER_LIST_REQUEST` |
| `WORLD` (4) | 3 | `CHARACTER_CREATE_REQUEST` |
| `WORLD` (4) | 4 | `LOGIN_REQUEST` (character selected) |
| `WORLD` (4) | 5 | `GAME_MSG` |
| `WORLD` (4) | 6 | `CHARACTER_DELETE_REQUEST` |
| `WORLD` (4) | 7 | `CHARACTER_RENAME_REQUEST` |
| `WORLD` (4) | 14 | `GENERAL_CHAT_MESSAGE` |
| `WORLD` (4) | 19 | `LEVEL_LOAD_COMPLETE` |
| `WORLD` (4) | 21 | `ROUTE_PACKET` |
| `WORLD` (4) | 22 | `POSITION_UPDATE` |
| `WORLD` (4) | 23 | `MAIL` |
| `WORLD` (4) | 25 | `STRING_CHECK` |

### Server → client (`CLIENT`, 5)

| ID | Message |
| ---: | --- |
| 0 | `LOGIN_RESPONSE` |
| 2 | `LOAD_STATIC_ZONE` |
| 4 | `CREATE_CHARACTER` |
| 6 | `CHARACTER_LIST_RESPONSE` |
| 7 | `CHARACTER_CREATE_RESPONSE` |
| 8 | `CHARACTER_RENAME_RESPONSE` |
| 11 | `DELETE_CHARACTER_RESPONSE` |
| 12 | `GAME_MSG` |
| 14 | `TRANSFER_TO_WORLD` |
| 59 | `CHAT_MODERATION_STRING` |
| 62 | `SERVER_STATES` |

### RakNet packet IDs (first byte, no application header)

| ID | Meaning |
| ---: | --- |
| `0x24` | Replica construction |
| `0x25` | Replica destruction |
| `0x27` | Replica serialization |
| `0x53` | User packet: the application header follows |

## Game-message IDs

Game messages mentioned on these pages, from
[MessageType/Game.h](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dCommon/dEnums/MessageType/Game.h):

| ID | Message | Usual direction |
| ---: | --- | --- |
| 19 | `TELEPORT` | server → client |
| 26 | `SET_PLAYER_CONTROL_SCHEME` | server → client |
| 37 | `DIE` | server → client |
| 43 | `PLAY_ANIMATION` | server → client |
| 118 | `ECHO_START_SKILL` | server → other clients |
| 119 | `START_SKILL` | client → server |
| 133 | `SET_CURRENCY` | server → client |
| 139 | `PICKUP_ITEM` | client → server |
| 154 / 155 | `PLAY_FX_EFFECT` / `STOP_FX_EFFECT` | server → client |
| 159 / 160 | `REQUEST_RESURRECT` / `RESURRECT` | client → server / server → client |
| 202 | `KNOCKBACK` | server → client |
| 227 | `ADD_ITEM_TO_INVENTORY_CLIENT_SYNC` | server → client |
| 231 | `EQUIP_INVENTORY` | client → server |
| 248 / 249 | `OFFER_MISSION` / `RESPOND_TO_MISSION` | server → client / client → server |
| 254 / 255 | `NOTIFY_MISSION` / `NOTIFY_MISSION_TASK` | server → client |
| 364 | `REQUEST_USE` | client → server |
| 505 | `PLAYER_LOADED` | client → server |
| 509 | `PLAYER_READY` | server → client |
| 529 / 530 | `DISPLAY_MESSAGE_BOX` / `MESSAGE_BOX_RESPOND` | server → client / client → server |
| 762 | `PLAY_CINEMATIC` | server → client |
| 770 | `FIRE_EVENT_SERVER_SIDE` | client → server |
| 781 | `SCRIPT_NETWORK_VAR_UPDATE` | server → client |
| 850 | `PARSE_CHAT_MESSAGE` | client → server |
| 1042 | `NOTIFY_CLIENT_OBJECT` | server → client |
| 1145 | `SYNC_SKILL` | both |
| 1213 | `FIRE_EVENT_CLIENT_SIDE` | server → client |
| 1468 | `RESTORE_TO_POST_LOAD_STATS` | server → client |
| 1642 | `SERVER_DONE_LOADING_ALL_OBJECTS` | server → client |

## Component types

The component type numbers used in `ComponentsRegistry` (column `component_type`). "Serialized"
marks the components that write data into construction and serialization packets, in the order
given in the [server contract](./Server%20Contract.md#5-object-construction-and-serialization);
all others exist only locally on the client and/or server. "Rows" is the number of
`ComponentsRegistry` rows using the type.

| ID | Component | Serialized | Rows |
| ---: | --- | :---: | ---: |
| 1 | Controllable physics | yes | 776 |
| 2 | Render | yes | 13,457 |
| 3 | Simple physics | yes | 8,614 |
| 4 | Character | yes | 2 |
| 5 | Script | yes | 2,112 |
| 6 | Bouncer | yes | 46 |
| 7 | Destroyable (server: a buff block followed by the destroyable block) | yes | 1,970 |
| 9 | Skill | yes | 2,426 |
| 10 | Spawner | | 1 |
| 11 | Item | yes | 6,832 |
| 12–14 | Rebuild, rebuild start, rebuild activator | | 4, 84, 1 |
| 16 | Vendor | yes | 77 |
| 17 | Inventory | yes | 485 |
| 18 | Projectile physics | | 143 |
| 19 | Shooting gallery | yes | 12 |
| 20 | Rigid body phantom physics | yes | 80 |
| 22 | Chest | | 1 |
| 23 | Collectible | yes | 75 |
| 24 | Blueprint | | 7 |
| 25 | Moving platform | yes | 273 |
| 26 | Pet | yes | 38 |
| 27 | Platform boundary | | 157 |
| 28 | Module (rocket/car part) | | 426 |
| 29 | Arcade | | 6 |
| 30 | Havok vehicle physics | yes | 22 |
| 31 | Movement AI | | 108 |
| 32 | Exhibit | | 12 |
| 35 | Minifig | | 493 |
| 36 | Property | | 6 |
| 37 | Pet creator | | 1 |
| 38 | Model builder | | 2 |
| 39 | Scripted activity | yes | 116 |
| 40 | Phantom physics | yes | 489 |
| 41 | Springpad | | 5 |
| 42 | Model | yes | 1,578 |
| 43 | Property entrance | | 13 |
| 45 | Property management | | 1 |
| 46 | Vehicle physics | | 8 |
| 47 | Physics system | | 44 |
| 48 | Quick build | yes | 288 |
| 49 | Switch | yes | 24 |
| 50 | Minigame control | yes | 2 |
| 51 | Changeling | | 13 |
| 52 | Choice build | | 5 |
| 53 | Package | | 162 |
| 54–56 | Sound repeater, ambient 2D, ambient 3D | | 2, 2, 1 |
| 57 | Precondition | | 9 |
| 59 | Custom build assembly | | 1 |
| 60 | Base combat AI | yes | 215 |
| 61 | Module assembly | yes | 4 |
| 62 | Showcase model handler | | 6 |
| 63 | Racing module | | 301 |
| 64 | Generic activator | | 3 |
| 65 | Property vendor | | 2 |
| 66 | HF light direction gadget | | 1 |
| 67 / 68 | Rocket launch / rocket landing | | 39, 2 |
| 71 | Racing control | yes | 6 |
| 72 | Faction trigger | | 139 |
| 73 | Mission offer | | 181 |
| 74 | Racing stats | | 2 |
| 75 | LUP exhibit | yes | 1 |
| 77 | Sound trigger | yes | 2 |
| 78 | Proximity monitor | | 38 |
| 79 | Racing sound trigger | yes | 2 |
| 95 | User control | | 4 |
| 97 | Multi-zone entrance | | 2 |
| 100 | Donation vendor | yes | 4 |
| 102 | Achievement vendor | yes | 2 |
| 103 | Gate rush control | | 2 |
| 104 | Rail activator | | 10 |
| 105 | Roller | | 3 |
| 106 | Player forced movement | yes (players) | 1 |
| 107 | Crafting | | 1 |
| 108 | Possessable | yes | 29 |
| 109 | Level progression | yes (players) | — |
| 110 | Possessor | yes (players) | — |
| 113 | Property plaque | | 1 |
| 114 | Build border | | 4 |
| 116 | Culling plane | | 1 |

Types 109 and 110 are not in the registry; the server adds them to player characters. The
brick-by-brick component (76) is always written as a single `0` bit.

## LDF data types

LDF ("LEGO data format") is the typed key-value format used in `boot.cfg`, the cfg files, scene
files, object configuration in construction packets, and the character data block. Text form:
`key=type:value`.

| Type | Value |
| ---: | --- |
| 0 | UTF-16 text |
| 1 | Signed 32-bit integer |
| 3 | 32-bit float |
| 4 | 64-bit float |
| 5 | Unsigned 32-bit integer |
| 7 | Boolean |
| 8 | 64-bit integer |
| 9 | Object ID (signed 64-bit) |
| 13 | UTF-8 text (binary blobs such as XML) |

## Character XML

The `xmlData` value in `CREATE_CHARACTER` is an XML document with the root `<obj v="1">`. The
client reads its own character from it. Elements written by DarkflameServer:

| Element | Content | Server component |
| --- | --- | --- |
| `mf` | Minifigure appearance: hair color and style, shirt and pants color, shirt style, eyebrows, eyes, mouth | Character |
| `char` | Account (`acct`), coins (`cc`), GM level (`gm`), free-trial flag (`ft`), last login (`llog`), U-score (`ls`), last zone position and rotation (`lzx` ... `lzrw`), statistics (`stt`), claim codes (`co`) | Character, character component |
| `char/vl` | Visited levels (zone IDs) | Character component |
| `char/zs` | Statistics per zone | Character component |
| `char/ue` | Unlocked emotes | Character |
| `dest` | Health, imagination, and armor (current and maximum) | Destroyable |
| `buff` | Active buffs | Buff |
| `inv` | Inventories: `bag` (sizes per inventory type), `items` (items per inventory with LOT, object ID, slot, count, equipped, bound), `grps` (item groups), `pet` (tamed pets) | Inventory |
| `lvl` | Level, character version, speed base | Level progression |
| `flag` | Player flags (bit fields) | Character |
| `mis` | Missions: `done` and `cur` (current, with task progress) | Mission |
| `res` | Respawn checkpoints per world | Character |

A newly created character starts with `mf`, `char` (with `vl`), `dest`, `inv` (shirt and pants
equipped), `lvl`, and an empty `flag`
([UserManager.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/UserManager.cpp)).

## Object ID flags

| Bit | Meaning |
| ---: | --- |
| 46 | Client-local object (also set by the server for parent IDs it writes) |
| 58 | Spawned object |
| 60 | Character |

The zone control object always has the ID `0x3FFFFFFFFFFE`.
