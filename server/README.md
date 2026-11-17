# DarkflameServer technical documentation

This folder documents the **server implementation** of Darkflame Universe. It is a code-oriented reference, not a complete catalogue of all LEGO Universe content or a substitute for the source.

- Official repository at the documented revision: [DarkflameServer](https://github.com/DarkflameUniverse/DarkflameServer/tree/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/)
- Revision used for this documentation: `8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4`
- Code-oriented directory guide: [src/README.md](./src/README.md)

The documents describe that source snapshot. Configuration, client data, and runtime state can change behavior; check the linked implementation when investigating a particular branch or feature.

## Documentation map

| Topic | Document | Main coverage |
|---|---|---|
| Content authoring | [Content Authoring](./content-authoring/README.md) | Practical workflows for zones, scene objects, spawners, native scripts, data dependencies, and validation. |
| Community projects | [Mods and Improvements](../wiki/Community%20Mods%20and%20Improvements.md) | Selected client modifications, companion applications, operator tools, and modding projects. |
| Processes and architecture | [Architecture and Repository Structure](./DarkflameServer%20Architecture%20and%20Repository%20Structure.md) | Service boundaries, startup, login, world instances, transfers, runtime ownership, build organization. |
| Client protocol | [Client-Server Protocol and Gameplay](./DarkflameServer%20Client-Server%20Protocol%20and%20Gameplay.md) | RakNet transport, packet families, login flow, game messages, example request paths. |
| World implementation | [World Simulation and Entity Model](./DarkflameServer%20World%20Simulation%20and%20Entity%20Model.md) | Zone loading, entities, components, native scripts, game-message dispatch, simulation and replication. |
| Persistence | [Data and Persistence Reference](./DarkflameServer%20Data%20and%20Persistence%20Reference.md) | Game database, CDClient data, migrations, character saves, property and other persistent state. |
| Commands | [Command Reference](./DarkflameServer%20Command%20Reference.md) | Registered slash commands, aliases, and required GM levels. |
| GM operations | [Gamemaster Guide](./DarkflameServer%20Gamemaster%20Guide.md) | Source-checked operational workflows and cautions for authorized staff. |

## Suggested reading paths

- **New to the server:** architecture → protocol → world simulation → persistence.
- **Tracing a client feature:** protocol packet family → relevant `WorldServer` handler → game-message or packet handler → entity/component/script → persistence or replication.
- **Tracing a database issue:** persistence reference → the relevant table interface/backend → migration or character/component save path.
- **Finding a source directory:** [src/README.md](./src/README.md) lists the principal subsystems and entry points.

## Evidence and limits

The implementation links are intended to make claims verifiable in code. The guides explain the main runtime paths and architectural boundaries; they do not provide a line-by-line description of every source file. In particular, observed behavior may depend on the exact client build, CDClient database, resource archive, server configuration, and loaded zone data.
