import time
import requests
import pandas as pd
import numpy as np

pd.set_option("display.float.format", "{:,.0f}".format)

from Scrapers.scraper import LlamaScraper
from selenium.common.exceptions import TimeoutException


class Dexes(LlamaScraper):
    def __init__(self) -> None:
        super().__init__()

    def get_table(self):

        url = "https://defillama.com/protocols/Dexes"

        self.create_browser(url)

        table_config = {
            "name": "/html/body/div[1]/div[1]/div/main/div[3]/div[3]/div[2]/div[{}]/div[2]/span/span/a",
            "tvl": "/html/body/div[1]/div[1]/div/main/div[3]/div[3]/div[2]/div[{}]/div[6]",
            "fees_7d": "/html/body/div[1]/div[1]/div/main/div[3]/div[3]/div[2]/div[{}]/div[7]",
            "revenue_7d": "/html/body/div[1]/div[1]/div/main/div[3]/div[3]/div[2]/div[{}]/div[8]",
            "volume_7d": "/html/body/div[1]/div[1]/div/main/div[3]/div[3]/div[2]/div[{}]/div[9]",
            "mcap_tvl": "/html/body/div[1]/div[1]/div/main/div[3]/div[3]/div[2]/div[{}]/div[10]",
            "fees_24h": "/html/body/div[1]/div[1]/div/main/div[3]/div[3]/div[2]/div[{}]/div[11]",
            "fees_30d": "/html/body/div[1]/div[1]/div/main/div[3]/div[3]/div[2]/div[{}]/div[12]",
            "revenue_24h": "/html/body/div[1]/div[1]/div/main/div[3]/div[3]/div[2]/div[{}]/div[13]",
            "volume_24h": "/html/body/div[1]/div[1]/div/main/div[3]/div[3]/div[2]/div[{}]/div[14]",
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
                tvl = self.read_data(table_config["tvl"].format(index), wait=True)
                fees_7d = self.read_data(
                    table_config["fees_7d"].format(index), wait=True
                )
                revenue_7d = self.read_data(
                    table_config["revenue_7d"].format(index), wait=True
                )
                volume_7d = self.read_data(
                    table_config["volume_7d"].format(index), wait=True
                )
                mcap_tvl = self.read_data(
                    table_config["mcap_tvl"].format(index), wait=True
                )
                fees_24h = self.read_data(
                    table_config["fees_24h"].format(index), wait=True
                )
                fees_30d = self.read_data(
                    table_config["fees_30d"].format(index), wait=True
                )
                revenue_24h = self.read_data(
                    table_config["revenue_24h"].format(index), wait=True
                )
                volume_24h = self.read_data(
                    table_config["volume_24h"].format(index), wait=True
                )

                # Clean data before adding it to list.
                tvl = self.format_dollar(tvl)
                fees_7d = self.format_dollar(fees_7d)
                revenue_7d = self.format_dollar(revenue_7d)
                volume_7d = self.format_dollar(volume_7d)
                try:
                    mcap_tvl = float(mcap_tvl)
                except ValueError:
                    mcap_tvl = np.nan
                fees_24h = self.format_dollar(fees_24h)
                fees_30d = self.format_dollar(fees_30d)
                revenue_24h = self.format_dollar(revenue_24h)
                volume_24h = self.format_dollar(volume_24h)
                table = {
                    "name": name,
                    "tvl": tvl,
                    "fees_24h": fees_24h,
                    "fees_7d": fees_7d,
                    "fees_30d": fees_30d,
                    "revenue_24h": revenue_24h,
                    "revenue_7d": revenue_7d,
                    "volume_24h": volume_24h,
                    "volume_7d": volume_7d,
                    "mcap/tvl": mcap_tvl,
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
        folder = "Dexes"
        file_name = "dexes"

        self.excel.export_to_excel(df, file_name, folder)
        self.excel.export_to_csv(df, file_name, folder)
