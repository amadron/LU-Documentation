# Client user interface

[Client overview](./README.md) | [Rendering](./Client%20Rendering.md) | [Scripting](./Client%20Scripting.md)

## Technology

The whole user interface is made of **Scaleform GFx** movies: Flash files (ActionScript) that
were converted to `.gfx` and are played inside the game. Images used by a movie are stored next
to it as `.dds` textures named after the movie (for example `inventory_i12.dds`). The game code
and the movies talk through Flash's `ExternalInterface`: the engine calls functions in a movie,
and the movie calls back into the engine. Client Lua scripts reach the UI with
`UI:SendMessage(name, data)`.

An embedded web browser, **Awesomium** (Chromium-based), shows HTML pages inside the game. The
executable creates web views and forwards keyboard and mouse input to them
(`awe_webview_inject_*` functions). It was used for web content such as account pages and
news.

## Movies in `res/ui`

| Folder | Movies | Purpose |
| --- | --- | --- |
| `frontend` | 20 | Everything before entering a world: login, EULA and terms, character selection and creation, face editor, loading screen, front-end help, free-trial screens |
| `ingame` | 135 (+2 in `uicomponents`) | HUD and all windows during play |
| `3d` | 11 (+ `lupstation`, `nexustower`) | Movies drawn onto 3D objects: scoreboards, rocket signs, quick-build requirements, loot name billboards |
| `brickbybrick` | 2 | Helpers for the brick-building mode |
| `fontlibs` | 4 | Font libraries for English, German, Polish, Russian |
| top level | 5 | Shared components: `clik_components`, `genericpopup`, `generictextfield`, `messagebox`, `gfxfontlib` |

Bitmap fonts for debug text are in `res/fonts` (`.nff`: Arial, Arial Rounded, Lucida Console).

### In-game windows by area

| Area | Movies |
| --- | --- |
| HUD | `hud`, `actionbar`, `statusbar`, `healthbar`, `minimap`, `chatbox`, `chatbubble`, `activebuffsindicator`, `weaponcount`, `tooltip`, `itemrollover`, `hovertip` |
| Character | `inventory`, `passport`, `achievements`, `bank`, `stacksplitter`, `itembinding`, `inspectplayer` |
| Missions | `mission`, `missiondisplay`, `missiontaskheader`, `missioncompletemessage`, `kitmission`, `factionmission`, `storybox`, `progresstip` |
| Social | `friends`, `friendsinvite`, `teaminvite`, `teamoptions`, `teamstatus`, `teamtextinput`, `guild`, `guildcreate`, `mail`, `mailnotification`, `trade` |
| Vendors | `vendorwindow`, `vendorconfirmation`, `donationvendor` |
| Navigation | `universemap`, `multizonenavigator`, `multizonedetails`, `zonesummary`, `instanceenter`, `instancelobby`, `instanceloading`, `instancestart`, `instancerewards`, `instancehelp` |
| Activities | Racing (`raceactionbar`, `racescoreboard`, `racespeedometer`, `raceposition`, `racewrongway`, ...), survival (`survivalscoreboard`, `survivalsummary`), shooting gallery (`sg_scoreboard`), foot race, leaderboards, `battlewavesscoreboard` |
| Building and properties | `propertyedit*` (10 movies), `propertymanagement`, `propertynavigator`, `propertyvendor`, `propertydetails`, `brickpullout`, `budgetmeter`, `modularbuildpartslist`, `modbuildconfirm`, `choicebuild`, `behavioreditor` |
| Pets | `pettaming`, `pettamingactions`, `petmenu`, `petname` |
| Dialogs | `messagebox`, `choicebox`, `confirmationbox`, `generictimedconfirmation`, `respawndialog` |
| System | `optionsmenu`, `keymap`, `helpmenu`, `helpreportdialog`, `news`, `credits`, `frameratewarning`, `performancewarning*` |
| Free trial | `freetrial*` (6 movies) |
| Developer | `objectdebugger`, `uidebugger`, `testcasemanager`, `missioneditor`, `missioneditorgridbox`, `dpsgui` |

## Layout and settings

- `res/ui/ingame/hud.xml` places HUD regions on the screen (about 60 named regions, such as
  `actionbar`, `chatbox`, `minimap`-related task headers, `teamStatus`, `petTaming`,
  `budgetMeter`, `RaceBoost`). Each region has anchors (`center`, `top`, `bottom`, ...) and
  offsets.
- `res/uisettings.xml` defines HUD window frames, sizes, and anchors. Its header states that
  these windows *can* be edited by the end user.
- `res/ui/ingame/settings.xml`, `blocksdef.xml`, and `res/ui/frontend/bguisettings.xml` hold
  further UI settings.
- `UI_AA` and `R_UILOWRES` in the player settings switch UI anti-aliasing and low-resolution UI
  textures.

## Cursors

The 31 `.cur` files in `res` are the mouse cursors. Many describe what clicking an object will
do: `interactive`, `mission`, `mission_complete`, `vendor`, `rebuild`, `shooting_gallery`,
`guild`, and gray variants (`*_gray.cur`) when the action is not available. Others are used
while building: `hand_open`, `hand_closed`, `brick_mode`, `Brick Edit`, `clone`, `paint`,
`hinge`, `put_away`, `behavior`. The choice of cursor follows the object's "pick type", which
client scripts can override (`onGetOverridePickType`, `SetPickType`).

## How the UI is driven

The UI reacts to three kinds of input:

1. **Local state** of the client (inventory contents, mission states, settings).
2. **Server messages.** Many windows open because the server asks for it, for example a vendor
   window when the player uses a vendor, a message box (`DISPLAY_MESSAGE_BOX`), a mission offer
   (`OFFER_MISSION`), or a zone summary. The player's answer goes back to the
   server (`MESSAGE_BOX_RESPOND`, `CHOICE_BOX_RESPOND`, `RESPOND_TO_MISSION`).
3. **Client scripts.** Activity scripts update scoreboards and HUD elements with
   `UI:SendMessage`. The most frequent targets in the shipped scripts are `SiegeUI` (39),
   `pushGameState` (32), `ToggleSurvivalScoreboard` (30), `UpdateSG` (28), `popGameState` (25),
   `UpdateSurvivalScoreboard` (18), `ToggleLeaderboard` (15), and `UpdateInstanceLobby` (11).

For a server this means: windows that depend on server data only work if the server sends the
expected game messages with valid content IDs. For example, a vendor window stays empty if the
vendor's inventory is not serialized, and mission texts only appear if the mission ID exists in
the client's `cdclient.fdb` and `locale.xml`.

## Localized UI

The movies contain text IDs, not texts. The text for each ID is taken from `locale.xml` in the
current language (see [Assets and content data](./Client%20Assets%20and%20Content%20Data.md#localization)).
Some movies and images have language-specific copies in `_loc` folders (for example
`ui/ingame/_loc/de_de`).
