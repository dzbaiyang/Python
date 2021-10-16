from datetime import datetime, date, timedelta
import numpy
import json
import time


yesterday = (date.today() + timedelta(days = -1)).strftime("%Y-%m-%d")
print(yesterday)