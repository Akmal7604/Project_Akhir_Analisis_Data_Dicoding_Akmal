import streamlit as st  
import pandas as pd  
import seaborn as sns  
import matplotlib.pyplot as plt  
from sklearn.model_selection import train_test_split  
from sklearn.linear_model import LinearRegression  
from cleaning_data import day_df, hour_df  

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

# Judul Dashboard  
st.title("Dashboard Penyewaan Sepeda")  

# Menampilkan visualisasi hubungan cuaca dan penyewaan sepeda  
st.subheader("Pola Cuaca vs. Jumlah Penyewaan Sepeda")  
plot_weather_vs_rentals(day_df)  
st.write("""  
    Grafik di atas menunjukkan hubungan antara variabel cuaca (temperatur, kelembaban, dan kecepatan angin) dan jumlah penyewaan sepeda.  
    Dapat dilihat bahwa temperatur yang tinggi, kelembapan yang moderat, dan kecepatan angin yang rendah akan meningkatkan tingkat penyewaan sepeda, begitu juga sebaliknya.  
""")  

# Menampilkan tren musiman  
st.subheader("Tren Penyewaan Berdasarkan Musim dan Hari dalam Seminggu")  
plot_seasonal_trends(day_df)  
st.write("""  
    Boxplot di bagian atas menunjukkan jumlah penyewaan sepeda berdasarkan musim. Musim panas memiliki jumlah penyewaan tertinggi, diikuti oleh musim semi, musim gugur, dan musim dingin.  

    Sedangkan Boxplot di bagian bawah menunjukkan tren penyewaan berdasarkan hari dalam seminggu. Hari Sabtu cenderung memiliki jumlah penyewaan yang lebih tinggi dibandingkan hari lainnya.  
""")  

# Menampilkan hari-hari penyewaan tidak biasa  
st.subheader("Hari-Hari dengan Penyewaan yang Tidak Biasa")  
unusual_days_df = identify_unusual_days(day_df)  
st.write(unusual_days_df)  
st.write("""  
    Tabel di atas menunjukkan hari-hari dengan penyewaan yang tidak biasa, baik itu sangat tinggi maupun sangat rendah.
    
    Pada tanggal - tanggal seperti 15, 22, dan 29 September 2012, jumlah penyewaan sepeda sangat tinggi, dari jam 8 pagi hingga jam 11 malam. Kejadian tersebut ketiganya terjadi pada hari sabtu yang dimana terdapat cuaca yang cerah (level 1), suhu yang tinggi, kelembaban yang moderat dan kecepatan angin yang sedang. Selain itu, terdapat acara H festival yang diselenggarakan di Washington DC.
    Sementara pada tanggal 26 Desember 2012, Jumlah penyewaan sepeda sangat rendah, dari jam 6 pagi hingga jam 11 malam. Kejadian tersebut terjadi pada hari senin yang dimana temperatur sangatlah rendah, cuaca level 3 (Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered), humidity yang lebih tinggi dari biasanya, dan wind speed yang sedang.
""")  

# Input untuk prediksi  
st.subheader("Prediksi Jumlah Penyewaan Berdasarkan Cuaca Saat Ini")  
temp_input = st.slider("Temperatur (Celcius)", min_value=-20, max_value=100, value=26)  
humid_input = st.slider("Kelembaban (%)", min_value=0, max_value=100, value=80)  
wind_input = st.slider("Kecepatan Angin (Km/h)", min_value=0, max_value=50, value=20)  

if st.button("Prediksi"):  
    prediction_result, r_squared = predict_rentals(temp_input, humid_input, wind_input)  
    st.write(f"Prediksi jumlah penyewaan sepeda: {prediction_result:.2f}")  
    st.write(f"Skor R^2 dari model: {r_squared:.2f}")  
    st.write("""  
        Skor R² menunjukkan seberapa baik model dapat menjelaskan variabilitas dalam data.   
        Nilai R² mendekati 1 berarti model sangat baik dalam memprediksi jumlah penyewaan berdasarkan cuaca saat ini.  
    """)  