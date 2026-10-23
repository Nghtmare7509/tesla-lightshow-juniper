# Tesla Light Show for Claude (Model Y Juniper edition)

A Claude plugin that turns a `.wav` or `.mp3` song into a Tesla custom light show (`.fseq` + matching audio file) for the Toybox Light Show app. This should work for other Models but was specifically setup for 2025+ Model Y Juniper with Lightbars.

Based on [zzorp/tesla-lightshow-skill](https://github.com/zzorp/tesla-lightshow-skill) (MIT). This version adds a Model Y Juniper channel map that was tested on a real car.

## Install in Claude

1. In the Claude desktop app, open **Customize → Plugins**.
2. Choose **Add marketplace → Add from a repository**.
3. Enter `Nghtmare7509/tesla-lightshow-juniper`.
4. Install **tesla-light-show** from the new marketplace.

Then start a chat, attach a `.wav` or `.mp3` (44.1 kHz), and ask for a light show.

Tips: Keep file names short and lowercase

## Other Stuff

I added a CHANNELS.md so you can see what channels do what if someone wants to modify or dig deeper into it. 

I was also trying to work out how to do custom messages with the Matrix Headlights. One of the older Lightshows from a holiday update used the Matrix Headlights to display TESLA on the wall in front of the car. I always liked that and think it would be pretty cool to be able to Spell out what you want. It turns out they changed the matrix headlights on newer model 3/Y's and that isn't possible anymore. 

## Requirements

Claude with plugins enabled. The scripts need Python 3 with numpy (and ffmpeg or librosa for .mp3); librosa, madmom and scipy are optional and improve beat and section detection.

## License

MIT. Original work © 2026 Zoran Pucar; Model Y Juniper changes by Nghtmare7509.
