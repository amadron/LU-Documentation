# Worlds Guide

[Game Guide](./README.md) | [Getting Started](./Getting%20Started.md) | [Quests](./Quest%20Guide.md) | [Pets](./Pet%20Guide.md) | [Racing](./Racing%20Guide.md)

Each world has its own missions, people, and activities. The names, routes,
and launch pads below come from the original client data (zone table, rocket
launch pad definitions, mission records, and English client strings). A stored
definition shows how the original game was set up; it does not prove that
every entrance, mission, or activity works on your server. Use your in-game
map and journal for the current route.

## The main worlds

| World | What to look for | Local reference |
|---|---|---|
| [Venture Explorer](./zones/1000.md) | The opening ship. Missions start with *Wake Up Call* ("Bob will tell you how to escape the ship!") and end with *Escape the Venture Explorer*: build a rocket and blast off to Avant Gardens. No launch pad leads back to this zone; see *Return to the Venture Explorer* below. | [Quest locations](./quests/locations/zone-1000.md) |
| [Avant Gardens](./zones/1100.md) | Early combat against the Maelstrom, the Sentinel camp, the Monument, and the Spider Cave. Missions start with *Get Help!* (find Epsilon Starcracker). Launch pads lead to Nimbus Station, the Block Yard and Avant Grove properties, and the *Return to the Venture Explorer* instance. | [Quest locations](./quests/locations/zone-1100.md) |
| [Nimbus Station](./zones/1200.md) | The central hub. Missions include *Find Mardolf the Orange*, *Rocket Builder*, and *Choose a Faction*. Launch pads lead to Avant Gardens, Pet Cove, Gnarled Forest, Forbidden Valley, Nexus Tower, and the Nimbus Rock and Nimbus Isle properties. Vertigo Loop Racetrack starts here. | [Quest locations](./quests/locations/zone-1200.md) |
| [Pet Cove](./zones/1201.md) | Pet taming: *Tame a Pet*, *Fetch!*, *Master Pet Tamer*, and Coalessa's pet-food requests. Reached by launch pad from Nimbus Station. | [Quest locations](./quests/locations/zone-1201.md) |
| [Gnarled Forest](./zones/1300.md) | Pirate-themed world. Missions start with *Bridge Out!*. Contains Cannon Cove Shooting Gallery, Keelhaul Canyon Racetrack, and the Chantey Shanty property. | [Quest locations](./quests/locations/zone-1300.md) |
| [Forbidden Valley](./zones/1400.md) | Ninja-themed world. Missions start with *Ravencloud Gate*. Contains the Forbidden Valley Dragon Battle, Dragonmaw Chasm Racetrack (at the Race Place), and the Raven Bluff property. | [Quest locations](./quests/locations/zone-1400.md) |
| [Nexus Tower](./zones/1900.md) | Home of the Nexus Force and the Faction Leaders; it protects the Imagination Nexus. Reached by launch pad from Nimbus Station. From here you reach Crux Prime and Ninjago Monastery. | [Quest locations](./quests/locations/zone-1900.md) |
| [Crux Prime](./zones/1800.md) | Battle world against the Maelstrom. Missions start with *Dropship Down!*. Reached from the Crux Prime launch bay (a console teleporter) in Nexus Tower. | [Quest locations](./quests/locations/zone-1800.md) |
| [Ninjago Monastery](./zones/2000.md) | The Ninjago world. Missions start with *See the Sensei!*. Reached by launch pad from Nexus Tower; the *Battle Against Frakjaw!* instance is here. | [Quest locations](./quests/locations/zone-2000.md) |
| [Starbase 3001](./zones/1600.md) | "Gateway to the New Worlds": the hub for the fan-built World Builder Planets. Reached through the Gateway in Nimbus Station. | [Quest locations](./quests/locations/zone-1600.md) |

The [world and zone database](./zones/README.md) links destinations to quest,
item, pet, and racing location evidence.
The [quest location index](./quests/locations/README.md) includes additional
areas from the local data. It lists candidate associations rather than
confirmed live spawns.

## How to travel

Most travel uses rocket launch pads. The client data stores these routes:

| From | Launch pad leads to |
|---|---|
| Venture Explorer | Avant Gardens (your first rocket flight) |
| Avant Gardens | Nimbus Station; Block Yard; Avant Grove; Return to the Venture Explorer |
| Nimbus Station | Avant Gardens; Pet Cove; Gnarled Forest; Forbidden Valley; Nexus Tower; Nimbus Rock; Nimbus Isle |
| Pet Cove, Gnarled Forest, Forbidden Valley | Nimbus Station; each world's own property (Chantey Shanty, Raven Bluff) |
| Nexus Tower | Nimbus Station; Ninjago Monastery |
| Ninjago Monastery | Nexus Tower |
| LEGO Club | Avant Gardens; Gnarled Forest; Forbidden Valley |
| Starbase 3001 | The World Builder Planets |

Conditions stored in the data:

