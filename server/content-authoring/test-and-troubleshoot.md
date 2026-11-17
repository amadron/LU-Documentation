# Test and Troubleshoot Content

## 1. Validate in layers

Test from the lowest dependency upward. This makes resource, static-data, and code failures easier to separate.

| Layer | Validation |
|---|---|
| Resource lookup | `zoneName` resolves to the zone file; scene/level files and required referenced assets are available to `AssetManager`. |
| Zone parsing | World starts the intended map, loads its scenes and paths, and builds the scene graph without parse/load errors. |
| Static data | Referenced map IDs, LOTs, component IDs, script IDs, and task/reward references exist in the same CDServer snapshot. |
| Entity construction | Object receives the expected components and script; transform, settings, parent/group data are correct. |
| Runtime behavior | Spawn activation, interactions, transfer routes, and state transitions occur as expected. |
| Replication | A ready client in range sees the entity; visibility changes do not leave stale or missing replicas. |
| Persistence | Character/property changes survive leaving the zone and reconnecting, where persistence is intended. |

Keep test saves and databases isolated. Reusing an old character can hide spawn, initial-state, or saved-location defects.

## 2. Common symptoms

| Symptom | Likely layer | First checks |
|---|---|---|
| Master cannot start or find a zone | Zone metadata/resources | `ZoneTable.zoneName`, `maps/` layout, CDServer file availability, asset path and case. |
| World process starts but never becomes ready | World startup | Zone parser errors, required scene/level assets, CDClient initialization, master connection, and zone-control creation. |
| Zone loads but has no objects | Scene/level content | Scene references, object placements, LOTs, level parsing, and scene graph. |
| Object is present but invisible to a player | Entity/replication | Player readiness, ghost reference point, zone visibility distances, collectable state, and construction logs. |
| Object appears but has no behavior | Data/code bridge | LOT registrations, supporting tables, `script_name`, exact C++ registry key, and callback path. |
| Spawner exists but produces nothing | Path/runtime policy | Spawner path type, valid nodes/LOT, activation, node limits, maintained/max counts, and group triggers. |
| Transfer request does not complete | Routing | Target map/clone, active instance capacity, target readiness, scene boundary or callback path, and master/world logs. |
| Progress disappears after moving or reconnecting | Persistence | Is the state meant to be XML-backed or stored in another table? Check save call, component XML hooks, and save-location policy. |

## 3. Test sequence for a new zone

1. Start with one zone and the smallest valid scene/resource set.
2. Load it using the master-managed process path and verify `WORLD_READY`.
3. Enter through a controlled transfer and confirm spawn coordinates, scene identification, and return/exit.
4. Add one static object, then one component-driven object, then one spawner; validate each before continuing.
5. Add script or mission behavior only after the base entity and its dependencies work.
6. Test from a clean character and repeat after zone exit/re-entry.
7. Check server and client logs and record the source data revision used.

For server startup, world loading, and transfer ownership see [Architecture and Repository Structure](../DarkflameServer%20Architecture%20and%20Repository%20Structure.md); for entity lifecycle see [World Simulation and Entity Model](../DarkflameServer%20World%20Simulation%20and%20Entity%20Model.md).

## 4. Limits of a successful server test

A server-side load test does not prove that a stock client can discover or display a new zone. Client UI, client-side scripts, localization, client assets, and matching client data may also be required. Conversely, an object that renders on a client is not proof that the server has the corresponding authoritative interaction or persistence behavior.

If server code changes are required, use the main repository's build instructions and respect its CMake source-path constraints. This guide does not claim that content data alone can implement a new protocol or gameplay capability.
