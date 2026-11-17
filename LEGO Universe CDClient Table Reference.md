# LEGO Universe CDClient Table Reference

This reference covers all **137 tables** found in the local
`res\res\cdclient.fdb` snapshot. Row counts describe that file only; they can
change between client-data versions. Counts are table rows, not counts of
unique objects, players, or gameplay entities.

Descriptions are concise interpretations of table names, column names, and
the way DarkflameServer accesses the data. A listed table is not necessarily
loaded or actively used by this server revision. Tables with zero rows are
present in the schema but contain no records in this snapshot.

## Object templates and components

| Table | Rows | Overview |
|---|---:|---|
| `Objects` | 12,985 | Object templates keyed by LOT, including names, type, placement/localization flags, and related metadata. |
| `ComponentsRegistry` | 42,521 | Maps a LOT and component type to the component-specific record ID used to construct an entity. |
| `AccessoryDefaultLoc` | 170 | Default positions and rotations for attaching accessories, grouped by attachment group. |
| `BaseCombatAIComponent` | 179 | Combat-AI settings such as behavior type, role, aggro/tether ranges, speeds, and timing. |
| `ChoiceBuildComponent` | 5 | Choice-build component definitions, including selections and imagination overrides. |
| `CollectibleComponent` | 79 | Collectible-object records and their mission requirement references. |
| `DestructibleComponent` | 1,437 | Destructible-object settings such as faction, health, loot/currency references, level, armor, and smashability. |
| `ExhibitComponent` | 11 | Exhibit dimensions, offsets, and reputation-size settings. |
| `Factions` | 66 | Faction relationships, including friendly and enemy lists. |
| `InventoryComponent` | 1,292 | Preset inventory entries for applicable object templates, including item LOT, count, and equip state. |
| `JetPackPadComponent` | 4 | Jetpack-pad distance and blocker/warning-volume settings. |
| `MinifigComponent` | 580 | Minifigure appearance-part IDs such as head, torso, legs, hair, and face details. |
| `MinifigDecals_Eyebrows` | 52 | Eyebrow decal asset paths and character-creation/gender validity flags. |
| `MinifigDecals_Eyes` | 51 | Eye decal asset paths and character-creation/gender validity flags. |
| `MinifigDecals_Legs` | 136 | Leg decal IDs and high-resolution asset paths. |
| `MinifigDecals_Mouths` | 61 | Mouth decal asset paths and character-creation/gender validity flags. |
| `MinifigDecals_Torsos` | 480 | Torso decal asset paths and character-creation/gender validity flags. |
| `MovementAIComponent` | 98 | Movement-AI type, wandering parameters, speed, radius, and optional attached path. |
| `NpcIcons` | 154 | NPC icon appearance, placement, scaling, rotation, and composite-icon settings. |
| `PackageComponent` | 159 | Package definitions that reference loot matrices and package types. |
| `PetAbilities` | 4 | Pet ability names, imagination costs, and localization status. |
| `PetComponent` | 35 | Pet taming, movement, form, elemental type, drain, audio, and buff settings. |
| `PetNestComponent` | 1 | Elemental type associated with a pet nest. |
| `PhysicsComponent` | 6,749 | Physics asset and movement/collision parameters for object templates. |
| `PossessableComponent` | 11 | Possession/mount control scheme, attachment animations/offsets, and related settings. |
| `ProximityMonitorComponent` | 40 | Per-object proximity-monitor configuration and client/server loading flags. |
| `ProximityTypes` | 8 | Named proximity types with radius, collision group, passive checks, and loading options. |
| `RebuildComponent` | 227 | Rebuildable-object timings, imagination costs, interruption, module, and activity settings. |
| `RebuildSections` | 99 | Rebuild-section object IDs, offsets, fall animation/height, required pieces, and placement state. |
| `ScriptComponent` | 1,484 | Server- and client-side script names associated with component records. |

## Skills, behaviors, combat, and progression

