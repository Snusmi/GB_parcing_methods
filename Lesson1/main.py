from pprint import pprint
import requests
import json
main_link = 'https://api.openweathermap.org/data/2.5/weather'
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
          'Accept':'*/*'}
city = 'Moscow'
appid = '2292b417245591415a85e86b30ac66b9'
params = {'q':city,
          'appid':appid}
response = requests.get(main_link,headers=header,params=params)
if response.ok:
    data = json.loads(response.text)

print(f"В городе {data['name']} температура {round(data['main']['temp'] - 273.15,2)} градусов")









# with open('file.pdf','wb') as f:
#     f.write(response.content)
