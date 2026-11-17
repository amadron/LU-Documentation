# Item Database — Methodology and Evidence

[Item database](./README.md)

Generated: **2026-11-17T09:32:48.349Z**. Server source revision: `8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4`. Static data comes from the supplied local CDClient FDB, exported into [db](../../db/README.md); this is not a query of a running server or the per-player runtime database.

## Scope and trust levels

1. **Template metadata:** 6832 ITEM component registrations (type 11), with Objects and ItemComponent metadata. Missing object rows and descriptions are retained explicitly. Raw client descriptions may be technical; no missing lore was generated. Localized tooltips/mission titles were not available in a locale.xml file.
2. **Static acquisition associations:** LootMatrix → LootTable → item LOT, linked to destructibles, packages, vendors, ActivityRewards, mission/achievement rewards, MissionEmail, and RewardCodes. A definition is a candidate route, not a claim of live availability.
3. **Map evidence:** exact normalized ZoneTable zoneName asset paths, parsed LUZ scene references, LVL object placements, LOT 176 spawntemplate settings, and LUZ spawner waypoints. Embedded world IDs are not used to invent zone matches. Source pages preserve XYZ, origin, feature gates, inactive-on-load spawners, and vendorInvOverride. Client-only placements are excluded. Not every waypoint spawns an independent entity; never interpret record counts as population or simultaneous spawn counts.
4. **Community facts:** separately labeled historical acquisition methods and named references, linked to fixed public wiki revisions. They do not override the local static snapshot.

## Probability model

The model follows the global `Loot::RollLootMatrix` routine in [Loot.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/Loot.cpp), [loot-table sorting](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dDatabase/CDClientDatabase/CDClientTables/CDLootTableTable.cpp), and [rarity-table loading](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dDatabase/CDClientDatabase/CDClientTables/CDRarityTableTable.cpp).

For each independent matrix entry:

- Trigger probability is `percent`, constrained to the random draw domain [0,1].
- Drop count N is a uniform integer from minToDrop to maxToDrop, inclusive.
- A uniform rarity roll is resolved against descending randmax thresholds, defaulting to rarity 1. The server walks the loot rows in descending rarity order. An exact match locks the rarity class; otherwise a lower-rarity row is added and becomes the new comparison rarity. The model preserves an implementation quirk: if a fallback class has only one row, the loop can also include rows from still-lower classes until a subsequent equality locks the class. It does not replace this loop with an idealized "highest lower class only" rule. No eligible row means no item.
- Each eligible loot-table row has equal weight; duplicate rows for the same LOT keep their multiplicity. Missing item-component metadata has the server's zero rarity default, not an invented ordinary rarity.
- If q is the item's per-draw probability, the entry's no-hit probability is `1 - p + p * average((1-q)^N)`.
- Across entries, `P(at least one) = 1 - product(entry_no_hit)`; expected counts add as `sum(p * mean(N) * q)`.

Percentages are **modeled pre-filter probabilities per matrix invocation**, not universal per-player drop rates or chances per random enemy kill. The mean is an expected count, not a second percentage. Discrete floating-point RNG endpoints and rounding can produce tiny differences from the continuous-threshold model. No empirical drop-rate measurements were made.

Mission-drop filtering, player mission eligibility, team distribution, ownership/range, scripts, and source-specific overrides can change actual receipt. Matrix flagID/gate_version are preserved, but the inspected generic roll routine does not use them to apply a player flag or feature gate. Other loaders and gameplay paths may still restrict availability.

Faction token LOT 13763 is a proxy, not an ordinary obtainable token: the player-aware loot path substitutes Assembly 8318 (mission 545), Venture 8321 (556), Sentinel 8319 (567), or Paradox 8320 (578), according to the completed faction-join check; without a faction it discards the proxy. The faction-token pages link this conditional source. The raw source-rates CSV retains the proxy LOT rather than pretending all factions receive all four tokens.

### Invalid generic ranges

54 matrices contain at least one reversed count range (maxToDrop < minToDrop). Generic loot probability is left undefined for the entire affected matrix. This is not assumed to be a zero drop chance or corrected silently. Many such rows are vendor inventory definitions with maxToDrop=0, which the vendor code handles differently.

Source definitions also reference four indexes without any LootMatrix rows
in this snapshot: [36](./sources/matrix-36.md), [209](./sources/matrix-209.md),
[359](./sources/matrix-359.md), and [828](./sources/matrix-828.md). Their source
links are retained on explicit missing-definition pages; no contents or rates
are invented for them.

## Vendor stock is not a drop rate

[VendorComponent.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dComponents/VendorComponent.cpp) refreshes stock separately. With either count endpoint equal to zero, all rows of that loot table are included. Otherwise it chooses an inclusive random count and samples row indices without replacement, stopping when the table is exhausted. For k occurrences of an item among n rows and s sampled rows, the no-stock probability is `C(n-k,s)/C(n,s)`; average over counts and combine independent matrix entries. Trigger percent and rarity weights are not used in this inventory-selection loop.

