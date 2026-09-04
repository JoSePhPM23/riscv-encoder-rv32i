# Documentación Técnica: Codificador Educativo RISC-V (RV32I)

**Curso:** CE-4301 Arquitectura de Computadores I 
**Institución**: Tecnológico de Costa Rica
**Autor:** Joseph Piedra Montero  

---

## 1. Descripción de la arquitectura del código y decisiones de diseño

El proyecto está diseñado bajo una arquitectura modular en Python dentro del archivo `encoder_skeleton.py`, estructurada en cuatro fases principales:

1. **Estructura de datos de la ISA:**  
   Se utiliza un diccionario principal (`ISA`) que mapea cada mnemónico soportado con su formato (`R`, `I`, `S`, `B`) y sus campos fijos en hexadecimal (`opcode`, `funct3`, `funct7`). Un segundo diccionario (`ABI_REGISTER_MAP`) permite traducir tanto registros en notación `x0`–`x31` como nombres ABI (`sp`, `ra`, `a0`, etc.) a su índice entero (0–31).

2. **Parser de instrucciones (`parse_instruction`):**  
   Recibe la cadena textual de la instrucción y extrae sus componentes utilizando expresiones regulares (`re`). Valida la cantidad de operandos y procesa las sintaxis de memoria tipo `imm(rs1)` para instrucciones de carga (`lw`, `lb`) y almacenamiento (`sw`, `sb`).

3. **Ensamblado y codificación de bits (`encode_instruction`):**  
   Aplica operaciones de desplazamiento de bits (`<<`), enmascaramiento (`&`) y lógica `OR` (`|`):
   * **Tipo R:** Ensambla `funct7`, `rs2`, `rs1`, `funct3`, `rd` y `opcode`.
   * **Tipo I:** Convierte inmediatos a complemento a 2 de 12 bits (`imm & 0xFFF`).
   * **Tipo S:** Divide el inmediato en `imm[11:5]` (bits 31–25) e `imm[4:0]` (bits 11–7).
   * **Tipo B:** Reordena las secciones del inmediato de 13 bits (`imm[12]`, `imm[10:5]`, `imm[4:1]`, `imm[11]`), omitiendo el bit 0 implícito debido a la alineación a 2 bytes.

4. **Interfaz de explicación visual (`explain_instruction`):**  
   Genera el desglose tabular en ASCII mostrando el rango de bits y valores binarios/decimales por campo. Imprime al final la línea requerida con el formato exacto `HEX: 0xXXXXXXXX` para posibilitar la evaluación automatizada.

---

## 2. Fuentes consultadas para los campos de codificación

Los valores de `opcode`, `funct3` y `funct7` fueron consultados directamente del manual oficial de la arquitectura RISC-V:
* **Fuente:** Andrew Waterman and Krste Asanović. *The RISC-V Instruction Set Manual, Volume I: Unprivileged ISA*, Document Version 20191213. RISC-V Foundation, 2019.

### Tabla de codificación del subconjunto soportado

| Categoría | Instrucción | Formato | Opcode (7 bits) | funct3 (3 bits) | funct7 (7 bits) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Aritmética Reg-Reg | `add` | R | `0110011` (`0x33`) | `000` (`0x0`) | `0000000` (`0x00`) |
| Aritmética Reg-Reg | `sub` | R | `0110011` (`0x33`) | `000` (`0x0`) | `0100000` (`0x20`) |
| Aritmética Reg-Reg | `and` | R | `0110011` (`0x33`) | `111` (`0x7`) | `0000000` (`0x00`) |
| Aritmética Reg-Reg | `or`  | R | `0110011` (`0x33`) | `110` (`0x6`) | `0000000` (`0x00`) |
| Aritmética Inmediato| `addi`| I | `0010011` (`0x13`) | `000` (`0x0`) | N/A |
| Aritmética Inmediato| `andi`| I | `0010011` (`0x13`) | `111` (`0x7`) | N/A |
| Carga de Memoria | `lb`  | I | `0000011` (`0x03`) | `000` (`0x0`) | N/A |
| Carga de Memoria | `lw`  | I | `0000011` (`0x03`) | `010` (`0x2`) | N/A |
| Almacenamiento | `sb`  | S | `0100011` (`0x23`) | `000` (`0x0`) | N/A |
| Almacenamiento | `sw`  | S | `0100011` (`0x23`) | `010` (`0x2`) | N/A |
| Salto Condicional | `beq` | B | `1100011` (`0x63`) | `000` (`0x0`) | N/A |
| Salto Condicional | `bne` | B | `1100011` (`0x63`) | `001` (`0x1`) | N/A |

