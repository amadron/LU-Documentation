# Client troubleshooting

[Client overview](./README.md) | [Server contract](./Server%20Contract.md) | [Architecture and startup](./Client%20Architecture%20and%20Startup.md#logging-and-error-reporting)

Common problems when running the unmodified client against a server, what they usually mean,
and which [server contract](./Server%20Contract.md) requirement is involved. Start with the
newest client log in `%LOCALAPPDATA%\LEGO Software\LEGO Universe\Log Files` and the server's
logs; the log lines quoted below are from the client.

## Connection and login

| Symptom | Log / evidence | Likely cause | Contract |
| --- | --- | --- | --- |
| Login screen waits, then reports that the server is unreachable | No `RakNet base connection to Auth acquired`; "Connection to Auth timed out." | `AUTHSERVERIP` in `boot.cfg` is wrong, the auth server is not running, or a firewall blocks UDP 1001 | N5 |
| Connection is established but closed immediately | `RakNet base connection ... acquired` without `Connection to Auth confirmed` | Wrong RakNet password, network version, or RakNet version | N1–N3 |
| Login rejected with a message | Result code in `LOGIN_RESPONSE` | Wrong password, banned or locked account, missing play key | L1, L2 |
| After login, the client cannot reach the world | `Attempting to connect to World...` without confirmation | The login response contains an address the client cannot reach (for example `localhost` for a client on another computer, or an internal address behind NAT) | L1, T2 |
| Character selection does not appear | `Submitting Validation to World...` and nothing after it | The session key is not accepted on the world server (auth and world do not share sessions, e.g. master server not running) | L3 |

`Auth rejected/terminated connection.` right after the world connection starts is normal: the
client no longer needs the auth server.

## Zone loading

| Symptom | Log / evidence | Likely cause | Contract |
| --- | --- | --- | --- |
| "The client's map files revision checksum does not match the server's checksum." | — | Client and server have different map files, e.g. a modified `.luz`/`.lvl` on one side only | C1, C2 |
| Loading screen does not finish | `LoadThread_FinishLoadingZone` appears, but the game does not start | The server does not complete the zone-entry sequence: missing `CREATE_CHARACTER`, player construction, `SERVER_DONE_LOADING_ALL_OBJECTS`, or `PLAYER_READY` | Z2–Z8 |
| Loading screen does not finish, no `LoadThread` lines | `Received Load Zone` missing or with an unknown zone | Zone ID not in the client's `ZoneTable`, or the zone file is missing in the client | C1, Z1 |
| Client disconnects when a zone loads | Server-side disconnect reason "map load failure" | Server could not load the zone | — |
| Warning `unable to load .EVC file ... Defaulting` | — | The zone has no `.evc` environment file; the client uses defaults. Harmless. | — |
| World rejects the client right after validation | Server log mentions the FDB checksum | `check_fdb` is on and the client's `cdclient.fdb` differs from the server's | C4 |

## In the world

| Symptom | Likely cause | Contract |
| --- | --- | --- |
| Client crashes or freezes when a certain object comes into view | Its construction data is malformed: a component writes too many or too few bits, or the components do not match the client's `ComponentsRegistry` for that LOT | C3, O2–O5 |
| Objects are invisible, at the wrong place, or have wrong health bars, but only after another object was constructed | The same as above; one bad object shifts all following data in the packet | O3, O4 |
| Other players do not move or jump around | Position updates are not replicated, or the ghosting/scope update is missing | O6, section 6 |
| Clicking an NPC or object does nothing | The server does not react to `REQUEST_USE` for that object (missing server-side script or component) | section 6 |
| A minigame or activity UI stays empty or never ends | The client script waits for a network variable, notification, or event the server does not send | S1–S3 |
| Controls stay in a special mode after an activity | `SET_PLAYER_CONTROL_SCHEME` back to the normal scheme was not sent | section 6 |
| Texts show IDs or are empty | Text ID not in the client's `locale.xml`, e.g. content added only on the server | C1, C5 |
| The player can walk through walls or fall through the floor in one area | Client collision data (`.hkx`) or terrain differs from the server's map data | C1 |

## Client installation

| Symptom | Likely cause |
| --- | --- |
| "Create D3D9 instance...FAILED" in the log | Direct3D 9 is not usable: graphics driver problem, or under Wine/Proton a missing D3D9 implementation (`d3dx9_34.dll` itself ships with the client) |
| No sound | `USENDAUDIO=0`, muted categories in `lwo.xml`, or missing `.fev`/`.fsb` files |
| Settings are not taken from `lwo.cfg.default` | `lwo.xml` in the user profile overrides them; delete it to reset |
| Many `ResMgr could not find file` warnings | A few are normal even in a complete installation; many indicate missing `res` folders |
