# Place Objects and Configure Spawners

## 1. Placed objects and LOTs

A scene object becomes a runtime `Entity` using its LOT/template plus placement information such as transform, object ID, and settings. The LOT identifies the template; the runtime object ID identifies that particular instance.

Before placing an object, verify:

1. The LOT exists and is appropriate in [`Objects`](../../db/Objects.md).
2. Its component registrations are present in [`ComponentsRegistry`](../../db/ComponentsRegistry.md).
3. Every required component has a native server implementation and its supporting data rows.
4. Its script name (if any) resolves through [`ScriptComponent`](../../db/ScriptComponent.md) and `CppScripts.cpp`.
5. The object can be loaded by the current client/resource set.

`Entity::Initialize` does not blindly instantiate every declared component. Component types have explicit native construction paths, special cases, and ID/sentinel rules. A row in the registry is not proof that the server implements the behavior.

## 2. Entity placement settings

Scene placement data is read through the zone/level loading path and converted into `EntityInfo`. The server also uses entity settings (LDF/name-value data), groups, parent/child relationships, and spawn metadata. These settings may be consumed by components or native scripts after the entity is created.

When diagnosing a placed-but-inert entity, compare:

- the object LOT and transform in the scene resource;
- the CDClient object/component/script records;
- the names and values in entity settings;
- parent/child or group relationships expected by the behavior; and
- the script callbacks and component event handlers that consume them.

Keep IDs and namespaces distinct: LOTs, object IDs, component IDs, script-component IDs, scene IDs, and map IDs are not interchangeable.

## 3. Zone paths and spawner nodes

`Zone::LoadPath` reads typed paths. A spawner path contains its spawned LOT, respawn time, maximum total spawns, maintained population, spawner object ID, and network-active state. Its waypoints provide node positions/rotations and can also carry per-node settings.

The runtime `Spawner` receives `SpawnerInfo` and a collection of `SpawnerNode`s. The node structure includes:

- position and rotation;
- node ID and node population limit;
- weight used to choose among available nodes; and
- settings inherited from the spawner's base configuration or overridden for a node.

The first waypoint's settings act as the base for the network; later nodes can override individual values. Check the current parser/loader when relying on a particular setting—field support depends on path type and path version.

Spawner population behavior is affected by `amountMaintained`, `maxToSpawn`, respawn timing, activation flags, node limits, and whether a spawn trigger/group is used. A valid path can still fail to produce entities if its LOT is invalid, its nodes are malformed, or the spawner never becomes active.

## 4. Recommended workflow

1. Test the LOT as a static placed object first.
2. Add the minimum required component registrations and supporting table rows.
3. Verify construction and visibility for a player in the target scene.
4. Add spawner paths/nodes and configure one spawn at a time.
5. Verify spawn count, node selection, respawn, group behavior, and cleanup.
6. Only then add scripts or mission hooks that depend on the spawned entity.

For server-side behavior, continue with [Add Scripts and Server Behavior](./add-scripts-and-server-behavior.md). For runtime entity composition and replication, see [World Simulation and Entity Model](../DarkflameServer%20World%20Simulation%20and%20Entity%20Model.md).
