import time
import pandas as pd


from Scrapers.Categories.chains import Chains
from Scrapers.Categories.oracles import Oracles
from Scrapers.Categories.dexes import Dexes
from Scrapers.Categories.rwa import RWA
from Scrapers.Categories.treasuries import Treasuries

# Set display options
# pd.set_option("display.float.format", "{:.2f}".format)

# path = "D:\\DEFILLAMA\\Chains\\chains_2024-5-14.csv"


# df = pd.read_csv(path)

# print(f"DF: {df}")


if __name__ == "__main__":
    start = time.time()
    c = Treasuries()
    c.get_table()
    end = time.time()

    elapse = end - start

    print(f"Elapse: {'{:,.2f}'.format(elapse)} seconds")
