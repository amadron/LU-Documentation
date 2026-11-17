# LEGO Universe Quest and Achievement Database

[Game Guide](../README.md) | [Quest Guide](../Quest%20Guide.md) | [Item Database](../items/README.md)

## Start with the player guide

To play a mission, follow the objectives in your in-game journal. The
[Quest Guide](../Quest%20Guide.md) explains accepting missions, completing
objectives, turning them in, and what to check when progress is blocked.
Use this database when you want to look up a particular mission or achievement.

Related activity references: [Racing Database](../racing/README.md) |
[Pet Database](../pets/README.md). These supplement the quest objectives with
activity-specific mechanics and source/location evidence.

**682 quests and 745 achievements have individual reference pages.** Each
page gives the official client texts where available, character associations, possible
locations, prerequisites, objectives, and rewards.

This is a lookup collection, not a live-server journal. Some entries are
legacy, test, or otherwise unavailable. Where client story text or steps
are missing, the pages say so rather than guessing.

## Browse all definitions

- **Quests**, in numeric ID order — pages: [1](indexes/quests-1.md) | [2](indexes/quests-2.md) | [3](indexes/quests-3.md) | [4](indexes/quests-4.md) | [5](indexes/quests-5.md) | [6](indexes/quests-6.md) | [7](indexes/quests-7.md)
- **Achievements**, in numeric ID order — pages: [1](indexes/achievements-1.md) | [2](indexes/achievements-2.md) | [3](indexes/achievements-3.md) | [4](indexes/achievements-4.md) | [5](indexes/achievements-5.md) | [6](indexes/achievements-6.md) | [7](indexes/achievements-7.md) | [8](indexes/achievements-8.md)
- [NPC / associated-object index](./NPC%20Index.md).
- [Zone and location index](./locations/README.md).
- [Full quest summary CSV](./Quest%20Summary.csv) for name/ID search and filtering.
- [Objective reference CSV](./Objective%20Reference.csv) for all 1800 attached objective rows, with typed target namespaces.

If you know the ID, open `<ID>.md` in this directory. Titles are the official English client names from locale.xml; definitions without a client name keep a marked community candidate title or a numeric placeholder. Numeric IDs remain stable lookup keys.

## Browse by passport category / region

Category labels are source data, not verified starting locations. Each index page contains at most 100 definitions.

| Category / subcategory | Quests | Achievements | Index pages |
| --- | --- | --- | --- |
| Battle / General | 0 | 27 | [1](indexes/group-1-1.md) |
| Battle / Nimbus Instance | 0 | 25 | [1](indexes/group-2-1.md) |
| Battle / Survival Games | 0 | 17 | [1](indexes/group-3-1.md) |
| Battle / Venture Instance | 6 | 9 | [1](indexes/group-4-1.md) |
| Build / No subtype | 0 | 31 | [1](indexes/group-5-1.md) |
| Events / Winter | 0 | 18 | [1](indexes/group-6-1.md) |
| General / No subtype | 0 | 98 | [1](indexes/group-7-1.md) |
| Hidden / Hidden | 253 | 54 | [1](indexes/group-8-1.md) &#124; [2](indexes/group-8-2.md) &#124; [3](indexes/group-8-3.md) &#124; [4](indexes/group-8-4.md) |
| Location / Avant Gardens | 51 | 43 | [1](indexes/group-9-1.md) |
| Location / Crux Prime | 25 | 93 | [1](indexes/group-10-1.md) &#124; [2](indexes/group-10-2.md) |
| Location / Forbidden Valley | 32 | 39 | [1](indexes/group-11-1.md) |
| Location / Gnarled Forest | 30 | 57 | [1](indexes/group-12-1.md) |
| Location / Nexus Tower | 90 | 40 | [1](indexes/group-13-1.md) &#124; [2](indexes/group-13-2.md) |
| Location / Nimbus Station | 56 | 27 | [1](indexes/group-14-1.md) |
| Location / Ninjago Monastery | 85 | 63 | [1](indexes/group-15-1.md) &#124; [2](indexes/group-15-2.md) |
| Location / Pet Cove | 13 | 7 | [1](indexes/group-16-1.md) |
| Location / Venture Explorer | 6 | 8 | [1](indexes/group-17-1.md) |
| LUPs / No subtype | 13 | 2 | [1](indexes/group-18-1.md) |
| Play / General | 0 | 23 | [1](indexes/group-19-1.md) |
| Play / Shooting Galleries | 0 | 19 | [1](indexes/group-20-1.md) |
| Racing / Forbidden Valley | 6 | 3 | [1](indexes/group-21-1.md) |
| Racing / General | 0 | 26 | [1](indexes/group-22-1.md) |
| Racing / Gnarled Forest | 6 | 8 | [1](indexes/group-23-1.md) |
| Racing / Nimbus Station | 9 | 8 | [1](indexes/group-24-1.md) |
| Test / Test | 1 | 0 | [1](indexes/group-25-1.md) |

## What these numbers mean

The counts below describe entries and evidence in the local reference data.
They do not mean every quest is available in your game. For source details
and interpretation, see [methodology](./Methodology.md).

| Evidence | Count |
| --- | ---: |
| Quest detail pages | 682 |
| Achievement detail pages | 745 |
| Attached objective rows | 1800 |
| Unattached objective rows (no Missions definition) | 4 |
| Definitions with conservative community associations | 409 |
| Definitions with an official client name (locale.xml) | 1353 |
| Definitions with official client description/offer texts | 1369 |
| Objective rows with client task text | 1717 |
| Public wiki pages researched | 757 |
| Definitions with a mapped candidate giver | 681 |
| Definitions with any mapped/typed location evidence | 1022 |
| Parsed referenced level files | 536 |

Evidence counts overlap. A data-derived objective summary is not original quest dialogue; a checklist is not proof of strict objective order. Static XYZ coordinates identify candidate map placements, not guaranteed active NPCs. Reward choices, repeats, and player eligibility remain important.

[Methodology and limitations](./Methodology.md) | [Community sources](./Community%20Sources.md) | [Machine-readable coverage](./Coverage.json)
