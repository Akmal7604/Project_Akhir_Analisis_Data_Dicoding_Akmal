import pandas as pd  
import seaborn as sns  
import matplotlib.pyplot as plt 
from cleaning_data import day_df, hour_df
from sklearn.model_selection import train_test_split  
from sklearn.linear_model import LinearRegression  


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