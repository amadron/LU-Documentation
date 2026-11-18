# Client input and camera

[Client overview](./README.md) | [Physics and building](./Client%20Physics%20and%20Building.md) | [Networking](./Client%20Networking.md)

## Input devices

- **Keyboard and mouse** through Windows messages.
- **Game controllers** through XInput 1.3 (`xinput1_3.dll`), i.e. Xbox 360-compatible pads.
  23 default bindings use pad buttons (`VK_PAD_A`, `VK_PAD_RSHOULDER`, `VK_PAD_LTHUMB_LEFT`, ...).

## Key bindings

The 125 key bindings in `lwo.cfg.default` map an *action* to one or more keys. `|` separates
alternatives, `+` combines keys: `BBB_COPY=0:VK_LCTRL+VK_C|VK_RCTRL+VK_C`. The in-game key map
(`keymap.gfx`) edits the same actions.

| Group | Actions (default keys) |
| --- | --- |
| Movement | `MOVE_LEFT`/`MOVE_RIGHT`, `BACKWARD_DIR` (S), `STRAFE_*`, `ROTATE_*` (Q/E), `JUMP` (Space), `WALK_MODIFIER` (Shift), `MOVE_AUTORUN` (Num Lock) |
| Actions | `INTERACT` (Shift, right mouse, pad B), `INTERACT_WITH_PLAYER` (Ctrl), `CAST_SKILL`, `CAST_SKILL_MOUSE`, `SKILL1`–`SKILL5` (1–5), `FACTION_SKILL_KEY` |
| Windows | `TOGGLE_INVENTORY` (B), `TOGGLE_PASSPORT` (P), `TOGGLE_MAP` (M), `TOGGLE_NEWS` (N), `TOGGLE_HELP` (H), `TOGGLE_FRIENDSLIST` (F), `TOGGLE_HIDE_INTERFACE` (F10), `TAKE_SCREENSHOT` (Print) |
| Chat | `START_CHATTING` (Enter), `TOGGLE_SPEEDCHAT` (C), `SPEEDCHAT0`–`SPEEDCHAT9` |
| Camera | `CAMERA_ROTATE_*`, `CAMERA_PITCH_*`, `CAMERA_ZOOM_*`, `CAMERA_ASCEND`/`DESCEND` (R/F), `CAMERA_SNAP`, `CAMERA_UNLOCK*` (mouse buttons), `CAMERA_CYCLE_TARGET_AMONG_TEAM` |
| Driving | `DRIVING_VEHICLE_ACCELERATE`/`DECELERATE`/`LEFT`/`RIGHT`, `_BOOST`, `_JUMP`, `_POWERSLIDE`, `_FIRE`, `_RESET`, `_CYCLE_CAMERA`, `_REVERSE_CAMERA` |
| Flying vehicles | `FLYING_VEHICLE_CLIMB`/`DIVE`/`THROTTLE_*` |
| Build mode (BBB) | `BBB_CAMERA_*` (pan, rotate, zoom), `BBB_COPY`, `BBB_CUT`, `BBB_DELETE`, ... |
| Property editing | `PROPERTY_CARRY_PLACE`, `PROPERTY_CARRY_REMOVE`, `PROPERTY_CARRY_PITCH_*`, `PROPERTY_CARRY_YAW_RIGHT` |
| Modular build | `MODULAR_BUILD_CONFIRM` (F12), `MODULAR_BUILD_CANCEL` (Esc) |
| Developer | `FREEZE` (F11), `DEV_EXIT_CINEMATIC` (~), `HVK_MODIFIER`, `ORT_MODIFIER` |

## Control schemes

A *control scheme* decides how input becomes movement. The player chooses a default
(`CONTROL_SCHEME_DEFAULT=0:SCHEME_A`), and the game switches schemes for special situations.
Scheme names in the executable and in DarkflameServer's
[eControlScheme.h](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dCommon/dEnums/eControlScheme.h):

| Scheme | Used for |
| --- | --- |
| `SCHEME_A`, `SCHEME_D`, `SCHEME_E` | Normal walking; the selectable keyboard/mouse styles |
| `SCHEME_GAMEPAD` | Controller |
| `SCHEME_FPS` | First-person/aiming activities (e.g. shooting gallery) |
| `SCHEME_DRIVING` | Racing cars |
| `SCHEME_FLYING` | Flying vehicles |
| `SCHEME_TAMING` (`SCHEME_TAMING_MINIGAME`) | Pet taming |
| `SCHEME_MODULAR_BUILD` | Rocket and car building |
| `SCHEME_WEAR_A_ROBOT` | Possessing another object (name from the server enum) |

The **server** switches schemes with the game message `SET_PLAYER_CONTROL_SCHEME`, for example
when an activity starts and ends. Client scripts can also pause player control
(`SetUserCtrlCompPause`, used 65 times in client scripts) or stun the player (`SetStunned`).

## Camera

Camera types in the executable:

| Camera | Use |
| --- | --- |
| `CAMERA_MAIN_GAME_D`, `CAMERA_MAIN_GAME_E` | Third-person follow camera (default `CAMERA_MAIN_GAME_D`) |
| `CAMERA_MAIN_GAME_VEHICLE`, `..._VEHICLE_BUMPER`, `..._VEHICLE_DRIVER`, `..._VEHICLE_REVERSE` | Racing views, cycled with `DRIVING_VEHICLE_CYCLE_CAMERA` |
| `CAMERA_SHOOTING_GALLERY` | Fixed cannon view in shooting galleries |
| `CAMERA_CINEMATIC` | Camera paths of cinematics |
| `CAMERA_FREE_LOOK` | Free camera (developer/GM), tuned by the `GAMEPAD_FREECAM_*` settings |

Camera defaults: field of view 40°, focal point 2.95 units above the character with an offset of
1.75, maximum zoom 10. Scripts control the camera with `CAMERA:ActivateCamera`,
`SetRenderCamera`, `AttachCameraToObj`, `SetCameraLookAtPoint`, `SetCameraZoom`,
`SetDesiredPitchMin`/`Max`, `SnapCameraToPlayer`, and `SetToPrevGameCam`.

The camera is entirely local. The server only affects it indirectly, through cinematics
(`PLAY_CINEMATIC`/`END_CINEMATIC`), control-scheme changes, and teleports.

## From input to the server

Input is handled locally; the server never receives key presses. What it receives are the
**results**:

| Local action | Sent to the server |
| --- | --- |
| Walking, jumping, driving | Periodic `POSITION_UPDATE` with position, rotation, velocity, and state flags (see [Physics](./Client%20Physics%20and%20Building.md#movement-and-the-server)) |
| Clicking or interacting with an object | `REQUEST_USE` for the object |
| Using a skill or attacking | `START_SKILL`, followed by `SYNC_SKILL` for multi-stage skills |
| Opening a window | Usually nothing; the window shows local data |
| Typing in chat | Chat packet or `PARSE_CHAT_MESSAGE` for slash commands |
| Choosing in a dialog | `MESSAGE_BOX_RESPOND`, `CHOICE_BOX_RESPOND`, `RESPOND_TO_MISSION` |
