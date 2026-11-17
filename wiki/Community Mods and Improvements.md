# Community Mods and Improvements

[Game Guide](./README.md) | [Server documentation](../server/README.md) | [Asset formats and tools](../server/content-authoring/asset-formats-and-tools.md)

This is a **selected, non-exhaustive** directory of public projects related
to LEGO Universe and DarkflameServer, reviewed on 2026-11-17. It distinguishes
actual client modifications from companion applications, operator tools, and
modding frameworks. Project descriptions below summarize their own
documentation; the projects were **not installed or independently tested**
for this guide. A listing is not an endorsement or a compatibility guarantee.

## Client modifications and companion applications

| Project | Type and purpose | Requirements and limitations |
|---|---|---|
| [LU Utility Mods](https://github.com/EmosewaMC/lu-utility-mods) | Client modification that writes the player's character save data to a local XML file. | The README describes standalone and mod-loader arrangements, with only one standalone mod at a time. Client-version and loader compatibility are not established here. Character saves may contain private information. |
| [Darkflame Rich Presence Client](https://github.com/DarkflameUniverse/DarkflameRPC) | Separate companion application that displays the current world and elapsed play time through Discord Rich Presence. | The project says it must be started separately and was tested on Windows 10 only. Discord status can disclose gameplay activity. |

These are not interchangeable: a DLL modification runs inside the game
client, while a companion application is a separate process. Check the rules
of the server on which you intend to play before using modifications.

## Server administration and deployment

| Project | Type and purpose | Requirements and limitations |
|---|---|---|
| [Nexus Dashboard](https://github.com/DarkflameUniverse/NexusDashboard) | Web application for server operations, including account and character management, moderation, reports, and property viewing. | Requires a working server and database access; some model-viewing features use client resources. The project lists invitations and invitation-only registration as **not yet implemented**. Restrict administrative access and secure any network exposure. |
| [HailStorm's Darkflame server scripts](https://github.com/HailStorm32/hailstorms-darkflame-server-scripts) | Operator scripts for activities such as database backup, character rescue, moderation, and player counts. | Environment-specific; some scripts modify accounts or character data. The optional ASSEMBLY bot features can send data to external services. Review settings, permissions, privacy, and recovery procedures before use. |
| [DarkflameServer Docker](https://github.com/tom300z/darkflameserver-docker) | Community Docker packaging for a DarkflameServer deployment. | Packaging and setup aid, not a gameplay mod. The project requires separately supplied client files and a database; check the supported versions and deployment configuration. |

These tools operate alongside a server rather than adding a drop-in gameplay
extension. Changes to live databases can be destructive; verify backups and
test against a separate instance first.

## Information and content-creation tools

| Project | Type and purpose | Requirements and limitations |
|---|---|---|
| [Crab Force](https://github.com/MasterTemple/Crab-Force) | Discord bot for looking up game data such as items, missions, vendors, and skills. | Its setup requires a client-derived SQLite database and localization file. It is an information bot, not an in-game mod; results depend on the supplied data and its calculations. |
| [Nejlika Libraries](https://github.com/Wincent01/nejlika-libraries) | Libraries and templates intended to support LEGO Universe modding, including world and model formats. | Developer framework, not a collection of ready-to-install mods. The project describes its command-line interface as work in progress and its overall documentation as incomplete. |
| [LU-Rebuilt navmesh-tools](https://github.com/LU-Rebuilt/navmesh-tools) | Tool for inspecting zone geometry and generating navigation-mesh output. | The project describes it as **early work in progress** and says interactive editing is not yet available. Test generated files with the intended server version. |
| [LU-Rebuilt CDClient Manager](https://github.com/LU-Rebuilt/cdclient-manager) | Database manager with table, loot, and skill editors. | The project describes itself as **work in progress**. Data edits must be checked against the matching client and server; a database edit alone does not implement missing server behavior. |

More file viewers and converters are listed in
[Asset Formats and Tools](../server/content-authoring/asset-formats-and-tools.md).
These tools help create changes; their presence does not imply that finished
gameplay mods are included.

## Experimental alternative client

[LU-Rebuilt](https://github.com/LU-Rebuilt/lu-rebuilt) describes a
cross-platform client remake and identifies DarkflameServer as a planned
backend. This is a separate client project, **not** a mod for the original
client. The project does not establish complete gameplay or compatibility
with a particular DarkflameServer deployment; check its current status before
relying on it.

## Before using third-party projects

1. Check the project's license, maintenance status, operating-system and
   version requirements, and whether it is intended for players or operators.
   Software licenses do not grant rights to original game assets or databases.
2. Obtain and use client resources only where authorized. Do not redistribute
   original client files or modified full databases without appropriate rights.
3. Back up the client and database, then test in an isolated environment.
   Never assume a client-only change also changes server behavior.
4. Review source, dependencies, release provenance, requested permissions, and
   any network or external-service integration. Protect account credentials,
   tokens, database contents, character saves, and player communications.
5. Pin the tested versions and check logs, gameplay, and persistence after
   updates. Follow the [testing guide](../server/content-authoring/test-and-troubleshoot.md).

For further discovery, [Awesome LEGO Universe](https://github.com/EliteMasterEric/awesome-lego-universe)
collects community guides and development resources; it is not a verified list
of compatible mods.
