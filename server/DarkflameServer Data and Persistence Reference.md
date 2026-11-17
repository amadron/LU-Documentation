# DarkflameServer Data and Persistence Reference

## Scope and source snapshot

This guide describes the main data stores and persistence paths in the local [DarkflameServer checkout](https://github.com/DarkflameUniverse/DarkflameServer/tree/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/) at revision `8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4`. It focuses on server-owned state and the static client-data database. It is not a full schema dictionary; see the [database reference](../db/README.md) for documented exported tables and the [Data Model and Public Research](../LEGO%20Universe%20Data%20Model%20and%20Public%20Research.md) for broader data context.

## 1. Separate data stores

DarkflameServer uses several data sources with different owners and lifecycles. The two SQLite files below are not interchangeable.

| Store | Contents | Access and lifecycle |
|---|---|---|
| Game database | Accounts, characters, social records, mail, property state, UGC, activity/command data, and other server-owned state. | Selected by `database_type`; accessed through `Database` and the `GameDatabase` table interfaces. |
| `resServer/CDServer.sqlite` | Static client-derived content: object/component definitions, skills, missions, zones, and other reference data used by server logic. | SQLite-only `CDClientDatabase`; prepared and migrated separately, then queried through typed CDClient table wrappers. |
| Client/resource archive | Zone, scene, level, terrain, names, chat-filter, and other runtime assets. | Read through `AssetManager`; it is not the game database and is not included in the server source repository. |

The master prepares the server-side CDClient database before zone processes use it. It can reuse an existing server/client SQLite database or convert the client's `cdclient.fdb` when needed. World processes open the prepared `resServer/CDServer.sqlite`; the active game database remains a separate service/backend.

## 2. Game database abstraction

[`Database`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dDatabase/GameDatabase/Database.cpp) owns the process-level database instance and selects the implementation from `database_type`:

- `sqlite` selects `SQLiteDatabase`;
- `mysql`, `mariadb`, and `maria` select the MySQL/MariaDB implementation; and
- an unknown or missing value falls back to the MySQL migration/backend path with a log message.

The backend implements [`GameDatabase`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dDatabase/GameDatabase/GameDatabase.h), which combines interfaces for separate domains such as accounts, character XML/info, play keys, mail, friends/ignores, properties, UGC, logs, migration history, and leaderboards. Callers use these interfaces rather than issuing backend-specific SQL for every feature.

For SQLite, the database path is resolved from the binary directory and configured `sqlite_database_path`; the connection enables WAL mode. The shared configuration also contains MariaDB/MySQL connection settings. The selected backend and its migration directory must agree with the database being maintained.

This abstraction centralizes SQL access but does not make every feature one atomic transaction. A feature may update component memory, character XML, and one or more table interfaces through different calls. Follow the feature's full save path before assuming its durability or transaction boundaries.

## 3. Static CDClient data

[`CDClientDatabase`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dDatabase/CDClientDatabase/CDClientDatabase.cpp) opens the SQLite file and provides query/prepared-statement operations. [`CDClientManager`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dDatabase/CDClientDatabase/CDClientManager.cpp) loads typed wrappers for tables used by gameplay, including object templates, component registrations, skills, missions, zone settings, loot, scripts, vendors, and progression data.

The static database participates directly in server behavior:

- `Entity::Initialize` combines a LOT/template with component registrations to decide which native components to attach.
- `dZoneManager` queries zone configuration such as caps, spawn/ghosting settings, and feature policy.
- Gameplay components query tables for parameters such as skill behavior, loot, rebuild, vendor, or mission definitions.
- Script names and component IDs connect static records to C++ implementations.

Some CDClient tables are cached while others are queried as needed; the default build does not enable the optional cache-all mode. A source change that assumes data presence should account for missing rows and the exact database snapshot.

## 4. Migration lifecycle

[`MigrationRunner.cpp`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dDatabase/MigrationRunner.cpp) handles two migration streams:

1. **Game database migrations** are selected under `migrations/dlu/sqlite` or `migrations/dlu/mysql`, based on the configured backend. Applied migration names are recorded in the game database's migration-history table. Some migration names trigger C++ transformations instead of plain SQL execution.
2. **CDServer migrations** are loaded from `migrations/cdserver` and applied to the static SQLite database, with a migration-history table in that database. The runner also checks the game database's history to reconcile older migration tracking.

The game database and CDServer therefore have separate schemas, histories, and update paths. Back them up independently before migration or manual data maintenance. A CDServer migration is not a substitute for a game database migration, and vice versa.

## 5. Character load and save path

Character persistence is split between character metadata and character XML. [`Character::UpdateInfoFromDatabase`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/Character.cpp) loads character info and the XML record through the game database interfaces. The XML is parsed into in-memory character state, and the world creates an entity for the character with components that load their relevant values from that XML.

On save, `Character::SaveXMLToDatabase`:

1. requires the character's runtime entity to still be available;
2. updates character attributes such as GM level and coins;
3. updates eligible saved location/world values, emotes, flags, respawn checkpoints, and component-owned XML through `Entity::UpdateXMLDoc`;
4. serializes the XML document; and
5. calls the `ICharXml` interface to update the stored record.

World processes save active characters periodically and again during graceful shutdown. Character destruction also saves its XML as part of the entity/user lifecycle. Property management has a separate save path, invoked periodically and at shutdown when that system is active. Mail, friends, leaderboards, UGC, and other domains use their own game-database interfaces rather than being assumed to live in character XML.

Saved location fields are conditional: the inspected implementation writes the normal last-zone/location values only for non-zero maps, clone `0`, and zones where saving the location is enabled. Instance/clone travel and zone-level policy can therefore affect the location written to character data.

## 6. Persistence boundaries and debugging

When data appears missing or stale, identify which store owns it before inspecting SQL:

| Symptom | First code path to inspect |
|---|---|
| Cannot log in / account state is wrong | Auth login path and account/play-key interfaces in `dNet/AuthPackets.cpp` and `dDatabase/GameDatabase/ITables/`. |
| Character loads with old inventory, flags, or position | Character XML loading, the relevant component's `LoadFromXml`/`UpdateXml`, and the world save/disconnect path. |
| Zone, object, or skill behavior differs from expectation | `CDServer.sqlite`, its typed table wrapper, and the entity/component/script code consuming it. |
| SQLite game database or CDServer schema is out of date | The matching migration history, backend selection, and correct migration folder. |
| Property data fails to persist | `PropertyManagementComponent::Save` and its `IProperty`/`IPropertyContents` backend interfaces. |

Useful entry points include [`GameDatabase.h`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dDatabase/GameDatabase/GameDatabase.h), [`SQLiteDatabase.cpp`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dDatabase/GameDatabase/SQLite/SQLiteDatabase.cpp), [`CDClientManager.cpp`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dDatabase/CDClientDatabase/CDClientManager.cpp), [`MigrationRunner.cpp`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dDatabase/MigrationRunner.cpp), [`Character.cpp`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/Character.cpp), and [`UserManager.cpp`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/UserManager.cpp).

## 7. Operational notes

- Keep backups of the game database and `resServer/CDServer.sqlite` separate; they have different contents and migration histories.
- Treat character XML as one persistence representation, not the sole source of all player state.
- Do not infer the effective world behavior from code alone: the CDClient revision and resource archive must match the server assumptions.
- Verify the selected backend before applying a migration or inspecting the SQLite file; a server configured for MariaDB/MySQL will not be using the SQLite game database path.
