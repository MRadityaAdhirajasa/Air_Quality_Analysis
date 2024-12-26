import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

aoti_df = pd.read_csv('PRSA_Data_Aotizhongxin_20130301-20170228.csv')
chang_df = pd.read_csv('PRSA_Data_Changping_20130301-20170228.csv')
ding_df = pd.read_csv('PRSA_Data_Dingling_20130301-20170228.csv')
dong_df = pd.read_csv('PRSA_Data_Dongsi_20130301-20170228.csv')
guan_df = pd.read_csv('PRSA_Data_Guanyuan_20130301-20170228.csv')
guch_df = pd.read_csv('PRSA_Data_Gucheng_20130301-20170228.csv')
huai_df = pd.read_csv('PRSA_Data_Huairou_20130301-20170228.csv')
nong_df = pd.read_csv('PRSA_Data_Nongzhanguan_20130301-20170228.csv')
shun_df = pd.read_csv('PRSA_Data_Shunyi_20130301-20170228.csv')
tian_df = pd.read_csv('PRSA_Data_Tiantan_20130301-20170228.csv')
wanl_df = pd.read_csv('PRSA_Data_Wanliu_20130301-20170228.csv')
wans_df = pd.read_csv('PRSA_Data_Wanshouxigong_20130301-20170228.csv')

merged_df = pd.concat([aoti_df, chang_df, guan_df, ding_df, dong_df, guch_df, huai_df, nong_df, shun_df,
                       tian_df, wanl_df, wans_df], ignore_index=True)

merged_df = merged_df.dropna()

def remove_outliers(df, column_name):
    if column_name not in df.columns:
        st.error(f"Column '{column_name}' not found in the DataFrame.")
        return None

    Q1 = df[column_name].quantile(0.25)
    Q3 = df[column_name].quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    filtered_df = df[(df[column_name] >= lower_bound) & (df[column_name] <= upper_bound)]

    df[column_name] = df[column_name].apply(
        lambda x: lower_bound if x < lower_bound else (upper_bound if x > upper_bound else x)
    )

    return filtered_df

remove_outliers(merged_df, "PM2.5")
remove_outliers(merged_df, "CO")
remove_outliers(merged_df, "NO2")

merged_df['datetime'] = pd.to_datetime(merged_df[['year', 'month', 'day', 'hour']])


# Fungsi untuk membaca data
@st.cache_data

def load_data():
    return merged_df

# Muat data
st.title("Analisis PM2.5 Berdasarkan Musim")
data = load_data()

# Sidebar untuk memilih filter
st.sidebar.header("Filter")
year_options = ["Semua Tahun"] + sorted(data['datetime'].dt.year.unique().tolist())  # Tambahkan "Semua Tahun"
year_filter = st.sidebar.selectbox("Pilih Tahun", year_options)
season = st.sidebar.selectbox("Pilih Musim", ["Musim Semi", "Musim Panas", "Musim Gugur", "Musim Dingin"])

# Filter data berdasarkan tahun dan musim
def filter_by_year_and_season(data, year, season):
    if year != "Semua Tahun": 
        data = data[data['datetime'].dt.year == year]
    if season == "Musim Semi":
        return data[data['datetime'].dt.month.isin([3, 4, 5])]
    elif season == "Musim Panas":
        return data[data['datetime'].dt.month.isin([6, 7, 8])]
    elif season == "Musim Gugur":
        return data[data['datetime'].dt.month.isin([9, 10, 11])]
    elif season == "Musim Dingin":
        return data[data['datetime'].dt.month.isin([12, 1, 2])]

# Data yang difilter berdasarkan tahun dan musim
filtered_data = filter_by_year_and_season(data, year_filter, season)
filtered_data['year_month'] = filtered_data['datetime'].dt.to_period('M')

# Perhitungan rata-rata PM2.5 per stasiun
grouped_data = filtered_data.groupby('station')['PM2.5'].mean().reset_index()
grouped_data.rename(columns={'PM2.5': 'avg_PM2.5'}, inplace=True)

# Cari stasiun dengan rata-rata PM2.5 tertinggi
if not grouped_data.empty:
    max_pm25_station = grouped_data.loc[grouped_data['avg_PM2.5'].idxmax(), 'station']
    max_pm25_value = grouped_data['avg_PM2.5'].max()
    st.markdown(f"## PM2.5 Tertinggi: {max_pm25_value:.2f} - Stasiun {max_pm25_station}")
else:
    st.markdown("## Tidak ada data untuk kombinasi tahun dan musim yang dipilih.")

# Klasifikasi kategori PM2.5
def categorize(pm25):
    if pm25 < 60:
        return "Rendah"
    elif 60 <= pm25 < 80:
        return "Sedang"
    else:
        return "Tinggi"

grouped_data['Kategori'] = grouped_data['avg_PM2.5'].apply(categorize)

# Warna kategori
def get_color(category):
    if category == "Rendah":
        return "lightblue"
    elif category == "Sedang":
        return "blue"
    elif category == "Tinggi":
        return "darkblue"

