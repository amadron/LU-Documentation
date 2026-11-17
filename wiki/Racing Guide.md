# Racing Guide

[Game Guide](./README.md) | [Quest Guide](./Quest%20Guide.md) | [Item Guide](./Item%20Guide.md)

Racing in LEGO Universe means building your own modular car and racing it
against other players on a three-lap track. The client data defines four car
racetracks, a racing mission chain with three racing NPCs, and a large set of
racing achievements. A stored track definition does not guarantee that every
race is enabled on the server you play on.

## The racetracks

| Track (client name) | Where the entrance is | Track page |
| --- | --- | --- |
| Vertigo Loop Racetrack | Race Place, Nimbus Station | [Vertigo Loop](./racing/tracks/vertigo-loop.md) · [zone 1203](./zones/1203.md) |
| Keelhaul Canyon Racetrack | Race Place, Gnarled Forest | [Keelhaul Canyon](./racing/tracks/keelhaul-canyon.md) · [zone 1303](./zones/1303.md) |
| Dragonmaw Chasm Racetrack | Race Place, Forbidden Valley | [Dragonmaw Chasm](./racing/tracks/dragonmaw-chasm.md) · [zone 1403](./zones/1403.md) |
| Space Blizzard Racetrack | Frostburgh Race Place (seasonal winter world) | [Space Blizzard](./racing/tracks/space-blizzard.md) · [zone 1261](./zones/1261.md) |

Space Blizzard was a winter event track. Its activity and server script are
present, but the local ZoneTable has no row for its race instance, so expect it
to be unavailable unless your server has added it.

Each entrance is a **Race Activator** at that world's Race Place. Mission text
tells you how to use it: "Drag a car model from your Backpack to the Race
Activator to start the event."

## Get your first car

The Nimbus Station racing chain is given by **Velocity Lane - Racing Trainer**
at the Nimbus Station Race Place. It becomes available after you complete one
of the faction Specialty Kit missions in Nimbus Station (Assembly, Venture
League, Paradox or Sentinel).

1. **[Get Ready to Race!](./quests/622.md)**: "Purchase a Car Chassis from
   Ludwig Clutchburn, the Nimbus Station Racing Vendor." The
   [Car Chassis](./items/8129.md) has a base value of 500 coins, and
   **Ludwig Clutchburn - Racing Vendor** sells it at that price (vendor buy
   scale 1.0). The reward is a [Red Hyperstarter Package](./items/9466.md):
   "Double-click to get the red Hyperstarter Car modules!"
2. **[Build Your Ride!](./quests/623.md)**: "Build your first modular car!"
   The Build Area is the gray platform next to Velocity Lane; "Interact with
   the car hologram on the Build Area to build a car." Reward: 3
   [Green Imaginite](./items/3039.md).
3. **[Enter a Race](./quests/624.md)**: "Compete in your first race at the
   Vertigo Loop racetrack."
4. **[Speed Boost!](./quests/625.md)**: "Collect Imagination during a race to
   use Boost!" Reward: [Red Racing Helmet](./items/7730.md).

A car is built from a chassis plus module slots such as wheels, front and rear
bumpers, engine panel, side panels and rear panel. Ludwig Clutchburn also sells
parts from the Hyperstarter, Chase Cutter, Thrust Bucket, Bolt Ox and Paragon
Warp families, plus racing helmets in several colors. The
[race car reference](./racing/tracks/race-cars-and-modules.md) has more on
the module items.

## How a race works

- **Racers:** 2 to 6 players, each racing alone (no teams). The race needs at
  least 2 players to start.
- **Laps:** 3 laps on every track.
- **Entry cost:** each track's activity lists 1 Green Imaginite as its cost.
- **Start:** On DarkflameServer, once two racers have loaded, the others have
  about 15 seconds to load. A player left alone for 30 seconds is sent back to
  the main world. Solo racing is off by default; server operators can turn it
  on with the `solo_racing` setting.

### Imagination and boost

Your car starts each race with 0 Imagination and holds up to 60.

- **Imagination power-ups** on the track give +10 each.
- **Imagination crates**: smashing one with your car refills the car to 60.
- **Boost** uses the Imagination you have. The boost skill checks your total
  and spends 60 for a 3.5-second boost, 40 for a 2-second boost, or 20 for a
  1-second boost. Below 20 it does nothing.

### Wrecks and smashables

Your car is wrecked when the game registers a crash or you fall off the
track. You respawn on the track after about 2 seconds, with half your
Imagination rounded up to the next 10. Wrecks count against "without wrecking" goals.