These are modeled **pre-filter default-stock probabilities per refresh**, not transaction or purchase success rates. SetupItem validation, scene vendorInvOverride, the vendor's HandleMrReeCameras filter, custom scripts, costs, flags, and live inventory state can restrict the result. Explicit local vendorInvOverride items are listed separately on item pages; the inspected server parses that setting as comma-separated LOTs. Default-stock location summaries exclude placements that explicitly override the inventory, including an explicitly empty override. BaseValue is not a final vendor price.

## Resolving named sources and rewards

- [Entity.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/Entity.cpp): destructible component selection uses collectible (23), overridden by quick-build (48), overridden by historical BUFF (7). A positive BUFF/collectible registration or scene is_smashable is required; quick-build registration alone is not declared an enemy drop source. Scene-only cases are marked on their source pages.
- Package component 53 links package LOTs to matrices. Follow the package's own item page to investigate how to obtain the containing package; its contents are not necessarily world drops.
- Vendor component 16 links sellers to default stock. Scene inventory overrides are extracted separately.
- ActivityRewards.objectTemplate is treated as an **activity ID**, not automatically as a source object LOT. A reward applies only when its rating threshold is the highest eligible one. SCRIPTED_ACTIVITY (39) registrations provide candidate object links where available; Activities.instanceMapID is recorded where present. Script-created activities and custom loot calls may not have such a static link.
- Mission rewards distinguish first completion, repeats, and choice rewards. A zero stored reward count is displayed as one according to the reward handler. Conditions, repeatability, preconditions, and feature gates can still prevent a reward. IDs and type/subtype are shown because localized quest titles are unavailable.
- MissionNPC component 73 and mission offer/target LOTs supply associated quest NPC candidates, not guaranteed active quest markers. Mission mail requires its actual mail trigger. A RewardCodes definition does not establish that a historical promotion remains redeemable.

## Public community research

Read-only requests used the standard MediaWiki API at `https://legouniverse.fandom.com/api.php`. No local client files or server source were uploaded. Acquisition-table item names were normalized and matched **only when the local name was unique**; ambiguous and unmatched names were excluded. These matches identify historical community claims, not verified LOT mappings. Only factual acquisition categories and named references were extracted; article prose was not reproduced. A blank community section means “not matched in this bounded research,” not “the Internet has no information.”

