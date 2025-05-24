# 🛡️ Aegis Pentest Automation

Una aplicación moderna de automatización de pentesting web con **interfaz CLI interactiva enriquecida**. Actúa como wrapper inteligente de las herramientas de seguridad más actualizadas.

## ✨ Características

- 🖥️ **CLI Interactiva**: Interfaz completamente interactiva con Rich y menús intuitivos
- 🎯 **Múltiples Tipos de Escaneo**: Rápido, completo, vulnerabilidades y sigiloso
- 🔧 **Herramientas Integradas**: Nmap, Nuclei, Gobuster, Nikto, SQLMap y más
- 📊 **Visualización Rica**: Tablas, progress bars, paneles y colores semánticos
- ⚙️ **Configuración Avanzada**: Sistema de configuración YAML completo
- 🚀 **Modo Asíncrono**: Operaciones concurrentes para mejor rendimiento
- 📋 **Gestión de Proyectos**: Organización automática de resultados
- 📄 **Reportes Múltiples**: HTML, JSON, XML y texto plano

## 🚀 Instalación Rápida

```bash
# Clonar repositorio
git clone https://github.com/aegis-security/aegis-pentest.git
cd aegis-pentest

# Instalar dependencias con Poetry (recomendado)
poetry install

# O instalar con pip
pip install -e .
```

## 📖 Uso

### Ejecutar CLI Interactiva

```bash
# Con Poetry
poetry run python aegis_cli.py

# O directamente
python aegis_cli.py

# O como script instalado
aegis
```

### Menú Principal

Al ejecutar, verás un menú interactivo con opciones:

```
╭─────────────────────────────────────────────╮
│           🎯 Menú Principal                 │
├─────┬───────────────────────────────────────┤
│  1  │ Escaneo Rápido - Puertos comunes     │
│  2  │ Escaneo Completo - Múltiples herram. │
│  3  │ Escaneo de Vulnerabilidades - CVEs   │
│  4  │ Escaneo Sigiloso - Evasión           │
│  5  │ Modo Interactivo - Config. avanzada  │
│  6  │ Estado de Herramientas               │
│  7  │ Configuración                        │
│  0  │ Salir                                │
╰─────┴───────────────────────────────────────╯
```

### Flujo de Trabajo Típico

1. **Seleccionar tipo de escaneo**: Elige entre rápido, completo, vulnerabilidades o sigiloso
2. **Ingresar objetivo**: IP, dominio o red (ej: `scanme.nmap.org`, `192.168.1.0/24`)
3. **Configurar parámetros**: Puertos, opciones avanzadas según el tipo
4. **Ejecutar escaneo**: Ver progreso en tiempo real con barras visuales
5. **Revisar resultados**: Tablas organizadas con puertos, servicios y vulnerabilidades

## 🎨 Características Visuales

### Banner ASCII Artístico
```
    ___    __________ _____ _____
   /   |  / ____/ __ \_   _/ ___/
  / /| | / __/ / / / / // / \__ \ 
 / ___ |/ /___/ /_/ _// /_____/ / 
/_/  |_/_____/\____/___//____/  

🛡️  Automatización de Pentesting Web 🛡️
```

### Visualización de Resultados
- **Estadísticas**: Resumen ejecutivo con métricas clave
- **Puertos**: Tabla de puertos abiertos con estados y servicios
- **Vulnerabilidades**: Lista priorizada por severidad (Critical → Info)
- **Servicios**: Información detallada de servicios detectados
- **OS Detection**: Identificación del sistema operativo objetivo

### Colores Semánticos
- 🟢 **Verde**: Éxito, disponible, seguro
- 🔴 **Rojo**: Error, crítico, no disponible
- 🟡 **Amarillo**: Advertencia, moderado
- 🔵 **Azul**: Información, configuración
- 🟣 **Magenta**: Avanzado, sigiloso

## 🔧 Herramientas Soportadas

| Herramienta | Función | Estado |
|-------------|---------|--------|
| **Nmap** | Escaneo de puertos y servicios | ✅ Core |
| **Nuclei** | Detección de vulnerabilidades | ✅ Integrado |
| **Gobuster** | Enumeración de directorios | ✅ Integrado |
| **Nikto** | Análisis de vulnerabilidades web | ✅ Integrado |
| **SQLMap** | Detección de inyecciones SQL | ✅ Integrado |
| **Hydra** | Ataques de fuerza bruta | 🔜 Próximamente |
| **Subfinder** | Enumeración de subdominios | 🔜 Próximamente |

## ⚙️ Configuración

### Archivo de Configuración
Ubicación: `~/.aegis/config.yaml`

```yaml
tools:
  nmap:
    path: /usr/local/bin/nmap
    timeout: 300
    default_args: ['-sV', '-sC', '--version-light']
  
  nuclei:
    path: /usr/local/bin/nuclei
    timeout: 600
    templates_path: ~/nuclei-templates

output:
  default_format: html
  save_path: ~/aegis-reports
  auto_save: true

threading:
  max_workers: 4
  timeout_multiplier: 1.5
```

