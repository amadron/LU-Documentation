# LEGO Universe Item Database

[Game Guide](../README.md) | [Item Guide](../Item%20Guide.md) | [Quest Guide](../Quest%20Guide.md)

## Find an item

Looking for an item to use in game? Start with the [Item Guide](../Item%20Guide.md),
then search the [flat item list](../../LEGO%20Universe%20Item%20List.md) or
browse this database by item type. Open an item's page to follow its possible
sources and location evidence.

This is the detailed reference behind the flat item list. The quick list
shows names and basic fields; these pages add possible sources, rewards,
locations, and evidence. Both cover item templates, not a live check of what
is currently available in your game.

For the player-facing mission steps behind an item reward, use the
[Quest Guide](../Quest%20Guide.md) or [quest database](../quests/README.md).

[Quest and Achievement Database](../quests/README.md): look up mission IDs
from item reward tables for objectives, requirements, and quest-giver locations.

**All 6,832 registered item templates have individual detail pages.** Find an item by type below, open its page, and follow a named source for reward definitions and mapped locations. If you already know its LOT (template number), open `<LOT>.md` in this directory.

Every page distinguishes client descriptions, source-specific modeled loot chances, vendor stock, conditional quest rewards, and historical community references. Missing evidence is shown explicitly; unused/test templates remain included.

## Browse by item type

Each index contains at most 200 items so it remains practical to read in GitLab. Use browser Find within an index, or the CSV for a full-database name search. Type names are raw database categories, not promises of player usability.

| Item type | Items | Index pages |
| --- | --- | --- |
| Unknown (0) | 36 | [1](types/type-0-1.md) |
| Brick | 1921 | [1](types/type-1-1.md) · [2](types/type-1-2.md) · [3](types/type-1-3.md) · [4](types/type-1-4.md) · [5](types/type-1-5.md) · [6](types/type-1-6.md) · [7](types/type-1-7.md) · [8](types/type-1-8.md) · [9](types/type-1-9.md) · [10](types/type-1-10.md) |
| Hat | 377 | [1](types/type-2-1.md) · [2](types/type-2-2.md) |
| Hair | 7 | [1](types/type-3-1.md) |
| Neck | 253 | [1](types/type-4-1.md) · [2](types/type-4-2.md) |
| Left hand | 249 | [1](types/type-5-1.md) · [2](types/type-5-2.md) |
| Right hand | 517 | [1](types/type-6-1.md) · [2](types/type-6-2.md) · [3](types/type-6-3.md) |
| Legs | 202 | [1](types/type-7-1.md) · [2](types/type-7-2.md) |
| Left trinket | 1 | [1](types/type-8-1.md) |
| Right trinket | 1 | [1](types/type-9-1.md) |
| Behavior | 83 | [1](types/type-10-1.md) |
| Property | 2 | [1](types/type-11-1.md) |
| Model | 20 | [1](types/type-12-1.md) |
| Collectible | 34 | [1](types/type-13-1.md) |
| Consumable | 284 | [1](types/type-14-1.md) · [2](types/type-14-2.md) |
| Chest | 1018 | [1](types/type-15-1.md) · [2](types/type-15-2.md) · [3](types/type-15-3.md) · [4](types/type-15-4.md) · [5](types/type-15-5.md) · [6](types/type-15-6.md) |
| Egg | 2 | [1](types/type-16-1.md) |
| Pet food | 1 | [1](types/type-17-1.md) |
| Quest object | 41 | [1](types/type-18-1.md) |
| Pet inventory item | 31 | [1](types/type-19-1.md) |
| Package | 166 | [1](types/type-20-1.md) |
| Loot model | 1531 | [1](types/type-21-1.md) · [2](types/type-21-2.md) · [3](types/type-21-3.md) · [4](types/type-21-4.md) · [5](types/type-21-5.md) · [6](types/type-21-6.md) · [7](types/type-21-7.md) · [8](types/type-21-8.md) |
| Vehicle | 44 | [1](types/type-22-1.md) |
| Mount | 11 | [1](types/type-24-1.md) |

## Locations and downloads

- [Mapped source locations](./locations/README.md): zones → sellers/enemies/quest NPCs → coordinates and source definitions.
- [Item summary CSV](./Item%20Summary.csv): all LOTs, full client descriptions, and evidence counts.
- [Source rates CSV](./Source%20Rates.csv): numeric probabilities on a 0–1 scale; blank means not applicable or undefined, not zero.
- [Methodology, sources, and limitations](./Methodology.md).
- [Machine-readable coverage report](./Coverage.json).

## Coverage in this snapshot

| Evidence | Item / record count |
| --- | ---: |
| Individual item pages | 6832 |
| Items with a client object description | 2628 |
| Items without an Objects row | 357 |
| Items with a qualifying static matrix/vendor association | 4609 |
| Items with a mission/achievement/mail/code reward association | 696 |
| Items with conservative community acquisition matches | 647 |
| Source LOTs with mapped placement candidates | 510 |
| Successfully parsed referenced level files | 536 |
| Referenced level parse failures | 0 |
| Excluded placements with non-finite coordinates | 1 |

Evidence counts overlap. A description or table association is **not proof that an item is obtainable**. Rates are per matrix invocation, not globally per kill; eligibility and scripts still apply. The generic loot model is not assigned to vendor-only reversed count ranges.
