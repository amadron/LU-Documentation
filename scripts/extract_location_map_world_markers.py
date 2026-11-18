"""Extract world-object, NPC, shop, and transition coordinates from client maps.

Usage (from the documentation root):
    py -3 scripts/extract_location_map_world_markers.py --client-res "C:\\path\\to\\res\\res"
"""

import argparse
import csv
import struct
from dataclasses import dataclass
from pathlib import Path

import build_location_maps


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "scripts" / "location_map_world_markers.csv"
NPC_TYPES = {"NPC", "UserGeneratedNPCs", "Enemies"}
PET_CLASSIFICATION = "pet"
VENDOR_COMPONENT_TYPES = {16, 65, 100, 102}
ROCKET_LAUNCH_COMPONENT = 67
ROCKET_LANDING_COMPONENT = 68
PROPERTY_ENTRANCE_COMPONENT = 43
MULTI_ZONE_ENTRANCE_COMPONENT = 97


@dataclass(frozen=True)
class Scene:
    scene_id: int
    scene_type: int
    name: str
    filename: str


@dataclass(frozen=True)
class TransitionPoint:
    scene_id: int
    layer_id: int
    position: tuple


@dataclass(frozen=True)
class SpawnerPath:
    name: str
    lot: int
    max_to_spawn: int
    waypoints: tuple


@dataclass(frozen=True)
class ZoneResource:
    scenes: dict
    transitions: tuple
    spawners: tuple


@dataclass(frozen=True)
class LevelObject:
    lot: int
    position: tuple
    settings: str


class BinaryReader:
    def __init__(self, data, path):
        self.data = data
        self.path = path
        self.offset = 0

    def read(self, format_string):
        size = struct.calcsize("<" + format_string)
        self.require(size)
        values = struct.unpack_from("<" + format_string, self.data, self.offset)
        self.offset += size
        return values[0] if len(values) == 1 else values

    def read_string(self, size_format="B", wide=False):
        count = self.read(size_format)
        size = count * (2 if wide else 1)
        self.require(size)
        raw = self.data[self.offset:self.offset + size]
        self.offset += size
        return raw.decode("utf-16le" if wide else "utf-8", errors="replace")

    def skip(self, size):
        self.require(size)
        self.offset += size

    def require(self, size):
        if size < 0 or self.offset + size > len(self.data):
            raise ValueError(
                f"{self.path}: truncated binary data at offset {self.offset} "
                f"(need {size} bytes, file has {len(self.data)})"
            )


def _read_spawner_path(reader, path_version, path_name):
    path_type = reader.read("I")
    reader.skip(8)  # flags and behavior
    max_to_spawn = 0

    if path_type == 1:  # Moving platform
        if path_version >= 18:
            reader.skip(1)
        elif path_version >= 13:
            reader.read_string(wide=True)
    elif path_type == 2:  # Property
        reader.skip(20)  # type, price, rental time, and associated zone
        if path_version >= 5:
            reader.read_string(wide=True)
            reader.read_string("I", wide=True)
        if path_version >= 6:
            reader.skip(4)
        if path_version >= 7:
            reader.skip(12)
        if path_version >= 8:
            reader.skip(20)
    elif path_type == 3:  # Camera
        reader.read_string(wide=True)
        if path_version >= 14:
            reader.skip(1)
    elif path_type == 4:  # Spawner
        lot = reader.read("I")
        reader.skip(4)  # respawn time
        max_to_spawn = reader.read("i")
        reader.skip(4 + 8 + 1)  # maintained count, object ID, active flag
    elif path_type not in (0, 5, 6, 7):
        raise ValueError(f"{reader.path}: unsupported LUZ path type {path_type}")

    waypoint_count = reader.read("I")
    waypoints = []
    for _ in range(waypoint_count):
        position = reader.read("fff")
        if path_type in (1, 3, 4, 6, 7):
            reader.skip(16)  # rotation

        if path_type == 1:
            reader.skip(9)  # lock player, speed, and wait
            if path_version >= 13:
                reader.read_string(wide=True)
                reader.read_string(wide=True)
        elif path_type == 3:
            reader.skip(20)  # camera settings
        elif path_type == 6:
            reader.skip(14)  # race node flags and dimensions
        elif path_type == 7 and path_version > 16:
            reader.skip(4)  # rail speed

        settings = {}
        if path_type in (0, 4, 7):
            setting_count = reader.read("I")
            for _ in range(setting_count):
                key = reader.read_string(wide=True)
                value = reader.read_string(wide=True)
                settings[key] = value
        waypoints.append((position, settings))

    if path_type == 4:
        return SpawnerPath(path_name, lot, max_to_spawn, tuple(waypoints))
    return None


