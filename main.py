import csv
import time
from playwright.sync_api import sync_playwright


def parse(page_count):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        with open('data.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Pair", "Price", "24H Volume"])

            for page_number in range(1, page_count + 1):
                page.goto(f"https://coinmarketcap.com/dexscan/networks/solana/?page={page_number}&swap=raydium")

                time.sleep(1)

                results = []

                for _ in range(20):
                    page.evaluate('window.scrollBy(0, window.innerHeight * 0.2)')

                    tbody = page.query_selector(
                        "xpath=/html/body/div[1]/div[3]/div/div[3]/div/div[2]/div[1]/div/div/div[1]/div[2]/table/tbody")
                    if tbody:
                        trs = tbody.query_selector_all("tr")
                        for tr in trs:
                            tds = tr.query_selector_all("td")
                            if len(tds) >= 8:
                                result = [tds[1].text_content(), tds[3].text_content(), tds[7].text_content()]
                                if result not in results:
                                    results.append(result)

                print(f"Parsed page number: {page_number}")

                for result in results:
                    writer.writerow(result)

        browser.close()


def main():
    try:
        pages_for_parse = int(input("Enter how many pages you want to parse: "))
        parse(pages_for_parse)
    except:
        print("You answer is incorrect")


if __name__ == '__main__':
    main()
