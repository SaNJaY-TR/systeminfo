import psutil
import platform
import subprocess
import re

def get_system_info():

    
    try:
        os_info = platform.uname()

        # Windows PowerShell komutu
        command = 'powershell "(Get-WmiObject Win32_Processor).Name"'
        output = subprocess.check_output(command, shell=True)
        cpu_info = output.decode('utf-8').strip()
        
        # Windows için
        if platform.system() == 'Windows':
            command = 'wmic path win32_VideoController get name'
            output = subprocess.check_output(command, shell=True)
            gpu_info = output.decode('utf-8').strip().split('\n')[1]
        # Linux için
        elif platform.system() == 'Linux':
            command = 'lspci | grep -i "VGA\|3D\|display"'
            output = subprocess.check_output(command, shell=True)
            gpu_info = output.decode('utf-8').strip().split(':')[2].strip()
        # Diğer işletim sistemleri için ekran kartı bilgisini alamıyoruz
                
        command = 'wmic memorychip get Manufacturer /format:list'
        output = subprocess.check_output(command, shell=True)
        ram_info = output.decode('utf-8').strip()
        # Dönüşüm yaparak daha okunabilir bir formata getirebilirsiniz
        ram_info_list = ram_info.split('\n')
        formatted_ram_info = {}
        for line in ram_info_list:
            key_value = line.split('=')
            if len(key_value) == 2:
                formatted_ram_info[key_value[0].strip()] = key_value[1].strip()
        
        mem_info = psutil.virtual_memory()

        command = 'wmic bios get SerialNumber, Manufacturer, SMBIOSBIOSVersion /format:list'
        output = subprocess.check_output(command, shell=True)
        bios_info = output.decode('utf-8').strip()
        # Dönüşüm yaparak daha okunabilir bir formata getirebilirsiniz
        bios_info_list = bios_info.split('\n')
        formatted_info = {}
        for line in bios_info_list:
            key_value = line.split('=')
            if len(key_value) == 2:
                formatted_info[key_value[0].strip()] = key_value[1].strip()
        
        command = 'wmic baseboard get Manufacturer, Product /format:list'
        output = subprocess.check_output(command, shell=True)
        mainboard_info = output.decode('utf-8').strip()
        # Dönüşüm yaparak daha okunabilir bir formata getirebilirsiniz
        mainboard_info_list = mainboard_info.split('\n')
        formatted_board_info = {}
        for line in mainboard_info_list:
            key_value = line.split('=')
            if len(key_value) == 2:
                formatted_board_info[key_value[0].strip()] = key_value[1].strip()        
        
        with open('log/sistem_bilgileri.txt', 'w') as file:
            file.write(f"isletim Sistemi:  {os_info.system} {os_info.release}\n")
            file.write(f"Sistem Sürümü: {os_info.release}\n")
            file.write(f"BIOS Bilgileri: {formatted_info.get('Manufacturer', 'Bilinmiyor')} {formatted_info.get('SMBIOSBIOSVersion', 'Bilinmiyor') }\n")
            file.write(f"İşlemci: {cpu_info}\n")
            file.write(f"Ekran Kartı: {gpu_info}\n")
            file.write(f"Anakart: {formatted_board_info.get('Manufacturer', 'Bilinmiyor')} {formatted_board_info.get('Product', 'Bilinmiyor')}\n")
            file.write(f"Ram Markası: {formatted_ram_info.get('Manufacturer', 'Bilinmiyor')}\n")
            file.write(f"Toplam RAM: {round(mem_info.total / (1024**3), 2)} GB\n")
            file.write("\n\n\n\n Bu Script Toplama Pc Forum'da kullanılmak üzere SaNJaY tarafından yazılmıştır.")

        print("Bilgiler başarıyla dosyaya yazıldı.")


    except Exception as e:
        print('Bilgileri alirken bir hata oluştu:', e)
        

get_system_info()
