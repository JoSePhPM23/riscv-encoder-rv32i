#!/usr/bin/env python3
"""
Esqueleto del Codificador Educativo de Instrucciones RISC-V.
CE4301 Arquitectura de Computadores I — Proyecto Individual — 2026-II

Este esqueleto ya implementa el contrato de línea de comandos y de salida
requerido por la especificación. Usted debe completar las dos funciones
marcadas con TODO; puede modificar el resto del archivo si lo necesita,
siempre que se preserve el contrato de invocación y la línea "HEX: 0x...".

No es obligatorio usar este esqueleto ni Python: puede implementar su
propia herramienta desde cero, en el lenguaje que prefiera, siempre que
respete el mismo contrato (ver especificación, sección "Modo de operación").
"""
import re
import sys

SOPORTADAS = ["add", "sub", "and", "or", "addi", "andi",
              "lw", "lb", "sw", "sb", "beq", "bne"]

# Mapeo oficial de la ISA RV32I para las 12 instrucciones
ISA = {
    # Tipo R
    "add":  {"fmt": "R", "opcode": 0x33, "funct3": 0x0, "funct7": 0x00},
    "sub":  {"fmt": "R", "opcode": 0x33, "funct3": 0x0, "funct7": 0x20},
    "and":  {"fmt": "R", "opcode": 0x33, "funct3": 0x7, "funct7": 0x00},
    "or":   {"fmt": "R", "opcode": 0x33, "funct3": 0x6, "funct7": 0x00},
    # Tipo I (Aritmetico)
    "addi": {"fmt": "I", "opcode": 0x13, "funct3": 0x0},
    "andi": {"fmt": "I", "opcode": 0x13, "funct3": 0x7},
    # Tipo I (Carga)
    "lb":   {"fmt": "I", "opcode": 0x03, "funct3": 0x0},
    "lw":   {"fmt": "I", "opcode": 0x03, "funct3": 0x2},
    # Tipo S (Almacenamiento)
    "sb":   {"fmt": "S", "opcode": 0x23, "funct3": 0x0},
    "sw":   {"fmt": "S", "opcode": 0x23, "funct3": 0x2},
    # Tipo B (Saltos)
    "beq":  {"fmt": "B", "opcode": 0x63, "funct3": 0x0},
    "bne":  {"fmt": "B", "opcode": 0x63, "funct3": 0x1},
}

# Mapeo de nombres de registros tanto x0-x31 como nombres ABI a su índice entero (0-31)
ABI_REGISTER_MAP = {
    "zero": 0,  "ra": 1,   "sp": 2,   "gp": 3,   "tp": 4,   "t0": 5,   "t1": 6,   "t2": 7,
    "s0": 8,    "fp": 8,   "s1": 9,   "a0": 10,  "a1": 11,  "a2": 12,  "a3": 13,  "a4": 14,
    "a5": 15,   "a6": 16,  "a7": 17,  "s2": 18,  "s3": 19,  "s4": 20,  "s5": 21,  "s6": 22,
    "s7": 23,   "s8": 24,  "s9": 25,  "s10": 26, "s11": 27, "t3": 28,  "t4": 29,  "t5": 30,  "t6": 31
}

def parse_register(reg_str: str) -> int:
    """
    Convierte una cadena de registro (p. ej. 'x5', 'x0', 'sp', 'a0') a su entero (0-31).
    """
    reg = reg_str.strip().lower()
    if reg.startswith("x") and reg[1:].isdigit():
        idx = int(reg[1:])
        if 0 <= idx <= 31:
            return idx
    if reg in ABI_REGISTER_MAP:
        return ABI_REGISTER_MAP[reg]
    raise ValueError(f"Registro no valido: '{reg_str}'")

