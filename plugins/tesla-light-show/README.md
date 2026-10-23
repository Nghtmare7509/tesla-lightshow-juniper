# Tesla Light Show

Turns a `.wav` or `.mp3` song into a Tesla custom light show (`.fseq` plus a matching audio file) for the Toybox Light Show app. Supports Model 3 / Model 3 Highland, Model S, Model X, Model Y, Model Y Juniper (2025+) and Cybertruck.

Based on [zzorp/tesla-lightshow-skill](https://github.com/zzorp/tesla-lightshow-skill) (MIT). Changes in this version:

- `model_y_juniper` target using an on-car verified channel map: rear light bar on ch 25, centre front bar on ch 11/12, outer front bar on 7/8, brake lamps on 26/27, interior RGB on 176–193 (kept bright). Channels that do nothing on Juniper are folded into ones that work.
- A bundled non-interactive validator (`scripts/validate_fseq.py`) with the same checks as Tesla's official one, so Tesla's repo is no longer needed.
- Script paths work from any folder, and the channel-count notes are corrected.

Requires Python 3 with numpy (plus ffmpeg or librosa for .mp3). Installing librosa, madmom and scipy is optional and improves beat and section detection.
