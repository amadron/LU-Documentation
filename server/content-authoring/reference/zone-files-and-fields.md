# Zone Files and Fields Reference

## Scope

This is a guide to fields and resource relationships consumed by the inspected server parser, not a complete official file-format specification or an asset-editor manual. The implementation is in [`Zone.h`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dZoneManager/Zone.h), [`Zone.cpp`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dZoneManager/Zone.cpp), and [`dZoneManager.cpp`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dZoneManager/dZoneManager.cpp).

## Zone metadata to resource path

`Zone::GetFilePathForZoneID` queries `CDZoneTable` by map ID, constructs `maps/` plus `zoneName`, lowercases the path, and normalizes backslashes to forward slashes. The resource directory is derived from that path; referenced scene filenames are resolved relative to it.

The separate accessibility check tests for a `ZoneTable` row and an asset at `maps/` plus the stored name. Keep the row and resource archive consistent and test on the target platform's asset lookup behavior.

## Zone-file data consumed by the parser

The current parser reads fields conditionally by file version. At a high level, the zone resource can carry:

- file-format version and map/scene revision data;
- world/map identity, spawn position, and spawn rotation;
- a list of scene references (filename, scene/layer identifiers, type, and metadata);
- boundary normals/points, destination map/instance, destination scene, and spawn location;
- raw terrain path and optional terrain data;
- scene transitions and their points; and
- path chunk metadata and typed paths.

The `Zone::FileFormatVersion` enum in this source lists versions `30`, `32`, `33`, `35`, `36`, `37`, `38`, `39`, `40`, and `41`; its comment says version timing is guessed. Treat parser branches as the reliable statement of this checkout's behavior, not as a guarantee for other exporters.

## Scene and path types

`SceneRef` points to a `Level` loaded from the zone's resource directory. Scene transitions connect scene IDs/layers; `dZoneManager::BuildSceneGraph` uses those connections for general scenes. Zone boundaries describe zone-level destinations.

The `PathType` enum currently defines:

| Value | Type | Typical server consumer |
|---:|---|---|
| 0 | Movement | Path-driven entity behavior |
| 1 | MovingPlatform | Moving-platform component |
| 2 | Property | Property bounds/metadata |
| 3 | Camera | Camera path behavior |
| 4 | Spawner | Spawner network and spawn nodes |
| 5 | Showcase | Showcase-related path data |
| 6 | Race | Racing path data |
| 7 | Rail | Rail movement/activation |

The parser reads type-specific fields only for applicable path types and versions. Do not assume that a waypoint field meaningful for one type is interpreted for every other type.

## Spawner path fields

The `SpawnerPath` structure contains:

| Field | Role in current code |
|---|---|
| `spawnedLOT` | Template/LOT used for spawned entities. |
| `respawnTime` | Delay used by the spawner's respawn logic. |
| `maxToSpawn` | Limit on total spawns (`-1` is used as no fixed maximum). |
| `amountMaintained` | Population target the spawner tries to maintain. |
| `spawnerObjID` | Source object ID for the spawner network. |
| `spawnerNetActive` | Network-active/activation setting read from the path. |

Waypoints provide spawn-node position/rotation and settings. The first node's settings act as shared base configuration; a later node can override individual keys. Each node also has a maximum concurrent count and weight. Runtime behavior is implemented in [`Spawner.cpp`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dZoneManager/Spawner.cpp) and detailed in [Place Objects and Configure Spawners](../place-objects-and-configure-spawners.md).

## ZoneTable fields most relevant to new maps

See the [exported ZoneTable reference](../../../db/ZoneTable.md) for the full local snapshot. Fields consumed by runtime code include:

- identity/path: `zoneID`, `zoneName`;
- script/control: `scriptID`, `zoneControlTemplate`;
- population: `population_soft_cap`, `population_hard_cap`;
- visibility: `ghostdistance_min`, `ghostdistance`;
- policy: `petsAllowed`, `mountsAllowed`, `PlayerLoseCoinsOnDeath`, `disableSaveLoc`.

This is not the full table contract. The client may read additional fields that the server does not directly consume.
