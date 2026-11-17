# Item Guide

[Game Guide](./README.md) | [Quest Guide](./Quest%20Guide.md) | [Racing Guide](./Racing%20Guide.md) | [Pet Guide](./Pet%20Guide.md)

Use this guide when you want to find an item, decide whether to equip it, or
work out where it might come from. For a particular item, start with the
[item database](./items/README.md). If you only need a quick name or number
search, open the [item summary CSV](./items/Item%20Summary.csv) in a
spreadsheet and use its search.

## Find an item

1. Search the [item summary CSV](./items/Item%20Summary.csv) by name, or browse the [item database](./items/README.md) by item type.
2. Open the item's page and check its description and possible sources.
3. Follow a source link for any extra location or requirement details.
4. Confirm the item and its conditions in game before spending time or currency.

If you already have the item's **LOT** (its template number), open the page
with that number in the item database, for example
[Healing Banana (LOT 1966)](./items/1966.md). Different copies of one item
share a LOT, even if they have different quantities or binding states.

## What kind of item is it?

Every item has a type in the client database. The type decides which slot it
uses and which part of your inventory it goes to. The type names below are the
database names; several of them do not mean what they seem to.

| Type in the database | What it is in plain English | Example | Stored in |
|---|---|---|---|
| Hat | Headgear | Knight Helm 1 | Backpack |
| Hair | Hairpieces | — | Backpack |
| Neck | Items worn around the neck or on the shoulders | Black Neck Scarf, Blue Shoulder Parrot | Backpack |
| Chest | **Shirts and torso armor**, not treasure chests | Monument Shirt, Knight Breastplate 1 | Backpack |
| Legs | Trousers and leg armor | Knight Leggings 1 | Backpack |
| Right hand | Weapons and tools | Knight Greatsword 1 | Backpack |
| Left hand | Shields and other off-hand items | Buckler Shield | Backpack |
| Consumable | Food, drinks, and other usable items | Healing Banana, Hot Chocolate | Backpack |
| Package | Bags and packs that you open for items | Brick Booster Pack | Backpack |
| Collectible, Egg, Pet food | Special items with a single use or role | Candy Cane | Backpack |
| Quest object | Items that a mission needs | — | Separate mission-item inventory |
| Brick | Loose LEGO bricks for building | — | Bricks inventory |
| Loot model | Mostly rocket and race-car parts | Classic Rocket Nose Cone | Models bag |
| Model, Vehicle, Mount, Pet inventory item | Built models, rockets, cars, and pets | Custom Rocket, Custom Racing Car | Models bag |
| Behavior | Behaviors for property models | — | Behaviors inventory |
| Property | Property deeds | — | Property inventory |

The client names your main inventory the **Backpack** and the model inventory
the **Models bag**. Some database entries are test or NPC items, so a type
listing does not prove that every entry can be obtained.

## Rarity

Each item has a rarity value. Most player items use values 1 to 4, where a
higher number is rarer. For example, Healing Banana is rarity 1, Monument Shirt
is rarity 2, and Knight Helm 1 is rarity 4. A small group of entries uses 5,
but these are mostly test, NPC, or other special objects.

Rarity is a loot-roll value, not a quality score. Compare an item's skills and
effects rather than only its rarity.

## Faction gear

Faction class gear, such as Knight Helm 1, is bought from faction vendors with
coins plus faction tokens: Assembly Token, Sentinel Faction Token, Paradox
Token, or Venture League Token. Knight Helm 1, for example, costs 1,500 coins
and 25 Sentinel Faction Tokens. All gear priced in faction tokens binds when
you pick it up. Wearing
several pieces of one rank gives set bonuses. See
[Faction Classes](./classes/README.md) for each class's gear, vendors, and set
bonuses, and the [Faction Guide](./Faction%20Guide.md) for joining a faction.

## Work out where it comes from

The item page may point to a mission reward, a vendor, an enemy or object, a
package, or a race. Treat these as leads, then check the matching source in
game:

- **Mission reward:** read the reward choices before finishing the mission.
  First-time and repeat rewards may differ.
- **Vendor:** check the current stock, price, currency, and requirements.
- **Enemy or object:** a possible drop is not a promise that every attempt will
  give the item.
- **Package or activity:** read its description and check the activity's own
  rules; a listed reward can depend on how the activity ends.

### How loot drops work on this server

Based on the DarkflameServer code:

- An enemy or object has a loot matrix. Each row of that matrix rolls a chance
  to drop. If the chance succeeds, the server rolls a rarity and picks an item
  of that rarity from the row's loot table. If no item of that rarity is
  available, it picks a less rare item.
- **Mission items** drop only when you, or a team member, have an active
  mission that needs them.
- **Faction tokens** drop as the token of your own faction. In a team, each
  member gets their own token. If you have not joined a faction, you get no
  token.
- **Coins** are split between team members, with the share rounded up.
- **Other items** in a team go to the next team member in turn who is close
  enough. If your team uses free-for-all loot, whoever picks the item up
  first gets it.
- **Power-ups** can be picked up by every team member.

The [item database](./items/README.md) includes modeled chances where the
source data supports them. Those figures are not a guaranteed chance per
enemy defeated or race completed, and server settings can change results.
See its [methodology](./items/Methodology.md) for how to interpret the
estimates and location evidence.

