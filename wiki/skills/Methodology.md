# Player Skill Database — Methodology

[Player skills](./README.md) | [Item database](../items/README.md)

This is a **candidate** catalog, not all skill definitions or a list of
verified playable abilities. The supplied snapshot has no localized skill
names or descriptions. We use skill IDs and linked equipment instead of
inventing names, effects, damage, or unlock instructions.

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

Records, names, and stored values are snapshot evidence: server configuration,
client localization, ownership, prerequisites, and implemented behavior may
differ. Follow linked item pages for acquisition evidence; the presence of a
skill or item does not establish current availability.

The pages were generated from local table exports using
`scripts/build_player_references.py`; the raw exports are not included in the
public website.
