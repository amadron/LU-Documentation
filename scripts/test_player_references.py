import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import build_player_references as refs
import enrich_skills


class PlayerReferenceTests(unittest.TestCase):
    TABLES = {
        "Objects": [
            {"id": "10", "name": "Dagger", "displayName": ""},
            {"id": "11", "name": "Test Helm", "displayName": "Helm"},
            {"id": "12", "name": "NPC", "displayName": ""},
            {"id": "13", "name": "GM Only - Hammer", "displayName": ""},
            {"id": "14", "name": "Hat", "displayName": ""},
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
            {"id": "14", "component_type": "11", "component_id": "2"},
        ],
        "ObjectSkills": [
            {"objectTemplate": "10", "skillID": "148", "castOnType": "0"},
            {"objectTemplate": "10", "skillID": "149", "castOnType": "1"},
            {"objectTemplate": "11", "skillID": "150", "castOnType": "0"},
            {"objectTemplate": "12", "skillID": "151", "castOnType": "0"},
            {"objectTemplate": "13", "skillID": "152", "castOnType": "0"},
            {"objectTemplate": "14", "skillID": "153", "castOnType": "0"},
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
    EVIDENCE = {
        "sources": {"example": {"label": "Example", "url": "https://example.com"}},
        "names": [{"id": "148", "name": "Sword Move", "item": "10",
                   "community_item": "Dagger", "source": "example"},
                  {"id": "153", "name": "Hat Trick", "item": "14",
                   "community_item": "Hat", "source": "example"}],
    }
    LOCALE = {"148": {"name": "Slash_Attack", "description": "%(DamageCombo) 1+2+3 %(ChargeUp)Spins | hits"}}

    def build(self, root, locale):
        items = root / "wiki" / "items"
        items.mkdir(parents=True, exist_ok=True)
        for lot in ("10", "11", "13", "14"):
            (items / f"{lot}.md").touch()
        return refs.build_skills(root, self.TABLES, self.EVIDENCE, locale)

    def test_selects_equipment_and_set_skills_without_npc_or_test_items(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.assertEqual(self.build(root, self.LOCALE), 3)
            skills = root / "wiki" / "skills"
            equipment = (skills / "148.md").read_text(encoding="utf-8")
            self.assertIn("[Dagger (LOT 10)](../items/10.md)", equipment)
            self.assertIn("slot `special_r`", equipment)
            self.assertTrue(equipment.startswith("# Slash&#95;Attack\n"))
            self.assertIn("**Skill ID:** 148", equipment)
            self.assertIn("## Description\n\nDamage: 1+2+3. Charge attack: Spins &#124; hits.\n", equipment)
            self.assertIn("**Historical community name:** Sword Move. [Example](https://example.com)", equipment)
            self.assertNotIn("Community name candidate", equipment)
            candidate = (skills / "153.md").read_text(encoding="utf-8")
            self.assertTrue(candidate.startswith("# Hat Trick\n"))
            self.assertIn("not a verified localized client name", candidate)
            index = (skills / "README.md").read_text(encoding="utf-8")
            self.assertIn("| Skill ID | Name | Equipment examples | Set associations |", index)
            self.assertIn("| [148](./148.md) | [Slash&#95;Attack](./148.md) |", index)
            self.assertIn("| [153](./153.md) | [Hat Trick](./153.md) (community candidate) |", index)
            self.assertIn("Official client names and tooltips: **1 of 3 skills**. Unnamed: **1**.", index)
            unnamed = (skills / "200.md").read_text(encoding="utf-8")
            self.assertTrue(unnamed.startswith("# Skill 200\n"))
            self.assertIn("No matching SkillBehavior", unnamed)
            self.assertIn("| [200](./200.md) | Name unknown |", index)
            self.assertIn("Set 1, 3 equipped pieces", unnamed)
            self.assertFalse((skills / "150.md").exists())
            self.assertFalse((skills / "152.md").exists())

    def test_matching_community_name_is_not_repeated(self):
        locale = {"148": {"name": "sword move", "description": "Cuts"}}
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.build(root, locale)
            page = (root / "wiki" / "skills" / "148.md").read_text(encoding="utf-8")
            self.assertTrue(page.startswith("# sword move\n"))
            self.assertNotIn("community name", page.lower())

    def test_enrich_matches_full_regeneration_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as old, tempfile.TemporaryDirectory() as new:
            self.build(Path(old), None)
            self.build(Path(new), self.LOCALE)
            skills = Path(old) / "wiki" / "skills"
            pages = sorted(skills.glob("[0-9]*.md"))
            names = {c["id"]: c for c in self.EVIDENCE["names"]}
            for _ in range(2):
                for page in pages:
                    enrich_skills.enrich_page(page, self.LOCALE, self.EVIDENCE, names)
                enrich_skills.enrich_index(skills / "README.md", {p.stem: {} for p in pages}, self.LOCALE, names)
            for page in pages + [skills / "README.md"]:
                expected = Path(new) / "wiki" / "skills" / page.name
                self.assertEqual(page.read_bytes(), expected.read_bytes(), page.name)

    def test_tooltip_rendering_and_line_start_escaping(self):
        self.assertEqual(
            refs.render_tooltip("%(DamageCombo) 1+2+2 %(AltCombo) 6+7+8 %(ChargeUp)Whirls - release"),
            "Damage: 1+2+2. Damage vs. Skeletons: 6+7+8. Charge attack: Whirls - release.")
        self.assertEqual(refs.render_tooltip(" %(ChargeUp)Restores 10"), "Charge attack: Restores 10.")
        self.assertEqual(refs.render_tooltip("%(DamageCombo) 4 %(Description) Throws 3 Kunai"),
                         "Damage: 4. Throws 3 Kunai.")
        self.assertEqual(refs.render_tooltip("Stuns enemies"), "Stuns enemies.")
        self.assertEqual(refs.escape_block("+1 AP."), "+1 AP.")
        self.assertEqual(refs.escape_block("- note"), "&#45; note")
        self.assertEqual(refs.escape_block("1. step"), "&#49;. step")

    def test_loads_english_skill_names_from_locale(self):
        xml = ('<?xml version="1.0" encoding="UTF-8" ?><localization><phrases>'
               '<phrase id="SkillBehavior_338_name"><translation locale="en_US">Roundhouse</translation>'
               '<translation locale="de_DE">Rundschlag</translation></phrase>'
               '<phrase id="SkillBehavior_338_descriptionUI">'
               '<translation locale="en_US">%(DamageCombo) 10</translation></phrase>'
               '<phrase id="SkillBehavior_9_name"><translation locale="de_DE">Nur Deutsch</translation></phrase>'
               '<phrase id="Other_1_name"><translation locale="en_US">Ignored</translation></phrase>'
               '</phrases></localization>')
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "locale.xml"
            path.write_text(xml, encoding="utf-8")
            locale = refs.load_skill_locale(path)
        self.assertEqual(locale, {"338": {"name": "Roundhouse", "description": "%(DamageCombo) 10"}})
        self.assertEqual(refs.official_skill(locale, "338"), ("Roundhouse", "Damage: 10."))
        self.assertEqual(refs.official_skill(locale, "9"), ("", ""))

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
