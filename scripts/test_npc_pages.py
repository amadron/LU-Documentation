import csv
import tempfile
import unittest
from pathlib import Path

import build_npc_pages as pages


class NpcPageTests(unittest.TestCase):
    def create_root(self, root):
        (root / "scripts").mkdir(parents=True)
        with (root / "LEGO Universe NPC List.csv").open(
            "w", encoding="utf-8", newline=""
        ) as file:
            writer = csv.DictWriter(file, fieldnames=(
                "LOT", "Name", "DisplayName", "InternalName", "NameSource",
                "ObjectType", "Classification", "NPCComponentMarkers",
                "CombatAIComponentID", "CombatBehaviorType", "AggroRadius",
                "MissionIDs", "MissionsOffered",
            ))
            writer.writeheader()
            writer.writerows((
                {
                    "LOT": "14381",
                    "Name": "Maelstrom Spider Queen",
                    "DisplayName": "Maelstrom Spider Queen",
                    "InternalName": "AG - Spider Queen",
                    "NameSource": "displayName",
                    "ObjectType": "Enemies",
                    "Classification": "Enemy, Combat AI",
                    "NPCComponentMarkers": "BASE_COMBAT_AI",
                    "CombatAIComponentID": "159",
                    "CombatBehaviorType": "3",
                    "AggroRadius": "1000",
                    "MissionIDs": "",
                    "MissionsOffered": "",
                },
                {
                    "LOT": "4009",
                    "Name": "Bob",
                    "DisplayName": "",
                    "InternalName": "Bob",
                    "NameSource": "name",
                    "ObjectType": "NPC",
                    "Classification": "NPC, Mission offer/accept",
                    "NPCComponentMarkers": "MISSION_NPC",
                    "CombatAIComponentID": "",
                    "CombatBehaviorType": "",
                    "AggroRadius": "",
                    "MissionIDs": "173",
                    "MissionsOffered": "Your Creative Spark",
                },
                {
                    "LOT": "5000",
                    "Name": "A vehicle",
                    "DisplayName": "",
                    "InternalName": "Vehicle",
                    "NameSource": "name",
                    "ObjectType": "Vehicle",
                    "Classification": "",
                    "NPCComponentMarkers": "",
                    "CombatAIComponentID": "",
                    "CombatBehaviorType": "",
                    "AggroRadius": "",
                    "MissionIDs": "",
                    "MissionsOffered": "",
                },
            ))
        with (root / "scripts" / "location_map_world_markers.csv").open(
            "w", encoding="utf-8", newline=""
        ) as file:
            writer = csv.DictWriter(file, fieldnames=(
                "zone", "category", "name", "lot", "x", "y", "z", "details", "path",
            ))
            writer.writeheader()
            writer.writerow({
                "zone": "1102",
                "category": "enemies",
                "name": "Maelstrom Spider Queen",
                "lot": "14381",
                "x": "-12.6",
                "y": "432.8",
                "z": "-68.2",
                "details": "Spawner: SpiderBoss; maximum 1",
                "path": "",
            })

    def test_builds_actor_pages_and_type_indexes_from_catalog_and_markers(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.create_root(root)

            stats = pages.build(root)
            spider = (root / "wiki" / "npcs" / "14381.md").read_text(encoding="utf-8")
            bob = (root / "wiki" / "npcs" / "4009.md").read_text(encoding="utf-8")
            index = (root / "wiki" / "npcs" / "indexes" / "enemies-1.md").read_text(encoding="utf-8")
            readme = (root / "wiki" / "npcs" / "README.md").read_text(encoding="utf-8")

            self.assertEqual(stats["actors"], 2)
            self.assertEqual(stats["mapped_actors"], 1)
            self.assertIn("**Catalog type:** Enemy", spider)
            self.assertIn("Combat behavior type | 3", spider)
            self.assertIn("[Zone 1102](../zones/1102/)", spider)
            self.assertIn("Spawner: SpiderBoss; maximum 1", spider)
            self.assertIn("No coordinate-based placement", bob)
            self.assertIn("[Maelstrom Spider Queen (LOT 14381)](../14381.md)", index)
            self.assertIn("2 NPC, enemy, and user-created NPC templates", readme)
            self.assertFalse((root / "wiki" / "npcs" / "5000.md").exists())

    def test_build_is_idempotent(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.create_root(root)

            pages.build(root)
            stats = pages.build(root)

            self.assertEqual(stats["updated_pages"], 0)

    def test_rejects_duplicate_actor_lots(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.create_root(root)
            catalog = root / "LEGO Universe NPC List.csv"
            original = catalog.read_text(encoding="utf-8")
            with catalog.open("a", encoding="utf-8", newline="") as file:
                file.write(original.splitlines()[1] + "\n")

            with self.assertRaisesRegex(ValueError, "duplicate actor LOT"):
                pages.build(root)


if __name__ == "__main__":
    unittest.main()
