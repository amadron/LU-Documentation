# Player Skill Database — Methodology

[Player skills](./README.md) | [Item database](../items/README.md)

This is a **candidate** catalog, not all skill definitions or a list of
verified playable abilities. Skill names and descriptions are the official
English client text from `locale.xml` (`en_US`), as described below; skills
without a localized name are listed by ID.

## Inclusion

- Direct equipment candidates require an `ObjectSkills` cast-on-type `0`
  association, an item component, and one of the `special_r`, `special_l`,
  `hair`, or `clavicle` slots. They must have an existing item page and a
  nonempty object name. Names explicitly containing test, unused, debug,
  proxy, GM, or developer are omitted; this heuristic cannot establish
  release status.
- Set candidates come from `ItemSets.skillSetWith2` through
  `skillSetWith6` joined to `ItemSetSkills.SkillSetID`. The piece count
  belongs to that association; it is not an acquisition requirement. Sets
  with explicitly technical or GM-named members are excluded.
- Skills without a matching `SkillBehavior` row remain listed with unknown
  settings. A skill can have both direct-equipment and set associations.
  Consumables, non-equipment skills, and equipment outside these slots are
  intentionally outside this catalog.

The selected rules follow the reviewed server's
[equipment-slot and skill lookup](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dComponents/InventoryComponent.cpp)
and [item-set associations](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dInventory/ItemSet.cpp).
The [StartSkill handler](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dGameMessages/GameMessageHandler.cpp)
uses the recorded imagination cost after a successful player cast. That does
not prove how every item-set or other skill path uses the field. Cooldown is
reported as a stored client value, not as measured game behavior.

## Names and descriptions

Names come from the client locale key `SkillBehavior_<ID>_name` and the
**Description** section from `SkillBehavior_<ID>_descriptionUI` (the in-game
tooltip), both in the `en_US` locale of the client's `locale/locale.xml`.
339 of the 356 listed skills have both; the other 17 (IDs 1160–1193, all
set bonuses) have no localized text and keep the title "Skill &lt;ID&gt;".

Tooltips contain layout tokens that the client replaces with labels. They
are rendered as readable text: `%(DamageCombo)` becomes "Damage:" (the
client's "Damage Combo" line), `%(ChargeUp)` becomes "Charge attack:" (the
"Charge-Up" line), `%(Description)` is shown as plain text, and
`%(AltCombo)` becomes "Damage vs. Skeletons:". The last label is an
inference: the client's rollover label for that line is "Skeletons Combo",
and the token appears only on Ninjago-era equipment and Spinjitzu skills.
Tooltip wording, including spelling, is reproduced as stored. A tooltip
describes the intended effect; the server's actual behavior can differ.

## Historical community names

Before client names were used, some pages carried a community name
candidate taken from the wiki articles below, which name certain historical
abilities in connection with particular equipment. We matched that equipment
to a local item LOT and then to its cast-on-type `0` skill association. Where
that indirect candidate differs from the official client name, the skill
page keeps it as a **historical community name** with its source; the
official name takes precedence. Matching candidates are not repeated.

The short name candidates and item-to-ID crosswalk are recorded in
`scripts/skill_name_evidence.json`; article prose and images are not copied.
Source: LEGO Universe Wiki contributors, under the wiki's
[CC-BY-SA license](https://www.fandom.com/licensing):

- [Faction Gear, revision 163921](https://legouniverse.fandom.com/api.php?action=query&prop=revisions&revids=163921&rvprop=ids%7Ccontent&rvslots=main&formatversion=2&format=json)
- [Sorcerer, revision 163840](https://legouniverse.fandom.com/api.php?action=query&prop=revisions&revids=163840&rvprop=ids%7Ccontent&rvslots=main&formatversion=2&format=json)
- [Shinobi, revision 164260](https://legouniverse.fandom.com/api.php?action=query&prop=revisions&revids=164260&rvprop=ids%7Ccontent&rvslots=main&formatversion=2&format=json)
- [Space Marauder, revision 164249](https://legouniverse.fandom.com/api.php?action=query&prop=revisions&revids=164249&rvprop=ids%7Ccontent&rvslots=main&formatversion=2&format=json)
- [Adventurer, revision 164153](https://legouniverse.fandom.com/api.php?action=query&prop=revisions&revids=164153&rvprop=ids%7Ccontent&rvslots=main&formatversion=2&format=json)

Records, names, and stored values are snapshot evidence: server configuration,
client localization, ownership, prerequisites, and implemented behavior may
differ. Follow linked item pages for acquisition evidence; the presence of a
skill or item does not establish current availability.

The pages were generated from local table exports and the client locale
using `scripts/build_player_references.py`; names and tooltips were added to
the existing pages with `scripts/enrich_skills.py`. The raw exports are not
included in the public website.
