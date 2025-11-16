#!/bin/bash

# Launch the script, downloading and transcribing all the new episodes for a specific podcast
source .venv/bin/activate
python -m podcast_downloader --config podcast-downloader-config.json
python trascript_podcasts.py --directory podcasts/the_bull --model medium --log-level INFO
.venv/bin/deactivate


