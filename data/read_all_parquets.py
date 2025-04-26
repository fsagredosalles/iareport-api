import os
import pandas as pd

# Directorio donde están los archivos Parquet
data_dir = r"C:\Users\Chinopio\Desktop\IAReport\apps\api\data"

# Obtener lista de archivos Parquet en la carpeta
parquet_files = [f for f in os.listdir(data_dir) if f.endswith(".parquet")]

# Iterar sobre cada archivo Parquet
for file_name in parquet_files:
    file_path = os.path.join(data_dir, file_name)
    print(f"\nLeyendo archivo: {file_name}")
    
    try:
        # Leer el archivo Parquet
        df = pd.read_parquet(file_path)
        
        # Mostrar el contenido del DataFrame
        print(df)
    except Exception as e:
        print(f"Error al leer el archivo {file_name}: {str(e)}")