---

## 3. Ejemplos de salida explicativa por formato

### Formato R (`add x7, x20, x6`)

![Formato R (add x7, x20, x6)](Evidencia/Formato%20R%20(%60add%20x7%2C%20x20%2C%20x6%60).PNG)

### Formato I (`addi x10, x1, -12`)

![Formato I (addi x10, x1, -12)](Evidencia/Formato%20I%20(%60addi%20x10%2C%20x1%2C%20-12%60).PNG)

### Formato S (`sw x8, -4(x2)`)

![Formato S (sw x8, -4(x2))](Evidencia/Formato%20S%20(%60sw%20x8%2C%20-4(x2)%60).PNG)

### Formato B (`beq x1, x2, 8`)

![Formato B (beq x1, x2, 8)](Evidencia/Formato%20B%20(%60beq%20x1%2C%20x2%2C%208%60).PNG)

---

## 4. Evidencia de la validación contra el toolchain oficial

Para comprobar que el codificador implementado genera exactamente las mismas instrucciones máquina que el toolchain oficial de RISC-V, se ejecutó el script automatizado `validate_36_cases.py`. Este script realiza la validación de 36 escenarios correspondientes a 12 instrucciones, considerando casos positivos, negativos y casos límite. Como resultado, se obtuvo una coincidencia exacta del 100% (36/36 casos exitosos).

Además de mostrar el resultado de la validación en consola, la ejecución del script genera automáticamente el archivo `evidencia_36_casos.md`. Este archivo contiene el detalle de cada uno de los casos evaluados, incluyendo la instrucción utilizada, el escenario de prueba, la salida generada por el modelo, la salida obtenida mediante `objdump -d` del toolchain oficial y una indicación de si ambas codificaciones coinciden.

La ejecución del comando:

```bash
python3 validate_36_cases.py
```

La salida obtenida confirma que los 36 casos fueron validados exitosamente:

![Validación contra el toolchain oficial](Evidencia/Validacion%20vs%20toolchain%20-%20validate_36_cases.PNG)

### Contenido de `evidencia_36_casos.md` 
El archivo generado presenta la evidencia detallada de la validación mediante la siguiente tabla:

# Evidencia de validación contra toolchain oficial (36 Casos)

