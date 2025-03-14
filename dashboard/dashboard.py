import streamlit as st  
import pandas as pd  
import seaborn as sns  
import matplotlib.pyplot as plt  
from sklearn.model_selection import train_test_split  
from sklearn.linear_model import LinearRegression  

# Mengimport dataset
day_df = pd.read_csv("data\day.csv")
hour_df = pd.read_csv("data\hour.csv")

# Set display options to show all columns when describing  
pd.set_option('display.max_columns', None)  # This shows all columns  
pd.set_option('display.float_format', '{:.6f}'.format)  # Set float format for better readability  

def assess_data(df):  
    # 1. Menampilkan informasi dasar tentang dataset  
    print("Basic Information:")  
    print(df.info())  
    
    # 2. Cek missing values  
    print("\nMissing Values (detected as 0):")  
    missing_value_counts = (df == 0).sum()  
    print(missing_value_counts[missing_value_counts > 0])  # Hanya tampilkan kolom yang memiliki 0  
    
    # 3. Cek duplikat  
    print("\nDuplicate Entries:")  
    print(df.duplicated().sum())  
    
    # 4. Cek deskripsi statistik  
    print("\nDescriptive Statistics:")  
    print(df.describe(include='all'))  # Include 'all' to show statistics for all columns  
    
    # 5. Cek nilai invalid  
    print("\nInvalid Values Check:")  
    valid_season = [1, 2, 3, 4]  
    valid_year = [0, 1]    # 0: 2011, 1: 2012  
    valid_month = list(range(1, 13))  
    valid_weekday = list(range(0, 7))  
    valid_holiday = [0, 1]  
    valid_weathersit = [1, 2, 3, 4]  
    
    invalid_season = df[~df['season'].isin(valid_season)]['season'].count()  
    invalid_year = df[~df['yr'].isin(valid_year)]['yr'].count()  
    invalid_month = df[~df['mnth'].isin(valid_month)]['mnth'].count()  
    invalid_weekday = df[~df['weekday'].isin(valid_weekday)]['weekday'].count()  
    invalid_holiday = df[~df['holiday'].isin(valid_holiday)]['holiday'].count()  
    invalid_weathersit = df[~df['weathersit'].isin(valid_weathersit)]['weathersit'].count()  
    
    print(f"Invalid Seasons: {invalid_season}")  
    print(f"Invalid Years: {invalid_year}")  
    print(f"Invalid Months: {invalid_month}")  
    print(f"Invalid Weekdays: {invalid_weekday}")  
    print(f"Invalid Holidays: {invalid_holiday}")  
    print(f"Invalid Weather Situations: {invalid_weathersit}")  
    
    # 6. Cek outlier 1.5
    for column in ['temp', 'atemp', 'hum', 'windspeed', 'casual', 'registered', 'cnt']:  
        # Assuming outlier is defined as values beyond 1.5 * IQR from Q1 and Q3  
        Q1 = df[column].quantile(0.25)  
        Q3 = df[column].quantile(0.75)  
        IQR = Q3 - Q1  
        low_limit = Q1 - 1.5 * IQR  
        high_limit = Q3 + 1.5 * IQR  
        outliers_count = df[(df[column] < low_limit) | (df[column] > high_limit)][column].count()  
        print(f"Outliers in {column}: {outliers_count}")  
    
    # 6. Cek outlier 3
    for column in ['temp', 'atemp', 'hum', 'windspeed', 'casual', 'registered', 'cnt']:  
        # Assuming outlier is defined as values beyond 3 * IQR from Q1 and Q3  
        Q1 = df[column].quantile(0.25)  
        Q3 = df[column].quantile(0.75)  
        IQR = Q3 - Q1  
        low_limit = Q1 - 3 * IQR  
        high_limit = Q3 + 3 * IQR  
        outliers_count = df[(df[column] < low_limit) | (df[column] > high_limit)][column].count()  
        print(f"Outliers in {column}: {outliers_count}") 

    
