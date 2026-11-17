# LEGO Universe Data Model and Public Research

## Scope and evidence

This guide combines the local DarkflameServer checkout at revision
`8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4` with publicly accessible format
specifications and community tools. It describes structures and relationships,
not the actual contents of a particular client database.

The DarkflameServer source and migrations are the primary evidence for how DLU
uses the data. Community editors and format parsers are useful corroboration,
but are not official specifications. Some of those tools explicitly describe
themselves as works in progress or AI-assisted. Their inferred field names and
parameter meanings should be treated as provisional.

## The two databases are different

| Database | Purpose | Where its contents come from |
|---|---|---|
| `CDServer.sqlite` | Static client/game definitions used by the server: object templates, components, skills, behavior data, missions, zones, and other reference tables. | Converted from the client's `cdclient.fdb`, or copied from an existing database. It is not the player save database. |
| `dlu.sqlite` (default SQLite game database) | Server-owned accounts, characters, social state, properties, UGC, and other persistent or operational records. | Schema is established by DLU migrations; most player records are created and updated while the server runs. |

The files in `dDatabase/CDClientDatabase/CDClientTables/` are typed access
wrappers that query static tables; they are not a replacement for the database
rows themselves. See the [database and migration overview](./server/DarkflameServer%20Architecture%20and%20Repository%20Structure.md)
for startup and configuration details.

## Static game definitions

For player-oriented introductions rather than database internals, start with
the [Player Wiki](./wiki/README.md), including the quest and item guides.

### Object templates and components

The core object identity is the **LOT** (the object template ID). The static
`Objects` table maps LOTs to object metadata such as internal name and type.
`ComponentsRegistry` associates a LOT with component types and component-table
IDs. Component-specific tables then carry type-specific definitions. For
example, `ItemComponent` contains fields such as equipment location, base
value, rarity, item type, stack size, currency costs, and requirements.

Conceptually:

```text
LOT
 ├── Objects metadata
 └── ComponentsRegistry entries
      ├── ItemComponent → item definition
      ├── InventoryComponent → preset contents for applicable objects
      ├── DestructibleComponent → destructible-object definition
      ├── ScriptComponent → server script association
      └── other registered component types
```

This is a relational/template model rather than a single wide object record.
DLU resolves a LOT's component registrations and loads the corresponding
component data when it constructs an entity. Not every registered component is
necessarily network-replicated or instantiated in the same way.

**A definition is not a live item.** A LOT describes the item type. A player
item is a runtime instance with its own object ID, LOT, count, inventory type
and slot, equipped/bound state, subkey/parent data, and optional configuration
XML.

### Skills and behavior trees

Skills are data-driven graphs interpreted by server code:

```text
object LOT ── ObjectSkills ──> skill ID
                                  │
                                  v
                         SkillBehavior root
                                  │ behavior ID
                                  v
                         BehaviorTemplate row
                           template ID / effect
                                  │
                                  v
                       BehaviorParameter rows
                   parameter name → numeric value
```

- `ObjectSkills` associates skills with object templates and cast context.
- `SkillBehavior` provides the skill's root behavior and skill-level settings.
- `BehaviorTemplate` maps a behavior ID to a template ID and effect metadata.
- `BehaviorParameter` stores named numeric parameters for a behavior ID.
- A parameter value can itself refer to another behavior ID, forming child
  edges. Some references can instead be back-references, so a graph is more
  accurate than assuming every skill is a simple tree.

The server dispatches template IDs to C++ behavior implementations in
[`Behavior.cpp`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dBehaviors/Behavior.cpp). The tables
provide the per-skill/per-behavior data; the interpreter and concrete effects
are implemented in server code. A value in a behavior table alone therefore
does not fully define gameplay. The FDB can contain behavior types that this
server revision does not implement; unhandled template IDs fall back to an
empty behavior rather than gaining functionality just because their data is
present.

