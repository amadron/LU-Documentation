# Pet Database — Methodology and Evidence

[Pet database](./README.md) | [Mapped locations](./locations/README.md)

Generated: **2026-11-17T10:10:56.826Z**. Reviewed DarkflameServer revision: `8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4`. The database uses the supplied static CDClient CSV exports and local map assets; it is not a query of a running world or a player’s runtime database.

## Scope and inclusion rules

The authoritative local pet marker is `eReplicaComponentType::PET`, derived from [eReplicaComponentType.h](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dCommon/dEnums/eReplicaComponentType.h) rather than guessed. This produces **38 registry rows on 38 unique LOTs**. A PET component alone is not proof of a tamable pet.

A template is called a **confirmed tamable pet** only when all five evidence markers agree: it has a PET component registration, a `TamingBuildPuzzles.NPCLot` row, a `PET_INVENTORY_ITEM` ItemComponent registration, an Objects description exactly identifying it as `Tamable Pet`, and a recorded species-name crosswalk to the fixed public roster. The crosswalk is explicitly checked against local object names (with the Mantis/Praying Mantis variant recorded). This yields 26 templates. All remaining PET-component and puzzle-only LOTs are still included with a cautious classification; absence of the markers is not proof the content never existed.

- **Tamable pet templates:** 26
- **Other PET templates:** 9
- **Other PET / puzzle templates:** 4

The extra records include pet component entries marked “Don't use”, a named non-tamable companion, test entries, a PET entry without an Objects row, and a taming-puzzle-only LOT. The LOT 3336 [technical pet-system template](./3336.md) has a PET_CREATOR component and PetNestComponent row and is deliberately excluded from animal counts. Mount item types are not classified as pets merely because they follow a player. Enemy/NPC definitions without the pet-specific evidence intersection are not swept into this catalog.

There are 35 PetComponent definition rows; 31 component IDs are referenced by PET registrations and 4 rows have no LOT mapping. Their raw values are retained as [individual technical rows](./components/README.md), without assigning a species. The adjacent PET_CONTROL and PET_TAMING_CONTROL component types have 0 and 0 registrations respectively; PET_CREATOR has 1.

## Taming rules and code behavior

- [PetComponent.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dComponents/PetComponent.cpp) checks that the pet is untamed, honors the scene `CheckPrecondition` value when supplied, finds a puzzle row by the pet LOT, and checks imagination before beginning the minigame.
- The puzzle row provides `ValidPiecesLXF`, `Timelimit`, `NumValidPieces`, and `imagCostPerBuild` to the reviewed loader. The imagination field is used as the threshold before start and is charged in the build-attempt handler. Thus page values are described as the local server’s per-build attempt cost, not a measured per-capture charge.
- The same loader does not read the client-table `PuzzleModelLot`, `Difficulty`, `TotalNumPieces`, `ModelName`, `FullModelLXF`, or `Duration` fields; its in-memory model LOT is set to the NPC LOT. Pages preserve the client fields as client data and do not claim they control the live server presentation.
- In [CDPetComponentTable.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dDatabase/CDClientDatabase/CDClientTables/CDPetComponentTable.cpp), this revision loads sprint speed and imagination-drain interval. The client chance/tamability, element, idle-time, pet-form, audio, and buff fields are marked unused by the loader. The `percentTameChance` column is therefore not presented as an odds estimate.
- On success, the server records the pet and adds an inventory model entry with the pet LOT. Owner-following, switch interactions, and treasure digging are implemented in code. The current server code gates treasure digging on completion of mission definition 842 and has a Skeleton Dragon-specific bone treasure branch.
- `PetAbilities` is a small global table, not a reliable species-to-ability join. The enum contains a dig ability but the component documents abilities as currently unused. No species ability is inferred from names, audio sets, or item metadata.

## Local database relationships

| Evidence table / component | Use |
|---|---|
| [Objects](../../db/Objects.md) | Template name, type, raw client description, gate version, and raw locStatus. |
| [ComponentsRegistry](../../db/ComponentsRegistry.md) | LOT-to-component registration; enum values are resolved from the checked-in header. |
| [PetComponent](../../db/PetComponent.md) | Pet movement/drain settings and currently unused legacy fields. |
| [TamingBuildPuzzles](../../db/TamingBuildPuzzles.md) | NPC LOT to puzzle file, time, valid pieces, and imagination cost. |
| [ItemComponent](../../db/ItemComponent.md) | PET_INVENTORY_ITEM, EGG, and PET_FOOD types; item pages are linked rather than copied. |
| [ItemEggData](../../db/ItemEggData.md) | 3 egg-data rows, kept separate from functional pet/template claims. |
| [PetAbilities](../../db/PetAbilities.md) | Small global ability lookup, not a pet-specific assignment. |
| [PetNestComponent](../../db/PetNestComponent.md) | Auxiliary pet-system component; LOT 3336 is shown separately. |
| [MissionTasks](../../db/MissionTasks.md) and [Missions](../../db/Missions.md) | Tasks whose enum is PET_TAMING and direct mission reward associations. |
| [ZoneTable](../../db/ZoneTable.md), parsed LUZ/LVL assets | Exact asset-path joins, static pet placements and spawner waypoints. |