def parse_instruction(instruction: str) -> dict:
    """
    Parsea una cadena de instrucción RISC-V y extrae el mnemónico, formato y operandos.
    Retorna un diccionario con los enteros correspondientes a cada campo.
    """
    text = instruction.strip()
    parts = text.split(None, 1)
    if not parts:
        raise ValueError("Instrucción vacía")

    mnemonic = parts[0].lower()
    if mnemonic not in ISA:
        raise ValueError(f"Instrucción no soportada: '{mnemonic}'")

    fmt = ISA[mnemonic]["fmt"]
    args_str = parts[1] if len(parts) > 1 else ""

    # Formato R: op rd, rs1, rs2
    if fmt == "R":
        args = [a.strip() for a in args_str.split(",") if a.strip()]
        if len(args) != 3:
            raise ValueError(f"En el formato R se requiere 3 operandos, se recibieron {len(args)}")
        return {
            "mnemonic": mnemonic,
            "fmt": fmt,
            "rd": parse_register(args[0]),
            "rs1": parse_register(args[1]),
            "rs2": parse_register(args[2]),
        }

    # Formato I: Aritmético (rd, rs1, imm) o Carga (rd, imm(rs1))
    elif fmt == "I":
        if mnemonic in ["lw", "lb"]:
            match = re.match(r"^\s*([^,]+)\s*,\s*([+-]?\d+)\s*\(\s*([^)]+)\s*\)\s*$", args_str)
            if not match:
                raise ValueError(f"Sintaxis invalida para {mnemonic}: '{args_str}'")
            return {
                "mnemonic": mnemonic,
                "fmt": fmt,
                "rd": parse_register(match.group(1)),
                "rs1": parse_register(match.group(3)),
                "imm": int(match.group(2)),
            }
        else:
            args = [a.strip() for a in args_str.split(",") if a.strip()]
            if len(args) != 3:
                raise ValueError(f"En el formato I aritmético se requiere 3 operandos, se recibieron {len(args)}")
            return {
                "mnemonic": mnemonic,
                "fmt": fmt,
                "rd": parse_register(args[0]),
                "rs1": parse_register(args[1]),
                "imm": int(args[2]),
            }

    # Formato S: op rs2, imm(rs1)
    elif fmt == "S":
        match = re.match(r"^\s*([^,]+)\s*,\s*([+-]?\d+)\s*\(\s*([^)]+)\s*\)\s*$", args_str)
        if not match:
            raise ValueError(f"Sintaxis invalida para {mnemonic}: '{args_str}'")
        return {
            "mnemonic": mnemonic,
            "fmt": fmt,
            "rs2": parse_register(match.group(1)),
            "rs1": parse_register(match.group(3)),
            "imm": int(match.group(2)),
        }

    # Formato B: op rs1, rs2, imm
    elif fmt == "B":
        args = [a.strip() for a in args_str.split(",") if a.strip()]
        if len(args) != 3:
            raise ValueError(f"En el formato B se requiere 3 operandos, se recibieron {len(args)}")
        return {
            "mnemonic": mnemonic,
            "fmt": fmt,
            "rs1": parse_register(args[0]),
            "rs2": parse_register(args[1]),
            "imm": int(args[2]),
        }

    raise ValueError(f"Formato no reconocido: {fmt}")


def encode_instruction(instruction: str) -> int:
    """
    Recibe una instrucción como texto, p. ej. "add x5, x6, x7", y
    retorna su codificación de 32 bits como entero (0 <= valor < 2**32).

    Soporta únicamente las instrucciones en SOPORTADAS. 
    """
    parsed = parse_instruction(instruction)
    mnemonic = parsed["mnemonic"]
    fmt = parsed["fmt"]
    info = ISA[mnemonic]

    # Codificación de Formato R
    if fmt == "R":
        opcode = info["opcode"]
        funct3 = info["funct3"]
        funct7 = info["funct7"]
        rd = parsed["rd"]
        rs1 = parsed["rs1"]
        rs2 = parsed["rs2"]

        word = ((funct7 & 0x7F) << 25) | \
               ((rs2 & 0x1F) << 20) | \
               ((rs1 & 0x1F) << 15) | \
               ((funct3 & 0x07) << 12) | \
               ((rd & 0x1F) << 7) | \
               (opcode & 0x7F)
        return word

    # Codificación de Formato I (Aritmético y Cargas)
    elif fmt == "I":
        opcode = info["opcode"]
        funct3 = info["funct3"]
        rd = parsed["rd"]
        rs1 = parsed["rs1"]
        imm = parsed["imm"]

        # Validación del rango representable para inmediatos de 12 bits con signo
        if not (-2048 <= imm <= 2047):
            raise ValueError(f"Inmediato está fuera de rango (-2048 a 2047): {imm}")

        imm_12 = imm & 0xFFF  # Conversión a complemento a 2 de 12 bits

        word = (imm_12 << 20) | \
               ((rs1 & 0x1F) << 15) | \
               ((funct3 & 0x07) << 12) | \
               ((rd & 0x1F) << 7) | \
               (opcode & 0x7F)
        return word

