# DarkflameServer Gamemaster Guide

## 1. Scope and evidence

This is a practical reference for authorized GMs, moderators, and administrators
using the local DarkflameServer checkout at revision
`8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4`.
Command syntax, permissions, and target behavior below were checked against
the source, not exercised on a running game server. This is a selected
operational guide, not an exhaustive list of developer commands.

For all registered commands, aliases, and permission thresholds, see the
[complete command reference](./DarkflameServer%20Command%20Reference.md).

- [Command registrations and help](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp)
- [Developer/GM command implementations](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommands/DEVGMCommands.cpp)
- [Moderation command implementations](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommands/GMGreaterThanZeroCommands.cpp)
- [Player command implementations](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommands/GMZeroCommands.cpp)
- [All exported database tables](../db/README.md)

In command examples, replace `<placeholders>` with actual values; do not type
the angle brackets. Use the lowercase command spellings shown here. Commands
do not share a universal player-target argument or quoting convention.

## 2. Permissions and getting started

Your account's authorized maximum GM level and your character's active GM
level are distinct. An administrator must grant account permissions through
the deployment's account-management process. `/setgmlevel` does not grant
permissions beyond the account maximum.

| Level | Source name | Selected commands available at this threshold |
|---:|---|---|
| 0 | `CIVILIAN` | `/help`, `/who`, `/instanceinfo`, `/ping`, `/setgmlevel` subject to account authorization |
| 1 | `FORUM_MODERATOR` | `/gminvis`, `/testmap` |
| 2 | `JUNIOR_MODERATOR` | `/kick`, `/showall`, `/findplayer`, `/spectate` |
| 3 | `MODERATOR` | `/mailitem` |
| 4 | `SENIOR_MODERATOR` | `/ban` |
| 5 | `LEAD_MODERATOR` | `/approveproperty` |
| 6 | `JUNIOR_DEVELOPER` | `/teleport`, `/mute` |
| 7 | `INACTIVE_DEVELOPER` | No additional commands listed in this guide |
| 8 | `DEVELOPER` | Item grants to self, mission/flag changes, spawning, announcements, and most diagnostics |
| 9 | `OPERATOR` | `/shutdownuniverse` |

These are actual command-registration thresholds, not a policy recommendation.
In particular, `/mute` requires level **6**, and `/gmadditem` requires **8**,
despite what historical role descriptions might suggest.
Access checks normally allow a command when the active level is at least its
registered threshold. Non-developer builds additionally force accounts whose
maximum is `JUNIOR_DEVELOPER` to civilian in the level-change handler.
See [the level enum](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dCommon/dEnums/eGameMasterLevel.h)
and the command sources for details.

Start with:

```text
/help
/help 2
/help mailitem
/instanceinfo
/who
```

`/help` lists commands accessible at your active level, ten per page.
For an authorized moderator account, `/setgmlevel 3` requests active level 3;
`/setgmlevel 0` returns to civilian mode. Request only the level needed.

### Operating rules

1. Confirm the exact character, account context, and world instance.
2. Record the support case, evidence, original state, and intended change.
3. Use a test character/private test environment for experimentation.
4. Make the smallest necessary change and verify the outcome before repeating it.
5. Escalate persistent-data changes to an administrator with a verified backup.
6. Never assume a command worked merely because it produced no error.

Commands registered above civilian level are submitted to the game database's
`command_log` before their handlers run. This records attempted execution, not
proof of success. Civilian-registered commands, including `/setgmlevel`, are
not covered by that particular logging condition. Maintain a support record
as well; command logging is not a rollback mechanism.

## 3. Understanding IDs and database data

| Identifier | Meaning | Where to look |
|---|---|---|
| LOT | Object template number, shared by instances of that template | [Objects](../db/Objects.md), [item catalog](../LEGO%20Universe%20Item%20List.md), [NPC catalog](../LEGO%20Universe%20NPC%20List.md) |
| Runtime object ID | A particular live entity or item instance, not a LOT | Runtime inspection and logs |
| Component ID | Key for component-specific data, not normally a spawn/item number | [ComponentsRegistry](../db/ComponentsRegistry.md) |
| Mission ID | Mission definition identifier | [Missions](../db/Missions.md), [MissionTasks](../db/MissionTasks.md) |
| Zone ID | Map/zone definition, not the unique running instance | [ZoneTable](../db/ZoneTable.md) |
| Flag ID | Player flag definition | [PlayerFlags](../db/PlayerFlags.md) |

The CSV/Markdown exports are **reference copies**, not the live database.
Editing them does not update the server.

