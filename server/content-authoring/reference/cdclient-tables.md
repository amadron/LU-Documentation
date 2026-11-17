# CDClient Table Guide for Content Authors

This page maps common authoring tasks to the locally documented CDClient tables and server consumers. For every field, use the table reference and verify the corresponding server handler; the same column can be interpreted differently by different code paths.

## Zones and world behavior

| Authoring need | Table/reference | Server connection |
|---|---|---|
| Map ID, resource name, population and zone policy | [`ZoneTable`](../../../db/ZoneTable.md) | `Zone`, `dZoneManager`, `InstanceManager`, and location-save logic |
| Global movement, physics, and gameplay defaults | [`WorldConfig`](../../../db/WorldConfig.md) | `dZoneManager::LoadWorldConfig` and gameplay systems |
| Scene-related definitions | [`SceneTable`](../../../db/SceneTable.md) | Zone/scene consumers; the zone resource still provides scene references and files |

## Objects and native behavior

| Authoring need | Table/reference | Server connection |
|---|---|---|
| LOT/template identity and object metadata | [`Objects`](../../../db/Objects.md) | Entity creation and template metadata |
| Which component types a LOT registers | [`ComponentsRegistry`](../../../db/ComponentsRegistry.md) | `Entity::Initialize` selects native component construction paths |
| Server/client script names | [`ScriptComponent`](../../../db/ScriptComponent.md) | `Entity::Initialize`, `ScriptComponent`, and `CppScripts` |
| Physics/destruction/interaction configuration | [`PhysicsComponent`](../../../db/PhysicsComponent.md), [`DestructibleComponent`](../../../db/DestructibleComponent.md) | Corresponding native components, when implemented |
| Object skills and behavior parameters | [`ObjectSkills`](../../../db/ObjectSkills.md), [`SkillBehavior`](../../../db/SkillBehavior.md), [`BehaviorParameter`](../../../db/BehaviorParameter.md) | Skill and behavior handlers/components |
| Loot or vendor data | [`LootMatrix`](../../../db/LootMatrix.md), [`LootTable`](../../../db/LootTable.md), [`VendorComponent`](../../../db/VendorComponent.md) | Loot and vendor gameplay systems |

## Mission content

| Authoring need | Table/reference | Server connection |
|---|---|---|
| Mission definition | [`Missions`](../../../db/Missions.md) | Mission component and mission handlers |
| Objectives/tasks | [`MissionTasks`](../../../db/MissionTasks.md) | Task-type-specific server progression |
| NPC mission offer/turn-in association | [`MissionNPCComponent`](../../../db/MissionNPCComponent.md) | Mission NPC component and mission availability |
| Mission text | `MissionText` in the [database reference](../../../db/README.md) | Client presentation; availability of localized source text depends on data |
| Rewards | `Rewards` in the [database reference](../../../db/README.md) | Reward processing and persistence |

The links point to the local exported database documentation. They describe the inspected data snapshot and are not an editor interface or a guarantee that every listed row is active in a particular server configuration.

## Suggested dependency walk

For a new entity-driven feature, follow this dependency chain:

```text
ZoneTable / zone resource
  -> scene placement or path
  -> Objects LOT
  -> ComponentsRegistry
  -> supporting component/script/behavior tables
  -> native server implementation
  -> runtime messages, replication, and persistence
```

If any link in the chain is absent, decide whether the feature should be data-only, needs a server implementation, or depends on client content outside this repository.