| Table | Rows | Overview |
|---|---:|---|
| `AICombatRoles` | 117 | Combat-role preferences and role-specific distance ranges. |
| `BehaviorEffect` | 22,057 | Visual, audio, camera, render, motion, and mesh effect definitions referenced by behaviors. |
| `BehaviorParameter` | 219,782 | Named/numbered parameter values keyed by behavior ID. |
| `BehaviorTemplate` | 41,126 | Behavior ID to template/effect mapping used by the behavior interpreter. |
| `BehaviorTemplateName` | 65 | Human-readable names for behavior template IDs. |
| `BuffDefinitions` | 68 | Buff IDs and their priority/UI icon metadata. |
| `BuffParameters` | 67 | Numeric, string, and effect parameters associated with buffs. |
| `LevelProgressionLookup` | 85 | Progression thresholds and associated behavior effects. |
| `ModelBehavior` | 6 | Model behavior records pointing to behavior-definition XML files. |
| `ObjectBehaviors` | 3 | Behavior XML data keyed by behavior ID. |
| `ObjectBehaviorXREF` | 0 | Intended LOT-to-behavior cross-reference table; empty in this snapshot. |
| `DevModelBehaviors` | 0 | Development model-to-behavior associations; empty in this snapshot. |
| `ObjectSkills` | 3,951 | Associates object templates with skills and cast-context/AI-weight information. |
| `PlayerFlags` | 415 | Player flag definitions, including session and zone scope. |
| `PlayerStatistics` | 27 | Player-statistic identifiers and display ordering. |
| `SkillBehavior` | 1,521 | Skill roots and settings such as cooldowns, cast type, cost, and UI bonuses. |
| `Preconditions` | 333 | Reusable requirement checks referencing target LOTs/groups/counts and valid contexts. |

## Items, currencies, vendors, and loot

| Table | Rows | Overview |
|---|---:|---|
| `CurrencyDenominations` | 9 | Currency denomination values and associated object IDs. |
| `CurrencyTable` | 166 | Currency reward ranges indexed by currency and NPC level. |
| `ItemComponent` | 7,405 | Item-template properties such as item type, rarity, stack, equipment, value, requirements, flags, and costs. |
| `ItemEggData` | 3 | Egg item chassis-type data. |
| `ItemFoodData` | 0 | Food-item elemental composition fields; empty in this snapshot. |
| `ItemSets` | 49 | Item-set definitions, kit metadata, localization, and skill-set references. |
| `ItemSetSkills` | 322 | Links item skill-set IDs to skills and cast types. |
| `LootMatrix` | 2,675 | Loot-matrix entries connecting loot tables, rarity tables, probabilities, and drop counts. |
| `LootMatrixIndex` | 581 | Loot-matrix index definitions and NPC-editor visibility. |
| `LootTable` | 6,519 | Item entries in loot tables, including mission-drop and sort-priority fields. |
| `LootTableIndex` | 756 | Loot-table index definitions. |
| `RarityTable` | 54 | Rarity weights/ranges within rarity-table indexes. |
| `RarityTableIndex` | 26 | Rarity-table index definitions. |
| `VendorComponent` | 92 | Vendor buy/sell scalars, stock refresh interval, and loot-matrix reference. |

## Missions, rewards, and activities

