# 📋 Sistema de Logs de Aegis Pentest

Este directorio contiene los archivos de log generados durante la ejecución de análisis de pentesting.

## 📁 Estructura de Archivos

Los archivos de log siguen el patrón:
```
aegis_analysis_YYYYMMDD_HHMMSS.txt
```

Ejemplo: `aegis_analysis_20241225_143052.txt`

## 📊 Contenido de los Logs

Cada archivo de log contiene:

### Header
- Fecha y hora de inicio del análisis
- Información del sistema
- Nombre del archivo de log

### Logs de Herramientas
- **INICIO**: Cuando se inicia una herramienta
- **COMANDO**: Comando exacto ejecutado
- **OUTPUT**: Salida en tiempo real de la herramienta
- **ERROR**: Errores encontrados durante la ejecución
- **PROGRESO**: Actualizaciones de progreso
- **FIN**: Finalización de la herramienta con estado

### Resumen por Herramienta
Al final de cada herramienta se incluye:
- ID único de ejecución
- Estado final (COMPLETADO/ERROR/TIMEOUT)
- Comando ejecutado
- Target analizado
- Duración total
- Outputs completos
- Errores encontrados

### Footer
- Fecha y hora de finalización
- Total de herramientas ejecutadas
- Referencia al archivo de log

## 🔍 Ejemplo de Contenido

```
================================================================================
AEGIS PENTEST AUTOMATION - ANÁLISIS LOG
================================================================================
Fecha/Hora inicio: 2024-12-25 14:30:52
Archivo de log: aegis_analysis_20241225_143052.txt
================================================================================

2024-12-25 14:30:53 | INFO     | aegis_tools    | INICIO | nmap | Target: example.com
2024-12-25 14:30:53 | INFO     | aegis_tools    | COMANDO | nmap | nmap -sS -sV -p 1-1000 -v example.com
2024-12-25 14:30:53 | INFO     | aegis_tools    | PROGRESO | nmap | 5% | Iniciando proceso...
2024-12-25 14:30:54 | INFO     | aegis_tools    | OUTPUT | nmap | Starting Nmap 7.94 ( https://nmap.org )
2024-12-25 14:30:54 | INFO     | aegis_tools    | OUTPUT | nmap | Initiating SYN Stealth Scan
...

------------------------------------------------------------
RESUMEN DE HERRAMIENTA: NMAP
------------------------------------------------------------
ID: nmap_1703515853
Estado Final: COMPLETADO
Comando: nmap -sS -sV -p 1-1000 -v example.com
Target: example.com
Inicio: 2024-12-25 14:30:53
Fin: 2024-12-25 14:32:15
Duración: 0:01:22

OUTPUTS (45 líneas):
[14:30:54] Starting Nmap 7.94 ( https://nmap.org )
[14:30:54] Initiating SYN Stealth Scan
...

ERRORES (0 líneas):

------------------------------------------------------------

================================================================================
FIN DEL ANÁLISIS
================================================================================
Fecha/Hora fin: 2024-12-25 14:35:20
Total de herramientas ejecutadas: 3
Archivo de log: aegis_analysis_20241225_143052.txt
================================================================================
```

## 🔧 Características del Sistema

### Monitoreo en Tiempo Real
- Muestra logs en vivo en el CLI
- Tabla de estado actualizada cada 2 segundos
- Barras de progreso por herramienta
- Indicadores de estado con colores

### Detección de Errores
- Detecta herramientas no encontradas
- Maneja timeouts automáticamente
- Captura errores de ejecución
- Logs de stderr separados

### Thread Safety
- Logs seguros para concurrencia
- Múltiples herramientas simultáneas
- Sincronización automática

## 📈 Uso de los Logs

### Para Debugging
Los logs permiten:
- Identificar exactamente qué falló
- Ver el comando exacto ejecutado
- Analizar la salida completa de herramientas
- Detectar problemas de configuración

### Para Auditoría
Los logs proporcionan:
- Rastro completo de todas las actividades
- Timestamps precisos
- Evidencia de comandos ejecutados
- Resultados completos de análisis

### Para Análisis Post-Mortem
Los logs incluyen:
- Duración exacta de cada herramienta
- Identificación de cuellos de botella
- Patrones de error
- Información de rendimiento

## ⚠️ Nota Importante

Los archivos `.txt` y `.log` en este directorio son ignorados por Git para:
- Evitar datos sensibles en el repositorio
- Mantener el repo limpio
- Proteger información de targets

El directorio `logs/` se mantiene en Git para estructura, pero no los archivos de log. 