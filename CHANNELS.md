# Model Y Juniper (2025+) light show channel guide

A full list of every channel in a Tesla light show file (`.fseq`) and what it does on a 2025+ Model Y "Juniper". Channel numbers start at 1, the same as in xLights.

**Status key**

- ✅ **Verified**: tested on a real Model Y Juniper (Oct 2026) and responded.
- ❌ **No effect**: tested on a real Juniper and nothing happened.
- 📘 **Tesla docs**: not tested on a Juniper. The behaviour comes from Tesla's official [light-show guide](https://github.com/teslamotors/light-show).

The "Tesla label" column is the name Tesla's xLights layout uses. On the Juniper some labels don't match what actually lights up, so read the "What it does on Juniper" column.

---

## Lights: front (channels 1–20)

| Ch | Tesla label | What it does on Juniper | Fades? | Status |
|----|-------------|-------------------------|--------|--------|
| 1 | Left Outer Main Beam | Left headlight (main beam) | Yes | ✅ Verified |
| 2 | Right Outer Main Beam | Right headlight (main beam) | Yes | ✅ Verified |
| 3 | Left Inner Main Beam | Left lower white front lamp | Yes | ✅ Verified |
| 4 | Right Inner Main Beam | Right lower white front lamp | Yes | ✅ Verified |
| 5 | Left Signature | Nothing | — | ❌ No effect |
| 6 | Right Signature | Nothing | — | ❌ No effect |
| 7 | Left Channel 4 | **Front light bar, outer section** | Yes | ✅ Verified |
| 8 | Right Channel 4 | **Front light bar, outer section** | Yes | ✅ Verified |
| 9 | Left Channel 5 | Nothing | — | ❌ No effect |
| 10 | Right Channel 5 | Nothing | — | ❌ No effect |
| 11 | Left Channel 6 | **Front light bar, whole centre section** | Yes | ✅ Verified |
| 12 | Right Channel 6 | **Front light bar, whole centre section** (same as 11) | Yes | ✅ Verified |
| 13 | Left Front Turn | Left amber front turn signal | Yes | ✅ Verified |
| 14 | Right Front Turn | Right amber front turn signal | Yes | ✅ Verified |
| 15 | Left Front Fog | Nothing | — | ❌ No effect |
| 16 | Right Front Fog | Nothing | — | ❌ No effect |
| 17 | Left Aux Park | Nothing | — | ❌ No effect |
| 18 | Right Aux Park | Nothing | — | ❌ No effect |
| 19 | Left Side Marker | Nothing | — | ❌ No effect |
| 20 | Right Side Marker | Nothing | — | ❌ No effect |

**Light bar notes**

- The front bar is **not** controllable LED by LED. Channel 11 *or* 12 lights the whole centre section, and channels 7/8 light the outer ends.
- Channels 47–200 (except the interior colour lights below) do nothing on the Juniper.

## Lights: sides and rear (channels 21–30)

| Ch | Tesla label | What it does on Juniper | Fades? | Status |
|----|-------------|-------------------------|--------|--------|
| 21 | Left Side Repeater | Left side repeater (on the front fender) | No (on/off) | ✅ Verified |
| 22 | Right Side Repeater | Right side repeater (on the front fender) | No (on/off) | ✅ Verified |
| 23 | Left Rear Turn | Left rear turn signal | No (on/off) | ✅ Verified |
| 24 | Right Rear Turn | Right rear turn signal | No (on/off) | ✅ Verified |
| 25 | Brake Lights | **Rear light bar** (full width across the liftgate) | No (on/off) | ✅ Verified |
| 26 | Left Tail | **Rear brake lamps** | No (on/off) | ✅ Verified |
| 27 | Right Tail | **Rear brake lamps** | No (on/off) | ✅ Verified |
| 28 | Reverse Lights | Reverse lights | No (on/off) | ✅ Verified |
| 29 | Rear Fog Lights | Nothing (not fitted on North American cars) | — | ❌ No effect |
| 30 | License Plate | License plate light | No (on/off) | ✅ Verified |

**Heads up:** Tesla's labels for 25 and 26/27 are swapped on the Juniper. "Brake" (25) is the rear light bar, and "Tail" (26/27) is the brake lamps.

## Things that move (channels 35–41 and 46)

> **Turn on Dance Moves first.** Moving parts only move if the car's light show **Dance Moves** option is enabled. With it off, the car ignores every command below and plays only the lights.

These channels send **commands**, not brightness. Use only these four values:

