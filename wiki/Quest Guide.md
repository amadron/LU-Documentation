# Quest Guide

[Game Guide](./README.md) | [Item Guide](./Item%20Guide.md) | [Racing Guide](./Racing%20Guide.md) | [Pet Guide](./Pet%20Guide.md)

Missions give you goals to pursue as you explore LEGO Universe. Talk to
characters, take on an assignment, follow its objectives, then return to claim
the reward when the game asks you to. Achievements track accomplishments and
often complete as you play.

Use your in-game mission journal as the source of truth for what to do next.
The [Quest and Achievement Database](./quests/README.md) is a lookup tool for
details such as prerequisites, associated characters, possible rewards, and
locations. It includes test and unused definitions too, so a listed quest
may not be available on your server.

For activity-specific advice, see the [Racing Guide](./Racing%20Guide.md)
or [Pet Guide](./Pet%20Guide.md). The detailed [Racing Database](./racing/README.md)
and [Pet Database](./pets/README.md) link activities back to their related quests.

## 1. Missions and achievements

LEGO Universe tracks both missions and achievements. Missions generally
involve accepting an assignment, completing its objectives, and turning it
in. Achievements track accomplishments and can complete automatically when
their objectives are fulfilled.

## 2. Starting a mission

1. Talk to an available mission-giving NPC and read the assignment.
2. Check any prerequisites shown in game.
3. Accept the mission before beginning its objectives unless the game
   explicitly indicates otherwise.
4. Open your mission journal and check the exact targets and quantities.

If a mission is not offered, earlier missions, a repeat cooldown, or other
requirements may be involved. An NPC can offer one mission and accept another;
do not assume that the giver is always the turn-in NPC.

Already owning an item or having performed an action does not guarantee
retroactive credit for every objective. Follow the active journal entry.

## 3. Completing objectives

| Objective | Practical approach |
|---|---|
| Smash enemies or objects | Confirm the exact target; similarly named enemies or scenery may not count. Watch the counter after one successful action. |
| Gather items | Collect the requested item and quantity. Keep required items until the mission is turned in. |
| Talk, interact, or deliver | Use the specified NPC or object; simply standing nearby is not always enough. |
| Explore | Visit the relevant area and check whether the exploration objective updates. |
| Use an item, skill, or emote | Use the requested action, not merely an item with a similar appearance. Some objectives require a particular target. |
| Race or perform an activity | Check the requested result, event, or condition rather than assuming any participation counts. |
| Build, tame a pet, or visit a property | Follow the specific task; other activities of the same broad kind may not qualify. |

These are broad objective families, not instructions for a particular quest.
Always follow the exact objective and conditions shown in your journal.

## 4. Turning in and choosing rewards

Completing the objective counters is not always the final step. If the
mission asks you to turn it in, return to the character or object shown in
your journal and finish the conversation.

- If a reward choice is presented, inspect the alternatives before confirming.
  Do not assume you receive every displayed choice.
- Gathered mission items can be consumed when rewards are granted.
- Repeatable missions can have different rewards on later completions.
- Check your inventory and any completion message before reporting a missing
  reward or repeating the activity.

For item requirements and comparing rewards, see the
[Item Guide](./Item%20Guide.md).

## 5. When progress is blocked

| Symptom | Check first |
|---|---|
| NPC does not offer a quest | Earlier prerequisites, whether the quest is already active/completed, and any repeat cooldown. |
| Objective counter does not move | Active mission, correct target/action, required quantity, and any journal-specific conditions. |
| All objectives appear finished | Whether a turn-in interaction or reward selection is still required. |
| Requested item appears missing | Relevant inventory categories and whether an earlier turn-in consumed it. Do not discard other quest items while investigating. |
| Repeat quest is unavailable | Whether it is actually repeatable and whether its cooldown has elapsed. |
| Guide/catalog content cannot be found | Whether it is test, unavailable, or unimplemented content in this server version. |

If the problem persists, send staff:

```text
Character:
Quest title and mission ID, if known:
Zone and NPC:
Current objective and counter:
What I did:
What happened instead:
Screenshot and approximate time:
```

Avoid repeatedly claiming rewards or trying GM commands as a workaround.
Staff can investigate definitions and saved progress separately.

## Optional: looking up quest details

You do not need to read the raw tables to play. If you want to investigate a
specific entry:

- [Quest and achievement database](./quests/README.md) resolves the joins into
  readable detail pages, with [quest-character](./quests/NPC%20Index.md) and
  [zone](./quests/locations/README.md) indexes.
- [Missions](../db/Missions.md) contains IDs, prerequisite expressions,
  repeatability, and reward fields. It is a technical reference, not a
  player-facing quest list.
- [MissionTasks](../db/MissionTasks.md) contains objectives grouped by mission
  ID. Its numeric fields are internal identifiers and can require
  interpretation.
- The [full NPC and creature template list](../LEGO%20Universe%20NPC%20List.md)
  is broader than the quest-character index; it does not give live positions
  or walking directions.
- The [item list](../LEGO%20Universe%20Item%20List.md) is a flat name lookup;
  the [item database](./items/README.md) provides more source details.

The exported mission tables alone do not provide original localized dialogue
or every scripted puzzle step. The database reconstructs supported objectives
and checklists rather than inventing the missing narrative. Its
[methodology](./quests/Methodology.md) explains how technical fields, map
evidence, and historical community matches were interpreted.

## Evidence

The mission/achievement distinction and completion behavior were checked in
the local [mission implementation](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dMission/Mission.cpp).
Objective families follow the server's
[task-type enum](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dCommon/dEnums/eMissionTaskType.h).
Exact availability and client presentation can differ between deployments.
