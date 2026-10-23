# Tesla Model-Specific Capabilities

Source: Tesla Light Show xLights Guide (`light-show/README.md`) and the reference `xlights_rgbeffects.xml`.

## Summary Table

| Capability                     | Model 3           | Model S (2021+)        | Model X (2021+)        | Model Y            | Cybertruck                         |
|--------------------------------|-------------------|------------------------|------------------------|--------------------|-------------------------------------|
| Outer Main Beam ramping        | reflector only    | reflector only         | reflector only         | reflector only     | Yes                                 |
| Inner Main Beam ramping        | Yes               | Yes                    | Yes                    | Yes                | Yes                                 |
| Signature                      | Ramping           | Boolean                | Boolean                | Ramping            | —                                   |
| Channels 4-6 ramping           | Yes (merged into one output; Ch4 leads) | Yes (indep L/R; Ch4 sets ramp for all 3) | Yes (same as S) | Yes (merged; Ch4 leads) | — |
| Front Turn                     | Ramping           | Boolean                | Boolean                | Ramping            | Ramping                             |
| Front Side Markers             | Boolean           | Boolean                | Boolean                | Boolean            | Ramping                             |
| Front Fog                      | Yes (not on 3 SR+)| Yes                    | Yes                    | Yes                | —                                   |
| Aux Park                       | Yes (not on 3 SR+)| Yes (indep L/R shared w/ marker) | Yes (same as S) | Yes (shared all-4 OR) | Used as **Frunk Light**          |
| Side Marker / Aux Park coupling| L/R OR'd together | L/R independent, marker+park OR'd per side | same as S | all-4 OR'd together | — |
| Side Repeaters                 | Boolean           | Boolean                | Boolean                | Boolean            | Repurposed as Rear Side Markers     |
| Rear Turn                      | Boolean           | Boolean                | Boolean                | Boolean            | **Full Brightness Control**         |
| Brake Lights                   | Boolean           | Boolean                | Boolean                | Boolean            | **Full Brightness Control**         |
| Tail Lights                    | Boolean (pre-Oct 2020 merged L/R/plate) | Boolean | Boolean | Boolean | Used as Reverse Lights (L/R)   |
| Reverse Lights                 | Boolean           | Boolean                | Boolean                | Boolean            | Used as Bed Lights (500 ms fixed ramp) |
| Rear Fog                       | Only non-NA       | Only non-NA            | Yes (including NA)     | Only non-NA        | —                                   |
| License Plate                  | Boolean (merged with tails pre-Oct 2020) | Boolean | Boolean | Boolean | Boolean                   |
| Front Light Bar (60 LEDs)      | —                 | —                      | —                      | Juniper: whole bar on ch 11/12 (centre, ramping) + 7/8 (outer) | **Yes (full brightness per LED)**   |
| Rear Light Bar (52 LEDs on bed door) | —            | —                      | —                      | Juniper: whole bar on ch 25 (boolean) | **Yes (full brightness per LED)**   |
| Offroad Light Bar (6 segs)     | —                 | —                      | —                      | —                  | Optional (full brightness per seg)  |
| Liftgate                       | Only power-liftgate trims | Yes            | Yes                    | Only power-liftgate trims | Yes (mapped from Liftgate → Frunk) |
| Mirrors                        | Yes               | Yes                    | Yes                    | Yes                | Yes                                 |
| Charge Port (dance=rainbow)    | Yes               | Yes                    | Yes                    | Yes                | Yes                                 |
| Windows                        | Yes               | Yes                    | Yes                    | Yes                | Yes                                 |
| Door Handles                   | —                 | Yes (4 indep)          | —                      | —                  | —                                   |
| Front Doors                    | —                 | —                      | Yes (20 s open)        | —                  | —                                   |
| Falcon Doors                   | —                 | —                      | Yes (20 s open)        | —                  | —                                   |
| Center Front Display RGB       | Yes               | Yes                    | Yes                    | Yes                | Yes                                 |
| Interior Accent RGB (5 segs)   | Only if equipped  | Only if equipped       | Only if equipped       | Only if equipped   | Yes                                 |

