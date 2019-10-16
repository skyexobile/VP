import os
import glob
import pandas as pd
os.chdir("../VP/A1")
filenames = [i for i in glob.glob('_BVP*.csv')]
combined = pd.concat([pd.read_csv(f) for f in filenames],sort=True)
combined.to_csv("combined.csv", index=False)
