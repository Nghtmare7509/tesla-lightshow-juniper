---
name: tesla-light-show
description: Analyze a .wav audio file and generate a Tesla custom light show (.fseq) that the Tesla Toybox Light Show app can play. Use this skill when the user wants to turn a song into a Tesla light show, create or design an .fseq for their Tesla, choreograph lights/closures to music, or asks about generating Tesla xLights sequences from music. Supports Model 3 (incl. Highland), Model S, Model X, Model Y (incl. 2025+ Juniper with front and rear light bars), and Cybertruck with model-specific optimization (boolean vs ramping channels, Falcon Doors / Front Doors on Model X, per-LED light bars on Cybertruck, verified Model Y Juniper light-bar channels, 200-channel extended output).
---

# Tesla Light Show Generator

Turn any `.wav` file into a compelling, model-tailored Tesla custom light show. The output is a validator-clean FSEQ v2.0 uncompressed binary (`.fseq`) paired with the original audio, ready to put in a `LightShow/` folder on a USB drive.

## Inputs and model selection

The skill needs two things:

1. **A path to a `.wav` file** (must be 44.1 kHz — warn the user if it is not; output will still be written but may drift on the vehicle).
2. **The Tesla model.** If the user didn't state it in the prompt, ask which of these they have — **do not guess**:
   - `Model 3` (pre-2024, no interior accent lights)
   - `Model 3 Highland` (2024+ refresh, has interior accent lights)
   - `Model S`
   - `Model X`
   - `Model Y` (2020–2024, no light bars)
   - `Model Y Juniper` (2025+ refresh, front and rear light bars)
   - `Cybertruck`

Accept natural variations ("cybertruck", "model s 2022", "3", "Y", "x", "plaid x", "highland", "2024 model 3", "new model 3", "juniper", "new model y", "2025 model y", "model y with light bar", etc.) and map them to the seven values. If the user just says "Model Y", ask whether it's the 2025+ refresh with light bars across the front and rear — the answer changes the output.

**About Model Y Juniper**: the 2025+ refresh added a full-width front light bar and a full-width rear light bar. Its channel map was verified on the owner's car (Oct 2026): front light bar centre = ch 11 or 12 (whole bar as one unit, ramps/fades); outer sections of the front bar = ch 7/8; **rear light bar = ch 25** (the channel Tesla labels "Brake"); rear brake lamps = ch 26/27 (labelled "Tail"); interior ambient/dash RGB = ch 176–193 (works; colours and fades OK). Dead on Juniper: ch 5, 6, 9, 10, 15–20, 29 — the composer folds their roles into live channels. Channels 47–162 (Cybertruck per-LED bars) do nothing on Juniper. The rear touchscreen cannot be controlled by a light show. The bars are whole units, not per-LED, so the composer animates them as segments (front outer → front centre → brake lamps → rear bar sweeps). Output is 200 channels (exterior channels 1–30 were confirmed to work in a 200-channel file).

**About Model 3 Highland**: the 2024+ refresh added a five-segment interior LED accent strip (left front, center front, right front, left rear, right rear) plus keeps the full-RGB center front display. We unlock these with the `model_3_highland` compose target which generates a 200-channel show. A 200-channel Highland show still plays on older Model 3s — the firmware simply ignores the channels the car's hardware doesn't have, so it's fully backward-compatible.

## What the skill produces

For each song it produces two files in the user's current directory (or an `output/` subdir, ask if unclear):

- `<basename>.fseq` — the binary light-show sequence.
- `<basename>.wav` — a copy of the audio (Tesla requires a filename-matched audio file to live in the same directory).

The `.fseq` has:

- Magic bytes `PSEQ`, version 2.0, uncompressed.
- Frame rate 50 fps (step time 20 ms).
- **48 channels** for Model 3 / S / X / Y (pre-Juniper) shows.
- **200 channels** for Cybertruck (front/rear light bars, offroad bar, interior RGB), Model Y Juniper (interior RGB; its light bars live on standard channels 7/8, 11/12 and 25) and Model 3 Highland (interior RGB) shows.
- Duration exactly matching the source audio, clipped to 4 h max.

