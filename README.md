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

## 🧪 Testing

Aegis incluye una suite completa de tests automatizados para garantizar la calidad y funcionalidad del código.

### Estructura de Tests

```
tests/
├── unit/                    # Tests unitarios individuales
│   ├── test_config.py      # Tests del sistema de configuración
│   └── test_tools.py       # Tests de wrappers de herramientas
├── integration/            # Tests de integración entre componentes
│   └── test_scanner_integration.py
├── performance/            # Tests de rendimiento y carga
│   └── test_performance.py
├── e2e/                    # Tests end-to-end completos
│   └── test_cli_workflows.py
├── installation/           # Tests del proceso de instalación
│   └── test_installation.py
└── scripts/
    └── run_tests.py        # Script para ejecutar tests
```

### 🚀 Ejecutar Todos los Tests

Para ejecutar toda la suite de tests de Aegis, utiliza el siguiente comando único:

```bash
poetry run test
```

Este comando ejecuta:
- ✅ **Todos los tests** (unitarios, integración, rendimiento, e2e, instalación)
- 📊 **Reporte de cobertura** en HTML y terminal
- 📋 **Reporte JUnit XML** para CI/CD
- 🎯 **Todos los tipos de verificación** automáticamente

### Tipos de Tests Incluidos

| Tipo | Descripción | Ubicación |
|------|-------------|-----------|
| **Unit** | Tests individuales de componentes | `tests/unit/` |
| **Integration** | Tests de interacción entre componentes | `tests/integration/` |
| **Performance** | Tests de rendimiento y memoria | `tests/performance/` |
| **E2E** | Tests completos de flujos de usuario | `tests/e2e/` |
| **Installation** | Tests del proceso de instalación | `tests/installation/` |

### Salida del Comando

Al ejecutar `poetry run test`, obtienes:

```bash
$ poetry run test
============== test session starts ==============
collected 50+ items

tests/unit/test_config.py ............     [ 20%]
tests/unit/test_tools.py ..............    [ 40%]
tests/integration/ .....................  [ 60%]
tests/performance/ ....................   [ 80%]
tests/e2e/ ............................   [ 90%]
tests/installation/ ..................    [100%]

---------- coverage: platform darwin -----------
aegis_pentest/config.py      95%   5 missing
aegis_pentest/scanner.py     88%   12 missing
aegis_pentest/tools/         92%   8 missing
Total coverage: 90%

=============== 50 passed in 45.2s ===============
```

### Reportes Generados

Después de ejecutar los tests, encontrarás:

- **Cobertura HTML**: `tests/coverage_html/index.html`
- **Cobertura XML**: `tests/coverage.xml` 
- **Resultados JUnit**: `tests/test_results.xml`

### Tests de Rendimiento

Los tests de performance verifican:
- **Uso de memoria** durante escaneos (< 100 MB)
- **Tiempo de ejecución** de operaciones (< 10 segundos para mocks)
- **Concurrencia** de múltiples escaneos
- **Detección de memory leaks**
- **Escalabilidad** con múltiples proyectos

### Tests en CI/CD

Los tests están diseñados para:
- **Ejecución automática** en pipelines de CI/CD
- **Paralelización** para mayor velocidad (usando pytest-xdist)
- **Mocking** de herramientas externas (no requiere instalación de nmap, etc.)
- **Tests de regresión** para detectar bugs en nuevas features

### Configuración Avanzada

Si necesitas ejecutar tests específicos manualmente:

```bash
# Solo tests unitarios
python -m pytest tests/unit/ -v

# Solo tests rápidos (sin performance)
python -m pytest tests/ -v -m "not slow"

# Tests específicos
python -m pytest tests/unit/test_config.py::TestConfig::test_config_initialization -v

# Tests con output detallado
python -m pytest tests/ -v -s --tb=long
```

### Benchmarks Esperados

| Métrica | Valor Esperado |
|---------|----------------|
| Suite completa | < 60 segundos |
| Tests unitarios | < 10 segundos |
| Tests integración | < 20 segundos |
| Tests performance | < 30 segundos |
| Cobertura mínima | > 85% |

## 📋 Menú Principal

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

| Tipo | Duración | Descripción |
|------|----------|-------------|
| **Rápido** | 5-15 min | Puertos comunes (1-1000) |
| **Completo** | 30-60 min | Todos los puertos + servicios |
| **Vulnerabilidades** | 20-45 min | CVEs con Nuclei + SQLMap |
| **Sigiloso** | 10-30 min | Técnicas de evasión |

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

**Tests fallan:**
```bash
# Instalar dependencias de test
poetry install --with test

# Ejecutar tests
poetry run test
```

**Herramientas no encontradas:**
- Verificar instalación con opción 6 en el menú
- Configurar rutas en `~/.aegis/config.yaml`

**Permisos:**
```bash
chmod +x aegis_cli.py
```

## 🔍 Desarrollo y Contribución

### Ejecutar Tests Durante Desarrollo

```bash
# Ejecutar toda la suite de tests
poetry run test

# Tests específicos durante desarrollo
python -m pytest tests/unit/test_config.py -v

# Tests con auto-reload (requiere pytest-watch)
ptw tests/unit/ --runner "python -m pytest"
```

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