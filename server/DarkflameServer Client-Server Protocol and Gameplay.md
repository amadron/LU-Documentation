# DarkflameServer Client-Server Protocol and Gameplay

## Scope and source snapshot

This guide documents the client-facing protocol and the gameplay path through the server code. It is based on the local [DarkflameServer source checkout](https://github.com/DarkflameUniverse/DarkflameServer/tree/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/) at revision `8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4`.

It is a code-oriented overview, not a complete byte-for-byte protocol specification. The authoritative message IDs and field serialization are in the source files linked below. The protocol is client-version-specific; the client network version is configurable in `sharedconfig.ini`.

For the process-level architecture and repository map, see [DarkflameServer Architecture and Repository Structure](./DarkflameServer%20Architecture%20and%20Repository%20Structure.md).

## 1. Protocol layers

### RakNet transport

Client and server communication runs over RakNet. RakNet handles connection establishment, transport-level packet delivery, and its own control messages. DLU application packets are carried as RakNet user packets; they are not raw application payloads sent directly over UDP.

The shared transport wrapper is [dNet/dServer.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dNet/dServer.cpp). Its common `Send` method uses reliable-ordered delivery, although individual code paths may use different reliability/channel arguments. The world service also configures RakNet's replica manager and network-ID manager for entity replication.

### DLU application header

DLU custom packets use a common 8-byte application header, written by [BitStreamUtils::WriteHeader](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dNet/BitStreamUtils.h) and skipped/read by the packet handlers:

| Field | Serialized size | Purpose |
|---|---:|---|
| `ID_USER_PACKET_ENUM` | 1 byte | Marks a RakNet user packet. |
| `ServiceType` | 2 bytes | Selects the application service/message namespace. |
| Internal packet ID | 4 bytes | Selects the operation within that service. |
| Padding | 1 byte | Reserved/padding byte. |

`ServiceType` is defined in [ServiceType.h](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dCommon/dEnums/ServiceType.h). Its values include `COMMON`, `AUTH`, `CHAT`, `WORLD`, `CLIENT`, and `MASTER`. Message IDs are declared separately under [dCommon/dEnums/MessageType/](https://github.com/DarkflameUniverse/DarkflameServer/tree/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dCommon/dEnums/MessageType/).

After the header, payloads are serialized in message-specific order using `RakNet::BitStream`. There is no single universal payload schema. Some strings use fixed-size `LUString`/`LUWString` fields; other payloads carry explicit lengths, structured values, or nested binary data. Do not infer a field layout from an enum alone: inspect the corresponding serializer and parser.

### Which side uses which message family?

| Direction / purpose | Service and message family | Examples |
|---|---|---|
| Client to authentication | `AUTH` / `MessageType::Auth` | `LOGIN_REQUEST`, `LOGOUT_REQUEST`, account creation. |
| Client to a world | `WORLD` / `MessageType::World` | `VALIDATION`, `GAME_MSG`, character operations, movement, chat. |
| Server to client | `CLIENT` / `MessageType::Client` | `LOGIN_RESPONSE`, `LOAD_STATIC_ZONE`, `CREATE_CHARACTER`, `TRANSFER_TO_WORLD`, `GAME_MSG`. |
| Internal world-to-master | `MASTER` / `MessageType::Master` | Session-key requests, instance/zone-transfer requests, readiness, shutdown. |
| Internal world-to-chat and chat-to-world | `CHAT` / `MessageType::Chat` | Player session notifications, chat, teams, friends, moderation. |
| Shared connection/control | `COMMON` / `MessageType::Server` | Version handshake and disconnect notifications. |

The service value is part of the application protocol and is distinct from RakNet's connection-level packet identifiers.

## 2. Connection and login lifecycle

The following sequence summarizes the implemented flow; optional checks and some client-driven transitions are omitted for clarity.

```text
Client             AuthServer          MasterServer          WorldServer (zone 0)
  |                     |                    |                       |
  |-- COMMON handshake ->|                    |                       |
  |<- version confirm ---|                    |                       |
  |-- AUTH LOGIN_REQUEST>|                    |                       |
  |                     |-- request zone 0 / session coordination -->|
  |                     |<------------- instance/transfer details ----|
  |<- CLIENT LOGIN_RESPONSE (session token + world address/port) -----|
  |------------------------------------------------------------------->|
  |-- COMMON handshake ------------------------------------------------>|
  |-- WORLD VALIDATION (username, token, optional client-data checksum)|
  |                     |                    |<-- REQUEST_SESSION_KEY--|
  |                     |                    |--- SESSION_KEY_RESPONSE>|
  |<- CLIENT LOAD_STATIC_ZONE / character-list response ---------------|
```

### 2.1 Common handshake

The client sends a `COMMON` packet with `MessageType::Server::VERSION_CONFIRM`. The receiver parses client version/service/process/port information and responds with its configured network version and server service information. The implementation is in [AuthPackets::HandleHandshake](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dNet/AuthPackets.cpp); the same handler is used by world and auth services.

The handshake is separate from application login. Passing it does not by itself authenticate an account.

### 2.2 Account login

The client sends `AUTH / LOGIN_REQUEST` to `AuthServer`. The current parser reads, in order, a username, password field, locale, client OS, memory and video-card strings, CPU information, and OS version information. `AuthServer` then checks the account and relevant account state, including password verification, ban/lock state, and play-key policy as configured.

On success, authentication obtains/resolves the zone-0 destination through the master and sends `CLIENT / LOGIN_RESPONSE`. The response contains the result, event/version settings, a generated session value/hash, and the world-server address and port used for the next connection. The chat address/port fields are marked unused in the implementation. The successful session value is also registered with the master for validation by a world process.

See [AuthServer.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dAuthServer/AuthServer.cpp) and [AuthPackets.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dNet/AuthPackets.cpp) for the account checks and the exact serializer.

### 2.3 World validation and character selection

The client connects to the returned world endpoint and sends `WORLD / VALIDATION` with its username, session token/hash, and client-data checksum. The world service asks the master for the corresponding session key, checks that the returned key matches the pending session, and then creates its in-memory `User` state.

For zone `0`, the world service requests the account's character list. It sends `CLIENT / LOAD_STATIC_ZONE` with the zone metadata/checksum as part of the client transition into the character-selection state. The client can then request the character list and submit character-create, rename, or delete requests.

The relevant dispatch is in [WorldServer.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dWorldServer/WorldServer.cpp); account/character operations are implemented by [UserManager.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/UserManager.cpp).

### 2.4 Entering a playable zone

1. The client selects a character using `WORLD / LOGIN_REQUEST` with the character object ID.
2. The world service checks that the requested character belongs to the authenticated user and starts character login.
3. The client loads the target zone and reports `WORLD / LEVEL_LOAD_COMPLETE`.
4. The world service creates the player entity, attaches the character's components, applies any needed character-data migration/fixes, and sends character/world state.
5. The entity manager constructs the player and relevant zone entities for that client. Zone content may include other players, NPCs, spawners, objects, and property content.
6. The client reports `WORLD / GAME_MSG` with inner message `MessageType::Game::PLAYER_LOADED`. The server performs post-load initialization, marks the player ready for updates, restores/sends relevant state, invokes zone/script callbacks, and signals completion.

The `LEVEL_LOAD_COMPLETE` path and entity construction are in [WorldServer.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dWorldServer/WorldServer.cpp). `PLAYER_LOADED` is handled in [GameMessageHandler.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dGameMessages/GameMessageHandler.cpp).

## 3. Client-to-server operations

### 3.1 World-level message IDs

`MessageType::World` is the outer world-service namespace. In this checkout, the world packet handler has explicit cases for the following operations:

| Message | Role in the current handler |
|---|---|
| `VALIDATION` | Associates a client connection with an authenticated session. |
| `CHARACTER_LIST_REQUEST` | Requests the user's character list. |
| `CHARACTER_CREATE_REQUEST` | Creates a character. |
| `LOGIN_REQUEST` | Selects/logs in a character. |
| `GAME_MSG` | Carries an entity-targeted gameplay message; detailed below. |
| `CHARACTER_DELETE_REQUEST` | Deletes a character. |
| `CHARACTER_RENAME_REQUEST` | Renames a character. |
| `LEVEL_LOAD_COMPLETE` | Signals that client-side zone loading has reached the server handoff point. |
| `POSITION_UPDATE` | Sends player/possessed-object movement state. |
| `MAIL` | Routes a mail operation to the mail handler. |
| `ROUTE_PACKET` | Forwards a chat/social packet to the chat service. |
| `STRING_CHECK` | Requests chat moderation/allow-list validation. |
| `GENERAL_CHAT_MESSAGE` | Sends a general chat message, subject to server checks. |
| `HANDLE_FUNNESS` | Reports the client's timing/funness state. |
| `UI_HELP_TOP_5` | Handles the client help/top-five request. |

The enum in [World.h](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dCommon/dEnums/MessageType/World.h) declares additional IDs. An enum declaration only assigns a protocol identifier; it does not prove that the current world handler implements that operation. For support status, compare the enum to the `HandlePacket` switch in `WorldServer.cpp`.

### 3.2 Entity-targeted gameplay messages (`GAME_MSG`)

Most interactions during play use the `WORLD / GAME_MSG` envelope. Its payload begins with:

1. the 8-byte DLU application header;
2. the target/source `LWOOBJID`;
3. a `MessageType::Game` identifier; and
4. message-specific serialized data.

The game-message identifier is an inner operation code, not a separate RakNet connection packet. Its enum is [MessageType/Game.h](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dCommon/dEnums/MessageType/Game.h).

At this revision, the world handler checks that the object ID is associated with the sending client before dispatching the message. [GameMessageHandler.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dGameMessages/GameMessageHandler.cpp) then requires an authenticated user and a live entity. A small typed-message factory handles several operations (including `REQUEST_USE`, `REQUEST_SERVER_OBJECT_INFO`, `SHOOTING_GALLERY_FIRE`, and `PICKUP_ITEM`); most others are handled by a switch that parses the payload and calls gameplay logic.

Common gameplay message families include:

| Gameplay area | Representative `MessageType::Game` operations |
|---|---|
| Readiness and zone lifecycle | `PLAYER_LOADED`, `READY_FOR_UPDATES`, `NOTIFY_SERVER_LEVEL_PROCESSING_COMPLETE` |
| Interaction, events, UI | `REQUEST_USE`, `REQUEST_SERVER_OBJECT_INFO`, `FIRE_EVENT_SERVER_SIDE`, `MESSAGE_BOX_RESPOND`, `CHOICE_BOX_RESPOND` |
| Movement and world objects | `REQUEST_PLATFORM_RESYNC`, `CLIENT_RAIL_MOVEMENT_READY`, `CANCEL_RAIL_MOVEMENT`, `PLAYER_RAIL_ARRIVED_NOTIFICATION` |
| Skills and combat | `START_SKILL`, `SYNC_SKILL`, `REQUEST_SERVER_PROJECTILE_IMPACT`, `REQUEST_DIE`, `REQUEST_RESURRECT` |
| Inventory and equipment | `MOVE_ITEM_IN_INVENTORY`, `MOVE_ITEM_BETWEEN_INVENTORY_TYPES`, `EQUIP_INVENTORY`, `UN_EQUIP_INVENTORY`, `PICKUP_ITEM` |
| Vendors, trade, and currencies | `BUY_FROM_VENDOR`, `SELL_TO_VENDOR`, `BUYBACK_FROM_VENDOR`, `CLIENT_TRADE_REQUEST`, `CLIENT_TRADE_ACCEPT`, `PICKUP_CURRENCY` |
| Missions and activities | `RESPOND_TO_MISSION`, `REQUEST_LINKED_MISSION`, `ACTIVITY_STATE_CHANGE_REQUEST`, `REQUEST_ACTIVITY_EXIT` |
| Building and properties | `PROPERTY_EDITOR_BEGIN`, `PROPERTY_CONTENTS_FROM_CLIENT`, `PLACE_PROPERTY_MODEL`, `BBB_SAVE_REQUEST`, `SET_PROPERTY_ACCESS` |
| Pets and racing | `PET_TAMING_TRY_BUILD`, `REQUEST_SET_PET_NAME`, `COMMAND_PET`, `RACING_CLIENT_READY`, vehicle boost/possession messages |
| Chat text and slash commands | `PARSE_CHAT_MESSAGE` |

This is a representative list of gameplay operations implemented in the handler, not a guarantee that every identifier in `MessageType::Game` is accepted or fully implemented. Unknown/unhandled IDs are logged. The complete current list of explicit dispatch cases is in `GameMessageHandler.cpp`.

### 3.3 Chat, social, and slash commands

Chat has two paths:

- `WORLD / GENERAL_CHAT_MESSAGE` handles general chat text in the world process. The world checks the logged-in user, mute state, and chat filter before sending approved text through chat packet code.
- `WORLD / ROUTE_PACKET` carries other chat/social requests to `ChatServer`. The chat handler owns friend/ignore lists, team operations, chat routing, and related service state. Internal traffic uses the `CHAT` service namespace.

An in-game slash command such as `/help`, `/tp`, or `/spawn` is **not** a special world opcode. A command string is carried in `WORLD / GAME_MSG` with inner message `MessageType::Game::PARSE_CHAT_MESSAGE`; if it begins with `/`, `HandleParseChatMessage` calls `SlashCommandHandler`. The handler resolves a registered name/alias and checks its required GM level before running it. The user-facing command reference is [docs/Commands.md](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/docs/Commands.md); implementation is in [SlashCommandHandler.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/SlashCommandHandler.cpp).

## 4. Server-to-client operations

The `CLIENT` message namespace is used for client-facing application messages. Common outer responses include:

| `MessageType::Client` | Purpose |
|---|---|
| `LOGIN_RESPONSE` | Login result, session data, and initial world endpoint. |
| `LOAD_STATIC_ZONE` | Static zone/load metadata. |
| `CHARACTER_LIST_RESPONSE` | Character-selection data. |
| `CREATE_CHARACTER`, `CHARACTER_CREATE_RESPONSE` | Character entity data and create result. |
| `CHARACTER_RENAME_RESPONSE`, `DELETE_CHARACTER_RESPONSE` | Character operation results. |
| `TRANSFER_TO_WORLD` | Target server address/port for a world change. |
| `GAME_MSG` | Server-to-client entity/game event or state update. |
| Chat/social response IDs | Friend, ignore, team, chat, and moderation results. |

The exact field order for these messages is implemented in [AuthPackets.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dNet/AuthPackets.cpp) and [WorldPackets.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dNet/WorldPackets.cpp), with additional response code in [ChatPackets.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dNet/ChatPackets.cpp) and gameplay send helpers in [GameMessages.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dGameMessages/GameMessages.cpp).

Not every server update is a `CLIENT` user packet. Entity construction and serialization also use RakNet's replica-manager packet IDs. Entity components provide construction/serialization data; `EntityManager` sends updates to clients that should observe those entities.

## 5. Gameplay implementation pipeline

An interaction typically passes through the following layers:

```text
RakNet receive
   -> service/opcode dispatch (WorldServer)
      -> GAME_MSG envelope parse (target entity + game-message ID)
         -> sender/user/entity checks
            -> GameMessageHandler payload decode
               -> GameMessages helper / component / manager / script callback
                  -> mutate server state and/or persistent state
                     -> send GAME_MSG response and/or replica serialization
```

### 5.1 Entity and component state

An `Entity` is a game object identified by an object ID and a LOT/template. It owns a set of components. The entity manager creates and indexes entities, updates them, schedules destruction, handles replication, and scopes/ghosts entities according to client visibility. Components hold domain state and implement behavior for systems such as character identity, physics, inventory, missions, skills, destruction, properties, pets, vendors, and activities.

Object/template data and component registrations are partly read from the static client-data database. At construction time the server looks up component registrations and attaches the native component implementations available in the codebase. This is why a change to an object's behavior may involve both a component and game-data/template configuration.

### 5.2 Gameplay logic and scripts

`GameMessageHandler` converts a wire message into a typed server operation. The operation may be implemented directly in `GameMessages.cpp`, in a manager, or in a component. Some game objects also use native C++ script classes registered against game content script-path identifiers. Zone scripts, AI scripts, and object scripts respond to events such as player load, interaction, timers, and server-side trigger notifications.

The server generally stores gameplay state in server-side objects/components and sends the client the changes or results it needs to display. The client remains responsible for presentation and portions of local input/animation behavior; the network message being a request does not, by itself, mean the client-provided result is trusted.

### 5.3 Per-frame update and replication

For a normal zone, the `WorldServer` loop:

1. computes elapsed time and updates entities and their timers/scripts; the entity manager then serializes queued changes and processes kills/deletions;
2. advances the physics world;
3. updates entity ghosting/visibility and zone spawners;
4. processes master and chat service traffic;
5. reads and dispatches a bounded batch of world packets;
6. updates RakNet replica state; and
7. periodically saves active character state.

`EntityManager::UpdateEntities` updates entities, serializes queued state, then processes kills and deletions. The world server performs physics, ghosting, and spawner updates around that entity pass. Some scheduling and frame rates vary by zone/configuration.

### 5.4 Persistence

Character and gameplay state is loaded into server-side entities/components when the player enters a zone. Persistent state is written through the game-database interfaces, including character XML and data represented in associated tables. The server saves active characters periodically and also saves/cleans up player state on disconnect or zone changes. Static game/client metadata is read separately from the CDClient SQLite database.

## 6. Example message flows

### Movement

1. The client sends `WORLD / POSITION_UPDATE` with its position, rotation, velocity, and movement flags.
2. `ClientPackets::HandleClientPositionUpdate` parses the payload.
3. The world resolves the authenticated user's current character and calls `Entity::ProcessPositionUpdate`.
4. The entity updates its controllable-physics state (or the possessed vehicle/mount), movement statistics, and ghost reference point.
5. The entity manager schedules the resulting state for serialization to appropriate observers.

Movement handling is in [WorldServer.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dWorldServer/WorldServer.cpp), [ClientPackets.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dNet/ClientPackets.cpp), and [Entity::ProcessPositionUpdate](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/Entity.cpp).

### Skill use

1. The client sends `WORLD / GAME_MSG` targeting its player entity with inner message `START_SKILL` and the skill payload.
2. The handler checks that the sender owns the target entity and decodes the request.
3. The server resolves skill behavior data from CDClient tables and asks the entity's skill component to execute it.
4. On success, server-side state such as imagination cost and mission progress is updated, and a client-facing `GAME_MSG` echo is sent.

See the `START_SKILL` case in [GameMessageHandler.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dGameMessages/GameMessageHandler.cpp) and the related skill implementation in [SkillComponent.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dComponents/SkillComponent.cpp).

### Slash command

1. A slash-prefixed chat string arrives as `WORLD / GAME_MSG` with inner message `MessageType::Game::PARSE_CHAT_MESSAGE`.
2. The server parses the text and passes it to `SlashCommandHandler`.
3. The command name/alias is looked up and its GM-level requirement checked.
4. The registered command runs server-side and may send feedback as game/chat messages.

This shares the regular game-message channel; there is no dedicated `/command` packet type.

## 7. Source map for protocol work

| Concern | Start reading here |
|---|---|
| Service IDs and outer message families | [ServiceType.h](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dCommon/dEnums/ServiceType.h), [MessageType/](https://github.com/DarkflameUniverse/DarkflameServer/tree/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dCommon/dEnums/MessageType/) |
| Common application header and string helpers | [BitStreamUtils.h](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dNet/BitStreamUtils.h), [dCommonVars.h](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dCommon/dEnums/dCommonVars.h) |
| Handshake and account login | [AuthPackets.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dNet/AuthPackets.cpp), [AuthServer.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dAuthServer/AuthServer.cpp) |
| World opcode routing and login flow | [WorldServer.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dWorldServer/WorldServer.cpp) |
| Client position/chat payload decoding | [ClientPackets.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dNet/ClientPackets.cpp) |
| Game-message dispatch | [GameMessageHandler.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dGameMessages/GameMessageHandler.cpp), [Game.h](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dCommon/dEnums/MessageType/Game.h) |
| Game-message serializers and handlers | [GameMessages.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dGameMessages/GameMessages.cpp) |
| Entity construction, state, and serialization | [Entity.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/Entity.cpp), [EntityManager.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/EntityManager.cpp), [dComponents/](https://github.com/DarkflameUniverse/DarkflameServer/tree/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dComponents/) |
| Chat/social service routing | [ChatServer.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dChatServer/ChatServer.cpp), [ChatPacketHandler.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dChatServer/ChatPacketHandler.cpp) |

## 8. Important interpretation notes

- Message enums are protocol namespaces, not a promise that every declared ID is implemented or supported.
- World-level messages and inner `MessageType::Game` operations are separate layers. A `GAME_MSG` is an outer world/client packet that carries a second operation ID and entity target.
- The same conceptual action can involve several request, response, internal-service, and replication messages.
- This guide describes the inspected source revision. For exact compatibility, use the matching client network version and check the serializer/parser in the target revision.
- The implementation is a legacy game protocol with fixed-width and custom binary fields; do not assume JSON, HTTP, or a generic length-prefixed RPC format.
