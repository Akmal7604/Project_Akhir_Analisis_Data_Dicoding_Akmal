from gathering_data import day_df, hour_df
import pandas as pd
from assessing_data import assess_data

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


