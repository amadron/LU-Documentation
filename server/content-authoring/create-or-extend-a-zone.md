# Create or Extend a Zone

## Scope

This guide describes the server-side dependencies for loading a map. It is not a binary zone/scene editor tutorial: DarkflameServer parses the relevant resources but does not provide a complete authoring pipeline for producing them.

Relevant implementation: [`Zone.cpp`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dZoneManager/Zone.cpp), [`dZoneManager.cpp`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dZoneManager/dZoneManager.cpp), and [`InstanceManager.cpp`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dMasterServer/InstanceManager.cpp).

## 1. Preflight

Before editing data, confirm:

- the map ID is not already assigned to a different zone in the target CDClient database;
- the client and server use compatible CDClient/resource revisions;
- the zone file and every referenced scene/level asset are available to `AssetManager`;
- you can test with a separate game database and CDServer database; and
- you know how players will reach the map (existing transition, mission/script flow, private zone flow, or a controlled admin test).

A zone row is necessary but not sufficient. Availability, client UI, mission requirements, and a working transfer route can involve other systems.

## 2. Add or update zone metadata

The [`ZoneTable`](../../db/ZoneTable.md) row is keyed by map ID. The server reads fields including:

- `zoneName` to locate the zone asset;
- `scriptID` for the zone-control script;
- `zoneControlTemplate` for the zone-control entity;
- `ghostdistance_min` and `ghostdistance` for entity visibility thresholds;
- `population_soft_cap` and `population_hard_cap`;
- `petsAllowed`, `mountsAllowed`, `PlayerLoseCoinsOnDeath`, and `disableSaveLoc`.

Defaults and `-1` sentinel handling are implemented in code; do not assume an empty cell is equivalent to zero. Check the relevant consumer before adding or changing a value.

## 3. Supply the zone and scene resources

`Zone::GetFilePathForZoneID` constructs the zone path from `maps/` plus `zoneName`, normalizes separators, and lowercases the path for loading. Each scene reference in the zone file then resolves relative to the zone's directory.

The current parser reads versioned zone metadata, scene references, boundaries, spawn information, raw-terrain path, scene transitions, and path data. Each referenced scene/level file must be present and valid for its parser. Terrain data may be optional in some cases, but a missing required zone file aborts loading.

Keep the CDClient `zoneName` and the actual resource layout aligned. Also test the separate accessibility check: `dZoneManager::CheckIfAccessibleZone` looks for a zone-table row and an asset at `maps/` plus the stored zone name.

## 4. Define scenes and transitions

Scene references are loaded into `Level` objects. `dZoneManager::BuildSceneGraph` creates adjacency information from scene-transition points for general scenes. Zone boundaries, by contrast, store a destination map/instance and spawn location and are used for zone-level exits.

For each entry and exit, check:

- the referenced scene/layer exists;
- the spawn position is inside the intended scene and has safe ground/clearance;
- transition points refer to valid scenes;
- boundary destinations have valid map metadata and a reachable/loaded target; and
- the intended client loading path has the scene/checksum data it expects.

Scene-to-scene navigation and world-to-world transfer are separate paths. For transfer negotiation and instance selection, see [Architecture and Repository Structure](../DarkflameServer%20Architecture%20and%20Repository%20Structure.md).

## 5. Set runtime policy

Use the zone table and `WorldConfig` deliberately:

- Population caps affect master instance selection.
- Zone settings influence ghosting distance and rules such as mounts, pets, coin loss, and saved location.
- `WorldConfig` holds global movement, physics, respawn, property, level-cap, and other world-wide values; it is not a per-zone content table.
- A `zoneControlTemplate` and `scriptID` need to resolve to compatible object/component/script data.

Do not change a global `WorldConfig` value to solve a problem that is specific to one map unless the global effect is intended.

## 6. Load and validate

Use the normal master-managed startup path so that the world receives the correct map, instance, clone, and port arguments. Confirm the world reaches `WORLD_READY`; inspect the world log for zone-file, scene, terrain, component, or script-load errors.

Validate incrementally:

1. Load the zone with only its required scenes and spawn.
2. Confirm zone-control creation and scene-graph construction.
3. Confirm an entry path and each boundary/transition.
4. Add objects and spawners only after the empty-zone path works.
5. Test on a clean character and repeat a transfer/restart to catch saved-location or persistent-state effects.

Use the [Testing and Troubleshooting](./test-and-troubleshoot.md) checklist before calling the zone complete.