| Table | Rows | Overview |
|---|---:|---|
| `Activities` | 158 | Activity configuration including instance map, teams, timing, entry costs, and leaderboard options. |
| `ActivityRewards` | 291 | Activity rating/reward rows with loot, currency, and challenge references. |
| `ActivityText` | 23 | Localized activity text records and gating metadata. |
| `DeletionRestrictions` | 16 | Rules describing restricted deletions and their check type/localization. |
| `MissionEmail` | 272 | Mission-related notification/email types, attachment LOTs, and localization. |
| `MissionNPCComponent` | 917 | Associates mission IDs with mission-offer/accept flags for a mission-offer component. |
| `Missions` | 1,427 | Mission definitions, prerequisites, targets, rewards, repeatability, time limits, and random pools. |
| `MissionTasks` | 1,804 | Mission objective/task definitions, target values, parameters, icons, and localization. |
| `MissionText` | 1,430 | Mission presentation data such as icons, animations, cinematics, audio events, and localization. |
| `RewardCodes` | 78 | Reward codes and their attachment LOTs. |
| `Rewards` | 10 | Reward records linked to levels/missions with reward type, value, and count. |
| `ReputationRewards` | 0 | Reputation level/sublevel reward values; empty in this snapshot. |
| `SmashableChain` | 4 | Step-level loot, rarity, currency, smash-count, and timing data for smashable chains. |
| `SmashableChainIndex` | 1 | Smashable-chain index, target group, description, and continuity flag. |
| `SmashableComponent` | 5 | Smashable component records referencing loot matrices. |
| `SmashableElements` | 775 | Smashable element IDs and their drop weights. |

## Zones, properties, and world configuration

| Table | Rows | Overview |
|---|---:|---|
| `LUPZoneIDs` | 5 | Zone IDs identified as LUP-related in this dataset. |
| `PropertyEntranceComponent` | 12 | Property entrance component records, including map, property name, and group type. |
| `PropertyTemplate` | 73 | Static property templates with map/zone, pricing, duration, clone, spawn, and build-height settings. |
| `SceneTable` | 61 | Scene IDs and scene names. |
| `WorldConfig` | 1 | World-wide gameplay defaults and tuning values, including movement, death, property, mail, and progression settings. |
| `ZoneLoadingTips` | 35 | Zone-specific loading-tip localization and weighting data. |
| `ZoneSummary` | 48 | Zone summary values keyed by zone and type. |
| `ZoneTable` | 1,056 | Zone configuration including names, scripts, population/physics settings, map folders, and feature flags. |

## Building, properties, and user-generated content

| Table | Rows | Overview |
|---|---:|---|
| `Blueprints` | 2 | Blueprint records with ownership, descriptive, pricing, category, file, and status fields. |
| `brickAttributes` | 25 | Brick icon, display-order, and localization-status metadata. |
| `BrickColors` | 53 | Brick color values and palette/validity metadata. |
| `BrickIDTable` | 1,909 | Maps LEGO brick identifiers to object IDs. |
| `LUPExhibitComponent` | 1 | LUP exhibit bounds and offsets. |
| `LUPExhibitModelData` | 4 | LUP exhibit model bounds, descriptions, and owner data. |
| `map_BlueprintCategory` | 1 | Blueprint category description and enabled state. |
| `ModularBuildComponent` | 4 | Modular-build definitions, XML, generated LOT/physics IDs, and audio events. |
| `ModuleComponent` | 387 | Build module definitions including part/build type, XML, sounds, and assembly effect. |
| `TamingBuildPuzzles` | 30 | Pet-taming puzzle models, valid/invalid pieces, difficulty, time, and imagination cost. |
| `UGBehaviorSounds` | 21 | User-generated behavior sound IDs/GUIDs and localization metadata. |

## Models, animation, rendering, and audio/visual effects

| Table | Rows | Overview |
|---|---:|---|
| `AnimationIndex` | 630 | Animation-group descriptions and group types. |
| `Animations` | 7,615 | Animation names and playback settings such as loops, duration, blend, priority, and body/face behavior. |
| `CelebrationParameters` | 14 | Celebration presentation settings including text, icons, camera path, lighting, fog, and audio. |
| `FlairTable` | 59 | Flair IDs mapped to asset references. |
| `Icons` | 3,279 | Icon IDs, paths, and names. |
| `MotionFX` | 6 | Motion-effect type and movement/scale/duration parameters. |
| `RenderComponent` | 13,690 | Render assets, icons, shaders, effects, animation groups, LODs, billboard, and audio settings. |
| `RenderComponentFlash` | 74 | Flash-render component settings and asset/node/element references. |
| `RenderComponentWrapper` | 2 | Default render-wrapper asset definitions. |
| `RenderIconAssets` | 897 | Icon asset mappings. |
| `TrailEffects` | 9 | Trail particle, texture, color, timing, and bone settings. |

