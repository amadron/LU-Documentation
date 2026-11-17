# Asset Formats and Tools

[Content authoring](./README.md) | [Zone file reference](./reference/zone-files-and-fields.md) | [Testing and troubleshooting](./test-and-troubleshoot.md)

This overview identifies formats and community tools useful when investigating
or creating content. Tool capabilities below are taken from the linked
projects' documentation, reviewed on 2026-11-17; **the tools and conversions
were not independently tested for this guide**. Support for a format does not
guarantee compatibility with every client version or a working in-game asset.

## Formats at a glance

| Format | Typical role | Starting point |
|---|---|---|
| `.pk` | Client resource archive | [PK tools](#archives) |
| `.luz`, `.lvl` | Zone metadata and referenced scene/level resources | [Zone tools](#zones-and-scenes); [server parser reference](./reference/zone-files-and-fields.md) |
| `.raw` | Terrain data referenced by zones | [Zone file reference](./reference/zone-files-and-fields.md); no editor workflow verified here |
| `.nif` | Gamebryo model and mesh data | [Model tools and NifSkope](#models-and-animation) |
| `.kf` | Gamebryo animation data | [Model tools](#models-and-animation) |
| `.hkx` | Havok physics and collision data | [Model tools](#models-and-animation) |
| `.lxf`, `.lxfml` | LEGO brick models | [Model tools and LU Toolbox](#brick-models) |
| `.dds` | Texture images | [GIMP](#textures) |
| `.fdb`, `.sqlite` | Client data and SQLite database files | [Database tools](#client-data-and-skills) |
| `.psb` | ForkParticle particle effects | [Particle editor](#particle-effects) |

These are not interchangeable formats: for example, converting a model is not
the same as registering an object in CDClient or implementing its server
behavior. [lu-assets](https://github.com/LU-Rebuilt/lu-assets) lists additional
formats it can parse, including audio and UI formats, but it is a programming
library rather than a general-purpose editor.

## Archives

- [LU-Rebuilt pk-tools](https://github.com/LU-Rebuilt/pk-tools) provides a
  command-line extractor and a Qt viewer. Its README says the CLI extracts
  entries as numbered `.bin` files; the viewer can resolve names from client
  manifests and extract selected files. The documented CLI and viewer are
  **extractors**, not a verified archive-repacking workflow.
- [LUPK Archiver](https://github.com/j-usti-n/LUPK_Archiver) describes itself
  as an archive editor. Its README does not document detailed format/version
  support or a tested repacking procedure.

Archive layouts, manifests, paths, and compression vary. Keep originals and
confirm how your particular client reads resources before changing a pack.

## Zones and scenes

[LU-Rebuilt zone-tools](https://github.com/LU-Rebuilt/zone-tools) describes:

- `zone_editor`: a Qt editor for zone data, referenced scenes, objects, and
  paths; its README describes saving LUZ and modified LVL files.
- `zone2json` and `json2zone`: command-line conversion between a zone with
  its referenced scenes and a JSON representation. The project reports
  round-trip testing, but explicitly excludes non-CHNK LVL files and some
  nonstandard LUZ containers.

The project documents CMake 3.25+, a C++20 compiler, and optional Qt6 for
the GUI. The client and server still need consistent resource paths, data
records, and an entry route; see [Create or Extend a Zone](./create-or-extend-a-zone.md).

## Models and animation

[LU-Rebuilt model-tools](https://github.com/LU-Rebuilt/model-tools) documents
viewers for NIF, HKX, and brick models, plus these conversions:

- `nif2usd`: NIF to USD for inspection or editing in tools such as Blender.
- `usd2nif`: USD meshes and basic materials back to NIF. The project says this
  is **not byte-identical** and does not currently import skeletons, animation,
  or collision. Do not treat it as a complete animated-model round trip.
- `kf2usd` and `hkx2usd`: animation and collision data to USD for inspection.
- `nif_viewer`: inspect NIF and, according to the project, generate and save
  HKX collision shapes from its geometry.

The USD utilities require OpenUSD; viewers require Qt6/OpenGL. Consult the
project README for build options and dependencies. Blender documents
[USD import and export](https://docs.blender.org/manual/en/latest/files/import_export/usd.html),
including its own limitations. Test coordinate orientation, materials,
textures, collision, and animation separately in the target client.

[NifSkope](https://github.com/niftools/nifskope) is a general NIF inspection
and editing tool. Its project documentation does not establish that every
LEGO Universe NIF variant or save operation is compatible with the target
client; verify on copies.

## Brick models

- [LU Toolbox](https://github.com/Squareville/lu-toolbox) is a Blender add-on
  that imports LXF/LXFML and prepares brick models. Its README specifies
  Blender 3.1 or later for v2.0 and requires a brick database or client
  resource directory. Import and preparation alone do not prove a complete
  export-to-client workflow.
- The `lxfml_viewer` in [model-tools](https://github.com/LU-Rebuilt/model-tools)
  opens LXF/LXFML; the project says brick geometry requires a client resource
  directory.

The LU Toolbox project also links an external
[DLU Asset Creation Guide](https://docs.google.com/document/d/15YDtHg3-i3Pn6HTEFkpAjKsvUF6u49ZsQam5b614YRw)
by cdmpants. Its content was not independently reviewed for this overview.

## Textures

[GIMP](https://www.gimp.org/news/2019/04/07/gimp-2-10-10-released/#dds-support)
documents built-in DDS loading and export starting with version 2.10.10.
When editing a texture, preserve the original and check compression, alpha,
mipmaps, and the target client's behavior; generic DDS support is not proof
that every exported variant will work in LEGO Universe.

## Client data and skills

- [LU-Rebuilt fdb-tools](https://github.com/LU-Rebuilt/fdb-tools) documents an
  FDB-to-SQLite converter and an FDB/SQLite viewer. The documented conversion
  is **FDB to SQLite**, not a round-trip guarantee.
- [FDB-Converter](https://github.com/IAmMajo/FDB-Converter) describes
  FDB-to-SQLite and SQLite-to-FDB conversion. Verify outputs and backups for
  the target client version. The project says its website processes files
  client-side; review its code and privacy properties before using a hosted tool.
- [LU-Rebuilt skill-editor](https://github.com/LU-Rebuilt/skill-editor)
  describes a graphical behavior-tree editor for CDClient SQLite data. It can
  load localization for names when that file is available. A modified database
  still needs compatible server and client behavior.

See the [CDClient Table Guide](./reference/cdclient-tables.md) for relationships
between records and server code.

## Particle effects

[LU-Rebuilt psb-editor](https://github.com/LU-Rebuilt/psb-editor) describes a
Qt/OpenGL editor for `.psb` emitters and effect `.txt` files. Its README
describes loading, previewing, and saving effects; texture lookup may require
a matching client resource directory.

## Safe workflow and rights

1. Work with authorized resources and keep untouched backups of files and
   databases. Tool licenses do not grant rights to the game assets themselves.
2. Record client, server, tool, and data versions. Build and run third-party
   software only after reviewing its source, dependencies, and license.
3. Use a disposable test copy. Compare converted output and test rendering,
   collision, interaction, and server logs independently before deployment.
4. Do not publish or upload original client assets or complete data exports
   without appropriate rights. A local tool may still fetch dependencies when
   built; a website's privacy claims require separate verification.

For in-game checks, use [Testing and Troubleshooting](./test-and-troubleshoot.md).
