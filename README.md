# Tesla Light Show for Claude (Model Y Juniper edition)

A Claude plugin that turns a `.wav` song into a Tesla custom light show (`.fseq` + matching `.wav`) for the Toybox Light Show app. Works for Model 3 / 3 Highland, Model S, Model X, Model Y, **Model Y Juniper (2025+)** and Cybertruck.

Based on [zzorp/tesla-lightshow-skill](https://github.com/zzorp/tesla-lightshow-skill) (MIT). This version adds a Model Y Juniper channel map that was tested on a real car.

## Install in Claude

1. In the Claude desktop app, open **Customize → Plugins**.
2. Choose **Add marketplace → Add from a repository**.
3. Enter `YOUR-GITHUB-USERNAME/tesla-lightshow-juniper`.
4. Install **tesla-light-show** from the new marketplace.

Then start a chat, attach a 44.1 kHz `.wav`, and ask for a light show for your car model.

## Model Y Juniper channel map (verified on-car, Oct 2026)

| Channel | Tesla's label | What it drives on Juniper |
|---|---|---|
| 3 / 4 | Inner main beam | Lower white front lamps |
| 7 / 8 | Channel 4 L/R | Outer sections of the front light bar |
| 11 / 12 | Channel 6 L/R | Centre front light bar (either one; fades work) |
| 13 / 14 | Front turn | Amber front lamps |
| 21 / 22 | Side repeater | Side repeaters |
| **25** | Brake | **Rear light bar** |
| 26 / 27 | Tail L/R | Rear brake lamps |
| 176–193 | Interior RGB | Ambient / dash lights and centre screen |

No visible effect on Juniper: 5, 6, 9, 10, 15–20, 29, and the Cybertruck per-LED bar channels 47–162. The rear touchscreen can't be controlled by a light show.

Tips: start shows from the car's touchscreen (not the phone app), keep file names short and lowercase, and reboot the screen if a show was interrupted.

## Requirements

Claude with plugins enabled. The scripts need Python 3 with numpy; librosa, madmom and scipy are optional and improve beat and section detection.

## License

MIT. Original work © 2026 Zoran Pucar; Model Y Juniper changes by Jared Braden.
