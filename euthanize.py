#!/usr/bin/env python3

import argparse
from pathlib import Path
from datetime import datetime, timedelta, timezone, date
from dateutil.relativedelta import relativedelta
from rich.console import Console

console = Console()

parser = argparse.ArgumentParser(
    prog = 'euthanize',
    description = 'Delete files older than a given age',
)

parser.add_argument('path', type=Path)
parser.add_argument('-d', '--days', type=int, required=True, help='The maximum file age of daily backups in days')
parser.add_argument('-w', '--weeks', type=int, required=True, help='The maximum file age of weekly backups in weeks')
parser.add_argument('-m', '--months', type=int, required=True, help='The maximum file age of monthly backups in months')
parser.add_argument('-y', '--years', type=int, required=True, help='The maximum file age of yearly backups in years')
parser.add_argument('-r', '--recursive', action='store_true', help='Search in sub-dierctories')

args = parser.parse_args()

if args.recursive:
    glob = '**/*'
else:
    glob = '*'

today = date.today()
oldest_daily = today - timedelta(days=args.days)
oldest_weekly = today - timedelta(weeks=args.weeks)
oldest_monthly = today - relativedelta(months=args.months)
oldest_yearly = today - relativedelta(years=args.months)

console.print(today, oldest_daily, oldest_weekly, oldest_monthly, oldest_yearly)

to_delete = []

with console.status("Euthanizing backups...", spinner="dots12"):
    for f in [f for f in  args.path.glob(glob) if f.is_file()]:
        modifield_date  = datetime.fromtimestamp(f.stat().st_mtime, tz=timezone.utc).date()

        if modifield_date >= oldest_daily:
            console.print(f'Keeping daily file {f.name} from {modifield_date}')
            continue
    
        if modifield_date >= oldest_weekly and modifield_date.weekday() == 0:
            console.print(f'Keeping weekly file {f.name} from {modifield_date} with day of week of {modifield_date.weekday()}')
            continue

        if modifield_date >= oldest_monthly and modifield_date.day == 1:
            console.print(f'Keeping monthly file {f.name} from {modifield_date} with month day of {modifield_date.day}')
            continue

        if modifield_date >= oldest_yearly and modifield_date.day == 1 and modifield_date.month == 1:
            console.print(f'Keeping yearly file {f.name} from {modifield_date} with month of {modifield_date.month} and day of {modifield_date.day}')
            continue

        to_delete.append(f)
