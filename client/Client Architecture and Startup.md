# Client architecture and startup

[Client overview](./README.md) | [Networking](./Client%20Networking.md) | [Server contract](./Server%20Contract.md)

## Files of an installation

A complete client installation has this layout:

| Path | Content |
| --- | --- |
| `legouniverse.exe` | The game (Windows, 32-bit, about 23 MB, file date 1 November 2011). Gamebryo, Havok, Scaleform, RakNet, Lua, zlib, TinyXML, and Expat are linked into it. |
| `*.dll`, `awesomiumprocess.exe` | Middleware that ships separately: FMOD, Bink, Awesomium, ICU, STLport, D3DX9, XInput, and LEGO's `cop.dll`. See [Client libraries](./Client%20Libraries.md). |
| `boot.cfg` | Server addresses, service URLs, and locale. Read before anything else. |
| `lwo.cfg.default` | Default player settings: graphics, audio, camera, and key bindings. |
| `locale/locale.xml` | All texts of the game in every supported language (about 9 MB). |
| `res/` | Content: models, textures, animations, worlds, UI, sound, scripts, and the content database `cdclient.fdb`. See [Assets and content data](./Client%20Assets%20and%20Content%20Data.md). |
| `Lwoclient.state` | A CruiseControl.NET build record (project `lwoclient`, build label 2180, build date 2010-07-10). It is a left-over from LEGO's build system and is not needed to run the game. |

Some community distributions add files that are not part of the 2011 release, for example
`legouniverse_mac.exe` (dated 2013) or `boot_backup.cfg` and `boot.cfg.orig` copies.

## Subsystems

The client is one process with one main loop. From the libraries it uses and the data it reads,
the following subsystems can be distinguished; each has its own page:

```text
                         legouniverse.exe
 ┌───────────────────────────────────────────────────────────────┐
 │  Input (XInput, Windows)  ──►  Control schemes / camera       │
 │                                         │                     │
 │  Network (RakNet) ◄──► Object & component model ◄── cdclient  │
 │        ▲                   │        │        │       .fdb     │
 │        │              Lua scripts   │        │                │
 │        │                   │        ▼        ▼                │
 │        │          Physics (Havok)  Render (Gamebryo/D3D9)     │
 │        │                            UI (Scaleform GFx)        │
 │        │                            Audio (FMOD) / Video (Bink)│
 └────────┼──────────────────────────────────────────────────────┘
          ▼
   Auth / world / chat servers
```

- **Object and component model.** Every thing in the world is an object with a 64-bit object
  ID and a template number (LOT). The template's components (render, physics, destructible,
  inventory, script, and about 80 other types) are listed in `cdclient.fdb`. The client builds
  the same component set as the server and fills it with the state the server sends. Component
  class names found in the executable include `RenderComponent`, `SkinnedRenderComponent`,
  `PhysicsComponent`, `RigidBodyPhantomComponent`, `HavokVehicleComponent`,
  `InventoryComponent`, `DestructibleComponent`, `PetComponent`, `VendorComponent`,
  `RebuildComponent`, `ModularBuildComponent`, `ScriptComponent`, and
  `RocketLaunchpadControlComponent`.
