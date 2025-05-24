"""
Configuración global de pytest para Aegis tests

Contiene fixtures y configuraciones compartidas por todos los tests.
"""

import pytest
import asyncio
import tempfile
import shutil
from pathlib import Path
from unittest.mock import MagicMock, patch
import yaml
import sys
import os

# Agregar el directorio raíz del proyecto al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from aegis_pentest.utils.config import Config
from aegis_pentest.core.project_manager import ProjectManager


@pytest.fixture(scope="session")
def event_loop():
    """Fixture para manejar el event loop asyncio en pytest."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def temp_dir():
    """Fixture que proporciona un directorio temporal para tests."""
    temp_path = tempfile.mkdtemp()
    yield Path(temp_path)
    shutil.rmtree(temp_path)


@pytest.fixture
def mock_config(temp_dir):
    """Fixture que proporciona una configuración mock para tests."""
    config_data = {
        'output': {
            'base_dir': str(temp_dir / 'output'),
            'format': 'json'
        },
        'tools': {
            'nmap': {
                'path': '/usr/bin/nmap',
                'timeout': 300
            },
            'nikto': {
                'path': '/usr/bin/nikto',
                'timeout': 600
            },
            'gobuster': {
                'path': '/usr/bin/gobuster',
                'timeout': 300
            },
            'sqlmap': {
                'path': '/usr/bin/sqlmap',
                'timeout': 600
            },
            'nuclei': {
                'path': '/usr/bin/nuclei',
                'timeout': 300
            }
        },
        'logging': {
            'level': 'DEBUG',
            'file': str(temp_dir / 'test.log')
        }
    }
    
    # Crear archivo de configuración temporal
    config_file = temp_dir / 'config.yaml'
    with open(config_file, 'w') as f:
        yaml.dump(config_data, f)
    
    with patch.object(Config, '_config_file', str(config_file)):
        yield Config()


@pytest.fixture
def mock_project_manager(temp_dir, mock_config):
    """Fixture que proporciona un ProjectManager configurado para tests."""
    return ProjectManager(str(temp_dir), mock_config)


@pytest.fixture
def sample_target():
    """Fixture que proporciona un target de ejemplo para tests."""
    return {
        'url': 'https://example.com',
        'ip': '93.184.216.34',
        'domain': 'example.com',
        'ports': [80, 443]
    }


@pytest.fixture
def mock_tool_output():
    """Fixture que simula output de herramientas de pentesting."""
    return {
        'nmap': {
            'exit_code': 0,
            'stdout': '''
                Starting Nmap 7.94
                Nmap scan report for example.com (93.184.216.34)
                Host is up (0.050s latency).
                PORT    STATE SERVICE
                80/tcp  open  http
                443/tcp open  https
            ''',
            'stderr': ''
        },
        'nikto': {
            'exit_code': 0,
            'stdout': '''
                + Target IP:          93.184.216.34
                + Target Hostname:    example.com
                + Target Port:        80
                + Server: ECS (sec/96EC)
            ''',
            'stderr': ''
        }
    }


@pytest.fixture(autouse=True)
def cleanup_env():
    """Fixture que limpia el entorno después de cada test."""
    yield
    # Cleanup después de cada test
    import logging
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)


@pytest.fixture
def mock_subprocess():
    """Fixture que mockea subprocess para evitar ejecutar herramientas reales."""
    with patch('subprocess.run') as mock_run:
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "Mocked output"
        mock_run.return_value.stderr = ""
        yield mock_run


# Configuración de pytest
def pytest_configure(config):
    """Configuración personalizada de pytest."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "performance: marks tests as performance tests"
    )
    config.addinivalue_line(
        "markers", "e2e: marks tests as end-to-end tests"
    )


def pytest_collection_modifyitems(config, items):
    """Modifica la colección de tests para agregar markers automáticamente."""
    for item in items:
        # Agregar marker 'slow' a tests que contengan 'slow' en el nombre
        if "slow" in item.nodeid:
            item.add_marker(pytest.mark.slow)
        
        # Agregar markers basados en la ubicación del archivo
        if "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        elif "performance" in str(item.fspath):
            item.add_marker(pytest.mark.performance)
        elif "e2e" in str(item.fspath):
            item.add_marker(pytest.mark.e2e) 