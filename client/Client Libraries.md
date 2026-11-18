# LEGO Universe Client Libraries

[Home](../index.md) | [Client documentation](./README.md) | [Data model](../LEGO%20Universe%20Data%20Model%20and%20Public%20Research.md) | [Server libraries](../server/DarkflameServer%20Libraries.md)

The LEGO Universe client (`legouniverse.exe`, final version from 2011) is built on licensed
middleware. Some libraries ship as separate DLLs next to the executable; others are linked into
the executable itself and can only be recognized by the version and copyright strings they leave
inside it, and by the file formats in the client's `res` folder.

## Separate DLLs in the client folder

Read from the files' Windows version information.

| File | Library | Vendor | Version | Used for |
| --- | --- | --- | --- | --- |
| `awesomium.dll`, `awesomiumprocess.exe` | Awesomium | Khrona LLC | 1.6.0.6 | Embedded web browser (Chromium-based) for HTML content shown inside the game |
| `binkw32.dll` | Bink Video | RAD Game Tools | 1.9m | Video playback; the intro and cinematic movies in `res/Movies` are `.bik` files |
| `fmodex.dll` | FMOD Ex | Firelight Technologies | 4.32.6 | Sound engine |
| `fmod_event.dll` | FMOD Ex Event System | Firelight Technologies | 4.32.6 | Sound events and music authored in FMOD Designer (`.fev` / `.fsb` banks in `res/audio`) |
| `icudt42.dll` | ICU (International Components for Unicode), data | IBM and others | 4.2.1 | Unicode and localization data (text handling for chat and UI) |
| `stlport.5.2.dll` | STLport | STLport Consulting | 5.2.1 | Replacement C++ standard library |
| `d3dx9_34.dll` | Direct3D 9 extensions (D3DX) | Microsoft | 9.19.949 | Rendering helpers for DirectX 9 |
| `xinput1_3.dll` | XInput 1.3 | Microsoft | 9.18.944 | Game controller input |
| `cop.dll` | COPDLL | LEGO Company A/S | 1.20 | LEGO's own component. Its class names (`COPBrick`, `COPPart`, `COPScene`, `COPMesh`, `COPBehaviorElement`) and the Havok collision filters inside it point to brick-model building and connection checks; the meaning of "COP" is not documented. |

## Linked into `legouniverse.exe`

Identified from strings inside the executable and from the client's asset formats.

| Library | Vendor | Version evidence | Used for |
| --- | --- | --- | --- |
| Gamebryo | Emergent Game Technologies | "Gamebryo Version 2.3", "Gamebryo File Format, Version 2" | 3D engine: scene graph, rendering, animation. The models are Gamebryo `.nif` files (over 10,000 in `res`) and `.kf`/`.kfm` animations. |
| Havok Physics | Havok | "Havok-7.1" in the executable; asset files saved with "Havok-5.1.0-r1" | Physics and collision; about 4,200 `.hkx` collision files, e.g. in `res/BrickModels` |
| Scaleform GFx | Scaleform | "GFx" classes, "Scaleform" | Flash-based user interface; about 1,000 `.gfx` files in `res/ui` |
| RakNet | Jenkins Software | RakNet classes (`RakPeer`, `NetworkIDObject`) | Networking with the game servers. DarkflameServer uses RakNet 3.25 to stay compatible. |
| Lua | PUC-Rio | Lua C API symbols | Client-side scripts; about 1,800 `.lua` files in `res/scripts` |
| zlib | Jean-loup Gailly, Mark Adler | "deflate 1.2.2 … inflate 1.2.2" | Compression, e.g. of the packed asset files |
| TinyXML | Lee Thomason | "TinyXML failed to load locale file" | Reading XML files such as `locale.xml` |
| Expat | James Clark and others | Expat parser error strings | XML parsing |

## LEGO-specific data

The client also ships data from LEGO's own tools rather than third-party code:

