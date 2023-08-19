import sys
import modal
from datetime import date

feed_url = sys.argv[1]

func = modal.Function.lookup("corise-podcast-project", "process_podcast")

results = func.remote(feed_url, '/content/podcast/')

details = results.get("podcast_details", False)
summary = results.get("podcast_summary", False)
guests = results.get("podcast_guests", False)
highlights = results.get("podcast_highlights", False)

if (not details):
    print("No podcast details found")
    exit()

filename = "-".join(f"{details['podcast_title']} {details['episode_title']}.json".lower().split(" "))

template = f"""---
title: {details['podcast_title']} | {details['episode_title']}
date: {date.today()}
---

![episode image]({details['episode_image']})

"""

if (summary):
    template += f"## Summary\n\n"

if (guests):
    template += f"## Guests\n\n"

    for guest in guests:
        guest_output = f"- {guest['name']}"

        if (guest.get("title", False)):
            guest_output += f" - _{guest['title']}_"

        if (guest.get("organization", False)):
            guest_output += f" - {guest['organization']}"

        if (guest.get("wiki", False)):
            guest_output += f"[Wikipedia]({guest['wiki']['url']})"

        template += f"{guest_output}\n"

if (highlights):
    template += f"\n## Highlights\n\n"
    template += f"{highlights}\n"

new_file = open(f"../content/podcasts/{filename}", "w")

new_file.write(template)
new_file.close()
