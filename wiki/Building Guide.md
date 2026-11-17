# Building and Properties Guide

[Game Guide](./README.md) | [Getting Started](./Getting%20Started.md) | [Worlds](./Worlds%20Guide.md) | [Items](./Item%20Guide.md)

Building takes several forms: a **Quick Build** assembles an object on the
spot, a **Modular Build** combines parts into a Custom Rocket or Custom Racing
Car, and a **Property** is your own world to fill with models, bricks, and
behaviors. Follow your client's prompts; the availability and behavior of each
feature depend on the server.

## The Thinking Hat

You need the [Thinking Hat](./items/6086.md) for Modular Builds and for
building on a Property. Sky Lane - Venture League Explorer gives it to you as
the reward for [Not Enough Lifepods?](./quests/308.md) on the Venture
Explorer, where you collect a Nose Cone, a Cockpit, and an Engine for your
escape rocket. The client's own hint reads: "Your Thinking Hat will only work
in Modular Build and Property areas." The server will not start Property
building if the hat is missing from your inventory, and the hat cannot be
moved to your vault.

## Quick Builds

Quick Builds are piles of bricks you interact with to assemble on the spot,
for example turrets, bridges, and Maelstrom Generators on Properties. Building
drains your **Imagination** a point at a time; most Quick Builds in the client
data cost 1 to 4 Imagination, and a few cost much more. If you run out before
the build is finished, it is cancelled. Some Quick Builds fall apart again
after a while if left unfinished or once their time is up.

## Rockets and cars (Modular Build)

A Modular Build station lets you snap parts into slots while wearing the
Thinking Hat. The result goes to the **Models** tab of your Backpack:

- **[Custom Rocket](./items/6416.md)**: nose cone, cockpit, and engine. You
  build your first one on the Venture Explorer and use it at launch pads to
  travel between worlds.
- **[Custom Racing Car](./items/8092.md)**: chassis plus modules such as
  wheels, bumpers, and panels, built at Car Build in the racing areas. See the
  [Racing Guide](./Racing%20Guide.md).

Swapping in different parts changes the look of the vehicle.

## Property worlds

Mission 320's description puts it simply: "Large launch pads lead to new
worlds. Small ones lead to Property Worlds." Each property world is a
separate private copy for each player. The client data defines six:

| Property | Reached from | Property Guard | Clearing mission |
| --- | --- | --- | --- |
| [Block Yard](./zones/1150.md) | Avant Gardens | Vance Bulwark | [Arachnophobia](./quests/768.md) (smash the Spider Queen) |
| [Avant Grove](./zones/1151.md) | Avant Gardens | Argo Butterchunks | [Clear Avant Grove!](./quests/1293.md) |
| [Nimbus Rock](./zones/1250.md) | Nimbus Station | Kendrix Starfish | [Clear Nimbus Rock!](./quests/872.md) |
| [Nimbus Isle](./zones/1251.md) | Nimbus Station | Bud Nippit | [Clear Nimbus Isle!](./quests/1322.md) |
| [Chantey Shanty](./zones/1350.md) | Gnarled Forest | Sunny Rayhawk | [Clear Chantey Shanty!](./quests/873.md) |
| [Raven Bluff](./zones/1450.md) | Forbidden Valley | Knuck Brassels | [Clear Raven Bluff!](./quests/874.md) |

An unclaimed property starts infested with the Maelstrom. Talk to its Property
Guard, then smash and build your way to the Imagination Orb (on Avant Grove,
for example, by smashing and rebuilding the Maelstrom Generator). Clearing a
property unlocks more behaviors, and afterwards you can claim it at its
**Property Console**. Avant Grove's clearing mission requires Check In with
Sky Lane first.

## Claim Block Yard: the tutorial chain

Block Yard is the first property and the one with a full tutorial. Vance
Bulwark - Property Guard gives each step:

1. [Back-up Bulwark!](./quests/377.md) (from Crash Helmut - Property Launch
   Pad Guard in Avant Gardens): fly to Block Yard and find Vance. Reward:
   Trial Venture League Gear.
