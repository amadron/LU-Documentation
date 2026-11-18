# Client networking

[Client overview](./README.md) | [Server contract](./Server%20Contract.md) | [Server protocol](../server/DarkflameServer%20Client-Server%20Protocol%20and%20Gameplay.md)

This page describes networking from the client's point of view: which servers it talks to, in
which order, and which kinds of data it exchanges. Field layouts are documented in the server
source; the server's
[Client-Server Protocol](../server/DarkflameServer%20Client-Server%20Protocol%20and%20Gameplay.md)
page explains the server side of the same flows.

## Transport

| Property | Value |
| --- | --- |
| Library | RakNet, protocol of version 3.25 (DarkflameServer ships a compatible, modified RakNet 3.25) |
| Transport | UDP with RakNet's reliability layer (reliable, ordered, sequenced channels) |
| Connection password | `3.25 ND1` (RakNet's incoming password; a server must set it or the client cannot connect) |
| Network version | `171022` for the final client; the server announces it in the handshake (`client_net_version` in DarkflameServer's `sharedconfig.ini`) |
| Byte order and encoding | Little-endian binary through `RakNet::BitStream`; text as fixed-length or length-prefixed ASCII (`LUString`) or UTF-16 (`LUWString`) |
| Compression | zlib for large payloads (character data, some LDF blocks) |

### Application header

Every application packet starts with an 8-byte header:

| Bytes | Field |
| --- | --- |
| 1 | RakNet `ID_USER_PACKET_ENUM` (`0x53`) |
| 2 | Service (remote connection type): `COMMON` 0, `AUTH` 1, `CHAT` 2, `WORLD` 4, `CLIENT` 5 |
| 4 | Message ID within the service |
| 1 | Padding |

The client **sends** `COMMON`, `AUTH`, `WORLD`, and `CHAT` (routed) messages and **receives**
`CLIENT` messages. Entity replication additionally uses RakNet's own replica-manager packet IDs
without this header: construction `0x24`, destruction `0x25`, serialization `0x27`.

## Servers the client connects to

The client holds one connection at a time:

| Server | Address from | Default port (DarkflameServer) | Used for |
| --- | --- | --- | --- |
| Authentication | `AUTHSERVERIP` in `boot.cfg` | 1001 | Login |
| World (character selection) | Login response | from 3000 upwards | Character list, create, rename, delete |
| World (zone instance) | `TRANSFER_TO_WORLD` | from 3000 upwards | Playing in one zone instance |

Chat and social messages are sent to the world server, which routes them to the chat server
(`ROUTE_PACKET`). Master, chat, and database are internal to the server side; the client never
connects to them directly in DarkflameServer.

## Sequence

```text
Client                         Auth server             World (char. select)       World (zone)
  | RakNet connect ("3.25 ND1")    |                          |                        |
  |-- COMMON VERSION_CONFIRM ----->|                          |                        |
  |<- VERSION_CONFIRM (171022) ----|                          |                        |
  |-- AUTH LOGIN_REQUEST --------->|                          |                        |
  |<- CLIENT LOGIN_RESPONSE -------|  (result, session key, world address)            |
  |                                                           |                        |
  |-- connect + VERSION_CONFIRM ------------------------------>|                        |
  |-- WORLD VALIDATION (name, session key, fdb checksum) ----->|                        |
  |-- CHARACTER_LIST_REQUEST --------------------------------->|                        |
  |<- CHARACTER_LIST_RESPONSE ---------------------------------|                        |
  |-- LOGIN_REQUEST (character ID) --------------------------->|                        |
  |<- TRANSFER_TO_WORLD (address, port) -----------------------|                        |
  |                                                                                     |
  |-- connect + VERSION_CONFIRM + VALIDATION -------------------------------------------->|
  |<- LOAD_STATIC_ZONE (zone ID, map checksum, spawn position) ---------------------------|
  |   ... client loads the zone ...                                                       |
  |-- LEVEL_LOAD_COMPLETE --------------------------------------------------------------->|
  |<- CREATE_CHARACTER (compressed character data), SERVER_STATES ------------------------|
  |<- replica CONSTRUCTION of the player and of all objects in range ---------------------|
  |<- GAME_MSG SERVER_DONE_LOADING_ALL_OBJECTS --------------------------------------------|
  |-- GAME_MSG PLAYER_LOADED ------------------------------------------------------------>|
  |<- GAME_MSG PLAYER_READY, RESTORE_TO_POST_LOAD_STATS, ... ------------------------------|
  |   ... play: POSITION_UPDATE, GAME_MSG in both directions, replica SERIALIZE ...        |
```

### Login result codes

`LOGIN_RESPONSE` carries a result the client shows on the login screen. Values used by
DarkflameServer ([eLoginResponse.h](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dCommon/dEnums/eLoginResponse.h)):
`GENERAL_FAILED` 0, `SUCCESS` 1, `BANNED` 2, `PERMISSIONS_NOT_HIGH_ENOUGH` 5, `INVALID_USER` 6,
`ACCOUNT_LOCKED` 7, `WRONG_PASS` 8, `ACCOUNT_ACTIVATION_PENDING` 9, `ACCOUNT_DISABLED` 10,
`GAME_TIME_EXPIRED` 11, `FREE_TRIAL_ENDED` 12, `PLAY_SCHEDULE_TIME_UP` 13,
`ACCOUNT_NOT_ACTIVATED` 14.

### Disconnect reasons

Before closing a connection, a server can send `COMMON / DISCONNECT_NOTIFY` with a reason, which
the client shows as a message
([eServerDisconnectIdentifiers.h](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dCommon/dEnums/eServerDisconnectIdentifiers.h)):
unknown error, wrong game version, wrong server version, connection on invalid port, duplicate
login, server shutdown, map load failure, invalid session key, account not in pending list,
character not found, character corrupted, kick, save failure, free trial expired, play schedule
time done.

### World transfers

To change zone, the client asks the server (for example by using a rocket launch pad or a
portal). The server finds or starts an instance and sends `TRANSFER_TO_WORLD` with the new
address and port. The client disconnects, connects to the new world server, validates with the
same session key, and repeats the zone-loading part of the sequence. Character data is saved by
the old server before the transfer.

## What travels over the connection

### Packet names in the client

The executable contains the names of 379 `MSG_...` and `GM_...` identifiers. They are the
shared enum of the original server software, so they include server-internal messages
(instance manager `MSG_IM_...`, chat server, blueprint server) as well as localization keys for
chat and social results (`MSG_FRIEND_...`, `MSG_TEAM_...`, `MSG_GUILD_...`). The names that
the client itself sends or receives are mainly:

| Family | Examples in the executable |
| --- | --- |
| Client → auth | `MSG_AUTH_LOGIN_REQUEST`, `MSG_AUTH_LOGOUT_REQUEST`, `MSG_AUTH_CREATE_NEW_ACCOUNT_REQUEST` |
| Client → world | `MSG_WORLD_CLIENT_VALIDATION`, `..._CHARACTER_LIST_REQUEST`, `..._CHARACTER_CREATE_REQUEST`, `..._CHARACTER_DELETE_REQUEST`, `..._CHARACTER_RENAME_REQUEST`, `..._LOGIN_REQUEST`, `..._GAME_MSG`, `..._LEVEL_LOAD_COMPLETE`, `..._POSITION_UPDATE`, `..._MAIL`, `..._ROUTE_PACKET`, `..._STRING_CHECK`, `..._GENERAL_CHAT_MESSAGE`, `..._HANDLE_FUNNESS`, `..._TOP_5_ISSUES_REQUEST`, `..._REQUEST_UGC_MANIFEST_INFO`, `..._BLUEPRINT_GET_ALL_DATA_REQUEST` |
| Server → client | `MSG_CLIENT_LOGIN_RESPONSE`, `..._LOAD_STATIC_ZONE`, `..._CREATE_CHARACTER`, `..._CHARACTER_LIST_RESPONSE`, `..._CHARACTER_CREATE_RESPONSE`, `..._TRANSFER_TO_WORLD`, `..._SERVER_STATES`, `..._GAME_MSG`, `..._MAIL`, friend, ignore, team, and guild responses, `..._BLUEPRINT_SAVE_RESPONSE`, `..._MODEL_INSTANTIATE_RESPONSE`, `..._GENERAL_TEXT_FOR_LOCALIZATION`, `..._IN_LOGIN_QUEUE` |
| Shared | `MSG_SERVER_VERSION_CONFIRM`, `MSG_SERVER_DISCONNECT_NOTIFY`, `MSG_SERVER_GENERAL_NOTIFY` |

### Game messages

Most gameplay runs through `GAME_MSG`: a packet with the object ID it concerns, a game-message
ID, and message-specific parameters. DarkflameServer's
[MessageType/Game.h](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dCommon/dEnums/MessageType/Game.h)
declares about 1,600 game-message IDs. The same message can usually go either way; whether the
client sends it, accepts it, or both depends on the message. The Lua method names in client
scripts (`PlayFXEffect`, `FireEventServerSide`, ...) are the same messages.

| Direction | Typical messages |
| --- | --- |
| Client → server | `PLAYER_LOADED`, `REQUEST_USE`, `START_SKILL`, `SYNC_SKILL`, `REQUEST_SERVER_PROJECTILE_IMPACT`, `RESPOND_TO_MISSION`, `MESSAGE_BOX_RESPOND`, `EQUIP_INVENTORY`, `MOVE_ITEM_IN_INVENTORY`, `BUY_FROM_VENDOR`, `PICKUP_ITEM`, `PICKUP_CURRENCY`, `FIRE_EVENT_SERVER_SIDE`, `PARSE_CHAT_MESSAGE` (slash commands), `REQUEST_RESURRECT`, `REQUEST_DIE` |
| Server → client | `SERVER_DONE_LOADING_ALL_OBJECTS`, `PLAYER_READY`, `ECHO_START_SKILL`, `PLAY_FX_EFFECT`, `STOP_FX_EFFECT`, `PLAY_ANIMATION`, `OFFER_MISSION`, `NOTIFY_MISSION`, `NOTIFY_MISSION_TASK`, `ADD_ITEM_TO_INVENTORY_CLIENT_SYNC`, `SET_CURRENCY`, `MODIFY_LEGO_SCORE`, `DIE`, `RESURRECT`, `TELEPORT`, `KNOCKBACK`, `SET_PLAYER_CONTROL_SCHEME`, `SCRIPT_NETWORK_VAR_UPDATE`, `NOTIFY_CLIENT_OBJECT`, `FIRE_EVENT_CLIENT_SIDE`, `DISPLAY_MESSAGE_BOX`, `UI_MESSAGE_SERVER_TO_SINGLE_CLIENT`, `PLAY_CINEMATIC` |

### Replication

Objects reach the client through RakNet's replica system:

1. **Construction** — the object ID, template (LOT), name, optional configuration (LDF), parent,
   spawner, scale, GM level, followed by the **initial state of every serialized component** in
   a fixed order.
2. **Serialization** — later changes; only components with changed ("dirty") data write their
   update, again in the same order.
3. **Destruction** — the object leaves the client's scope or is deleted.

The server decides which objects a client receives: objects within the ghosting distance of the
player, plus objects marked as always in scope. The client's `S_GHOSTING_RADIUS_SCALAR`
setting and the script calls `AddObjectToAlwaysInScopeList` / `onScopeChanged` relate to this
mechanism.

There is no length field per component. If a component writes too many or too few bits, every
following component and object in the packet is read wrongly. See
[Server contract](./Server%20Contract.md#5-object-construction-and-serialization).

### Character data

`CREATE_CHARACTER` sends the player's own character as a zlib-compressed LDF block with the
object ID, name, GM level, chat mode, reputation, property clone ID, and `xmlData`: the
character's XML document with minifigure appearance, inventory, missions, flags, levels, and
statistics. The client reads its inventory and mission states from this XML when it enters a
zone (client scripts can react with `onCharacterUnserialized`), and later changes arrive as game
messages.