# assess_data(day_df)
# Report:
#   - Missing value : 
#     - 1 hum, (untuk data 0 yang lain tidak perlu karena merupakan parameter)
#   - Invalid value : 0
#   - Duplicate data : 0
#   - Outlier 1.5 IQR: 
#     - casual : 44,
#     - hum : 2,
#     - windspeed : 13,
#   - Outlier 3 IQR: 0

# assess_data(hour_df)
# Report:
#   - Missing value : 
#     - 22 hum,
#     - 2180 windspeed,
#     - 2 atemp,
#     - (untuk data 0 yang lain tidak perlu karena merupakan parameter/ perhitungan pelanggan yang logis apabila data nya 0)
#   - Invalid value : 0
#   - Duplicate data : 0
#   - Outlier 1.5 IQR : 
#     - casual : 1192,
#     - hum : 22,
#     - windspeed : 342,
#     - cnt : 505
#     - registered : 680
#   - Outlier 3 IQR : 
#     - casual : 491,
#     - windspeed : 10,
#     - registered : 45

# Berdasarkan report yang diambil dari proses assessing data, saya mendapatkan 2 hal yang perlu saya perbaiki, yaitu:
# 1. Melakukan metode (imputation) untuk missing value. Metode ini saya pilih dengan pertimbangan untuk menjawab kedua pertanyaan bisnis yang ada.
# 2. Mengatasi nilai outlier yang ada pada proses assessing data, tentunya setelah mengatasi missing value. 
# 3. Nilai outlier yang ada pada casual, registered, dan cnt terjadi karena ada kesalahan pada dataset hour.csv dimana pengumpulan data dilakukan dalam waktu kurang dari 24 jam.

# Imputasi pada day_df  
print("Handling Missing Values for day_df:")  

# Mengganti nilai 0 di kolom 'hum' dengan median  
if (day_df['hum'] == 0).any():  # Cek apakah ada nilai 0 di 'hum'  
    median_hum_day = day_df['hum'].median()  
    day_df['hum'].replace(0, median_hum_day, inplace=True)  # Ganti 0 dengan median  
    print(f"Replaced 0 values in 'hum' with median: {median_hum_day}")  

# Imputasi pada hour_df  
print("\nHandling Missing Values for hour_df:")  

# Mengganti nilai 0 di kolom 'hum' dengan median  
if (hour_df['hum'] == 0).any():  
    median_hum_hour = hour_df['hum'].median()  
    hour_df['hum'].replace(0, median_hum_hour, inplace=True)  
    print(f"Replaced 0 values in 'hum' with median: {median_hum_hour}")  

# Mengganti nilai 0 di kolom 'atemp' dengan median  
if (hour_df['atemp'] == 0).any():  
    median_atemp_hour = hour_df['atemp'].median()  
    hour_df['atemp'].replace(0, median_atemp_hour, inplace=True)  
    print(f"Replaced 0 values in 'atemp' with median: {median_atemp_hour}")  

# Mengganti nilai 0 di kolom 'windspeed' dengan median  
if (hour_df['windspeed'] == 0).any():  
    median_windspeed_hour = hour_df['windspeed'].median()  
    hour_df['windspeed'].replace(0, median_windspeed_hour, inplace=True)  
    print(f"Replaced 0 values in 'windspeed' with median: {median_windspeed_hour}")   

# Menghapus tanggal yang tidak memiliki 24 entri di hour_df dari day_df dan hour_df  
print("\nRemoving dates with less than 24 entries in hour_df:")  

# Mendapatkan jumlah entri per tanggal  
hour_counts = hour_df['dteday'].value_counts()  

# Menentukan tanggal-tanggal yang memiliki kurang dari 24 entri  
dates_to_remove = hour_counts[hour_counts < 24].index.tolist()  

# Menghapus tanggal tersebut dari hour_df  
hour_df = hour_df[~hour_df['dteday'].isin(dates_to_remove)]  

# Menghapus tanggal yang sama dari day_df  
day_df = day_df[~day_df['dteday'].isin(dates_to_remove)]  

