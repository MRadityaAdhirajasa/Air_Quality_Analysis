import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

aoti_df = pd.read_csv('Dataset/PRSA_Data_Aotizhongxin_20130301-20170228.csv')
chang_df = pd.read_csv('Dataset/PRSA_Data_Changping_20130301-20170228.csv')
ding_df = pd.read_csv('Dataset/PRSA_Data_Dingling_20130301-20170228.csv')
dong_df = pd.read_csv('Dataset/PRSA_Data_Dongsi_20130301-20170228.csv')
guan_df = pd.read_csv('Dataset/PRSA_Data_Guanyuan_20130301-20170228.csv')
guch_df = pd.read_csv('Dataset/PRSA_Data_Gucheng_20130301-20170228.csv')
huai_df = pd.read_csv('Dataset/PRSA_Data_Huairou_20130301-20170228.csv')
nong_df = pd.read_csv('Dataset/PRSA_Data_Nongzhanguan_20130301-20170228.csv')
shun_df = pd.read_csv('Dataset/PRSA_Data_Shunyi_20130301-20170228.csv')
tian_df = pd.read_csv('Dataset/PRSA_Data_Tiantan_20130301-20170228.csv')
wanl_df = pd.read_csv('Dataset/PRSA_Data_Wanliu_20130301-20170228.csv')
wans_df = pd.read_csv('Dataset/PRSA_Data_Wanshouxigong_20130301-20170228.csv')

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
st.title("Air Quality Analysis")
st.markdown("---------------------------------------------------------------------------------------------------")
st.markdown("## PM2.5 Analysis by Season & Year")
data = load_data()

# Sidebar untuk memilih filter
st.sidebar.header("Filter")
year_options = ["All Years"] + sorted(data['datetime'].dt.year.unique().tolist())  # Tambahkan "Semua Tahun"
year_filter = st.sidebar.selectbox("Select Year", year_options)
season = st.sidebar.selectbox("Select Season", ["Spring", "Summer", "Autumn", "Winter"])

# Filter data berdasarkan tahun dan musim
def filter_by_year_and_season(data, year, season):
    if year != "All Years": 
        data = data[data['datetime'].dt.year == year]
    if season == "Spring":
        return data[data['datetime'].dt.month.isin([3, 4, 5])]
    elif season == "Summer":
        return data[data['datetime'].dt.month.isin([6, 7, 8])]
    elif season == "Autumn":
        return data[data['datetime'].dt.month.isin([9, 10, 11])]
    elif season == "Winter":
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
    st.markdown(f"## Highest PM2.5: {max_pm25_value:.2f} - {max_pm25_station} station")
else:
    st.markdown("## There is no data for the selected year and season combination.")

# Klasifikasi kategori PM2.5
def categorize(pm25):
    if pm25 < 60:
        return "Low"
    elif 60 <= pm25 < 80:
        return "Moderate"
    else:
        return "High"

grouped_data['Kategori'] = grouped_data['avg_PM2.5'].apply(categorize)

# Warna kategori
def get_color(category):
    if category == "Low":
        return "lightblue"
    elif category == "Moderate":
        return "blue"
    elif category == "High":
        return "darkblue"

# Barplot - Rata-rata PM2.5 per stasiun
st.subheader(f"Average PM2.5 at Each Station ({season} {year_filter})")
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
    st.write("There is no data to display on the bar graph.")

# Pie Chart - Proporsi kategori PM2.5
st.subheader(f"Proportion of Stations by PM2.5 Category ({season} {year_filter})")
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
    st.write("No data for the category is available.")

# Line Chart - Tingkat Polusi PM2.5 Bulanan
st.subheader(f"Monthly PM2.5 Pollution Level ({season})")
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
    st.write("There is no data to display on the line graph.")

#--------------------------------------------------------------------------------------------------------------
st.markdown("---------------------------------------------------------------------------------------------------")
# Muat data
st.markdown("## NO2 and CO Air Emission Analysis")
data = load_data()

# Filter data untuk tahun yang dipilih dan jam sibuk (7:00–9:00 dan 17:00–19:00)
filtered_emisi = data[
    ((data['datetime'].dt.year == year_filter) if year_filter != "All Years" else True) &
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
        return 'High'
    elif row['NO2'] > 0.4 or row['CO'] > 0.4:
        return 'Moderate'
    else:
        return 'Low'

scaled_emisi['Kategori'] = scaled_emisi.apply(classify_station, axis=1)

# Menampilkan stasiun dengan NO2 & CO terendah dan tertinggi
if not scaled_emisi.empty:
    # Stasiun dengan NO2 tertinggi dan terendah
    max_no2_station = scaled_emisi.loc[scaled_emisi['NO2'].idxmax(), 'station']
    max_no2_value = scaled_emisi['NO2'].max()
    min_no2_station = scaled_emisi.loc[scaled_emisi['NO2'].idxmin(), 'station']
    min_no2_value = scaled_emisi['NO2'].min()
    
    # Stasiun dengan CO tertinggi dan terendah
    max_co_station = scaled_emisi.loc[scaled_emisi['CO'].idxmax(), 'station']
    max_co_value = scaled_emisi['CO'].max()
    min_co_station = scaled_emisi.loc[scaled_emisi['CO'].idxmin(), 'station']
    min_co_value = scaled_emisi['CO'].min()

    # Menampilkan informasi
    st.markdown(f"""
    - #### Station with the Highest Emissions: {max_no2_station} & {max_co_station}
    - #### Station with the Lowest Emissions: {min_no2_station} & {min_co_station}
    """)
else:
    st.write("No emissions data is available for display.")

# Visualisasi Heatmap
st.subheader(f"Heatmap of NO2 and CO Levels per Station {year_filter} (Peak Hours)")
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
category_colors_emition = {'Low': 'blue', 'Moderate': 'orange', 'High': 'red'}
st.subheader(f"Scatter Plot NO2 vs CO {year_filter} (Peak Hours)")
fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.scatterplot(
    data=scaled_emisi, 
    x='NO2', 
    y='CO', 
    hue='Kategori', 
    style='Kategori', 
    s=100, 
    ax=ax2,
    palette=category_colors_emition
)
ax2.set_title('Scatter Plot of NO2 vs CO Levels by Station (Peak Hours)')
ax2.set_xlabel('NO2 (Normalized)')
ax2.set_ylabel('CO (Normalized)')
ax2.grid(True)
st.pyplot(fig2)

# Visualisasi Pie Chart
st.subheader(f"Distribution Category of NO2 & CO {year_filter} (Peak Hours)")
fig3, ax3 = plt.subplots(figsize=(8, 8))
scaled_emisi['Kategori'].value_counts().plot.pie(
    autopct='%1.1f%%',
    colors=[category_colors_emition[cat] for cat in scaled_emisi['Kategori'].value_counts().index],
    ax=ax3
)
ax3.set_title('Distribution of NO2 & CO Categories')
ax3.set_ylabel('')
st.pyplot(fig3)

# Informasi Tambahan
st.subheader("Legend")
st.markdown("""
#### PM2.5
- **High**: PM2.5 >= 80  
- **Moderate**: 60 <= PM2.5 < 80  
- **Low**: PM2.5 < 60
#### Emission
- **High**: NO2 > 0.7 or CO > 0.7  
- **Moderate**: NO2 > 0.4 or CO > 0.4  
- **Low**: NO2 <= 0.4 and CO <= 0.4
- **Peak Hours**: 7-9 AM & 5-7 PM
""")
