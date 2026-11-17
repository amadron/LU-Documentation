# Loot matrix 501

[Item database](../README.md) | [Methodology](../Methodology.md)

## Sources and mapped locations

| Kind | Source | Location evidence | Conditions |
| --- | --- | --- | --- |
| Activity | [AM - Aura Blossom Flowers (LOT 12199)](../sources/object-12199.md) | [Crux Prime (1800)](../locations/zone-1800.md) | AM - Blue Flowers to be watered (activity ID 12199, rating threshold -1, reward 161); Selected only if this is the highest eligible rating threshold; instance zone not specified.; Static association, not a live-spawn guarantee |

## Item candidates

Default vendor-stock probabilities are shown only when this matrix has a registered vendor. Loot probabilities use the generic algorithm, not a guarantee of actual use by every script/activity.

| Item | Modeled loot chance / expected count | Default vendor stock |
| --- | --- | --- |
| Imagination Powerup 2 points (LOT 4035; not an item registration) | 100%; mean 1 | Not associated with a vendor |
| Armor Powerup 2 points (LOT 11912; not an item registration) | 50%; mean 0.5 | Not associated with a vendor |
| Life Powerup 2 points (LOT 11915; not an item registration) | 25%; mean 0.25 | Not associated with a vendor |
| ![](../../../assets/icons/objects/12317.webp){ .lu-ti width="24" loading="lazy" } [Aura Blossoms (LOT 12317)](../12317.md) | 100%; mean 1 | Not associated with a vendor |

## Raw matrix entries

| Row | Loot table | Rarity table | Trigger | Min | Max | Flag | Gate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1766 | 415 | 4 | 0.25 | 1 | 1 |  |  |
| 1767 | 419 | 4 | 1 | 1 | 1 |  |  |
| 1768 | 423 | 4 | 0.5 | 1 | 1 |  |  |
| 2126 | 454 | 24 | 1 | 1 | 1 |  |  |

[LootMatrix](../../../db/LootMatrix.md), [LootTable](../../../db/LootTable.md), [RarityTable](../../../db/RarityTable.md).