print(f"Removed dates: {dates_to_remove}")  
print(f"Remaining entries in hour_df: {len(hour_df)}")  
print(f"Remaining entries in day_df: {len(day_df)}")  


# Cek apakah masih ada missing values
# assess_data(day_df)
# Report:
#   - Missing value : 0
#     - (untuk data 0 yang lain tidak perlu karena merupakan parameter)
#   - Invalid value : 0
#   - Duplicate data : 0
#   - Outlier IQR 1.5: 
#     - casual : 41,
#     - windspeed : 16,
#     - hum : 1,
#   - Outlier IQR 3: 0

# assess_data(hour_df)
# Report:
#   - Missing value : 0
#     - (untuk data 0 yang lain tidak perlu karena merupakan parameter/ perhitungan pelanggan yang logis apabila data nya 0)
#   - Invalid value : 0
#   - Duplicate data : 0
#   - Outlier IQR 1.5: 
#     - casual : 1038,
#     - windspeed : 578,
#     - cnt : 398
#     - registered : 591
#   - Outlier IQR 3: 
#     - casual : 394,
#     - windspeed : 51,
#     - registered : 23

# Pertanyaan:
# 1. Bagaimana pola cuaca (temperatur, kelembapan, kecepatan angin) mempengaruhi jumlah penyewaan sepeda dan 
# 2. Bagaimana kita dapat mengategorikan penyewaan sepeda berdasarkan musim dan hari dalam seminggu untuk memahami tren penyewaan?
# 3. Hari apa yang memiliki jumlah penyewaan yang tidak biasa?
# 3. apakah kita dapat memprediksi jumlah penyewaan berdasarkan kondisi cuaca saat ini?
# 4. Apa pola musiman dalam penyewaan sepeda? Bagaimana frekuensi penyewaan berubah dari satu musim ke musim lainnya?

def plot_weather_vs_rentals(day_df):  
    plt.figure(figsize=(12, 8))  
    
    # Scatter plot untuk melihat hubungan temperatur dan jumlah penyewaan  
    sns.scatterplot(data=day_df, x='temp', y='cnt', label='Temperature')  
    
    # Scatter plot untuk kelembaban  
    sns.scatterplot(data=day_df, x='hum', y='cnt', color='orange', label='Humidity')  
    
    # Scatter plot untuk kecepatan angin  
    sns.scatterplot(data=day_df, x='windspeed', y='cnt', color='green', label='Windspeed')  
    
    plt.title('Pola Cuaca vs. Jumlah Penyewaan Sepeda')  
    plt.xlabel('Cuaca (Normalized)')  
    plt.ylabel('Jumlah Penyewaan Sepeda (cnt)')  
    plt.legend()  
    plt.show()  

# Fungsi 2: Mengategorikan Penyewaan Berdasarkan Musim dan Hari  
def plot_seasonal_trends(day_df):  
    plt.figure(figsize=(12, 6))  
    
    # Boxplot untuk membandingkan penyewaan berdasarkan musim  
    sns.boxplot(data=day_df, x='season', y='cnt')  
    plt.title('Jumlah Penyewaan Sepeda berdasarkan Musim')  
    plt.xlabel('Musim')  
    plt.ylabel('Jumlah Penyewaan (cnt)')  
    plt.xticks([0, 1, 2, 3], ['Musim Dingin', 'Musim Semi', 'Musim Panas', 'Musim Gugur'])  
    plt.show()  
    
    # Menampilkan tren penyewaan berdasarkan hari dalam seminggu  
    plt.figure(figsize=(12, 6))  
    sns.boxplot(data=day_df, x='weekday', y='cnt')  
    plt.title('Jumlah Penyewaan Sepeda berdasarkan Hari dalam Seminggu')  
    plt.xlabel('Hari dalam Seminggu')  
    plt.ylabel('Jumlah Penyewaan (cnt)')  
    plt.xticks([0, 1, 2, 3, 4, 5, 6], ['Minggu','Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'])  
    plt.show()  
    
