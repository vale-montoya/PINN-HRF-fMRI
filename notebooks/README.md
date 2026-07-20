# Notebooks

Los notebooks deben renombrarse con una secuencia estable y un título descriptivo. La propuesta de orden es:

```text
01_preparacion_datos_hcp.ipynb
02_extraccion_roi_motor.ipynb
03_glm_datos_reales_inicial.ipynb
04_generacion_datos_sinteticos.ipynb
05_mlp_sintetica.ipynb
06_pinn_sintetica_piloto.ipynb
06b_pinn_inversa_ventana.ipynb
07_pinn_sintetica_lote.ipynb
08_comparacion_sintetica.ipynb
09_preparacion_datos_reales.ipynb
10_modelos_reales_piloto.ipynb
11_modelos_reales_lote.ipynb
12_analisis_final_experimentos.ipynb
```

Los nombres `01`–`04` deben ajustarse a los notebooks reales existentes. No dupliques notebooks equivalentes.

## Recomendaciones

- Mantener una breve celda Markdown al inicio con objetivo, entradas y salidas.
- Usar rutas relativas o una única variable `PROJECT_ROOT`.
- Guardar configuraciones relevantes en `configs/`.
- Evitar resultados intermedios innecesariamente grandes.
- Conservar las salidas finales que demuestran reproducibilidad.
- No incluir credenciales ni rutas personales.
- No subir los datos HCP crudos.
- Los notebooks de lote deben poder reanudarse sin duplicar resultados.
