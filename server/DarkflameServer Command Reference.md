# DarkflameServer Command Reference

Complete inventory of slash commands registered by the local DarkflameServer checkout at revision `8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4`.

**147 command entries**, **205 unique registered spellings** (including aliases): 105 server-handled entries and 42 entries marked client-handled.

## How to read this reference

- Commands and aliases are shown with their leading `/`. Preserve spelling and case, including `/removeIgnore` and `/victory!`.
- Minimum levels come from command registration, not historical role descriptions. An omitted registration level defaults to `OPERATOR` (9).
- The description column reproduces the short help text from the registry; it is not a separately verified argument specification. Some source help is incomplete or misleading. For checked syntax, target behavior, and safety notes, see the [Gamemaster Guide](./DarkflameServer%20Gamemaster%20Guide.md).
- Use `/help`, `/help 2`, or `/help command` in game to inspect accessible entries and their longer source descriptions. Do not include `/` before the command name passed to `/help`.
- Client-handled entries have an empty server handler. Their registration does not prove that a client feature or historical external website still works, nor is this a complete enumeration of all commands a client might implement.
- This is a source-derived reference. No commands were executed on a live server to generate it.

## GM levels

| Level | Name |
|---:|---|
| 0 | `CIVILIAN` |
| 1 | `FORUM_MODERATOR` |
| 2 | `JUNIOR_MODERATOR` |
| 3 | `MODERATOR` |
| 4 | `SENIOR_MODERATOR` |
| 5 | `LEAD_MODERATOR` |
| 6 | `JUNIOR_DEVELOPER` |
| 7 | `INACTIVE_DEVELOPER` |
| 8 | `DEVELOPER` |
| 9 | `OPERATOR` |

The active character level must meet the command threshold and is bounded by the account authorization. Additional build/configuration checks can apply. In non-developer builds, the level-change handler forces accounts whose maximum is `JUNIOR_DEVELOPER` to civilian mode.

## Duplicate alias: `/kick`

Registration is first-wins for executable aliases. `/kick` is registered first as the level-2 server disconnect command. The later client-handled team-kick entry cannot replace that spelling; its other spellings remain registered and are listed below under `/kickplayer`. The in-game help index is maintained separately and can therefore be misleading for this collision.

## Server-handled commands

These include administrative, moderation, developer/debug, and ordinary player commands. Registration does not imply a command is safe for production. Commands such as inventory deletion, arbitrary execution, deliberate crashes, mass gameplay changes, and shutdown are not routine support tools.

