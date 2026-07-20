# Estimación robusta de la HRF en fMRI mediante PINNs

Proyecto final de la asignatura **Inteligencia Artificial en Salud**, desarrollado por **Valentinna Belén Montoya Aising**, estudiante del **Magíster en Ciencias de la Ingeniería Biomédica**, bajo la docencia del **Dr. Alejandro Veloz Baeza**.

## Descripción

Este proyecto implementa y evalúa una **red neuronal informada por la física (PINN)** para estimar la función de respuesta hemodinámica (HRF) y parámetros efectivos del modelo **Balloon–Windkessel** a partir de señales fMRI BOLD.

La metodología combina:

- fidelidad a los datos BOLD;
- residuos de las ecuaciones diferenciales del modelo Balloon–Windkessel;
- condiciones iniciales de homeostasis;
- diferenciación automática;
- optimización Adam seguida de L-BFGS;
- simulación ODE independiente para evaluar la generalización fuera de muestra.

El método propuesto se compara con dos referencias:

1. **GLM** con HRF canónica de SPM;
2. **MLP** puramente basada en datos y sin restricciones fisiológicas.

## Diseño experimental

### Validación sintética

Se generaron señales sintéticas con parámetros conocidos y tres niveles de relación señal–ruido:

- SNR = 10;
- SNR = 5;
- SNR = 2.

El diseño incluyó 4 escenarios, 3 niveles de SNR y 5 réplicas, para un total de **60 experimentos pareados por modelo**.

### Aplicación en fMRI real

Se utilizaron datos de tarea motora 3T del **Human Connectome Project**, sujeto **100206**, corridas LR y RL. Se analizaron señales de la corteza motora primaria izquierda y derecha.

La evaluación real fue bidireccional:

- entrenamiento en bloque 1 y evaluación en bloque 2;
- entrenamiento en bloque 2 y evaluación en bloque 1.

Esto produjo **8 evaluaciones reales** para cada modelo.

## Resultados principales

### Datos sintéticos

La PINN obtuvo un desempeño robusto en los tres niveles de ruido:

| SNR | RMSE fuera de muestra [% BOLD] | R² fuera de muestra | R² de la HRF |
|---:|---:|---:|---:|
| 10 | 0.0577 ± 0.0234 | 0.9922 | 0.9923 |
| 5 | 0.0655 ± 0.0263 | 0.9900 | 0.9902 |
| 2 | 0.0800 ± 0.0428 | 0.9836 | 0.9826 |

Las pruebas de Friedman y Wilcoxon pareadas mostraron diferencias significativas a favor de la PINN frente al GLM y la MLP en reconstrucción y recuperación de la HRF.

### Datos reales

| Modelo | RMSE medio [% BOLD] | R² medio | Pearson medio | Ganadores por RMSE |
|---|---:|---:|---:|---:|
| PINN | **0.5019** | **0.152** | **0.754** | **4/8** |
| GLM | 0.5538 | 0.035 | 0.460 | 2/8 |
| MLP | 0.5646 | -0.142 | 0.711 | 2/8 |

En los datos reales no se observaron diferencias globales significativas en RMSE (`p = 0.2231`). Sí se identificaron diferencias globales en correlación temporal (`p = 0.0076`): tanto la MLP como la PINN superaron al GLM, sin diferencia significativa entre MLP y PINN.

La MLP presentó la mayor brecha entre entrenamiento y prueba, compatible con una mayor tendencia al sobreajuste. La HRF estimada por la PINN mostró una correlación media bidireccional de **0.958**.

## Alcance e interpretación

Los resultados sintéticos validan el método cuando el modelo generador y los parámetros verdaderos son conocidos. La aplicación real constituye una evaluación metodológica sobre un sujeto y cuatro combinaciones corrida–ROI; no corresponde a una validación clínica ni poblacional.

Los parámetros estimados (`epsilon`, `tau`, `alpha`) deben interpretarse como **parámetros efectivos del modelo bajo las constantes, las regiones de interés y el preprocesamiento utilizados**, no como mediciones clínicas directas.

## Estructura del repositorio

```text
.
├── configs/                 Configuraciones reproducibles
├── data/                    Documentación y datos procesados livianos
├── docs/                    Evolución del proyecto y decisiones metodológicas
├── notebooks/               Desarrollo reproducible y experimentos
├── report/                  Código LaTeX, figuras, tablas y PDF final
├── results/                 Resultados finales livianos
├── scripts/                 Utilidades de auditoría y preparación
├── src/pinn_hrf/            Código modular reutilizable
├── tests/                   Pruebas mínimas del modelo fisiológico
├── requirements.txt
└── README.md
```

## Requisitos

- Python 3.10 o superior
- Entorno con GPU recomendado para entrenar las PINN
- Acceso autorizado a los datos HCP para reproducir la aplicación real

Instalación:

```bash
python -m venv .venv
```

En Windows:

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

En Linux/macOS:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

## Datos

Los archivos fMRI crudos no se incluyen en el repositorio debido a su tamaño y a las condiciones de uso del HCP. Consulta [`data/README.md`](data/README.md) para conocer la estructura esperada y los archivos mínimos requeridos.

## Reproducción

El flujo general es:

1. preparar las señales BOLD y los archivos de eventos;
2. generar y validar el conjunto sintético;
3. ejecutar GLM, MLP y PINN sobre datos sintéticos;
4. ejecutar la comparación estadística sintética;
5. preparar los datos reales y realizar control de calidad;
6. ejecutar los ocho experimentos reales;
7. consolidar tablas, pruebas estadísticas y figuras finales.

Los notebooks deben conservar una numeración secuencial y ejecutarse en orden. El orden exacto se documentará en [`notebooks/README.md`](notebooks/README.md).

## Informe

El código fuente LaTeX y el PDF final se almacenarán en `report/`. El informe no incluirá listados extensos del código; la implementación completa se evaluará desde este repositorio.

## Limitaciones

- análisis real limitado a un sujeto;
- número reducido de escenarios reales;
- identificabilidad limitada de algunos parámetros, especialmente `tau`;
- dependencia de constantes fisiológicas fijadas;
- ausencia de validación clínica y multicéntrica;
- las asociaciones entre repetibilidad y desempeño son exploratorias.

## Autor

**Valentinna Belén Montoya Aising**  
Magíster en Ciencias de la Ingeniería Biomédica  
Universidad de Valparaíso
