#!/usr/bin/env python3

# Utilidad joiner, https://github.com/dev-pep/utilidades
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

# Utilidad para juntar en un solo archivo .md todos los archivos pertenecientes
# a un repositorio de documentación.
# El archivo resultante puede ser procesado con pandoc para convertir la documentación
# en un solo archivo de cualquier formato.


import os
import sys
import os.path
import re


def procesa(root):
    fout = open(root + "_tmp.md", "wt")
    fin = open(root + "/README.md", "rt")
    fout.write(fin.read())
    fout.write("\n")
    fin.close()
    listadir = os.listdir(root + "/capitulos")
    listadir.sort()
    for f in listadir:
        fname = root + "/capitulos/" + f
        fin = open(fname, "rt")
        fout.write(fin.read())
        fout.write("\n")
        fin.close()
    fout.close()

    # Reemplazar links a anchor y eliminar líneas en blanco duplicadas:
    fin = open(root + "_tmp.md", "rt")  # reabrimos archivo temporal para procesar
    fout = open(root + ".md", "wt")
    lastline = ""
    for linea in fin:
        linea = linea.rstrip()
        if linea == "" and lastline == "":
            continue
        # Si es un anchor a otro archivo, eliminamos el nombre de archivo, dejando el anchor:
        m = re.search("(.*\[.*]\()(.*\.md)#(.*)\)", linea)
        if m:
            linea = m.group(1) + "#" + m.group(3) + ")"
            continue
        # Si es link a otro md, obtenemos el título (primera línea) dentro del texto
        # de ese archivo, y lo covertimos en anchor:
        m = re.search("(.*\[.*]\()(.*\.md)\)", linea)
        if m:
            f = open(root + "/" + m.group(2))
            l = f.readline()
            anchor = "#" + l.lstrip("#").lower().strip().replace(" ", "-")
            f.close()
            linea = m.group(1) + anchor + ")"
        fout.write(linea + "\n")
        lastline = linea
    fin.close()
    fout.close()
    os.remove(root + "_tmp.md")  # borramos archivo temporal


if len(sys.argv) != 2:
    print("""Uso: joiner.py <dir> | alldoc
             Los nombres de directorios se indican sin barras.
             alldoc actúa sobre todos los directorios doc-*.
             El script debe estar en la misma carpeta que el directorio doc-*.""")
else:
    root = sys.argv[1].strip()
    if root == "alldoc":  ## actúa sobre todos los directorios doc-*
        listadir = os.listdir()
        for f in listadir:
            if f[:4] == "doc-" and os.path.isdir(f):
                print("Procesando", f)
                procesa(f)
    elif not os.path.isdir(root):
        print("No existe directorio", root)
    elif (not os.path.isfile(root + "/README.md")) or (not os.path.isdir(root + "/capitulos")):
        print("No existe archivo README.md o directorio de capítulos")
    else:
        if '/' in root or '\\' in root:
            print("El nombre del directorio no debe contener barras")
        else:
            procesa(root)
