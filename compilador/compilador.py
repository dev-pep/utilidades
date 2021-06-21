#!/usr/bin/env python3

# Utilidad compilador, https://github.com/dev-pep/utilidades
# (c) dev-pep, 2021

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see https://www.gnu.org/licenses/.

# Utilidad para compilar varios capítulos de documentación en un solo
# archivo .md.
# Proceso posterior con pandoc para conversión a otros formatos.
# Todo según archivo 'Makelist', que debe estar en el mismo directorio
# que el script.

import os
import re


def procesa(archivo, destino, atributo):
    fin = open(archivo, "rt")
    fout = open(destino, atributo)
    fout.write("\n")
    for linea in fin:
        # Eliminaremos los enlaces, si los hay:
        m = re.search("(.*[^!]\[.*]\().*(\).*)", linea)
        if m:
            linea = m.group(1) + "#" + m.group(2) + "\n"
        else:  # no es enlace; ¿será imagen?
            m = re.search("(.*!\[.*]\()(.*)(\).*)", linea)
            if m:  # si es imagen, convertimos de path relativo a absoluto
                # (se asume ruta de la imagen relativa al archivo .md)
                ruta = (os.path.normpath(
                    os.path.join(os.path.dirname(archivo), m.group(2))))
                linea = m.group(1) + ruta + m.group(3) + "\n"
        fout.write(linea)
    fout.close()
    fin.close()


def next_linea(f):
    l = ""
    while not l:
        l = f.readline()
        if not l:
            return l
        l = l.strip()
        if l and l[0] == '#':
            l = ""
    return l.strip()


base = 'GitHub'
output = 'docs'
scriptDir = os.path.dirname(os.path.abspath(__file__))
try:
    fMakeList = open(os.path.join(scriptDir, 'Makelist'), 'rt')
except FileNotFoundError:
    print(f"Archivo 'Makelist' no existente.\n")
    exit(0)

# Parse config:
linea = next_linea(fMakeList)
while linea:
    if linea.startswith("dirbase"):
        base = linea.split('=')[1].strip()
    elif linea.startswith("diroutput"):
        output = linea.split('=')[1].strip()
    elif linea.startswith("salida"):
        break
    else:
        print("Error de formato.\n")
    linea = next_linea(fMakeList)
if not linea:
    print("Terminado, sin compilaciones.\n")

# Set directorios:
baseDir = outputDir = scriptDir
while os.path.basename(baseDir) != base:
    if baseDir == os.path.dirname(baseDir):
        print(f"Directorio base '{base}' no encontrado.\n")
        exit(0)
    baseDir = os.path.dirname(baseDir)
outputDir = os.path.join(baseDir, output)
if not os.path.isdir(outputDir):
    os.mkdir(outputDir)
if not os.path.isdir(outputDir):
    print(f"No se pudo crear directorio de salida '{output}'.\n")
    exit(0)

# Parse compilaciones:
compilaciones = []
while linea:
    if linea.startswith("salida"):
        salida = linea.split('=')[1].strip()
        ignora = False
        primero = True
    elif linea.startswith("ignora"):
        ignora = True
    elif not ignora:
        if primero:
            print(f"Procesando '{salida}.md'...")
            procesa(os.path.join(baseDir, linea),
                    os.path.join(outputDir, salida + ".md"), "wt")
            primero = False
            compilaciones.append(salida)
        else:
            procesa(os.path.join(baseDir, linea),
                    os.path.join(outputDir, salida + ".md"), "at")
    linea = next_linea(fMakeList)

fMakeList.close()

# Vamos a exportar ahora a otros formatos (todos los archivos .md del
# directorio de salida):
for c in compilaciones:
    inFile = os.path.join(outputDir, c + ".md")

    # HTML
#    print(f"Exportando '{c}.html'")
#    outFile = os.path.join(outputDir, c + ".html")
#    os.system('pandoc --standalone --toc --toc-depth 2 --quiet '
#        f'--data-dir {scriptDir} -H styles.html '
#        f'-o "{outFile}" "{inFile}"')
    # TO-DO: imágenes en HTML

    # ODT
    print(f"Exportando '{c}.odt'")
    outFile = os.path.join(outputDir, c + ".odt")
    refFile = os.path.join(scriptDir, "plantilla-pandoc.odt")
    os.system(f'pandoc -o "{outFile}" --reference-doc="{refFile}" "{inFile}"')

    # PDF desde ODT (con libreoffice)
<<<<<<< HEAD
#    print(f"Exportando '{c}.pdf'")
#    inFileOdt = os.path.join(outputDir, c + ".odt")
    # Solo Unix con libreoffice (debe ir después de conversión ODT):
#    os.system(f'libreoffice --headless --convert-to pdf --outdir "{outputDir}" "{inFileOdt}" >/dev/null 2>&1')
=======
    print(f"Exportando '{c}.pdf'")
    inFileOdt = os.path.join(outputDir, c + ".odt")
    # Solo Unix con libreoffice (debe ir después de conversión ODT):
    os.system(f'libreoffice --headless --convert-to pdf --outdir "{outputDir}" "{inFileOdt}" >/dev/null 2>&1')
>>>>>>> f26913ef408275f1116fb64120054157e1567ffb

    # EPUB desde markup
#    print(f"Exportando '{c}.epub'")
#    outFile = os.path.join(outputDir, c + ".epub")
#    os.system(f'pandoc -o "{outFile}" --metadata title="{c}" "{inFile}"')

    # EPUB desde html
<<<<<<< HEAD
#    print(f"Exportando '{c}.epub'")
#    outFile = os.path.join(outputDir, c + ".epub")
#    inFileHtml = os.path.join(outputDir, c + ".html")
#    os.system(f'pandoc -o "{outFile}" --metadata title="{c}" "{inFileHtml}"')
=======
    print(f"Exportando '{c}.epub'")
    outFile = os.path.join(outputDir, c + ".epub")
    inFileHtml = os.path.join(outputDir, c + ".html")
    os.system(f'pandoc -o "{outFile}" --metadata title="{c}" "{inFileHtml}"')
>>>>>>> f26913ef408275f1116fb64120054157e1567ffb
