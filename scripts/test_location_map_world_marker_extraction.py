import struct
import unittest
from pathlib import Path

import extract_location_map_world_markers as extraction


def _string(value, wide=False, size_format="B"):
    encoded = value.encode("utf-16le" if wide else "utf-8")
    count = len(encoded) // (2 if wide else 1)
    return struct.pack("<" + size_format, count) + encoded


def _make_zone():
    data = bytearray(struct.pack("<III", 41, 0, 1100))
    data.extend(struct.pack("<7f", 0, 0, 0, 0, 0, 0, 1))
    data.extend(struct.pack("<I", 2))
    for scene_id, filename, name in (
        (1, "main.lvl", "Main Scene"),
        (2, "sublevel.lvl", "Sublevel"),
    ):
        data.extend(_string(filename))
        data.extend(struct.pack("<II", scene_id, 0))
        data.extend(_string(name))
        data.extend(b"\0\0\0")
    data.extend(b"\0")  # no zone boundaries
    data.extend(_string("terrain.raw"))
    data.extend(_string("Test Zone"))
    data.extend(_string(""))
    data.extend(struct.pack("<I", 1))  # one scene transition
    data.extend(struct.pack("<II3f", 1, 0, 1, 2, 3))
    data.extend(struct.pack("<II3f", 2, 0, 4, 5, 6))
    data.extend(struct.pack("<III", 0, 1, 1))  # path length, chunk version, count
    data.extend(struct.pack("<I", 18))
    data.extend(_string("Friendly NPCs", wide=True))
    data.extend(struct.pack("<III", 4, 0, 0))  # spawner, flags, behavior
    data.extend(struct.pack("<IiiIQB", 4712, 30, 4, 1, 99, 1))
    data.extend(struct.pack("<I", 2))
    for position in ((10, 20, 30), (40, 50, 60)):
        data.extend(struct.pack("<3f4fI", *position, 0, 0, 0, 1, 1))
        data.extend(_string("spawner_name", wide=True))
        data.extend(_string("Friendly NPCs", wide=True))
    return bytes(data)


def _level_object(object_id, lot, position, settings):
    encoded_settings = settings.encode("utf-16le")
    return (
        struct.pack(
            "<QIII3f4ffI",
            object_id, lot, 0, 0, *position, 0, 0, 0, 1, 1, len(settings),
        )
        + encoded_settings
        + struct.pack("<I", 0)
    )


def _chunk(chunk_id, payload, offset):
    size = 20 + len(payload)
    return (
        b"CHNK"
        + struct.pack("<IHHII", chunk_id, 0, 0, size, offset + 20)
        + payload
    )


def _make_chunked_level():
    file_info = struct.pack("<5I", 48, 0, 0, 0, 0)
    info_chunk = _chunk(1000, file_info, 0)
    object_data = (
        struct.pack("<I", 2)
        + _level_object(1, 4712, (1, 2, 3), "loadOnClientOnly=7:0")
        + _level_object(2, 4713, (4, 5, 6), "loadOnClientOnly=7:1")
    )
    return info_chunk + _chunk(2001, object_data, len(info_chunk))


def _make_legacy_level():
    version = 43
    data = bytearray(struct.pack("<HHB", version, 0, 1))
    data.extend(struct.pack("<I", 0))  # revision
    data.extend(bytes(48))  # three legacy vectors
    data.extend(bytes(48))  # version 39+ vectors
    data.extend(struct.pack("<I", 0))  # version 40+ data count
    data.extend(bytes(12))
    data.extend(bytes(12))
    data.extend(struct.pack("<I", 0))  # sky dome data length
    data.extend(struct.pack("<5I", 0, 0, 0, 0, 0))
    data.extend(struct.pack("<I", 1))
    data.extend(_level_object(3, 4714, (7, 8, 9), ""))
    return bytes(data)


class WorldMarkerExtractionTests(unittest.TestCase):
    def test_parses_scene_transitions_and_spawner_waypoints(self):
        zone = extraction.parse_zone(_make_zone(), Path("test.luz"))

        self.assertEqual(len(zone.transitions), 1)
        self.assertEqual(zone.transitions[0][1].position, (4.0, 5.0, 6.0))
        self.assertEqual(len(zone.spawners), 1)
        self.assertEqual(zone.spawners[0].lot, 4712)
        self.assertEqual(zone.spawners[0].max_to_spawn, 4)
        self.assertEqual(len(zone.spawners[0].waypoints), 2)
        self.assertEqual(
            zone.spawners[0].waypoints[0][1]["spawner_name"],
            "Friendly NPCs",
        )

    def test_parses_chunked_level_and_omits_client_only_objects(self):
        objects = extraction.parse_level_objects(_make_chunked_level(), Path("test.lvl"))

        self.assertEqual([(obj.lot, obj.position) for obj in objects], [(4712, (1.0, 2.0, 3.0))])

    def test_parses_legacy_level_layout(self):
        objects = extraction.parse_level_objects(_make_legacy_level(), Path("legacy.lvl"))

        self.assertEqual([(obj.lot, obj.position) for obj in objects], [(4714, (7.0, 8.0, 9.0))])

    def test_classifies_enemies_separately_and_excludes_pets(self):
        self.assertEqual(
            extraction._world_category(
                {"ObjectType": "Enemies", "Classification": "Enemy"},
                set(),
            ),
            "enemies",
        )
        self.assertEqual(
            extraction._world_category(
                {"ObjectType": "NPC", "Classification": "NPC, Pet/creature"},
                set(),
            ),
            None,
        )
        self.assertEqual(
            extraction._world_category(
                {"ObjectType": "UserGeneratedNPCs", "Classification": "Vendor"},
                {16},
            ),
            "shops",
        )


if __name__ == "__main__":
    unittest.main()
