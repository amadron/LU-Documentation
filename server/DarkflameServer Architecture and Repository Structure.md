# DarkflameServer Architecture and Repository Structure

## Scope and source snapshot

This document describes the `DarkflameServer` source at the revision below. It is an architecture and code-navigation guide, not a complete protocol specification or an installation tutorial.

- Repository: [DarkflameUniverse/DarkflameServer](https://github.com/DarkflameUniverse/DarkflameServer/tree/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/)
- Source revision reviewed: `8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4`
- Documentation index: [server/README.md](./README.md)
- Project setup and build instructions: [README.md](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/README.md)
- Additional repository documentation: [docs/](https://github.com/DarkflameUniverse/DarkflameServer/tree/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/docs/)
- Client protocol and gameplay flow: [DarkflameServer Client-Server Protocol and Gameplay](./DarkflameServer%20Client-Server%20Protocol%20and%20Gameplay.md)
- Detailed world loading, entity/component composition, scripts, simulation, and replication: [DarkflameServer World Simulation and Entity Model](./DarkflameServer%20World%20Simulation%20and%20Entity%20Model.md)
- Game database, CDClient data, migrations, and character persistence: [DarkflameServer Data and Persistence Reference](./DarkflameServer%20Data%20and%20Persistence%20Reference.md)
- Static game data and player persistence: [LEGO Universe Data Model and Public Research](../LEGO%20Universe%20Data%20Model%20and%20Public%20Research.md)
- GM permissions, commands, and support workflows: [DarkflameServer Gamemaster Guide](./DarkflameServer%20Gamemaster%20Guide.md)
- Complete registered slash-command list: [DarkflameServer Command Reference](./DarkflameServer%20Command%20Reference.md)

The codebase evolves. Check the current source and its README before relying on implementation details described here.

## 1. System overview

DarkflameServer (DLU) is a C++ server emulator for LEGO Universe. It is not a single server executable: it is a set of cooperating network services, shared libraries, game data, and support tools.

```text
                         +--------------------+
                         |     MasterServer   |
                         | service registry,  |
                         | sessions, instances|
                         +----+----------+----+
                              |          |
                   control / |          | control / session
                    registry |          |
                  +----------+--+     +-+----------------+
                  | AuthServer  |     | ChatServer       |
                  +-------------+     +--------+---------+
                                               |
                                               | chat messages
                                               |
 Client <---- game protocol ----> +------------+----------+
                                  | WorldServer processes |
                                  | one per zone instance |
                                  +-----------------------+
                                         |             |
                                         |             +--> CDClient SQLite
                                         +-----------------> Game database
```

The diagram is conceptual. Each service is a separate process and can have its own listening socket, configuration, and main loop. World processes are created on demand by the master for map/instance/clone combinations. The master also coordinates service registration and player movement between zones.

### Main runtime processes

| Process | Main responsibility | Code entry point |
|---|---|---|
| `MasterServer` | Coordinates the universe: connects to persistent data, owns the instance manager, starts or restarts services, and routes session and zone-transfer coordination. | [dMasterServer/MasterServer.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dMasterServer/MasterServer.cpp), [dMasterServer/InstanceManager.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dMasterServer/InstanceManager.cpp) |
| `AuthServer` | Accepts client authentication/login traffic and participates in the master-coordinated session flow. | [dAuthServer/AuthServer.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dAuthServer/AuthServer.cpp) |
| `ChatServer` | Handles chat, friends/ignores, and team-related service state; it can also host the optional chat web API. | [dChatServer/ChatServer.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dChatServer/ChatServer.cpp) |
| `WorldServer` | Runs a loaded world/zone, accepts gameplay traffic, updates entities and simulation, and communicates with the master and chat services. | [dWorldServer/WorldServer.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dWorldServer/WorldServer.cpp) |

`WorldServer` is not necessarily one process for the whole game. The master launches it with map, instance, clone, port, and player-capacity arguments. Zone `0` is a special world-server mode used in the startup/login flow; it does not initialize a normal map zone.

## 2. Process and request lifecycle

### Startup and service coordination

1. `MasterServer` reads `masterconfig.ini`, initializes logging and diagnostics, connects to the configured game database, prepares the client-data database, and runs migrations.
2. The master creates its server endpoint and stores connection information for other services in the game database.
3. If pre-starting services is enabled, it launches the chat service, a zone-0 world process, the initial public world, and the auth service. World instances can also be started later when requested.
4. `AuthServer`, `ChatServer`, and `WorldServer` use the shared `dServer` transport wrapper to connect back to the master. They report their service/zone information as part of this connection.
5. The master tracks registered services and world instances. It can start auth or chat again after a disconnect; world instances are separately created and removed as their lifecycle changes.

The operating-system process creation is implemented in [dMasterServer/Start.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dMasterServer/Start.cpp). The instance manager selects a free port, assigns a zone identity and capacities, and starts `WorldServer` in [dMasterServer/InstanceManager.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dMasterServer/InstanceManager.cpp).

### Login and entering a world

At a high level, client login spans more than one process:

1. The client connects to the authentication endpoint and submits login traffic.
2. Authentication and the master coordinate session validation.
3. A world process receives a master response for the pending session, verifies the session-key hash it expects, and creates the user state for that client.
4. In zone `0`, the world process requests/sends the character list rather than loading a map. A selected character is then handled by the world service.
5. Once the client completes world loading, the world process adds it to the entity-replication flow and constructs its in-world character/entity state.

Relevant implementations include [dAuthServer/AuthServer.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dAuthServer/AuthServer.cpp), [dWorldServer/WorldServer.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dWorldServer/WorldServer.cpp), and the user lifecycle in [dGame/UserManager.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/UserManager.cpp). This summary is intentionally not a packet-by-packet authentication specification.

### Zone transfers and instances

When gameplay requests a transfer, the current world asks the master to resolve a target map and clone. The master:

- finds a suitable existing instance, or starts a new world process;
- keeps transfer requests pending while a new instance is not ready;
- requests an affirmation from a ready destination before returning connection/zone details to the client; and
- redirects pending requests if an instance shuts down.

The relevant state and decisions are in [dMasterServer/InstanceManager.h](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dMasterServer/InstanceManager.h) and [dMasterServer/InstanceManager.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dMasterServer/InstanceManager.cpp). This design separates universe-level routing from simulation within a world process.

## 3. Networking and service boundaries

### Shared transport

[dNet/](https://github.com/DarkflameUniverse/DarkflameServer/tree/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dNet/) contains packet definitions, serialization helpers, service/message identifiers, and the common `dServer` wrapper. The transport is based on RakNet. The wrapper manages a listening peer and, for non-master services, a separate peer used to connect to the master. World processes also establish a chat connection.

Packets use a common service/message header followed by service-specific payloads serialized through RakNet bit streams. The message families are separated into headers such as `AuthPackets`, `ChatPackets`, `MasterPackets`, `WorldPackets`, and the game-message types. The exact wire format and message semantics should be verified in the corresponding packet code before making protocol changes.

For world processes, `dServer` configures RakNet's replica manager and network-ID manager. Gameplay entities are explicitly constructed, serialized, and scoped to clients by the entity manager rather than being automatically exposed to every connection.

### Service-specific behavior

- **Master connection:** services report information and receive control/session/transfer messages.
- **Client connection:** auth, chat, and world traffic are handled by their respective services; a world process handles gameplay packets and game messages.
- **World-to-chat connection:** world processes forward chat-related traffic to the chat service.
- **Optional web surface:** `ChatServer` can start its embedded web server and register chat API routes, controlled by chat configuration.

The network boundary is distributed across [dNet/](https://github.com/DarkflameUniverse/DarkflameServer/tree/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dNet/), each service's packet handler, and `dGame/dGameMessages/`. Do not assume every client-originated packet maps directly to a single gameplay function.

## 4. Gameplay and world simulation

### Entity/component model

The in-world model is component-oriented:

- [Entity](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/Entity.h) represents an object with an object ID, template/LOT, hierarchy, settings, and a collection of components.
- [EntityManager](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/EntityManager.h) creates, indexes, updates, destroys, serializes, and replicates entities. It also performs spatial visibility/ghosting updates so clients receive relevant nearby entities.
- Components implement behavior and state such as character, physics, inventory, missions, skills, destruction, properties, pets, vendors, racing, and triggers. They are grouped under [dGame/dComponents/](https://github.com/DarkflameUniverse/DarkflameServer/tree/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dComponents/).
- [GameMessages](https://github.com/DarkflameUniverse/DarkflameServer/tree/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dGameMessages/) defines typed game messages and their routing/serialization. `GameMessageHandler` dispatches client messages to the relevant entities.
- [dGame/dInventory/](https://github.com/DarkflameUniverse/DarkflameServer/tree/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dInventory/), [dGame/dMission/](https://github.com/DarkflameUniverse/DarkflameServer/tree/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dMission/), [dGame/dBehaviors/](https://github.com/DarkflameUniverse/DarkflameServer/tree/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dBehaviors/), and [dGame/dPropertyBehaviors/](https://github.com/DarkflameUniverse/DarkflameServer/tree/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dPropertyBehaviors/) contain related gameplay subsystems.

Entity composition is partly data-driven. Component registry and template data are read from the client-data database; `Entity` uses those rows to decide which native components to attach. This means a gameplay object's effective behavior is usually a combination of server implementation and client-derived data.

### Native script mapping

[dScripts/](https://github.com/DarkflameUniverse/DarkflameServer/tree/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dScripts/) organizes native gameplay scripts into areas such as `02_server`, `ai`, `client`, `EquipmentScripts`, `EquipmentTriggers`, and `zone`. These are built as C++ targets and assembled into the `dScripts` library.

[CppScripts.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dScripts/CppScripts.cpp) maps script-path identifiers (many end in `.lua`) to native C++ script classes. Those identifiers correspond to game content; their presence does not imply that this codebase generally interprets Lua source at runtime. Scripts integrate with entity components and world/game-message events.

### Zones, assets, physics, and navigation

- [dZoneManager/](https://github.com/DarkflameUniverse/DarkflameServer/tree/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dZoneManager/) owns the currently loaded zone, its configuration, spawners, scene graph, and zone-control entity.
- [Zone.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dZoneManager/Zone.cpp) loads zone/scene data from the asset manager, including scene transitions, path/spawner information, and terrain data when available.
- [dPhysics/](https://github.com/DarkflameUniverse/DarkflameServer/tree/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dPhysics/) provides the server-side physics world and collision/entity primitives.
- [dNavigation/](https://github.com/DarkflameUniverse/DarkflameServer/tree/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dNavigation/) wraps navigation mesh functionality. The build prepares navigation data from the `navmeshes` resource archive.
- [dWorldServer/WorldServer.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dWorldServer/WorldServer.cpp) drives the update loop: packet handling, entity updates, physics stepping, ghosting, and spawner updates are performed as part of world simulation.

The server reads game resources from a separately supplied client/resource directory. The project does not include or distribute the LEGO Universe client files; see the official repository README for supported resource setup and checksums.

## 5. Data and persistence

DLU has two distinct data stores with different purposes.

### Game database

The game database stores server-owned and player-owned state: accounts, characters, character XML, inventory-related data, mail, friends/ignores, properties, activity/command logs, leaderboards, and other persistent records.

The abstraction is exposed through [GameDatabase.h](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dDatabase/GameDatabase/GameDatabase.h) and interfaces in `dDatabase/GameDatabase/ITables/`. The selected implementation is created by [Database.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dDatabase/GameDatabase/Database.cpp):

- `database_type=sqlite` selects SQLite. The checked-in `resources/sharedconfig.ini` currently uses SQLite by default, and this backend enables WAL mode.
- `database_type=mysql`, `mariadb`, or `maria` selects the MariaDB/MySQL Connector/C++ implementation.

Configuration keys for both backends are in [resources/sharedconfig.ini](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/resources/sharedconfig.ini). Despite the `mysql_*` names, the selected backend is controlled separately by `database_type`.

### Client-data database

`CDClientDatabase` is a separate SQLite database containing static game/client metadata such as zone, component, object/template, mission, and other content tables. `CDClientManager` and generated table wrappers provide query access.

At startup the master ensures a server-side `resServer/CDServer.sqlite` is available. If it is absent, it can reuse an existing SQLite file or convert a client `cdclient.fdb`; the world service then opens this prepared SQLite database. This static-data store is not the same thing as the player/game database.

### Migrations

`MigrationRunner` runs migrations for the game database and the client-data SQLite database. It records migration history and selects the game-database migration set based on the configured backend. Migration SQL lives under [migrations/](https://github.com/DarkflameUniverse/DarkflameServer/tree/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/migrations/). Some migrations also perform data transformation in C++ rather than only executing SQL.

## 6. Repository structure

| Path | Role |
|---|---|
| `dAuthServer/` | Authentication process entry point and auth packet dispatch. |
| `dChatServer/` | Chat process, player/team containers, chat packet handling, filtering, and optional web API routes. |
| `dMasterServer/` | Master process, service/instance coordination, and child-process startup. |
| `dWorldServer/` | World process entry point, game loop, packet routing, and world runtime integration. |
| `dNet/` | RakNet-based transport wrapper, packet layouts, serialization helpers, and service/message identifiers. |
| `dCommon/` | Shared configuration, logging, diagnostics, utilities, serialization, math, client identifiers, and common types. |
| `dDatabase/` | Client-data and game-database access, backend implementations, table interfaces, and migration logic. |
| `dGame/` | Core gameplay model and managers, split further into components, messages, entities, inventory, missions, behaviors, and utilities. |
| `dZoneManager/` | Zone loading/runtime state, scenes, paths, spawners, and zone-level settings. |
| `dScripts/` | Native C++ gameplay scripts, organized by game-content area and registered through `CppScripts`. |
| `dPhysics/`, `dNavigation/` | Simulation collision/physics and navigation mesh support. |
| `dChatFilter/`, `dWeb/` | Chat filtering and embedded HTTP/web support used by services. |
| `resources/` | Default `.ini` configuration, chat filter data, and navigation mesh archive copied/prepared during configuration. |
| `vanity/` | Server-provided informational/credit XML and markdown assets. |
| `migrations/` | SQL/data migrations for game and client-data stores. |
| `thirdparty/` | Vendored or fetched dependencies, including RakNet, SQLite, Mongoose, and navigation libraries. |
| `tests/` | CTest targets, including common utilities and game/component/message/zone-manager tests. |
| `docs/` | Focused project references, including [Commands.md](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/docs/Commands.md), vanity notes, and chat API specifications. |
| `cmake/`, `CMakeLists.txt`, `CMakeVariables.txt`, `CMakePresets.json` | Build configuration and project options. |
| `Dockerfile`, `docker-compose.yml`, `entrypoint.sh`, `systemd.example` | Container and service deployment support. |

## 7. Build organization

The root [CMakeLists.txt](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/CMakeLists.txt) sets C99 and C++20, creates shared libraries/object targets, and then defines the four server executables. The principal libraries are built before the process targets; the master target is added last so it can depend on the other server binaries. Tests are included when `ENABLE_TESTING` is enabled.

The helper [build.sh](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/build.sh) configures a Release build under `build/` and invokes CMake's build command. The project README specifies CMake 3.25 through 3.31 for its documented setup. The root CMake configuration also explicitly rejects a source path containing spaces, which is an important checkout/build constraint.

Build configuration prepares runtime assets such as configuration files, migrations, vanity files, and navigation meshes in or beside the binary output. Server processes locate their executable/runtime directory and expect these resources to be present. Keep the executable directory and generated runtime data together when packaging or running a server.

## 8. Suggested code-reading paths

For a focused investigation, these paths give a useful orientation:

1. **Build and runtime assumptions:** [README.md](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/README.md), [CMakeLists.txt](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/CMakeLists.txt), [resources/](https://github.com/DarkflameUniverse/DarkflameServer/tree/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/resources/).
2. **Process topology:** [MasterServer.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dMasterServer/MasterServer.cpp), [Start.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dMasterServer/Start.cpp), [InstanceManager.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dMasterServer/InstanceManager.cpp).
3. **Transport and protocol:** [dServer.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dNet/dServer.cpp), then the relevant packet definitions and the service's packet handler.
4. **Gameplay state:** [Entity.h](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/Entity.h), [EntityManager.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/EntityManager.cpp), and the component/message responsible for the feature.
5. **Map behavior:** [Zone.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dZoneManager/Zone.cpp), [dZoneManager.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dZoneManager/dZoneManager.cpp), then the associated native script under `dScripts/`.
6. **Persistence:** [Database.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dDatabase/GameDatabase/Database.cpp), the relevant `ITables` interface, its SQLite/MySQL implementation, and `MigrationRunner.cpp`.

## 9. Operational boundaries

- The project README recommends small-scale/private use and does not recommend hosting a public server. Do not treat this architecture overview as a production hardening or large-scale deployment guide.
- Client files are separate from this source repository and are not supplied by the project.
- The project is licensed under AGPL-3.0; consult [LICENSE](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/LICENSE) and the README for obligations when modifying or distributing a server.
- Keep database state, client-derived data, and runtime resources backed up separately. A `CDServer.sqlite` static-data file and the game database serve different purposes and have different migration lifecycles.

## 10. Detailed runtime lifecycle

The services are separate processes, but the master coordinates their startup and hand-offs. The following sequence is based on [MasterServer.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dMasterServer/MasterServer.cpp), [WorldServer.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dWorldServer/WorldServer.cpp), [Start.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dMasterServer/Start.cpp), and [InstanceManager.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dMasterServer/InstanceManager.cpp).

### Master bootstrap and world readiness

1. `MasterServer` loads its configuration, connects to the game database, prepares the resource/client-data state, runs migrations, and loads the client-data tables it needs for zone caps.
2. The master creates its network endpoint and an in-memory `InstanceManager`. With `prestart_servers` enabled, it starts `ChatServer`, requests zone `0` and the default public zone `1000`, then starts `AuthServer`.
3. Each world process receives its map, port, instance, maximum-client count, and clone as command-line arguments. It opens the prepared `CDServer.sqlite`, connects to the game database, initializes its user and network services, and connects to both the master and chat.
4. For a normal map, `WorldServer` loads physics, zone/scene data, the zone-control entity, and the scene graph before it can announce readiness. Zone `0` is a login/character-selection world: it does not initialize a normal map zone.
5. Once its initialization has completed and its master connection is active, the world sends `WORLD_READY`. The master marks its `Instance` record ready and releases requests that were waiting for startup.

The master keeps process records and transfer state in memory; these are not a durable registry. A recorded instance is not considered an available transfer target until its ready state has been set.

### Login and session ownership

Authentication and world admission are separate steps:

1. `AuthServer` handles the client's handshake and login request. It looks up account state in the game database and checks the configured account restrictions and password.
2. On successful credentials, the auth service requests a transfer to zone `0`. The response to the client includes the selected world endpoint and a hash of a generated session key; the auth service also sends the raw key and username to the master.
3. The master stores the active session key by username. When a client reaches a world and presents its username and hash, the world requests that username's key from the master and checks the hash before creating a `User`.
4. Zone `0` then sends the character list. After a successful world admission, the world notifies the master with `PLAYER_ADDED`, which updates that instance's population count.

The relevant code is in [AuthPackets.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dNet/AuthPackets.cpp), the master session handlers in [MasterServer.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dMasterServer/MasterServer.cpp), and the world session handlers in [WorldServer.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dWorldServer/WorldServer.cpp). The master replaces an existing active key for the same username and alerts connected worlds about the new session.

### Zone-transfer path

The normal zone-transfer path crosses all three layers: the requesting world, the master, and the destination world.

1. The source world's `ZoneInstanceManager` assigns a request ID, stores the callback, and sends the requested map and clone to the master.
2. The master selects a non-private, non-shutting-down instance with matching map and clone and available capacity. Normal selection uses the soft population cap; friend-transfer selection can use the hard cap. The ordinary `REQUEST_ZONE_TRANSFER` handler currently passes `false` for the friend-transfer argument.
3. If no suitable instance exists, the master assigns an instance ID and port and starts a world process. The instance record remains pending until that process reports `WORLD_READY`.
4. A request received while the destination is starting is queued and receives its endpoint when the destination becomes ready. For an already-ready destination, the master first sends `AFFIRM_TRANSFER_REQUEST`; the destination acknowledges it, after which the master returns the endpoint to the requesting service.
5. The source service matches the response by request ID and invokes its callback, which completes the client-facing hand-off.

The affirmation is a destination-process handshake; capacity was selected earlier by the master. Private zones use a separate create/join path, where the master finds the private instance by its password rather than using normal public-instance selection. See [ZoneInstanceManager.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dNet/ZoneInstanceManager.cpp), [MasterPackets.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dNet/MasterPackets.cpp), and [InstanceManager.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dMasterServer/InstanceManager.cpp).

For world processes, the chosen port is also used to derive the local master-peer and chat-peer ports: the master connection listens on the world port plus one, and the chat connection uses the world port plus two. This is why the instance manager advances its port allocation in steps of three.

### World tick and state updates

The main loop in [WorldServer.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dWorldServer/WorldServer.cpp) owns the normal zone's simulation and packet dispatch. Its main phases are:

1. Calculate elapsed time and update entities.
2. Step physics, refresh spatial ghosting (at roughly one-second intervals), and update zone spawners.
3. Drain master-control packets and chat packets, then process world/client packets with a per-frame packet-count and elapsed-time budget.
4. Update RakNet replica state, perform periodic work, and sleep until the next frame.

Within the entity phase, [EntityManager.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/EntityManager.cpp) updates entities, serializes pending state, then processes kills and deletions. Zone loading and spawner updates are owned by [dZoneManager.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dZoneManager/dZoneManager.cpp) and [Zone.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dZoneManager/Zone.cpp). Zone `0` skips normal entity/physics/spawner simulation; its principal role is the login and character-list path.

World instances periodically save active characters and property data. On graceful shutdown they save active characters and properties again, disconnect replica participants, and send a shutdown response to the master. An empty non-zero-zone instance also shuts down after its configured empty interval (30 minutes for clone `0`, 5 minutes for other clones in this snapshot).

## 11. Runtime ownership and failure boundaries

| State or responsibility | Primary owner | Notes |
|---|---|---|
| Account credentials and persistent game records | Game database, accessed by auth/world services | Backend selection is shared configuration; SQLite and MariaDB/MySQL implement the same table interfaces. |
| Active session keys and instance/transfer registry | `MasterServer` process memory | Rebuilt during process startup; the game database separately stores master connection information. |
| Live users, entities, components, and loaded zone | A `WorldServer` process | Gameplay handlers and simulation run in the world process that owns the zone instance. |
| Static zone/object/component/mission definitions | `CDServer.sqlite` | Loaded through the client-data database wrappers; distinct from player persistence. |
| Chat service state and filtering | `ChatServer` plus shared chat-filter code | World processes connect separately to chat rather than routing chat through their game-world listener. |

`dServer` wraps RakNet peers for a service's listener and its master connection; the world process additionally creates its chat peer. For world processes, the master-connection peer binds locally to the world port plus one, and the chat peer binds to the world port plus two. This keeps control messages, client/game traffic, and chat on separate connections even though the world loop services them in one process. World state is not shared memory with the master: the master learns about readiness, player counts, and transfers through explicit messages.

The master removes a world record when its master connection is lost. Auth and chat processes are explicitly restarted by the master after disconnection; a lost world is instead recreated when a later request needs that map/clone. Graceful world shutdown has a save-and-disconnect path, while an abrupt process loss cannot run that path.

For code changes, trace both sides of a service message: packet definition/serialization in `dNet/`, dispatch in the receiving process, and the state owner that applies the result. A packet handler alone may not show the full lifecycle.
