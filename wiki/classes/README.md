# Faction Classes

[Game Guide](../README.md) | [Faction Guide](../Faction%20Guide.md) | [Items](../items/README.md) | [Player skills](../skills/README.md)

Each faction offers three specialty classes. A class is defined by its kit: the
equipment you wear gives you its abilities. This page explains how classes and their
ranks work; every class has its own page with abilities, unlock path, and equipment.

## All classes

| Class | Faction | Role (summary) | Weapon | Rank-1 head ability | Rank-3 signature ability |
| --- | --- | --- | --- | --- | --- |
| [Engineer](./engineer.md) | Assembly | Support / builder | Engineer Wrench | [Deploy Turret 1](../skills/624.md) | [Personal Fortress](../skills/649.md) |
| [Inventor](./inventor.md) ¹ | Assembly | Support / summoner | Inventor Improved Launcher | [Summon Make-Shift Buddy 1](../skills/1055.md) | [Gadgets Extreme](../skills/1058.md) |
| [Summoner](./summoner.md) | Assembly | Summoner / support | Summoner Staff | [Summon Bulper 1](../skills/631.md) | [Summon Scratch](../skills/673.md) |
| [Shinobi](./shinobi.md) ¹ | Paradox | Melee damage | Shinobi Katana | [Dark Lightning 1](../skills/1075.md) | [Shuriken Barrage](../skills/482.md) |
| [Sorcerer](./sorcerer.md) | Paradox | Caster / imagination support | Sorcerer Wand | [Maelstrom Breath 1](../skills/346.md) | [Last Blast](../skills/655.md) |
| [Space Marauder](./space-marauder.md) | Paradox | Ranged damage | Space Marauder Blaster | [Plasma Ball 1](../skills/458.md) | [Cluster Strike](../skills/606.md) |
| [Knight](./knight.md) | Sentinels | Defender | Knight Greatsword | [Strengthen Armor 1](../skills/777.md) | [Roundhouse](../skills/338.md) |
| [Samurai](./samurai.md) | Sentinels | Defender | Samurai Katana | [Strengthen Armor 1](../skills/777.md) | [Ronin Rush](../skills/550.md) |
| [Space Ranger](./space-ranger.md) ¹ | Sentinels | Crowd control | Space Ranger Zipgun | [Gravity Well 1](../skills/1088.md) | [Sentinel Blast](../skills/1093.md) |
| [Adventurer](./adventurer.md) ¹ | Venture League | Support / mobility | Adventurer Crossbow | [Path Cutter 1](../skills/1070.md) | [Rations](../skills/1073.md) |
| [Buccaneer](./buccaneer.md) | Venture League | Hybrid damage | Buccaneer Pistol &amp; Cutlass | [Super Jump 1](../skills/445.md) | [Funky Monkey 1](../skills/383.md) |
| [Daredevil](./daredevil.md) | Venture League | Ranged damage / mobility | Daredevil Flareguns | [Super Jump 1](../skills/445.md) | [Fire Extinguisher 3](../skills/599.md) |

¹ Added in a later content update; not covered by the 2010 guide.

Role summaries are an editorial reading of the ability descriptions in the client data,
not an official classification.

## How classes work

- **Faction membership.** Every kit piece requires the matching faction flag, so you
  can only use the classes of the faction you joined. You can unlock all three.
- **Ranks.** Every rank requires a minimum level (5, 15, or 30) and the class's rank
  achievement. Valiant weapons need level 35, valiant capes level 40.
- **Class books.** Using a *Rank N … Book* completes that rank's achievement.
  The rank-1 book comes in the starter package and is sold by the Nimbus Station vendor;
  wearing a complete set of one rank (*The … Gear N* achievement) rewards the next
  rank's book. Completing the rank-3 set gives LEGO Score only.
- **Abilities.** The head piece and weapons carry the active abilities; rank 2 adds an
  off-hand ability for most classes and rank 3 a neck/back capstone ability.
