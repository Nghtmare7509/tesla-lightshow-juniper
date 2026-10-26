# Tesla Light Show for Claude (Model Y Juniper edition)

A Claude plugin that turns a `.wav` or `.mp3` song into a Tesla custom light show (`.fseq` + matching audio file) for the Toybox Light Show app. I set out to do this because I did not like that almost every lightshow(all but a few and then the tesla created ones) out there did not use the lightbar or ambient lights during the shows. I had tried several different sites that create them including this plugin zzorp created that i piggybacked on. This should work for other Models when you tell it what model you have but was specifically setup for 2025+ Model Y Juniper with Lightbars and the interior ambient lighting.

## Install in Claude(Paid Accounts)

1. In the Claude desktop app, open **Customize → Plugins**.
2. Choose **Add marketplace → Add from a repository**.
3. Enter `Nghtmare7509/tesla-lightshow-juniper`.
4. Install **tesla-light-show** from the new marketplace.

Then start a chat, attach a `.wav` or `.mp3` (44.1 kHz), and ask for a light show.

Tips: Keep file names short and lowercase

## Free Claude accounts

Plugins need a paid Claude plan, but **skills work on every plan, including Free**. Free users can install the same light show generator as a skill:

1. Download [`tesla-light-show-skill.zip`](tesla-light-show-skill.zip) from this repo (don't unzip it).
2. In Claude, go to **Settings → Capabilities** and turn on **Code execution and file creation** (it may be called **Create and edit files**).
3. Go to **Customize → Skills**, choose to upload a skill, and select the zip.
4. Start a chat, attach your song, and ask for a light show for your car.

Tip: use an `.mp3` rather than a `.wav`; `.wav` files are much larger and may hit the chat's upload size limit. Free plans also have lower usage limits, so a long song may take more than one try.

## Without Claude (command line)

The scripts are plain Python, so anyone can run them without a Claude account. You need Python 3 with numpy (plus ffmpeg for `.mp3`). From the `plugins/tesla-light-show/skills/tesla-light-show/scripts` folder:

```bash
python3 analyze_audio.py mysong.mp3 mysong.json
python3 compose_show.py --analysis mysong.json --model model_y_juniper --out mysong.fseq
python3 validate_fseq.py mysong.fseq
```

Other `--model` options: `model_3`, `model_3_highland`, `model_s`, `model_x`, `model_y`, `cybertruck`. Copy `mysong.fseq` and `mysong.mp3` into a `LightShow` folder on your USB drive.

## Other Stuff

The commands required are not difficult for AI/SI systems. I know with grok you can just give it the github repo link and ask it to create the lightshow and it can sandbox mode it and run the processes. Others may as well if you have a service you pay for. 

I added a CHANNELS.md so you can see what channels do what if someone wants to modify or dig deeper into it. I walked through and watched every channel to see what it did and noted it for the CHANNELS.md. 

I was also trying to work out how to do custom messages with the Matrix Headlights. One of the older Lightshows from a holiday update used the Matrix Headlights to display TESLA on the wall in front of the car. I always liked that and think it would be pretty cool to be able to Spell out what you want. It turns out they changed the matrix headlights on newer model 3/Y's and that isn't possible anymore. 

## Credits

Based on [zzorp/tesla-lightshow-skill](https://github.com/zzorp/tesla-lightshow-skill) (MIT). This version adds a Model Y Juniper channel map that was tested on a real car.

Built on top of the Tesla Motors light-show reference project (Tesla's official xLights guide, validator, and channel mapping). This skill doesn't include or redistribute any Tesla code — just documents and uses the published format.

## License

MIT. Original work © 2026 Zoran Pucar; Model Y Juniper changes by Nghtmare7509.
