import pyreadstat
import pandas as pd

# Load XPT file
df, meta = pyreadstat.read_xport("C:\\Users\\abhis\\Downloads\\LLCP2022XPT\\LLCP2022.XPT", encoding="latin1")

# Save as CSV
df.to_csv("BRFSS_2022.csv", index=False)
