"""
Tests de instalación y configuración inicial
"""

import pytest
import shutil
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

from aegis_pentest.test_installer import test_dependencies


class TestInstallation:
    """Tests para el proceso de instalación"""
    
    def test_python_version_compatibility(self):
        """Test de compatibilidad con la versión de Python"""
        # Verificar que estamos usando Python 3.9+
        assert sys.version_info >= (3, 9), "Python 3.9+ is required"
        
        # Verificar funcionalidades específicas disponibles
        import asyncio
        import pathlib
        import dataclasses
        
        # Estas deberían estar disponibles en Python 3.9+
        assert hasattr(asyncio, 'gather')
        assert hasattr(pathlib.Path, 'exists')
        assert hasattr(dataclasses, 'dataclass')
    
    def test_required_dependencies_import(self):
        """Test de importación de dependencias requeridas"""
        required_packages = [
            'yaml',      # pyyaml
            'requests',  # requests
            'rich',      # rich
            'inquirer',  # inquirer
            'tabulate',  # tabulate
            'prompt_toolkit',  # prompt-toolkit
            'bs4',       # beautifulsoup4
            'colorama',  # colorama
            'docx',      # python-docx
            'jinja2',    # jinja2
            'aiohttp',   # aiohttp
        ]
        
        missing_packages = []
        for package in required_packages:
            try:
                __import__(package)
            except ImportError:
                missing_packages.append(package)
        
        assert len(missing_packages) == 0, f"Missing required packages: {missing_packages}"
    
    def test_optional_dependencies_import(self):
        """Test de importación de dependencias opcionales"""
        optional_packages = [
            'pytest',    # testing
            'black',     # code formatting
            'flake8',    # linting
            'mypy',      # type checking
        ]
        
        available_optional = []
        for package in optional_packages:
            try:
                __import__(package)
                available_optional.append(package)
            except ImportError:
                pass
        
        # Al menos pytest debería estar disponible en el entorno de test
        assert 'pytest' in available_optional, "pytest should be available for testing"
    
    def test_tool_availability_check(self):
        """Test de verificación de disponibilidad de herramientas externas"""
        tools_to_check = [
            'nmap',
            'nikto', 
            'gobuster',
            'sqlmap',
            'nuclei'
        ]
        
        available_tools = []
        missing_tools = []
        
        for tool in tools_to_check:
            if shutil.which(tool):
                available_tools.append(tool)
            else:
                missing_tools.append(tool)
        
        # En el entorno de test, es normal que las herramientas no estén instaladas
        # Solo verificamos que el check funciona
        assert isinstance(available_tools, list)
        assert isinstance(missing_tools, list)
        assert len(available_tools) + len(missing_tools) == len(tools_to_check)
    
    @patch('subprocess.run')
    def test_tool_version_check(self, mock_run):
        """Test de verificación de versiones de herramientas"""
        # Mock de respuestas de versión
        version_outputs = {
            'nmap': 'Nmap version 7.94',
            'nikto': 'Nikto 2.5.0',
            'gobuster': 'Version: 3.6',
            'sqlmap': 'sqlmap/1.7.2',
            'nuclei': 'Nuclei 2.9.15'
        }
        
        def mock_version_check(cmd, **kwargs):
            tool = cmd[0]
            if tool in version_outputs:
                result = MagicMock()
                result.returncode = 0
                result.stdout = version_outputs[tool]
                result.stderr = ""
                return result
            else:
                result = MagicMock()
                result.returncode = 1
                result.stdout = ""
                result.stderr = "command not found"
                return result
        
        mock_run.side_effect = mock_version_check
        
        # Test del verificador de dependencias
        result = test_dependencies()
        
        # Verificar que el test detecta las herramientas "instaladas"
        assert isinstance(result, dict)
        assert 'tools' in result
        
        # Verificar que el check de versión funciona
        for tool in version_outputs.keys():
            mock_run.assert_any_call([tool, '--version'], 
                                   capture_output=True, 
                                   text=True, 
                                   timeout=10)
    
    def test_config_file_creation(self, temp_dir):
        """Test de creación de archivo de configuración"""
        from aegis_pentest.utils.config import Config
        
        # Crear configuración en directorio temporal
        config_file = temp_dir / 'test_config.yaml'
        
        # Simular configuración inicial
        initial_config = {
            'tools': {
                'nmap': {'path': '/usr/bin/nmap', 'timeout': 300},
                'nikto': {'path': '/usr/bin/nikto', 'timeout': 600}
            },
            'output': {
                'base_dir': str(temp_dir / 'output'),
                'format': 'json'
            },
            'logging': {
                'level': 'INFO',
                'file': str(temp_dir / 'aegis.log')
            }
        }
        
        # Escribir configuración
        import yaml
        with open(config_file, 'w') as f:
            yaml.dump(initial_config, f)
        
        # Verificar que se puede cargar
        with patch.object(Config, '_config_file', str(config_file)):
            config = Config()
            assert config.get('tools.nmap.path') == '/usr/bin/nmap'
            assert config.get('output.format') == 'json'
    
    def test_directory_structure_creation(self, temp_dir):
        """Test de creación de estructura de directorios"""
        from aegis_pentest.core.project_manager import ProjectManager
        from aegis_pentest.utils.config import Config
        
        # Configurar config mock
        config = Config()
        
        # Crear project manager
        pm = ProjectManager(str(temp_dir), config)
        
        # Crear proyecto de prueba
        project_path = pm.create_project("installation_test")
        
        # Verificar estructura de directorios
        project_dir = Path(project_path)
        assert project_dir.exists()
        assert project_dir.is_dir()
        
        # Verificar archivos de proyecto
        expected_files = ['project_info.yaml']
        for file_name in expected_files:
            assert (project_dir / file_name).exists()
    
    def test_permissions_and_access(self, temp_dir):
        """Test de permisos y acceso a archivos"""
        # Crear archivo de test
        test_file = temp_dir / 'permission_test.txt'
        test_file.write_text('test content')
        
        # Verificar permisos de lectura
        assert test_file.exists()
        assert test_file.is_file()
        assert test_file.stat().st_size > 0
        
        # Verificar que se puede leer
        content = test_file.read_text()
        assert content == 'test content'
        
        # Verificar que se puede escribir
        test_file.write_text('modified content')
        modified_content = test_file.read_text()
        assert modified_content == 'modified content'
    
    def test_logging_configuration(self, temp_dir):
        """Test de configuración del sistema de logging"""
        import logging
        from aegis_pentest.main import setup_logging
        
        # Configurar logging temporal
        log_file = temp_dir / 'test.log'
        
        with patch('aegis_pentest.utils.config.Config') as mock_config_class:
            mock_config = MagicMock()
            mock_config.get.side_effect = lambda key, default=None: {
                'logging.level': 'DEBUG',
                'logging.file': str(log_file)
            }.get(key, default)
            mock_config_class.return_value = mock_config
            
            # Configurar logging
            setup_logging()
            
            # Probar logging
            logger = logging.getLogger('test_logger')
            logger.info('Test log message')
            
            # Verificar que el archivo de log se creó
            assert log_file.exists()
    
    def test_cli_entry_point(self):
        """Test del punto de entrada de la CLI"""
        from aegis_pentest.main import main
        
        # Mock para evitar ejecución real de CLI
        with patch('aegis_pentest.main.main_cli') as mock_main_cli:
            mock_main_cli.return_value = None
            
            # Verificar que el punto de entrada existe y es callable
            assert callable(main)
            
            # Simular llamada (no debería fallar)
            try:
                main()
            except SystemExit:
                # Es normal que la CLI termine con SystemExit
                pass
    
    def test_package_integrity(self):
        """Test de integridad del paquete"""
        # Verificar que los módulos principales se pueden importar
        try:
            import aegis_pentest
            import aegis_pentest.core
            import aegis_pentest.tools
            import aegis_pentest.utils
            import aegis_pentest.cli
        except ImportError as e:
            pytest.fail(f"Failed to import main package modules: {e}")
        
        # Verificar que el paquete tiene los atributos esperados
        assert hasattr(aegis_pentest, '__version__') or hasattr(aegis_pentest, '__init__')
    
    def test_configuration_validation(self, mock_config):
        """Test de validación de configuración"""
        # Verificar configuración de herramientas
        required_tools = ['nmap', 'nikto', 'gobuster', 'sqlmap', 'nuclei']
        
        for tool in required_tools:
            path = mock_config.get(f'tools.{tool}.path')
            timeout = mock_config.get(f'tools.{tool}.timeout')
            
            assert path is not None, f"Tool {tool} path not configured"
            assert timeout is not None, f"Tool {tool} timeout not configured"
            assert isinstance(timeout, int), f"Tool {tool} timeout should be integer"
            assert timeout > 0, f"Tool {tool} timeout should be positive"
    
    def test_dependency_installation_check(self):
        """Test de verificación de instalación de dependencias"""
        # Este test verifica que las dependencias se instalaron correctamente
        # ejecutando algunos imports y verificaciones básicas
        
        dependency_tests = [
            # (package, test_function)
            ('yaml', lambda: __import__('yaml').dump({'test': 'data'})),
            ('requests', lambda: hasattr(__import__('requests'), 'get')),
            ('rich', lambda: hasattr(__import__('rich'), 'print')),
            ('aiohttp', lambda: hasattr(__import__('aiohttp'), 'ClientSession')),
        ]
        
        for package, test_func in dependency_tests:
            try:
                test_func()
            except Exception as e:
                pytest.fail(f"Dependency {package} not working correctly: {e}")
    
    @patch('shutil.which')
    def test_installation_script_simulation(self, mock_which):
        """Test de simulación del script de instalación"""
        # Simular herramientas disponibles
        available_tools = ['nmap', 'nikto']
        missing_tools = ['gobuster', 'sqlmap', 'nuclei']
        
        def mock_tool_check(tool):
            return f'/usr/bin/{tool}' if tool in available_tools else None
        
        mock_which.side_effect = mock_tool_check
        
        # Ejecutar verificación de dependencias
        result = test_dependencies()
        
        # Verificar resultado
        assert isinstance(result, dict)
        assert 'python_version' in result
        assert 'packages' in result
        assert 'tools' in result
        
        # Verificar detección de herramientas
        for tool in available_tools:
            assert result['tools'][tool]['available'] is True
        
        for tool in missing_tools:
            assert result['tools'][tool]['available'] is False 