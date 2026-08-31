## Instalación del Toolchain Oficial RISC-V (32 bits)

Para validar la herramienta contra el ensamblador oficial y `objdump`, se instaló el toolchain `riscv-elf` en Ubuntu bajo WSL 2:

```bash
sudo apt update
sudo apt install -y gcc-riscv64-unknown-elf binutils-riscv64-unknown-elf