# Fungsi 3: Menemukan Hari-Hari dengan Penyewaan yang Tidak Biasa  
def identify_unusual_days(day_df):  
    mean_count = day_df['cnt'].mean()  
    std_count = day_df['cnt'].std()  
    
    # Identifikasi hari-hari dengan penyewaan luar biasa  
    unusual_days = day_df[(day_df['cnt'] > mean_count + 2 * std_count) |   
                          (day_df['cnt'] < mean_count - 2 * std_count)]  
    
    print("Hari-hari dengan penyewaan yang tidak biasa:")  
    print(unusual_days[['dteday', 'cnt']]) 
        
# Fungsi 4: Memprediksi Jumlah Penyewaan Berdasarkan Cuaca  
def predict_rentals(day_df, tempr, humid, wind):  
    features = day_df[['temp', 'hum', 'windspeed']]  
    target = day_df['cnt']  
    
    # Split data into training and testing set  
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)  
    
    # Create and fit the model  
    model = LinearRegression()  
    model.fit(X_train, y_train)  
    
    score = model.score(X_test, y_test)  
    print(f"Model R^2 Score: {score:.2f}")  

    sample_data = pd.DataFrame({'temp': [(tempr/41)], 'hum': [(humid/100)], 'windspeed': [(wind/67)]})  
    prediction = model.predict(sample_data)  
    print(f"Prediksi jumlah penyewaan: {prediction[0]:.2f}")  

# Fungsi 5: Pola Musiman Penyewaan Sepeda  
def seasonal_patterns(day_df):  
    seasonal_counts = day_df.groupby('season')['cnt'].mean()  
    
    plt.figure(figsize=(8, 6))  
    sns.barplot(x=seasonal_counts.index, y=seasonal_counts.values)  
    plt.title('Pola Musiman Penyewaan Sepeda')  
    plt.xlabel('Musim')  
    plt.ylabel('Rata-rata Jumlah Penyewaan (cnt)')  
    plt.xticks([0, 1, 2, 3], ['Musim Dingin', 'Musim Semi', 'Musim Panas', 'Musim Gugur'])  
    plt.show()  

# Menjalankan Eksplorasi  
plot_weather_vs_rentals(day_df)  
plot_seasonal_trends(day_df)  
identify_unusual_days(day_df)
predict_rentals(day_df, 26, 100, 20)  
seasonal_patterns(day_df)  

# Report:
# 1. Pola Cuaca vs. Jumlah Penyewaan Sepeda: Peningkatan temperatur cenderung meningkatkan jumlah penyewaan sepeda, sedangkan kelembaban yang lebih tinggi dapat 
# mengurangi minat orang untuk menyewa sepeda.
# 
# 2. Tren Penyewaan Berdasarkan Musim dan Hari dalam Seminggu: Analisis menunjukkan bahwa musim panas memiliki jumlah penyewaan tertinggi, 
# sedangkan musim dingin biasanya memiliki penyewaan yang rendah. Ini menunjukkan preferensi pengguna atau pengaruh cuaca yang lebih baik pada saat musim panas. 
# Sementara hari dalam seminggu, haru sabtu cenderung memiliki jumlah penyewaan yang lebih tinggi daripada hari-hari lainnya.
# 
# 3. Prediksi jumlah penyewaan berdasarkan cuaca saat ini: 
#          dteday   cnt
# 0    2011-01-01   985
# 7    2011-01-08   959
# 8    2011-01-09   822
# 16   2011-01-17  1000
# 35   2011-02-05  1005
# 51   2011-02-21  1107
# 105  2011-04-16   795
# 301  2011-10-29   627
# 340  2011-12-07   705
# 357  2011-12-24  1011
# 360  2011-12-27  1162
# 477  2012-04-22  1027
# 623  2012-09-15  8714
# 630  2012-09-22  8395
# 637  2012-09-29  8555
# 725  2012-12-26   441
# Pada tanggal - tanggal seperti 15, 22, dan 29 September 2012, jumlah penyewaan sepeda sangat tinggi, dari jam 8 pagi hingga jam 11 malam. Kejadian tersebut ketiganya terjadi pada hari
# sabtu yang dimana terdapat cuaca yang cerah (level 1), suhu yang tinggi, kelembaban yang moderat dan kecepatan angin yang sedang. Selain itu, terdapat acara H festival yang diselenggarakan di
# Washington DC.
# Sementara pada tanggal 26 Desember 2012, Jumlah penyewaan sepeda sangat rendah, dari jam 6 pagi hingga jam 11 malam. Kejadian tersebut terjadi pada hari senin yang dimana temperatur
# sangatlah rendah, cuaca level 3 (Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered), humidity yang lebih tinggi dari biasanya, dan wind speed yang sedang.
# 
# 4. Prediksi jumlah penyewaan berdasarkan cuaca saat ini: Model regresi linier memberikan skor R^2 sebesar 0.32, yang berarti model dapat menjelaskan 32% variabilitas dalam data,
# ketika temperatur lebih rendah, kelembapan lebih tinggi, dan keceparan angin lebih tinggi, maka jumlah penyewaan sepeda akan lebih rendah. Dan sebaliknya.
# 
# 5. Pola Musiman Penyewaan Sepeda: Pola musiman penyewaan sepeda menunjukkan bahwa musim panas memiliki jumlah penyewaan tertinggi, diikuti oleh musim semi, musim gugur, dan musim dingin
# sebagai musim dengan penyewaan terendah. Ini menunjukkan preferensi pengguna atau pengaruh cuaca yang lebih baik pada saat musim panas.

