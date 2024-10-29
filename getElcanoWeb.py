from playwright.async_api import async_playwright
import asyncio


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

            #print("Page loaded successfully.")
            print("Response Status:", response.status)

        except Exception as e:
            print(f"An error occurred: {e}")
            await browser.close()
            return

        # Wait for the iframe to be available
        await page.wait_for_selector("#inner-iframe")
        #print("Iframe has appeared.")

        # Get the iframe element
        iframe_element = await page.query_selector("#inner-iframe")

        # Wait for the iframe's content to load and switch to it
        iframe_content = await iframe_element.content_frame()
        await iframe_content.wait_for_load_state("load")
        #print("Iframe content has fully loaded.")

        # Extract all clickable links within the iframe
        links = await iframe_content.query_selector_all("a")

        # Open a text file to save the output
        with open("toys/cachedList.txt", "w") as file:
            # Extract href and text for each link
            for link in links:
                href = await link.get_attribute("href")
                text = await link.inner_text()
                # Strip the 'acestream://' prefix and write to file
                if href.startswith("acestream://"):
                    href = href[len("acestream://"):]

                # Write text and href without extra newlines
                file.write(f"{text.strip()}\n{href}\n")
                print(f"{text.strip()}\n{href}")

        #print("Clickable content has been saved to 'cached_list.txt'.")

        # Keep the browser open for an hour before closing
        await asyncio.sleep(1)
        await browser.close()


# Example usage
async def main():
    url = 'https://proxy.zeronet.dev/18D6dPcsjLrjg2hhnYqKzNh2W6QtXrDwF/'
    await extract_links_from_iframe(url)


# Run the async function
asyncio.run(main())
