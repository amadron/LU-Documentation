# Client world file formats

[Client overview](./README.md) | [Assets and content data](./Client%20Assets%20and%20Content%20Data.md) | [Server contract](./Server%20Contract.md)

The structure of the zone files that the client and the server both read. Layouts follow
DarkflameServer's readers in
[dZoneManager](https://github.com/DarkflameUniverse/DarkflameServer/tree/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dZoneManager/)
(`Zone.cpp`, `Level.cpp`, `Raw.cpp`). DarkflameServer skips parts it does not need (environment
and particle data); those parts are described only as far as their position in the file. Version
statistics come from the files in the final client.

All values are little-endian. Strings are written with a length prefix: `str8` = `u8` length +
ASCII, `wstr32` = `u32` length (characters) + UTF-16.

## How the files fit together

```text
ZoneTable (cdclient.fdb)  ── zone ID → zoneName (path of the .luz)
        │
        ▼
  nd_avant_gardens.luz ── zone: spawn point, scenes, boundaries, terrain file, paths
        ├── nd_avant_gardens.raw            terrain
        ├── nd_avant_gardens_10_....lvl     scene (objects, environment, particles)
        │     └── nd_avant_gardens_10_....lutriggers   triggers of that scene (optional)
        ├── nd_avant_gardens_10x1_audio.lvl audio scene
        └── nd_avant_gardens.evc            environment configurations (optional)
```

## Zone file `.luz`

39 files. Format versions in the final client: 41 (28 files), 40 (3), 39 (3), 38 (1), 36 (4).
DarkflameServer names the versions from `PrePreAlpha` (30) to `Latest` (41); fields marked with
a version are only present from that version on.

| Field | Type | Notes |
| --- | --- | --- |
| File format version | `u32` | |
| Map revision | `u32` | ≥ 36. Enters the map checksum. |
| World ID | `u32` | Should equal the map ID in `ZoneTable` |
| Spawn position | 3 × `f32` | ≥ 38 |
| Spawn rotation | 4 × `f32` (quaternion w, x, y, z) | ≥ 38 |
| Scene count | `u8` before 37, `u32` from 37 | |
| Scenes | repeated | see below |
| Boundary count | `u8` | Zone boundaries: lines where the player is moved to another zone |
| Boundaries | repeated: normal, point, destination map, instance, scene, spawn location | |
| Terrain file | `str8` | `.raw` file name |
| Zone name, description | `str8`, `str8` | > 30 |
| Scene transitions | count + entries | ≥ 32; camera and loading transitions between scenes |
| Path data length, path chunk version, path count | `u32`, `u32`, `u32` | ≥ 35 |
| Paths | repeated | see below |

### Scene entry

| Field | Type | Notes |
| --- | --- | --- |
| File name | `str8` | `.lvl` file next to the `.luz` |
| Scene ID | `u32` (≥ 33) | Enters the map checksum |
| Scene type (layer) | `u32` (≥ 33) | 0 = general, 1 = audio; enters the map checksum |
| Scene name | `str8` (≥ 33) | |
| Unknown | 3 × `f32` + `f32` | Only in version 33 |
| Color | 3 × `u8` (r, b, g) | ≥ 33; editor color of the scene |

A `.lutriggers` file with the scene's base name is loaded with the scene if it exists.

### Paths

A path has a version, a name, a type, and a list of waypoints; waypoints can carry LDF
configuration. Path types:

| Type | Use |
| ---: | --- |
| 0 | Movement (NPC routes) |
| 1 | Moving platform |
| 2 | Property (property boundary) |
| 3 | Camera |
| 4 | Spawner (each waypoint is a spawn node; LDF such as `spawner_node_id`, `spawner_max_per_node`) |
| 5 | Showcase |
| 6 | Race (racing checkpoints) |
| 7 | Rail |

The server uses movement, platform, spawner, race, and rail paths for simulation; the client uses
the same paths for camera paths, rail movement, and prediction. Client scripts read them with
`LEVEL:GetPathWaypoints` and `GAMEOBJ:GetWaypointPos`.

### Map checksum

The checksum that the server sends in `LOAD_STATIC_ZONE` is a Fletcher-style sum over the
32-bit map revision and, for each scene, the scene ID, the layer (scene type), and the scene's
revision from its `.lvl` file
([Zone::CalculateChecksum](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dZoneManager/Zone.cpp)).
Changing an object's position in a `.lvl` does not change the checksum unless the revision is
changed; adding or removing a scene or changing a revision does.

## Scene file `.lvl`

661 files. 650 use the chunk format, 11 an older format without chunks.

A chunked file is a sequence of chunks:

| Field | Type |
| --- | --- |
| Magic | `CHNK` |
| Chunk ID | `u32` |
| Chunk version | `u16` |
| Chunk type | `u16` |
| Size | `u32` (including this header) |
| Data start | `u32` (file offset) |

| Chunk ID | Content | Files containing it |
| ---: | --- | ---: |
| 1000 | File info: version, revision, offsets of the other chunks | 650 |
| 2000 | Environment: lighting, fog, sky, and similar settings | 486 |
| 2001 | Scene objects | 593 |
| 2002 | Particles placed in the scene | 129 |

Scene file versions in the final client: 48 (349 files), 47 (100), 46 (64), 45 (124), 44 (13).

### Scene objects (chunk 2001)

| Field | Type | Notes |
| --- | --- | --- |
| Object count | `u32` | |
| *Per object:* | | |
| Object ID | `u64` | Unique within the zone |
| LOT | `u32` | Template |
| Node type | `u32` | Version ≥ 38 |
| Glom ID | `u32` | Version ≥ 32 |
| Position | 3 × `f32` | |
| Rotation | 4 × `f32` | Quaternion (w, x, y, z) |
| Scale | `f32` | |
| Configuration | `wstr32` | LDF text: one `key=type:value` per line, e.g. `spawntemplate=1:4712`, `custom_script_server=0:...` |
| Unknown | `u32` | Read and not used by DarkflameServer |

The configuration decides much of an object's behavior: spawners (`spawntemplate`,
`spawner_node_id`), scripts that override the template's script (`custom_script_server`,
`custom_script_client`), groups (`groupID`), and activity settings. Two keys decide whether the
server creates an object at all
([Level.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dZoneManager/Level.cpp)):

