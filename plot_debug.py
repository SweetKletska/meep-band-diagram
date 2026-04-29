import matplotlib.pyplot as plt
import numpy as np

# Пытаемся загрузить данные
try:
    # Пробуем разные варианты
    import os
    if os.path.exists('frequencies_real.txt'):
        filename = 'frequencies_real.txt'
    elif os.path.exists('fre.dat'):
        filename = 'fre.dat'
    else:
        print("ОШИБКА: Не найден файл с данными!")
        print("Файлы в папке:", os.listdir('.'))
        exit(1)
    
    print(f"Загружаем {filename}...")
    
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    print(f"Всего строк в файле: {len(lines)}")
    
    # Парсим строки
    kx_list = []
    freq_list = []
    
    for line_idx, line in enumerate(lines):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        # Убираем "freqs:," если есть
        if line.startswith('freqs:'):
            line = line[6:]  # убираем "freqs:"
        if line.startswith(','):
            line = line[1:]  # убираем запятую
        
        parts = line.split(',')
        
        # Печатаем первые несколько строк для отладки
        if line_idx < 3:
            print(f"Строка {line_idx}: {len(parts)} частей")
            print(f"  {parts[:5]}...")
        
        if len(parts) >= 5:
            try:
                kx = float(parts[1])  # второй столбец
                # Частоты с 5-го столбца
                for i in range(4, len(parts)):
                    freq = float(parts[i])
                    if 0 < freq < 1.0:  # все положительные частоты
                        kx_list.append(kx)
                        freq_list.append(freq)
            except ValueError as e:
                print(f"Ошибка в строке {line_idx}: {e}")
                continue
    
    print(f"\nЗагружено точек: {len(kx_list)}")
    
    if len(kx_list) == 0:
        print("\nНЕТ ДАННЫХ ДЛЯ ГРАФИКА!")
        print("Проверьте формат файла. Первые 3 строки:")
        for i in range(min(3, len(lines))):
            print(f"  {lines[i][:100]}")
        exit(1)
    
    print(f"Диапазон kx: от {min(kx_list):.3f} до {max(kx_list):.3f}")
    print(f"Диапазон частот: от {min(freq_list):.3f} до {max(freq_list):.3f}")
    
    # Строим график
    plt.figure(figsize=(12, 8))
    plt.plot(kx_list, freq_list, 'bo', markersize=4, alpha=0.7)
    
    # Световой конус
    kx_light = np.linspace(0, 0.5, 100)
    plt.fill_between(kx_light, kx_light, 1.0, color='gray', alpha=0.3)
    
    plt.xlabel('kₓ (2π/a)', fontsize=14)
    plt.ylabel('ω (2πc/a)', fontsize=14)
    plt.title('Band Diagram', fontsize=16)
    plt.xlim(0, 0.5)
    plt.ylim(0, 0.6)
    plt.grid(True, alpha=0.3)
    
    plt.savefig('band_diagram_debug.png', dpi=150)
    print("\n✓ График сохранен как 'band_diagram_debug.png'")
    plt.show()
    
except Exception as e:
    print(f"ОШИБКА: {e}")
    import traceback
    traceback.print_exc()