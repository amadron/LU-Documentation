# DarkflameServer Libraries

[Server documentation](./README.md) | [Architecture](./DarkflameServer%20Architecture%20and%20Repository%20Structure.md) | [Client libraries](../client/Client%20Libraries.md)

DarkflameServer is written in C++ and builds with CMake. Apart from the system C/C++
runtime, it relies on the third-party libraries below. Most are kept in the repository under
`thirdparty/`, some are Git submodules, and a few are downloaded by CMake while configuring
the build.

Checked against DarkflameServer revision
[`8b7d1b9`](https://github.com/DarkflameUniverse/DarkflameServer/tree/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4)
(28 October 2026). Versions change between revisions; `thirdparty/`, `.gitmodules`, and the
`cmake/` folder of your checkout are authoritative.

## Libraries in the server

| Library | Version | Included as | Used for | Used in | License |
| --- | --- | --- | --- | --- | --- |
| [RakNet](https://github.com/facebookarchive/RakNet) | 3.25 (modified) | Copied into `thirdparty/raknet` | UDP networking with the game client. The original client was built against RakNet, so the server must speak the same version of the protocol. | `dNet` and all servers | Original RakNet license (see the folder) |
| [MariaDB Connector/C++](https://github.com/mariadb-corporation/mariadb-connector-cpp) | 1.1.7 (Connector/C 3.4.8 on Windows) | Submodule; prebuilt connector downloaded on Windows | Connection to the MySQL/MariaDB game database (accounts, characters, properties) | `dDatabase/GameDatabase/MySQL` | LGPL 2.1 |
| [SQLite](https://www.sqlite.org/) | 3.47.1 | Copied into `thirdparty/SQLite` | Reading the CDClient/CDServer content database; optional SQLite game database | `dDatabase` | Public domain |
| [tinyxml2](https://github.com/leethomason/tinyxml2) | Submodule commit `a977397` | Submodule | Reading and writing XML: character data (inventory, missions, stats), configuration, and level data | `dGame`, `dCommon`, `dZoneManager` | zlib |
| [Recast & Detour](https://github.com/recastnavigation/recastnavigation) | Submodule commit `9f4ce64` | Submodule | Navigation meshes and pathfinding for NPCs and enemies | `dNavigation`, `dPhysics` | zlib |
| [libbcrypt](https://github.com/trusch/libbcrypt) | Submodule commit `d6523c3` | Submodule (built from its source files) | Hashing and checking account passwords | `dDatabase`, `dNet`, `dMasterServer` | See its repository |
| [magic_enum](https://github.com/Neargye/magic_enum) | Submodule commit `e55b9b5` | Submodule | Converting enums to readable names (logging, commands, web API) | `dCommon`, `dNet`, `dWeb`, `dChatServer` | MIT |
| [nlohmann/json](https://github.com/nlohmann/json) | 3.11.3 | Copied into `thirdparty/nlohmann` | JSON for the web API and chat server messages | `dCommon`, `dChatServer`, `dWeb` | MIT |
| [Mongoose](https://github.com/cesanta/mongoose) | 7.16 | Copied into `thirdparty/mongoose` | Embedded HTTP server for the web interface/API | `dWeb` | GPL 2.0 or commercial |
| [cpplinq](https://github.com/mrange/cpplinq) | Single header | Copied into `thirdparty/cpplinq` | LINQ-style queries over the cached CDClient tables | `dDatabase` (21 table classes) | Microsoft Public License |
| MD5 (RSA reference implementation) | — | Copied into `thirdparty/MD5` | MD5 checksum of the client's `cdclient.fdb` (optional `check_fdb` setting, compares the player's client database) | `dNet`, `dWorldServer` | RSA MD5 license |
| [GLM](https://github.com/g-truc/glm) | 1.0.3 | Downloaded by CMake (`FetchContent`) | Vector and matrix math | `dGame`, `dCommon`, `dNet` | MIT |
| [zlib](https://zlib.net/) | System library, or 1.3.2 downloaded by CMake | System package or `FetchContent` | Compression: the client's packed asset files (`.pk`, `.sd0`) and compressed world packets | `dCommon`, `dNet` | zlib |

## Build and test only

| Library | Version | Included as | Used for |
| --- | --- | --- | --- |
| [GoogleTest](https://github.com/google/googletest) | release-1.12.1 | Downloaded by CMake | Unit tests in `tests/` |
| [libbacktrace](https://github.com/ianlancetaylor/libbacktrace) | Latest at build time | Optional download (Linux, `INCLUDE_BACKTRACE`) | Readable stack traces in crash logs |
| `dl`, `pthread` | System | Linked on Linux/macOS | Dynamic loading and threads |

## Source code availability

All libraries the server uses are open source; that is why DarkflameServer can ship them in its
repository or download them while building. The one special case is **RakNet**: the server uses
a modified copy of version 3.25 kept in `thirdparty/raknet`, chosen for compatibility with the
game client. RakNet was released as open source under a BSD license by Oculus in 2014
([repository](https://github.com/facebookarchive/RakNet)), but that release is the later 4.x
line; the 3.x versions were originally distributed under the license terms of their time. See
the license notes in `thirdparty/raknet`.

The [client libraries page](../client/Client%20Libraries.md#source-code-availability)
lists which client components are open source and which open alternatives exist.

## Notes

- **No physics engine.** The original client uses Havok (see the
  [client libraries](../client/Client%20Libraries.md)). DarkflameServer does not use
  Havok or another physics library; `dPhysics` contains its own simple shapes and collision
  checks.
- **Client data is read directly.** The server reads the game's content database
  (`CDServer.sqlite`, a SQLite conversion of the client's `cdclient.fdb`) and the client's
  map files (`.luz`, `.lvl`) with its own code; no third-party format library is involved.
- **Licenses.** The license column is a summary for orientation. Check the license files in
  each library's folder or repository before redistributing a build.