CDClient defines items, missions, NPC templates, and zones. The separate game
database stores accounts, character state, mail, property ownership, and other
runtime records. Character inventories and mission state are serialized in
character XML; `ItemComponent` is not a player's inventory.
See [the data-model guide](../LEGO%20Universe%20Data%20Model%20and%20Public%20Research.md).

## 4. Finding and observing players

| Command | Minimum level | Actual scope |
|---|---:|---|
| `/who` | 0 | Lists players in the current instance, not the entire universe. |
| `/instanceinfo` | 0 | Reports current instance information. |
| `/ping` | 0 | Reports your average ping; `/ping -l` requests the latest ping. |
| `/showall` | 2 | Requests player/zone information through the chat service. |
| `/findplayer <CharacterName>` | 2 | Requests a player lookup through the chat service. |
| `/spectate <CharacterName>` | 2 | Targets the camera at a player resolved in the current world process. |
| `/spectate` | 2 | Returns the camera target to your own character. |
| `/gminvis` | 1 | Sends the GM-invisibility toggle message; not a substitute for access control. |

The character name used by these handlers is not necessarily the account's
login name. A player being online elsewhere does not mean a local-world
command can find them.

## 5. Replacing a lost item

1. Check the report and confirm that replacement is justified.
2. Find the intended item's LOT in the [item catalog](../LEGO%20Universe%20Item%20List.md).
   Check its requirements, binding, and whether it is an actual item template.
3. Confirm the recipient's exact character name.
4. Send one approved replacement:

   ```text
   /mailitem <CharacterName> <ItemLOT>
   ```

5. Ask the player to check their mailbox, then verify receipt before retrying.

`/mailitem` requires level **3**. It resolves the character through the game
database and does not require the recipient to be present in your world.
The handler attaches **one item** with a fixed replacement subject/body; it
does not implement a quantity argument.

For testing on your own character:

```text
/lookup <SearchText>
/gmadditem <ItemLOT> 1
```

Both require level **8**. `/lookup` searches object names/descriptions, with
at most 50 query results; results are not restricted to inventory items.
`/gmadditem <ItemLOT> [Count]` adds items to **your own** inventory, not another
player's. Its alias is `/give`; this does not change its target behavior.

Do not confuse an item's LOT with `ItemComponent.id`. Resolve component data
through [ComponentsRegistry](../db/ComponentsRegistry.md).

## 6. Travel and stuck-character reports

Before moving anyone, record the zone, instance, clone, and safe destination.
Two players in the same zone ID can still be in different instances.

| Command | Minimum level | Behavior |
|---|---:|---|
| `/pos` | 8 | Prints and logs your current coordinates. |
| `/testmap <ZoneID>` | 1 | Requests a zone transfer for your own character, subject to zone accessibility. |
| `/teleport <X> <Y> <Z>` | 6 | Teleports yourself within the current world; supports relative axes such as `~5`. |
| `/teleport <SourceCharacter> <TargetCharacter>` | 6 | Moves the source player to the target player's position; both must resolve locally. |
| `/tpall` | 8 | Moves all character entities in the current world to your position. Avoid for individual support. |

Example for moving only yourself five units upward:

```text
/teleport ~ ~5 ~
```

Use the three-coordinate form for coordinate teleports. The two-number form
sets the outgoing Y coordinate to zero in this revision; do not rely on its
help text to guarantee safe terrain-height placement. Always provide valid
arguments; this handler does not return immediately after its usage message.

For player recovery, first verify local presence with `/who`. If appropriate,
stand in a known safe location and use
`/teleport <AffectedCharacter> <YourCharacter>`.
This is not a cross-zone summon.

## 7. Investigating mission and flag problems

Start with definitions, not forced completion:

1. Find the mission in [Missions](../db/Missions.md).
2. Check its prerequisite expression, repeatability, cooldown, and reward fields.
3. Review objectives in [MissionTasks](../db/MissionTasks.md).
4. Check NPC associations in [MissionNPCComponent](../db/MissionNPCComponent.md).
   Its `id` is a mission-offer component ID, not the NPC LOT.
5. Consult [Preconditions](../db/Preconditions.md) and
   [PlayerFlags](../db/PlayerFlags.md) where applicable.
6. Reproduce the issue on a test character and distinguish bad static data,
   missing server logic, and incorrect saved player state.

The following commands require level **8** and operate on **the executing
character**:

| Command | Effect |
|---|---|
| `/addmission <MissionID>` | Calls mission acceptance with the force option. |
| `/completemission <MissionID>` | Calls mission completion with the force option. |
| `/resetmission <MissionID>` | Calls the mission reset operation. |
| `/setflag <FlagID>` | Sets a player flag to true. |
| `/clearflag <FlagID>` | Sets a player flag to false. |

