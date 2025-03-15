from gathering_data import day_df, hour_df
import pandas as pd

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