- **Gnarled Forest and Forbidden Valley** launch pads require the mission
  [*Choose a Faction*](./quests/474.md). Otherwise the pad shows: "Faction
  members only. Find the Recruiter in Nimbus Station and join a Faction!" See
  the [Faction Guide](./Faction%20Guide.md).
- **Alternative landings:** launching to Gnarled Forest while wearing pirate
  gear (for example a Black Pirate Hat) lands you at the beach ("Equip a pirate
  hat to land at the beach!"). Launching to Forbidden Valley while wearing a
  Maelstrom-Infused Ninja Hood lands you at a different spawn point.
- **Starbase 3001's launcher** requires the mission
  [*Travel to the Stars*](./quests/956.md) ("Talk to Hess LaCoil in Starbase
  3001.").
- **Crux Prime** has no rocket pad in the data; it is reached from a console in
  Nexus Tower ("Do you want to travel to Crux Prime?").
- **Starbase 3001** is reached through the Gateway in Nimbus Station
  ("Interact with the Gateway to travel to Starbase 3001."). The LEGO Club is
  also reached through a door in Nimbus Station.

## Activities and side areas

| Area | Where | Notes |
|---|---|---|
| [Return to the Venture Explorer](./zones/1001.md) | Launch pad in Avant Gardens | Battle instance; mission [*Return to the Venture Explorer*](./quests/1071.md) ("Use the launchpad behind me to rocket back to the Venture Explorer!"). |
| [Avant Gardens Survival](./zones/1101.md) | Avant Gardens | Survival battle instance. |
| [Spider Queen Battle](./zones/1102.md) | Block Yard and the Spider Cave | Confront her when you claim the Block Yard property, then again in a battle instance; look in the Spider Cave to join. |
| [The Battle of Nimbus Station](./zones/1204.md) | Nimbus Station | "Travel back in time and defend Nimbus Station from a Maelstrom invasion!" Team up and find Wenn Wuzzit. |
| [Vertigo Loop Racetrack](./zones/1203.md) | Nimbus Station | See the [Racing Guide](./Racing%20Guide.md). |
| Cannon Cove Shooting Gallery | Gnarled Forest | Shooting gallery instance. |
| [Keelhaul Canyon Racetrack](./zones/1303.md) | Gnarled Forest | Racing. |
| [Forbidden Valley Dragon Battle](./zones/1402.md) | Forbidden Valley | Dragon fight instance. |
| [Dragonmaw Chasm Racetrack](./zones/1403.md) | Forbidden Valley | "Look for the Race Place in Forbidden Valley!" |
| [Battle Against Frakjaw!](./zones/2001.md) | Ninjago Monastery | Battle instance. |

**Properties** (launch pads in the matching world): [Block Yard](./zones/1150.md)
and [Avant Grove](./zones/1151.md) in Avant Gardens,
[Nimbus Rock](./zones/1250.md) and [Nimbus Isle](./zones/1251.md) in Nimbus
Station (Nimbus Isle's pad is by the water's edge in Brick Annex),
[Chantey Shanty](./zones/1350.md) in Gnarled Forest, and
[Raven Bluff](./zones/1450.md) in Forbidden Valley. Most have a "Clear ...!"
mission, such as *Clear Nimbus Rock!*. See the
[Building Guide](./Building%20Guide.md).

**World Builder Planets** (from Starbase 3001; "These are exciting LEGO
Universe worlds created by LEGO fans!"): DeepFreeze (Luptario's Winter
Wonderland), Robot City (DeerBite's Metropolis of Robots), MoonBase (Alpha
Team's Moonbase), and Portabello (Brickazon's Fantasy Land). Quest locations:
[1601](./quests/locations/zone-1601.md), [1602](./quests/locations/zone-1602.md),
[1603](./quests/locations/zone-1603.md), [1604](./quests/locations/zone-1604.md).

## Explore without missing a lead

1. On arrival, use the map and speak to available mission characters.
2. Track the exact objective before traveling; some tasks need a specific
   interaction, item, or result.
3. Each world has hidden Heart Flags or Backpack Flags; finding all of them
   earns more Life or Backpack space. Nimbus Station also offers a *Treasure
   Hunter* mission for each world. Use the journal to confirm credit.
4. Before traveling away, review unfinished tasks. The Venture Explorer itself
   cannot be revisited by launch pad; later visits use the *Return to the
   Venture Explorer* instance.

For activity-specific details, see the [Pet Guide](./Pet%20Guide.md),
[Racing Guide](./Racing%20Guide.md), and
[Building Guide](./Building%20Guide.md).

## Source and limitations

World names, zone summaries, launch pad routes and conditions, mission names,
and loading-screen tips come from the original client data: the `ZoneTable`,
`RocketLaunchpadControlComponent`, `Preconditions`, `Missions`, and
`ZoneLoadingTips` tables of the client database, with English text from the
client's `locale.xml`. Travel to Starbase 3001, the LEGO Club, and Crux Prime by
console or door is taken from the DarkflameServer scripts and the matching
client strings. The general tone and exploration advice were first summarized
from the user-provided *LEGO Universe Official Game Guide* (2010), pp. 89–164.
None of these sources alone proves that an activity is available in a
particular deployment.
