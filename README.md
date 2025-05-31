# Aegis Pentest Automation

CLI interactiva para automatización de pentesting web. Wrapper de herramientas de seguridad con interfaz moderna y manejo automático de privilegios.

## Características Principales

- CLI interactiva con menús intuitivos
- 4 tipos de escaneo: Rápido, completo, vulnerabilidades, sigiloso  
- Herramientas integradas: Nmap, Nuclei, Gobuster, Nikto, SQLMap
- Sistema de logging en tiempo real
- Manejo automático de privilegios de administrador
- Configuración flexible con YAML

## Instalación y Uso

### Requisitos
- Python 3.9+
- Poetry
- Privilegios de administrador/sudo

### Instalación
```bash
git clone git@github.com:Daniel-Santiago-Acosta-1013/Aegis.git
cd Aegis
poetry install
```

### Ejecución
```bash
poetry run aegis
```

El comando verifica dependencias, maneja privilegios y detecta herramientas automáticamente.

## Sistema de Privilegios

Aegis requiere privilegios elevados para:
- Escaneos SYN Stealth (-sS) con Nmap
- Detección de sistemas operativos (-O)
- Escaneos UDP avanzados
- Funcionalidades completas de pentesting

### Estados de Privilegios

| Estado | Descripción | Funcionalidad |
|--------|-------------|---------------|
| Administrador | Ejecutándose como root/admin | Completa |
| Sudo Disponible | Usuario con sudo configurado | Completa |
| Limitado | Sin privilegios elevados | Parcial |

## Sistema de Logging

Los logs se guardan automáticamente en el directorio `logs/` con formato:
```
logs/aegis_analysis_YYYYMMDD_HHMMSS.txt
```

Cada log contiene:
- Header con información del análisis
- Outputs limpios de cada herramienta organizados por secciones
- Errores capturados
- Duración y estado final

### Formato de Logs

```
============================================================
NMAP
============================================================
Target: example.com
Inicio: 2025-05-30 23:43:59
Fin: 2025-05-30 23:44:14
Duración: 0:15

OUTPUTS (25 líneas):
Starting Nmap 7.97 ( https://nmap.org )
NSE: Loaded 158 scripts for scanning
[... outputs en crudo de la herramienta ...]

ERRORES (0 líneas):

============================================================
```

## Menú Principal

```
1. Escaneo Rápido - Puertos comunes
2. Escaneo Completo - Múltiples herramientas  
3. Escaneo de Vulnerabilidades - CVEs
4. Escaneo Sigiloso - Evasión
5. Análisis SSL/TLS - Certificados
6. Modo Interactivo - Configuración avanzada
7. Estado de Herramientas
8. Estado de Privilegios
9. Configuración
0. Salir
```

## Herramientas Requeridas

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

## Tipos de Escaneo

| Tipo | Duración | Privilegios | Descripción |
|------|----------|-------------|-------------|
| Rápido | 5-15 min | Requeridos | Puertos comunes (1-1000) |
| Completo | 30-60 min | Requeridos | Todos los puertos + servicios |
| Vulnerabilidades | 20-45 min | Requeridos | CVEs con Nuclei + SQLMap |
| Sigiloso | 10-30 min | Requeridos | Técnicas de evasión |

## Configuración

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

## Solución de Problemas

### Errores de Privilegios
El comando principal maneja automáticamente la elevación de privilegios. Si aparece un error de permisos:

```bash
# Verificar sudo
sudo -v

# Agregar usuario a sudo (como root)
usermod -aG sudo $USER
```

### Errores Comunes

**Módulos faltantes:**
```bash
poetry install
```

**Herramientas no encontradas:**
- Instalar herramientas según tu sistema operativo
- Configurar rutas en `~/.aegis/config.yaml`

**Problemas con logs:**
- Verificar permisos de escritura en directorio `logs/`
- Revisar archivo de log para detalles

## Desarrollo

### Verificación de Código
```bash
poetry run flake8 aegis_pentest/
poetry run black aegis_pentest/
poetry run mypy aegis_pentest/
```

## Licencia

MIT License

---

**Uso Legal**: Solo para sistemas propios o con autorización explícita.

**Nota de Seguridad**: Aegis solicita privilegios de administrador para funcionalidad completa. Verifica el código antes de ejecutar con sudo.