- **Set bonuses.** Wearing several pieces of the *same class and rank* unlocks passive
  bonuses. DarkflameServer applies a tier when the equipped count reaches it and removes
  it when the count drops below, so the tiers add up. Color variants and valiant items
  count as members of the rank-3 set.
- **Prices.** Usually 25 tokens per rank-1 piece, 60 per rank-2 piece, and 180 per
  rank-3 piece; valiant weapons cost 500 and valiant capes 250. Two-handed weapons cost
  double and occupy the off-hand slot through a hidden proxy item.

## Starting a class

1. **Join a faction** in Nimbus Station (achievement *Join Assembly!*, *Join Paradox!*,
   *Join The Sentinels!*, or *Join Venture League!*).
2. **Pick a starter kit.** Nexus Jay offers *Get your … Gear!*, completed at your
   faction's Nimbus Station vendor. Its reward is a choice of one of the three
   *Rank 1 … Kit Package* items.
3. **Use the rank-1 book** from the package, then equip the four pieces.
4. **Wear the full set** to receive the rank-2 book, and buy rank-2 pieces at level 15.

## Faction vendors

| Faction | Nimbus Station (rank 1–2 gear, rank-1 books) | Nexus Tower (rank 3, color variants, valiant gear) |
| --- | --- | --- |
| Assembly | [Meldric Steamvalve - Assembly Vendor (LOT 6633)](../items/sources/object-6633.md) | [Torbert Oscillator - Assembly Vendor (LOT 13380)](../items/sources/object-13380.md) |
| Paradox | [Cog Blammo - Paradox Vendor (LOT 6632)](../items/sources/object-6632.md) | [Sutoro Hatto - Paradox Vendor (LOT 13378)](../items/sources/object-13378.md) |
| Sentinels | [Xeno Blueblade - Sentinel Vendor (LOT 6631)](../items/sources/object-6631.md) | [Nikolai Gammapulse - Sentinel Vendor (LOT 13376)](../items/sources/object-13376.md) |
| Venture League | [Magnus Bumperdent - Venture League Vendor (LOT 6634)](../items/sources/object-6634.md) | [Billy Ganges - Venture League Vendor (LOT 13384)](../items/sources/object-13384.md) |

All four Nimbus Station vendors stand on the Plaza. The Nexus Tower vendors are spread
over the tower's faction areas; the vendor pages list exact map coordinates. Vendors also
sell faction consumables, Imaginite bags, and (Nexus Tower) faction car and rocket parts.

## Earning faction tokens

Tokens are paid in your own faction's currency. DarkflameServer converts the neutral
*Faction Token Proxy* (LOT 13763) to your faction's token when you receive it; without a
faction it is discarded. Verified sources in the supplied data and server code:

- **Drops:** the proxy is in a loot table shared by 259 loot matrices — many smashables,
  crates, and enemies across the worlds — with a 2% chance per drop roll.
- **Maelstrom converters:** turning in 25 *Maelstrom-Infected Bricks* (LOT 6194) gives
  5 tokens, at the quick-build token console in Nimbus Station and at the *Maelstrom
  Converter* console in Nexus Tower (LOT 14087).

No mission in the supplied data rewards faction tokens directly.

## Server implementation notes

Checked against the DarkflameServer source in this repository:

- Set bonuses, full-set achievements, class books, vendor purchases with faction tokens,
  and the token proxy conversion are implemented.
- The behavior types used by the class abilities (attacks, projectiles, summons, buffs,
  heals, shields, and so on) are implemented. Two minor behavior types that some weapon
  attack chains reference — *Alter Chain Delay* and *Alter Cooldown* — are accepted but
  have no effect, so combo timing can differ slightly from the original game.

## Source and limitations

Generated by `scripts/build_classes.py` from the `ItemSets`, `ItemSetSkills`,
`ItemComponent`, `ObjectSkills`, `SkillBehavior`, `Missions`, and `Preconditions` tables
and the English client locale. Regenerate with `py -3 scripts/build_classes.py`.