| Public page | Revision | Revision timestamp | Matched item LOTs | Retrieved |
| --- | --- | --- | --- | --- |
| [Weapons](https://legouniverse.fandom.com/wiki/Weapons?oldid=163946) | 163946 | 2024-08-02T18:42:44Z | 157 | 2026-11-17T09:23:11.199Z |
| [Headgear](https://legouniverse.fandom.com/wiki/Headgear?oldid=164262) | 164262 | 2025-12-11T00:36:13Z | 90 | 2026-11-17T09:23:11.740Z |
| [Neck Items](https://legouniverse.fandom.com/wiki/Neck_Items?oldid=161377) | 161377 | 2021-09-25T04:26:03Z | 37 | 2026-11-17T09:23:12.264Z |
| [Left-Hand Items](https://legouniverse.fandom.com/wiki/Left-Hand_Items?oldid=163215) | 163215 | 2021-12-01T20:34:32Z | 41 | 2026-11-17T09:23:12.807Z |
| [Shirts](https://legouniverse.fandom.com/wiki/Shirts?oldid=163412) | 163412 | 2022-06-28T18:53:23Z | 102 | 2026-11-17T09:23:13.329Z |
| [Pants](https://legouniverse.fandom.com/wiki/Pants?oldid=164250) | 164250 | 2025-10-13T13:14:50Z | 28 | 2026-11-17T09:23:13.844Z |
| [Consumable](https://legouniverse.fandom.com/wiki/Consumable?oldid=164121) | 164121 | 2025-03-09T03:39:28Z | 54 | 2026-11-17T09:23:14.403Z |
| [Other Items](https://legouniverse.fandom.com/wiki/Other_Items?oldid=161549) | 161549 | 2021-11-14T06:03:36Z | 0 | 2026-11-17T09:23:14.916Z |
| [Faction Gear](https://legouniverse.fandom.com/wiki/Faction_Gear?oldid=163921) | 163921 | 2024-06-23T23:33:22Z | 0 | 2026-11-17T09:23:15.460Z |
| [Specialties](https://legouniverse.fandom.com/wiki/Specialties?oldid=163848) | 163848 | 2023-08-13T06:05:39Z | 17 | 2026-11-17T09:23:15.974Z |
| [Ninjago Items](https://legouniverse.fandom.com/wiki/Ninjago_Items?oldid=163250) | 163250 | 2022-01-06T03:10:42Z | 117 | 2026-11-17T09:23:16.494Z |
| [Package](https://legouniverse.fandom.com/wiki/Package?oldid=161666) | 161666 | 2021-11-16T17:53:21Z | 0 | 2026-11-17T09:23:17.042Z |
| [Everlasting Items](https://legouniverse.fandom.com/wiki/Everlasting_Items?oldid=132116) | 132116 | 2012-07-15T19:42:53Z | 0 | 2026-11-17T09:23:17.626Z |
| [Valiant Gear](https://legouniverse.fandom.com/wiki/Valiant_Gear?oldid=164194) | 164194 | 2025-04-23T16:40:26Z | 0 | 2026-11-17T09:23:18.157Z |
| [Items](https://legouniverse.fandom.com/wiki/Items?oldid=163260) | 163260 | 2022-01-10T18:43:49Z | 4 | 2026-11-17T09:23:18.681Z |
| [Mounts](https://legouniverse.fandom.com/wiki/Mounts?oldid=163459) | 163459 | 2022-07-06T01:47:33Z | 0 | 2026-11-17T09:23:19.394Z |
| [Promotional Items](https://legouniverse.fandom.com/wiki/Promotional_Items?oldid=153579) | 153579 | 2013-06-02T17:23:00Z | 0 | 2026-11-17T09:23:19.922Z |

The 17 pages yielded facts for 647 unique item LOTs; counts per page overlap. `luwiki.lu` could not be resolved and LU-Explorer reported unavailability during this work, so neither was used to fill missing facts.

## Map coverage and unresolved files

39 LUZ assets were parsed, 34 matched at least one ZoneTable asset path. 536 distinct referenced LVL files from matched maps parsed successfully; 0 failed. 10760 direct object records and 4494 spawner waypoint records were read for matched map processing, before source filtering. 1122 client-only placement candidates were excluded. See [Coverage.json](./Coverage.json) for exact counts and errors.

No unresolved referenced levels.

One object in `maps/01_live_maps/wbl/deep_freeze_intro/wbl_deep_freeze_intro.lvl`
has non-finite XYZ coordinates: LOT **5632**, zone **1601**. Only this placement
was excluded; all 226 object records in that level were parsed, and the valid
placements were retained. The excluded record is listed in
[Coverage.json](./Coverage.json). Non-finite coordinates were not converted to
zero or published as a usable location.

### LUZ assets without a ZoneTable path match

| Asset | Embedded world ID (not assumed to be a valid zone mapping) |
| --- | --- |
| maps/01&#95;live&#95;maps/gnarled&#95;forest/survival/nd&#95;gf&#95;survival&#95;trench.luz | 58001 |
| maps/earthgauntlet/earthgauntlet.luz | 2100 |
| maps/earthgauntlet/nd&#95;nj&#95;earth.luz | 2100 |
| maps/seasonal&#95;live maps/december/ns&#95;winter&#95;racetrack/nd&#95;nimbus&#95;station&#95;winter-racetrack.luz | 1261 |
| maps/seasonal&#95;live maps/december/winter&#95;celebrity&#95;property/ns&#95;property&#95;large&#95;winter.luz | 1260 |

## Remaining limitations

This is not an exhaustive audit of every server Lua/C++ script, scripted item grant, crafting recipe, pet reward, minigame custom payout, trading path, event configuration, or runtime vendor override. It does not prove reachability, feature enablement, player eligibility, or whether legacy/test items still exist on a deployed server. Coordinates are static map coordinates, not navigation instructions. Failed/unmatched map assets are not counted as evidence of absence.

The database deliberately preserves unknown descriptions, unresolved consumers, missing placements, and invalid probability inputs instead of inventing farming instructions. All 6832 pages exist even where no supported source was found. Type indexes are paginated; item and source-rate CSVs support full-data filtering. Percentages in CSV are fractions (0–1); blanks mean not applicable/undefined.

## Validation performed

- Verified all 6,832 LOT pages against the source item catalog, without
  duplicates or omissions.
- Compared all 2,628 populated client descriptions with the source data.
- Validated 87,033 matrix/item rate records for numeric bounds, unique keys,
  undefined reversed ranges, and separation of vendor stock from loot chance.
- Checked more than 405,000 local Markdown links: no broken targets.
  The largest generated Markdown page is 208,225 bytes; item-type indexes
  contain no more than 200 items each.
- Passed seven focused tests covering CSV fidelity, rarity thresholds,
  duplicate row weighting, the singleton-fallback quirk, inclusive draw counts,
  independent matrix entries, vendor sampling, and malformed map coordinates.
- Independently simulated the literal server loop for 100,000 trials each:
  matrix 335 / LOT 8318 modeled 68.359375%, simulated 68.335%;
  matrix 620 / LOT 1883 modeled 10.26939174%, simulated 10.268%.
  These simulations validate the calculation, not actual in-game availability
  or measured player drop rates.
