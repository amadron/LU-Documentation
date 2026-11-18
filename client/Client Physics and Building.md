# Client physics and building

[Client overview](./README.md) | [Input and camera](./Client%20Input%20and%20Camera.md) | [Server contract](./Server%20Contract.md)

## Physics engine

The client uses **Havok Physics** (version string "Havok-7.1" in the executable). Collision
shapes are stored as Havok packfiles (`.hkx`): about 4,100 in `res/physics` and about 50 in
`res/BrickModels`. Which shape an object uses is set in the content data (`PhysicsComponent`
table in `cdclient.fdb`).

Physics component types the client knows:

| Component | Role on the client |
| --- | --- |
| Controllable physics | The player character (and other players' characters): walking, jumping, falling, gravity, speed multipliers, jetpack |
| Simple physics | Objects that move in simple ways or are static colliders |
| Rigid body phantom | Static or kinematic collision volumes |
| Phantom physics | Trigger volumes without collision: the client reports entering and leaving them (`onCollisionPhantom`, `onOffCollisionPhantom` in scripts) and applies effects such as pushes or gravity changes |
| Havok vehicle physics | Racing cars (`HavokVehicleComponent`) |

### Who simulates what

- **The local player.** The client simulates its own character with Havok against the zone's
  collision and moves it immediately in response to input. It is *client-predicted* and, in
  practice, client-authoritative for position.
- **Other players.** Their positions arrive from the server and are interpolated.
- **NPCs and moving objects.** Their movement is decided by the server (AI, paths, moving
  platforms) and sent as component updates; the client interpolates and animates them.
- **Smashed bricks and visual debris** are purely local (`R_MAXSMASHBRICKS`,
  `SMASHABLES_MAX_BRICK_COUNT`, `QUICKBUILD_MAX_BOUNCING_BRICKS`).

DarkflameServer does not run Havok. It has its own simplified collision code (`dPhysics`) for
trigger volumes and proximity checks and uses navigation meshes for NPC movement.

### Movement and the server

The client sends `POSITION_UPDATE` packets while the player moves. The fields, as parsed by
[ClientPackets.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dNet/ClientPackets.cpp):

| Field | Type |
| --- | --- |
| Position | 3 × float |
| Rotation | quaternion, 4 × float (x, y, z, w) |
| On ground, on rail | 2 × bool |
| Linear velocity | flag + 3 × float |
| Angular velocity | flag + 3 × float |
| Local space info (standing on a moving platform) | flag + platform object ID, relative position, optional velocity |
| Remote input info (vehicles) | flag + steering X/Y, power-slide, modified flag, ... |

The server applies the update to the player's controllable-physics state and forwards it to
other clients in its serialization. When the server needs to move a player itself, it sends
`TELEPORT`, `KNOCKBACK`, `ORIENT_TO_POSITION`, or forced-movement and gravity changes
(`SET_GRAVITY_SCALE`, `SET_JET_PACK_MODE`); the client then simulates from the new state.

## Brick building

Building is where LEGO Universe differs most from other online games. The client contains a
LEGO brick system shared with LEGO Digital Designer:

| Data | Content |
| --- | --- |
| `res/brickdb.zip` | Brick database: brick definitions and connection points |
| `res/brickprimitives` | Brick geometry in several detail levels (`.g`, `.g1`, `.g2`, ... about 5,900 files) |
| `res/brickdefaults.paxml` | Default brick settings |
| `res/BrickModels` | About 2,400 pre-made models as `.lxfml` (brick lists), plus a few `.nif`/`.hkx` |
| `cop.dll` | LEGO component with classes `COPBrick`, `COPPart`, `COPScene`, `COPMesh` and Havok collision filters; used for brick connection and collision checks |

The executable has loaders for **LXFML versions 4 and 5** (`ModelLoaderLXFML4`,
`ModelLoaderLXFML5`) and a saver for version 5 (`ModelSaverLXFML5`). LXFML is an XML format
listing bricks, their positions, colors, and connections.

### Kinds of building

| Kind | Client side | Server side |
| --- | --- | --- |
| **Quick build** (rebuild) | Shows the build animation, the bricks flying in, and the progress UI (`quickbuildreqs.gfx`) | Owns the state (open, building, complete, resetting), checks imagination, and grants rewards; serialized in the quick-build component |
| **Modular build** (rockets, cars) | Part selection UI (`modularbuildpartslist.gfx`), assembly preview (`SCHEME_MODULAR_BUILD`) | Validates the chosen modules and stores the assembly as an item |
| **Brick-by-brick build** (free building) | Full brick editor: placing, rotating, painting, hinges, copying, undo/redo; produces LXFML | Saves the model (`BBB_SAVE_REQUEST`, response `MSG_CLIENT_BLUEPRINT_SAVE_RESPONSE`) and stores it as user-generated content |
| **Property editing** | Moving models on a property (`propertyedit*.gfx`, `PROPERTY_CARRY_*` keys) | Persists placed models (`PLACE_PROPERTY_MODEL`, `PROPERTY_CONTENTS_FROM_CLIENT`) |
| **Behaviors** | Behavior editor (`behavioreditor.gfx`) for programmable models | Runs and stores model behaviors |
| **Choice build** | `choicebuild.gfx` | `CHOICE_BUILD_SELECTION_CONFIRMED` |

A brick-built model is shown to other players as LXFML: the server sends the stored model data,
and each client builds the geometry itself from its own brick database. In the live game, LEGO's
moderators also approved models (`MSG_CHAT_BLUEPRINT_MODERATED`,
`MSG_WORLD_BPSERVER_BLUEPRINT_MODEL_READY`); a private server can skip moderation, but it must
answer the save and load messages so that the client leaves build mode correctly.