# Codificación de Formato S (Almacenamiento)
    elif fmt == "S":
        opcode = info["opcode"]
        funct3 = info["funct3"]
        rs1 = parsed["rs1"]
        rs2 = parsed["rs2"]
        imm = parsed["imm"]

        if not (-2048 <= imm <= 2047):
            raise ValueError(f"El inmediato está fuera de rango (-2048 a 2047): {imm}")

        imm_12 = imm & 0xFFF
        imm_11_5 = (imm_12 >> 5) & 0x7F
        imm_4_0 = imm_12 & 0x1F

        return ((imm_11_5 & 0x7F) << 25) | \
               ((rs2 & 0x1F) << 20) | \
               ((rs1 & 0x1F) << 15) | \
               ((funct3 & 0x07) << 12) | \
               ((imm_4_0 & 0x1F) << 7) | \
               (opcode & 0x7F)

    # Codificación de Formato B (Saltos condicionales)
    elif fmt == "B":
        opcode = info["opcode"]
        funct3 = info["funct3"]
        rs1 = parsed["rs1"]
        rs2 = parsed["rs2"]
        imm = parsed["imm"]

        if not (-4096 <= imm <= 4095):
            raise ValueError(f"El inmediato de salto fuera de rango (-4096 a 4095): {imm}")
        if imm % 2 != 0:
            raise ValueError(f"El inmediato de salto debe ser par (alineado a 2 bytes): {imm}")

        imm_13 = imm & 0x1FFF
        imm_12 = (imm_13 >> 12) & 0x1
        imm_11 = (imm_13 >> 11) & 0x1
        imm_10_5 = (imm_13 >> 5) & 0x3F
        imm_4_1 = (imm_13 >> 1) & 0x0F

        return (imm_12 << 31) | \
               (imm_10_5 << 25) | \
               ((rs2 & 0x1F) << 20) | \
               ((rs1 & 0x1F) << 15) | \
               ((funct3 & 0x07) << 12) | \
               (imm_4_1 << 8) | \
               (imm_11 << 7) | \
               (opcode & 0x7F)

    raise ValueError(f"Formato desconocido: {fmt}")


def explain_instruction(instruction: str, word: int) -> str:
    """
    Debe retornar un texto (para imprimirse en pantalla) que muestre, de
    forma visual, los 32 bits de 'word' divididos en los campos del
    formato correspondiente (R, I, S o B) — indicando el rango de bits y
    el valor de cada campo — junto con una breve explicación de cada uno.
    El formato visual (colores, tabla, arte ASCII, etc.) queda a su
    criterio, siempre que sea claro.
    """
    # TODO: implementar.
    raise NotImplementedError("explain_instruction: pendiente de implementar")


def main():
    if len(sys.argv) != 2:
        print(f'Uso: {sys.argv[0]} "<instruccion>"', file=sys.stderr)
        print(f'Ejemplo: {sys.argv[0]} "add x5, x6, x7"', file=sys.stderr)
        sys.exit(2)

    instruction = sys.argv[1]
    word = encode_instruction(instruction) & 0xFFFFFFFF

    print(explain_instruction(instruction, word))

    # No modificar el formato de la siguiente línea: la especificación la
    # requiere, literal, para permitir la validación automática.
    print(f"HEX: 0x{word:08x}")


if __name__ == "__main__":
    main()