Driving through smashable objects counts toward smashing achievements. On
Dragonmaw Chasm, Dragon Eggs are a separate target for
[Dragonscourge](./quests/1181.md) and Terror of Dragonmaw Chasm. No data source
used here shows a way to smash other players' cars on purpose.

## Rewards

After the race you click the reward button to get coins and a loot roll. Both
depend on how many racers took part and where you finished. On Vertigo Loop
(the starter track) the fixed coin amounts are lower:

| Racers | 1st | 2nd | 3rd | 4th | 5th | 6th |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | 250 (200) | 190 (152) | | | | |
| 3 | 590 (472) | 510 (408) | 350 (280) | | | |
| 4–6 | 710 (568) | 560 (448) | 450 (360) | 400 (320) | 350 (280) | 250 (200) |

Values are coins for Keelhaul Canyon, Dragonmaw Chasm and Space Blizzard, with
Vertigo Loop in parentheses. The loot roll can include car modules, racing
helmets and faction token items. Its odds are a per-roll model, not a promise
that any item will drop; see each track page for the reward tables.

## Racing missions and achievements

Racing missions are given by three NPCs:

- **Velocity Lane - Racing Trainer**, Nimbus Station Race Place: the starter
  chain above, then [Vertigo Loop Top 3](./quests/626.md),
  [Max Velocity](./quests/627.md) (beat a 1:10 lap) and
  [Vertigo Loop Victory](./quests/628.md). Later she also gives
  [Race Series 1](./quests/668.md): "Win 1 race each at the Vertigo Loop and
  Keelhaul Canyon racetracks." Its reward is a Very Large Bag of Faction Tokens.
- **Swifty McGurk - Racing Pirate**, Gnarled Forest Race Place
  ([Find Swifty McGurk](./quests/629.md)): Keelhaul Canyon Top 3,
  Swifty's Best Lap (1:40), Swifty's Best Time (5:00 total), No Wreckin' and
  Keelhaul Canyon Victory.
- **Zip Lash - Racing Ninja**, Forbidden Valley Race Place:
  [Quick as a Lash](./quests/1161.md) (1:27 lap),
  [Dragonscourge](./quests/1181.md) (smash 10 Dragon Eggs),
  [Faster! Faster!](./quests/1160.md) (4:05 total),
  [Nerves of Steel](./quests/1165.md) (no wrecks),
  [Dragonmaw Top 3](./quests/1163.md) and
  [Dragonmaw Chasm Victory](./quests/1162.md).

Racing achievements include per-track goals: Winners' Circle, Champion, Super
Champ (10 wins), Pacesetter, Speed Demon, Safe Driver, Flag Racer and
Racemaster. Vertigo Loop Pacesetter, for example, asks for a 1:05 lap, and
Vertigo Loop Speed Demon for a 3:10 total. There are also career series:
Low Deductible (races without wrecking), Street Sweeper (smashables),
Drive-Thru Dreamer (Imagination power-ups), Racing Fanatic (races entered),
Five-/Ten-/Twenty-/Fifty-Time Champion, Try, Try Again (10 last-place
finishes), Complete Overhaul ("Swap out every module while building a car.")
and Go Outside and Play (complete racing achievements).

**Placement and win goals need at least 3 racers.** Many client texts say
"(at least 3 players in the race)". On DarkflameServer, no placement, win or
last-place goal counts in a two-player race unless solo racing is enabled.
Finishing, lap and total times, no-wreck runs, smashables and Imagination
pickups count in any race.

The [racing mission index](./racing/Racing%20Quests%20and%20Achievements.md)
links every racing quest and achievement page.

## If a race is unavailable

The track may be disabled, seasonal, or missing from the server version you
are playing. A race also needs at least one other player unless the server
allows solo racing. If you need help, tell staff the track name, the world,
what you interacted with, and what the game did instead.

## Source and limitations

This guide was checked against the local client database (`CDServer.sqlite`:
ZoneTable, Activities, ActivityRewards, CurrencyTable, Missions, MissionTasks,
Objects, ItemComponent, VendorComponent, LootMatrix/LootTable and the boost
skill's behavior parameters), the English client strings (`locale.xml`), and
the DarkflameServer source. The source used covers the track scripts,
RacingControlComponent, the racing object scripts and the reward/loot code.
Lobby timing, the wreck-respawn Imagination rule, reward-button handling and
the 3-racer rule for placement goals describe DarkflameServer behavior, which
may differ from the original live servers. Entrance locations come from
mission texts and the generated track pages. Driving routes, shortcuts and
hazards are not covered here; the [Racing Database](./racing/README.md) marks
those as historical community descriptions.
