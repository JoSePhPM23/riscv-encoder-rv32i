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


def encode_instruction(instruction: str) -> int:
    """
    Recibe una instrucción como texto, p. ej. "add x5, x6, x7", y debe
    retornar su codificación de 32 bits como entero (0 <= valor < 2**32).

    Debe soportar únicamente las instrucciones en SOPORTADAS. Los valores
    de opcode/funct3/funct7 de cada una NO se proveen aquí: deben
    investigarse en el manual oficial de la ISA RISC-V (ver referencia en
    la especificación) y documentarse en el README.
    """
    # TODO: implementar. Sugerencia: parsear el mnemónico y los operandos,
    # despachar según el formato (R/I/S/B), y ensamblar los campos con
    # operaciones de bits.
    raise NotImplementedError("encode_instruction: pendiente de implementar")


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