### Variables de Entorno
```bash
export AEGIS_CONFIG="/path/to/custom/config.yaml"
export AEGIS_TOOLS_PATH="/custom/tools/path"
export AEGIS_OUTPUT_DIR="/custom/output/path"
```

## 🎯 Tipos de Escaneo

### 1. Escaneo Rápido (5-15 min)
- Nmap en puertos comunes (1-1000)
- Detección básica de servicios
- Ideal para reconocimiento inicial

### 2. Escaneo Completo (30-60 min)
- Nmap en todos los puertos (1-65535)
- Detección de OS y servicios
- Scripts NSE opcionales
- Gobuster para enumeración web

### 3. Escaneo de Vulnerabilidades (20-45 min)
- Nuclei con templates actualizados
- Scripts NSE de vulnerabilidades
- SQLMap para inyecciones SQL
- Nikto para análisis web

### 4. Escaneo Sigiloso (10-30 min)
- Técnicas de evasión
- Timeouts extendidos
- Fragmentación de paquetes
- Ideal para entornos monitoreados

## 📊 Ejemplos de Salida

### Estado de Herramientas
```
╭──────────────┬──────────────────┬──────────────────────┬─────────────────────╮
│ Herramienta  │      Estado      │       Versión        │        Ruta         │
├──────────────┼──────────────────┼──────────────────────┼─────────────────────┤
│ NMAP         │  🟢 Disponible   │ Nmap version 7.95    │ /usr/local/bin/nmap │
│ NUCLEI       │  🟢 Disponible   │ v3.0.4               │ /usr/bin/nuclei     │
│ GOBUSTER     │ 🔴 No disponible │ N/A                  │ No encontrado       │
╰──────────────┴──────────────────┴──────────────────────┴─────────────────────╯
```

### Resultados de Escaneo
```
╭────────────────────────────────────────────────────────────────────╮
│                        📊 Estadísticas                           │
├─────────────────┬──────────┬────────────────────────────────────────┤
│ Puertos Escaneados │    1000    │                🔍                │
│ Puertos Abiertos   │      8     │                🟢                │
│ Servicios Detectados │    6     │                ⚙️                │
│ Vulnerabilidades   │      3     │                🚨                │
╰─────────────────┴──────────┴────────────────────────────────────────╯
```

## 🛠️ Instalación de Herramientas

### Ubuntu/Debian
```bash
# Herramientas básicas
sudo apt update && sudo apt install -y nmap nikto sqlmap

# Gobuster
wget https://github.com/OJ/gobuster/releases/download/v3.6.0/gobuster_Linux_x86_64.tar.gz
tar -xzf gobuster_Linux_x86_64.tar.gz
sudo mv gobuster /usr/local/bin/

# Nuclei
GO111MODULE=on go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
```

### macOS
```bash
# Con Homebrew
brew install nmap gobuster nikto sqlmap

# Nuclei
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
```

### Windows
- Descargar binarios desde las páginas oficiales
- Agregar al PATH del sistema
- Configurar rutas en `~/.aegis/config.yaml`

## 🚦 Troubleshooting

### Herramientas No Encontradas
```bash
# Verificar estado
python aegis_cli.py  # Opción 6: Estado de Herramientas

# Instalar herramientas faltantes
sudo apt install nmap nikto  # Linux
brew install nmap nikto      # macOS
```

### Errores de Permisos
```bash
# Linux/macOS
chmod +x aegis_cli.py
sudo chown $USER:$USER ~/.aegis/

# Verificar permisos de herramientas
ls -la /usr/local/bin/nmap
```

### Problemas de Red
- Verificar conectividad: `ping target.com`
- Probar con diferentes objetivos
- Revisar configuración de proxy/firewall

## 🎓 Casos de Uso

### Para DevSecOps
- Integración en pipelines CI/CD
- Auditorías automatizadas programadas
- Generación de reportes para compliance

### Para Administradores de Sistema
- Monitoreo continuo de infraestructura
- Validación de configuraciones de seguridad
- Detección temprana de vulnerabilidades

### Para Pentesters
- Reconocimiento inicial automatizado
- Enumeración comprehensiva de servicios
- Detección de vectores de ataque

### Para Analistas de Seguridad
- Análisis de superficie de ataque
- Correlación de vulnerabilidades
- Reporting ejecutivo

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el repositorio
2. Crear branch de feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push al branch (`git push origin feature/nueva-funcionalidad`)
5. Abrir Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para detalles.

## 🆘 Soporte

- **Documentación**: [Wiki del proyecto](https://github.com/aegis-security/aegis-pentest/wiki)
- **Issues**: [GitHub Issues](https://github.com/aegis-security/aegis-pentest/issues)
- **Discusiones**: [GitHub Discussions](https://github.com/aegis-security/aegis-pentest/discussions)
- **Email**: aegis@security.com

---

**⚠️ Nota Legal**: Esta herramienta está diseñada para profesionales de seguridad y uso educativo. Úsala únicamente en sistemas que poseas o tengas autorización explícita para probar. El uso indebido puede ser ilegal.

**🛡️ Aegis Security Team - 2024** 