# Fungsi untuk membuat visualisasi pola penyewaan berdasarkan musim  
def plot_seasonal_rentals(day_df):  
    seasonal_counts = day_df.groupby('season')['cnt'].sum()  
    
    # Membuat bar plot untuk jumlah penyewaan berdasarkan musim  
    plt.figure(figsize=(10, 6))  
    bars = plt.bar(seasonal_counts.index, seasonal_counts.values)  
    plt.title('Jumlah Penyewaan Sepeda Berdasarkan Musim')  
    plt.xlabel('Musim')  
    plt.ylabel('Jumlah Penyewaan (cnt)')  
    plt.xticks([1, 2, 3, 4], ['Musim Dingin', 'Musim Semi', 'Musim Panas', 'Musim Gugur'])  

    # Menetapkan warna berdasarkan musim  
    colors = ['blue', 'orange', 'red', 'black']  
    for bar, color in zip(bars, colors):  
        bar.set_color(color)  

    plt.show()  
    
    # Penjelasan di bawah grafik  
    print("\nSetelah menganalisis total penyewaan berdasarkan musim, kita dapat mengamati pola yang jelas:",
          "\n-Musim Panas: Memiliki jumlah penyewaan tertinggi. Ini mungkin menunjukkan bahwa cuaca yang lebih hangat mendorong lebih banyak orang untuk bersepeda.",
          "\n-Musim Dingin: Biasanya memiliki penyewaan terendah. Hal ini dapat diakibatkan oleh cuaca yang kurang mendukung untuk beraktivitas luar ruangan.")

