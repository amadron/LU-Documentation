# Add Scripts and Server Behavior

## 1. Decide whether a script is sufficient

First determine whether an existing native component or C++ script already provides the required behavior. Content data can select and configure implemented behavior; it cannot create a new server capability by itself.

The relevant bridge is:

```text
CDClient object/component/script records
  -> Entity::Initialize
  -> ScriptComponent
  -> CppScripts name registry
  -> native C++ script class
  -> Entity/component/GameMessages callbacks
```

See [`Entity.cpp`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/Entity.cpp), [`ScriptComponent.cpp`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dComponents/ScriptComponent.cpp), and [`CppScripts.cpp`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dScripts/CppScripts.cpp).

## 2. Data names are registry keys

The `ScriptComponent` table provides `script_name` and `client_script_name`. The server-side name is looked up in `CppScripts`; many historical identifiers end in `.lua`, but in this implementation they are identifiers for native C++ factories, not Lua files that the server generally interprets.

If the name has no server-side mapping, `CppScripts::GetScript` returns `InvalidScript` (and logs a diagnostic for non-empty names not on its excluded list). Adding a row or changing a string without adding the matching registry mapping does not implement the behavior.

The client-script name is a separate field and does not substitute for server logic. Client presentation and server authority should be tested independently.

## 3. Register a native behavior

When a new server behavior genuinely requires code:

1. Find the nearest existing script/component pattern with similar callbacks and ownership.
2. Implement the native behavior through the established `CppScripts::Script` and/or component interfaces.
3. Register the exact script identifier in `CppScripts.cpp` and ensure its headers/source are included in the existing build target.
4. Add or update the relevant CDClient component/script records in the test data.
5. Validate entity creation, callback invocation, state changes, client response/replication, and cleanup.
6. If state must survive a restart, implement and test the persistence path separately.

Do not put stateful per-entity data in a script object unless the existing script API supports that ownership model. `ScriptComponent` treats registered script objects as shared and warns against deleting them per component; use the entity/component state model for per-object state.

## 4. Prefer the narrowest extension point

| Requirement | Prefer |
|---|---|
| Existing behavior with different data values | Existing component and CDClient data |
| Object event/lifecycle behavior with existing script callbacks | Registered native script |
| Reusable domain state updated/serialized/persisted for an entity | Native component |
| New client request or protocol operation | Message enum, parser/dispatcher, validation, handler, and response path |
| New zone transition or instance-selection policy | Existing transfer API if possible; otherwise master/world control-plane code |
| New persistent record type | Game-database table interface, backend implementations, migrations, and tests |

For message routing, access checks, and serialization layers, use the [Client-Server Protocol and Gameplay guide](../DarkflameServer%20Client-Server%20Protocol%20and%20Gameplay.md). For component lifecycle and update behavior, use [World Simulation and Entity Model](../DarkflameServer%20World%20Simulation%20and%20Entity%20Model.md).

## 5. Script validation

- Confirm the exact `script_name` string in CDClient.
- Confirm that `CppScripts.cpp` contains the exact key and correct factory.
- Check the server log for `InvalidScript` diagnostics.
- Confirm the entity is created with the script component and its expected settings.
- Trigger the specific callback; entity construction alone does not prove that the callback path is active.
- Verify client output and persisted state separately.
