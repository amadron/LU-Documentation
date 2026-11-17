# Concepts and Prerequisites

## Scope and evidence

This page establishes the terms used by the content-authoring guides. It describes the local [DarkflameServer source](https://github.com/DarkflameUniverse/DarkflameServer/tree/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/) at revision `8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4`.

## 1. A world feature can span three layers

| Layer | Examples | Primary consumer |
|---|---|---|
| Resource assets | Zone `.luz`, referenced scene/level files, terrain, and optional trigger data | `AssetManager`, `Zone`, `Level`, and `dZoneManager` |
| Static client data | Zone metadata, object/LOT rows, component registrations, script names, missions and behavior parameters | `CDClientDatabase` table wrappers and game systems |
| Server implementation | Entity/component logic, native C++ scripts, message handlers, transfer and persistence code | `WorldServer`, `dGame`, `dScripts`, and related modules |

An object can exist in the database but fail to appear if its scene/resource is absent. A scene can load an object whose expected component or script data is missing. A data record can point to a script name for which the current server has no native implementation. Validate all applicable layers rather than treating one row or one code change as the whole feature.

## 2. Map, instance, clone, scene

- **Map/zone ID** selects the world definition. `CDZoneTable` supplies metadata such as `zoneName`, population caps, zone-control template, script ID, and zone policy.
- **Instance ID** identifies one running world process for that map. The master assigns it and selects an endpoint.
- **Clone ID** distinguishes variants/parallel copies of a map. Clone and instance are not interchangeable.
- **Scene ID/layer** identifies a scene inside a map. Scene transitions connect scenes; they are not the same as a master-routed map transfer.

At runtime these values are carried in `LWOZONEID`. A new map row alone does not provide a scene, assets, a client route, or gameplay content.

## 3. What the repository does and does not provide

The server code parses existing zone and level resources, reads CDClient data, creates entities/components, runs native server logic, and routes players between zones. The repository does not include LEGO Universe client assets and is not, by itself, a full scene/terrain editor.

Before planning a new map, establish that you have:

- a unique map ID and a compatible client/CDClient data set;
- a zone resource whose path matches the `zoneName` lookup;
- all referenced scene/level/terrain assets in the resource set visible to `AssetManager`;
- a valid entry route or a controlled test route; and
- a test server/database isolated from any live data.

Use the [Zone File Reference](./reference/zone-files-and-fields.md) to understand what the current parser consumes. File-version enum values and parser branches are evidence about this checkout, not a guarantee of compatibility with arbitrary exporters.

## 4. Determine whether code is required

Start with the existing object and component data:

1. Find the LOT in [`Objects`](../../db/Objects.md).
2. Check its [`ComponentsRegistry`](../../db/ComponentsRegistry.md) registrations.
3. Follow each component type to its native implementation and supporting table.
4. For script-driven behavior, check [`ScriptComponent`](../../db/ScriptComponent.md) and the server-side script registry.

If existing components/scripts express the behavior, content changes may be enough. If the behavior needs a new message handler, component, script callback, persistence rule, or transfer rule, a C++ change is required. The server's object/component model is described in [World Simulation and Entity Model](../DarkflameServer%20World%20Simulation%20and%20Entity%20Model.md).

## 5. Safe authoring workflow

- Keep source assets, CDClient changes, and server-code changes in a reproducible test copy.
- Record the map ID, LOTs, component IDs, script names, and resource paths changed.
- Avoid editing the only copy of a database or resource archive.
- Validate loading before adding more content; then validate behavior and persistence.
- Distinguish client presentation from server implementation. A client script name or visual asset does not mean the server has matching logic.

For table ownership and migration boundaries, see [Data and Persistence Reference](../DarkflameServer%20Data%20and%20Persistence%20Reference.md).
