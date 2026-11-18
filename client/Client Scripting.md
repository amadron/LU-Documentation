# Client scripting

[Client overview](./README.md) | [User interface](./Client%20User%20Interface.md) | [Server contract](./Server%20Contract.md)

## Lua in LEGO Universe

Much of LEGO Universe's object behavior was written in **Lua**. The client contains 1,798 `.lua`
files in `res/scripts`. Not all of them run on the client: in the original game the servers also
ran Lua, and the client ships both kinds.

| Folder | Files | Content |
| --- | --- | --- |
| `client` | 531 | Client scripts: local effects, UI updates, interaction checks |
| `02_client` | 146 | More client scripts (later content) |
| `ai` | 976 | Mostly server-side object and NPC scripts, grouped by world (`ag`, `fv`, `gf`, `ns`, `np`, ...) and activity (`minigame`, `pets`, `act`) |
| `zone` | 55 | Zone control scripts |
| `equipmentscripts`, `equipmenttriggers` | 24, 37 | Scripts attached to equipped items |

Each object template can name two scripts in the `ScriptComponent` table of the content database:
`script_name` (server) and `client_script_name` (client). In the 2011 data, 1,485 script
components exist; 1,186 name a server script and 860 name a client script. Example:
`scripts\ai\MINIGAME\SG_GF\SERVER\SG_CANNON.lua` on the server and
`scripts\ai\MINIGAME\SG_GF\CLIENT\SG_CANNON_CLIENT.lua` on the client.

**DarkflameServer does not run the Lua server scripts.** It reimplements their behavior as C++
classes in `dScripts`, registered by script path. The **client still runs its own client
scripts** unchanged, so a server has to produce the events those scripts wait for.

## Script lifecycle and callbacks

A script is a set of functions that the engine calls when something happens to its object. The
most frequent callback definitions in all shipped scripts:

| Callback | Count | Called when |
| --- | ---: | --- |
| `onStartup` | 1,041 | The object is created |
| `onTimerDone` | 310 | A timer started by the script ends |
| `onCollisionPhantom` / `onOffCollisionPhantom` | 290 / 57 | Something enters / leaves a trigger volume |
| `onNotifyObject` | 194 | Another object sends a notification |
| `onClientUse` / `onUse` | 149 / 121 | The player uses (clicks) the object |
| `onProximityUpdate` | 120 | Something enters or leaves a proximity radius |
| `onRebuildNotifyState` | 98 | A quick build changes state |
| `onRenderComponentReady` | 95 | The object's model is loaded |
| `onCollision` / `onOffCollision` | 74 / 36 | Physical collision |
| `onGetOverridePickType`, `onGetPriorityPickListType` | 73 each | The cursor hovers over the object |
| `onFireEvent` | 65 | A named event is fired at the object |
| `onCheckUseRequirements` | 58 | Before use, to decide if it is allowed |
| `onNotifyClientObject` | 56 | The **server** sends a notification to the client object |
| `onMessageBoxRespond` | 55 | The player answers a message box |
| `onScriptNetworkVarUpdate` | 49 | A **network variable** sent by the server changes |
| `onPlayerLoaded`, `notifyPlayerReady`, `onPlayerReady` | 39, 26, 13 | The local player finished loading |
| `onFireEventServerSide` | 35 | (server scripts) an event fired by a client |
| `onScopeChanged` | 24 | The object enters or leaves the player's scope |
| `onShutdown` | 31 | The object is destroyed |

## Engine API

Scripts call into the engine through global objects and through methods on game objects.

### Global objects

