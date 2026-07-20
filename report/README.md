# Informe LaTeX - versión 1

Esta carpeta contiene una primera versión completa y compilable del informe.

## Uso dentro del repositorio

Copia todo el contenido de esta carpeta dentro de `report/` del repositorio, reemplazando el README anterior cuando corresponda.

## Compilación en PowerShell

Desde la raíz del repositorio:

```powershell
cd .\report
latexmk -pdf main.tex
```

Si `latexmk` no está disponible, compila con:

```powershell
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

## Antes de entregar

1. Revisar nombre oficial del programa y unidad académica.
2. Confirmar el nombre del profesor.
3. Incorporar el enlace de la presentación grabada.
4. Revisar que el enlace de GitHub sea correcto.
5. Sustituir o mejorar las figuras cuando se exporten en formato definitivo.
6. Ajustar extensión y formato a las instrucciones específicas del curso.
7. Compilar y revisar visualmente cada página.
