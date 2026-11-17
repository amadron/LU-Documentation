# Loot matrix 469

[Item database](../README.md) | [Methodology](../Methodology.md)

## Sources and mapped locations

| Kind | Source | Location evidence | Conditions |
| --- | --- | --- | --- |
| Drop | [GF - Racer Welding Tool (LOT 6996)](../sources/object-6996.md) | [Gnarled Forest Deep Dive Map (375)](../locations/zone-375.md); [Gnarled Forest (1300)](../locations/zone-1300.md); [Nimbus Station (1200)](../locations/zone-1200.md) | DestructibleComponent 1606; static component precedence; Static association, not a live-spawn guarantee |

## Item candidates

Default vendor-stock probabilities are shown only when this matrix has a registered vendor. Loot probabilities use the generic algorithm, not a guarantee of actual use by every script/activity.

| Item | Modeled loot chance / expected count | Default vendor stock |
| --- | --- | --- |
| [White Top Hat (LOT 11291)](../11291.md) | 0% in the generic loot model | Not associated with a vendor |
| Imagination Powerup 3 points (LOT 11910; not an item registration) | 45%; mean 0.675 | Not associated with a vendor |
| Armor Powerup 2 points (LOT 11912; not an item registration) | 33%; mean 0.33 | Not associated with a vendor |
| Life Powerup 2 points (LOT 11915; not an item registration) | 33%; mean 0.33 | Not associated with a vendor |

## Raw matrix entries

| Row | Loot table | Rarity table | Trigger | Min | Max | Flag | Gate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1520 | 415 | 4 | 0.33 | 1 | 1 |  |  |
| 1521 | 420 | 4 | 0.45 | 1 | 2 |  |  |
| 1522 | 423 | 4 | 0.33 | 1 | 1 |  |  |
| 1523 | 383 | 23 | 1 | 1 | 1 |  |  |

[LootMatrix](../../../db/LootMatrix.md), [LootTable](../../../db/LootTable.md), [RarityTable](../../../db/RarityTable.md).
