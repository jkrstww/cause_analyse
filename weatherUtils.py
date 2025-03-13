import requests
import pandas as pd

def get_adcode(file_path):
    df1 = pd.read_excel(file_path, sheet_name='sheet1')

    names = df1['中文名']
    codes = df1['adcode']
    dict = {}
    for i in range(len(names)):
        dict[names[i]] = codes[i]

    return dict

def get_weather(city):
    adcodes = get_adcode('D:\cause_analyse\llamaProject\static\\files\AMap_adcode_citycode.xlsx')

    if city not in adcodes:
        print("地名输入错误")
        return

    citycode = adcodes[city]

    response = requests.get(f"https://restapi.amap.com/v3/weather/weatherInfo?key=33873fddaf4eeb697c880e005679eca3&city={citycode}")

    return response.json()


if __name__ == "__main__":
    weather = get_weather("武侯区")
    print(weather)