Do not append a player's name expecting to target them: these handlers do not
provide that interface. Forced mission changes can affect rewards and
prerequisites. Reset is not a general undo or guaranteed reward reversal.
Escalate another player's persistent-state repair rather than experimenting
with their character XML while they are online.

## 8. Moderation and property review

Use these only under the server's moderation policy, with an evidence record.

| Command | Minimum level | Scope and caveats |
|---|---:|---|
| `/kick <CharacterName>` | 2 | Disconnects a player found in the current world process. |
| `/ban <CharacterName>` | 4 | Resolves a character to an account and marks that account banned, not just that character. An offline character can be resolved through the database. |
| `/mute <CharacterName> <Days> [Hours]` | 6 | Updates the account's unmute time and notifies the chat service. Without a duration, the handler uses an indefinite mute. |
| `/approveproperty` | 5 | Approves the current property through its property-management component; takes no owner/property-ID argument. |

Prefer an explicit, policy-approved mute duration. Do not invent `/unban` or
`/unmute` syntax: no such commands are registered in the reviewed command
registry. Escalate reversal to the administrator's supported management process.
For remote enforcement, verify the result independently; local lookup and
disconnect behavior does not imply immediate removal from every world.

For property review, visit and confirm the exact property before approval.
[PropertyTemplate](../db/PropertyTemplate.md) describes property types;
actual ownership and placed models belong to the game database.

## 9. Spawning and controlled gameplay tests

`/spawn <LOT>` requires level **8** and constructs an entity at your current
position/rotation. Use the [NPC catalog](../LEGO%20Universe%20NPC%20List.md)
as a starting point, not proof that every template is safe to spawn.
The catalog includes test objects and unresolved/candidate templates.

Spawning does not itself edit a level asset or create a persistent property
placement. A spawned entity can still execute scripts, attack, drop loot, or
change other state. Spawn one object at a time in a controlled test instance
and plan cleanup before starting.

Useful definition chains:

- Combat: [DestructibleComponent](../db/DestructibleComponent.md),
  [BaseCombatAIComponent](../db/BaseCombatAIComponent.md),
  [Factions](../db/Factions.md).
- Drops: [LootMatrix](../db/LootMatrix.md) to [LootTable](../db/LootTable.md),
  with [RarityTable](../db/RarityTable.md) and
  [CurrencyTable](../db/CurrencyTable.md).
- Skills: [ObjectSkills](../db/ObjectSkills.md) to
  [SkillBehavior](../db/SkillBehavior.md), then behavior definitions.
- Vendors: [VendorComponent](../db/VendorComponent.md) to its loot matrix.

`/inspect localCharacter` (level **8**) opens inspection for your own entity.
Inspection with an actual runtime object ID is different from looking up a LOT.

## 10. Announcements, saves, and maintenance

These announcement commands require level **8**:

```text
/setanntitle Scheduled maintenance
/setannmsg Please finish your current activity and log out.
/announce
```

Title and message are stored on the executing character before sending.
Announcement delivery is routed through the chat service as well as local
clients. Confirm delivery rather than repeatedly sending it.

- `/forcesave` (level **8**) saves **your character XML** to the database.
  It is not a universe-wide save or a database backup.
- `/shutdown` (level **8**) invokes shutdown handling for the current world
  process. It is not interchangeable with shutting down the universe.
- `/shutdownuniverse` (level **9**) sends a shutdown request to the master and
  broadcasts a fixed message saying maintenance is in ten minutes.
  The command handler itself does not establish that delay; coordinate the
  actual shutdown sequence with the administrator rather than treating the
  announcement as a timing guarantee.

For maintenance, agree on the window, notify players, use the deployment's
backup and shutdown procedure, and verify recovery afterward. This guide
does not execute or recommend experimenting with shutdown commands on live.

## 11. Closing a support case

- Confirm the result with the player and, where appropriate, after relogging.
- Record the character, zone/instance, relevant IDs, action, and outcome.
- Check that no duplicate replacement/reward was created.
- End spectating and restore any temporary GM state you changed.
- Record remaining test entities and coordinate cleanup.
- Return to civilian mode when elevated permissions are no longer needed.

For more context, see the
[architecture guide](./DarkflameServer%20Architecture%20and%20Repository%20Structure.md),
[protocol/gameplay guide](./DarkflameServer%20Client-Server%20Protocol%20and%20Gameplay.md),
and [complete table reference](../LEGO%20Universe%20CDClient%20Table%20Reference.md).
