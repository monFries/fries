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
            print(f"oh oh!: {e}")
            await browser.close()
            return

        # Wait for the iframe to be available
        await page.wait_for_selector("#inner-iframe")

        # Get the iframe element
        iframe_element = await page.query_selector("#inner-iframe")

        # Wait for the iframe's content to load and switch to it
        iframe_content = await iframe_element.content_frame()
        await iframe_content.wait_for_load_state("load")

        # Extract all clickable links within the iframe
        links = await iframe_content.query_selector_all("a")

        # Collect AceStream links in a list
        acestream_links = []
        for link in links:
            href = await link.get_attribute("href")
            text = await link.inner_text()

            # Check if href starts with 'acestream://' and contains exactly 40 alphanumeric characters
            if href and href.startswith("acestream://"):
                content = href[len("acestream://"):]
                if re.fullmatch(r'[A-Za-z0-9]{40}', content):
                    acestream_links.append((text.strip(), content))

        # Write to file only if there are AceStream links
        if acestream_links:
            with open("toys/cachedList.txt", "w") as file:
                for text, href in acestream_links:
                    file.write(f"{text}\n{href}\n")
                    #print(f"{text}\n{href}")
            print(f"{len(acestream_links)} enlaces aceStream guardados")
        else:
            print("No se han encontrado enlaces acestream. No se ha modificado elcano.txt")

        # Close the browser
        await browser.close()


async def main():
    await extract_links_from_iframe(url)


# Run the async function
asyncio.run(main())
