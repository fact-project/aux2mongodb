import matplotlib.pyplot as plt
from aux2mongodb import MagicWeather, PfMini
import pandas as pd
from tqdm import tqdm
import datetime

plt.style.use('ggplot')


magic_weather = MagicWeather(auxdir='/fact/aux')
pf_mini = PfMini(auxdir='/fact/aux')
dates = pd.date_range('2015-10-20', datetime.date.today())

outside = pd.DataFrame()
camera = pd.DataFrame()
for d in tqdm(dates):
    try:
        outside = outside.append(magic_weather.read_date(d), ignore_index=True)
    except FileNotFoundError:
        continue
    try:
        camera = camera.append(pf_mini.read_date(d), ignore_index=True)
    except FileNotFoundError:
        continue

outside.set_index('timestamp', inplace=True)
camera.set_index('timestamp', inplace=True)
outside = outside.resample('24h').mean()
camera = camera.resample('24h').mean()

fig, ax = plt.subplots()
ax.set_title('Camera vs. Outside Humidity (24h mean)')

outside.plot(y='humidity', legend=False, label='Outside', ax=ax)
camera.plot(y='humidity', legend=False, label='In Camera', ax=ax)

ax.legend()
ax.set_ylabel('Humidity / %')
fig.tight_layout()
plt.show()