# Fungsi untuk menganalisis pengaruh faktor cuaca  
def plot_weather_influence(day_df):  
    # Temperatur vs Jumlah Penyewaan  
    plt.figure(figsize=(10, 6))  
    plt.scatter(day_df['temp'], day_df['cnt'], alpha=0.5)  
    plt.title('Hubungan Temperatur vs. Jumlah Penyewaan Sepeda')  
    plt.xlabel('Temperatur (Normalized)')  
    plt.ylabel('Jumlah Penyewaan (cnt)')  
    plt.grid()  
    plt.show()  
    
    print("Peningkatan temperatur cenderung meningkatkan jumlah penyewaan sepeda, namun dengan pengecualian peningkatan temperatur yang cukup ekstrim cenderung menurunkan jumlah penyewaan sepeda.")  

    # Kelembaban vs Jumlah Penyewaan  
    plt.figure(figsize=(10, 6))  
    plt.scatter(day_df['hum'], day_df['cnt'], alpha=0.5, color='orange')  
    plt.title('Hubungan Kelembaban vs. Jumlah Penyewaan Sepeda')  
    plt.xlabel('Kelembaban (Normalized)')  
    plt.ylabel('Jumlah Penyewaan (cnt)')  
    plt.grid()  
    plt.show()  

    print("\nDari data yang ada, kira dapat melihat bahwa pesepeda lebih menyukai kelembapan yang moderat dari rentang 0,4 hingga 0,8 dengan tingkat penyewaan tertinggi berada pada rentang 0,5.",
          "\nKelembapan yang terlalu tinggi atau terlalu rendah dapat mengurangi jumlah penyewaan sepeda karena cuaca yang lembap biasanya kurang nyaman untuk aktivitas di luar",
          "\ndan cuaca yang terlalu kering juga dapat mengurangi kenyamanan pengguna dalam bersepeda.")  

    # Kecepatan Angin vs Jumlah Penyewaan  
    plt.figure(figsize=(10, 6))  
    plt.scatter(day_df['windspeed'], day_df['cnt'], alpha=0.5, color='green')  
    plt.title('Hubungan Kecepatan Angin vs. Jumlah Penyewaan Sepeda')  
    plt.xlabel('Kecepatan Angin (Normalized)')  
    plt.ylabel('Jumlah Penyewaan (cnt)')  
    plt.grid()  
    plt.show()  
 
    print("\nSementara itu, kecepatan angin yang lebih tinggi mungkin mengurangi minat mayoritas pengguna untuk menyewa sepeda.")  

# Menjalankan visualisasi  
plot_seasonal_rentals(day_df)  
plot_weather_influence(day_df)  

# Fungsi untuk memplot hubungan cuaca vs penyewaan  
def plot_weather_vs_rentals(day_df):  
    plt.figure(figsize=(12, 8))  
    
    # Scatter plot untuk melihat hubungan temperatur dan jumlah penyewaan  
    sns.scatterplot(data=day_df, x='temp', y='cnt', label='Temperature')  
    
    # Scatter plot untuk kelembaban  
    sns.scatterplot(data=day_df, x='hum', y='cnt', color='orange', label='Humidity')  
    
    # Scatter plot untuk kecepatan angin  
    sns.scatterplot(data=day_df, x='windspeed', y='cnt', color='green', label='Windspeed')  
    
    plt.title('Pola Cuaca vs. Jumlah Penyewaan Sepeda')  
    plt.xlabel('Cuaca (Normalized)')  
    plt.ylabel('Jumlah Penyewaan Sepeda (cnt)')  
    plt.legend()  
    st.pyplot(plt)  

# Fungsi untuk memplot tren musiman  
def plot_seasonal_trends(day_df):  
    plt.figure(figsize=(12, 6))  
    
    # Boxplot untuk membandingkan penyewaan berdasarkan musim  
    sns.boxplot(data=day_df, x='season', y='cnt')  
    plt.title('Jumlah Penyewaan Sepeda berdasarkan Musim')  
    plt.xlabel('Musim')  
    plt.ylabel('Jumlah Penyewaan (cnt)')  
    plt.xticks([0, 1, 2, 3], ['Musim Dingin', 'Musim Semi', 'Musim Panas', 'Musim Gugur'])  
    st.pyplot(plt)  

    # Menampilkan tren penyewaan berdasarkan hari dalam seminggu  
    plt.figure(figsize=(12, 6))  
    sns.boxplot(data=day_df, x='weekday', y='cnt')  
    plt.title('Jumlah Penyewaan Sepeda berdasarkan Hari dalam Seminggu')  
    plt.xlabel('Hari dalam Seminggu')  
    plt.ylabel('Jumlah Penyewaan (cnt)')  
    plt.xticks([0, 1, 2, 3, 4, 5, 6], ['Minggu','Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'])  
    st.pyplot(plt)   

