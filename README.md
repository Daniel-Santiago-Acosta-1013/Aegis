# 🛡️ Aegis Pentest Automation

CLI interactiva para automatización de pentesting web. Wrapper de herramientas de seguridad con interfaz moderna.

## 🎯 Características

- **CLI Interactiva**: Menús intuitivos con Rich
- **4 Tipos de Escaneo**: Rápido, completo, vulnerabilidades, sigiloso
- **Herramientas Integradas**: Nmap, Nuclei, Gobuster, Nikto, SQLMap
- **Visualización Rica**: Tablas, progress bars, colores semánticos
- **Configuración YAML**: Sistema de configuración flexible

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