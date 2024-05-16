import time
import requests
import pandas as pd
import numpy as np

pd.set_option("display.float.format", "{:,.0f}".format)

from Scrapers.scraper import LlamaScraper

from selenium.common.exceptions import TimeoutException

"/html/body/div[1]/div[1]/div/main/div[4]/div[2]/div[1]/div[1]/span/a"


class Oracles(LlamaScraper):
    def __init__(self) -> None:
        super().__init__()

    def get_table(self):

        url = "https://defillama.com/oracles"

        self.create_browser(url)

        table_config = {
            "name": "/html/body/div[1]/div[1]/div/main/div[4]/div[2]/div[{}]/div[1]/span/a",
            "protocols_secured": "/html/body/div[1]/div[1]/div/main/div[4]/div[2]/div[{}]/div[3]",
            "tvs": "/html/body/div[1]/div[1]/div/main/div[4]/div[2]/div[{}]/div[4]",
        }

        scraping = True
        index = 1
        entries = []
        scroll_interval = 10
        pixel_count = 320
        # self.scroll_page(200)
        while scraping:
            try:
                if index % scroll_interval == 0:
                    pass
                    growth = 0.03
                    pixel_count = pixel_count + (pixel_count * growth)
                    self.scroll_page(pixel_count)
                    print("--------------------------------------------------------")
                    time.sleep(2)

                name = self.read_data(table_config["name"].format(index), wait=True)
                protocols_secured = self.read_data(
                    table_config["protocols_secured"].format(index), wait=True
                )
                tvs = self.read_data(table_config["tvs"].format(index), wait=True)

                # Clean data before adding it to list.
                protocols_secured = int(protocols_secured)
                tvs = int(self.format_dollar(tvs))
                table = {
                    "name": name,
                    "protocols_secured": protocols_secured,
                    "tvs": tvs,
                }
                entries.append(table)
                index += 1
            except TimeoutException:
                self.clean_close()
                scraping = False

        # except MaxRetryError:
        #     self.clean_close()

        df = pd.DataFrame(entries)
        df = df.set_index("name")
        folder = "Oracles"
        file_name = "oracles"

        self.excel.export_to_excel(df, file_name, folder)
        self.excel.export_to_csv(df, file_name, folder)
