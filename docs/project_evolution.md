# Evolución del alcance del proyecto

## Pregunta central preservada

Desde la propuesta inicial, el proyecto mantuvo la misma pregunta científica: evaluar si la incorporación explícita del modelo Balloon–Windkessel en una red neuronal informada por la física permite estimar la HRF con mayor robustez e interpretabilidad que métodos convencionales o puramente basados en datos.

## Alcance planteado inicialmente

La propuesta consideró:

- una cohorte de 40 sujetos HCP;
- múltiples ROI;
- validación externa mediante OpenNeuro;
- comparación principal con GLM;
- inferencia de variables y parámetros neurovasculares.

## Ajuste del alcance en la entrega final

La implementación final priorizó profundidad metodológica y reproducibilidad:

- 60 experimentos sintéticos con ground truth conocido;
- comparación pareada GLM–MLP–PINN;
- tres niveles de SNR y cinco réplicas;
- aplicación real al sujeto HCP 100206;
- corridas MOTOR LR y MOTOR RL;
- M1 izquierda y derecha;
- evaluación bidireccional entre bloques;
- ocho experimentos reales por modelo;
- pruebas estadísticas pareadas;
- análisis de sobreajuste y consistencia de parámetros y HRF.

## Justificación

El ajuste se realizó por cuatro razones:

1. Los paquetes completos de fMRI por sujeto presentan un costo elevado de almacenamiento y transferencia.
2. La validación de una PINN inversa requiere comprobar primero la identificabilidad en un entorno con parámetros verdaderos conocidos.
3. Los primeros pilotos mostraron que una formulación física blanda podía producir soluciones aparentes sin generalización; fue necesario reformular el método antes de escalarlo.
4. Un análisis profundo y reproducible sobre un sujeto, acompañado por una validación sintética extensa, entrega evidencia más defendible que una cohorte amplia procesada con una formulación no validada.

## Coherencia con las entregas parciales

La entrega final conserva:

- el mismo problema de estimación robusta de la HRF;
- el uso del modelo Balloon–Windkessel;
- el uso de PINNs y diferenciación automática;
- el conjunto HCP y los eventos reales;
- la comparación con el GLM;
- la inferencia de parámetros latentes;
- la preocupación por ruido, convergencia y generalización.

Los cambios corresponden al alcance experimental, la implementación en PyTorch y la incorporación de una MLP como referencia adicional. Estos ajustes deben explicarse explícitamente en el informe y la presentación para demostrar desarrollo sistemático y evitar que parezcan inconsistencias no justificadas.
