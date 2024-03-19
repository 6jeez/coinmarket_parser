import time
from playwright.sync_api import sync_playwright


def unique_list(l):
    seen = set()
    return [x for x in l if not (x in seen or seen.add(x))]


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://coinmarketcap.com/dexscan/networks/solana/?page=2&swap=raydium")

    time.sleep(1)

    results = []
    i = 1

    for _ in range(20):
        page.evaluate('window.scrollBy(0, window.innerHeight * 0.2)')
        # time.sleep(0.5)

        tbody = page.query_selector("xpath=/html/body/div[1]/div[3]/div/div[3]/div/div[2]/div[1]/div/div/div[1]/div[2]/table/tbody")
        if tbody:
            trs = tbody.query_selector_all("tr")
            for tr in trs:
                tds = tr.query_selector_all("td")
                if len(tds) >= 8:
                    result = f'{tds[1].text_content()} | {tds[3].text_content()} | {tds[7].text_content()}'
                    results.append(result)
        print(f'iteration number {i}/20')
        i += 1


    results = unique_list(results)

    for result in results:
        print(result)

    time.sleep(5)

    browser.close()
