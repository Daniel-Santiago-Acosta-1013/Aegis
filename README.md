# Aegis - Automatización de Pentesting Web

![Aegis Logo](https://img.shields.io/badge/Aegis-Pentest%20Automation-red?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![Qt](https://img.shields.io/badge/Qt-6.6+-green?style=for-the-badge&logo=qt)

## Descripción

Aegis es una aplicación de automatización de pentesting web desarrollada en Python que actúa como wrapper de las herramientas de seguridad más actualizadas. Proporciona una interfaz gráfica moderna basada en Qt6 para facilitar la ejecución y gestión de pruebas de penetración web.

## Características

- 🎯 **Interfaz Gráfica Moderna**: GUI basada en Qt6 con diseño intuitivo
- 🔧 **Wrapper de Herramientas**: Integración con las mejores herramientas de pentesting
- 📊 **Reportes Automáticos**: Generación de reportes en múltiples formatos
- ⚡ **Ejecución Paralela**: Múltiples pruebas simultáneas
- 🔍 **Análisis Completo**: Desde reconocimiento hasta explotación
- 💾 **Gestión de Proyectos**: Organización y persistencia de resultados

## Herramientas Integradas

### Reconocimiento
- **Nmap**: Escaneo de puertos y servicios
- **Nuclei**: Templates de vulnerabilidades
- **Subfinder**: Enumeración de subdominios
- **Gobuster**: Fuzzing de directorios

### Análisis de Vulnerabilidades
- **Nikto**: Escáner de vulnerabilidades web
- **SQLMap**: Detección de inyecciones SQL
- **OWASP ZAP**: Proxy y escáner de seguridad
- **Wapiti**: Auditoría de aplicaciones web

### Explotación
- **Metasploit**: Framework de explotación
- **Burp Suite**: Herramientas de testing manual
- **Hydra**: Ataques de fuerza bruta

## Instalación

### Requisitos Previos

```bash
# macOS
brew install python3 poetry nmap gobuster nuclei nikto

# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip nmap gobuster
pip3 install poetry

# Instalar herramientas adicionales
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
```

### Instalación del Proyecto

```bash
# Clonar el repositorio
git clone <repository-url>
cd aegis-pentest-automation

# Instalar dependencias con Poetry
poetry install

# Activar el entorno virtual
poetry shell
```

## Uso

### Interfaz Gráfica

```bash
# Ejecutar la aplicación GUI
poetry run aegis-pentest
```

### Línea de Comandos

```bash
# Escaneo básico
aegis-pentest scan --target example.com

# Escaneo completo con todas las herramientas
aegis-pentest full-audit --target example.com --output report.html
```

## Estructura del Proyecto

```
aegis-pentest-automation/
├── aegis_pentest/
│   ├── __init__.py
│   ├── main.py                 # Punto de entrada principal
│   ├── gui/
│   │   ├── __init__.py
│   │   ├── main_window.py      # Ventana principal de Qt
│   │   ├── widgets/            # Widgets personalizados
│   │   └── styles/             # Estilos CSS para Qt
│   ├── core/
│   │   ├── __init__.py
│   │   ├── scanner.py          # Motor principal de escaneo
│   │   ├── project_manager.py  # Gestión de proyectos
│   │   └── report_generator.py # Generación de reportes
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── nmap_wrapper.py     # Wrapper para Nmap
│   │   ├── nuclei_wrapper.py   # Wrapper para Nuclei
│   │   ├── sqlmap_wrapper.py   # Wrapper para SQLMap
│   │   └── ...                 # Otros wrappers
│   └── utils/
│       ├── __init__.py
│       ├── config.py           # Configuración global
│       └── helpers.py          # Funciones auxiliares
├── tests/                      # Tests unitarios
├── docs/                       # Documentación
├── resources/                  # Recursos (iconos, templates)
└── examples/                   # Ejemplos de uso
```

## Configuración

El archivo de configuración se encuentra en `~/.aegis/config.yaml`:

```yaml
tools:
  nmap:
    path: "/usr/bin/nmap"
    timeout: 300
  nuclei:
    path: "/usr/local/bin/nuclei"
    templates_path: "~/nuclei-templates"
  
output:
  default_format: "html"
  save_path: "~/aegis-reports"

threading:
  max_workers: 4
```

## Contribuir

1. Fork el proyecto
2. Crea una rama feature (`git checkout -b feature/amazing-feature`)
3. Commit tus cambios (`git commit -m 'Add amazing feature'`)
4. Push a la rama (`git push origin feature/amazing-feature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Descargo de Responsabilidad

Esta herramienta está destinada únicamente para uso educativo y pruebas de seguridad autorizadas. El uso no autorizado de esta herramienta en sistemas que no son de su propiedad es ilegal. Los desarrolladores no se responsabilizan por el mal uso de esta herramienta.

## Soporte

- 📧 Email: support@aegis-security.com
- 🐛 Issues: [GitHub Issues](link-to-issues)
- 📖 Documentación: [Wiki](link-to-wiki) 