## Per-Model Production Recipes

### Model 3 / Model Y

Default headlight behavior: **fully ramping on every front light**. Lean into smooth fades and sweeping brightness curves — they look much more polished than boolean blinks on these cars.

Best creative channels:
- Outer/Inner Main Beam, Signature, Front Turn, Channels 4-6 → all smooth ramping
- Brake + Tail + Reverse → punchy boolean beats (back of car)
- Charge Port dance → rainbow accent
- Center Front Display RGB → full-color cabin wash (very visible from outside)

Constraints:
- Only 1 aux park / side marker group (OR'd across all 4). Use sparsely as a single "front accent" channel.
- Channel 4 is the ramp-duration leader for the merged ch4-6 output; the skill's writer does this automatically.
- Liftgate is only controllable on power-liftgate trims — treat as optional.

Recommend **48-channel** output for Model 3/Y.

### Model Y Juniper (2025+ refresh)

Exterior headlight, turn-signal and closure behaviour is the same as the regular Model Y (ramping Signature, Front Turn and Channels 4–6). The refresh adds:

- A full-width **front light bar** between the headlights.
- A full-width **rear (tail) light bar** across the liftgate.

Tesla's official xLights guide only documents light bars for Cybertruck. The mapping below was **verified on the owner's 2025+ Model Y (Oct 2026)** with isolated channel tests, and agrees with teslamotors/light-show issue #183 for the front bar:

| Ch | Tesla label | What it actually drives on Juniper |
|----|-------------|------------------------------------|
| 3/4 | Inner main beam | Lower white front lamps |
| 7/8 | Channel 4 L/R | Outer sections of the front light bar |
| 11/12 | Channel 6 L/R | Centre front light bar — either channel lights the whole centre; fades/ramps work |
| 13/14 | Front turn | Amber front lamps |
| 21/22 | Side repeater | Side repeaters (on the front fenders) |
| 25 | Brake | **Rear light bar** |
| 26/27 | Tail L/R | Rear brake lamps |
| 176–193 | Interior RGB | Ambient/dash strip + centre display (colours, fades work; appears dim) |
| 5, 6, 9, 10, 15–20, 29 | — | No visible effect |
| 47–162 | CT light bars | No effect (Juniper bars are not per-LED) |

The rear touchscreen does not respond to any channel tested (176–200, 107–110, 163–174).

Composer behaviour for `model_y_juniper`:
- 200 channels; exterior channels 1–30 work in a 200-channel file (verified).
- Rear bar (25) and brake lamps (26/27) flash on beats; centre front bar (11/12) and outer bar (7/8) follow the Channel 4–6 beat logic.
- Climax: front-to-back segment sweep (7/8 → 11/12 → 26/27 → 25), then both bars held lit for ~4.5 s with the centre bar on a 2 s fade-up and the rear bar pulsing on beats.
- Secondary drops: 1.2 s front-to-back sweep.
- Dead channels are folded into live ones (signature→11/12, ch5→7/8, fog→3/4, aux park + markers→21/22, rear fog→30) and zeroed.
- Interior RGB kept at 0.75–1.0 brightness.

Recommend **200-channel** output for Model Y Juniper.

### Model 3 Highland (2024+ refresh)

Exterior hardware is identical to the regular Model 3 — headlights ramp, turn signals ramp, same channel layout. The difference is the **interior**:

- **Center Front Display RGB** (always had this, even pre-refresh)
- **Five-segment interior accent LED strip** added with the Highland refresh:
  - Center Front (dashboard)
  - Left Front (driver's door)
  - Right Front (passenger's door)
  - Left Rear (rear driver's side)
  - Right Rear (rear passenger's side)

All six surfaces are full RGB. They sit on FSEQ channels 176–193 (six 3-byte groups), which means the show needs to be written as a **200-channel** file.

Composer behaviour for `model_3_highland`:
- Channels 1–46: byte-identical to a `model_3` show (same exterior choreography).
- Channels 47–175: all zero (these are Cybertruck-only hardware).
- Channels 176–193: driven by `_chroma_rgb_layer` — hue from chroma, saturation from HPSS harmonic richness, value from RMS, with a small per-surface hue offset so colour spatial-gradients across the cabin.
- Channels 194–200: all zero (reserved).

**Backward compatible:** a 200-channel Highland show plays on any pre-refresh Model 3 — the firmware ignores the channels the hardware doesn't have. So if you share a Highland show with a friend who has an older car, it still works.

Recommend **200-channel** output for Model 3 Highland.

### Model S

Signature and Front Turn are **boolean only** on Model S — so give them crisp on-beat blinks rather than fades. Ramping is still available for Main Beams and Ch 4-6.

Best creative channels:
- Inner/Outer Main Beam → ramping fades
- Channels 4-6 → tight boolean strobe patterns, with Ch 4 setting the global ramp duration per group
- Signature/Front Turn → hard on-beat hits
- Brake + Tail + Reverse → rear groove
- Door Handles (4 independent) can 'appear' before a drop (20 actuations = plenty for 4 handles)

Constraints:
- Aux Park + Side Marker are OR'd together per side. Leaving even one of the pair on prevents a visible flash.
- No Falcon/Front Doors (those are X-only). No Rear Fog in NA.

Recommend **48-channel** output for Model S.

### Model X

Boolean Signature/Front Turn like Model S, but the star of the Model X show is the **closure choreography**.

Best creative channels:
- Inner/Outer Main Beam → ramping fades
- Channels 4-6 → tight strobe patterns, Ch 4 leads
- Signature/Front Turn → hard on-beat hits
- Brake + Tail + Reverse + **Rear Fog (available even in NA)** → extra rear accent the other cars lack
- **Falcon Doors** → open ~25 s before a big drop, Dance through the first ~6 s of chorus, then Close
- **Front Doors** → open ~25 s before a big drop, Close ~6 s after (no Dance on front doors — use Open/Close)
- Charge Port dance → rainbow accent

Constraints:
- No Door Handles (those are S-only).
- Aux Park + Side Marker OR'd together per side like on Model S.
- Falcon Doors: 20 s open / 8 s close, limit 6 actuations, supports Dance.
- Front Doors: 22 s open / 3 s close, limit 6 actuations, **does not support Dance** — use Open + Close only.
- Moving Windows during Model X door movement can cause false pinch detections that stop the show — **avoid window movement while doors are opening or closing.**
- Plan the whole show around 1–2 major door moments; budget everything else around them.

Recommend **48-channel** output for Model X.

### Cybertruck

Cybertruck unlocks the most creative hardware:
- **Front Light Bar (60 LEDs)** with per-LED full brightness control → integrated xLights effects (Curtain, Bars, Marble, Morph, On) translate to striking sweeps. We emulate these effects in the writer.
- **Rear Light Bar (52 LEDs)** on the bed door → same effect potential, rear-facing.
- **Offroad Light Bar (6 segs)** → sharp accent bars if equipped.
- **Brake & Rear Turn full brightness** → use continuous intensity curves driven by the music envelope, not just on/off.
- Powered Frunk "liftgate" position → dramatic open on big drops (long 14 s open time, plan ahead).
- **Bed Lights** always ramp 500 ms no matter what; commands shorter than that just come out as half-lit pulses.

We must **generate a 200-channel show** to use the light bars and interior RGB. Put big sweeping light-bar effects on the drops and chorus; keep verses sparse so the contrast is felt.

### Universal rules

- Frame interval: **20 ms** (xLights FPS = 50). Any value 15–100 ms is legal but 20 ms matches every example and is recommended.
- Max duration: 4 hours.
- Sample rate: audio must be 44.1 kHz.
- File must be FSEQ v2.0 **uncompressed** (compression_type byte = 0).
- Channel count must be exactly 48 or 200 (the validator refuses anything else).
