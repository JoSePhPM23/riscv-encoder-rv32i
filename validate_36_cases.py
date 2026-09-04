import subprocess
import os
import sys
import re

from encoder_skeleton import encode_instruction

CASES = [
    # --- R-Type ---
    ("add", "add x5, x6, x7", "Positivo (registros estándar)"),
    ("add", "add x0, x1, x2", "Límite (destino registro x0)"),
    ("add", "add x31, x30, x29", "Límite (registros máximos x31)"),
    
    ("sub", "sub x10, x11, x12", "Positivo (registros estándar)"),
    ("sub", "sub x0, x5, x5", "Límite (resta de sí mismo en x0)"),
    ("sub", "sub x31, x1, x30", "Límite (combinación con x31)"),

    ("and", "and x15, x16, x17", "Positivo (operación lógica and)"),
    ("and", "and x0, x4, x8", "Límite (destino x0)"),
    ("and", "and x28, x29, x30", "Límite (registros altos)"),

    ("or",  "or x8, x9, x10", "Positivo (operación lógica or)"),
    ("or",  "or x0, x2, x3", "Límite (destino x0)"),
    ("or",  "or x31, x31, x31", "Límite (mismo registro x31)"),

    # --- I-Type (Aritmética) ---
    ("addi", "addi x5, x6, 100", "Positivo (inmediato positivo)"),
    ("addi", "addi x10, x1, -2048", "Negativo / Límite (mínimo inmediato 12-bit)"),
    ("addi", "addi x15, x0, 2047", "Límite (máximo inmediato 12-bit)"),

    ("andi", "andi x8, x9, 15", "Positivo (máscara lógica)"),
    ("andi", "andi x12, x13, -1", "Negativo / Límite (inmediato -1, todos bits en 1)"),
    ("andi", "andi x0, x1, 2047", "Límite (máximo inmediato en x0)"),

    # --- I-Type (Carga) ---
    ("lw", "lw x5, 8(x6)", "Positivo (desplazamiento positivo)"),
    ("lw", "lw x10, -2048(x1)", "Negativo / Límite (mínimo offset -2048)"),
    ("lw", "lw x0, 2047(x31)", "Límite (máximo offset 2047)"),

    ("lb", "lb x2, 16(x3)", "Positivo (desplazamiento positivo)"),
    ("lb", "lb x4, -50(x5)", "Negativo (desplazamiento negativo)"),
    ("lb", "lb x31, 0(x0)", "Límite (offset 0 en base x0)"),

    # --- S-Type (Almacenamiento) ---
    ("sw", "sw x8, 12(x2)", "Positivo (offset positivo)"),
    ("sw", "sw x9, -2048(x4)", "Negativo / Límite (mínimo offset -2048)"),
    ("sw", "sw x30, 2047(x31)", "Límite (máximo offset 2047)"),

    ("sb", "sb x1, 4(x2)", "Positivo (offset positivo)"),
    ("sb", "sb x3, -100(x4)", "Negativo (offset negativo)"),
    ("sb", "sb x0, 0(x0)", "Límite (offset 0 con registros x0)"),

    # --- B-Type (Saltos) ---
    ("beq", "beq x1, x2, 16", "Positivo (salto hacia adelante)"),
    ("beq", "beq x3, x4, -4096", "Negativo / Límite (mínimo salto negativo 13-bit)"),
    ("beq", "beq x0, x0, 0", "Límite (salto 0 con x0)"),

    ("bne", "bne x5, x6, 100", "Positivo (salto hacia adelante)"),
    ("bne", "bne x7, x8, -200", "Negativo (salto hacia atrás)"),
    ("bne", "bne x29, x30, 4094", "Límite (máximo salto positivo 13-bit)"),
]

def format_for_gas(instr: str) -> str:
    """Ajusta sintaxis de saltos para que GNU Assembler use desplazamientos relativos al PC."""
    parts = instr.strip().split(None, 1)
    mnemonic = parts[0].lower()
    if mnemonic in ["beq", "bne"]:
        args = [a.strip() for a in parts[1].split(",")]
        imm = int(args[2])
        sign = "+" if imm >= 0 else "-"
        return f"{mnemonic} {args[0]}, {args[1]}, . {sign} {abs(imm)}"
    return instr

def run_official_toolchain(instr: str) -> str:
    s_file = "temp_val.s"
    o_file = "temp_val.o"

    gas_instr = format_for_gas(instr)

    with open(s_file, "w") as f:
        f.write(f".section .text\n.option norelax\n.globl _start\n_start:\n    {gas_instr}\n")

    try:
        subprocess.run(
            ["riscv64-unknown-elf-gcc", "-march=rv32i", "-mabi=ilp32", "-nostdlib", "-c", s_file, "-o", o_file],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        res = subprocess.check_output(
            ["riscv64-unknown-elf-objdump", "-d", o_file, "-M", "numeric,no-aliases"],
            text=True
        )
        for line in res.splitlines():
            if ":" in line and "\t" in line:
                parts = line.strip().split("\t")
                if len(parts) >= 2:
                    hex_val = parts[1].strip().split()[0]
                    return f"0x{int(hex_val, 16):08x}"
    finally:
        if os.path.exists(s_file): os.remove(s_file)
        if os.path.exists(o_file): os.remove(o_file)
    
    return "ERROR"

def main():
    print("Ejecutando validación de 36 casos contra Toolchain Oficial...\n")
    results = []
    passed = 0

    for cat, instr, desc in CASES:
        model_word = encode_instruction(instr) & 0xFFFFFFFF
        model_hex = f"0x{model_word:08x}"
        toolchain_hex = run_official_toolchain(instr)
        
        match = (model_hex == toolchain_hex)
        if match:
            passed += 1
        
        results.append((instr, desc, model_hex, toolchain_hex, "SI" if match else "NO"))

    print(f"Resultado: {passed}/36 casos exitosos.\n")

    md_table = []
    md_table.append("| N° | Instrucción | Escenario / Descripción | Salida Modelo | Salida objdump | ¿Coincide? |")
    md_table.append("|:---|:---|:---|:---|:---|:---:|")
    
    for idx, (instr, desc, m_hex, t_hex, match) in enumerate(results, 1):
        md_table.append(f"| {idx} | `{instr}` | {desc} | `{m_hex}` | `{t_hex}` | {match} |")

    table_str = "\n".join(md_table)
    
    with open("evidencia_36_casos.md", "w") as f:
        f.write("# Evidencia de validación contra toolchain oficial (36 Casos)\n\n")
        f.write(table_str)

    print("Tabla Markdown generada exitosamente en 'evidencia_36_casos.md'.")

if __name__ == "__main__":
    main()