# Fungsi 3: Menemukan Hari-Hari dengan Penyewaan yang Tidak Biasa  
def identify_unusual_days(day_df):  
    mean_count = day_df['cnt'].mean()  
    std_count = day_df['cnt'].std()  
    
    # Identifikasi hari-hari dengan penyewaan luar biasa  
    unusual_days = day_df[(day_df['cnt'] > mean_count + 2 * std_count) |   
                          (day_df['cnt'] < mean_count - 2 * std_count)]  
    
    return unusual_days[['dteday', 'cnt']]  # Mengembalikan DataFrame  

# Fungsi untuk memprediksi jumlah penyewaan  
def predict_rentals(temp, humid, wind):  
    features = day_df[['temp', 'hum', 'windspeed']]  
    target = day_df['cnt']  
    
    # Split data into training and testing set  
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)  
    
    # Create and fit the model  
    model = LinearRegression()  
    model.fit(X_train, y_train)  
    r_squared = model.score(X_test, y_test)  # Mendapatkan skor R^2  

    # Normalisasi input berdasarkan rentang data pelatihan  
    temp_normalized = (temp + 40) / 81  # Normalisasi temperatur ke rentang [0, 1]  
    humid_normalized = humid / 100  # Sudah dalam rentang [0, 1]  
    wind_normalized = wind / 67  # Normalisasi ke rentang [0, 1]  
    
    sample_data = pd.DataFrame({'temp': [temp_normalized], 'hum': [humid_normalized], 'windspeed': [wind_normalized]})  
    prediction = model.predict(sample_data)  

    return prediction[0], r_squared  # Mengembalikan hasil prediksi dan R^2  
###############################################################################################
# import streamlit as st  
# import pandas as pd  
# import seaborn as sns  
# import matplotlib.pyplot as plt  
# from sklearn.model_selection import train_test_split  
# from sklearn.linear_model import LinearRegression   

# ================== FUNGSI UTAMA ================== #  
def plot_weather_vs_rentals(df):  
    plt.figure(figsize=(12, 8))  
    sns.scatterplot(data=df, x='temp', y='cnt', label='Temperature')  
    sns.scatterplot(data=df, x='hum', y='cnt', color='orange', label='Humidity')  
    sns.scatterplot(data=df, x='windspeed', y='cnt', color='green', label='Windspeed')  
    plt.title('Pola Cuaca vs. Jumlah Penyewaan Sepeda')  
    plt.xlabel('Cuaca (Normalized)')  
    plt.ylabel('Jumlah Penyewaan Sepeda (cnt)')  
    plt.legend()  
    st.pyplot(plt)  

def plot_seasonal_trends(df):  
    season_mapping = {1: "Dingin", 2: "Semi", 3: "Panas", 4: "Gugur"}  
    df['Musim'] = df['season'].map(season_mapping)  
    
    plt.figure(figsize=(12, 6))  
    sns.boxplot(data=df, x='Musim', y='cnt')  
    plt.title('Jumlah Penyewaan Sepeda berdasarkan Musim')  
    plt.xlabel('Musim')  
    plt.ylabel('Jumlah Penyewaan (cnt)')  
    st.pyplot(plt)  

    plt.figure(figsize=(12, 6))  
    sns.boxplot(data=df, x='weekday', y='cnt')  
    plt.title('Jumlah Penyewaan Sepeda berdasarkan Hari dalam Seminggu')  
    plt.xlabel('Hari dalam Seminggu')  
    plt.ylabel('Jumlah Penyewaan (cnt)')  
    plt.xticks([0, 1, 2, 3, 4, 5, 6], ['Minggu','Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'])  
    st.pyplot(plt)  

def identify_unusual_days(df):  
    mean_count = df['cnt'].mean()  
    std_count = df['cnt'].std()  
    unusual_days = df[(df['cnt'] > mean_count + 2 * std_count) |   
                      (df['cnt'] < mean_count - 2 * std_count)]  
    return unusual_days[['dteday', 'cnt']]  