The bundled validator `scripts/validate_fseq.py` (same checks as Tesla's official validator) MUST accept the output (channel count 48 or 200, compression 0, frames × step ≤ 4 h).

## How to generate a show

Work in the user's chosen output directory. The scripts live in this skill's `scripts/` folder — below, `<skill-dir>` means the directory that contains this SKILL.md (use its absolute path). Requires Python 3 with numpy.

### Step 1 — analyze the audio

```bash
python3 <skill-dir>/scripts/analyze_audio.py <path/to/song.wav> /tmp/<basename>.json
```

This writes a JSON timeline sampled at 20 ms. The analyzer is
**stereo-aware** — it preserves L/R all the way through the FFT and
extracts features that depend on the stereo field (panning, width,
mid/side). That lets the composer do things like "fire the right-side
markers because the hi-hats are panned right in this bar".

Features emitted (all arrays are 0..1 unless noted; one value per 20 ms frame):

- **Energy (global)**: `rms`, `bass` (20–200 Hz), `low_mid` (200–800), `mid` (800–3200), `high` (3200+), `mel[32]` (log-spaced)
- **Energy (per-section)**: `rms_local`, `bass_local`, `mid_local`, `high_local` — re-normalised within each detected section so quiet verses preserve their own dynamic range
- **Mid/Side**: `mid_energy`, `side_energy`, `stereo_width` (0 = mono, 1 = fully wide)
- **Panning** (−1 = hard left, +1 = hard right): `pan_bass`, `pan_mid`, `pan_high`, `pan_overall`
- **HPSS**: `perc_rms`, `perc_onset`, `harm_rms`
- **Broadband**: `onset`, `brightness`
- **Chroma / harmony**: `chroma[12]`, `key_tonic` (0..11), `key_mode` (0=minor, 1=major)
- **Beats + downbeats**: `beat_frames`, `beat_confidence` (0.7..2.5), `downbeat_frames`, `strong_beat_frames`, `tempo_bpm`, `meter` (3 or 4), `beat_agreement_pct`
- **Structure**: `segments` — list of `{"start", "end", "label", "energy", "index"}` with labels intro/verse/chorus/bridge/outro
- **Drops**: `drop_frames`
- **Metadata**: `analyzer_stack` — list of libraries in use (e.g. `["librosa", "madmom"]`)

#### Optional libraries (auto-detected)

The analyzer works with pure numpy but uses three optional libraries
when they're installed. Install any or all for a quality boost:

```bash
pip3 install librosa      # chroma, CQT, segmentation, fallback beat tracker
pip3 install madmom       # excellent beat + downbeat tracker
pip3 install scipy        # faster HPSS (pure-numpy fallback exists)
```

**librosa + madmom cross-check**: when both are installed, the
analyzer runs both beat trackers and cross-checks. Beats confirmed by
both (±40 ms) get confidence 2.0, madmom-only beats get 1.0,
librosa-only get 0.7, and any beat that coincides with a strong
percussive onset gets a further +0.5 bonus. This means the composer
can gate its biggest hits on high-confidence beats only — the
`strong_beat_frames` list is derived from real downbeats (madmom) when
available, not "every 4th beat" guesses.

**Structural segmentation**: uses librosa's self-similarity + agglomerative
clustering on a chroma+MFCC feature stack. Segment count adapts to
song length (3–5 for short, 4–7 for medium, 5–9 for long). Labels are
inferred heuristically: low-energy first/last segments become intro/outro,
the highest-energy segments become choruses, medium segments between
choruses become bridges, and the rest are verses. The composer uses
the detected sections to place the narrative arc — the climax now
lands on the song's actual highest-energy chorus instead of at a fixed
55–85% time window.

All three libraries are permissive / OSI-approved licences
(BSD / ISC / MIT-equivalent) — free for any use.

### Step 2 — compose the show

```bash
python3 <skill-dir>/scripts/compose_show.py --analysis /tmp/<basename>.json \
  --model {model_3|model_3_highland|model_s|model_x|model_y|model_y_juniper|cybertruck} --out <basename>.fseq
```

Normalize the model argument to one of: `model_3`, `model_3_highland`, `model_s`, `model_x`, `model_y`, `model_y_juniper`, `cybertruck`.

The composer binds audio features to model-appropriate channels (see `references/model_capabilities.md` and `references/channel_map.md`). It respects closure actuation limits and pre-opens liftgates/charge ports in time for dances at drops.

### Step 3 — copy the wav next to the fseq

Tesla requires the audio file next to the .fseq with the **same basename**. Either copy, symlink, or tell the user to do so — default: copy.

```bash
cp <path/to/song.wav> <basename>.wav
```

### Step 4 — validate

```bash
python3 <skill-dir>/scripts/validate_fseq.py <basename>.fseq
```

It never prompts for input. Exit code 0 and a line starting `OK Found <N> frames, step time of 20 ms …` means the file is valid. Exit code 1 and a line containing `INVALID` (e.g. `Expected 48 or 200 channels, got <X>`, `Expected file format to be V2 Uncompressed`) means it will not play on the vehicle — **fix it before declaring success.**

### Step 5 — report

Tell the user:
- Where the files are
- Duration, tempo, channel count
- For Model Y Juniper: tip to start the show from the car touchscreen (front lights may not respond when started from the phone app)
- A short written description of the choreography highlights (which lights fire on which musical features — they will appreciate the intent)
- How to install: put both files under a `LightShow/` folder on a FAT32/exFAT USB drive (not NTFS, no `TeslaCam/` folder), then Toybox → Light Show → Schedule Show.

## Channel binding rules (summary)

Full tables are in `references/channel_map.md` and `references/model_capabilities.md`. Quick reference for composition:

- **Kick / bass-heavy beats** (detected via `perc_onset` + `bass >= mid`) → Main beams (outer + inner), front turn signals, all Ch4-6 simultaneously, brake lights, Cybertruck bed lights. On climax kicks also: license + reverse.
- **Snare / mid-heavy beats** → Signature, Channels 4-6, rear turn signals, front fog (non-CT), tail lights. Model X adds rear fog.
- **Hi-hats / high-band onsets** → Side markers + side repeaters. **Stereo-aware**: `pan_high < -0.15` → left side only; `> +0.15` → right side only; near-center → both. Both-side in climax also lights license + aux park.
- **Stereo opening moments** — jumps in `side_energy` or `stereo_width` above a 3 s baseline → brief fog + aux park wash (mimics a reverb tail or strings spreading out).
- **Sustained loudness (RMS)** → Interior RGB wash (CT only in 200-ch), Cybertruck light bar brightness envelope.
- **Climax peak** (guaranteed — loudest sustained 2 s in 55–85% of track, independent of drop detection) → Liftgate opens 14 s before, mirror 3-flap, charge port Dance (rainbow), full-front blast, model-specific reveal (S door handles / X falcon + front doors).
- **Audio-detected drops outside climax** → Mini front-light blast, no closures (stays subordinate to the climax).
- **Brightness / spectral centroid** → Hue mapping for interior RGB (warm when dark, cool when bright).
- **Yellow blinker layer** — front turn signals alternate L↔R on 2× beat subdivisions in build, 4× in climax (the signature "yellow blinker" pattern).
- **Narrative arc** — intro (0–15%) soft outer-beam ramps only; build (15–55%) every-other-beat; climax (55–85%) full density; outro (85–100%) long 2 s breathing ramps.
- Use ramping variants (70/80/90%) on Model 3 / Y / Cybertruck where smooth fades read better than boolean snaps.

## Model-specific reminders

- **Model 3 / Model Y** — exploit the ramping on Front Turn, Signature, and Channels 4-6. Prefer ramp_pulse over instant pulses for anything lasting > 200 ms. Aux Park / Side Markers are OR'd together — don't stack them continuously or they won't appear to flash.
- **Model Y Juniper (2025+)** — everything in the Model 3 / Model Y bullet applies, with the verified mapping above: rear light bar on beats via ch 25, brake lamps via 26/27, centre front bar via 11/12 (ramping), front bar outer sections via 7/8. Climax = front-to-back segment sweep then both bars held lit with the centre bar fading up; secondary drops = quick front-to-back sweep. Dead channels (5, 6, 9, 10, 15–20, 29) are remapped: signature→11/12, ch5→7/8, fog→3/4, aux park + side markers→side repeaters 21/22, rear fog→licence 30. Interior RGB 176–193 kept near full brightness (ambient strips read dim on the car).
- **Model 3 Highland (2024+)** — same exterior behaviour as Model 3 (the two are byte-identical for channels 1–46) but the composer also writes channels 176–193 (the six interior RGB surfaces) with chroma-driven colour. Hue follows the dominant pitch class relative to the song's detected key; saturation follows HPSS harmonic richness with a 0.7 floor so the palette stays visually intense; value follows RMS with a 0.35 floor during harmonic content. Minor keys shift the hue wheel ~0.08 toward warmer. Each of the six surfaces gets a small per-surface hue offset so colours spatial-gradient across the cabin. The show is 200 channels but the extra bytes are all zero outside the RGB range, so it plays fine on older Model 3s too.
- **Model S** — Signature and Front Turn are boolean only; use crisp hits. Door Handles (4 independent) are a unique accent — pop them 1.2 s before a drop and close 0.5 s after for a cool reveal. 20-actuation budget is generous. No Falcon or Front Doors.
- **Model X** — Same boolean headlights as Model S (no ramping on Signature / Front Turn) but with **Falcon Doors** and **Front Doors** for the most dramatic choreography of any car. Falcon Doors open in ~20 s and close in ~8 s; Front Doors open in ~22 s and close in ~3 s — schedule Opens **~25 s before a drop** so doors are fully open for the Dance/Close beat. Only **6 actuations** each per show, use them for headline moments. Model X also has **Rear Fog (even in NA)** — an extra accent channel the other US cars don't have. No Door Handles (those are S-only).
- **Cybertruck** — Generate 200-channel output. Animate the front/rear light bars (curtain, chase, bars, full styles). Brake + Rear Turn are full-brightness controlled: drive them with the RMS envelope instead of 0/100 values. Bed Lights always ramp 500 ms regardless of request.
- **Cybertruck closures** — Liftgate is mapped to Powered Frunk; Aux Park is mapped to Frunk Light; Rear Turn Signals are disabled on the car (leave the xLights channels 0). The 48→200 mapping happens in the composer automatically.

## Constraints the output must satisfy

- Channel count: exactly 48 or 200 (`scripts/validate_fseq.py` and Tesla's validator reject otherwise).
- Compression type byte: 0 (uncompressed).
- Max duration: 4 h. Longer audio should be truncated or the user should trim.
- Sample rate: 44.1 kHz. Warn if not.
- Frame interval: 20 ms (supported: 15–100 ms, but 20 ms is every example and recommended).
- Closure actuation limits per show (count only Open/Close/Dance):
  - Liftgate / Frunk ≤ 6, Mirrors ≤ 20, Charge Port ≤ 3, Windows ≤ 6, Door Handles (S) ≤ 20, Front Doors (X) ≤ 6, Falcon Doors (X) ≤ 6.
  - Total dance time ≤ ~30 s per show (thermal).
- Dance only works when a closure is already open — schedule an Open earlier and leave time per `references/channel_map.md` (Closure Movement Durations).
- Don't close windows during the show — music would be muffled.

## If something breaks

- **Validator rejects channel count** → ensure the writer uses 48 for Model 3 / S / X / Y and 200 for Cybertruck, Model Y Juniper and Model 3 Highland. No other value is accepted.
- **Juniper light bars stay dark** → check the show was started from the car touchscreen (not the phone app), that the files have short lowercase names, and reboot the screen if a show was interrupted. The verified map is: rear bar ch 25, centre front bar ch 11/12, front outer 7/8.
- **Validator rejects compression** → header byte at offset 20 must be 0.
- **Validator rejects duration** → clip the audio or reduce frame count.
- **Show plays but a specific light is stuck on** → check the Aux Park / Side Marker OR'ing rules (a single channel staying on keeps the group lit).
- **Dance did nothing** → the closure wasn't open before Dance was commanded. Insert an Open at least (durations in closure table) before the Dance effect.

## Files in this skill

- `SKILL.md` — this file.
- `scripts/analyze_audio.py` — audio feature extractor (numpy preferred; pure-Python fallback).
- `scripts/fseq_writer.py` — minimal FSEQ v2.0 uncompressed writer + level/command constants.
- `scripts/compose_show.py` — binds audio features to Tesla channels per model and writes the .fseq.
- `scripts/validate_fseq.py` — non-interactive validator with the same checks as Tesla's official one.
- `references/channel_map.md` — complete 48/200 channel layout, brightness byte table, closure command bytes.
- `references/model_capabilities.md` — per-model capability matrix and production recipes.
- `references/fseq_format.md` — binary layout of the FSEQ v2.0 uncompressed header.