| Command | Other active aliases | Min. GM level | Source help description | Registration |
|---|---|---:|---|---|
| `/activatespawner` | - | 8 | Activates spawner by name | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L299) |
| `/addfaction` | - | 8 | Add the faction to the users list of factions | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L749) |
| `/addmission` | - | 8 | Accepts the mission, adding it to your journal. | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L308) |
| `/announce` | - | 8 | Send and announcement | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L219) |
| `/approveproperty` | - | 5 | Approves a property | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L869) |
| `/attackimmune` | - | 8 | Make yourself immune to attacks | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L896) |
| `/ban` | - | 4 | Bans a user from the server | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L860) |
| `/barfight` | - | 8 | Turns all players&#39; pvp mode on | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L1486) |
| `/boost` | - | 8 | Adds boost to a vehicle | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L317) |
| `/buff` | - | 8 | Applies a buff | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L335) |
| `/buffme` | - | 8 | Sets health, armor, and imagination to 999 | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L344) |
| `/buffmed` | - | 8 | Sets health, armor, and imagination to 9 | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L353) |
| `/castskill` | - | 8 | Casts the skill as the player | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L794) |
| `/clearflag` | - | 8 | Clear a player flag | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L362) |
| `/completemission` | - | 8 | Completes the mission | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L371) |
| `/crash` | `/pumpkin` | 9 | Crash the server | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L776) |
| `/createprivate` | - | 8 | Creates a private zone with password | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L380) |
| `/credits` | - | 0 | Displays DLU Credits | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L980) |
| `/debugui` | - | 8 | Toggle Debug UI | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L389) |
| `/deleteinven` | - | 8 | Delete all items from a specified inventory | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L803) |
| `/despawn` | - | 8 | Despawns an object by id | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L1494) |
| `/die` | - | 0 | Smashes the player | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L998) |
| `/dismount` | - | 8 | Dismounts you from the vehicle or mount | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L398) |
| `/execute` | `/exec` | 8 | Execute commands with modified context (Minecraft-style) | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L812) |
| `/findplayer` | - | 2 | Find the World Server a player is in if they are online | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L951) |
| `/fix-stats` | - | 0 | Resets skills, buffs, and destroyables | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L1043) |
| `/fly` | - | 8 | Toggle flying | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L887) |
| `/forcesave` | `/force-save` | 8 | Force save your player | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L416) |
| `/freecam` | - | 8 | Toggles freecam mode | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L425) |
| `/freemoney` | `/givemoney`, `/money`, `/givecoins`, `/coins` | 8 | Give yourself coins | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L434) |
| `/getadjacentscenes` | `/adjacentscenes` | 8 | Get all scenes adjacent to your current scene | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L830) |
| `/getfactions` | - | 8 | Shows the player&#39;s factions | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L758) |
| `/getnavmeshheight` | - | 8 | Display the navmesh height | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L443) |
| `/getscene` | `/scene` | 8 | Get the current scene ID and name at your position | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L821) |
| `/giveuscore` | - | 8 | Gives uscore | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L452) |
| `/gmadditem` | `/give` | 8 | Give yourseld an item | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L461) |
| `/gmimmune` | - | 8 | Sets the character&#39;s GMImmune state | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L905) |
| `/gminvis` | - | 1 | Toggles invisibility for the character | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L914) |
| `/help` | `/h` | 0 | Display command info | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L971) |
| `/info` | - | 0 | Displays server info | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L989) |
| `/inspect` | - | 8 | Inspect an object | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L470) |
| `/instanceinfo` | - | 0 | Display LWOZoneID info for the current zone | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L1079) |
| `/join` | - | 0 | Join a private zone | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L1052) |
| `/kick` | - | 2 | Kicks the player off the server | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L842) |
| `/kill` | - | 8 | Smash a user | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L201) |
| `/leave-zone` | `/leavezone` | 0 | Leave an instanced zone | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L1061) |
| `/list-spawns` | `/listspawns` | 8 | List spawn points for players | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L479) |
| `/locrow` | - | 8 | Prints the your current position and rotation information to the console | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L488) |
| `/lookup` | - | 8 | Lookup an object | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L497) |
| `/mailitem` | - | 3 | Mails an item to the given player | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L851) |
| `/metrics` | - | 8 | Display server metrics | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L210) |
| `/mute` | - | 6 | Mute a player | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L878) |
| `/ping` | - | 0 | Displays your average ping. | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L1007) |
| `/playanimation` | `/playanim` | 8 | Play an animation with given ID | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L506) |
| `/playeffect` | - | 8 | Plays an effect | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L515) |
| `/playlvlfx` | - | 8 | Plays the level up animation on your character | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L524) |
| `/playrebuildfx` | - | 8 | Plays the quickbuild animation on your character | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L533) |
| `/pos` | - | 8 | Displays your current position in chat and in the console | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L542) |
| `/pvp` | - | 0 | Toggle your PVP flag | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L1016) |
| `/refillstats` | - | 8 | Refills health, armor, and imagination to their maximum level | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L551) |
| `/reforge` | - | 8 | Reforges an item | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L560) |
| `/reloadconfig` | `/reload-config` | 8 | Reload Server configs | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L407) |
| `/reportproxphys` | - | 9 | Display proximity sensor info | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L272) |
| `/requestmailcount` | `/checkmail` | 0 | Gets the players mail count | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L1025) |
| `/resetmission` | - | 8 | Sets the state of the mission to accepted but not yet started | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L569) |
| `/resurrect` | - | 8 | Resurrects the player | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L1070) |
| `/rollloot` | `/roll-loot` | 8 | Simulate loot rolls | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L785) |
| `/rot` | - | 8 | Displays your current rotation in chat and in the console | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L578) |
| `/runmacro` | - | 8 | Run a macro | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L587) |
| `/setannmsg` | - | 8 | Sets the message of an announcement | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L237) |
| `/setanntitle` | - | 8 | Sets the title of an announcement | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L228) |
| `/setcontrolscheme` | - | 8 | Sets the character control scheme to the specified number | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L596) |
| `/setcurrency` | `/setcoins` | 8 | Sets your coins | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L605) |
| `/setfaction` | - | 8 | Set the players faction | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L740) |
| `/setflag` | - | 8 | Set a player flag | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L614) |
| `/setgmlevel` | `/makegm`, `/gmlevel` | 0 | Change the GM level of your character | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L174) |
| `/setinventorysize` | `/setinvsize`, `/setinvensize` | 8 | Set your inventory size | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L623) |
| `/setlevel` | - | 8 | Set player level | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L722) |
| `/setminifig` | - | 1 | Alters your player&#39;s minifig | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L254) |
| `/setname` | - | 8 | Sets a temporary name for your player | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L923) |
| `/setrewardcode` | - | 8 | Set a reward code for your account | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L767) |
| `/setskillslot` | - | 8 | Set an action slot to a specific skill | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L731) |
| `/setuistate` | - | 8 | Changes UI state | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L632) |
| `/showall` | - | 2 | Show all online players across World Servers | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L942) |
| `/shutdown` | - | 8 | Shuts this world down | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L1477) |
| `/shutdownuniverse` | - | 9 | Sends a shutdown message to the master server | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L246) |
| `/spawn` | - | 8 | Spawns an object at your location by id | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L641) |
| `/spawngroup` | - | 8 | No short help text provided in the registry. | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L650) |
| `/spawnphysicsverts` | - | 8 | Spawns a 1x1 brick at all vertices of phantom physics objects | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L281) |
| `/spectate` | `/follow` | 2 | Spectate a player | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L960) |
| `/speedboost` | - | 8 | Set the players speed multiplier | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L659) |
| `/startcelebration` | - | 8 | Starts a celebration effect on your character | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L668) |
| `/stopeffect` | - | 8 | Stops the given effect | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L677) |
| `/teleport` | `/tele`, `/tp` | 6 | Teleports you to a position or a player to another player. | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L290) |
| `/testmap` | `/tm` | 1 | Transfers you to the given zone | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L263) |
| `/title` | - | 8 | Give your character a title | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L933) |
| `/toggle` | - | 8 | Toggles UI state | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L686) |
| `/togglenameplate` | `/tnp` | 0 | Toggle the visibility of your nameplate. This must be enabled by a server admin to be used. | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L183) |
| `/toggleskipcinematics` | `/tsc` | 0 | Toggle Skipping Cinematics | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L192) |
| `/tpall` | - | 8 | Teleports all characters to your current position | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L695) |
| `/triggerspawner` | - | 8 | Triggers spawner by name | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L704) |
| `/unboost` | - | 8 | Removes a passive vehicle boost | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L326) |
| `/unlock-emote` | `/unlockemote` | 8 | Unlocks for your character the emote of the given id | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L713) |
| `/uptime` | - | 8 | Display the time the current world server has been active | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L1088) |
| `/who` | - | 0 | Displays all players on the instance | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L1034) |