## Vehicles, movement, and control

| Table | Rows | Overview |
|---|---:|---|
| `Camera` | 16 | Camera follow, zoom, pitch/yaw, movement, collision, and field-of-view tuning. |
| `ControlSchemes` | 9 | Keyboard/gamepad movement, rotation, zoom, and free-camera sensitivity settings. |
| `MovingPlatforms` | 41 | Moving-platform motion vectors, duration, start direction, and description. |
| `RacingModuleComponent` | 57 | Racing module performance values such as speed, acceleration, handling, stability, and imagination. |
| `RailActivatorComponent` | 11 | Rail activation animation, sound/effect, collision, camera, damage, and precondition settings. |
| `RocketLaunchpadControlComponent` | 36 | Rocket launch destination, animation/audio, landing, and precondition settings. |
| `SurfaceType` | 15 | Surface identifiers mapped to footstep audio metadata. |
| `VehiclePhysics` | 28 | Vehicle physics and handling parameters, including chassis, tires, steering, boost, collision, and audio. |
| `VehicleStatMap` | 12 | Maps module stats to Havok vehicle-physics stats and per-module changes. |

## Interface, text, and localization

| Table | Rows | Overview |
|---|---:|---|
| `Emotes` | 389 | Emote commands, animations, icons, channels, unlocks, and localization. |
| `LanguageType` | 1 | Language IDs and descriptions. |
| `mapIcon` | 2,224 | LOT/state-to-icon mappings. |
| `mapItemTypes` | 23 | Item type descriptions and equipment-location mappings. |
| `mapRenderEffects` | 13 | Game render-effect IDs and descriptions. |
| `mapShaders` | 100 | Shader labels, game values, and priorities. |
| `mapTextureResource` | 80 | Texture paths and associated surface types. |
| `SpeedchatMenu` | 64 | Hierarchical speedchat entries, emotes, images, and localization. |
| `TextDescription` | 0 | Text-description records; empty in this snapshot. |
| `TextLanguage` | 0 | Language-specific text records; empty in this snapshot. |
| `WhatsCoolItemSpotlight` | 88 | Items featured in the “What’s Cool” spotlight with localization metadata. |
| `WhatsCoolNewsAndTips` | 83 | “What’s Cool” news/tips entries, icons, type, and localization. |

## Lookup, asset, release, and database metadata

| Table | Rows | Overview |
|---|---:|---|
| `EventGating` | 8 | Named event availability windows with start/end dates. |
| `FeatureGating` | 35 | Feature-version gating metadata and descriptions. |
| `mapAnimationPriorities` | 12 | Animation-priority IDs and names. |
| `mapAssetType` | 11 | Asset type labels and path-directory mappings. |
| `Release_Version` | 126 | Release-version/date records. |
| `SubscriptionPricing` | 3 | Country, subscription fee, and currency-symbol formatting data. |
| `DBExclude` | 104 | Table/column exclusions used as database-processing metadata. |
| `dtproperties` | 0 | Legacy database diagram/property metadata; empty in this snapshot. |
| `sysdiagrams` | 1 | Database diagram metadata, not a gameplay definition. |

## Reading the catalog

- `ComponentsRegistry` is the main bridge from an object LOT to a component
  table. A component-table row count therefore does not directly tell you how
  many unique objects use that component.
- Mission NPC associations are stored in `MissionNPCComponent` and are
  resolved through the component ID registered for `MISSION_OFFER`.
- Item definitions are in `ItemComponent`; player inventory instances are
  runtime character data, not rows in this static item-definition table.
- The database also has intentional or incidental empty tables in this
  snapshot. Their presence does not prove that the corresponding feature has
  data or is active.
- For the key relationships and the distinction between static CDClient data
  and DLU's runtime game database, see
  [LEGO Universe Data Model and Public Research](./LEGO%20Universe%20Data%20Model%20and%20Public%20Research.md).