def parse_zone(data, path):
    reader = BinaryReader(data, path)
    version = reader.read("I")
    if version >= 36:
        reader.skip(4)  # map revision
    reader.skip(4)  # world ID
    if version >= 38:
        reader.skip(28)  # spawn position and rotation

    scene_count = reader.read("I" if version >= 37 else "B")
    scenes = {}
    for index in range(scene_count):
        filename = reader.read_string()
        scene_id = reader.read("I") if version >= 33 or version < 30 else index
        scene_type = reader.read("I") if version >= 33 else 0
        name = reader.read_string() if version >= 33 else Path(filename).stem
        if version == 37:
            reader.skip(16)
        if version >= 33:
            reader.skip(3)  # scene color
        scenes[scene_id] = Scene(scene_id, scene_type, name, filename)

    boundary_count = reader.read("B")
    for _ in range(boundary_count):
        reader.skip(24)  # plane normal and point
        reader.skip(8)  # destination map and instance
        reader.skip(4)  # destination scene
        reader.skip(12)  # spawn position

    reader.read_string()  # raw terrain path
    if version > 30:
        reader.read_string()  # zone name
        reader.read_string()  # zone description

    transitions = []
    if version >= 32:
        transition_count = reader.read("I")
        point_count = 2 if version <= 33 or version >= 39 else 5
        for _ in range(transition_count):
            if version < 40:
                reader.read_string()  # transition name
                reader.skip(4)  # transition width
            points = []
            for _ in range(point_count):
                points.append(TransitionPoint(
                    reader.read("I"),
                    reader.read("I"),
                    reader.read("fff"),
                ))
            transitions.append(tuple(points))

    spawners = []
    if version >= 35:
        reader.read("I")  # path data length
        path_chunk_version = reader.read("I")
        if path_chunk_version != 1:
            raise ValueError(
                f"{path}: unsupported LUZ path chunk version {path_chunk_version}"
            )
        path_count = reader.read("I")
        for _ in range(path_count):
            path_version = reader.read("I")
            path_name = reader.read_string(wide=True)
            spawner = _read_spawner_path(reader, path_version, path_name)
            if spawner is not None:
                spawners.append(spawner)

    if reader.offset != len(data):
        raise ValueError(
            f"{path}: parsed through offset {reader.offset}, "
            f"but file has {len(data)} bytes"
        )
    return ZoneResource(scenes, tuple(transitions), tuple(spawners))


def _load_on_client_only(settings):
    for line in settings.splitlines():
        key, separator, encoded_value = line.partition("=")
        if separator and key.strip() == "loadOnClientOnly":
            value = encoded_value.rsplit(":", 1)[-1].strip().lower()
            return value in {"1", "true"}
    return False


