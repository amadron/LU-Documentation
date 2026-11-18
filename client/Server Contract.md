# Server contract

[Client overview](./README.md) | [Networking](./Client%20Networking.md) | [Reference tables](./Client%20Reference%20Tables.md) | [Troubleshooting](./Client%20Troubleshooting.md) | [Server protocol](../server/DarkflameServer%20Client-Server%20Protocol%20and%20Gameplay.md)

The LEGO Universe client cannot be changed, so any server has to adapt to it. This page lists
what a server must provide for an **unmodified final client** (network version 171022) to work.
It is the client's side of the contract that DarkflameServer implements.

Requirements are marked by how the client reacts when they are not met:

| Level | Meaning |
| --- | --- |
| **MUST** | Without it the client cannot connect, rejects the zone, misreads data, or hangs on a loading screen. |
| **SHOULD** | Without it a feature does not work, the UI shows wrong or empty content, or a client script waits forever. |
| **MAY** | Optional; the client works without it. |

The evidence for each requirement is the client's files and strings, and the way DarkflameServer
meets it (linked to the source at revision `8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4`). Where the
client's exact reaction to a violation is not known, the level reflects what breaks in practice.

## 1. Content parity

The server sends only IDs; the client looks everything up in its own files.

| # | Requirement | Level |
| --- | --- | --- |
| C1 | Use the **same content data** as the client: the same `cdclient.fdb` (server: its SQLite conversion) and the same zone files. LOTs, skill IDs, mission IDs, effect IDs, animation names, item IDs, and text IDs must exist in the client's data. | MUST |
| C2 | The checksum in `LOAD_STATIC_ZONE` must match the client's zone files. It is a checksum over the scene IDs, layer IDs, and revisions listed in the zone's `.luz` ([Zone::CalculateChecksum](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dZoneManager/Zone.cpp)). On mismatch the client reports "The client's map files revision checksum does not match the server's checksum." | MUST |
| C3 | The component layout the server serializes for a LOT must be the one the client derives from `ComponentsRegistry` for the same LOT (see [section 5](#5-object-construction-and-serialization)). | MUST |
| C4 | Check the client's `cdclient.fdb` MD5 sent in `VALIDATION` to reject modified or outdated clients (`check_fdb` in DarkflameServer). | MAY |
| C5 | Custom content (new zones, objects) must be added to the client *and* the server in the same form; a server cannot send new content to an unmodified client. | MUST |

## 2. Connection

| # | Requirement | Level |
| --- | --- | --- |
| N1 | Accept RakNet 3.25-compatible connections on UDP. A RakNet from another major version is not compatible. | MUST |
| N2 | Set RakNet's incoming password to `3.25 ND1` ([dNetCommon.h](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dNet/dNetCommon.h)). | MUST |
| N3 | Answer the client's `COMMON / VERSION_CONFIRM` with network version `171022` and the server's service type. | MUST |
| N4 | Frame every application packet with the 8-byte header (`0x53`, service, message ID, padding) and serialize fields in exactly the order and width the client expects. There are no per-field tags or lengths. | MUST |
| N5 | Run the authentication service at the address the client's `boot.cfg` names (`AUTHSERVERIP`); DarkflameServer's default port is 1001. | MUST |
| N6 | Send `DISCONNECT_NOTIFY` with a reason before closing a connection, so the client shows a message instead of a timeout. | SHOULD |
| N7 | Provide a patch server or the UGC/"3D services" of the original game. | MAY (not needed) |

## 3. Login and character selection

| # | Requirement | Level |
| --- | --- | --- |
| L1 | Reply to `AUTH / LOGIN_REQUEST` with `CLIENT / LOGIN_RESPONSE`: a result code, a session key, and the address and port of a world server for character selection. | MUST |
| L2 | Use the login result codes the client knows (`SUCCESS` 1, `WRONG_PASS` 8, `BANNED` 2, ...), so the login screen shows the right message. | SHOULD |
| L3 | Accept the session key in `WORLD / VALIDATION` on the world server and associate the connection with the account. | MUST |
| L4 | Answer `CHARACTER_LIST_REQUEST` with `CHARACTER_LIST_RESPONSE` (the account's characters with name, appearance, last zone, and equipped items). | MUST |
| L5 | Answer create, rename, and delete requests with their response messages; the character-creation screen waits for them. | MUST |
| L6 | On `LOGIN_REQUEST` (character chosen), send `TRANSFER_TO_WORLD` with the address and port of the instance of the character's zone. | MUST |

## 4. Entering a zone

The client expects this order. Each step waits for the previous one; a missing step leaves the
client on the loading screen.

| Step | Server action | Level |
| --- | --- | --- |
| Z1 | After validation, send `LOAD_STATIC_ZONE` with the zone ID (map, instance, clone), the map checksum (C2), and the player's spawn position. | MUST |
| Z2 | Wait for `LEVEL_LOAD_COMPLETE` from the client before sending objects. | MUST |
| Z3 | Send `CREATE_CHARACTER` with the compressed LDF block: `objid`, `template` (1), `name`, `gmlevel`, `chatmode`, `reputation`, `propertycloneid`, and `xmlData`, the character's XML (appearance, inventory, missions, flags, levels, statistics). The client builds its inventory and mission log from this XML. | MUST |
| Z4 | Send `SERVER_STATES`. | SHOULD |
| Z5 | Construct the **zone control object**: ID `0x3FFFFFFFFFFE` (a value the client also uses) with the zone's control template from `ZoneTable`. Client scripts use it constantly (`GAMEOBJ:GetZoneControlID`, 503 calls). | MUST |
| Z6 | Construct the player's own object, then all objects in its scope. | MUST |
| Z7 | Send `SERVER_DONE_LOADING_ALL_OBJECTS` to the player. | MUST |
| Z8 | When the client sends `PLAYER_LOADED`, send `PLAYER_READY` for the player and for the zone control object, and restore stats (`RESTORE_TO_POST_LOAD_STATS`). Client scripts react to this (`onPlayerReady`, `notifyPlayerReady`, `onPlayerLoaded`). | MUST |
| Z9 | Send pending state the UI needs right away: inventory sizes, mail count, team and friends status. | SHOULD |

DarkflameServer's implementation: the `LEVEL_LOAD_COMPLETE` case in
[WorldServer.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dWorldServer/WorldServer.cpp)
and `PLAYER_LOADED` in
[GameMessageHandler.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dGameMessages/GameMessageHandler.cpp).

## 5. Object construction and serialization

This is the most fragile part of the contract. Construction and serialization packets contain no
length or type information per component. The client reads them by knowing, from the LOT, which
components follow and how each one is laid out.

| # | Requirement | Level |
| --- | --- | --- |
| O1 | Give each object a unique 64-bit object ID. Use the ID flags the client understands: bit 46 for client-local IDs, bit 58 for spawned objects, bit 60 for characters ([eObjectBits.h](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dCommon/dEnums/eObjectBits.h)). | MUST |
| O2 | Write the base data of a construction in order: object ID, LOT, name, time since creation, optional LDF configuration, trigger flag, optional spawner/parent, optional spawner node, optional scale, object world state, optional GM level, then parent/child information. | MUST |
| O3 | Write the components in the client's fixed order, not in registry order. | MUST |
| O4 | In a serialization (update), every component that exists still writes its block; unchanged parts are skipped with "dirty" flags inside the block, not by leaving the block out. | MUST |
| O5 | Write the closing bit for the brick-by-brick component (DarkflameServer always writes `0`). | MUST |
| O6 | Construct objects for a client only within its scope (ghosting distance, plus objects that must always be in scope), and destroy them when they leave it. | SHOULD |

The component order used by DarkflameServer
([Entity::WriteComponents](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/Entity.cpp)),
for the components an object has:

1. Possessable
2. Module assembly
3. Controllable physics
4. Simple physics
5. Rigid body phantom physics
6. Havok vehicle physics
7. Phantom physics
8. Sound trigger, racing sound trigger
9. Buff, followed directly by destroyable
10. Collectible (destroyable first, if not yet written)
11. Pet
12. Character, preceded by possessor, level progression, and player forced movement
13. Item
14. Inventory
15. Script
16. Skill
17. Base combat AI
18. Quick build (destroyable first, if not yet written)
19. Moving platform
20. Switch
21. Vendor, donation vendor, achievement vendor
22. Bouncer
23. Scripted activity
24. Shooting gallery
25. Racing control
26. LUP exhibit
27. Model
28. Render
29. Destroyable, if not written before
30. Minigame control
31. Brick-by-brick (one `0` bit)

Destroyable data is written exactly once, at the first of these positions that applies. Errors in
this area typically show as invisible or misplaced objects, wrong health bars, or a client crash
when the object is constructed.

## 6. Gameplay

The client sends requests and expects specific answers. Representative pairs:

| Client sends | Server should respond with | Level |
| --- | --- | --- |
| `POSITION_UPDATE` | Apply to the player's controllable physics and replicate to other clients in range. | MUST |
| `REQUEST_USE` on an object | The object's reaction: a mission offer (`OFFER_MISSION`), vendor data, an activity start, a message box, ... | SHOULD |
| `START_SKILL` | Run the skill's behavior from the content data, apply damage and costs, send `ECHO_START_SKILL` to other clients, and update destroyable state. | SHOULD |
| `RESPOND_TO_MISSION` | `NOTIFY_MISSION` with the new mission state, task updates (`NOTIFY_MISSION_TASK`), and rewards. | SHOULD |
| Inventory requests (`EQUIP_INVENTORY`, `MOVE_ITEM_IN_INVENTORY`, ...) | Apply and keep the client's inventory in sync (`ADD_ITEM_TO_INVENTORY_CLIENT_SYNC`, ...); equipment changes are visible to others through serialization. | SHOULD |
| `BUY_FROM_VENDOR`, `SELL_TO_VENDOR` | Item changes and `SET_CURRENCY`. | SHOULD |
| `PICKUP_ITEM`, `PICKUP_CURRENCY` | Add the loot the server itself dropped earlier; reject anything else. | SHOULD |
| `PARSE_CHAT_MESSAGE` starting with `/` | Run the slash command; there is no separate command packet. | MAY |
| `REQUEST_RESURRECT` | `RESURRECT`, with the respawn position. | SHOULD |
| Activity, racing, pet, and building messages | The matching state changes and UI messages described in the server documentation. | SHOULD |

Additional rules:

- **Authority.** The client is trusted only for what it simulates (its own movement and
  presentation). Damage, loot, currency, mission progress, and inventory are decided by the server;
  a client request is a request, not a fact.
- **Movement by the server.** To move a player, send `TELEPORT` or `KNOCKBACK`; changing the
  position only in the server's state does not move the client.
- **Control schemes.** Activities that need special controls (racing, shooting gallery, pet
  taming, modular build) must switch them with `SET_PLAYER_CONTROL_SCHEME` and switch back
  afterwards.

## 7. Client scripts

The client runs its own Lua scripts for many objects (see [Client scripting](./Client%20Scripting.md)).

| # | Requirement | Level |
| --- | --- | --- |
| S1 | Send the network variables a client script expects, initially in the script component and on change with `SCRIPT_NETWORK_VAR_UPDATE`, using the variable names the client script reads. | SHOULD |
| S2 | Send the notifications (`NOTIFY_CLIENT_OBJECT`) and client-side events (`FIRE_EVENT_CLIENT_SIDE`) that client scripts wait for, with the expected names. | SHOULD |
| S3 | Handle `FIRE_EVENT_SERVER_SIDE` from client scripts for the objects that use it. | SHOULD |
| S4 | Keep the zone control object and named object groups available, because client scripts look them up (`GetZoneControlID`, `GetObjectsInGroup`). | SHOULD |

## 8. World transfers

| # | Requirement | Level |
| --- | --- | --- |
| T1 | Save the character before the transfer. | MUST |
| T2 | Send `TRANSFER_TO_WORLD` with an address and port the client can reach. The client then reconnects and runs the zone entry (section 4) again with the same session key. | MUST |
| T3 | Accept the same session on the target instance. | MUST |

## 9. Chat and social

| # | Requirement | Level |
| --- | --- | --- |
| H1 | Accept `GENERAL_CHAT_MESSAGE` and chat requests via `ROUTE_PACKET` and deliver chat to the right recipients. | SHOULD |
| H2 | Answer `STRING_CHECK` so the chat input knows whether text is allowed. | SHOULD |
| H3 | Answer friend, ignore, and team requests with the response messages the social UI expects. | SHOULD |
| H4 | Mail (`MAIL`) requests and responses for the mailbox UI. | MAY |
| H5 | Guilds: the client has a guild UI and messages, but guilds were never released. | MAY |

## What the client does not need

- Patch server, Akamai download manager, LEGO account web pages, crash-log server.
- The original blueprint and moderation services; a server can approve all models itself.
- The free-trial and subscription system. The client still contains its UI (`freetrial*.gfx`);
  DarkflameServer does not use it.

## Checklist

A minimal server that lets an unmodified client walk around in a zone needs:

- [ ] Same `cdclient.fdb` and map files as the client (C1, C2)
- [ ] RakNet 3.25, password `3.25 ND1`, version `171022` (N1–N3)
- [ ] Auth service at `AUTHSERVERIP` with `LOGIN_RESPONSE` (N5, L1)
- [ ] World validation and character list/create/select (L3–L6)
- [ ] `LOAD_STATIC_ZONE` → wait for `LEVEL_LOAD_COMPLETE` → `CREATE_CHARACTER` → zone control
      object → player and objects → `SERVER_DONE_LOADING_ALL_OBJECTS` → on `PLAYER_LOADED`
      `PLAYER_READY` (Z1–Z8)
- [ ] Exact component serialization for every LOT it constructs (O1–O5)
- [ ] `POSITION_UPDATE` handling and replication to other players (section 6)

Everything else — combat, missions, inventory, vendors, activities, building, chat — is required
feature by feature.