def predict_rentals(temp, humid, wind, df):  
    features = df[['temp', 'hum', 'windspeed']]  
    target = df['cnt']  
    
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)  
    
    model = LinearRegression()  
    model.fit(X_train, y_train)  
    r_squared = model.score(X_test, y_test)  

    # Normalisasi input  
    temp_normalized = (temp + 40) / 81  
    humid_normalized = humid / 100  
    wind_normalized = wind / 67  
    
    sample_data = pd.DataFrame({  
        'temp': [temp_normalized],  
        'hum': [humid_normalized],  
        'windspeed': [wind_normalized]  
    })  
    
    prediction = model.predict(sample_data)  
    return prediction[0], r_squared  

# ================== KONFIGURASI FILTER ================== #  
st.sidebar.header("Filter Data")  

# Konversi tanggal  
day_df['dteday'] = pd.to_datetime(day_df['dteday'])  
min_date = day_df['dteday'].min().date()  
max_date = day_df['dteday'].max().date()  

# Widget filter  
selected_dates = st.sidebar.date_input(  
    "Rentang Tanggal",  
    value=(min_date, max_date),  
    min_value=min_date,  
    max_value=max_date  
)  

season_options = {  
    1: "🛷 Musim Dingin",  
    2: "🌸 Musim Semi",  
    3: "🏖️ Musim Panas",  
    4: "🍂 Musim Gugur"  
}  
selected_seasons = st.sidebar.multiselect(  
    "Pilih Musim",  
    options=list(season_options.values()),  
    default=list(season_options.values())  
)  

weather_options = {  
    1: "☀️ Cerah",  
    2: "⛅ Berawan",  
    3: "🌧️ Hujan/Salju"  
}  
selected_weather = st.sidebar.multiselect(  
    "Kondisi Cuaca",  
    options=list(weather_options.values()),  
    default=list(weather_options.values())  
)  

# ================== PROSES FILTERING ================== #  
filtered_df = day_df.copy()  

# Filter tanggal  
if len(selected_dates) == 2:  
    filtered_df = filtered_df[  
        (filtered_df['dteday'].dt.date >= selected_dates[0]) &  
        (filtered_df['dteday'].dt.date <= selected_dates[1])  
    ]  

# Filter musim  
season_codes = [k for k,v in season_options.items() if v in selected_seasons]  
filtered_df = filtered_df[filtered_df['season'].isin(season_codes)]  

# Filter cuaca  
weather_codes = [k for k,v in weather_options.items() if v in selected_weather]  
filtered_df = filtered_df[filtered_df['weathersit'].isin(weather_codes)]  

# ================== TAMPILAN DASHBOARD ================== #  
st.title("🚴 Dashboard Analisis Penyewaan Sepeda")  

# Panel informasi filter  
st.subheader("🔍 Filter Aktif")  
col1, col2, col3 = st.columns(3)  
with col1:  
    st.metric("Rentang Tanggal", f"{selected_dates[0]} - {selected_dates[1]}")  
with col2:  
    st.metric("Musim Terpilih", ", ".join(selected_seasons))  
with col3:  
    st.metric("Kondisi Cuaca", ", ".join(selected_weather))  

# Visualisasi  
st.subheader("📈 Analisis Pola Penyewaan")  
plot_weather_vs_rentals(filtered_df)  

st.subheader("📅 Tren Musiman dan Harian")  
plot_seasonal_trends(filtered_df)  

st.subheader("❗ Hari dengan Aktivitas Tidak Biasa")  
unusual_days = identify_unusual_days(filtered_df)  
st.dataframe(unusual_days.style.highlight_max(color='#90EE90').highlight_min(color='#FFCCCB'))  

# Prediksi  
st.subheader("🔮 Prediksi Penyewaan")  
temp_input = st.slider("Temperatur (°C)", -20, 50, 25)  
humid_input = st.slider("Kelembaban (%)", 0, 100, 60)  
wind_input = st.slider("Kecepatan Angin (km/jam)", 0, 100, 15)  

if st.button("Lakukan Prediksi"):  
    prediction, r2 = predict_rentals(temp_input, humid_input, wind_input, filtered_df)  
    st.success(f"Prediksi jumlah penyewaan: **{prediction:.0f}** sepeda")  
    st.metric("Akurasi Model (R²)", f"{r2:.2%}")  
    st.progress(r2)  