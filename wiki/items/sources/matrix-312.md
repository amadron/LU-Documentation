# Loot matrix 312

[Item database](../README.md) | [Methodology](../Methodology.md)

## Sources and mapped locations

| Kind | Source | Location evidence | Conditions |
| --- | --- | --- | --- |
| Drop | [Pirate Treasure Chest (LOT 8660)](../sources/object-8660.md) | [Gnarled Forest Deep Dive Map (375)](../locations/zone-375.md); [Gnarled Forest (1300)](../locations/zone-1300.md) | DestructibleComponent 901; static component precedence; Static association, not a live-spawn guarantee |

## Item candidates

Default vendor-stock probabilities are shown only when this matrix has a registered vendor. Loot probabilities use the generic algorithm, not a guarantee of actual use by every script/activity.

| Item | Modeled loot chance / expected count | Default vendor stock |
| --- | --- | --- |
| [Numb Chuck's Treasure (LOT 8662)](../8662.md) | 100%; mean 1 | Not associated with a vendor |
| Imagination Powerup 5 points (LOT 11911; not an item registration) | 100%; mean 1.5 | Not associated with a vendor |
| Armor Powerup 3 points (LOT 11913; not an item registration) | 100%; mean 1.5 | Not associated with a vendor |
| Life Powerup 3 points (LOT 11916; not an item registration) | 100%; mean 1 | Not associated with a vendor |
| [Faction Token Proxy (LOT 13763)](../13763.md) | 2.5%; mean 0.025 | Not associated with a vendor |

## Raw matrix entries

| Row | Loot table | Rarity table | Trigger | Min | Max | Flag | Gate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 751 | 196 | 4 | 1 | 1 | 1 |  |  |
| 1438 | 416 | 4 | 1 | 1 | 1 | 7 |  |
| 1439 | 421 | 4 | 1 | 1 | 2 |  |  |
| 1440 | 424 | 4 | 1 | 1 | 2 |  |  |
| 4076 | 670 | 23 | 0.025 | 1 | 1 |  |  |

[LootMatrix](../../../db/LootMatrix.md), [LootTable](../../../db/LootTable.md), [RarityTable](../../../db/RarityTable.md).
