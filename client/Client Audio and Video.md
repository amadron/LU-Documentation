# Client audio and video

[Client overview](./README.md) | [Rendering](./Client%20Rendering.md) | [Assets](./Client%20Assets%20and%20Content%20Data.md)

## Sound engine

Sound runs on **FMOD Ex 4.32** (`fmodex.dll`) with the **FMOD event system**
(`fmod_event.dll`). The game's sound layer is called **NDAudio** (ND for NetDevil): the
configuration keys start with `NDAUDIO_` and all banks are in `res/audio/NDAudio`.

Sound designers authored *events* in FMOD Designer. An event bundles one or more sound samples
with rules for variation, volume, 3D position, and parameters. The game triggers events by name
or GUID; it does not play raw sample files.

| File type | Count | Content |
| --- | --- | --- |
| `.fev` | 42 | Event project: event definitions, categories, and parameters |
| `.fsb` | 98 | Sound bank: the compressed samples referenced by the events |

### Event projects

| Category | Projects |
| --- | --- |
| Ambience | General ambience plus one project per world: Avant Gardens, Build the Flag, Forbidden Valley, Gnarled Forest, Nexus Tower, Nimbus Station, Ninjago, Pet Rock, pirate shooting gallery, racing, spaceship, "life" |
| Music | `Music_Front_End`, `music_global` |
| Voice-over | `VO/default` and one per language: Danish, Dutch, French, German, Italian, Norwegian, Portuguese, Spanish, Swedish |
| Gameplay | `skills`, `weapons`, `destructibles`, `interacts`, `missions`, `emotes`, `footsteps`, `foley`, `vehicles`, `build_mode` |
| Creatures | `creatures_mechanical`, `creatures_organic`, `creatures_pets` |
| Other | `ui`, `dialog`, `cinematics`, `min_install` (the minimum set for a partial installation) |

Zone-specific sound placement is stored next to the maps in `.aud` files (77 files in
`res/maps`).

### Audio settings

From `lwo.cfg.default`:

| Key | Default | Meaning |
| --- | --- | --- |
| `USENDAUDIO`, `MUTENDAUDIO` | `1`, `0` | Enable / mute the sound system |
| `NDAUDIO_NUM_VOICES` | `256` | Virtual voices (events that can be active) |
| `NDAUDIO_NUM_OUTPUT_VOICES` | `64` | Voices actually mixed at the same time |
| `NDAUDIO_CATEGORY_VOLUME_MUSIC` / `_SFX` / `_DIALOG` / `_AMBIENCE` | `1.0` | Volume per category |
| `NDAUDIO_MUTE_ON_UNFOCUS` | `1` | Mute when the window loses focus |
| `NDAUDIO_DIAGNOSTIC_LOGGING`, `NDAUDIO_DEBUG_LOG_LEVEL` | `0`, `3` | Diagnostics |

### What triggers sounds

- **Animations and effects.** Most gameplay sounds are attached to animations and effects that
  are defined in the content data; playing the effect plays its sound.
- **Music cues.** Background music is a set of named cues that are switched on and off. Client
  scripts use `SOUND:ActivateNDAudioMusicCue`, `DeactivateNDAudioMusicCue`, and
  `FlashNDAudioMusicCue`, and objects can do the same (`ActivateNDAudioMusicCue{...}`).
- **Emitters and sound triggers.** Objects can play 3D sound emitters (`PlayNDAudioEmitter`).
  Objects with a sound-trigger component (also a server-serialized component) play sounds when
  the player enters an area.
- **UI sounds** come from the `ui` project and are played by the movies.

For a server, sound needs little work: sounds follow from effects, animations, and components
it already sends. A server that sends a game message to play an emitter or music cue must use a
name or GUID that exists in the client's banks.

## Video

Movies are **Bink** files (`binkw32.dll`, version 1.9) in `res/Movies`:

| File | Content |
| --- | --- |
| `IntroCinematicCrash.bik` | Intro cinematic |
| `conversionvideo.bik`, `conversionvideo_de_de.bik` | Video shown for the free-trial conversion, with a German version |

Whether intro and new-character videos can be skipped is controlled by
`R_INTRO_VIDEO_SKIPPABLE` and `R_NEW_CHARACTER_VIDEO_SKIPPABLE`.

In-game cinematics are not video files. They are camera paths and scripted scenes rendered by
the engine (`PlayCinematic`, `EndCinematic`, `cinematicbars.gfx`), with sound from the
`cinematics` event project.
