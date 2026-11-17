# Content Recipes

These are repeatable investigation and implementation patterns, not ready-made asset files. Each recipe assumes a test copy of the resource archive, CDServer database, and game database.

## Recipe A: Place an existing NPC/object in a zone

1. Find its LOT in [`Objects`](../../db/Objects.md) and inspect its registered components in [`ComponentsRegistry`](../../db/ComponentsRegistry.md).
2. Check the scene/resource placement data for the target zone and confirm the LOT, transform, object ID, groups, and settings.
3. Inspect any supporting component tables and server-side script mapping.
4. Load the zone and verify that the object is constructed for a nearby player.
5. Trigger its expected interaction and review world logs.

If it renders but does not behave, compare its data registrations with `Entity::Initialize` and the native component/script implementation.

## Recipe B: Add a spawn group

1. Identify a valid spawned LOT and verify its component/script dependencies.
2. Add or modify a spawner path with sensible node positions, rotations, IDs, node limits, and settings.
3. Set maintained population, maximum spawn count, respawn timing, and activation behavior intentionally.
4. Verify the spawner activates, selects valid nodes, spawns the expected count, and cleans up/resets correctly.
5. Test respawn and group/death-trigger behavior; do not infer those paths from a static spawn alone.

See [Spawner Nodes and Paths](./place-objects-and-configure-spawners.md#3-zone-paths-and-spawner-nodes).

## Recipe C: Make a map reachable

1. Verify the map ID, `ZoneTable` row, `zoneName`, and `maps/` resource.
2. Load the map locally through the normal master-managed path.
3. Add a client-relevant route using an existing boundary, mission/script transfer, GM test route, or supported private-zone flow.
4. Verify the target is selected by the master and the world reaches readiness.
5. Test entry, spawn position, return route, and saved-location behavior.

Adding a `ZoneTable` row does not automatically add a UI button, unlock requirement, mission route, or client-visible menu entry.

## Recipe D: Add mission-driven content

1. Identify the mission's giver, task target, prerequisites, and reward records in the relevant [`Missions`](../../db/Missions.md), [`MissionTasks`](../../db/MissionTasks.md), [`MissionNPCComponent`](../../db/MissionNPCComponent.md), text, and reward tables.
2. Verify that every referenced LOT/zone/item exists in the same static-data snapshot.
3. Check how the server's mission component and task handlers interpret the stored task type and target namespace.
4. Verify acceptance, objective credit, turn-in, and reward persistence independently.

The mission data reference is useful for table relationships, but exact runtime behavior must be checked in the server's mission/component handlers.

## Recipe E: Add a scripted interaction

1. Confirm a built-in component/script cannot express the behavior.
2. Define what owns state, what event starts the interaction, what validates the requester, and what result is sent to clients.
3. Implement/register the native behavior and provide the matching data records.
4. Test valid, invalid, repeated, and disconnect/zone-change cases.
5. If the action changes persistent state, verify it after leaving and re-entering the zone.

Use the [script and behavior guide](./add-scripts-and-server-behavior.md) and the [persistence reference](../DarkflameServer%20Data%20and%20Persistence%20Reference.md).
