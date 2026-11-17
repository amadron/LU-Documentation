# DarkflameServer content-authoring guide

This guide is for adding or changing **world content** for the local DarkflameServer source snapshot. It separates data/resource authoring from server-code changes; the right workflow depends on whether the feature already exists in the server.

## Choose the right path

| Goal | Usually involves | Start here |
|---|---|---|
| Add a map or scene | Zone-table metadata plus compatible zone/scene/resource assets and a way to reach the map | [Create or Extend a Zone](./create-or-extend-a-zone.md) |
| Place an existing object or NPC | Scene object data, an existing LOT/template, and the component registrations it needs | [Place Objects and Configure Spawners](./place-objects-and-configure-spawners.md) |
| Add spawn groups or moving content | Zone paths/spawner nodes and compatible LOT/component data | [Place Objects and Configure Spawners](./place-objects-and-configure-spawners.md) |
| Add server-side interaction or behavior | Existing native component/script, or a code change and C++ script registration | [Add Scripts and Server Behavior](./add-scripts-and-server-behavior.md) |
| Add a mission or other database-driven content | The relevant CDClient tables, object/NPC references, and any required runtime behavior | [Content Recipes](./content-recipes.md) and [CDClient Table Guide](./reference/cdclient-tables.md) |

## Read in this order

1. [Concepts and Prerequisites](./concepts-and-prerequisites.md): understand maps, instances, clones, source assets, and the data/code boundary.
2. Select the workflow above and follow its checklist.
3. Use the [Zone File Reference](./reference/zone-files-and-fields.md) and [CDClient Table Guide](./reference/cdclient-tables.md) when working with source formats and static data.
4. Validate with [Testing and Troubleshooting](./test-and-troubleshoot.md).
5. Use the [Content-to-Code Map](./reference/content-to-code-map.md) to trace a data field to its runtime consumer.

## Important scope note

The DarkflameServer repository is a server emulator, not a complete world editor or asset-authoring suite. The server reads zone, scene, level, and terrain resources supplied separately from the source checkout. These instructions explain the server-side dependencies and validation points; they do not claim that the repository can create or convert every client asset format.

The guides refer to source revision `8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4`. Confirm behavior against the source, CDClient database, resource archive, and client version you actually use.
