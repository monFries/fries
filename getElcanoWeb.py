import re
from playwright.async_api import async_playwright
import asyncio

url = 'https://proxy.zeronet.dev/18D6dPcsjLrjg2hhnYqKzNh2W6QtXrDwF/'


async def extract_links_from_iframe(url):
    async with async_playwright() as p:
        # Launch the browser in headful mode
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Navigate to the URL and capture the response
        try:
            response = await page.goto(url)

            # Check if the response was successful
            if response.status != 200:
                print(f"Error: Page not available (status code: {response.status})")
                await browser.close()
                return

            print("Response Status:", response.status)

        except Exception as e:
            print(f"An error occurred: {e}")
            await browser.close()
            return

        # Wait for the iframe to be available
        await page.wait_for_selector("#inner-iframe")

        # Get the iframe element
        iframe_element = await page.query_selector("#inner-iframe")

        # Wait for the iframe's content to load and switch to it
        iframe_content = await iframe_element.content_frame()
        await iframe_content.wait_for_load_state("load")

        # Extract all links from the linksList container
        links_list = await iframe_content.query_selector("#linksList")
        list_items = await links_list.query_selector_all("li")

        # Collect AceStream links in a list
        acestream_links = []
        for item in list_items:
            name = await item.query_selector(".link-name")
            url_div = await item.query_selector(".link-url")
            link_actions = await item.query_selector_all(".link-actions a")

            # Get the name and url
            name_text = await name.inner_text() if name else None
            url_text = await url_div.inner_text() if url_div else None

            # Check if there are any links in the actions
            for link in link_actions:
                href = await link.get_attribute("href")
                # Extract the stream ID from the href
                if href and "getstream?id=" in href:
                    stream_id = href.split("id=")[-1]
                    # Check if stream_id is valid (40 alphanumeric characters)
                    if re.fullmatch(r'[A-Za-z0-9]{40}', stream_id):
                        acestream_links.append((name_text.strip(), stream_id))

        # Write to file only if there are AceStream links
        if acestream_links:
            with open("toys/cachedList.txt", "w") as file:
                for text, href in acestream_links:
                    file.write(f"{text}\n{href}\n")
                    #print(f"{text}\n{href}")
            print(f"{len(acestream_links)} AceStream links saved.")
        else:
            print("No AceStream links found. cachedList.txt has not been modified.")

        # Close the browser
        await browser.close()


async def main():
    await extract_links_from_iframe(url)


# Run the async function
#asyncio.run(main())