- **LEGO Digital Designer brick data** (`res/brickdb.zip`, `res/brickprimitives`): the brick
  geometry and connection points used for building models, shared with LEGO Digital Designer.
- **`cdclient.fdb`**: the content database in LEGO Universe's own "FDB" format. DarkflameServer
  converts it to SQLite (`CDServer.sqlite`); see the [table reference](../LEGO%20Universe%20CDClient%20Table%20Reference.md).

## Source code availability

Whether the source code of a library is public, and which open alternatives exist. Open
replacements and readers were written independently (open source projects or reverse
engineering of the file formats); they are not the original code. Availability of source code
does not mean the client's copies may be redistributed.

| Library | Source code | Open alternatives and tools |
| --- | --- | --- |
| zlib | Open source ([zlib license](https://zlib.net/zlib_license.html)) | — |
| Lua | Open source ([MIT](https://www.lua.org/license.html)) | The client's scripts are plain `.lua` files in `res/scripts`. |
| TinyXML | Open source (zlib license) | — |
| Expat | Open source ([MIT](https://github.com/libexpat/libexpat)) | — |
| ICU | Open source ([ICU license](https://github.com/unicode-org/icu)) | — |
| STLport | Open source (permissive license) | — |
| RakNet | Open source since 2014: Oculus released it under a BSD license ([announcement](https://www.meta.com/blog/announcing-oculus-connect-raknet-open-source-and-e3-2014-awards/), [repository](https://github.com/facebookarchive/RakNet)). Before that the source was free for small games. | DarkflameServer ships a modified RakNet 3.25 that is compatible with the client. |
| Awesomium | Proprietary, discontinued | Built on Chromium, which is [open source](https://www.chromium.org/). |
| D3DX9, XInput | Proprietary (Microsoft) | [Wine](https://github.com/wine-mirror/wine/tree/master/dlls/d3dx9_34) contains independent open source implementations, e.g. `d3dx9_34` and `xinput1_3`. |
| Bink Video | Proprietary (RAD Game Tools, now Epic Games) | [FFmpeg](https://github.com/FFmpeg/FFmpeg/blob/master/libavcodec/bink.c) has an open source Bink video decoder that plays the `.bik` movies. |
| FMOD Ex | Proprietary (Firelight Technologies); the SDK with headers was free to download, the source was not | [vgmstream](https://github.com/vgmstream/vgmstream/blob/master/doc/FORMATS.md) reads FMOD sound banks (FSB1–FSB5), including the `.fsb` files of the client. |
| Gamebryo | Proprietary; source code only for licensees | The `.nif` model format is documented by reverse engineering in the [NifTools](https://www.niftools.org/) project (NifSkope, niflib). |
| Havok Physics | Proprietary; free binaries were offered for non-commercial use at times, but no source code | Only a few community tools for the `.hkx` format. |
| Scaleform GFx | Proprietary, discontinued (Autodesk) | `.gfx` is a variant of Flash SWF; the open source [JPEXS Free Flash Decompiler](https://github.com/jindrapetrik/jpexs-decompiler) can open GFX files. |
| `cop.dll` | Proprietary (LEGO); no public documentation | — |
| `legouniverse.exe` | Proprietary | The network protocol and the data formats (`.fdb`, `.luz`, `.lvl`, packed assets) were documented by the community through reverse engineering; [DarkflameServer](https://github.com/DarkflameUniverse/DarkflameServer) is built on this work. |

## How this was determined and limits

- DLL versions come from the Windows version information of each file in an unmodified
  installation of the final client.
- Embedded libraries are identified by version and copyright strings in `legouniverse.exe` and
  by matching file formats. Exact versions are given only where a string states them; libraries
  without such a string are listed without a version.
- Small helper code without identifying strings may be missing from this list.
- The client is proprietary. These libraries were licensed by NetDevil and The LEGO Group for
  the original game; the list is for reference and does not grant any rights to the files.
