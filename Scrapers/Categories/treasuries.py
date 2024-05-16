import time
import requests
import pandas as pd
import numpy as np

pd.set_option("display.float.format", "{:,.0f}".format)

from Scrapers.scraper import LlamaScraper
from selenium.common.exceptions import TimeoutException


class Treasuries(LlamaScraper):
    def __init__(self) -> None:
        super().__init__()

    def get_table(self):

        url = "https://defillama.com/treasuries"

        self.create_browser(url)

        table_config = {
            "name": "/html/body/div[1]/div[1]/div/main/div[2]/div[2]/div[1]/div[{}]/span/a",
            # "name": "/html/body/div[1]/div[1]/div/main/div[2]/div[2]/div[1]/div[1]/span/a"
            "stablecoins": "/html/body/div[1]/div[1]/div/main/div[2]/div[2]/div[{}]/div[3]",
            "major_coins": "/html/body/div[1]/div[1]/div/main/div[2]/div[2]/div[{}]/div[4]",
            "own_tokens": "/html/body/div[1]/div[1]/div/main/div[3]/div[3]/div[2]/div[{}]/div[8]",
            "others": "/html/body/div[1]/div[1]/div/main/div[3]/div[3]/div[2]/div[{}]/div[9]",
            "total_excluding_own_tokens": "/html/body/div[1]/div[1]/div/main/div[3]/div[3]/div[2]/div[{}]/div[10]",
            "total": "/html/body/div[1]/div[1]/div/main/div[3]/div[3]/div[2]/div[{}]/div[11]",
            "mcap": "/html/body/div[1]/div[1]/div/main/div[3]/div[3]/div[2]/div[{}]/div[12]",
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
                stablecoins = self.read_data(
                    table_config["stablecoins"].format(index), wait=True
                )
                major_coins = self.read_data(
                    table_config["major_coins"].format(index), wait=True
                )
                own_tokens = self.read_data(
                    table_config["own_tokens"].format(index), wait=True
                )
                others = self.read_data(
                    table_config["volume_7d"].format(index), wait=True
                )
                total_excluding_own_tokens = self.read_data(
                    table_config["total_excluding_own_tokens"].format(index), wait=True
                )
                total = self.read_data(table_config["total"].format(index), wait=True)
                mcap = self.read_data(table_config["mcap"].format(index), wait=True)

                # Clean data before adding it to list.
                stablecoins = self.format_dollar(stablecoins)
                major_coins = self.format_dollar(major_coins)
                own_tokens = self.format_dollar(own_tokens)
                others = self.format_dollar(others)
                total_excluding_own_tokens = self.format_dollar(
                    total_excluding_own_tokens
                )
                total = self.format_dollar(total)
                mcap = self.format_dollar(mcap)

                table = {
                    "name": name,
                    "stablecoins": stablecoins,
                    "major_coins": major_coins,
                    "own_tokens": own_tokens,
                    "others": others,
                    "total_excluding_own_token": total_excluding_own_tokens,
                    "total": total,
                    "marketcap": mcap,
                }

                print(f"Table: {table}")
                entries.append(table)
                index += 1
            except TimeoutException:
                self.clean_close()
                scraping = False

        # except MaxRetryError:
        #     self.clean_close()

        df = pd.DataFrame(entries)
        df = df.set_index("name")
        folder = "Treasuries"
        file_name = "treasuries"

        self.excel.export_to_excel(df, file_name, folder)
        self.excel.export_to_csv(df, file_name, folder)
