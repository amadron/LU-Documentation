# Client packet formats

[Client overview](./README.md) | [Networking](./Client%20Networking.md) | [Reference tables](./Client%20Reference%20Tables.md) | [Server contract](./Server%20Contract.md)

Field-by-field layouts of the packets a client needs to log in, select a character, and enter a
zone. They are taken from DarkflameServer's serializers and parsers at revision
`8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4`, which work with the unmodified final client. Every
packet starts with the 8-byte [application header](./Client%20Networking.md#application-header);
the tables list the fields after it.

## Conventions

| Notation | Meaning |
| --- | --- |
| `u8`, `u16`, `u32`, `u64` | Unsigned little-endian integers |
| `i64` | Signed 64-bit integer (object IDs) |
| `f32` | 32-bit float |
| `bool` | 1 byte in packets written byte-aligned; 1 bit inside bit-packed data (game messages, replication) |
| `str(n)` | ASCII text in a fixed field of `n` bytes, padded with zeros. Default `n` = 33. |
| `wstr(n)` | UTF-16 text in a fixed field of `n` characters (2·`n` bytes), padded with zeros. Default `n` = 33. |
| `skip(n)` | `n` bytes the server ignores or writes as zero |

The login and character packets are byte-aligned. Game messages and replica data are
bit-packed: booleans take one bit, and later fields are not aligned to bytes.

## Handshake: `COMMON / VERSION_CONFIRM` (0)

Sent first on every new connection, by the client and answered by the server.

**Client → server**

| Field | Type | Notes |
| --- | --- | --- |
| Network version | `u32` | `171022` |
| — | `skip(4)` | |
| Service type | `u16` | `CLIENT` (5) |
| — | `skip(2)` | |
| Process ID | `u32` | Client process |
| Local port | `u16` | Should match the UDP source port |
| — | `skip(33)` | |

**Server → client**

| Field | Type | Notes |
| --- | --- | --- |
| Network version | `u32` | Must be `171022` for the final client |
| Unknown | `u32` | DarkflameServer writes `861228100` |
| Server's service type | `u32` | e.g. `AUTH` (1) or `WORLD` (4) |
| Unknown | `u64` | DarkflameServer writes `219818307120` |

## Login: `AUTH / LOGIN_REQUEST` (0)

| Field | Type |
| --- | --- |
| Username | `wstr(33)` |
| Password | `wstr(41)` |
| Language code | `u16` (Windows language ID, e.g. `0x0409` en-US, `0x0407` de-DE) |
| Client OS | `u8` (1 = Windows) |
| Memory statistics | `wstr(256)` |
| Video card | `wstr(128)` |
| Number of processors, processor type | `u32`, `u32` |
| Processor level, processor revision | `u16`, `u16` |
| OS version info size, major, minor, build, platform | 5 × `u32` |

The connection itself is encrypted by RakNet's secure-connection layer (see
[Networking](./Client%20Networking.md#transport)), but inside it the password is a plain field.
Anyone running a server receives the passwords users type.

## Login result: `CLIENT / LOGIN_RESPONSE` (0)

| Field | Type | Notes |
| --- | --- | --- |
| Result | `u8` | [Login result codes](./Client%20Networking.md#login-result-codes) |
| Event gates 1–8 | 8 × `str(33)` | Names of active events (seasonal content gating); may be empty |
| Version major, current, minor | 3 × `u16` | DarkflameServer default `1`, `10`, `64` |
| Session key | `wstr(33)` | Used later in `VALIDATION` |
| World server IP | `str(33)` | Address the client connects to next |
| Chat server IP | `str(33)` | Unused, empty |
| World server port | `u16` | |
| Chat server port | `u16` | Unused, 0 |
| CDN key | `str(33)` | Empty |
| CDN ticket | `str(37)` | Zero GUID |
| Language | `u32` | 0 = en_US |
| Country | `str(3)` | `US` |
| Just upgraded from free trial | `u8` | |
| Is free-trial account | `u8` | |
| Free-trial time remaining | `u64` | |
| Custom error message length | `u16` | Characters |
| Custom error message | UTF-16, length as above | Shown for some result codes |
| Stamp block size | `u32` | Bytes, including this field |
| Stamps | repeated: type `u32`, value `u32`, timestamp `u64` | Login timing markers (`PASSPORT_AUTH_...`), visible in the client log as `Stamp ...` |

## World validation: `WORLD / VALIDATION` (1)

| Field | Type | Notes |
| --- | --- | --- |
| Username | `wstr(33)` | |
| Session key | `wstr(33)` | From `LOGIN_RESPONSE` |
| `cdclient.fdb` checksum | `str(32)` | MD5 as hex text; sometimes followed by a zero byte |

## Character list

**Request:** `WORLD / CHARACTER_LIST_REQUEST` (2), no fields.

**Response:** `CLIENT / CHARACTER_LIST_RESPONSE` (6)

| Field | Type |
| --- | --- |
| Number of characters | `u8` |
| Index of the preselected character | `u8` |
| *Per character:* | |
| Object ID | `i64` |
| Unknown | `u32` (0) |
| Name | `wstr(33)` |
| Requested name awaiting approval | `wstr(33)` |
| Name rejected | `u8` |
| Is free-trial character | `u8` |
| Unknown | `str(10)` |
| Shirt color, shirt style, pants color, hair style, hair color | 5 × `u32` |
| Left hand, right hand, eyebrows, eyes, mouth | 5 × `u32` |
| Unknown | `u32` (0) |
| Last zone: map ID, instance | `u16`, `u16` |
| Last zone: clone ID | `u32` |
| Last login | `u64` (Unix time) |
| Number of equipped items | `u16` |
| Equipped item LOTs | `u32` each |

The client renders each minifigure in the selection screen from the appearance values and the
equipped LOTs; it has no other source for them.

## Character creation: `WORLD / CHARACTER_CREATE_REQUEST` (3)

| Field | Type | Notes |
| --- | --- | --- |
| Custom name | `wstr(33)` | May be empty |
| Predefined name: first, middle, last index | 3 × `u32` | Line numbers in `res/names/minifigname_*.txt` |
| — | `skip(9)` | |
| Shirt color, shirt style, pants color, hair style, hair color | 5 × `u32` | |
| Left hand, right hand, eyebrows, eyes, mouth | 5 × `u32` | |

**Response:** `CLIENT / CHARACTER_CREATE_RESPONSE` (7), one `u8`: `0` success,
`1` object ID unavailable, `2` name not allowed, `3` predefined name in use, `4` custom name in
use. After success, the server also sends a new character list.

**Rename:** `CHARACTER_RENAME_RESPONSE` (8), one `u8`: `0` success, `1` unknown error,
`2` name unavailable, `3` name in use. **Delete:** `DELETE_CHARACTER_RESPONSE` (11), one `u8`
(1 = deleted).

## Character selection: `WORLD / LOGIN_REQUEST` (4)

| Field | Type |
| --- | --- |
| Character object ID | `i64` |

The server answers with `TRANSFER_TO_WORLD` to the instance of the character's zone.

## Transfer: `CLIENT / TRANSFER_TO_WORLD` (14)

| Field | Type | Notes |
| --- | --- | --- |
| Server IP | `str(33)` | |
| Server port | `u16` | |
| Mythran shift | `u8` | Flag named after the staff ("Mythran") characters; DarkflameServer sets it for some GM transfers |

## Zone load: `CLIENT / LOAD_STATIC_ZONE` (2)

| Field | Type | Notes |
| --- | --- | --- |
| Map ID | `u16` | Row in `ZoneTable` |
| Instance ID | `u16` | |
| Clone ID | `u32` | DarkflameServer writes 0 here |
| Map checksum | `u32` | Over scene revisions; must match the client's `.luz` ([contract C2](./Server%20Contract.md#1-content-parity)) |
| Unknown | `u16` | 0 |
| Spawn position | 3 × `f32` | |
| Activity flag | `u32` | 0; 4 for activity worlds according to a server comment |

**Reply:** `WORLD / LEVEL_LOAD_COMPLETE` (19) when the client has loaded the zone. Only then does
DarkflameServer add the client as a replication participant and create the player object.

## Player character: `CLIENT / CREATE_CHARACTER` (4)

| Field | Type | Notes |
| --- | --- | --- |
| Block size | `u32` | Compressed size + 9 |
| Compressed | `u8` | 1 |
| Uncompressed size | `u32` | |
| Compressed size | `u32` | |
| Data | zlib | LDF block: number of entries `u32`, then entries |

LDF entries in the block: `objid` (object ID), `template` (`1`), `xmlData` (character XML, see
[reference tables](./Client%20Reference%20Tables.md#character-xml)), `name`, `gmlevel`,
`chatmode`, `reputation`, `propertycloneid`. Each binary LDF entry is: key length `u8` (in
bytes), key as UTF-16, type `u8` ([LDF types](./Client%20Reference%20Tables.md#ldf-data-types)),
value (text values with a `u32` length prefix).

## Game message envelope

`WORLD / GAME_MSG` (5) from the client and `CLIENT / GAME_MSG` (12) from the server share one
layout:

| Field | Type |
| --- | --- |
| Object ID | `i64` |
| Game-message ID | `u16` |
| Parameters | bit-packed, specific to the message |

Optional parameters are usually written as a flag bit followed by the value only if the flag is
set; parameters at their default value are left out this way. The exact parameters of each
message are in
[GameMessages.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dGameMessages/GameMessages.cpp).
Messages without parameters, such as `PLAYER_READY` and `SERVER_DONE_LOADING_ALL_OBJECTS`,
consist of the object ID and the message ID only.

## Movement: `WORLD / POSITION_UPDATE` (22)

Bit-packed, see [Physics and building](./Client%20Physics%20and%20Building.md#movement-and-the-server).