## Entries marked client-handled

The server registers these with `GMZeroCommands::ClientHandled`, whose body is empty. The level column is the server registration threshold, not a guarantee of how every client processes the input.

| Command | Other active aliases | Min. GM level | Source help description | Registration |
|---|---|---:|---|---|
| `/addfriend` | - | 0 | &#91;name&#93; Add a player to your friends list. | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L1432) |
| `/addignore` | - | 0 | &#91;name&#93; Add a player to your ignore list. | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L1423) |
| `/backflip` | - | 0 | Do a flip! | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L1171) |
| `/camp` | `/logoutcharacter` | 0 | Returns you to the character select screen. | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L1189) |
| `/cancelqueue` | - | 0 | Cancel Your position in the queue if you are in one. | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L1342) |
| `/clap` | - | 0 | A round of applause! | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L1180) |
| `/cringe` | - | 0 | I don&#39;t even want to talk about it... | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L1324) |
| `/cry` | - | 0 | Show everyone your &#39;Aw&#39; face. | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L1441) |
| `/dance` | - | 0 | Dance &#39;til you can&#39;t dance no more. | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L1288) |
| `/exit` | `/quit` | 0 | Exit to desktop | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L1144) |
| `/faq` | `/faqs` | 0 | Show the LU FAQ Page | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L1099) |
| `/forums` | - | 0 | Show the LU Forums! | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L1135) |
| `/gasp` | - | 0 | Oh my goodness! | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L1414) |
| `/giggle` | - | 0 | A good little chuckle | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L1450) |
| `/invite` | `/inviteteam`, `/teaminvite`, `/tinvite` | 0 | &#91;name&#93; Invite a player to your team. | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L1279) |
| `/kickplayer` | `/teamkickplayer`, `/tkick`, `/tkickplayer` | 0 | &#91;name&#93; Kick a player from your current team. (Alias /kick is shadowed by an earlier registration.) | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L1360) |
| `/leader` | `/setleader`, `/teamsetleader`, `/tleader`, `/tsetleader` | 0 | &#91;name&#93; Set the leader for your current team. | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L1315) |
| `/leave` | `/leaveteam`, `/teamleave`, `/tleave` | 0 | Leave your current team. | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L1243) |
| `/loc` | `/locate`, `/location` | 0 | Output your current location on the map to the chat box. | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L1216) |
| `/logout` | `/logoutaccount` | 0 | Returns you to the login screen. | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L1225) |
| `/minigames` | - | 0 | Show the LEGO minigames page! | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L1126) |
| `/perfoptionshigh` | - | 0 | Sets the default high-spec performance options in the cfg file | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L1405) |
| `/perfoptionslow` | - | 0 | Sets the default low-spec performance options in the cfg file | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L1351) |
| `/perfoptionsmid` | - | 0 | Sets the default medium-spec performance options in the cfg file | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L1396) |
| `/recommendedperfoptions` | - | 0 | Sets the recommended performance options in the cfg file | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L1306) |
| `/removefriend` | - | 0 | &#91;name&#93; Removes a player from your friends list. | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L1261) |
| `/removeIgnore` | - | 0 | &#91;name&#93; Removes a player from your ignore list. | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L1468) |
| `/s` | `/say` | 0 | Say something outloud so that everyone can hear you | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L1198) |
| `/salute` | - | 0 | For those about to build... | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L1459) |
| `/setloot` | `/teamsetloot`, `/tloot`, `/tsetloot` | 0 | &#91;rr&#124;ffa&#93; Set the loot for your current team (round-robin/free for all). | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L1252) |
| `/shop` | `/store` | 0 | Show the LEGO shop page. | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L1117) |
| `/shrug` | - | 0 | I dunno... | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L1234) |
| `/sigh` | - | 0 | Another day, another brick. | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L1297) |
| `/talk` | - | 0 | Jibber Jabber | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L1333) |
| `/team` | `/t` | 0 | Send a message to your teammates. | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L1108) |
| `/tell` | `/w`, `/whisper` | 0 | Send a private message to another player. | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L1207) |
| `/thanks` | - | 0 | Express your gratitude for another. | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L1369) |
| `/thumb` | `/thumbs`, `/thumbsup` | 0 | Oh, yeah! | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L1153) |
| `/victory!` | - | 0 | Victory! | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L1162) |
| `/wave` | - | 0 | Wave to other players. | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L1378) |
| `/why` | - | 0 | Why&#124;!?!! | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L1387) |
| `/yes` | - | 0 | Aye aye, captain! | [source](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp#L1270) |

## Implementation and related documentation

- [Registration, first-wins alias handling, permission checks, and help](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp)
- [Default command permission level](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.h)
- [GM level enum](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dCommon/dEnums/eGameMasterLevel.h)
- [Developer/GM handlers](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommands/DEVGMCommands.cpp)
- [Moderation handlers](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommands/GMGreaterThanZeroCommands.cpp)
- [Player handlers and empty client handler](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommands/GMZeroCommands.cpp)
- [Gamemaster Guide](./DarkflameServer%20Gamemaster%20Guide.md)
- [Database table overview](../db/README.md)