2. [One Size Fits All](./quests/1950.md): equip the Trial Faction Gear.
3. [Arachnophobia](./quests/768.md): smash the Spider Queen on Block Yard.
4. [Stake a Claim](./quests/870.md): interact with the Property Console to
   claim the property.
5. [Model Mania](./quests/871.md): find the Models tab in your Backpack and
   place 4 models.
6. [Model Movers](./quests/891.md): pick up, rotate, and put away a model.
7. [Check In with Sky Lane](./quests/320.md): report back to Sky Lane at the
   Avant Gardens launch area.

The client's guide text sums it up: "All you need is a Thinking Hat, bricks,
models and Imagination!"

## Place and build

- Walk into the build area and put on your Thinking Hat to enter Build Mode.
  Click the check mark in the upper right to leave it.
- Open the **Models** tab of your Backpack, pick a model, place it, and
  rotate it as needed. You can pick placed models up again or put them back
  in your Backpack.
- Brick building lets you assemble your own models from loose bricks. On
  this server the bricks are not removed from your inventory when you save a
  creation. Breaking a brick-built model back into its bricks is not
  supported; the server only removes the model.
- While you are building, your property is set to private and other players
  on it are sent back to the launch pad's world. Your models are reset and
  paused until you finish.

Models, bricks, and other building items have different roles. If something
cannot be placed, check its type and whether you are inside your property's
build area. See the [Item Guide](./Item%20Guide.md) for inventory checks.

## Behaviors

Click a placed model in Build Mode to enter **Behavior Mode**. A behavior is
a chain of blocks: a trigger such as On Interact, On Attack, On Chat, On
Timer, or on startup, followed by actions such as moving, flying, spinning,
tilting, waiting, playing a sound, chatting, smashing, or dropping health,
armor, or Imagination. Start with one simple chain, test it, then add more.
The server's behavior system is still being completed; some actions may not
play, and the running state of a behavior is not saved.

## Property Console, visitors, and Reputation

"Use the Property Console to name your Property, write a description, allow
visitors, and view your Property's Reputation." Making a property public
sends it for moderator approval, and finishing a building session resets that
approval. Other players can visit public properties through the property
launch pads, and visits progress missions such as Avant Gardens Property
Visitor ("Visit 5 Block Yard or Avant Grove Properties today").

Building-related achievements in the client data include:

- **Model Mover** series: place 25, 75, 150, then 250 models.
- **Ain't Misbehavin'** series: add 5, 25, 50, then 75 behaviors.
- **The Visitor** series: visit 25, 75, 150, 250, then 500 properties.
- **Reputation** series: earn 100, 1,000, 10,000, 100,000, then 1,000,000
  Reputation.

## Property rules in the client data

- Build height limit: 128 on most properties, 256 on Avant Grove.
- Claim price listed in the client: Block Yard free; Nimbus Rock, Chantey
  Shanty, and Raven Bluff 500; Avant Grove and Nimbus Isle 1,000. Several
  guard missions mention a monthly fee. This is historical: the server's
  claim code does not deduct coins.
- You can only claim the copy of the property that is yours.

## If something does not work

Check that the property is cleared and claimed, the correct mission is
active, your Thinking Hat is in your inventory, and the object is a placeable
model. If access, saving, or behavior editing still fails, report the
property name, the step attempted, and any message to the server's staff.

## Source and limitations

Names, missions, NPCs, achievements, and property values come from the client
database (`PropertyTemplate`, `ZoneTable`, `Missions`, `MissionTasks`,
`Objects`, `RebuildComponent`, `ModularBuildComponent`) and the English
client strings in `locale.xml`. Server behavior (Thinking Hat check, claiming,
building sessions, moderation, behaviors, brick handling, Quick Build
Imagination drain) comes from the DarkflameServer source. The general building
concepts were first summarized from the *LEGO Universe Official Game Guide*
(2010), pp. 12 and 165–169. The "Reached from" column is inferred from each
mission's world and guard; launch-pad requirements for the other properties
are not verified here, and server support should be tested in game.