- `loadOnClientOnly` — the object exists only on the client. The server skips it, and the
  client creates it from its own copy of the file without any server message.
- `gatingOnFeature` — the object belongs to a feature or event. The server loads it only if the
  feature is unlocked in the `FeatureGating` table or named in one of its `event_1` ...
  `event_8` settings, the same event names it sends to the client in `LOGIN_RESPONSE`.

All other objects are created by the server and reach the client through replication.

## Terrain `.raw`

One per zone (39 files, up to about 22 MB). After a header with version and chunk count, the
terrain consists of chunks; each chunk has an ID, width and height, offset, shader ID, four
texture IDs, a scale factor, a height map (`f32` per vertex), a color map, a light map (embedded
DDS), a blend map (embedded DDS), "flair" (placed vegetation and decoration with position,
rotation, scale, and color), and a scene map that assigns each terrain cell to a scene.
DarkflameServer reads the height map and scene map to find the scene at a position.

## Triggers `.lutriggers`

XML ("DO NOT EDIT THIS FILE"). Each trigger has an ID, events, and commands:

```xml
<triggers nextID="157">
    <trigger id="1" enabled="1">
        <event id="OnEnter">
            <command id="zonePlayer" target="target" args="312" />
        </event>
    </trigger>
    <trigger id="44" enabled="1">
        <event id="OnCreate">
            <command id="SetPhysicsVolumeEffect" target="self" args="push,75,0.9,2,-0.4..." />
        </event>
    </trigger>
</triggers>
```

Scene objects refer to a trigger by ID in their configuration. Commands such as `zonePlayer`
(send the player to another zone) are executed by the server; whether an object has triggers is
also written in its construction data (the trigger flag in
[contract O2](./Server%20Contract.md#5-object-construction-and-serialization)).

## Other zone files

| File | Format | Content |
| --- | --- | --- |
| `.evc` | XML | Binds scenes to environment configurations. Optional: if missing, the client logs "unable to load .EVC file ... Defaulting" and uses defaults. |
| `.aud` | — | Audio placement for the zone |
| `.ast` | Text | Asset list: one line per file to preload, prefixed with `A:` (for example sound banks) |
| `.zal` | Text | Zone asset list in `res/maps/assetlists`: animation and model files used in the zone |
| `*x1_audio.lvl` | `.lvl` | Audio scenes (scene type 1) |
