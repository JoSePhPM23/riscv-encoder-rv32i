import sys
from encoder_skeleton import encode_instruction

def test_all_vectors():
    """
    Lee un archivo de vectores de prueba y valida que la función encode_instruction
    genere las salidas hexadecimales esperadas para cada instrucción de ensamblador.
    """
    # Inicialización de contadores para el reporte final
    passed = 0
    failed = 0
    
    # Lectura del archivo de pruebas línea por línea con su número correspondiente
    with open("vectores_ejemplo.txt", "r") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            
            # Ignora las líneas en blanco y comentarios que inicien con '#'
            if not line or line.startswith("#"):
                continue
            
            # Separa la instrucción del valor esperado dividiendo por ';'
            parts = [p.strip() for p in line.split(";")]
            if len(parts) != 2:
                continue
            
            instr, expected_hex = parts[0], parts[1].lower()
            
            try:
                # Codifica instrucción y asegura una máscara de 32 bits (4 bytes)
                word = encode_instruction(instr) & 0xFFFFFFFF
                # Formatea la palabra resultante a cadena hexadecimal de 8 dígitos con '0x'
                obtained_hex = f"0x{word:08x}"
                
                # Compara el resultado obtenido contra el esperado
                if obtained_hex == expected_hex:
                    passed += 1
                else:
                    failed += 1
                    print(f"[FAIL] Línea {line_num}: '{instr}'")
                    print(f"       Obtenido: {obtained_hex} | Esperado: {expected_hex}")
            except Exception as e:
                # Captura excepciones en caso de sintaxis no soportada o errores en el encoder
                failed += 1
                print(f"[ERROR] Línea {line_num}: '{instr}' -> {e}")

    # Se muestra la tabla de resumen con las métricas finales de ejecución
    print("\n" + "=" * 40)
    print("RESUMEN DE VERIFICACIÓN DE VECTORES")
    print("=" * 40)
    print(f"Pruebas exitosas: {passed}")
    print(f"Pruebas fallidas: {failed}")
    print(f"Total evaluado:   {passed + failed}")

    # Finalización limpia o salida con estado de error (1) para integración continua
    if failed == 0 and passed > 0:
        print("\n¡ÉXITO TOTAL! Todas las instrucciones coinciden con el resultado esperado.")
    else:
        sys.exit(1)

# Punto de entrada principal para ejecutar las pruebas
if __name__ == "__main__":
    test_all_vectors()