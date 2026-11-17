# Avant Gardens timed obstacle course

[Racing index](../README.md) | [Foot races](./foot-races.md) | [Monument Race](./monument-race.md)

The Avant Gardens obstacle course is a separate scripted on-foot activity, not one of the four car tracks, the generic foot-race manager, or Monument Race. The local Objects table names LOT 3004 “AG - Obstacle Course Starter,” LOT 4997 “AG - Obstacle Course Finish Line Flagger,” and LOT 5025 “AG -Finish Line Flags”; LOT 3004 is registered to `NpcAgCourseStarter.cpp`. The Monument goal/cancel scripts are separate handlers and do not establish that the obstacle-course starter owns their `race_manager` group.

## Local implementation

- **Starter object:** LOT 3004 — AG - Obstacle Course Starter.
- **Activity mechanism:** scripted activity component and client object messages; the NPC script uses start/exit, timer, cancel, finish, and leaderboard behavior. This is separate from the generic `BaseFootRaceManager`.
- **Mission hooks:** the NPC script calls `ForceProgressTaskType(1884, 1, 1, false)` and reports elapsed time via `PERFORM_ACTIVITY`. Consult [Mission 1884](../../quests/1884.md) for the actual objective interpretation and reward/prerequisites.
- **Finish/cancel:** the NPC handles `course_finish` and `course_cancel` events. The Monument Race goal/cancel triggers use a `race_manager` group and are separate scripts; this page does not claim they use LOT 3004.
- **Starter placement in Avant Gardens:**

No valid static placements for these template IDs were identified in the parsed map assets.

Other course/finish candidates in Avant Gardens, not individually proven to be required triggers:

No valid static placements for these template IDs were identified in the parsed map assets.

The object-name/registration data supports a local AG obstacle-course activity, but does not establish that the course is currently enabled, identify every client-side gate, or prove that every listed nearby trigger is a required course object. No separate `ActivityRewards` row is inferred from its relation to the Monument Race.

Local source: [NpcAgCourseStarter.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dScripts/02_server/Map/AG/NpcAgCourseStarter.cpp), [Activities.csv](../../../db/Activities.csv), [Objects.csv](../../../db/Objects.csv), and [ComponentsRegistry.csv](../../../db/ComponentsRegistry.csv).
