import pandas as pd  
import matplotlib.pyplot as plt  
import seaborn as sns  
from cleaning_data import day_df, hour_df

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