The community [skill-editor](https://github.com/LU-Rebuilt/skill-editor)
provides a useful supplementary model: its loader joins skills, behavior
templates, parameters, object-skill assignments, and object names. Its
[`behavior_schema.json`](https://github.com/LU-Rebuilt/skill-editor/blob/main/src/behavior_schema.json)
adds readable parameter names/types for known template IDs, including
repeatable behavior references. That schema is an editor aid and an inferred
description of semantics, not an authoritative game specification.

## Findings from the local client data

The expanded `res\res` folder contains a 42,140,012-byte `cdclient.fdb`. A
read-only structural parse found **137 tables and 418,262 rows**. This changes
the analysis from schema inference alone to a review of the actual static
dataset supplied to this server.

| Area | Tables and observed row counts | What the data represents |
|---|---|---|
| Objects and item definitions | `Objects` 12,985; `ComponentsRegistry` 42,521; `ItemComponent` 7,405; `InventoryComponent` 1,292; `ItemSets` 49; `ItemSetSkills` 322 | LOTs identify object templates. The registry links a LOT to component records; item definitions are only one component type. |
| Item economy and drops | `LootMatrix` 2,675; `LootMatrixIndex` 581; `LootTable` 6,519; `LootTableIndex` 756; `VendorComponent` 92; `CurrencyTable` 166; `CurrencyDenominations` 9; `RarityTable` 54; `RarityTableIndex` 26 | Item sources, vendor stock configuration, currencies, and rarity are separate linked data sets. |
| Skills and behaviors | `BehaviorTemplate` 41,126; `BehaviorParameter` 219,782; `BehaviorTemplateName` 65; `BehaviorEffect` 22,057; `SkillBehavior` 1,521; `ObjectSkills` 3,951; `BuffDefinitions` 68; `BuffParameters` 67 | Skills point to root behaviors; behavior records reference template types, effect data, and named numeric parameters. This is a data graph interpreted by server code. |
| NPCs and creatures | `MinifigComponent` 580; `BaseCombatAIComponent` 179; `MovementAIComponent` 98; `MissionNPCComponent` 917; `PetComponent` 35; `PetAbilities` 4; `DestructibleComponent` 1,437; `SmashableElements` 775; `Factions` 66; `NpcIcons` 154 | NPC/creature traits are component definitions attached to object templates, not a single NPC table. These counts are component rows, not unique NPC totals. |
| Missions and rewards | `Missions` 1,427; `MissionTasks` 1,804; `MissionText` 1,430; `MissionEmail` 272; `Rewards` 10; `RewardCodes` 78 | Mission objectives, NPC associations, text/presentation data, rewards, and email are stored separately. |
| Properties and building | `PropertyTemplate` 73; `PropertyEntranceComponent` 12; `Blueprints` 2; `ModuleComponent` 387; `ModularBuildComponent` 4; `BrickIDTable` 1,909; `BrickColors` 53 | Client-side property types/entrances and building/module definitions are distinct from a player's claimed property and placed objects. |
| Zones and scenes | `ZoneTable` 1,056; `SceneTable` 61; `ZoneSummary` 48; `ZoneLoadingTips` 35; `LUPZoneIDs` 5 | Zone configuration, scene names, summaries, and loading tips are separate. Do not assume one row or one asset file per playable zone. |
| Entity presentation and physics | `RenderComponent` 13,690; `PhysicsComponent` 6,749; `ScriptComponent` 1,484; `Animations` 7,615 | Object appearance, physics, script associations, and animation data are represented separately and joined through component/template IDs. |

These are **table-row counts, not counts of unique gameplay objects**: a LOT can
have several component rows, and association tables contain one row per
relationship. To build useful lists from this database:

- **Item catalog:** join `Objects` to `ComponentsRegistry` by LOT, filter the
  item component type, then join the registry's component ID to
  `ItemComponent.id`. Add `ItemSets` and loot/vendor tables for set membership
  and acquisition context.
- **NPC catalog:** include `Objects` rows typed `NPC`, `Enemies`, or
  `UserGeneratedNPCs`, and supplement them with other object types carrying
  NPC-relevant component registrations. Join those component IDs to
  `MinifigComponent`, `BaseCombatAIComponent`, `MovementAIComponent`,
  `MissionNPCComponent`, or `PetComponent`. No one table is a complete NPC
  list.
- **Skill/behavior catalog:** join `ObjectSkills` → `SkillBehavior` →
  `BehaviorTemplate`, then use `BehaviorParameter` and `BehaviorEffect` to
  follow each skill's behavior graph and effects.
- **Property catalog:** use `PropertyTemplate` and
  `PropertyEntranceComponent` for static property definitions; use the game
  database for actual player-owned properties and placements.
- **Zone catalog:** use `ZoneTable` for zone configuration and relate it to
  `SceneTable` and the corresponding `.luz`/`.lvl` resources.

For a row-counted, one-line overview of every table in the local FDB, see the
[CDClient Table Reference](./LEGO%20Universe%20CDClient%20Table%20Reference.md).
The complete rows are available as per-table CSV files in the
[CDClient database export](./db/README.md).

### Item list export

The GitLab-readable [LEGO Universe Item List](./LEGO%20Universe%20Item%20List.md)
shows every item in a Markdown table with LOT, name, readable item type, rarity
code, equipment location, stack size, base value, and loot/vendor flags. The
[CSV export](./LEGO%20Universe%20Item%20List.csv) is available for sorting and
filtering and includes additional component fields such as kit/unique/binding
flags, requirements, and currency costs. Both contain all **6,832**
`ComponentsRegistry` rows whose component type is `ITEM` (`11` in this server
revision), joined to `ItemComponent` and, where available, `Objects`. `LOT` is
the object/item number; `ItemComponentID` is a separate component-table key.
`Name` uses `displayName` when present and falls back to the internal `name`;
`NameSource` records which case applies.

Item type labels are derived from the server's `eItemType` enum. Rarity remains
the numeric value in the FDB; the data does not provide a verified human-readable
rarity name. The loot/vendor columns are boolean flags only, not the names of
specific loot sources or vendors.

The CSV keeps 357 registered item LOTs that lack an `Objects` row, leaving
their name fields blank rather than inventing names. It excludes 619
`ItemComponent` records that have no matching `ITEM` registry entry and hence
no LOT mapping in this dataset.

### NPC and creature list export

The GitLab-readable [LEGO Universe NPC and Creature Template List](./LEGO%20Universe%20NPC%20List.md)
contains **1,484 unique LOTs** from this client dataset. It includes 1,403
objects whose `Objects.type` is `NPC`, `Enemies`, or `UserGeneratedNPCs`, plus
48 objects of other types that have at least one of these registered component
markers: `MINIFIG`, `BASE_COMBAT_AI`, `MOVEMENT_AI`, `MISSION_OFFER`, `PET`,
`PET_CREATOR`, or `POSSESSABLE`. Those additional rows include vehicles,
rebuildables, and environmental objects; they are marked as NPC-like
component templates rather than asserted to be NPCs. It also retains 33
component-registration LOTs that have no matching `Objects` row as unresolved
entries with blank names and no inferred object type.

The [NPC CSV export](./LEGO%20Universe%20NPC%20List.csv) includes names and
their source, object type, classification markers, raw `npcTemplateID`,
component IDs, selected combat/movement/pet fields, and mission associations.
Mission associations are joined from the registered `MISSION_OFFER` component
ID to `MissionNPCComponent.id`; the Markdown table shows associated mission
IDs where present. Names fall back to `Objects.name` when `displayName` is
empty. The server wrapper marks `npcTemplateID` unused, so it is provided for
reference only.

This is a template catalog, not proof that every listed LOT is instantiated
in a particular zone or used as an NPC in gameplay. Component-row counts do
not equal unique entity counts, and the component-driven additions are
intentionally identified as candidates rather than definitive NPCs.

The server's table wrappers in
[`CDClientTables/`](https://github.com/DarkflameUniverse/DarkflameServer/tree/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dDatabase/CDClientDatabase/CDClientTables/)
show the concrete query/lookup patterns. For example,
[`CDComponentsRegistryTable`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dDatabase/CDClientDatabase/CDClientTables/CDComponentsRegistryTable.h)
and [`CDObjectsTable`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dDatabase/CDClientDatabase/CDClientTables/CDObjectsTable.h)
define the LOT/component relationship used by the server.

The expanded `res\res` folder also contains **661 `.lvl`**, **39 `.luz`**, and
**2,429 `.lxfml`** files. These are separate client resources, not rows in
`cdclient.fdb`. The `.luz`/`.lvl` format specifications linked above help
describe their binary structure.

This copy also contains empty tables such as `TextDescription`, `TextLanguage`,
and `ObjectBehaviorXREF`. Their presence in the schema therefore does not
prove that a feature is populated in this particular dataset.

### Static property definitions versus saved properties

The `CDClient` rows above define available property templates and entrances.
They do **not** represent the current owners or the objects players placed on
their properties. Those are server-owned records in the game database:

- `properties` stores owner, template, clone, name/description, rent, privacy,
  moderation state, and zone.
- `properties_contents` stores each placed LOT and its transform, plus optional
  UGC and behavior fields.
- `ugc` stores submitted build data (including LXFML); `ugc_modular_build`
  stores associated modular-build configuration.

The client-data `Blueprints` table has only two rows in this snapshot, so it
should not be mistaken for a full catalogue of player-created builds.

Likewise, `ItemComponent` defines item types; a player's live inventory is
stored as item instances in their character XML, not as the static item list.

The native DLU converter in
[`FdbToSqlite.cpp`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dCommon/FdbToSqlite.cpp) creates SQLite
tables from FDB column names and types and inserts the rows. It does not
reconstruct declared primary/foreign-key constraints from the FDB. Relationships
must be established from ID columns, observed data, and the server's query and
component-loading code. The loader also reads selected CDClient tables rather
than treating every table in the FDB as an active server subsystem.

## Player and character persistence

The initial DLU game schema separates account identity from character identity:

- `accounts` stores account credentials and server-side account state.
- `charinfo` stores a character ID, owning account, name/rename state, last
  login, and permissions.
- `charxml` stores an XML document keyed by character ID.
- Other tables store separate relationships and systems, including friends,
  ignores, mail, leaderboard entries, properties, property contents, UGC,
  activity logs, and player-specific behavior records.

The game database's `behaviors` table is separate from the static CDClient
`BehaviorTemplate` and `BehaviorParameter` tables. Similar names do not mean
they store the same kind of data.

Character XML is an important persistence boundary, but not the only one.
Character and entity components update that document before it is written to
`charxml`. For example, the inventory serializer stores inventory groups and
item instances with attributes for LOT, object ID, slot, count, binding,
equipped state, subkey, parent, and optional configuration data. Database
tables hold some other state separately; properties and UGC, for instance,
have their own relational records.

This explains why the game database schema does not list every item in every
character as a separate normalized `items` table: the player inventory is
serialized inside the character XML document in this implementation.

## World and asset formats

Public Kaitai Struct definitions in
[`lcdr/lu_formats`](https://github.com/lcdr/lu_formats/tree/master/files)
document several binary formats used by LEGO Universe:

- [`fdb.ksy`](https://github.com/lcdr/lu_formats/blob/master/files/fdb.ksy)
  describes the flat database container: table descriptors, column names and
  types, hash buckets, rows, and typed values.
- [`luz.ksy`](https://github.com/lcdr/lu_formats/blob/master/files/luz.ksy)
  describes zone-level data, including scene references, boundaries, zone
  transitions, and path data.
- [`lvl.ksy`](https://github.com/lcdr/lu_formats/blob/master/files/lvl.ksy)
  describes chunked level/scene data, including environment, object, and
  particle chunks.
- [`pk.ksy`](https://github.com/lcdr/lu_formats/blob/master/files/pk.ksy)
  describes the archive table of contents and packed-file entries.

The repository also contains definitions for other formats such as audio,
animation, geometry, raw, and compressed data. These specifications help
explain how the client assets are organized, but they do not supply the assets
or all of their game-specific semantics.

## Public tools and what they provide

| Resource | What it is useful for | Important limitation |
|---|---|---|
| [`LU-Rebuilt/fdb-tools`](https://github.com/LU-Rebuilt/fdb-tools) | Converts a user-provided FDB to SQLite and browses FDB/SQLite tables. Its README says the output is intended to be compatible with DLU's CDServer format. | A converter/viewer, not a database-content download. It requires an input FDB. |
| [`LU-Rebuilt/skill-editor`](https://github.com/LU-Rebuilt/skill-editor) | Inspects skill roots and behavior references in a CDClient database. | Parameter names/types and graph interpretation partly rely on an editor-maintained schema. |
| [`LU-Rebuilt/cdclient-manager`](https://github.com/LU-Rebuilt/cdclient-manager) | Work-in-progress table/schema, loot/vendor, and skill editing. | Its README labels the project work in progress; treat edits and inferred schema as experimental. |
| [`lcdr/lu_formats`](https://github.com/lcdr/lu_formats) | Machine-readable structural definitions for client data and asset formats. | A binary layout is not the same thing as a complete semantic game-data reference. |

The DarkflameServer schema and source are also public: see the
[initial SQLite game migration](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/migrations/dlu/sqlite/0_initial.sql),
[object table wrapper](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dDatabase/CDClientDatabase/CDClientTables/CDObjectsTable.h),
[component registry wrapper](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dDatabase/CDClientDatabase/CDClientTables/CDComponentsRegistryTable.h),
[item component wrapper](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dDatabase/CDClientDatabase/CDClientTables/CDItemComponentTable.h),
[character persistence](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/Character.cpp), and
[inventory persistence](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dComponents/InventoryComponent.cpp).

## Is a complete database publicly available?

In the sources checked for this guide, I found public parsers, schema wrappers,
format definitions, and editors, but no verified official download of a
complete `CDClient` data database. Tool availability should not be confused
with the availability or redistribution rights of the original client data.
Without a legitimate copy of the relevant client data, the server code can
show expected table structure and usage, but not the complete static row set
(for example, all item definitions, behavior parameters, missions, or zone
records).

## Confidence and limits

- **High confidence:** the separation between the static CDClient database and
  the DLU game database; the account/character table split; the use of
  character XML for inventory persistence; the LOT/component lookup approach;
  and the server's behavior-template dispatch. These are visible in DLU
  migrations and source.
- **Good structural evidence:** the FDB, LUZ, LVL, and PK layouts documented in
  the public Kaitai files. These are community-maintained reverse-engineered
  format definitions, not an official vendor specification.
- **Provisional semantics:** exact meanings for poorly named fields, every
  behavior parameter, unused/unknown columns, and the complete dependency graph
  among all static tables. Verify these against server/client code and a
  legitimate database before treating them as definitive.

For the runtime architecture and protocol path, continue with
[DarkflameServer Architecture and Repository Structure](./server/DarkflameServer%20Architecture%20and%20Repository%20Structure.md)
and [DarkflameServer Client-Server Protocol and Gameplay](./server/DarkflameServer%20Client-Server%20Protocol%20and%20Gameplay.md).