Quest and achievement associations link to existing [individual quest pages](../quests/README.md); pet pages preserve the raw task target/group and definition metadata. A direct reward field is not the same thing as taming or unlocking a pet.

## English client strings

The pages were first generated without the client locale. They have since been enriched by `scripts/enrich_pets_racing.py` in the documentation repository, which reads the English (en_US) strings of the client's `locale.xml` together with `CDServer.sqlite`:

- Species names and page titles come from `Objects_<lot>_name` without the trailing “Pet” (so LOT 5642 is the **Mantis**, as the client calls it, not “Praying Mantis”). Every LOT page shows the client name and description next to the Objects table values, or says that no client string exists.
- Quest and achievement names come from `Missions_<id>_name`; the task tables add the client task text (`MissionTasks_<uid>_description`, falling back to the mission description).
- Tasks whose target group lists several pets are marked as shared. Achievements 521 “Speed Tamer 1” and 522 “Speed Tamer” name 19 pet templates (one target plus 18 in the group), so they appear on every listed pet's page but are general speed-taming achievements, not pet-specific ones.
- locale.xml describes exactly 26 objects as “Tamable Pet”, which matches the 26 confirmed templates, so no tamable pet is missing. LOT 5638 (a puzzle row only) and LOT 16479 (PET component and a puzzle that copies the Bunny's carrot puzzle) have no Objects row, no client name, no map placement and no mission of their own; their pages explain this.

## Map locations and conditions

The source parser follows the exact normalized `ZoneTable.zoneName` path to a local LUZ file and its referenced LVL files. Embedded world IDs are not used to invent a zone join. It retains direct placements, LOT 176 `spawntemplate` placements, and LUZ spawner waypoints. Every listed coordinate is a static candidate, not an assertion that the object is actively spawned, reachable, or present on a particular deployment. Inactive-on-load spawners, feature gates, mission IDs, and scene preconditions are preserved. Client-only placements and non-finite positions are excluded; their counts/errors appear in [Coverage.json](./Coverage.json). `ZoneTable.petsAllowed` is reproduced only as source metadata and is not interpreted as a taming rule.

The map scan found 39 LUZ files; 34 matched an exact ZoneTable path and 536 referenced LVL files parsed with 0 failures. The 5 unmatched LUZ assets and any pet templates without matched positions are not assigned invented zones or coordinates; see [Coverage.json](./Coverage.json).

## Public community evidence

A read-only request to the standard MediaWiki API retrieved fixed page revisions at **2026-11-17T10:00:00.220Z**. No local database, source code, or map files were sent to the API. Article prose is summarized rather than copied.

| Page | Revision | Revision timestamp | Use |
| --- | --- | --- | --- |
| [Pets](https://legouniverse.fandom.com/wiki/Pets?oldid=160061) | 160061 | 2018-04-03T23:13:01Z | Historical species roster, discovery locations, stated imagination costs, item/mission/achievement requirements, and faction pets. |
| [Pet Cove](https://legouniverse.fandom.com/wiki/Pet_Cove?oldid=163381) | 163381 | 2022-04-16T07:42:02Z | Historical introduction to pet taming in Pet Cove and Coalessa’s teaching role. |


The historical [Pets](https://legouniverse.fandom.com/wiki/Pets?oldid=160061) roster is the source for species names, broad locations, stated imagination costs, some required items, and later mission/achievement/faction conditions. Its own LOT identifiers are absent. The build performs an explicit local name crosswalk and keeps the community source separate from local object/template evidence. The [Pet Cove](https://legouniverse.fandom.com/wiki/Pet_Cove?oldid=163381) article is used only for the historical introduction to taming and Coalessa’s teaching role. Locations from the article are not promoted to local coordinate evidence.

The public article’s reported imagination cost and the CDClient `imagCostPerBuild` are separate evidence columns. Two mismatches are retained rather than resolved by guess: the historical article reports 8 for Buffalo and 10 for Earth Dragon, while the local puzzle rows say 10 and 8 respectively. Species pages expose both values with their source labels. Public acquisition requirements are historical, not a guarantee of current live availability.

## Exclusions and uncertainty

- Creature, enemy, and mount templates that only resemble pet names are excluded unless the pet-specific components/puzzle/items support their inclusion. A registered PET LOT may still be a test object, visual variant, pre-tame entity, technical record, or unresolved template; those are not silently promoted to tamable pets.
- Pet eggs and pet food are listed as related item definitions, not assumed functional summoning or taming requirements. Several local descriptions explicitly mark entries as test/unused.
- Empty names, absent Objects rows, unused component fields, absent puzzle rows, missing map placements, unknown costs, and unspecified faction pet locations remain blank/unknown. No acquisition path, live rate, species name, or unlock requirement is fabricated.
- Fixed map placements do not prove reachability or active spawning; a missing placement does not prove a pet was unavailable.
- Public historical facts may not apply to a modern private server. Check that server’s content gates and configuration in game.

## Output and validation

This folder contains 39 LOT pages, one technical pet-system template page, 4 unreferenced PetComponent definition pages, a zone-location index with coordinates, and [Coverage.json](./Coverage.json). All registered PET-component lots and all puzzle-only LOTs are page-covered. Generated page content is limited to this pet folder; the existing shared wiki navigation and item/quest/racing catalogs are untouched.
