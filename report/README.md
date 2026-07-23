# Informe final ampliado

Este directorio contiene la versión extensa del informe del proyecto PINN--HRF.

## Compilación

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

La bibliografía se procesa con BibTeX mediante `latexmk`.

## Contenido

- `main.tex`: documento principal.
- `sections/`: capítulos y apéndices.
- `figures/`: figuras generadas por los notebooks y gráficos de síntesis.
- `tables/`: CSV de resultados exactos utilizados para auditoría.
- `references.bib`: bibliografía.

El informe distingue explícitamente entre verificación sintética bajo modelo correctamente especificado y aplicación real exploratoria.

Link del video: https://drive.google.com/file/d/1M47oeaWy-gqEI8wY3vhF6Gqxt67hvKkD/view?usp=sharing
