# LEGO Universe client documentation

[Home](../index.md) | [Server documentation](../server/README.md) | [Client libraries](./Client%20Libraries.md)

This section documents the **game client**: the final 2011 build of `legouniverse.exe` and the
files it ships with. It describes what the client does, how it is organized into subsystems, and
which behavior it expects from a game server. The last part, the
[server contract](./Server%20Contract.md), lists what a server must provide so that an
unmodified client can log in, load a world, and play.

The client is proprietary and its source code is not public. Everything here was determined from
the shipped files (configuration, resources, scripts, version and text strings inside the
executable) and from [DarkflameServer](../server/README.md), an open source server that is
compatible with the unmodified client. Where a statement is an inference rather than something
read directly from a file, the page says so.

## Documentation map

| Area | Page | Main coverage |
| --- | --- | --- |
| Overview and startup | [Architecture and Startup](./Client%20Architecture%20and%20Startup.md) | Files of an installation, subsystems, configuration files, startup sequence, game states |
| Rendering | [Rendering](./Client%20Rendering.md) | Gamebryo and Direct3D 9, shaders, LOD, shadows, particles, graphics settings |
| User interface | [User Interface](./Client%20User%20Interface.md) | Scaleform GFx movies, HUD layout, front end, cursors, embedded browser |
| Audio and video | [Audio and Video](./Client%20Audio%20and%20Video.md) | FMOD event banks, music cues, voice-over languages, Bink movies |
| Input and camera | [Input and Camera](./Client%20Input%20and%20Camera.md) | Key bindings, gamepad, control schemes, camera modes |
| Physics and building | [Physics and Building](./Client%20Physics%20and%20Building.md) | Havok collision, client-side movement, brick building, LXFML models |
| Scripting | [Client Scripting](./Client%20Scripting.md) | Client-side Lua scripts, callbacks, engine API, network variables |
| Assets and content data | [Assets and Content Data](./Client%20Assets%20and%20Content%20Data.md) | `res` folder layout, file formats, `cdclient.fdb`, maps, localization, chat lists |
| Networking | [Networking](./Client%20Networking.md) | RakNet connection, packet families, login, world transfer, replication |
| Server contract | [Server Contract](./Server%20Contract.md) | Requirements a server must meet for the client to work, as a checklist |
| Troubleshooting | [Troubleshooting](./Client%20Troubleshooting.md) | Symptoms, client log lines, likely causes, related contract requirements |
| Packet formats | [Packet Formats](./Client%20Packet%20Formats.md) | Field layouts of handshake, login, character, transfer, zone-load, and game-message packets |
| World files | [World File Formats](./Client%20World%20File%20Formats.md) | `.luz`, `.lvl`, `.raw`, `.lutriggers`; map checksum; which scene objects the server creates |
| Reference | [Reference Tables](./Client%20Reference%20Tables.md) | Packet and game-message IDs, component type IDs, LDF types, character XML, object ID flags |
| Middleware | [Client Libraries](./Client%20Libraries.md) | Third-party libraries, versions, open alternatives |

## Suggested reading paths

- **Understanding the client:** architecture → assets → rendering, UI, audio → scripting.
- **Writing or debugging a server:** networking → server contract → reference tables →
  troubleshooting → the server's
  [client-server protocol](../server/DarkflameServer%20Client-Server%20Protocol%20and%20Gameplay.md).
- **Modding the client:** assets → the area you want to change → scripting.

## The client at a glance

| Subsystem | Implemented with | Data in `res` |
| --- | --- | --- |
| 3D engine, scene graph, animation | Gamebryo 2.3 on Direct3D 9 | `mesh` (`.nif`), `animations` (`.kf`, `.kfm`), `shaders` (`.fxo`) |
| Physics and collision | Havok 7.1 | `physics` (`.hkx`) |
| User interface | Scaleform GFx (Flash) | `ui` (`.gfx`, `.xml`), `fonts` |
| Sound and music | FMOD Ex 4.32 with the event system | `audio` (`.fev`, `.fsb`) |
| Video | Bink 1.9 | `Movies` (`.bik`) |
| Network | RakNet (3.25-compatible) | — |
| Game logic on the client | Lua scripts | `scripts` (`.lua`) |
| Building | LEGO brick database, `cop.dll` | `brickdb.zip`, `brickprimitives`, `BrickModels` (`.lxfml`) |
| Content data | FDB database | `cdclient.fdb` |
| Worlds | LEGO Universe zone and level files | `maps` (`.luz`, `.lvl`, `.raw`, ...) |
| Text | XML locale file | `locale/locale.xml` |

## Division of responsibilities

LEGO Universe is server-authoritative for game state and client-authoritative for presentation:

- The **server** decides what exists in the world (objects, their components and state), owns
  the character's persistent data (inventory, missions, currency, levels), runs combat and loot,
  and validates requests.
- The **client** draws the world, plays sound and animation, runs the user interface, reads
  input, simulates its own player's movement locally and reports the result, and runs client
  scripts for local effects. It needs the same content data as the server (`cdclient.fdb`, the
  zone files) because the server only sends IDs and changes, not models or definitions.

Because the client contains the complete content, a server never sends meshes, textures,
scripts, or UI. It sends object IDs, template numbers (LOTs), component state, and game
messages that refer to content the client already has.

## Glossary

| Term | Meaning |
| --- | --- |
| **LOT** | Template number of an object; row ID in the `Objects` table. The player character is LOT 1. |
| **Object ID** (`LWOOBJID`) | 64-bit ID of one object instance; some high bits mark characters, spawned, and client-local objects. |
| **Component** | A building block of an object (render, physics, inventory, ...). Which components a LOT has is listed in `ComponentsRegistry`. |
| **LDF** | Typed key-value format (`key=type:value`) used in configuration, scenes, and packets. |
| **Zone / map, instance, clone** | A zone ID has three parts: the map (`ZoneTable`), the instance (one running copy), and the clone (a player's property). The log shows them as `1151:2:0`. |
| **Scene / level** | A `.lvl` file with the objects of one part of a zone. |
| **Zone control object** | Object with the fixed ID `0x3FFFFFFFFFFE` that holds the zone's scripts and state. |
| **Ghosting / scope** | The server's decision which objects a client receives, mainly by distance. |
| **Construction / serialization** | First full transfer of an object to a client / later changes to it. |
| **Game message (GM)** | An operation on one object, carried in `GAME_MSG` packets; also callable from Lua. |
| **Network variable** | Script variable set by the server and replicated to the client script. |
| **Control scheme** | How input becomes movement (walking, driving, taming, ...). |
| **Quick build / rebuild** | Building an object from a pile of bricks with imagination. |
| **BBB** | "Brick by brick": free building with single bricks. |
| **LXFML** | XML format of brick models. |
| **NDAudio** | NetDevil's sound layer on top of FMOD. |
| **GM level** | Staff permission level of an account (not related to game messages). |
| **U-score** | Universe score: the experience points that raise the player's level. |

## Evidence and limits

- File lists and counts come from an unmodified installation of the final client.
- Packet names (`MSG_...`) and some engine messages appear as text inside `legouniverse.exe`.
  Their presence shows that the client knows the name, not that it sends or accepts the message.
- Script statistics count occurrences in the shipped `.lua` files.
- Server-side behavior refers to DarkflameServer revision
  `8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4`, which the rest of this site also documents.
