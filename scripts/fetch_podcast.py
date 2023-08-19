import sys
import modal
from datetime import date

feed_url = sys.argv[1]

func = modal.Function.lookup("corise-podcast-project", "process_podcast")

results = func.remote(feed_url, '/content/podcast/')

podcast_details = results.get("podcast_details", False)

if (not podcast_details):
    print("No podcast details found")
    exit()

filename = "-".join(f"{podcast_details['podcast_title']} {podcast_details['episode_title']}.json".lower().split(" "))

template = f"""---
title: {podcast_details['podcast_title']} | {podcast_details['episode_title']}
date: {date.today()}
---

![episode image]({podcast_details['episode_image']})

{podcast_details['podcast_summary']}

## Guests

"""

for guest in podcast_details["podcast_guests"]:
    guest_output = f"- {guest['name']}"

    if (guest.get("title", False)):
        guest_output += f" - _{guest['title']}_"

    if (guest.get("organization", False)):
        guest_output += f" - {guest['organization']}"

    if (guest.get("wiki", False)):
        guest_output += f"[Wikipedia]({guest['wiki']['url']})"

    template += f"{guest_output}\n"

template += f"\n## Highlights\n\n"
template += f"{podcast_details['highlights']}\n"

new_file = open(f"../content/podcasts/{filename}", "w")

new_file.write(template)
new_file.close()
