import os
from pathlib import Path
from datetime import date, timedelta
import shutil

today = date.today()
epoch_time = date(1970, 1, 1)

data_dir = Path('data/')
shutil.rmtree(data_dir)
data_dir.mkdir(parents=True, exist_ok=True)

for i in range(365):
    f = data_dir / f"today_minus_{i}"
    timestamp = (today - timedelta(days=i)) - epoch_time
    f.touch()
    os.utime(f, (timestamp.total_seconds(), timestamp.total_seconds()))