def parse_level_objects(data, path):
    offset = 0
    file_version = None
    object_data_offset = None
    if data.startswith(b"CHNK"):
        while offset < len(data):
            if data[offset:offset + 4] != b"CHNK":
                raise ValueError(f"{path}: expected CHNK at offset {offset}")
            if offset + 20 > len(data):
                raise ValueError(f"{path}: truncated CHNK header at offset {offset}")
            chunk_id, _, _, chunk_size, data_offset = struct.unpack_from(
                "<IHHII", data, offset + 4
            )
            if chunk_size < 20 or offset + chunk_size > len(data):
                raise ValueError(f"{path}: invalid CHNK size {chunk_size} at offset {offset}")
            if data_offset < offset + 20 or data_offset > offset + chunk_size:
                raise ValueError(f"{path}: invalid CHNK data offset {data_offset}")
            if chunk_id == 1000:
                file_version = struct.unpack_from("<I", data, data_offset)[0]
            elif chunk_id == 2001:
                object_data_offset = data_offset
            offset += chunk_size
    else:
        reader = BinaryReader(data, path)
        file_version = reader.read("H")
        reader.skip(2)  # legacy chunk type
        important = reader.read("B")
        if file_version > 36:
            reader.skip(4)  # revision
        if file_version >= 45:
            reader.skip(4)
        reader.skip(48)  # three legacy vectors
        if file_version >= 31:
            if file_version >= 39:
                reader.skip(48)
                if file_version >= 40:
                    reader.skip(reader.read("I") * 12)
            else:
                reader.skip(8)
            reader.skip(12)
        if file_version >= 36:
            reader.skip(12)
        if file_version < 42:
            reader.skip(12)
            if file_version >= 33:
                reader.skip(16)
        reader.skip(reader.read("I"))  # sky dome data
        if file_version >= 33:
            for _ in range(5):
                reader.skip(reader.read("I"))
        if not important and file_version >= 37:
            reader.skip(4)
            reader.skip(reader.read("I") * 12)
        object_data_offset = reader.offset

    if object_data_offset is None:
        return []

    reader = BinaryReader(data, path)
    reader.offset = object_data_offset
    object_count = reader.read("I")
    objects = []
    for _ in range(object_count):
        reader.read("Q")  # object ID
        lot = reader.read("I")
        if file_version >= 38:
            reader.skip(4)  # node type
        if file_version >= 32:
            reader.skip(4)  # glom ID
        position = reader.read("fff")
        reader.skip(20)  # rotation and scale
        settings = reader.read_string("I", wide=True)
        reader.skip(4)  # value3
        if not _load_on_client_only(settings):
            objects.append(LevelObject(lot, position, settings))
    return objects


def _read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def _world_category(npc, component_types):
    if component_types & VENDOR_COMPONENT_TYPES:
        return "shops"
    if not npc or npc["ObjectType"] not in NPC_TYPES:
        return None
    if PET_CLASSIFICATION in npc["Classification"].casefold():
        return None
    return "enemies" if npc["ObjectType"] == "Enemies" else "npcs"


def _marker(zone, category, name, position, details, lot=None):
    return {
        "zone": zone,
        "category": category,
        "name": name,
        "lot": lot,
        "x": position[0],
        "y": position[1],
        "z": position[2],
        "details": details,
        "path": "",
    }


def _scene_name(scene):
    return scene.name or Path(scene.filename).stem