## Currencies

| Currency | What it is used for |
|---|---|
| Coins | The main currency. Vendors charge the item's coin price. |
| Faction tokens | Assembly Token, Sentinel Faction Token, Paradox Token, and Venture League Token. Used for faction gear, together with coins. |
| Candy Cane | Event currency, for example for Jingle Blazer car parts (40 Candy Canes each). |
| Ingredients | A few food items are made from ingredients instead of only coins. For example, Dirt Sandwich costs 2 Rock Fruit and 4 Hardtack Biscuit plus coins. |
| Green Imaginite | Not a vendor currency in the client data. A Nexus Tower combat challenge script uses one Green Imaginite to start. Blue and Red Imaginite exist in the data with only short descriptions; this guide does not confirm a use for them. |

Tokens and similar currency items stack up to 999 in one inventory slot.

## Inventory and Vault space

| Inventory | Starting slots on this server |
|---|---|
| Backpack | 20 |
| Vault (items) | 40 |
| Vault (models) | 40 |
| Bricks, Models bag | 240 each |

Some missions and achievements add Backpack slots, most often 4 at a time. The
Backpack and Vault do not grow by themselves. Other inventories, such as
bricks and mission items, expand automatically when they get close to full.
To move an item into or out of the Vault, you must stand near a Vault
interface.

**Stacking:** the stack size depends on the item. Many consumables stack to
10 (for example Healing Banana and Hot Chocolate). Gear normally does not
stack. Tokens and Candy Canes stack to 999.

## Using consumables and packages

- **Consumables:** using one removes one from the stack, if the item has a
  consumable effect.
- **Packages:** opening one gives you its contents only if everything fits in
  your inventory. If anything does not fit, nothing happens and you keep the
  package. Free some slots and try again.
- **Mounts and pets:** some zones do not allow them.

## Before equipping or trading

1. Read the item's in-game requirements, such as level or faction. If you do not
   meet them, the item will not equip.
2. Compare its actual skills and effects, not only its name or rarity.
3. Check the binding warning. The client calls binding "linking": *"Once an
   item is linked to you it cannot be Traded."*
4. Keep quest-related items until the objective and turn-in are complete.

There are two binding rules in the data:

- **Bind on pickup:** the item is linked to you as soon as you get it. Most
  faction class gear works like this.
- **Bind on equip:** the item can be traded until you equip it for the first
  time. When you buy such an item, the client asks: *"This item will be linked
  to you. Are you sure you want to purchase it?"*

If an item will not equip or trade, check its type, requirements, and the
binding state of that particular copy. Rocket parts, race-car parts, and
vehicles cannot be equipped like gear. They are used at launch pads, building
areas, or race car stations.

## Selling and buy-back

- At most vendors you get **10% of the item's coin price** when you sell it.
  For an item bought with tokens, you also get back a small share of the
  tokens.
- Items with no coin price cannot be sold.
- Sold items go to the vendor's buy-back list. You can buy an item back for
  the same amount you got for it.

## If something seems wrong

| Problem | First thing to check |
|---|---|
| A mission reward is missing | Was the mission fully turned in, and was a reward choice required? |
| You cannot pick something up | Is your Backpack full? The client says: *"You must make room in your Inventory to pick up more items."* |
| You cannot find an item | Check the Backpack, Models bag, and Vault, and whether it was used, sold, or consumed by a mission. |
| A package will not open | Free some inventory slots; a package opens only if all its contents fit. |
| A vendor's price differs from the list | Trust the current in-game price; a catalog value is only a data reference. |
| An item cannot be equipped or traded | Check requirements, item type, and binding state. |
| A listed item seems unavailable | The entry may be unused, a test item, or disabled on this server. A database entry does not prove availability. |

When asking staff for help, include the item name and LOT if known, quantity,
where you expected to get it, what happened, and roughly when. A screenshot
can help distinguish similarly named items.

## More detailed references

- [Full item database](./items/README.md), including [source locations](./items/locations/README.md)
- [Faction Classes](./classes/README.md) for class gear and set bonuses
- [Quest and achievement database](./quests/README.md)
- [Pet Guide](./Pet%20Guide.md) and [Pet Database](./pets/README.md)
- [Racing Guide](./Racing%20Guide.md) and [Racing Database](./racing/README.md)

The item database includes technical fields for readers who want the source
data. Those fields are optional for ordinary gameplay.

## Source and limitations

This guide is based on:

- the client database (`ItemComponent`, `Objects`, `VendorComponent`,
  `LootMatrix`, `LootTable`, `RarityTable`, and `Missions` tables) for item
  types, rarity, binding flags, stack sizes, prices, currencies, and the
  missions that add Backpack space;
- the English client strings (`locale.xml`) for UI names such as Backpack,
  Models bag, Vault, and the linking messages;
- the DarkflameServer source code for inventory sizes, loot drops, selling,
  buy-back, packages, and consumables.

Starting inventory sizes, the loot rules, and the sell percentage describe
this server's code. They may not match the original live game exactly, and
server operators can change them. Prices and stock shown in game always take
priority over this guide.