| Value (byte) | xLights % | Command | What happens |
|--------------|-----------|---------|--------------|
| 64 | 25% | **Open** | Starts opening and stops when fully open |
| 128 | 50% | **Dance** | Wiggles back and forth (only works once it's already open) |
| 191 | 75% | **Close** | Starts closing and stops when fully closed |
| 255 | 100% | **Stop** | Stops immediately |
| 0 | 0% | Idle | No new command; lets a move already under way finish |

| Ch | Name | On Model Y Juniper | Time to move | Max moves per show | Status |
|----|------|--------------------|--------------|--------------------|--------|
| 35 | Left Mirror | **Close = fold in, Open = unfold** (normal driving position) | ~2 s | 20 | ✅ Verified |
| 36 | Right Mirror | **Close = fold in, Open = unfold** (normal driving position) | ~2 s | 20 | ✅ Verified |
| 37 | Left Front Window | Lowers / raises window (dance works from closed) | ~4 s | 6 per window | ✅ Verified |
| 38 | Left Rear Window | Lowers / raises window (dance works from closed) | ~4 s | 6 per window | ✅ Verified |
| 39 | Right Front Window | Lowers / raises window (dance works from closed) | ~4 s | 6 per window | ✅ Verified |
| 40 | Right Rear Window | Lowers / raises window (dance works from closed) | ~4 s | 6 per window | ✅ Verified |
| 41 | Liftgate | Opens / closes the power rear hatch; dances once open | ~14 s open, ~4 s close | 6 | ✅ Verified |
| 46 | Charge Port | Opens / closes the port door. **Dance makes the port LED cycle rainbow colours.** | ~2 s (auto-closes after ~2 min) | 3 | ✅ Verified |

**Rules for moving parts**

- Only Open, Close and Dance count toward the per-show limits. Each mirror and each window has its own count.
- **Dance needs the part to be open first.** Send Open early enough for it to finish (for example, open the liftgate about 15 s before you want it to dance). Windows are the exception and can dance from closed.
- Keep total dance time to about **30 s per show** or the car may stop the moves to protect the motors.
- Music plays only from the cabin speakers, so Tesla suggests leaving windows down during the show. Put them back up before it ends.
- Make sure there's room around the car before using the liftgate or mirrors.

## Interior colour lights (channels 176–193, 200-channel files only)

Each zone takes three channels in a row, **Red, Green, Blue** (0 = off, 255 = full). Mix them for any colour.

| Ch (R, G, B) | Tesla zone name | What it actually lights on Juniper | Status |
|--------------|-----------------|------------------------------------|--------|
| 176, 177, 178 | Centre front display | Centre screen colour | ✅ Verified |
| 185, 186, 187 | Centre front accent | Dash ambient strip | ✅ Verified |
| 182, 183, 184 | Right front | **Left front** door strip (driver) | ✅ Verified |
| 188, 189, 190 | Left front | **Right front** door strip (passenger) | ✅ Verified |
| 179, 180, 181 | Right rear | **Left rear** door strip | ✅ Verified |
| 191, 192, 193 | Left rear | **Right rear** door strip | ✅ Verified |

- **Heads up:** Tesla's left/right names for the four door zones are mirrored on the Juniper. Use the "What it actually lights" column.
- All six zones respond to single colours, mixed colours and smooth fades.
- The ambient strips look fairly **dim** even at full value. That's the car's limit, not the file's.
- The **rear touchscreen can't be controlled**. Nothing in 107–110, 163–174 or 176–200 changed it.

## Unused channels

Keep these at 0. They don't control anything on the Juniper:

- **31–34 and 42–45**: no matching hardware on Model Y.
- **47–174 and 194–200**: no effect. Each one was tested on its own for 4 s, watching the outside and the cabin. None of them light anything, and there's no per-LED control of the light bars or the ambient strips.
- **175**: not tested (it's the suspension channel on another model); leave it at 0.

---

## Brightness values for light channels

Every light channel takes a value from 0 to 255. On channels that **fade** (1–14 in the tables above), certain values also set the fade speed:

| Byte | xLights % | Fading channel | On/off channel |
|------|-----------|----------------|----------------|
| 0 | 0% | Off instantly | Off |
| 26 | 10% | Fade off over 0.5 s | Off |
| 51 | 20% | Fade off over 1 s | Off |
| 76 | 30% | Fade off over 2 s | Off |
| 178 | 70% | Fade on over 0.5 s | On |
| 204 | 80% | Fade on over 1 s | On |
| 230 | 90% | Fade on over 2 s | On |
| 255 | 100% | On instantly | On |

On on/off channels, any value of 128 or more means on.

## File basics

- **48 channels** covers all the exterior lights and moving parts. **200 channels** adds the interior colour lights. Both work on the Juniper, and the exterior lights behave the same in either.
- Use 20 ms frames (50 fps), FSEQ v2, uncompressed.
- Put the `.fseq` and a matching `.wav` or `.mp3` with the **same file name** in a `LightShow` folder on a FAT32 or exFAT USB drive.
- Start the show from the car's **touchscreen** (Toybox → Light Show). Shows started from the phone app may not light the front of the car.
- Use short, lowercase file names. If a show gets interrupted, reboot the screen before the next one.

## Sources

- On-car channel tests on a 2025+ Model Y Juniper, October 2026 (this project).
- [teslamotors/light-show](https://github.com/teslamotors/light-show): Tesla's official guide, used for the moving-part commands, limits and timings.
- [teslamotors/light-show issue #183](https://github.com/teslamotors/light-show/issues/183): another owner's Juniper front-bar findings, which match these.
