# Air Quality Analysis using Python and Streamlit

## Dataset

Dataset terdiri dari data kualitas udara yang diambil dari beberapa stasiun di China. Data mencakup informasi seperti konsentrasi PM2.5, PM10, SO2, NO2, CO, O3, suhu, tekanan, curah hujan, dan kecepatan angin, serta waktu dan lokasi pengambilan sampel.

## Pertanyaan Bisnis

- **Bagaimana pola konsentrasi PM2.5 selama musim dingin di berbagai stasiun dari tahun 2013-2017, dan bagaimana daerah-daerah tersebut dapat dikelompokkan berdasarkan tingkat polusi?**
- **Bagaimana konsentrasi gas berbahaya (NO2 dan CO) di berbagai stasiun selama jam sibuk (7:00–9:00 dan 17:00–19:00) pada tahun 2016, dan bagaimana stasiun-stasiun tersebut dapat dikelompokkan berdasarkan tingkat emisi?**

## Streamlit Dashboard

Membuat dashboard di streamlit dan deploy di streamlit cloud

![image](https://github.com/user-attachments/assets/388f370b-3c1a-4c26-aab0-6bea01ee9dfa)

## Conclusion

- Selama musim panas dari tahun 2013 hingga 2015, konsentrasi PM2.5 menunjukkan variasi yang cukup signifikan di berbagai stasiun. 75% dari stasiun tergolong dalam tingkat polusi sedang, sementara sisanya berada dalam kategori rendah. Stasiun **Changping**, **Dingling**, dan **Huairou** mencatat rata-rata polusi PM2.5 terendah, menjadikannya daerah dengan kualitas udara yang relatif lebih baik selama musim panas. Sebaliknya, stasiun **Guanyuan**, **Tiantan**, dan **Wanliu** memiliki rata-rata polusi PM2.5 tertinggi, meskipun nilai tersebut masih berada dalam kategori tingkat polusi sedang. Puncak polusi tertinggi pada musim panas tercatat pada Juni 2013, sedangkan polusi terendah terjadi pada Agustus 2015, menunjukkan adanya fluktuasi tahunan. Pola ini mencerminkan bahwa meskipun ada perbedaan antarstasiun, mayoritas wilayah masih menunjukkan tingkat polusi yang tidak terlalu ekstrem, tetapi tetap perlu diperhatikan untuk menjaga kualitas udara tetap baik.

- Pada jam sibuk tahun 2016, 75% stasiun memiliki emisi NO2 & CO yang tinggi, sementara hanya 8.3% yang rendah. **Dingling** dan **Huairou** tercatat dengan emisi terendah, sedangkan **Shunyi** berada pada tingkat sedang. Ada korelasi positif antara NO2 dan CO, di mana peningkatan salah satu gas diikuti oleh gas lainnya. Meskipun mayoritas stasiun menunjukkan emisi tinggi, beberapa stasiun tetap rendah meski pada jam sibuk, mencerminkan perbedaan kondisi lingkungan atau aktivitas di sekitarnya.

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
