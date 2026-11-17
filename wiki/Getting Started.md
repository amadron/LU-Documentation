# Getting Started

[Game Guide](./README.md) | [Worlds](./Worlds%20Guide.md) | [Quests](./Quest%20Guide.md) | [Items](./Item%20Guide.md)

New to LEGO Universe? Start with the missions in front of you, take time to
explore, and use the **Mission Tracker** (the orange circle at the top of the
screen) to see what to do next. Your **Passport** lists Achievements to
complete. The route below follows the mission chains stored in the original
client database; individual servers may change missions, controls, or
available activities.

## Your first adventure

1. **[Venture Explorer](./zones/1000.md):** the ship has been attacked by the
   Maelstrom. Jett Moonshot - Venture League Officer starts you on
   [Wake Up Call](./quests/1727.md) ("Talk to Bob"). Then:
   - [Your Creative Spark](./quests/173.md) — Bob asks you to collect 6
     Imagination power-ups. It rewards 100 coins and +6 maximum Imagination;
     completing it also unlocks your Imagination
     ([Unlock Your Imagination](./quests/664.md)).
   - [Bounce to Sky Lane](./quests/660.md) — build a bouncer to reach
     Sky Lane - Venture League Explorer.
   - [Venture into Knowledge](./quests/1896.md) — Sky Lane introduces the
     Mission Tracker.
   - [Not Enough Lifepods?](./quests/308.md) — collect 3 rocket parts (a Nose
     Cone, a Cockpit and an Engine; check the upper platforms for the Engine).
     Rewards include the [Thinking Hat](./items/6086.md) ("Wear this hat to
     start building!").
   - [Escape the Venture Explorer](./quests/1732.md) — build your rocket,
     blast off, and talk to Wisp Lee when you land on Avant Gardens.

   Look around before leaving: the ship also has Achievements such as
   [Spaceship Observer](./quests/488.md) (use all 5 binoculars),
   [The Venture Explorer Story](./quests/757.md) (read all Story Plaques) and
   [Classic Rocketeer](./quests/354.md) (find all 3 white rocket modules).
   The original guide treats this first visit as a one-way trip. The data
   does include a later return: after
   [Choose a Faction](./quests/474.md), Sky Lane offers
   [Return to the Venture Explorer](./quests/1071.md), which leads to the
   separate [Return to the Venture Explorer](./zones/1001.md) battle instance.
2. **[Avant Gardens](./zones/1100.md):** Wisp Lee - Paradox Researcher sends
   you to Epsilon Starcracker - Nexus Force Scout ([Get Help!](./quests/311.md),
   with a choice of [Basic Shortsword](./items/4880.md),
   [Basic Spear](./items/4881.md) or [Basic Hammer](./items/4883.md)).
   Equip it for To Arms!, then [Smash Or Be Smashed](./quests/312.md)
   (smash 15 Stromlings). Beck Strongheart - Sentinel Faction Commander then
   teaches salutes, armor (buy Armor Polish), Quick Build turrets, the Sentinel
   Shield and your Action Bar, and finally
   [Impress the Sentinel Faction](./quests/479.md) asks you to last 1 minute in
   the Survival challenge. Later chains take you to Melodie Foxtrot, to
   Rusty Steele - Assembly Foreman and the Monument
   ([A Monumental View](./quests/318.md)), and to Vance Bulwark - Property
   Guard for your first property missions. The area ends with
   [Check In with Sky Lane](./quests/320.md).
3. **[Nimbus Station](./zones/1200.md):** [Faction Time](./quests/483.md) sends
   you to Nexus Jay - Nexus Force Recruiter. He sends you to Mardolf the
   Orange - Assembly Wizard ([Find Mardolf the Orange](./quests/476.md),
   Rocket Builder) and Johnny Thunder - Venture League Hero (A Thunderous
   Collection), whose [Choose a Faction](./quests/474.md) leads to your faction
   choice. After that, Nexus Jay's "Get your … Gear!" missions send you to the
   faction vendors for your Specialty Kit. The
   [Faction Guide](./Faction%20Guide.md) helps you compare the choices.
4. **Pet Cove and beyond:** in [Pet Cove](./zones/1201.md), Coalessa - Assembly
   Mystic offers [Tame a Pet](./quests/110.md) (see the
   [Pet Guide](./Pet%20Guide.md)). Once you have a Specialty Kit, Nexus Jay's
   [Head to Gnarled Forest](./quests/779.md) points you to Hugo First -
   Venture League Grunt in [Gnarled Forest](./zones/1300.md). In
   [Forbidden Valley](./zones/1400.md), Ninja Tashi - Ninja Scout starts
   Ravencloud Gate. Racing begins with Velocity Lane - Racing Trainer in
   Nimbus Station (see the [Racing Guide](./Racing%20Guide.md)).

The order above follows the stored mission prerequisites; it is not a
guarantee for every server. For world-specific ideas and related entries,
see the [Worlds Guide](./Worlds%20Guide.md) and the
[quest database](./quests/README.md).

## Health, Armor, and Imagination

Three resources are worth watching:

- **Health** measures how much damage you can take before being smashed.
  The player definition in the client database starts with 4 Health.
- **Armor** absorbs damage before your Health; it comes from equipment
  (the player starts with 0 Armor). Beck Strongheart's Sentinel Shine mission
  introduces it.
- **Imagination** powers abilities and some builds. The player starts with
  0 Imagination; Your Creative Spark grants the first +6. Collecting the
  Imagination Brick in a world (the "A Creative Opportunity" Achievements in
  Avant Gardens and Nimbus Station) adds +1 more, and the Avant Gardens Flag
  Hunter Achievement (10 Heart Flags) adds +1 Health.

Look for pickups when your resources are low and read an item's effects
before equipping it. Some abilities require Imagination, so check the
on-screen feedback if one does not activate. Current values, equipment effects,
and recovery rules depend on the server and the specific item.

## Combat and rebuilding

Approach unfamiliar enemies carefully, keep moving, and compare the weapon
and ability descriptions in your inventory. Some weapons have successive
attacks or charged abilities; try them where there is room to retreat.
If you are smashed, the client shows "Smashed!" and a **Rebuild** button;
check your health, resources, and mission progress before trying again.

When you are smashed you drop some coins. The client database sets this to
1% of your coins (at least 1, at most 10,000), and all the starting worlds
above have coin loss enabled. In the DarkflameServer source the lost coins are
dropped as loot at your position, and coin loss is skipped in hardcore mode.

## Useful habits

- Read the current mission objective in the Mission Tracker and check your
  Passport for Achievements.
- Search the [item database](./items/README.md) when you need a lead on gear,
  and the [NPC index](./quests/NPC%20Index.md) when looking for a character.
- Ask other players for help when an activity supports groups.
- Treat controls shown by your client as authoritative; bindings may differ.
  (Mission texts mention, for example, pressing 3 for the Sentinel Shield
  skill and loading items into slot 5 of the Action Bar.)

## Source and limitations

Originally based on the user-provided *LEGO Universe Official Game Guide*
(2010), pp. 6–14, 20–21, and 89–96; this is a new summary, not a
reproduction of the book. Mission names, NPC names, objectives, rewards,
prerequisites, player starting stats and coin-loss values were checked
against the original client data: the `Missions`, `Objects`,
`DestructibleComponent`, `ZoneTable` and `WorldConfig` tables of the client
database (CDServer.sqlite) and the English strings in `locale.xml`. Coin-drop
behavior was also checked in the DarkflameServer source. These are stored
definitions, not proof that everything works the same way on a particular
DarkflameServer deployment.
