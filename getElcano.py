import json
import requests
import os

# Define the URL and output file path
url = "https://proxy.zeronet.dev/18D6dPcsjLrjg2hhnYqKzNh2W6QtXrDwF/links.json"
output_file = "toys/cachedList.txt"


def getCachedList():

    # Fetch the JSON data from the URL
    response = requests.get(url)
    data = response.json()

    # Prepare content for saving
    content_lines = []
    for link in data["links"]:
        content_lines.append(link['name'].strip())
        #print(link['name'])
        content_lines.append(link['url'].replace('acestream://', '').strip())
        #print(link['url'].replace('acestream://', ''))

    # Write content to the output file
    with open(output_file, "w") as f:
        f.write("\n".join(content_lines))

    print(f"Data saved to {output_file}.")


#getCachedList()
