# Loot matrix 232

[Item database](../README.md) | [Methodology](../Methodology.md)

## Sources and mapped locations

| Kind | Source | Location evidence | Conditions |
| --- | --- | --- | --- |
| Drop | [GF - Siren Crate (LOT 6911)](../sources/object-6911.md) | [Gnarled Forest Deep Dive Map (375)](../locations/zone-375.md); [Gnarled Forest (1300)](../locations/zone-1300.md) | DestructibleComponent 648; static component precedence; Static association, not a live-spawn guarantee |

## Item candidates

Default vendor-stock probabilities are shown only when this matrix has a registered vendor. Loot probabilities use the generic algorithm, not a guarantee of actual use by every script/activity.

| Item | Modeled loot chance / expected count | Default vendor stock |
| --- | --- | --- |
| ![](../../../assets/icons/objects/6912.webp){ .lu-ti width="24" loading="lazy" } [Mermaid Head (LOT 6912)](../6912.md) | 100%; mean 1 | Not associated with a vendor |
| Imagination Powerup 3 points (LOT 11910; not an item registration) | 100%; mean 1.5 | Not associated with a vendor |
| Armor Powerup 2 points (LOT 11912; not an item registration) | 100%; mean 1 | Not associated with a vendor |
| Life Powerup 2 points (LOT 11915; not an item registration) | 50%; mean 0.5 | Not associated with a vendor |
| ![](../../../assets/icons/objects/13763.webp){ .lu-ti width="24" loading="lazy" } [Faction Token Proxy (LOT 13763)](../13763.md) | 2%; mean 0.02 | Not associated with a vendor |

## Raw matrix entries

| Row | Loot table | Rarity table | Trigger | Min | Max | Flag | Gate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 507 | 415 | 4 | 0.5 | 1 | 1 |  |  |
| 508 | 420 | 4 | 1 | 1 | 2 |  |  |
| 509 | 423 | 4 | 1 | 1 | 1 |  |  |
| 510 | 115 | 4 | 1 | 1 | 1 |  |  |
| 4075 | 670 | 23 | 0.02 | 1 | 1 |  |  |

[LootMatrix](../../../db/LootMatrix.md), [LootTable](../../../db/LootTable.md), [RarityTable](../../../db/RarityTable.md).
