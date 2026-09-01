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