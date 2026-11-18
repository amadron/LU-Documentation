# Client rendering

[Client overview](./README.md) | [User interface](./Client%20User%20Interface.md) | [Assets](./Client%20Assets%20and%20Content%20Data.md)

## Engine and graphics API

The client renders with **Gamebryo 2.3** (Emergent Game Technologies) on **Direct3D 9**, using
the D3DX9 helper library (`d3dx9_34.dll`). Gamebryo provides the scene graph, the model format
(`.nif`), skinned animation (`.kf`, `.kfm`), and the material system. The executable contains
Gamebryo's shader fragments and targets for shader models 1.1 to 3.0 (`vs_1_1`, `vs_2_0`,
`vs_3_0`, `ps_2_0`, `ps_3_0`), so the game runs on Shader Model 2.0 hardware and uses more
effects where Shader Model 3.0 is available.

Gamebryo scene-graph classes present in the executable include `NiSceneGraphComponent`,
`NiTransformationComponent`, `NiCameraComponent`, `NiLightComponent`, `NiActorComponent`, and
`NiShadowGeneratorComponent`.

## What is drawn

| Content | Source files | Notes |
| --- | --- | --- |
| Static and dynamic objects | `res/mesh/**/*.nif` (about 10,000) with `.dds` textures | Loaded by an object's render component; the asset path comes from `cdclient.fdb` (`RenderComponent` table) |
| Minifigures | Shared minifigure meshes plus decal textures for torso, legs, and face | Colors and decals come from the character data the server sends |
| Brick-built models | Built at run time from `.lxfml` brick lists and the brick primitives in `res/brickprimitives` | See [Physics and building](./Client%20Physics%20and%20Building.md) |
| Terrain | `res/maps/**/*.raw` height maps with blend textures | One terrain per zone |
| Sky | `skydome` shader; per-zone sky set by the level or by scripts (`LEVEL:SetSkyDome`) | |
| Water, lava, ice | Dedicated shaders `ocean`, `lake`, `river`, `brickwater`, `lava` | |
| Particles | `res/forkp/effects` (`.psb` particle systems, about 11,000) | Triggered by effects (`PlayFXEffect`) |
| Text above heads | `headicon` shader, `looticonnamebillboard.gfx` | Names, icons, chat bubbles |
| 3D UI surfaces | Scaleform movies rendered onto models (`res/ui/3d`, `tvscreen` shader) | Scoreboards, signs, the LUP station TV |

## Shaders

The compiled effect files in `res/shaders` (`.fxo`, with shared includes `.fxp`) are:

| Group | Files |
| --- | --- |
| LEGO plastic lighting (main material) | `legopplighting`, `legopplighting_low`, `legopplighting_noenv`, `legopplighting_noenv_nospec`, `legopplighting_item*`, `legopplighting_frontend`, shared `legoppcommon.fxp` |
| Special materials | `clearplastic`, `metallic`, `alphaasalpha`, `powerups`, `flair` |
| Environment | `terraindiffuse`, `skydome`, `vertexfog`, `ocean`, `lake`, `river`, `brickwater`, `lava`, `water_jbrown` |
| Effects | `particles`, `textureproject` (projected decals, e.g. selection rings), `shadowbake`, `headicon`, `tvscreen` |
| Full-screen | `fullscreeneffects`, `postprocessingshaders`, `hdrscene` |
| Shared code | `basicshaders`, `common.fxp` |

The `_low`, `_noenv`, and `_nospec` variants are lower-quality versions selected by the shader
quality settings. `flair` is the shiny highlight on special items and is switched by
`R_FLAIR_ON`.

## Quality and performance settings

The graphics options are stored as `R_...` keys (see
[configuration](./Client%20Architecture%20and%20Startup.md#lwocfgdefault-and-player-settings)).
Meanings are inferred from the key names and the option menu (`optionsmenu.gfx`):

| Area | Keys |
| --- | --- |
| Shader quality | `R_LEGO_SHADER_QUALITY`, `R_TERRAIN_SHADER_QUALITY`, `R_SHADER_RADII0`, `R_SHADER_RADII1` (distances at which objects switch to cheaper shaders: 750 and 1,500 units) |
| Shadows | `R_CAST_SHADOW`, `R_CAST_SHADOW_TERRAIN_ONLY`, `R_CAST_CHEAP_SHADOW`, `R_USE_DYNAMIC_SHADOW`, `R_SHADOWMAPPING_RES`, `R_DYNAMIC_SHADOW_NOISE_SCALAR` |
| Level of detail | `R_LOD_DISTANCE_SKEW`, `R_RENDER_COMPONENT_LOD`, `R_TERRAIN_MESH_DETAIL_ADJUSTMENT`, `R_MINIFIG_TEXTURE_LOD`, `TEXRES` |
| Animation LOD | `R_ANIM_LOD`, `R_MID_ANIM_LOD_DIS`/`_SKIP`, `R_FAR_ANIM_LOD_DIS`/`_SKIP` (animate distant characters less often) |
| Impostors | `R_IMPOSTERS`, `R_IMPOSTER_NEAR`, `R_IMPOSTER_FAR` (flat stand-ins for distant objects) |
| Particles and effects | `R_PARTICLES_ON`, `R_PARTICLES_PRIO`, `R_PARTICLES_NUMBUFF`, `R_EFFECTS`, `R_MAXSMASHBRICKS` |
| Full-screen effects | `HDR`, `R_BLUR`, `R_CLUT` (color look-up tables, also set by scripts with `LEVEL:CLUTEffect`), `R_FADE`, `R_OVERLAY` |
| UI | `UI_AA`, `R_UILOWRES`, `R_HIRESGAMESIGNS` |
| View range | `VIEW_RANGE_MINMAX_SLIDER`, `S_GHOSTING_RADIUS_SCALAR` |

The client warns about low frame rates with `frameratewarning.gfx`,
`performancewarningself.gfx`, and `performancewarningother.gfx`.

## What the server influences

Rendering is local, but much of what is drawn is decided by the server:

- **Which objects exist.** The client only draws objects the server has constructed for it.
  The server limits these by distance ("ghosting"), so the visible range depends on the server's
  ghosting distance as well as on the client's view-range setting.
- **Appearance state.** The serialized render component carries the effects currently playing
  on an object. Game messages start and stop effects (`PlayFXEffect`, `StopFXEffect`), play
  animations (`PlayAnimation`), change visibility, and attach render effects.
- **Environment.** Lights, sky, fog, and color grading come from the zone files and can be
  changed by client scripts in response to server events (`LEVEL:SetLights`,
  `LEVEL:SetSkyDome`, `LEVEL:ModifyEnvironmentSettings`, `LEVEL:FadeEffect`).

A server must use effect IDs, animation names, and LOTs that exist in the client's data. Unknown
IDs are not drawn; they do not need to be sent as assets.