- **Rendering, UI, audio, video, input, physics, scripting** — see the pages in the
  [documentation map](./README.md#documentation-map).

## Configuration files

### `boot.cfg`

`boot.cfg` holds the addresses of the services the client contacts. Each entry has the form
`KEY=type:value,`. The type number is the same one LEGO Universe uses for typed key-value data
(LDF) everywhere: `0` text, `1` signed integer, `3` floating point, `5` unsigned integer,
`7` boolean.

| Key | Purpose | Value in the live game (2011) |
| --- | --- | --- |
| `AUTHSERVERIP` | Host name or address of the authentication server. **This is the entry a private server changes.** | `login.lu1.mia.legouniverse.com` |
| `SERVERNAME` | Display name of the server | `Overbuild Universe (US)` |
| `PATCHSERVERIP`, `PATCHSERVERPORT`, `PATCHSERVERDIR` | Patch/content server (HTTP) | `cache.legouniverse.com`, `80`, `luclient` |
| `AKAMAIDLM`, `CPCODE`, `DATACENTERID` | Akamai download manager and CDN settings for patching | `0`, `89164`, `150` |
| `UGCUSE3DSERVICES`, `UGCSERVERIP`, `UGCSERVERDIR` | Service for user-generated content (model images and data) | `1`, `cache.legouniverse.com`, `3dservices` |
| `PASSURL`, `SIGNINURL`, `SIGNUPURL`, `REGISTERURL` | Web pages opened for account functions | LEGO account web pages |
| `CRASHLOGURL` | Address that receives crash reports | `http://services.lego.com/cls.aspx` |
| `LOCALE` | Language | `en_US` |
| `LOGGING` | Log level | `100` |
| `MANIFESTFILE`, `TRACK_DSK_USAGE`, `HD_SPACE_FREE`, `HD_SPACE_USED` | Written by the patcher/launcher | — |

The LEGO web services no longer exist. With a private server, `AUTHSERVERIP` (and usually
`PATCHSERVERIP` and `UGCSERVERIP`) point to the server's address; the other URLs are not needed
to play.

### `lwo.cfg.default` and player settings

`lwo.cfg.default` contains 193 default settings in the same `KEY=type:value` format, grouped by
comments:

| Group | Examples |
| --- | --- |
| `# camera` | `FIELD_OF_VIEW=3:40.0`, `CAMERA_ZOOM_MAX=3:10.0`, `MOUSESCALAR=3:0.00425`, `MOUSE_INVERT` |
| `# audio` | `NDAUDIO_NUM_VOICES=5:256`, category volumes for music, SFX, dialog, ambience, `NDAUDIO_MUTE_ON_UNFOCUS` |
| `# game` | Window (`WINDOWED`, `WIDTH`, `HEIGHT`), graphics quality (`R_...` keys, `HDR`, `UI_AA`), `CONTROL_SCHEME_DEFAULT`, `REMEMBER_LOGIN`, `S_GHOSTING_RADIUS_SCALAR` |
| `# quickbuilds` | Number of bricks shown when quick builds assemble or objects are smashed |
| `# keyboard` | All key bindings (see [Input and camera](./Client%20Input%20and%20Camera.md)) |
| `# driving` | Racing car controls |
| `# gamepad + freecam` | Free camera speeds and damping |
| `# HF` | Settings of the internal level editor ("HF", autosave, spline subdivision) |

The game does not edit the default file. Changed settings are saved per Windows user (see
[files outside the installation](#files-outside-the-installation)).

## Files outside the installation

The client writes to the user's profile, not to its own folder:

| Path | Content |
| --- | --- |
| `%LOCALAPPDATA%\LEGO Software\LEGO Universe\lwo.xml` | The player's settings. XML with one `ConfigurableOption` per key (`name`, `type` as in the cfg files) and one or more `ValueSet` entries; key bindings with alternatives have one `ValueSet` per key. Also stores values detected on first start, such as `AUTO_DETECTED_SETTINGS_SPEC`. |
| `%LOCALAPPDATA%\LEGO Software\LEGO Universe\<character name>\lwo_override.xml` | Settings that differ for one character ("Custom settings for this character"), in the same format. A folder is created per character that has played. |
| `%LOCALAPPDATA%\LEGO Software\LEGO Universe\Log Files\` | One log per start: `log_legouniverse_<MM-DD-YY>_<HH-MM-SS>__<process ID>.log` |
| `<Documents>\NetDevil\LEGO Universe\Screenshots` | Screenshots (`TAKE_SCREENSHOT`, format chosen by `SCREENSHOT_FORMAT`). The executable contains the path `%s\NetDevil\LEGO Universe\Screenshots`; the base folder is presumably the user's documents folder. |

Deleting `lwo.xml` restores the defaults from `lwo.cfg.default`.

## Startup sequence

The order below is reconstructed from the configuration, the front-end UI files, and the
messages the client exchanges with a server.

1. **Read `boot.cfg`** and the locale. Load `locale.xml` for the chosen language.
2. **Patcher (live game only).** The original launcher compared the installation with a manifest
   on the patch server and downloaded changed files. Private servers usually skip this; the
   client also starts without a reachable patch server.
3. **Initialize subsystems:** create the Direct3D 9 device ("Create D3D9 instance..." in the
   log), load shaders, FMOD with the front-end banks, Scaleform, and open `cdclient.fdb`.
4. **Front end** (Scaleform movies in `res/ui/frontend`): intro movie, EULA/terms of service
   (`eulatos.gfx`; the client keeps checksums of the accepted texts), login screen
   (`loginscreen.gfx`).
5. **Login:** connect to the auth server from `boot.cfg`, send name and password, receive a
   session key and a world server address. See [Networking](./Client%20Networking.md).
6. **Character selection and creation** (`characterselection.gfx`, `charactercreation.gfx`,
   `facecreate.gfx`). Names are suggested from `res/names/minifigname_*.txt`.
7. **Zone loading** (`loadingscreen.gfx`): load the zone file named by the server, its scenes,
   terrain and objects, then report to the server that loading is complete.
8. **In game:** HUD and the main game loop until the player logs out, switches worlds (back to
   step 7 with another server), or the connection is lost.

### Game states

The UI and scripts switch between named game states. Client scripts call
`UI:SendMessage("pushGameState", ...)` 32 times and `popGameState` 25 times, for example to
enter minigames, build mode, or cinematics and then return. The state stack decides which UI
layers are visible and which control scheme is active.

## Logging and error reporting

- The log level comes from `LOGGING` in `boot.cfg`.
- Each log line has tab-separated fields: time, level, category, message. Level `2` is
  information, `3` a warning, `4` a note about data; categories include `GUI` (messages from the
  Scaleform movies), `RESOURCE` (file loading and zone loading), and an empty category for the
  core and network code.
- A normal login and zone entry looks like this in the log (account, key, and addresses
  removed):

  ```text
  2   Attempting to connect to Auth...
  2   RakNet base connection to Auth acquired.  Sending version...
  2   Connection to Auth confirmed. (NetID 0)
  2   Submitting Login info to Auth...
  2   Attempting to connect to World...
  2   RakNet base connection to World acquired.  Sending version...
  2   Auth rejected/terminated connection.          (expected: the auth connection is closed)
  2   Connection to World confirmed. (NetID 1)
  2   Submitting Validation to World... (accnt: ..., key: ...)
  2   Received TransferToWorld (ip ..., port 3006)
  2   Connection to 'Unknown Server' Dropped. (... Port 3000, Reason: 2)
  2   Connection to World confirmed. (NetID 2)
  2   Submitting Validation to World... (accnt: ..., key: ...)
  2   Received Load Zone, ID (1151:2:0)                (map ID : instance : clone)
  2   RESOURCE  LoadThread_Run: MSG_LOAD_ZONE: (zone 1151:2:0, ...)
  2   RESOURCE  LoadThread_DoZoneLoadPart2: (zone 1151:2:0, file {maps/.../....luz} ...)
  2   RESOURCE  LoadThread_FinishLoadingZone: (...)
  ```

  The log is the first place to look when a server does not behave as the client expects; see
  [Troubleshooting](./Client%20Troubleshooting.md).
- `RESOURCE` warnings about missing files (for example `ResMgr could not find file:
  mesh\miscellaneous\Login.NIF`) and many `GUI` warnings ("... had no listeners") also appear
  in a working installation and are harmless.
- After a crash, the client builds an HTML crash report from `res/crashsubmit.inc` and sends it to
  `CRASHLOGURL`. `res/bugsubmit.inc` is the template for in-game bug reports. A full minidump
  option (`DEBUG_FULLMINIDUMP`) exists in the executable.
- In-game help and reports use `helpmenu.gfx` and `helpreportdialog.gfx`; the
  "top 5 issues" request is a server message (`MSG_WORLD_CLIENT_TOP_5_ISSUES_REQUEST`).

## Developer features left in the client

The release build still contains several internal tools. They are not needed to play and most
require a server-side GM level:

- `res/macros`: 266 `.scm` files, each a list of slash commands run in sequence, for example
  `agstart.scm` (`/resetmissions`, `/tele ...`, `/addmission 173`, ...). The commands
  themselves are executed by the server.
- Debug UI movies: `objectdebugger.gfx`, `uidebugger.gfx`, `testcasemanager.gfx`,
  `missioneditor.gfx`.
- The level editor settings (`HF_...`) and messages to push, pull, or reload maps
  (`MSG_WORLD_CLIENT_SLASH_PUSH_MAP`, `..._PULL_MAP`, `..._RELOAD_MAP`).