| Object | Most used functions (count) |
| --- | --- |
| `GAMEOBJ` | `GetTimer` (1,423), `GetObjectByID` (574), `GetLocalCharID` (509), `GetZoneControlID` (503), `GetControlledID` (237), `DeleteObject` (170), `GetWaypointPos`, `GetSystemTime`, `GenerateSpawnedID`, `GetDBTable` |
| `UI` | `SendMessage` (533), `SendChat`, `DisplayToolTip`, `DisplayTripleBuild` |
| `LEVEL` | `GetSpawnerByName` (78), `SetLights` (38), `CLUTEffect` (28), `AttachCameraParticles`, `FadeEffect`, `SetSkyDome`, `GetPathWaypoints`, `GetSceneAtPos`, `GetCinematicInfo`, `ModifyEnvironmentSettings`, `GetCurrentZoneID` |
| `CAMERA` | `SnapCameraToPlayer`, `SetRenderCamera`, `ActivateCamera`, `SetToPrevGameCam`, `SetCameraZoom`, `SetCameraLookAtPoint`, `AttachCameraToObj` |
| `SOUND` | `ActivateNDAudioMusicCue`, `DeactivateNDAudioMusicCue`, `FlashNDAudioMusicCue`, `PlaySequence`, `StopSequence` |

### Object methods

Methods on objects are written `obj:Name{ key = value, ... }` with a table of named arguments.
Most of them have the same names as **game messages** of the network protocol (`PlayFXEffect` –
`PLAY_FX_EFFECT`, `FireEventServerSide` – `FIRE_EVENT_SERVER_SIDE`). Most calls are handled on the
client; a few, such as `FireEventServerSide`, result in a message to the server. Most frequent in
client scripts:

| Method | Count | Effect |
| --- | ---: | --- |
| `PlayAnimation` | 226 | Plays an animation on the object |
| `PlayFXEffect` / `StopFXEffect` | 218 / 57 | Starts / stops a visual effect |
| `GetObjectsInGroup` | 110 | Finds objects by group name |
| `NotifyObject` | 106 | Sends a notification to another object |
| `DisplayChatBubble` | 100 | Shows a speech bubble |
| `GetMissionState` | 86 | Reads the player's mission state (from data the server sent) |
| `SetVisible` | 74 | Shows or hides the object |
| `SetUserCtrlCompPause` | 65 | Pauses player control |
| `FireEventServerSide` | 52 | Sends a named event **to the server** |
| `SendLuaNotificationRequest` / `Cancel` | 52 / 50 | Subscribes to engine events of another object |
| `SetProximityRadius` | 50 | Creates a proximity radius |
| `GetFlag` / `SetFlag` | 44 / 21 | Reads / sets player flags |
| `TerminateInteraction` | 34 | Ends an interaction |
| `DisplayTooltip`, `DisplayMessageBox` | 29, 15 | Shows UI |

## Communication between client and server scripts

Client and server scripts of the same object cooperate through four channels:

| Channel | Direction | Mechanism |
| --- | --- | --- |
| Network variables | Server → client | The server sets a variable on the object; the client receives `SCRIPT_NETWORK_VAR_UPDATE` and calls `onScriptNetworkVarUpdate`; the client reads it with `GetNetworkVar`. Initial values are sent in the script component during construction. |
| Client notifications | Server → client | `NOTIFY_CLIENT_OBJECT` with a name and parameters → `onNotifyClientObject` |
| Client-side events | Server → client | `FIRE_EVENT_CLIENT_SIDE` → `onFireEvent` on the client |
| Server-side events | Client → server | `FireEventServerSide` → `FIRE_EVENT_SERVER_SIDE` → the server script's `onFireEventServerSide` |

Example: a minigame's server script counts points and sets a network variable `score`; the
client script receives the update and calls `UI:SendMessage("UpdateSG", ...)` to refresh the
scoreboard.

## What this means for a server

- Client scripts are **content**. A server cannot change them, but it must feed them: the
  network variable names, notification names, and event names a client script expects are part
  of the contract for that object. When a feature "does nothing" on a private server, the client
  script is often waiting for a variable or notification that the server-side reimplementation
  does not send.
- The client script source in `res/scripts` is the best reference for these names. Reading the
  client script next to the matching server script (`script_name`) shows both sides of the
  exchange.
- Initial network variables are part of the object's construction data (script component); later
  changes must be sent as `SCRIPT_NETWORK_VAR_UPDATE`.
