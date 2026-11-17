# Content-to-Code Map

Use this map to trace authored data into the runtime. A data record describes inputs; the linked code determines whether and how the server consumes them.

| Authored surface | Runtime path | Main source entry points |
|---|---|---|
| Zone ID and `zoneName` | Zone lookup and resource loading | [`Zone.cpp`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dZoneManager/Zone.cpp), [`dZoneManager.cpp`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dZoneManager/dZoneManager.cpp) |
| Zone boundary or scene transition | Destination resolution or scene graph | [`Zone.cpp`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dZoneManager/Zone.cpp), [`dZoneManager.cpp`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dZoneManager/dZoneManager.cpp), [`ZoneInstanceManager.cpp`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dNet/ZoneInstanceManager.cpp) |
| Scene placement and LOT | Level parsing → `EntityInfo` → entity construction | [`Level.cpp`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dZoneManager/Level.cpp), [`EntityManager.cpp`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/EntityManager.cpp), [`Entity.cpp`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/Entity.cpp) |
| `ComponentsRegistry` row | LOT/component lookup → native component creation | [`Entity.cpp`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/Entity.cpp), [`CDComponentsRegistryTable.h`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dDatabase/CDClientDatabase/CDClientTables/CDComponentsRegistryTable.h) |
| `ScriptComponent` row | Script name → registered native C++ factory | [`ScriptComponent.cpp`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dComponents/ScriptComponent.cpp), [`CppScripts.cpp`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dScripts/CppScripts.cpp) |
| Spawner path and nodes | Parsed path → spawner/node setup → entity spawn | [`Zone.cpp`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dZoneManager/Zone.cpp), [`dZoneManager.cpp`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dZoneManager/dZoneManager.cpp), [`Spawner.cpp`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dZoneManager/Spawner.cpp) |
| Mission/task rows | Mission component → task-specific progress handler | [`MissionComponent.cpp`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dComponents/MissionComponent.cpp), [`GameMessageHandler.cpp`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dGameMessages/GameMessageHandler.cpp) |
| Client request/game message | World packet → validation → handler/component/script | [`WorldServer.cpp`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dWorldServer/WorldServer.cpp), [`GameMessageHandler.cpp`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dGameMessages/GameMessageHandler.cpp) |
| Persistent character state | Component state → character XML or table interface | [`Character.cpp`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/Character.cpp), [`UserManager.cpp`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/UserManager.cpp) |

## How to use this map

1. Start at the authored row/resource and confirm it is present in the exact data snapshot used by the server.
2. Follow the first parser/lookup listed above and verify the runtime object is created.
3. Continue to the component/script/message consumer and verify its preconditions.
4. Trace client replication and persistence separately; they are different output paths.

The map gives entry points rather than every caller. Use symbol references and tests in the source checkout when tracing a specific implementation.
