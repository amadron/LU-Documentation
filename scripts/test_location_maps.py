import json
import tempfile
import unittest
from pathlib import Path

import build_location_maps as maps


class LocationMapTests(unittest.TestCase):
    def create_root(self, root, zone=1100):
        (root / "assets" / "minimaps").mkdir(parents=True)
        (root / "assets" / "minimaps" / f"{zone}.webp").touch()
        item_sources = root / "wiki" / "items" / "sources"
        item_sources.mkdir(parents=True)
        (item_sources / "object-4990.md").write_text(
            "# Fan Smashable — source LOT 4990\n\n"
            "## Mapped placements and spawner waypoints\n\n"
            "| Zone | X | Y | Z | Scene / path | Conditions / stock override |\n"
            "| --- | --- | --- | --- | --- | --- |\n"
            f"| [Test Zone ({zone})](../locations/zone-{zone}.md) | 27.817 | 419.344 | 228.324 | Scene test.lvl | No condition |\n",
            encoding="utf-8",
        )
        item_locations = root / "wiki" / "items" / "locations"
        item_locations.mkdir(parents=True)
        (item_locations / f"zone-{zone}.md").write_text(
            f"# Test Zone — zone {zone}\n\n"
            "[Locations](./README.md)\n\n"
            "| Source LOT | Mapped records | Uses |\n"
            "| --- | --- | --- |\n"
            "| Example | 1 | Drop |\n",
            encoding="utf-8",
        )
        pet_locations = root / "wiki" / "pets" / "locations"
        pet_locations.mkdir(parents=True)
        (pet_locations / f"zone-{zone}.md").write_text(
            f"# Test Zone — zone {zone}\n\n"
            "| Pet template | X | Y | Z | Scene / spawner | Recorded conditions |\n"
            "| --- | --- | --- | --- | --- | --- |\n"
            "| [Triceratops (3195)](../3195.md) | -420 | 367.7 | -35.54 | Pet spawner | No gate |\n",
            encoding="utf-8",
        )
        zones = root / "wiki" / "zones"
        zones.mkdir(parents=True)
        (zones / f"{zone}.md").write_text(
            f"# Test Zone — zone {zone}\n\n"
            "<!-- media:start -->\n"
            f"![Minimap](../../assets/minimaps/{zone}.webp)\n"
            "<!-- media:end -->\n\n"
            "[Zones](./README.md)\n",
            encoding="utf-8",
        )
        scripts = root / "scripts"
        scripts.mkdir(parents=True)
        (scripts / "location_map_world_markers.csv").write_text(
            "zone,category,name,lot,x,y,z,details,path\n",
            encoding="utf-8",
        )

    def test_builds_pilot_markers_with_coordinate_projection(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.create_root(root)

            stats = maps.build(root)
            data = json.loads((root / "assets" / "location-maps" / "1100.json").read_text(encoding="utf-8"))

            self.assertEqual((stats["items"], stats["pets"], stats["markers"]), (1, 1, 2))
            item, pet = data["markers"]
            self.assertEqual(item["path"], "wiki/items/sources/object-4990/")
            self.assertEqual((item["pixelX"], item["pixelY"]), (500.41, 416.865))
            self.assertEqual(pet["path"], "wiki/pets/3195/")
            self.assertEqual(data["projection"]["pixelsPerWorldUnit"], 5 / 12)
            self.assertTrue(data["projection"]["xAxisReversed"])
            self.assertTrue(data["projection"]["provisional"])
            zone_page = (root / "wiki" / "zones" / "1100.md").read_text(encoding="utf-8")
            self.assertIn('data-category="all"', zone_page)
            self.assertIn('data-map-data="../../../assets/location-maps/1100.json"', zone_page)
            self.assertIn("terrain-bounds projection is still provisional", zone_page)
            self.assertIn('data-category="items"', (root / "wiki" / "items" / "locations" / "zone-1100.md").read_text(encoding="utf-8"))
            self.assertIn('data-category="pets"', (root / "wiki" / "pets" / "locations" / "zone-1100.md").read_text(encoding="utf-8"))

    def test_builds_forbidden_valley_projection_and_embeds_all_pages(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.create_root(root, zone=1400)

            stats = maps.build(root, zone=1400)
            data = json.loads((root / "assets" / "location-maps" / "1400.json").read_text(encoding="utf-8"))

            self.assertEqual((stats["items"], stats["pets"], stats["markers"]), (1, 1, 2))
            self.assertEqual(data["projection"]["pixelsPerWorldUnit"], 0.5)
            self.assertEqual((data["markers"][0]["pixelX"], data["markers"][0]["pixelY"]), (498.091, 397.838))
            self.assertIn('data-zone="1400"', (root / "wiki" / "zones" / "1400.md").read_text(encoding="utf-8"))
            self.assertIn('data-map-data="../../../assets/location-maps/1400.json"', (root / "wiki" / "zones" / "1400.md").read_text(encoding="utf-8"))
            self.assertIn('data-category="items"', (root / "wiki" / "items" / "locations" / "zone-1400.md").read_text(encoding="utf-8"))
            self.assertIn('data-category="pets"', (root / "wiki" / "pets" / "locations" / "zone-1400.md").read_text(encoding="utf-8"))

    def test_build_is_idempotent(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.create_root(root)

            maps.build(root)
            stats = maps.build(root)

            self.assertFalse(stats["data_updated"])
            self.assertEqual(stats["updated_pages"], 0)
            zone_page = (root / "wiki" / "zones" / "1100.md").read_text(encoding="utf-8")
            self.assertEqual(zone_page.count(maps.START), 1)

    def test_builds_world_markers_without_required_lots_or_detail_links(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.create_root(root)
            source = root / "scripts" / "location_map_world_markers.csv"
            source.write_text(
                "zone,category,name,lot,x,y,z,details,path\n"
                "1100,launchpads,AG launch pad,14216,10,0,20,Destination zone 1150,\n"
                "1100,transitions,Scene transition,,0,0,0,Connected scene: Main Scene,\n",
                encoding="utf-8",
            )

            stats = maps.build(root)
            data = json.loads(
                (root / "assets" / "location-maps" / "1100.json").read_text(encoding="utf-8")
            )
            markers = {marker["name"]: marker for marker in data["markers"]}

            self.assertEqual(stats["launchpads"], 1)
            self.assertEqual(stats["transitions"], 1)
            self.assertEqual(markers["AG launch pad"]["lot"], 14216)
            self.assertNotIn("path", markers["AG launch pad"])
            self.assertNotIn("lot", markers["Scene transition"])
            self.assertEqual(markers["Scene transition"]["pixelX"], 512.0)

    def test_links_actor_markers_to_existing_npc_pages(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.create_root(root)
            npc_page = root / "wiki" / "npcs" / "14381.md"
            npc_page.parent.mkdir(parents=True)
            npc_page.write_text("# Spider Queen\n", encoding="utf-8")
            source = root / "scripts" / "location_map_world_markers.csv"
            source.write_text(
                "zone,category,name,lot,x,y,z,details,path\n"
                "1100,enemies,Spider Queen,14381,10,0,20,Spawner: SpiderBoss,\n",
                encoding="utf-8",
            )

            maps.build(root)
            data = json.loads(
                (root / "assets" / "location-maps" / "1100.json").read_text(encoding="utf-8")
            )
            marker = next(marker for marker in data["markers"] if marker["name"] == "Spider Queen")

            self.assertEqual(marker["path"], "wiki/npcs/14381/")

    def test_rejects_world_markers_outside_calibrated_map(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.create_root(root)
            source = root / "scripts" / "location_map_world_markers.csv"
            source.write_text(
                "zone,category,name,lot,x,y,z,details,path\n"
                "1100,transitions,Invalid transition,,2000,0,0,,\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "projects outside"):
                maps.build(root)

    def test_rejects_points_outside_calibrated_map(self):
        with self.assertRaisesRegex(ValueError, "projects outside"):
            maps.coordinates_to_pixel(2000, 0, 1100, Path("object-1.md"), 10)

    def test_projects_non_square_zone_with_independent_axis_scales(self):
        self.assertEqual(
            maps.coordinates_to_pixel(10, 20, 1402, Path("object-1.md"), 10),
            (502.0, 495.333),
        )

    def test_offsets_projection_to_raw_terrain_center(self):
        self.assertEqual(
            maps.coordinates_to_pixel(0, 0, 1251, Path("object-1.md"), 10),
            (597.333, 512.0),
        )

    def test_rejects_invalid_coordinates_in_supported_zone_table(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.create_root(root)
            source = root / "wiki" / "items" / "sources" / "object-4990.md"
            source.write_text(
                source.read_text(encoding="utf-8").replace("| 27.817 |", "| unknown |"),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "invalid map coordinate"):
                maps.item_source_markers(root, 1100)


if __name__ == "__main__":
    unittest.main()