# Barplot - Rata-rata PM2.5 per stasiun
st.subheader(f"Rata-rata PM2.5 di Setiap Stasiun ({season} {year_filter})")
fig1, ax1 = plt.subplots(figsize=(10, 6))
if not grouped_data.empty:
    sns.barplot(
        x='station', 
        y='avg_PM2.5', 
        data=grouped_data, 
        palette=[get_color(kat) for kat in grouped_data['Kategori']],
        ax=ax1
    )
    ax1.set_xlabel("Station")
    ax1.set_ylabel("Average PM2.5")
    ax1.set_title(f"Average PM2.5 Levels by Station ({season} {year_filter})")
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig1)
else:
    st.write("Tidak ada data untuk ditampilkan pada grafik batang.")

# Pie Chart - Proporsi kategori PM2.5
st.subheader(f"Proporsi Stasiun Berdasarkan Kategori PM2.5 ({season} {year_filter})")
category_counts = grouped_data['Kategori'].value_counts()
if not category_counts.empty:
    pie_colors = [get_color(cat) for cat in category_counts.index]
    fig2, ax2 = plt.subplots(figsize=(8, 8))
    category_counts.plot.pie(
        autopct='%1.1f%%', 
        colors=pie_colors, 
        labels=category_counts.index,
        ax=ax2
    )
    ax2.set_title("Proportion of Stations by PM2.5 Category")
    ax2.set_ylabel("")
    st.pyplot(fig2)
else:
    st.write("Tidak ada data untuk kategori yang tersedia.")

# Line Chart - Tingkat Polusi PM2.5 Bulanan
st.subheader(f"Tingkat Polusi PM2.5 Bulanan ({season})")
monthly_data = filtered_data.groupby('year_month')['PM2.5'].mean().reset_index()
monthly_data['year_month'] = monthly_data['year_month'].dt.to_timestamp()

fig3, ax3 = plt.subplots(figsize=(10, 6))
if not monthly_data.empty:
    ax3.plot(
        monthly_data['year_month'], 
        monthly_data['PM2.5'], 
        marker='o', 
        linestyle='-', 
        color='blue'
    )
    ax3.set_xlabel('Month')
    ax3.set_ylabel('Average PM2.5')
    ax3.set_title(f"Average PM2.5 Levels by Month ({season})")
    ax3.grid(True)
    ax3.set_xticks(monthly_data['year_month'])
    ax3.set_xticklabels(monthly_data['year_month'].dt.strftime('%b %Y'), rotation=45, ha='right')
    st.pyplot(fig3)
else:
    st.write("Tidak ada data untuk ditampilkan pada grafik garis.")

#--------------------------------------------------------------------------------------------------------------

# Muat data
st.title("Analisis Emisi Udara NO2 dan CO")
data = load_data()

# Filter data untuk tahun yang dipilih dan jam sibuk (7:00–9:00 dan 17:00–19:00)
filtered_emisi = data[
    ((data['datetime'].dt.year == year_filter) if year_filter != "Semua Tahun" else True) &
    (data['datetime'].dt.hour.isin([7, 8, 9, 17, 18, 19]))
]

# Agregasi rata-rata NO2 dan CO per stasiun
aggregated_emisi = filtered_emisi.groupby('station')[['NO2', 'CO']].mean().reset_index()

# Normalisasi data menggunakan MinMaxScaler
scaled_emisi = aggregated_emisi.copy()
scaler = MinMaxScaler()
scaled_emisi[['NO2', 'CO']] = scaler.fit_transform(aggregated_emisi[['NO2', 'CO']])

# Klasifikasi stasiun berdasarkan kategori emisi
def classify_station(row):
    if row['NO2'] > 0.7 or row['CO'] > 0.7:
        return 'Tinggi'
    elif row['NO2'] > 0.4 or row['CO'] > 0.4:
        return 'Sedang'
    else:
        return 'Rendah'

scaled_emisi['Kategori'] = scaled_emisi.apply(classify_station, axis=1)

# Visualisasi Heatmap
st.subheader(f"Heatmap Tingkat NO2 dan CO per Stasiun {year_filter} (Jam Sibuk)")
fig1, ax1 = plt.subplots(figsize=(12, 6))
sns.heatmap(
    scaled_emisi.set_index('station')[['NO2', 'CO']], 
    annot=True, 
    cmap='coolwarm', 
    ax=ax1
)
ax1.set_title('Heatmap of NO2 and CO Levels by Station (Peak Hours)')
ax1.set_xlabel('Gases')
ax1.set_ylabel('Stations')
st.pyplot(fig1)

# Visualisasi Scatter Plot
category_colors = {'Rendah': 'blue', 'Sedang': 'orange', 'Tinggi': 'red'}
st.subheader(f"Scatter Plot NO2 vs CO {year_filter} (Jam Sibuk)")
fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.scatterplot(
    data=scaled_emisi, 
    x='NO2', 
    y='CO', 
    hue='Kategori', 
    style='Kategori', 
    s=100, 
    ax=ax2,
    palette=category_colors
)
ax2.set_title('Scatter Plot of NO2 vs CO Levels by Station (Peak Hours)')
ax2.set_xlabel('NO2 (Normalized)')
ax2.set_ylabel('CO (Normalized)')
ax2.grid(True)
st.pyplot(fig2)

# Informasi Tambahan
st.subheader("Keterangan")
st.markdown("""
- **Tinggi**: NO2 > 0.7 atau CO > 0.7  
- **Sedang**: NO2 > 0.4 atau CO > 0.4  
- **Rendah**: NO2 <= 0.4 dan CO <= 0.4
- **Jam Sibuk**: 7-9 AM & 5-7 PM
""")