# CDClient Table Schema

This reference lists the names and columns of 137 tables from the local CDClient schema, with a short purpose summary.
It contains no table rows or player data. Full local table exports are not part of this public site.

## Browse by topic

- [Building, properties, and user-generated content](#building-properties-and-user-generated-content)
- [Interface, text, and localization](#interface-text-and-localization)
- [Items, currencies, vendors, and loot](#items-currencies-vendors-and-loot)
- [Lookup, asset, release, and database metadata](#lookup-asset-release-and-database-metadata)
- [Missions, rewards, and activities](#missions-rewards-and-activities)
- [Models, animation, rendering, and audio/visual effects](#models-animation-rendering-and-audiovisual-effects)
- [Object templates and components](#object-templates-and-components)
- [Skills, behaviors, combat, and progression](#skills-behaviors-combat-and-progression)
- [Vehicles, movement, and control](#vehicles-movement-and-control)
- [Zones, properties, and world configuration](#zones-properties-and-world-configuration)

## Building, properties, and user-generated content

### `Blueprints` {#table-blueprints}

Blueprint records with ownership, descriptive, pricing, category, file, and status fields.

**Columns:** `id`, `name`, `description`, `accountid`, `characterid`, `price`, `rating`, `categoryid`, `lxfpath`, `deleted`, `created`, `modified`

### `brickAttributes` {#table-brickattributes}

Brick icon, display-order, and localization-status metadata.

**Columns:** `ID`, `icon_asset`, `display_order`, `locStatus`

### `BrickColors` {#table-brickcolors}

Brick color values and palette/validity metadata.

**Columns:** `id`, `red`, `green`, `blue`, `alpha`, `legopaletteid`, `description`, `validTypes`, `validCharacters`, `factoryValid`

### `BrickIDTable` {#table-brickidtable}

Maps LEGO brick identifiers to object IDs.

**Columns:** `NDObjectID`, `LEGOBrickID`

### `LUPExhibitComponent` {#table-lupexhibitcomponent}

LUP exhibit bounds and offsets.

**Columns:** `id`, `minXZ`, `maxXZ`, `maxY`, `offsetX`, `offsetY`, `offsetZ`

### `LUPExhibitModelData` {#table-lupexhibitmodeldata}

LUP exhibit model bounds, descriptions, and owner data.

**Columns:** `LOT`, `minXZ`, `maxXZ`, `maxY`, `description`, `owner`

### `map_BlueprintCategory` {#table-map-blueprintcategory}

Blueprint category description and enabled state.

**Columns:** `id`, `description`, `enabled`

### `ModularBuildComponent` {#table-modularbuildcomponent}

Modular-build definitions, XML, generated LOT/physics IDs, and audio events.

**Columns:** `id`, `buildType`, `xml`, `createdLOT`, `createdPhysicsID`, `AudioEventGUID_Snap`, `AudioEventGUID_Complete`, `AudioEventGUID_Present`

### `ModuleComponent` {#table-modulecomponent}

Build module definitions including part/build type, XML, sounds, and assembly effect.

**Columns:** `id`, `partCode`, `buildType`, `xml`, `primarySoundGUID`, `assembledEffectID`

### `TamingBuildPuzzles` {#table-tamingbuildpuzzles}

Pet-taming puzzle models, valid/invalid pieces, difficulty, time, and imagination cost.

**Columns:** `id`, `PuzzleModelLot`, `NPCLot`, `ValidPiecesLXF`, `InvalidPiecesLXF`, `Difficulty`, `Timelimit`, `NumValidPieces`, `TotalNumPieces`, `ModelName`, `FullModelLXF`, `Duration`, `imagCostPerBuild`

### `UGBehaviorSounds` {#table-ugbehaviorsounds}

User-generated behavior sound IDs/GUIDs and localization metadata.

**Columns:** `id`, `guid`, `localize`, `locStatus`, `gate_version`

## Interface, text, and localization

### `Emotes` {#table-emotes}

Emote commands, animations, icons, channels, unlocks, and localization.

**Columns:** `id`, `animationName`, `iconFilename`, `channel`, `command`, `locked`, `localize`, `locStatus`, `gate_version`

### `LanguageType` {#table-languagetype}

Language IDs and descriptions.

**Columns:** `LanguageID`, `LanguageDescription`

### `mapIcon` {#table-mapicon}

LOT/state-to-icon mappings.

**Columns:** `LOT`, `iconID`, `iconState`

### `mapItemTypes` {#table-mapitemtypes}

Item type descriptions and equipment-location mappings.

**Columns:** `id`, `description`, `equipLocation`

### `mapRenderEffects` {#table-maprendereffects}

Game render-effect IDs and descriptions.

**Columns:** `id`, `gameID`, `description`

### `mapShaders` {#table-mapshaders}

Shader labels, game values, and priorities.

**Columns:** `id`, `label`, `gameValue`, `priority`

### `mapTextureResource` {#table-maptextureresource}

Texture paths and associated surface types.

**Columns:** `id`, `texturepath`, `SurfaceType`

### `SpeedchatMenu` {#table-speedchatmenu}

Hierarchical speedchat entries, emotes, images, and localization.

**Columns:** `id`, `parentId`, `emoteId`, `imageName`, `localize`, `locStatus`, `gate_version`

### `TextDescription` {#table-textdescription}

Text-description records; empty in this snapshot.

**Columns:** `TextID`, `TestDescription`

### `TextLanguage` {#table-textlanguage}

Language-specific text records; empty in this snapshot.

**Columns:** `TextID`, `LanguageID`, `Text`

### `WhatsCoolItemSpotlight` {#table-whatscoolitemspotlight}

Items featured in the “What’s Cool” spotlight with localization metadata.

**Columns:** `id`, `itemID`, `localize`, `gate_version`, `locStatus`

### `WhatsCoolNewsAndTips` {#table-whatscoolnewsandtips}

“What’s Cool” news/tips entries, icons, type, and localization.

**Columns:** `id`, `iconID`, `type`, `localize`, `gate_version`, `locStatus`

## Items, currencies, vendors, and loot

### `CurrencyDenominations` {#table-currencydenominations}

Currency denomination values and associated object IDs.

**Columns:** `value`, `objectid`

### `CurrencyTable` {#table-currencytable}

Currency reward ranges indexed by currency and NPC level.

**Columns:** `currencyIndex`, `npcminlevel`, `minvalue`, `maxvalue`, `id`

### `ItemComponent` {#table-itemcomponent}

Item-template properties such as item type, rarity, stack, equipment, value, requirements, flags, and costs.

**Columns:** `id`, `equipLocation`, `baseValue`, `isKitPiece`, `rarity`, `itemType`, `itemInfo`, `inLootTable`, `inVendor`, `isUnique`, `isBOP`, `isBOE`, `reqFlagID`, `reqSpecialtyID`, `reqSpecRank`, `reqAchievementID`, `stackSize`, `color1`, `decal`, `offsetGroupID`, `buildTypes`, `reqPrecondition`, `animationFlag`, `equipEffects`, `readyForQA`, `itemRating`, `isTwoHanded`, `minNumRequired`, `delResIndex`, `currencyLOT`, `altCurrencyCost`, `subItems`, `audioEventUse`, `noEquipAnimation`, `commendationLOT`, `commendationCost`, `audioEquipMetaEventSet`, `currencyCosts`, `ingredientInfo`, `locStatus`, `forgeType`, `SellMultiplier`

### `ItemEggData` {#table-itemeggdata}

Egg item chassis-type data.

**Columns:** `id`, `chassie_type_id`

### `ItemFoodData` {#table-itemfooddata}

Food-item elemental composition fields; empty in this snapshot.

**Columns:** `id`, `element_1`, `element_1_amount`, `element_2`, `element_2_amount`, `element_3`, `element_3_amount`, `element_4`, `element_4_amount`

### `ItemSets` {#table-itemsets}

Item-set definitions, kit metadata, localization, and skill-set references.

**Columns:** `setID`, `locStatus`, `itemIDs`, `kitType`, `kitRank`, `kitImage`, `skillSetWith2`, `skillSetWith3`, `skillSetWith4`, `skillSetWith5`, `skillSetWith6`, `localize`, `gate_version`, `kitID`, `priority`

### `ItemSetSkills` {#table-itemsetskills}

Links item skill-set IDs to skills and cast types.

**Columns:** `SkillSetID`, `SkillID`, `SkillCastType`

### `LootMatrix` {#table-lootmatrix}

Loot-matrix entries connecting loot tables, rarity tables, probabilities, and drop counts.

**Columns:** `LootMatrixIndex`, `LootTableIndex`, `RarityTableIndex`, `percent`, `minToDrop`, `maxToDrop`, `id`, `flagID`, `gate_version`

### `LootMatrixIndex` {#table-lootmatrixindex}

Loot-matrix index definitions and NPC-editor visibility.

**Columns:** `LootMatrixIndex`, `inNpcEditor`

### `LootTable` {#table-loottable}

Item entries in loot tables, including mission-drop and sort-priority fields.

**Columns:** `itemid`, `LootTableIndex`, `id`, `MissionDrop`, `sortPriority`

### `LootTableIndex` {#table-loottableindex}

Loot-table index definitions.

**Columns:** `LootTableIndex`

### `RarityTable` {#table-raritytable}

Rarity weights/ranges within rarity-table indexes.

**Columns:** `id`, `randmax`, `rarity`, `RarityTableIndex`

### `RarityTableIndex` {#table-raritytableindex}

Rarity-table index definitions.

**Columns:** `RarityTableIndex`

### `VendorComponent` {#table-vendorcomponent}

Vendor buy/sell scalars, stock refresh interval, and loot-matrix reference.

**Columns:** `id`, `buyScalar`, `sellScalar`, `refreshTimeSeconds`, `LootMatrixIndex`

## Lookup, asset, release, and database metadata

### `DBExclude` {#table-dbexclude}

Table/column exclusions used as database-processing metadata.

**Columns:** `table`, `column`

### `dtproperties` {#table-dtproperties}

Legacy database diagram/property metadata; empty in this snapshot.

**Columns:** `id`, `objectid`, `property`, `value`, `uvalue`, `lvalue`, `version`

### `EventGating` {#table-eventgating}

Named event availability windows with start/end dates.

**Columns:** `eventName`, `date_start`, `date_end`

### `FeatureGating` {#table-featuregating}

Feature-version gating metadata and descriptions.

**Columns:** `featureName`, `major`, `current`, `minor`, `description`

### `mapAnimationPriorities` {#table-mapanimationpriorities}

Animation-priority IDs and names.

**Columns:** `id`, `name`, `priority`

### `mapAssetType` {#table-mapassettype}

Asset type labels and path-directory mappings.

**Columns:** `id`, `label`, `pathdir`, `typelabel`

### `Release_Version` {#table-release-version}

Release-version/date records.

**Columns:** `ReleaseVersion`, `ReleaseDate`

### `SubscriptionPricing` {#table-subscriptionpricing}

Country, subscription fee, and currency-symbol formatting data.

**Columns:** `id`, `countryCode`, `monthlyFeeGold`, `monthlyFeeSilver`, `monthlyFeeBronze`, `monetarySymbol`, `symbolIsAppended`

### `sysdiagrams` {#table-sysdiagrams}

Database diagram metadata, not a gameplay definition.

**Columns:** `name`, `principal_id`, `diagram_id`, `version`, `definition`

## Missions, rewards, and activities

### `Activities` {#table-activities}

Activity configuration including instance map, teams, timing, entry costs, and leaderboard options.

**Columns:** `ActivityID`, `locStatus`, `instanceMapID`, `minTeams`, `maxTeams`, `minTeamSize`, `maxTeamSize`, `waitTime`, `startDelay`, `requiresUniqueData`, `leaderboardType`, `localize`, `optionalCostLOT`, `optionalCostCount`, `showUIRewards`, `CommunityActivityFlagID`, `gate_version`, `noTeamLootOnDeath`, `optionalPercentage`

### `ActivityRewards` {#table-activityrewards}

Activity rating/reward rows with loot, currency, and challenge references.

**Columns:** `objectTemplate`, `ActivityRewardIndex`, `activityRating`, `LootMatrixIndex`, `CurrencyIndex`, `ChallengeRating`, `description`

### `ActivityText` {#table-activitytext}

Localized activity text records and gating metadata.

**Columns:** `activityID`, `type`, `localize`, `locStatus`, `gate_version`

### `DeletionRestrictions` {#table-deletionrestrictions}

Rules describing restricted deletions and their check type/localization.

**Columns:** `id`, `restricted`, `ids`, `checkType`, `localize`, `locStatus`, `gate_version`

### `MissionEmail` {#table-missionemail}

Mission-related notification/email types, attachment LOTs, and localization.

**Columns:** `ID`, `messageType`, `notificationGroup`, `missionID`, `attachmentLOT`, `localize`, `locStatus`, `gate_version`

### `MissionNPCComponent` {#table-missionnpccomponent}

Associates mission IDs with mission-offer/accept flags for a mission-offer component.

**Columns:** `id`, `missionID`, `offersMission`, `acceptsMission`, `gate_version`

### `Missions` {#table-missions}

Mission definitions, prerequisites, targets, rewards, repeatability, time limits, and random pools.

**Columns:** `id`, `defined_type`, `defined_subtype`, `UISortOrder`, `offer_objectID`, `target_objectID`, `reward_currency`, `LegoScore`, `reward_reputation`, `isChoiceReward`, `reward_item1`, `reward_item1_count`, `reward_item2`, `reward_item2_count`, `reward_item3`, `reward_item3_count`, `reward_item4`, `reward_item4_count`, `reward_emote`, `reward_emote2`, `reward_emote3`, `reward_emote4`, `reward_maximagination`, `reward_maxhealth`, `reward_maxinventory`, `reward_maxmodel`, `reward_maxwidget`, `reward_maxwallet`, `repeatable`, `reward_currency_repeatable`, `reward_item1_repeatable`, `reward_item1_repeat_count`, `reward_item2_repeatable`, `reward_item2_repeat_count`, `reward_item3_repeatable`, `reward_item3_repeat_count`, `reward_item4_repeatable`, `reward_item4_repeat_count`, `time_limit`, `isMission`, `missionIconID`, `prereqMissionID`, `localize`, `inMOTD`, `cooldownTime`, `isRandom`, `randomPool`, `UIPrereqID`, `gate_version`, `HUDStates`, `locStatus`, `reward_bankinventory`

### `MissionTasks` {#table-missiontasks}

Mission objective/task definitions, target values, parameters, icons, and localization.

**Columns:** `id`, `locStatus`, `taskType`, `target`, `targetGroup`, `targetValue`, `taskParam1`, `largeTaskIcon`, `IconID`, `uid`, `largeTaskIconID`, `localize`, `gate_version`

### `MissionText` {#table-missiontext}

Mission presentation data such as icons, animations, cinematics, audio events, and localization.

**Columns:** `id`, `story_icon`, `missionIcon`, `offerNPCIcon`, `IconID`, `state_1_anim`, `state_2_anim`, `state_3_anim`, `state_4_anim`, `state_3_turnin_anim`, `state_4_turnin_anim`, `onclick_anim`, `CinematicAccepted`, `CinematicAcceptedLeadin`, `CinematicCompleted`, `CinematicCompletedLeadin`, `CinematicRepeatable`, `CinematicRepeatableLeadin`, `CinematicRepeatableCompleted`, `CinematicRepeatableCompletedLeadin`, `AudioEventGUID_Interact`, `AudioEventGUID_OfferAccept`, `AudioEventGUID_OfferDeny`, `AudioEventGUID_Completed`, `AudioEventGUID_TurnIn`, `AudioEventGUID_Failed`, `AudioEventGUID_Progress`, `AudioMusicCue_OfferAccept`, `AudioMusicCue_TurnIn`, `turnInIconID`, `localize`, `locStatus`, `gate_version`

### `ReputationRewards` {#table-reputationrewards}

Reputation level/sublevel reward values; empty in this snapshot.

**Columns:** `repLevel`, `sublevel`, `reputation`

### `RewardCodes` {#table-rewardcodes}

Reward codes and their attachment LOTs.

**Columns:** `id`, `code`, `attachmentLOT`, `locStatus`, `gate_version`

### `Rewards` {#table-rewards}

Reward records linked to levels/missions with reward type, value, and count.

**Columns:** `id`, `LevelID`, `MissionID`, `RewardType`, `value`, `count`

### `SmashableChain` {#table-smashablechain}

Step-level loot, rarity, currency, smash-count, and timing data for smashable chains.

**Columns:** `chainIndex`, `chainLevel`, `lootMatrixID`, `rarityTableIndex`, `currencyIndex`, `currencyLevel`, `smashCount`, `timeLimit`, `chainStepID`

### `SmashableChainIndex` {#table-smashablechainindex}

Smashable-chain index, target group, description, and continuity flag.

**Columns:** `id`, `targetGroup`, `description`, `continuous`

### `SmashableComponent` {#table-smashablecomponent}

Smashable component records referencing loot matrices.

**Columns:** `id`, `LootMatrixIndex`

### `SmashableElements` {#table-smashableelements}

Smashable element IDs and their drop weights.

**Columns:** `elementID`, `dropWeight`

## Models, animation, rendering, and audio/visual effects

### `AnimationIndex` {#table-animationindex}

Animation-group descriptions and group types.

**Columns:** `animationGroupID`, `description`, `groupType`

### `Animations` {#table-animations}

Animation names and playback settings such as loops, duration, blend, priority, and body/face behavior.

**Columns:** `animationGroupID`, `animation_type`, `animation_name`, `chance_to_play`, `min_loops`, `max_loops`, `animation_length`, `hideEquip`, `ignoreUpperBody`, `restartable`, `face_animation_name`, `priority`, `blendTime`

### `CelebrationParameters` {#table-celebrationparameters}

Celebration presentation settings including text, icons, camera path, lighting, fog, and audio.

**Columns:** `id`, `animation`, `backgroundObject`, `duration`, `subText`, `mainText`, `iconID`, `celeLeadIn`, `celeLeadOut`, `cameraPathLOT`, `pathNodeName`, `ambientR`, `ambientG`, `ambientB`, `directionalR`, `directionalG`, `directionalB`, `specularR`, `specularG`, `specularB`, `lightPositionX`, `lightPositionY`, `lightPositionZ`, `blendTime`, `fogColorR`, `fogColorG`, `fogColorB`, `musicCue`, `soundGUID`, `mixerProgram`

### `FlairTable` {#table-flairtable}

Flair IDs mapped to asset references.

**Columns:** `id`, `asset`

### `Icons` {#table-icons}

Icon IDs, paths, and names.

**Columns:** `IconID`, `IconPath`, `IconName`

### `MotionFX` {#table-motionfx}

Motion-effect type and movement/scale/duration parameters.

**Columns:** `id`, `typeID`, `slamVelocity`, `addVelocity`, `duration`, `destGroupName`, `startScale`, `endScale`, `velocity`, `distance`

### `RenderComponent` {#table-rendercomponent}

Render assets, icons, shaders, effects, animation groups, LODs, billboard, and audio settings.

**Columns:** `id`, `render_asset`, `icon_asset`, `IconID`, `shader_id`, `effect1`, `effect2`, `effect3`, `effect4`, `effect5`, `effect6`, `animationGroupIDs`, `fade`, `usedropshadow`, `preloadAnimations`, `fadeInTime`, `maxShadowDistance`, `ignoreCameraCollision`, `renderComponentLOD1`, `renderComponentLOD2`, `gradualSnap`, `animationFlag`, `AudioMetaEventSet`, `billboardHeight`, `chatBubbleOffset`, `staticBillboard`, `LXFMLFolder`, `attachIndicatorsToNode`

### `RenderComponentFlash` {#table-rendercomponentflash}

Flash-render component settings and asset/node/element references.

**Columns:** `id`, `interactive`, `animated`, `nodeName`, `flashPath`, `elementName`, `_uid`

### `RenderComponentWrapper` {#table-rendercomponentwrapper}

Default render-wrapper asset definitions.

**Columns:** `id`, `defaultWrapperAsset`

### `RenderIconAssets` {#table-rendericonassets}

Icon asset mappings.

**Columns:** `id`, `icon_asset`, `blank_column`

### `TrailEffects` {#table-traileffects}

Trail particle, texture, color, timing, and bone settings.

**Columns:** `trailID`, `textureName`, `blendmode`, `cardlifetime`, `colorlifetime`, `minTailFade`, `tailFade`, `max_particles`, `birthDelay`, `deathDelay`, `bone1`, `bone2`, `texLength`, `texWidth`, `startColorR`, `startColorG`, `startColorB`, `startColorA`, `middleColorR`, `middleColorG`, `middleColorB`, `middleColorA`, `endColorR`, `endColorG`, `endColorB`, `endColorA`

## Object templates and components

### `AccessoryDefaultLoc` {#table-accessorydefaultloc}

Default positions and rotations for attaching accessories, grouped by attachment group.

**Columns:** `GroupID`, `Description`, `Pos_X`, `Pos_Y`, `Pos_Z`, `Rot_X`, `Rot_Y`, `Rot_Z`

### `BaseCombatAIComponent` {#table-basecombataicomponent}

Combat-AI settings such as behavior type, role, aggro/tether ranges, speeds, and timing.

**Columns:** `id`, `behaviorType`, `combatRoundLength`, `combatRole`, `minRoundLength`, `maxRoundLength`, `tetherSpeed`, `pursuitSpeed`, `combatStartDelay`, `softTetherRadius`, `hardTetherRadius`, `spawnTimer`, `tetherEffectID`, `ignoreMediator`, `aggroRadius`, `ignoreStatReset`, `ignoreParent`

### `ChoiceBuildComponent` {#table-choicebuildcomponent}

Choice-build component definitions, including selections and imagination overrides.

**Columns:** `id`, `selections`, `imaginationOverride`

### `CollectibleComponent` {#table-collectiblecomponent}

Collectible-object records and their mission requirement references.

**Columns:** `id`, `requirement_mission`

### `ComponentsRegistry` {#table-componentsregistry}

Maps a LOT and component type to the component-specific record ID used to construct an entity.

**Columns:** `id`, `component_type`, `component_id`

### `DestructibleComponent` {#table-destructiblecomponent}

Destructible-object settings such as faction, health, loot/currency references, level, armor, and smashability.

**Columns:** `id`, `faction`, `factionList`, `life`, `imagination`, `LootMatrixIndex`, `CurrencyIndex`, `level`, `armor`, `death_behavior`, `isnpc`, `attack_priority`, `isSmashable`, `difficultyLevel`

### `ExhibitComponent` {#table-exhibitcomponent}

Exhibit dimensions, offsets, and reputation-size settings.

**Columns:** `id`, `length`, `width`, `height`, `offsetX`, `offsetY`, `offsetZ`, `fReputationSizeMultiplier`, `fImaginationCost`

### `Factions` {#table-factions}

Faction relationships, including friendly and enemy lists.

**Columns:** `faction`, `factionList`, `factionListFriendly`, `friendList`, `enemyList`

### `InventoryComponent` {#table-inventorycomponent}

Preset inventory entries for applicable object templates, including item LOT, count, and equip state.

**Columns:** `id`, `itemid`, `count`, `equip`

### `JetPackPadComponent` {#table-jetpackpadcomponent}

Jetpack-pad distance and blocker/warning-volume settings.

**Columns:** `id`, `xDistance`, `yDistance`, `warnDistance`, `lotBlocker`, `lotWarningVolume`

### `MinifigComponent` {#table-minifigcomponent}

Minifigure appearance-part IDs such as head, torso, legs, hair, and face details.

**Columns:** `id`, `head`, `chest`, `legs`, `hairstyle`, `haircolor`, `chestdecal`, `headcolor`, `lefthand`, `righthand`, `eyebrowstyle`, `eyesstyle`, `mouthstyle`

### `MinifigDecals_Eyebrows` {#table-minifigdecals-eyebrows}

Eyebrow decal asset paths and character-creation/gender validity flags.

**Columns:** `ID`, `High_path`, `Low_path`, `CharacterCreateValid`, `male`, `female`

### `MinifigDecals_Eyes` {#table-minifigdecals-eyes}

Eye decal asset paths and character-creation/gender validity flags.

**Columns:** `ID`, `High_path`, `Low_path`, `CharacterCreateValid`, `male`, `female`

### `MinifigDecals_Legs` {#table-minifigdecals-legs}

Leg decal IDs and high-resolution asset paths.

**Columns:** `ID`, `High_path`

### `MinifigDecals_Mouths` {#table-minifigdecals-mouths}

Mouth decal asset paths and character-creation/gender validity flags.

**Columns:** `ID`, `High_path`, `Low_path`, `CharacterCreateValid`, `male`, `female`

### `MinifigDecals_Torsos` {#table-minifigdecals-torsos}

Torso decal asset paths and character-creation/gender validity flags.

**Columns:** `ID`, `High_path`, `CharacterCreateValid`, `male`, `female`

### `MovementAIComponent` {#table-movementaicomponent}

Movement-AI type, wandering parameters, speed, radius, and optional attached path.

**Columns:** `id`, `MovementType`, `WanderChance`, `WanderDelayMin`, `WanderDelayMax`, `WanderSpeed`, `WanderRadius`, `attachedPath`

### `NpcIcons` {#table-npcicons}

NPC icon appearance, placement, scaling, rotation, and composite-icon settings.

**Columns:** `id`, `color`, `offset`, `LOT`, `Texture`, `isClickable`, `scale`, `rotateToFace`, `compositeHorizOffset`, `compositeVertOffset`, `compositeScale`, `compositeConnectionNode`, `compositeLOTMultiMission`, `compositeLOTMultiMissionVentor`, `compositeIconTexture`

### `Objects` {#table-objects}

Object templates keyed by LOT, including names, type, placement/localization flags, and related metadata.

**Columns:** `id`, `name`, `placeable`, `type`, `description`, `localize`, `npcTemplateID`, `displayName`, `interactionDistance`, `nametag`, `_internalNotes`, `locStatus`, `gate_version`, `HQ_valid`

### `PackageComponent` {#table-packagecomponent}

Package definitions that reference loot matrices and package types.

**Columns:** `id`, `LootMatrixIndex`, `packageType`

### `PetAbilities` {#table-petabilities}

Pet ability names, imagination costs, and localization status.

**Columns:** `id`, `AbilityName`, `ImaginationCost`, `locStatus`

### `PetComponent` {#table-petcomponent}

Pet taming, movement, form, elemental type, drain, audio, and buff settings.

**Columns:** `id`, `minTameUpdateTime`, `maxTameUpdateTime`, `percentTameChance`, `tamability`, `elementType`, `walkSpeed`, `runSpeed`, `sprintSpeed`, `idleTimeMin`, `idleTimeMax`, `petForm`, `imaginationDrainRate`, `AudioMetaEventSet`, `buffIDs`

### `PetNestComponent` {#table-petnestcomponent}

Elemental type associated with a pet nest.

**Columns:** `id`, `ElementalType`

### `PhysicsComponent` {#table-physicscomponent}

Physics asset and movement/collision parameters for object templates.

**Columns:** `id`, `static`, `physics_asset`, `jump`, `doublejump`, `speed`, `rotSpeed`, `playerHeight`, `playerRadius`, `pcShapeType`, `collisionGroup`, `airSpeed`, `boundaryAsset`, `jumpAirSpeed`, `friction`, `gravityVolumeAsset`

### `PossessableComponent` {#table-possessablecomponent}

Possession/mount control scheme, attachment animations/offsets, and related settings.

**Columns:** `id`, `controlSchemeID`, `minifigAttachPoint`, `minifigAttachAnimation`, `minifigDetachAnimation`, `mountAttachAnimation`, `mountDetachAnimation`, `attachOffsetFwd`, `attachOffsetRight`, `possessionType`, `wantBillboard`, `billboardOffsetUp`, `depossessOnHit`, `hitStunTime`, `skillSet`

### `ProximityMonitorComponent` {#table-proximitymonitorcomponent}

Per-object proximity-monitor configuration and client/server loading flags.

**Columns:** `id`, `Proximities`, `LoadOnClient`, `LoadOnServer`

### `ProximityTypes` {#table-proximitytypes}

Named proximity types with radius, collision group, passive checks, and loading options.

**Columns:** `id`, `Name`, `Radius`, `CollisionGroup`, `PassiveChecks`, `IconID`, `LoadOnClient`, `LoadOnServer`

### `RebuildComponent` {#table-rebuildcomponent}

Rebuildable-object timings, imagination costs, interruption, module, and activity settings.

**Columns:** `id`, `reset_time`, `complete_time`, `take_imagination`, `interruptible`, `self_activator`, `custom_modules`, `activityID`, `post_imagination_cost`, `time_before_smash`

### `RebuildSections` {#table-rebuildsections}

Rebuild-section object IDs, offsets, fall animation/height, required pieces, and placement state.

**Columns:** `id`, `rebuildID`, `objectID`, `offset_x`, `offset_y`, `offset_z`, `fall_angle_x`, `fall_angle_y`, `fall_angle_z`, `fall_height`, `requires_list`, `size`, `bPlaced`

### `ScriptComponent` {#table-scriptcomponent}

Server- and client-side script names associated with component records.

**Columns:** `id`, `script_name`, `client_script_name`

## Skills, behaviors, combat, and progression

### `AICombatRoles` {#table-aicombatroles}

Combat-role preferences and role-specific distance ranges.

**Columns:** `id`, `preferredRole`, `specifiedMinRangeNOUSE`, `specifiedMaxRangeNOUSE`, `specificMinRange`, `specificMaxRange`

### `BehaviorEffect` {#table-behavioreffect}

Visual, audio, camera, render, motion, and mesh effect definitions referenced by behaviors.

**Columns:** `effectID`, `effectType`, `effectName`, `trailID`, `pcreateDuration`, `animationName`, `attachToObject`, `boneName`, `useSecondary`, `cameraEffectType`, `cameraDuration`, `cameraFrequency`, `cameraXAmp`, `cameraYAmp`, `cameraZAmp`, `cameraRotFrequency`, `cameraRoll`, `cameraPitch`, `cameraYaw`, `AudioEventGUID`, `renderEffectType`, `renderEffectTime`, `renderStartVal`, `renderEndVal`, `renderDelayVal`, `renderValue1`, `renderValue2`, `renderValue3`, `renderRGBA`, `renderShaderVal`, `motionID`, `meshID`, `meshDuration`, `meshLockedNode`

### `BehaviorParameter` {#table-behaviorparameter}

Named/numbered parameter values keyed by behavior ID.

**Columns:** `behaviorID`, `parameterID`, `value`

### `BehaviorTemplate` {#table-behaviortemplate}

Behavior ID to template/effect mapping used by the behavior interpreter.

**Columns:** `behaviorID`, `templateID`, `effectID`, `effectHandle`

### `BehaviorTemplateName` {#table-behaviortemplatename}

Human-readable names for behavior template IDs.

**Columns:** `templateID`, `name`

### `BuffDefinitions` {#table-buffdefinitions}

Buff IDs and their priority/UI icon metadata.

**Columns:** `ID`, `Priority`, `UIIcon`

### `BuffParameters` {#table-buffparameters}

Numeric, string, and effect parameters associated with buffs.

**Columns:** `BuffID`, `ParameterName`, `NumberValue`, `StringValue`, `EffectID`

### `DevModelBehaviors` {#table-devmodelbehaviors}

Development model-to-behavior associations; empty in this snapshot.

**Columns:** `ModelID`, `BehaviorID`

### `LevelProgressionLookup` {#table-levelprogressionlookup}

Progression thresholds and associated behavior effects.

**Columns:** `id`, `requiredUScore`, `BehaviorEffect`

### `ModelBehavior` {#table-modelbehavior}

Model behavior records pointing to behavior-definition XML files.

**Columns:** `id`, `definitionXMLfilename`

### `ObjectBehaviors` {#table-objectbehaviors}

Behavior XML data keyed by behavior ID.

**Columns:** `BehaviorID`, `xmldata`

### `ObjectBehaviorXREF` {#table-objectbehaviorxref}

Intended LOT-to-behavior cross-reference table; empty in this snapshot.

**Columns:** `LOT`, `behaviorID1`, `behaviorID2`, `behaviorID3`, `behaviorID4`, `behaviorID5`, `type`

### `ObjectSkills` {#table-objectskills}

Associates object templates with skills and cast-context/AI-weight information.

**Columns:** `objectTemplate`, `skillID`, `castOnType`, `AICombatWeight`

### `PlayerFlags` {#table-playerflags}

Player flag definitions, including session and zone scope.

**Columns:** `id`, `SessionOnly`, `OnlySetByServer`, `SessionZoneOnly`

### `PlayerStatistics` {#table-playerstatistics}

Player-statistic identifiers and display ordering.

**Columns:** `statID`, `sortOrder`, `locStatus`, `gate_version`

### `Preconditions` {#table-preconditions}

Reusable requirement checks referencing target LOTs/groups/counts and valid contexts.

**Columns:** `id`, `type`, `targetLOT`, `targetGroup`, `targetCount`, `iconID`, `localize`, `validContexts`, `locStatus`, `gate_version`

### `SkillBehavior` {#table-skillbehavior}

Skill roots and settings such as cooldowns, cast type, cost, and UI bonuses.

**Columns:** `skillID`, `locStatus`, `behaviorID`, `imaginationcost`, `cooldowngroup`, `cooldown`, `inNpcEditor`, `skillIcon`, `oomSkillID`, `oomBehaviorEffectID`, `castTypeDesc`, `imBonusUI`, `lifeBonusUI`, `armorBonusUI`, `damageUI`, `hideIcon`, `localize`, `gate_version`, `cancelType`

## Vehicles, movement, and control

### `Camera` {#table-camera}

Camera follow, zoom, pitch/yaw, movement, collision, and field-of-view tuning.

**Columns:** `camera_name`, `pitch_angle_tolerance`, `starting_zoom`, `zoom_return_modifier`, `pitch_return_modifier`, `tether_out_return_modifier`, `tether_in_return_multiplier`, `verticle_movement_dampening_modifier`, `return_from_incline_modifier`, `horizontal_return_modifier`, `yaw_behavior_speed_multiplier`, `camera_collision_padding`, `glide_speed`, `fade_player_min_range`, `min_movement_delta_tolerance`, `min_glide_distance_tolerance`, `look_forward_offset`, `look_up_offset`, `minimum_vertical_dampening_distance`, `maximum_vertical_dampening_distance`, `minimum_ignore_jump_distance`, `maximum_ignore_jump_distance`, `maximum_auto_glide_angle`, `minimum_tether_glide_distance`, `yaw_sign_correction`, `set_1_look_forward_offset`, `set_1_look_up_offset`, `set_2_look_forward_offset`, `set_2_look_up_offset`, `set_0_speed_influence_on_dir`, `set_1_speed_influence_on_dir`, `set_2_speed_influence_on_dir`, `set_0_angular_relaxation`, `set_1_angular_relaxation`, `set_2_angular_relaxation`, `set_0_position_up_offset`, `set_1_position_up_offset`, `set_2_position_up_offset`, `set_0_position_forward_offset`, `set_1_position_forward_offset`, `set_2_position_forward_offset`, `set_0_FOV`, `set_1_FOV`, `set_2_FOV`, `set_0_max_yaw_angle`, `set_1_max_yaw_angle`, `set_2_max_yaw_angle`, `set_1_fade_in_camera_set_change`, `set_1_fade_out_camera_set_change`, `set_2_fade_in_camera_set_change`, `set_2_fade_out_camera_set_change`, `input_movement_scalar`, `input_rotation_scalar`, `input_zoom_scalar`, `minimum_pitch_desired`, `maximum_pitch_desired`, `minimum_zoom`, `maximum_zoom`, `horizontal_rotate_tolerance`, `horizontal_rotate_modifier`

### `ControlSchemes` {#table-controlschemes}

Keyboard/gamepad movement, rotation, zoom, and free-camera sensitivity settings.

**Columns:** `control_scheme`, `scheme_name`, `rotation_speed`, `walk_forward_speed`, `walk_backward_speed`, `walk_strafe_speed`, `walk_strafe_forward_speed`, `walk_strafe_backward_speed`, `run_backward_speed`, `run_strafe_speed`, `run_strafe_forward_speed`, `run_strafe_backward_speed`, `keyboard_zoom_sensitivity`, `keyboard_pitch_sensitivity`, `keyboard_yaw_sensitivity`, `mouse_zoom_wheel_sensitivity`, `x_mouse_move_sensitivity_modifier`, `y_mouse_move_sensitivity_modifier`, `freecam_speed_modifier`, `freecam_slow_speed_multiplier`, `freecam_fast_speed_multiplier`, `freecam_mouse_modifier`, `gamepad_pitch_rot_sensitivity`, `gamepad_yaw_rot_sensitivity`, `gamepad_trigger_sensitivity`

### `MovingPlatforms` {#table-movingplatforms}

Moving-platform motion vectors, duration, start direction, and description.

**Columns:** `id`, `platformIsSimpleMover`, `platformMoveX`, `platformMoveY`, `platformMoveZ`, `platformMoveTime`, `platformStartAtEnd`, `description`

### `RacingModuleComponent` {#table-racingmodulecomponent}

Racing module performance values such as speed, acceleration, handling, stability, and imagination.

**Columns:** `id`, `topSpeed`, `acceleration`, `handling`, `stability`, `imagination`

### `RailActivatorComponent` {#table-railactivatorcomponent}

Rail activation animation, sound/effect, collision, camera, damage, and precondition settings.

**Columns:** `id`, `startAnim`, `loopAnim`, `stopAnim`, `startSound`, `loopSound`, `stopSound`, `effectIDs`, `preconditions`, `playerCollision`, `cameraLocked`, `StartEffectID`, `StopEffectID`, `DamageImmune`, `NoAggro`, `ShowNameBillboard`

### `RocketLaunchpadControlComponent` {#table-rocketlaunchpadcontrolcomponent}

Rocket launch destination, animation/audio, landing, and precondition settings.

**Columns:** `id`, `targetZone`, `defaultZoneID`, `targetScene`, `gmLevel`, `playerAnimation`, `rocketAnimation`, `launchMusic`, `useLaunchPrecondition`, `useAltLandingPrecondition`, `launchPrecondition`, `altLandingPrecondition`, `altLandingSpawnPointName`

### `SurfaceType` {#table-surfacetype}

Surface identifiers mapped to footstep audio metadata.

**Columns:** `SurfaceType`, `FootstepNDAudioMetaEventSetName`

### `VehiclePhysics` {#table-vehiclephysics}

Vehicle physics and handling parameters, including chassis, tires, steering, boost, collision, and audio.

**Columns:** `id`, `hkxFilename`, `fGravityScale`, `fMass`, `fChassisFriction`, `fMaxSpeed`, `fEngineTorque`, `fBrakeFrontTorque`, `fBrakeRearTorque`, `fBrakeMinInputToBlock`, `fBrakeMinTimeToBlock`, `fSteeringMaxAngle`, `fSteeringSpeedLimitForMaxAngle`, `fSteeringMinAngle`, `fFwdBias`, `fFrontTireFriction`, `fRearTireFriction`, `fFrontTireFrictionSlide`, `fRearTireFrictionSlide`, `fFrontTireSlipAngle`, `fRearTireSlipAngle`, `fWheelWidth`, `fWheelRadius`, `fWheelMass`, `fReorientPitchStrength`, `fReorientRollStrength`, `fSuspensionLength`, `fSuspensionStrength`, `fSuspensionDampingCompression`, `fSuspensionDampingRelaxation`, `iChassisCollisionGroup`, `fNormalSpinDamping`, `fCollisionSpinDamping`, `fCollisionThreshold`, `fTorqueRollFactor`, `fTorquePitchFactor`, `fTorqueYawFactor`, `fInertiaRoll`, `fInertiaPitch`, `fInertiaYaw`, `fExtraTorqueFactor`, `fCenterOfMassFwd`, `fCenterOfMassUp`, `fCenterOfMassRight`, `fWheelHardpointFrontFwd`, `fWheelHardpointFrontUp`, `fWheelHardpointFrontRight`, `fWheelHardpointRearFwd`, `fWheelHardpointRearUp`, `fWheelHardpointRearRight`, `fInputTurnSpeed`, `fInputDeadTurnBackSpeed`, `fInputAccelSpeed`, `fInputDeadAccelDownSpeed`, `fInputDecelSpeed`, `fInputDeadDecelDownSpeed`, `fInputSlopeChangePointX`, `fInputInitialSlope`, `fInputDeadZone`, `fAeroAirDensity`, `fAeroFrontalArea`, `fAeroDragCoefficient`, `fAeroLiftCoefficient`, `fAeroExtraGravity`, `fBoostTopSpeed`, `fBoostCostPerSecond`, `fBoostAccelerateChange`, `fBoostDampingChange`, `fPowerslideNeutralAngle`, `fPowerslideTorqueStrength`, `iPowerslideNumTorqueApplications`, `fImaginationTankSize`, `fSkillCost`, `fWreckSpeedBase`, `fWreckSpeedPercent`, `fWreckMinAngle`, `AudioEventEngine`, `AudioEventSkid`, `AudioEventLightHit`, `AudioSpeedThresholdLightHit`, `AudioTimeoutLightHit`, `AudioEventHeavyHit`, `AudioSpeedThresholdHeavyHit`, `AudioTimeoutHeavyHit`, `AudioEventStart`, `AudioEventTreadConcrete`, `AudioEventTreadSand`, `AudioEventTreadWood`, `AudioEventTreadDirt`, `AudioEventTreadPlastic`, `AudioEventTreadGrass`, `AudioEventTreadGravel`, `AudioEventTreadMud`, `AudioEventTreadWater`, `AudioEventTreadSnow`, `AudioEventTreadIce`, `AudioEventTreadMetal`, `AudioEventTreadLeaves`, `AudioEventLightLand`, `AudioAirtimeForLightLand`, `AudioEventHeavyLand`, `AudioAirtimeForHeavyLand`, `bWheelsVisible`

### `VehicleStatMap` {#table-vehiclestatmap}

Maps module stats to Havok vehicle-physics stats and per-module changes.

**Columns:** `id`, `ModuleStat`, `HavokStat`, `HavokChangePerModuleStat`

## Zones, properties, and world configuration

### `LUPZoneIDs` {#table-lupzoneids}

Zone IDs identified as LUP-related in this dataset.

**Columns:** `zoneID`

### `PropertyEntranceComponent` {#table-propertyentrancecomponent}

Property entrance component records, including map, property name, and group type.

**Columns:** `id`, `mapID`, `propertyName`, `isOnProperty`, `groupType`

### `PropertyTemplate` {#table-propertytemplate}

Static property templates with map/zone, pricing, duration, clone, spawn, and build-height settings.

**Columns:** `id`, `mapID`, `vendorMapID`, `spawnName`, `type`, `sizecode`, `minimumPrice`, `rentDuration`, `path`, `cloneLimit`, `durationType`, `achievementRequired`, `zoneX`, `zoneY`, `zoneZ`, `maxBuildHeight`, `localize`, `reputationPerMinute`, `locStatus`, `gate_version`

### `SceneTable` {#table-scenetable}

Scene IDs and scene names.

**Columns:** `sceneID`, `sceneName`

### `WorldConfig` {#table-worldconfig}

World-wide gameplay defaults and tuning values, including movement, death, property, mail, and progression settings.

**Columns:** `WorldConfigID`, `pegravityvalue`, `pebroadphaseworldsize`, `pegameobjscalefactor`, `character_rotation_speed`, `character_walk_forward_speed`, `character_walk_backward_speed`, `character_walk_strafe_speed`, `character_walk_strafe_forward_speed`, `character_walk_strafe_backward_speed`, `character_run_backward_speed`, `character_run_strafe_speed`, `character_run_strafe_forward_speed`, `character_run_strafe_backward_speed`, `global_cooldown`, `characterGroundedTime`, `characterGroundedSpeed`, `globalImmunityTime`, `character_max_slope`, `defaultrespawntime`, `mission_tooltip_timeout`, `vendor_buy_multiplier`, `pet_follow_radius`, `character_eye_height`, `flight_vertical_velocity`, `flight_airspeed`, `flight_fuel_ratio`, `flight_max_airspeed`, `fReputationPerVote`, `nPropertyCloneLimit`, `defaultHomespaceTemplate`, `coins_lost_on_death_percent`, `coins_lost_on_death_min`, `coins_lost_on_death_max`, `character_votes_per_day`, `property_moderation_request_approval_cost`, `property_moderation_request_review_cost`, `propertyModRequestsAllowedSpike`, `propertyModRequestsAllowedInterval`, `propertyModRequestsAllowedTotal`, `propertyModRequestsSpikeDuration`, `propertyModRequestsIntervalDuration`, `modelModerateOnCreate`, `defaultPropertyMaxHeight`, `reputationPerVoteCast`, `reputationPerVoteReceived`, `showcaseTopModelConsiderationBattles`, `reputationPerBattlePromotion`, `coins_lost_on_death_min_timeout`, `coins_lost_on_death_max_timeout`, `mail_base_fee`, `mail_percent_attachment_fee`, `propertyReputationDelay`, `LevelCap`, `LevelUpBehaviorEffect`, `CharacterVersion`, `LevelCapCurrencyConversion`

### `ZoneLoadingTips` {#table-zoneloadingtips}

Zone-specific loading-tip localization and weighting data.

**Columns:** `id`, `zoneid`, `imagelocation`, `localize`, `gate_version`, `locStatus`, `weight`, `targetVersion`

### `ZoneSummary` {#table-zonesummary}

Zone summary values keyed by zone and type.

**Columns:** `zoneID`, `type`, `value`, `_uniqueID`

### `ZoneTable` {#table-zonetable}

Zone configuration including names, scripts, population/physics settings, map folders, and feature flags.

**Columns:** `zoneID`, `locStatus`, `zoneName`, `scriptID`, `ghostdistance_min`, `ghostdistance`, `population_soft_cap`, `population_hard_cap`, `DisplayDescription`, `mapFolder`, `smashableMinDistance`, `smashableMaxDistance`, `mixerProgram`, `clientPhysicsFramerate`, `serverPhysicsFramerate`, `zoneControlTemplate`, `widthInChunks`, `heightInChunks`, `petsAllowed`, `localize`, `fZoneWeight`, `thumbnail`, `PlayerLoseCoinsOnDeath`, `disableSaveLoc`, `teamRadius`, `gate_version`, `mountsAllowed`
