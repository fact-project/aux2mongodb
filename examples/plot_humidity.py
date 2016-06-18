import matplotlib.pyplot as plt
from aux2mongodb import MagicWeather
from datetime import date


m = MagicWeather(auxdir='/fact/aux')

df = m.read_date(date(2015, 12, 31))

df.plot(x='timestamp', y='humidity', legend=False)
plt.ylabel('Humidity / %')
plt.show()
