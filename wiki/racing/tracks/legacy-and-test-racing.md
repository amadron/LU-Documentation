# Legacy, seasonal, and test racing content

[Racing index](../README.md) | [Methodology](../Methodology.md)

This page separates content that appears in local definitions/assets but cannot be treated as an ordinary, currently available public race.

## Frostburgh / Space Blizzard

Activity 60 and reward rows exist in `Activities` / `ActivityRewards`; local map assets contain an LUZ with embedded world ID 1261 and a winter racetrack LVL. It is not path-matched by a ZoneTable row. The [Space Blizzard](./space-blizzard.md) page therefore documents the static definition and historical seasonal identity but does not claim that Frostburgh is live or that the activity can be entered.

## Unassigned/test activities and assets

- Activity ID 23 exists with inactive/unlocalized flags and no instance map. Two task-type-2 objectives target activity/Quick Build identifier 23 (the quest catalog resolves these to a Pirate Quick Build); they are not racing tasks and are excluded from racing-objective totals.
- Local script registrations include a deprecated `GF_RACE_TEST.lua` / `RACE_CLIENT.lua` reference and an object LOT 12652 named “TESTFV - Race Activator,” registered to activity 54. This is labeled a test-named duplicate/entry object, not another track.
- Unused/disabled race-related objects include biplane/track-piece/track-layout and “test” names, e.g. LOTs 2251–2255, 4627, 6283–6284, and 10785. Their presence does not establish a playable race.
- The public historical article [NAZCAR Hollows](../Community%20Sources.md#nazcar-hollows) describes an unreleased modular-track prototype. No playable NAZCAR activity or matched ZoneTable world was established in this local snapshot.
- A temporary/beta race entry, event contest, or unreleased planned track mentioned in community history is not counted as a server-backed track unless the local tables/map/script support it.

## Inclusion boundary

The overview covers the four local car-racing Activities 39/42/54/60; generic timed foot races; the separate [AG obstacle course](./ag-obstacle-course.md); [Monument Race](./monument-race.md); and the above legacy/test references. Racecar components, race boosters, smashed track objects and rewards are cross-linked as relevant items/evidence, not treated as independent races. See [Coverage.json](../Coverage.json) for exact counts and unmatched assets.
