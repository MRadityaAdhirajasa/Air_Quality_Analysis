# Air Quality Analysis using Python and Streamlit

## Dataset

The dataset consists of air quality data taken from several stations in China. The data includes information such as concentrations of PM2.5, PM10, SO2, NO2, CO, O3, temperature, pressure, precipitation, and wind speed, as well as sampling time and location.

## Pertanyaan Bisnis

- **What is the pattern of PM2.5 concentrations during winter at various stations from 2013-2017, and how can these areas be categorized based on pollution levels?**
- **What were the concentrations of harmful gases (NO2 and CO) at various stations during peak hours (7:00-9:00 and 17:00-19:00) in 2016, and how can the stations be categorized by emission levels?**

## Streamlit Dashboard

Create dashboards using streamlit and deploy on streamlit cloud

![image](https://github.com/user-attachments/assets/388f370b-3c1a-4c26-aab0-6bea01ee9dfa)

## Conclusion

- During the summer season from 2013 to 2015, PM2.5 concentrations showed significant variations across stations. 75% of the stations belonged to moderate pollution levels, while the rest were in the low category. The **Changping**, **Dingling**, and **Huairou** stations recorded the lowest average PM2.5 pollution, making them areas with relatively better air quality during summer. In contrast, stations **Guanyuan**, **Tiantan**, and **Wanliu** had the highest average PM2.5 pollution, although these values still fall within the moderate pollution level category. The highest pollution peak in summer was recorded in June 2013, while the lowest pollution occurred in August 2015, indicating annual fluctuations. This pattern reflects that while there are differences between stations, the majority of areas still show less extreme pollution levels, but still need to be considered to maintain good air quality.

- In 2016 peak hours, 75% of stations had high NO2 & CO emissions, while only 8.3% were low. **Dingling** and **Huairou** were recorded with the lowest emissions, while **Shunyi** was at a medium level. There is a positive correlation between NO2 and CO, where an increase in one of the gases is followed by the other. While the majority of stations showed high emissions, some stations remained low even during peak hours, reflecting differences in environmental conditions or surrounding activities.

## Link

Dataset : https://drive.google.com/drive/folders/1no8MgmNPSa6eBsB2HkP82c2iJNz6U7C-?usp=drive_link

Streamlit : https://airqualityanalysis2712.streamlit.app/

## How to RUN using VSCode Terminal

### Install requirements.txt
```
pip install -r requirements.txt
```

### Run steamlit app
```
streamlit run dashboard.py
```
