import discord
import asyncio
import random
import json
from datetime import datetime
from colorama import Fore, Style, init

# Inisialisasi colorama
init(autoreset=True)

# Load konfigurasi
with open('config.json', 'r') as f:
    config = json.load(f)

USER_TOKEN = config['token']  # User token, bukan bot token
CHANNEL_ID = config['channel_id']
MIN_DELAY = config['min_delay']
MAX_DELAY = config['max_delay']
AUTO_DELETE = config.get('auto_delete', False)
DELETE_AFTER = config.get('delete_after_seconds', 5)

# Load daftar pesan
with open('messages.txt', 'r', encoding='utf-8') as f:
    messages = [line.strip() for line in f if line.strip()]

# Variabel kontrol
running = True

# Inisialisasi client untuk user account
client = discord.Client()

def log(message, level="INFO"):
    """Fungsi logging dengan warna"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if level == "INFO":
        color = Fore.CYAN
    elif level == "SUCCESS":
        color = Fore.GREEN
    elif level == "WARNING":
        color = Fore.YELLOW
    elif level == "ERROR":
        color = Fore.RED
    else:
        color = Fore.WHITE
    
    print(f"{Fore.WHITE}[{timestamp}] {color}[{level}]{Style.RESET_ALL} {message}")

async def keyboard_listener():
    """Listener untuk mendeteksi keyboard interrupt"""
    global running
    try:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, input, f"{Fore.YELLOW}Tekan ENTER untuk menghentikan...{Style.RESET_ALL}\n")
        running = False
        log("Interrupt diterima! Menghentikan...", "WARNING")
    except Exception as e:
        log(f"Error di keyboard listener: {e}", "ERROR")

async def send_messages():
    """Fungsi utama untuk mengirim pesan"""
    global running
    await client.wait_until_ready()
    
    try:
        channel = await client.fetch_channel(CHANNEL_ID)
    except:
        log(f"Channel dengan ID {CHANNEL_ID} tidak ditemukan!", "ERROR")
        running = False
        return
    
    log(f"Siap kirim pesan! Channel target: #{channel.name}", "SUCCESS")
    log(f"Total pesan tersedia: {len(messages)}", "INFO")
    log(f"Delay: {MIN_DELAY}-{MAX_DELAY} detik", "INFO")
    log(f"Auto-delete: {'Aktif' if AUTO_DELETE else 'Nonaktif'}", "INFO")
    
    message_count = 0
    
    while running:
        try:
            # Pilih pesan random
            random_message = random.choice(messages)
            
            # Kirim pesan
            sent_message = await channel.send(random_message)
            message_count += 1
            
            log(f"Pesan #{message_count} terkirim: {random_message[:50]}...", "SUCCESS")
            
            # Auto delete jika diaktifkan
            if AUTO_DELETE:
                await asyncio.sleep(DELETE_AFTER)
                await sent_message.delete()
                log(f"Pesan #{message_count} dihapus setelah {DELETE_AFTER} detik", "INFO")
            
            # Random delay sebelum pesan berikutnya
            delay = random.uniform(MIN_DELAY, MAX_DELAY)
            log(f"Menunggu {delay:.2f} detik untuk pesan berikutnya...", "INFO")
            
            # Sleep dengan check running
            for _ in range(int(delay)):
                if not running:
                    break
                await asyncio.sleep(1)
            
        except discord.Forbidden:
            log("Tidak memiliki izin untuk mengirim/menghapus pesan!", "ERROR")
            running = False
        except discord.HTTPException as e:
            log(f"HTTP Error: {e}", "ERROR")
            await asyncio.sleep(5)
        except Exception as e:
            log(f"Error tidak terduga: {e}", "ERROR")
            await asyncio.sleep(5)
    
    log(f"Script dihentikan. Total pesan terkirim: {message_count}", "SUCCESS")
    await client.close()

@client.event
async def on_ready():
    """Event ketika user berhasil login"""
    log(f"Login sebagai {client.user.name}#{client.user.discriminator}", "SUCCESS")
    
    # Jalankan background tasks
    client.loop.create_task(send_messages())
    client.loop.create_task(keyboard_listener())

if __name__ == "__main__":
    try:
        log("Memulai Discord Auto Message (User Account)...", "INFO")
        client.run(USER_TOKEN)  # ✅ Langsung jalankan dengan token user
    except KeyboardInterrupt:
        log("Script dihentikan dengan Ctrl+C", "WARNING")
    except Exception as e:
        log(f"Error fatal: {e}", "ERROR")
