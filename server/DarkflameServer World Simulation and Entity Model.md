# DarkflameServer World Simulation and Entity Model

## Scope and source snapshot

This guide follows the normal `WorldServer` path from process startup through zone loading, entity creation, gameplay dispatch, simulation, and replication. It describes the local [DarkflameServer source checkout](https://github.com/DarkflameUniverse/DarkflameServer/tree/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/) at revision `8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4`.

The world is not determined by C++ alone. Runtime behavior is composed from C++ systems, static CDClient records, resource files, and native script mappings. For the process-level control plane and zone-transfer negotiation, see [Architecture and Repository Structure](./DarkflameServer%20Architecture%20and%20Repository%20Structure.md). For packet formats and wire-level dispatch, see [Client-Server Protocol and Gameplay](./DarkflameServer%20Client-Server%20Protocol%20and%20Gameplay.md).

## 1. World process startup

[`WorldServer.cpp`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dWorldServer/WorldServer.cpp) is both the process entry point and the main integration loop. The process receives its map, port, instance, maximum-client count, and clone as arguments from the master. Startup then establishes configuration, resource access, database access, and service connections before entering the loop.

| Startup stage | Main work |
|---|---|
| Process identity and configuration | Initializes diagnostics, signal handling, `worldconfig.ini`, logging, and zone/instance-specific process identity. |
| Resource access | Creates `AssetManager` from `client_location` (defaulting to `./res` relative to the binary directory). |
| Static game data | Opens `resServer/CDServer.sqlite` and loads the typed CDClient table data needed by the process. |
| Persistent game data | Connects to the configured game database and reads the master's connection information. |
| User and service setup | Initializes `UserManager` and chat filtering, creates the world `dServer`, then opens a separate RakNet peer for chat. |
| World contents | Creates `EntityManager` and `dZoneManager`. For non-zero maps it initializes physics and the zone; zone `0` does not load a normal map. |
| Runtime handlers | Registers slash commands for normal zones and enters the game loop. |

The world announces itself to the master only after its zone initialization has completed and the master connection is active. This readiness message is what lets the master release transfers queued while a new process was loading.

## 2. Zone and scene loading

[`dZoneManager.cpp`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dZoneManager/dZoneManager.cpp) coordinates zone setup. It creates a `Zone`, queries zone-level settings from CDClient, initializes the entity manager, creates the zone-control entity, initializes the zone data, builds the scene graph, loads world configuration, and spawns server-provided vanity content.

[`Zone.cpp`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dZoneManager/Zone.cpp) parses versioned zone resources. Depending on the file version and available assets, it loads:

- scene references and scene identifiers;
- zone boundaries, destination zones, and spawn locations;
- scene transitions and their points;
- path data used by moving objects and spawners;
- optional `.lutriggers` content associated with a scene; and
- optional raw terrain data used for scene/terrain lookups.

The referenced level/scene assets are loaded separately and contribute objects to the runtime scene graph. Missing or unsupported optional terrain data is logged and can leave the zone without terrain-based scene lookups; a missing required zone file aborts zone initialization.

Zone settings also influence runtime policy. The zone table can provide the zone-control LOT, ghosting-distance settings, and rules such as whether mounts, pets, saving locations, or coin loss are enabled. These are inputs to the server behavior, not properties inferred from the zone's C++ code alone.

## 3. Entity identity and construction

An [`Entity`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/Entity.h) is a runtime game object. Its **object ID** identifies the instance of that object; its **LOT** identifies the object template. `EntityInfo` carries creation inputs such as LOT, initial position/rotation, settings, and spawner metadata.

[`EntityManager::CreateEntity`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/EntityManager.cpp) centralizes creation and indexing:

1. Use an explicitly supplied ID when the caller provides one.
2. For player entities, use the persistent character identity with the character object flags.
3. For other entities, retain a supplied static ID or generate a new object ID.
4. Apply client/spawned object flags where applicable, initialize the entity, and insert it into the manager's object-ID index.
5. Record special roles such as the zone-control entity and named respawn points.

Object IDs and RakNet replica network IDs are different namespaces. The manager assigns a network ID when it first constructs an entity for replication; clients use the replicated form to track objects on the wire.

### Data-driven component composition

During [`Entity::Initialize`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/Entity.cpp), the server queries `CDComponentsRegistryTable` using the entity's LOT and component type. It then attaches native C++ component implementations for registered features such as controllable/simple physics, inventory, missions, skills, destruction, properties, vendors, pets, or racing.

The composition is partly data-driven, not wholly generic. Some behaviors have explicit C++ conditions, implicit components, special templates, or fallback setup. For example, characters receive character-oriented state and XML-backed components; some components may use IDs `0` or `-1` to represent implicit/design-defined cases. A database registration therefore does not guarantee that every component type has an implemented native behavior, and a code change may need both a component implementation and compatible CDClient data.

[`Component`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dComponents/Component.h) defines common hooks for update, use, loading/saving XML, and serialization. Components hold a reference to their parent entity and can register game-message handlers with it. The entity owns its components and forwards lifecycle or gameplay events to the relevant component/script paths.

## 4. Gameplay messages and native scripts

Client gameplay requests have an outer world packet and, for entity-directed operations, an inner game-message ID. The world handler parses the target entity and sender, performs the world-level sender check, and hands the inner operation to [`GameMessageHandler`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dGameMessages/GameMessageHandler.cpp).

The game-message handler resolves the logged-in user and target entity. Some message IDs are constructed through a typed-handler registry; many others are handled in a switch and forwarded to a `GameMessages` helper or component. Authorization is specific to the message and implementation: do not infer that every syntactically valid message is allowed for every entity or user.

A typical implementation path is:

```text
WorldServer packet dispatch
  -> validate sender and parse target/message IDs
  -> GameMessageHandler decodes operation
  -> message helper, entity component, manager, or native script
  -> mutate authoritative server-side state
  -> send a response and/or queue entity serialization
```

### Native script bridge

`ScriptComponent` resolves the script name through [`CppScripts.cpp`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dScripts/CppScripts.cpp). The registry maps game-content path strings (many end in `.lua`) to native C++ script factories. These path strings are identifiers; they do not mean that this server generally executes the corresponding Lua source at runtime. Script instances are managed by the C++ script system and are designed to be shared rather than owned and deleted by each component.

The entity/script interface exposes callbacks for lifecycle and gameplay events, including startup, update, use, timers, proximity, collision, player entry/exit, server-side events, and property interactions. A feature may therefore be split across a data registration, a `ScriptComponent`, a registered native class, and one or more entity/component callbacks. When a script appears inert, verify both its CDClient script name and the matching registry key in `CppScripts.cpp`.

## 5. Simulation, update ordering, and spawners

For a normal zone, the current `WorldServer` loop updates simulation before processing that frame's incoming master, chat, and world/client packets:

1. Compute elapsed time (`deltaTime`).
2. Update entities, including their component/script update hooks.
3. Step the physics world.
4. Refresh entity ghosting on its slower visibility-update cadence.
5. Update zone spawners.
6. Drain master and chat packets, then process a bounded batch of world packets.
7. Update RakNet replica state and perform timed saves/maintenance.

`EntityManager::UpdateEntities` performs an entity update pass, serializes queued entity changes, and then processes pending kills and deletions. The exact work done by each entity depends on its components and script. Zone `0` skips normal zone simulation and is primarily the login/character-selection world.

[`Spawner.cpp`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dZoneManager/Spawner.cpp) uses zone path/node information and spawner settings to decide when and where to create entities. Spawn behavior can be constrained by available nodes, per-node limits, maintained population, maximum total spawns, respawn timers, active state, and weighted node choice. Spawners can also connect to entity groups or react to spawned-entity death callbacks. The created entity is sent through the same entity/component construction path as other world objects.

## 6. Visibility and replication

The world server uses RakNet's replica manager, but entity construction and visibility are explicitly coordinated by `EntityManager`. The manager serializes construction/destruction data and maintains a set of entities eligible for ghosting.

For each player, ghosting compares the entity position with that player's ghost reference point. When an entity enters the configured visibility range, the server constructs it for that client; when it leaves the larger leave range, the server destroys that client's replica. Separate enter/leave thresholds reduce repeated create/destroy churn near a boundary. Zone configuration supplies the relevant distances, and special cases (such as collectables already recorded as collected) can prevent construction.

Replication is therefore not simply “broadcast every entity to every player.” The entity's observer/ghost state, player readiness, entity construction state, and zone-specific visibility rules all affect what a client receives. See [`EntityManager.cpp`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/EntityManager.cpp), [`dServer.cpp`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dNet/dServer.cpp), and the [protocol guide](./DarkflameServer%20Client-Server%20Protocol%20and%20Gameplay.md).

## 7. Feature tracing checklist

When investigating a gameplay feature, follow the full path rather than stopping at the first matching symbol:

1. Find the outer packet or game-message ID in `dCommon/dEnums/MessageType/`.
2. Trace the packet handler in `WorldServer.cpp` and the payload parser in `dNet/` or `GameMessageHandler.cpp`.
3. Identify the target entity's component registrations in CDClient and its component construction in `Entity.cpp`.
4. Follow the component, manager, or registered C++ script that changes state.
5. Check whether the result is serialized to clients, stored in the game database, or both.
6. Verify zone/configuration/client-data dependencies that can gate the behavior.

Useful starting points: [`WorldServer.cpp`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dWorldServer/WorldServer.cpp), [`Entity.cpp`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/Entity.cpp), [`EntityManager.cpp`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/EntityManager.cpp), [`GameMessageHandler.cpp`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dGameMessages/GameMessageHandler.cpp), [`Zone.cpp`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dZoneManager/Zone.cpp), and [`CppScripts.cpp`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dScripts/CppScripts.cpp).
