# Discord Auto Sender

## Cara Penggunaan
1. Install dependencies:​
```bash
pip install -r requirements.txt
```
2. Konfigurasi:​

- Edit config.json dan masukkan token Discord kamu
- Masukkan channel ID tujuan (aktifkan Developer Mode di Discord untuk copy ID)
- Atur delay minimum dan maksimum (dalam detik)
- Set auto_delete ke true jika ingin pesan otomatis terhapus

3. Tambahkan pesan:​

- Edit messages.txt dan tambahkan pesan-pesan yang ingin dikirim (satu pesan per baris)

4. Jalankan bot:​
```bash
python main.py
```
5. Untuk menghentikan:​

- Tekan ENTER di terminal, atau
- Tekan Ctrl+C untuk force stop

## Fitur Utama
- Random Message: Bot memilih pesan secara acak dari messages.txt​
- Random Delay: Waktu tunggu antar pesan bervariasi antara min_delay dan max_delay​
- Auto Delete (Opsional): Pesan akan otomatis terhapus setelah durasi yang ditentukan jika fitur diaktifkan​
- Colorful Logs: Log berwarna untuk memudahkan monitoring​
- Graceful Shutdown: Bot dapat dihentikan dengan ENTER atau Ctrl+C tanpa error​
- Error Handling: Menangani berbagai error Discord API dengan retry mechanism​