def extract_markers(client_res, root=ROOT):
    database = root / "db"
    zone_rows = _read_csv(database / "ZoneTable.csv")
    object_rows = _read_csv(database / "Objects.csv")
    component_rows = _read_csv(database / "ComponentsRegistry.csv")
    npc_rows = _read_csv(root / "LEGO Universe NPC List.csv")
    rocket_rows = _read_csv(database / "RocketLaunchpadControlComponent.csv")
    entrance_rows = _read_csv(database / "PropertyEntranceComponent.csv")

    objects = {int(row["id"]): row for row in object_rows}
    npcs = {int(row["LOT"]): row for row in npc_rows}
    components = {}
    for row in component_rows:
        components.setdefault(int(row["id"]), set()).add((
            int(row["component_type"]),
            int(row["component_id"]),
        ))
    rocket_controls = {int(row["id"]): row for row in rocket_rows}
    property_entrances = {int(row["id"]): row for row in entrance_rows}
    markers = []

    for zone in build_location_maps.ZONE_CONFIGS:
        zone_row = next(
            (row for row in zone_rows if int(row["zoneID"]) == zone),
            None,
        )
        if zone_row is None:
            raise ValueError(f"{database / 'ZoneTable.csv'}: missing zone {zone}")
        relative_path = zone_row["zoneName"].replace("\\", "/")
        zone_path = client_res / "maps" / Path(*relative_path.split("/"))
        resource = parse_zone(zone_path.read_bytes(), zone_path)

        def append_projected(marker):
            marker["pixelX"], marker["pixelY"] = build_location_maps.coordinates_to_pixel(
                marker["x"], marker["z"], zone, zone_path, 1
            )
            markers.append(marker)

        for transition in resource.transitions:
            for point in transition:
                scene = resource.scenes.get(point.scene_id)
                if scene is None or scene.scene_type != 0:
                    continue
                other_scenes = [
                    _scene_name(resource.scenes[other.scene_id])
                    for other in transition
                    if other.scene_id != point.scene_id
                    and other.scene_id in resource.scenes
                ]
                details = (
                    "Connected scene: " + ", ".join(dict.fromkeys(other_scenes))
                    if other_scenes else "Scene transition"
                )
                append_projected(_marker(
                    zone,
                    "transitions",
                    f"Transition in {_scene_name(scene)}",
                    point.position,
                    details,
                ))

        for spawner in resource.spawners:
            npc = npcs.get(spawner.lot)
            component_types = {
                component_type for component_type, _ in components.get(spawner.lot, set())
            }
            category = _world_category(npc, component_types)
            if category is None:
                continue
            object_row = objects.get(spawner.lot, {})
            name = (
                npc["DisplayName"] or npc["Name"]
                if npc else object_row.get("displayName") or object_row.get("name")
            )
            name = name or f"LOT {spawner.lot}"
            details = f"Spawner: {spawner.name}"
            if spawner.max_to_spawn >= 0:
                details += f"; maximum {spawner.max_to_spawn}"
            for position, _ in spawner.waypoints:
                append_projected(_marker(
                    zone, category, name, position, details, spawner.lot
                ))

        for scene in resource.scenes.values():
            if scene.scene_type != 0:
                continue
            level_path = zone_path.parent / scene.filename
            for placed_object in parse_level_objects(level_path.read_bytes(), level_path):
                component_entries = components.get(placed_object.lot, set())
                component_types = {entry[0] for entry in component_entries}
                object_row = objects.get(placed_object.lot, {})
                npc = npcs.get(placed_object.lot)
                category = _world_category(npc, component_types)
                details = f"Placed in {_scene_name(scene)}"

                if ROCKET_LAUNCH_COMPONENT in component_types or ROCKET_LANDING_COMPONENT in component_types:
                    category = "launchpads"
                    name = object_row.get("displayName") or object_row.get("name")
                    name = name or "Rocket launch / landing pad"
                    controls = [
                        rocket_controls[component_id]
                        for component_type, component_id in component_entries
                        if component_type == ROCKET_LAUNCH_COMPONENT
                        and component_id in rocket_controls
                    ]
                    if controls:
                        details = f"Destination zone {controls[0]['targetZone']}"
                        if controls[0]["targetScene"]:
                            details += f"; scene {controls[0]['targetScene']}"
                elif PROPERTY_ENTRANCE_COMPONENT in component_types:
                    category = "transitions"
                    name = object_row.get("displayName") or object_row.get("name")
                    entrance_ids = [
                        component_id for component_type, component_id in component_entries
                        if component_type == PROPERTY_ENTRANCE_COMPONENT
                    ]
                    entrance = next(
                        (property_entrances[value] for value in entrance_ids if value in property_entrances),
                        None,
                    )
                    if entrance:
                        details = (
                            f"Property entrance to zone {entrance['mapID']} "
                            f"({entrance['propertyName']})"
                        )
                elif MULTI_ZONE_ENTRANCE_COMPONENT in component_types:
                    category = "transitions"
                    name = object_row.get("displayName") or object_row.get("name")
                    details = "Multi-zone entrance"
                elif category:
                    name = (
                        npc["DisplayName"] or npc["Name"]
                        if npc else object_row.get("displayName") or object_row.get("name")
                    )
                else:
                    continue

                append_projected(_marker(
                    zone,
                    category,
                    name or f"LOT {placed_object.lot}",
                    placed_object.position,
                    details,
                    placed_object.lot,
                ))

    return markers


def write_markers(markers, output=OUTPUT):
    fieldnames = ("zone", "category", "name", "lot", "x", "y", "z", "details", "path")
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for marker in sorted(markers, key=lambda item: (
            item["zone"], item["category"], item["name"].casefold(),
            item["lot"] or 0, item["x"], item["z"],
        )):
            writer.writerow({field: marker.get(field, "") for field in fieldnames})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--client-res",
        required=True,
        type=Path,
        help="Client resource root containing maps/ (for example res/res)",
    )
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    markers = extract_markers(args.client_res, ROOT)
    write_markers(markers, args.output)
    counts = {}
    for marker in markers:
        counts[marker["category"]] = counts.get(marker["category"], 0) + 1
    print(f"Wrote {len(markers)} world markers to {args.output}")
    print(", ".join(f"{key}: {value}" for key, value in sorted(counts.items())))


if __name__ == "__main__":
    main()
