import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import build_player_references as refs


class PlayerReferenceTests(unittest.TestCase):
    def test_selects_equipment_and_set_skills_without_npc_or_test_items(self):
        tables = {
            "Objects": [
                {"id": "10", "name": "Dagger", "displayName": ""},
                {"id": "11", "name": "Test Helm", "displayName": "Helm"},
                {"id": "12", "name": "NPC", "displayName": ""},
                {"id": "13", "name": "GM Only - Hammer", "displayName": ""},
            ],
            "ItemComponent": [
                {"id": "1", "equipLocation": "special_r"},
                {"id": "2", "equipLocation": "hair"},
            ],
            "ComponentsRegistry": [
                {"id": "10", "component_type": "11", "component_id": "1"},
                {"id": "11", "component_type": "11", "component_id": "2"},
                {"id": "12", "component_type": "9", "component_id": "1"},
                {"id": "13", "component_type": "11", "component_id": "1"},
            ],
            "ObjectSkills": [
                {"objectTemplate": "10", "skillID": "148", "castOnType": "0"},
                {"objectTemplate": "10", "skillID": "149", "castOnType": "1"},
                {"objectTemplate": "11", "skillID": "150", "castOnType": "0"},
                {"objectTemplate": "12", "skillID": "151", "castOnType": "0"},
                {"objectTemplate": "13", "skillID": "152", "castOnType": "0"},
            ],
            "ItemSetSkills": [{"SkillSetID": "3", "SkillID": "200"}],
            "ItemSets": [
                {"setID": "1", "itemIDs": "10", "skillSetWith2": "",
                 "skillSetWith3": "3", "skillSetWith4": "", "skillSetWith5": "",
                 "skillSetWith6": ""},
                {"setID": "2", "itemIDs": "11", "skillSetWith2": "3",
                 "skillSetWith3": "", "skillSetWith4": "", "skillSetWith5": "",
                 "skillSetWith6": ""},
            ],
            "SkillBehavior": [
                {"skillID": "148", "imaginationcost": "2", "cooldown": "0.5"},
            ],
        }
        evidence = {
            "sources": {"example": {"label": "Example", "url": "https://example.com"}},
            "names": [{"id": "148", "name": "Sword Move", "item": "10",
                       "community_item": "Dagger", "source": "example"}],
        }
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            items = root / "wiki" / "items"
            items.mkdir(parents=True)
            (items / "10.md").touch()
            (items / "11.md").touch()
            (items / "13.md").touch()
            self.assertEqual(refs.build_skills(root, tables, evidence), 2)
            equipment = (root / "wiki" / "skills" / "148.md").read_text(encoding="utf-8")
            self.assertIn("[Dagger (LOT 10)](../items/10.md)", equipment)
            self.assertIn("slot `special_r`", equipment)
            self.assertIn("# Sword Move — skill 148", equipment)
            self.assertIn("not a verified localized client name", equipment)
            self.assertIn("Sword Move — skill 148 (candidate)", (root / "wiki" / "skills" / "README.md").read_text(encoding="utf-8"))
            self.assertIn("No matching SkillBehavior", (root / "wiki" / "skills" / "200.md").read_text(encoding="utf-8"))
            self.assertIn("name unknown", (root / "wiki" / "skills" / "README.md").read_text(encoding="utf-8"))
            self.assertIn("Set 1, 3 equipped pieces", (root / "wiki" / "skills" / "200.md").read_text(encoding="utf-8"))
            self.assertFalse((root / "wiki" / "skills" / "150.md").exists())
            self.assertFalse((root / "wiki" / "skills" / "152.md").exists())

    def test_name_evidence_requires_a_matching_item(self):
        evidence = {
            "sources": {"example": {"label": "Example", "url": "https://example.com"}},
            "names": [{"id": "148", "name": "Sword Move", "item": "99",
                       "community_item": "Dagger", "source": "example"}],
        }
        with self.assertRaisesRegex(ValueError, "not associated"):
            refs.validate_skill_names(evidence, {"148": {"items": {"10"}}})

    def test_zone_links_only_existing_evidence_and_distinguishes_unmatched_zone(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            tracks = root / "wiki" / "racing" / "tracks"
            tracks.mkdir(parents=True)
            (tracks / "space-blizzard.md").touch()
            locations = root / "wiki" / "quests" / "locations"
            locations.mkdir(parents=True)
            (locations / "zone-1100.md").touch()
            with patch.object(refs, "ZONES", ((1100, "Avant Gardens", "World"), (1261, "Space Blizzard", "Seasonal racetrack"))):
                refs.build_zones(root, {"ZoneTable": [{"zoneID": "1100"}]})
            world = (root / "wiki" / "zones" / "1100.md").read_text(encoding="utf-8")
            seasonal = (root / "wiki" / "zones" / "1261.md").read_text(encoding="utf-8")
            self.assertIn("../quests/locations/zone-1100.md", world)
            self.assertNotIn("../pets/locations/zone-1100.md", world)
            self.assertIn("No ZoneTable row", seasonal)
            self.assertIn("../racing/tracks/space-blizzard.md", seasonal)

    def test_stale_generated_pages_are_reported(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp)
            (output / "10.md").touch()
            with self.assertRaisesRegex(RuntimeError, "10"):
                refs.check_stale_pages(output, {"11"})


if __name__ == "__main__":
    unittest.main()
