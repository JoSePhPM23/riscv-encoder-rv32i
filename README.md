# Codificador Educativo de Instrucciones RISC-V (RV32I)

Este repositorio contiene la herramienta de codificación de instrucciones para el subconjunto RV32I del curso CE-4301 Arquitectura de Computadores I.

## Preparación del entorno

Para garantizar la correcta ejecución del punto de entrada automatizado `./run.sh`, asegúrese de contar con los siguientes requisitos en su sistema (Linux / WSL 2):

### 1. Requisitos de software

* Python 3.8 o superior instalado.

En sistemas basados en Debian/Ubuntu, puede instalarlo ejecutando:

```bash
sudo apt update
sudo apt install -y python3
```

### 2. Permisos de ejecución

Asegúrese de que el script de entrada tenga permisos de ejecución concedidos:

```bash
chmod +x run.sh
```

## Punto de entrada fijo

La herramienta opera recibiendo una única instrucción por línea de comandos:

```bash
./run.sh "<instruccion>"
```

## Ejemplos de uso

```bash
./run.sh "add x5, x6, x7"
./run.sh "addi x10, x1, -12"
./run.sh "lw x5, 8(x6)"
./run.sh "sw x8, -4(x2)"
./run.sh "beq x1, x2, 8"
```

## Autoevaluación con vectores de ejemplo

Para comprobar el correcto funcionamiento de la herramienta frente a los vectores de prueba suministrados (`vectores_ejemplo.txt`), ejecute:

```bash
python3 test_vectors.py
```