| N° | Instrucción | Escenario / Descripción | Salida Modelo | Salida objdump | ¿Coincide? |
|:---|:---|:---|:---|:---|:---:|
| 1 | `add x5, x6, x7` | Positivo (registros estándar) | `0x007302b3` | `0x007302b3` | SI |
| 2 | `add x0, x1, x2` | Límite (destino registro x0) | `0x00208033` | `0x00208033` | SI |
| 3 | `add x31, x30, x29` | Límite (registros máximos x31) | `0x01df0fb3` | `0x01df0fb3` | SI |
| 4 | `sub x10, x11, x12` | Positivo (registros estándar) | `0x40c58533` | `0x40c58533` | SI |
| 5 | `sub x0, x5, x5` | Límite (resta de sí mismo en x0) | `0x40528033` | `0x40528033` | SI |
| 6 | `sub x31, x1, x30` | Límite (combinación con x31) | `0x41e08fb3` | `0x41e08fb3` | SI |
| 7 | `and x15, x16, x17` | Positivo (operación lógica and) | `0x011877b3` | `0x011877b3` | SI |
| 8 | `and x0, x4, x8` | Límite (destino x0) | `0x00827033` | `0x00827033` | SI |
| 9 | `and x28, x29, x30` | Límite (registros altos) | `0x01eefe33` | `0x01eefe33` | SI |
| 10 | `or x8, x9, x10` | Positivo (operación lógica or) | `0x00a4e433` | `0x00a4e433` | SI |
| 11 | `or x0, x2, x3` | Límite (destino x0) | `0x00316033` | `0x00316033` | SI |
| 12 | `or x31, x31, x31` | Límite (mismo registro x31) | `0x01ffefb3` | `0x01ffefb3` | SI |
| 13 | `addi x5, x6, 100` | Positivo (inmediato positivo) | `0x06430293` | `0x06430293` | SI |
| 14 | `addi x10, x1, -2048` | Negativo / Límite (mínimo inmediato 12-bit) | `0x80008513` | `0x80008513` | SI |
| 15 | `addi x15, x0, 2047` | Límite (máximo inmediato 12-bit) | `0x7ff00793` | `0x7ff00793` | SI |
| 16 | `andi x8, x9, 15` | Positivo (máscara lógica) | `0x00f4f413` | `0x00f4f413` | SI |
| 17 | `andi x12, x13, -1` | Negativo / Límite (inmediato -1, todos bits en 1) | `0xfff6f613` | `0xfff6f613` | SI |
| 18 | `andi x0, x1, 2047` | Límite (máximo inmediato en x0) | `0x7ff0f013` | `0x7ff0f013` | SI |
| 19 | `lw x5, 8(x6)` | Positivo (desplazamiento positivo) | `0x00832283` | `0x00832283` | SI |
| 20 | `lw x10, -2048(x1)` | Negativo / Límite (mínimo offset -2048) | `0x8000a503` | `0x8000a503` | SI |
| 21 | `lw x0, 2047(x31)` | Límite (máximo offset 2047) | `0x7fffa003` | `0x7fffa003` | SI |
| 22 | `lb x2, 16(x3)` | Positivo (desplazamiento positivo) | `0x01018103` | `0x01018103` | SI |
| 23 | `lb x4, -50(x5)` | Negativo (desplazamiento negativo) | `0xfce28203` | `0xfce28203` | SI |
| 24 | `lb x31, 0(x0)` | Límite (offset 0 en base x0) | `0x00000f83` | `0x00000f83` | SI |
| 25 | `sw x8, 12(x2)` | Positivo (offset positivo) | `0x00812623` | `0x00812623` | SI |
| 26 | `sw x9, -2048(x4)` | Negativo / Límite (mínimo offset -2048) | `0x80922023` | `0x80922023` | SI |
| 27 | `sw x30, 2047(x31)` | Límite (máximo offset 2047) | `0x7fefafa3` | `0x7fefafa3` | SI |
| 28 | `sb x1, 4(x2)` | Positivo (offset positivo) | `0x00110223` | `0x00110223` | SI |
| 29 | `sb x3, -100(x4)` | Negativo (offset negativo) | `0xf8320e23` | `0xf8320e23` | SI |
| 30 | `sb x0, 0(x0)` | Límite (offset 0 con registros x0) | `0x00000023` | `0x00000023` | SI |
| 31 | `beq x1, x2, 16` | Positivo (salto hacia adelante) | `0x00208863` | `0x00208863` | SI |
| 32 | `beq x3, x4, -4096` | Negativo / Límite (mínimo salto negativo 13-bit) | `0x80418063` | `0x80418063` | SI |
| 33 | `beq x0, x0, 0` | Límite (salto 0 con x0) | `0x00000063` | `0x00000063` | SI |
| 34 | `bne x5, x6, 100` | Positivo (salto hacia adelante) | `0x06629263` | `0x06629263` | SI |
| 35 | `bne x7, x8, -200` | Negativo (salto hacia atrás) | `0xf2839ce3` | `0xf2839ce3` | SI |
| 36 | `bne x29, x30, 4094` | Límite (máximo salto positivo 13-bit) | `0x7fee9fe3` | `0x7fee9fe3` | SI |

En todos los casos evaluados, la codificación hexadecimal generada por el modelo coincide exactamente con la obtenida mediante el toolchain oficial, por lo que la validación alcanza un resultado de 36/36 casos exitosos (100%).

## 5. Instrucciones de instalación del toolchain e instalación/uso de la herramienta

### Instalación del toolchain oficial de RISC-V (32 bits)
Para llevar a cabo la verificación contra el ensamblador oficial y `objdump`, se instaló el paquete `gcc-riscv64-unknown-elf` :

```bash
sudo apt update
sudo apt install -y gcc-riscv64-unknown-elf binutils-riscv64-unknown-elf
```

### Comando de ensamblado y desensamblado

1. **Ensamblar código de 32 bits :** 
```bash
riscv64-unknown-elf-gcc -march=rv32i -mabi=ilp32 -nostdlib -c fuente.s -o objeto.o
```
2. **Obtener la codificación hexadecimal con `objdump` :**
```bash
riscv64-unknown-elf-objdump -d objeto.o -M numeric,no-aliases
```

### Instalación, preparación y uso de la herramienta

1. **Clonar repositorio e ingresar a la carpeta :**
```bash
git clone https://github.com/JoSePhPM23/riscv-encoder-rv32i.git
cd riscv-encoder-rv32i
```
2. **Asignar permisos de ejecución al script :**
```bash
chmod +x run.sh
```
3. **Ejecutar la herramienta :**
```bash
./run.sh "add x5, x6, x7"
./run.sh "sw x8, -4(x2)"
```