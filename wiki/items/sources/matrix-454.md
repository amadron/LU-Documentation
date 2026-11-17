# Loot matrix 454

[Item database](../README.md) | [Methodology](../Methodology.md)

## Sources and mapped locations

| Kind | Source | Location evidence | Conditions |
| --- | --- | --- | --- |
| Drop | [WBL - Equip Crate 07 (LOT 10737)](../sources/object-10737.md) | [MoonBase (1603)](../locations/zone-1603.md) | DestructibleComponent 1578; static component precedence; Static association, not a live-spawn guarantee |

## Item candidates

Default vendor-stock probabilities are shown only when this matrix has a registered vendor. Loot probabilities use the generic algorithm, not a guarantee of actual use by every script/activity.

| Item | Modeled loot chance / expected count | Default vendor stock |
| --- | --- | --- |
| [Moonbase Fuel Rod (LOT 11211)](../11211.md) | 40%; mean 0.4 | Not associated with a vendor |
| Imagination Powerup 3 points (LOT 11910; not an item registration) | 100%; mean 2.5 | Not associated with a vendor |
| Armor Powerup 2 points (LOT 11912; not an item registration) | 100%; mean 1.5 | Not associated with a vendor |
| Life Powerup 2 points (LOT 11915; not an item registration) | 100%; mean 1 | Not associated with a vendor |

## Raw matrix entries

| Row | Loot table | Rarity table | Trigger | Min | Max | Flag | Gate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1429 | 369 | 25 | 0.4 | 1 | 1 |  |  |
| 1640 | 415 | 4 | 1 | 1 | 1 |  |  |
| 1641 | 420 | 4 | 1 | 2 | 3 |  |  |
| 1642 | 423 | 4 | 1 | 1 | 2 |  |  |

[LootMatrix](../../../db/LootMatrix.md), [LootTable](../../../db/LootTable.md), [RarityTable](../../../db/RarityTable.md).
