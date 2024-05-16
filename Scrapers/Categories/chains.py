import time
import requests
import pandas as pd
import numpy as np

pd.set_option("display.float.format", "{:,.0f}".format)

from Scrapers.scraper import LlamaScraper

from selenium.common.exceptions import TimeoutException
from urllib3.exceptions import MaxRetryError


class Chains(LlamaScraper):
    def __init__(self) -> None:
        super().__init__()

    def get_table(self):

        url = "https://defillama.com/chains"

        self.create_browser(url)

        table_config = {
            "name": "/html/body/div[1]/div[1]/div/main/div[2]/div[4]/div[2]/div[{}]/div[1]/span/a",
            "protocols": "/html/body/div[1]/div[1]/div/main/div[2]/div[4]/div[2]/div[{}]/div[2]",
            "active_address": "/html/body/div[1]/div[1]/div/main/div[2]/div[4]/div[2]/div[{}]/div[3]",
            "tvl": "/html/body/div[1]/div[1]/div/main/div[2]/div[4]/div[2]/div[{}]/div[7]",
            "24h_volume": "/html/body/div[1]/div[1]/div/main/div[2]/div[4]/div[2]/div[{}]/div[10]",
            "24h_fees": "/html/body/div[1]/div[1]/div/main/div[2]/div[4]/div[2]/div[{}]/div[11]",
            "mcap/tvl": "/html/body/div[1]/div[1]/div/main/div[2]/div[4]/div[2]/div[{}]/div[12]",
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
                print(f"Name: {name}")
                protocols = self.read_data(
                    table_config["protocols"].format(index), wait=True
                )
                active_address = self.read_data(
                    table_config["active_address"].format(index)
                )
                tvl = self.read_data(table_config["tvl"].format(index))
                volume_24h = self.read_data(
                    table_config["24h_volume"].format(index), wait=True
                )
                fees_24h = self.read_data(
                    table_config["24h_fees"].format(index), wait=True
                )
                mcap_tvl = self.read_data(
                    table_config["mcap/tvl"].format(index), wait=True
                )

                # Clean data before adding it to list.
                protocols = int(protocols)
                active_address = self.format_basic(active_address)
                tvl = self.format_dollar(tvl)
                volume_24h = self.format_dollar(volume_24h)
                fees_24h = self.format_dollar(fees_24h)
                try:
                    mcap_tvl = float(mcap_tvl)
                except ValueError:
                    mcap_tvl = np.nan
                table = {
                    "name": name,
                    "protocols": protocols,
                    "active_address": active_address,
                    "tvl": tvl,
                    "volume_24h": volume_24h,
                    "fees_24h": fees_24h,
                    "mcap/tvl": mcap_tvl,
                }
                print(f"{index}: {table}")
                entries.append(table)
                index += 1
            except TimeoutException:
                self.clean_close()
                scraping = False

        # except MaxRetryError:
        #     self.clean_close()

        df = pd.DataFrame(entries)
        df = df.set_index("name")
        folder = "Chains"
        file_name = "chains"

        self.excel.export_to_excel(df, file_name, folder)
        self.excel.export_to_csv(df, file_name, folder)


# 1  36 ICP
