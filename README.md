# 🛡️ Aegis Pentest Automation

CLI interactiva para automatización de pentesting web. Wrapper de herramientas de seguridad con interfaz moderna y **manejo automático de privilegios de administrador**.

## 🎯 Características

- **CLI Interactiva**: Menús intuitivos con Rich
- **4 Tipos de Escaneo**: Rápido, completo, vulnerabilidades, sigiloso
- **Herramientas Integradas**: Nmap, Nuclei, Gobuster, Nikto, SQLMap
- **Visualización Rica**: Tablas, progress bars, colores semánticos
- **Configuración YAML**: Sistema de configuración flexible
- **Sistema de Logging**: Monitoreo en tiempo real con logs detallados
- **🔐 Manejo de Privilegios**: Elevación automática de permisos para herramientas que lo requieren

## ⚡ Instalación y Uso

### Requisitos
- Python 3.9+
- Poetry
- Privilegios de administrador/sudo (para funcionalidad completa)

### Instalación
```bash
git clone git@github.com:Daniel-Santiago-Acosta-1013/Aegis.git
cd Aegis
poetry install
```

### Ejecutar (Comando Único)
```bash
# Un solo comando optimizado que maneja todo automáticamente
poetry run python aegis_cli.py
```

**¡Eso es todo!** 🎯 El comando único:
- ✅ Verifica dependencias automáticamente
- 🔐 Maneja privilegios de administrador
- 🛠️ Detecta herramientas disponibles
- 🚀 Inicia la aplicación optimizada

## 🔐 Sistema de Privilegios

### ¿Por qué necesita privilegios de administrador?

Aegis necesita privilegios elevados para:
- **Escaneos SYN Stealth** (`-sS`) con Nmap
- **Detección de Sistemas Operativos** (`-O`)
- **Escaneos UDP** con herramientas especializadas
- **Funcionalidades avanzadas** de pentesting

### Manejo Automático de Privilegios

✅ **Al inicio**, Aegis verifica automáticamente:
- Si tienes privilegios de administrador
- Si `sudo` está disponible
- Solicita credenciales cuando sea necesario

✅ **Durante ejecución**, las herramientas:
- Se ejecutan con `sudo` automáticamente si lo requieren
- Muestran claramente cuándo usan privilegios elevados
- Manejan errores de permisos de forma inteligente

### Estados de Privilegios

| Estado | Descripción | Funcionalidad |
|--------|-------------|---------------|
| 🔐 **Administrador** | Ejecutándose como root/admin | Completa |
| 🔑 **Sudo Disponible** | Usuario con sudo configurado | Completa (con solicitud de password) |
| ⚠️ **Limitado** | Sin privilegios elevados | Parcial (algunos escaneos fallarán) |

## 📋 Sistema de Logging Avanzado

Aegis incluye un sistema de logging completo que monitorea todas las herramientas en tiempo real.

### Características del Sistema de Logs

- **📊 Monitoreo en Tiempo Real**: Visualización en vivo del estado de herramientas
- **📁 Logs Unificados**: Todos los outputs en archivos organizados
- **🚨 Detección de Errores**: Identificación automática de fallos y timeouts
- **⚡ Thread-Safe**: Manejo seguro de múltiples herramientas simultáneas
- **🎯 Progreso Visual**: Barras de progreso y estados por herramienta
- **🔐 Log de Privilegios**: Registro de cuándo se usan permisos elevados

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
- **Registro de Privilegios**: Cuándo se ejecutaron comandos con sudo
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
│  5  │ Análisis SSL/TLS - Certificados       │
│  6  │ Modo Interactivo - Config. avanzada   │
│  7  │ Estado de Herramientas                │
│  8  │ Estado de Privilegios                 │
│  9  │ Configuración                         │
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

| Tipo                 | Duración  | Privilegios | Descripción                   |
|----------------------|-----------|-------------|-------------------------------|
| **Rápido**           | 5-15 min  | 🔐 Requeridos | Puertos comunes (1-1000) con SYN stealth |
| **Completo**         | 30-60 min | 🔐 Requeridos | Todos los puertos + servicios + OS |
| **Vulnerabilidades** | 20-45 min | 🔐 Requeridos | CVEs con Nuclei + SQLMap      |
| **Sigiloso**         | 10-30 min | 🔐 Requeridos | Técnicas de evasión           |

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

### Errores de Privilegios

**Error "Permission denied" o "requires root privileges":**
```bash
# El comando único maneja esto automáticamente
poetry run python aegis_cli.py

# Si aparece el prompt, permite la reejección con sudo
```

**Sudo no funciona:**
- Verificar que tu usuario esté en el grupo `sudo`:
  ```bash
  groups $USER
  ```
- Agregar usuario a sudo (como root):
  ```bash
  usermod -aG sudo $USER
  ```

### Otros Errores Comunes

**Error de módulos:**
```bash
poetry install  # Reinstalar dependencias
```

**Herramientas no encontradas:**
- El comando único muestra herramientas faltantes automáticamente
- Instalar herramientas sugeridas según el sistema operativo
- Configurar rutas en `~/.aegis/config.yaml` si es necesario

**Problemas con logs:**
- Los logs se guardan automáticamente en `logs/`
- Verificar permisos de escritura en el directorio
- Revisar archivo de log para detalles de errores

### Verificación Rápida del Sistema

```bash
# El comando único hace todas estas verificaciones automáticamente:
poetry run python aegis_cli.py

# Mostrará:
# ✅ Versión de Python correcta
# ✅ Dependencias principales verificadas  
# 🔑 Usuario normal detectado - privilegios sudo disponibles
# ✅ Herramientas disponibles: nmap
# 🎯 Sistema verificado - Iniciando Aegis
```

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

**🔐 Nota de Seguridad**: Aegis solicita privilegios de administrador para funcionalidad completa de pentesting. Siempre verifica el código fuente antes de ejecutar con sudo.