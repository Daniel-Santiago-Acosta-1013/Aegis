# 🛡️ Aegis Pentest Automation

CLI interactiva para automatización de pentesting web. Wrapper de herramientas de seguridad con interfaz moderna.

## 🎯 Características

- **CLI Interactiva**: Menús intuitivos con Rich
- **4 Tipos de Escaneo**: Rápido, completo, vulnerabilidades, sigiloso
- **Herramientas Integradas**: Nmap, Nuclei, Gobuster, Nikto, SQLMap
- **Visualización Rica**: Tablas, progress bars, colores semánticos
- **Configuración YAML**: Sistema de configuración flexible
- **Sistema de Logging**: Monitoreo en tiempo real con logs detallados

## ⚡ Instalación y Uso

### Requisitos
- Python 3.9+
- Poetry

### Instalación
```bash
git clone git@github.com:Daniel-Santiago-Acosta-1013/Aegis.git
cd aegis-pentest
poetry install
```

### Ejecutar
```bash
poetry run python aegis_cli.py
```

## 📋 Sistema de Logging Avanzado

Aegis incluye un sistema de logging completo que monitorea todas las herramientas en tiempo real.

### Características del Sistema de Logs

- **📊 Monitoreo en Tiempo Real**: Visualización en vivo del estado de herramientas
- **📁 Logs Unificados**: Todos los outputs en archivos organizados
- **🚨 Detección de Errores**: Identificación automática de fallos y timeouts
- **⚡ Thread-Safe**: Manejo seguro de múltiples herramientas simultáneas
- **🎯 Progreso Visual**: Barras de progreso y estados por herramienta

### Ubicación de Logs

```
logs/
├── aegis_analysis_20241225_143052.txt
├── aegis_analysis_20241225_150230.txt
└── README.md
```

### Contenido de los Logs

Cada archivo incluye:
- **Header**: Información de inicio del análisis
- **Logs en Tiempo Real**: Output completo de cada herramienta
- **Detección de Errores**: Errores y timeouts capturados
- **Resumen por Herramienta**: Estado final, duración, y resultados
- **Footer**: Resumen final del análisis

### Ejemplo de Monitoreo en Vivo

Durante la ejecución verás:

```
┌────────────────── 🔍 Monitoreo de Herramientas en Tiempo Real ──────────────────┐
│ Herramienta │ Estado      │ Progreso              │ Última Actividad             │
├─────────────┼─────────────┼───────────────────────┼─────────────────────────────────┤
│ nmap        │ EJECUTANDO  │ [████████░░] 80%      │ Scanning 192.168.1.1 port 443 │
│ nuclei      │ COMPLETADO  │ [██████████] 100%     │ Completado exitosamente       │
│ gobuster    │ INICIANDO   │ [█░░░░░░░░░] 10%      │ Iniciando escaneo...          │
└─────────────┴─────────────┴───────────────────────┴─────────────────────────────────┘
```

## 📋 Menú Principal

```
╭─────────────────────────────────────────────╮
│           🎯 Menú Principal                  │
├─────┬───────────────────────────────────────┤
│  1  │ Escaneo Rápido - Puertos comunes      │
│  2  │ Escaneo Completo - Múltiples herram.  │
│  3  │ Escaneo de Vulnerabilidades - CVEs    │
│  4  │ Escaneo Sigiloso - Evasión            │
│  5  │ Modo Interactivo - Config. avanzada    │
│  6  │ Estado de Herramientas                │
│  7  │ Configuración                          │
│  0  │ Salir                                 │
╰─────┴───────────────────────────────────────╯
```

## 🔧 Herramientas Requeridas

Instalar herramientas de pentesting:

**Linux/Ubuntu:**
```bash
sudo apt install nmap nikto sqlmap
# Gobuster y Nuclei desde GitHub releases
```

**macOS:**
```bash
brew install nmap nikto sqlmap gobuster
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
```

## 🎯 Tipos de Escaneo

| Tipo                 | Duración  | Descripción                   |
|----------------------|-----------|-------------------------------|
| **Rápido**           | 5-15 min  | Puertos comunes (1-1000)      |
| **Completo**         | 30-60 min | Todos los puertos + servicios |
| **Vulnerabilidades** | 20-45 min | CVEs con Nuclei + SQLMap      |
| **Sigiloso**         | 10-30 min | Técnicas de evasión           |

## ⚙️ Configuración

Archivo: `~/.aegis/config.yaml`
```yaml
tools:
  nmap:
    path: /usr/local/bin/nmap
    timeout: 300
  nuclei:
    path: /usr/local/bin/nuclei
    timeout: 600

output:
  save_path: ~/aegis-reports
  auto_save: true
```

## 🚦 Troubleshooting

**Error de módulos:**
```bash
poetry install  # Reinstalar dependencias
```

**Herramientas no encontradas:**
- Verificar instalación con opción 6 en el menú
- Configurar rutas en `~/.aegis/config.yaml`

**Permisos:**
```bash
chmod +x aegis_cli.py
```

**Problemas con logs:**
- Los logs se guardan automáticamente en `logs/`
- Verificar permisos de escritura en el directorio
- Revisar archivo de log para detalles de errores

## 🔍 Desarrollo y Contribución

### Verificar Calidad de Código

```bash
# Linting
poetry run flake8 aegis_pentest/

# Formateo de código
poetry run black aegis_pentest/

# Type checking
poetry run mypy aegis_pentest/
```

## 📝 Licencia

MIT License - Ver archivo LICENSE

---

**⚠️ Uso Legal**: Solo para sistemas propios o con autorización explícita.