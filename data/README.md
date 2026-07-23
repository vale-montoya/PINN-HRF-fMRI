# Datos

## Datos reales

La aplicación real utiliza datos de tarea motora 3T del Human Connectome Project para el sujeto `100206`.

Los datos crudos no deben subirse a GitHub. La estructura local utilizada durante el desarrollo fue:

```text
data/raw/100206/MNINonLinear/Results/
├── tfMRI_MOTOR_LR/
│   ├── tfMRI_MOTOR_LR_hp0_clean_rclean_tclean.nii.gz
│   ├── Movement_Regressors.txt
│   └── EVs/
│       ├── cue.txt
│       ├── lf.txt
│       ├── lh.txt
│       ├── rf.txt
│       ├── rh.txt
│       └── t.txt
└── tfMRI_MOTOR_RL/
    ├── tfMRI_MOTOR_RL_hp0_clean_rclean_tclean.nii.gz
    ├── Movement_Regressors.txt
    └── EVs/
        ├── cue.txt
        ├── lf.txt
        ├── lh.txt
        ├── rf.txt
        ├── rh.txt
        └── t.txt
```

Los archivos `.nii.gz` y los datos sujetos a condiciones de acceso se mantienen fuera del repositorio.

## Datos procesados livianos



- series temporales BOLD de las ROI;
- metadatos de adquisición;
- tablas de bloques;
- configuraciones de escenarios;
- resúmenes de control de calidad.


## Datos sintéticos

Los datos sintéticos pueden regenerarse a partir de:

- los parámetros de `configs/`;
- los archivos de eventos;
- el modelo Balloon–Windkessel;
- las semillas aleatorias documentadas.

No es necesario versionar archivos sintéticos muy grandes si existen scripts reproducibles para generarlos.
