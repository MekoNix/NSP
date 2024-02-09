import asyncio
import sys
from pyppeteer import launch


async def generate_pdf(url, pdf_path):
    browser = await launch()
    page = await browser.newPage()

    await page.goto(url)

    await page.pdf({'path': pdf_path, 'format': 'A4'})

    await browser.close()


async def main():
    if len(sys.argv) != 3:
        print("Usage: python pdf_generator.py <url> <pdf_filepath>")
        return

    url = sys.argv[1]
    pdf_filepath = sys.argv[2]

    await generate_pdf(url, pdf_filepath)


if __name__ == "__main__":
    asyncio.run(main())
