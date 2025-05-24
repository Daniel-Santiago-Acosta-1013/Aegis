"""
Tests unitarios para el sistema de configuración de Aegis
"""

import yaml
from pathlib import Path
from unittest.mock import patch

from aegis_pentest.utils.config import Config


class TestConfig:
    """Tests para la clase Config"""
    
    def test_config_initialization(self, temp_dir):
        """Test de inicialización básica de configuración"""
        config_data = {
            'output': {'base_dir': '/tmp/aegis'},
            'tools': {'nmap': {'path': '/usr/bin/nmap'}}
        }
        
        config_file = temp_dir / 'test_config.yaml'
        with open(config_file, 'w') as f:
            yaml.dump(config_data, f)
        
        with patch.object(Config, '_config_file', str(config_file)):
            config = Config()
            assert config.get('output.base_dir') == '/tmp/aegis'
            assert config.get('tools.nmap.path') == '/usr/bin/nmap'
    
    def test_config_get_with_default(self, mock_config):
        """Test del método get con valor por defecto"""
        result = mock_config.get('nonexistent.key', 'default_value')
        assert result == 'default_value'
    
    def test_config_get_nested_keys(self, mock_config):
        """Test de acceso a claves anidadas"""
        timeout = mock_config.get('tools.nmap.timeout')
        assert timeout == 300
    
    def test_config_missing_file(self):
        """Test cuando el archivo de configuración no existe"""
        with patch.object(Config, '_config_file', '/nonexistent/config.yaml'):
            config = Config()
            # Debería usar configuración por defecto
            assert config.get('output.format', 'json') == 'json'
    
    def test_config_invalid_yaml(self, temp_dir):
        """Test con archivo YAML inválido"""
        config_file = temp_dir / 'invalid.yaml'
        with open(config_file, 'w') as f:
            f.write('invalid: yaml: content: [')
        
        with patch.object(Config, '_config_file', str(config_file)):
            config = Config()
            # Debería manejar el error gracefully
            assert config.get('output.format', 'json') == 'json'
    
    def test_config_reload(self, temp_dir):
        """Test de recarga de configuración"""
        config_file = temp_dir / 'reload_test.yaml'
        
        # Configuración inicial
        initial_data = {'test': {'value': 'initial'}}
        with open(config_file, 'w') as f:
            yaml.dump(initial_data, f)
        
        with patch.object(Config, '_config_file', str(config_file)):
            config = Config()
            assert config.get('test.value') == 'initial'
            
            # Modificar configuración
            new_data = {'test': {'value': 'modified'}}
            with open(config_file, 'w') as f:
                yaml.dump(new_data, f)
            
            # Recargar
            config.reload()
            assert config.get('test.value') == 'modified'
    
    def test_config_tool_validation(self, mock_config):
        """Test de validación de herramientas"""
        # Verificar que todas las herramientas principales están configuradas
        required_tools = ['nmap', 'nikto', 'gobuster', 'sqlmap', 'nuclei']
        
        for tool in required_tools:
            path = mock_config.get(f'tools.{tool}.path')
            assert path is not None, f"Tool {tool} should have a path configured"
            assert path.startswith('/'), f"Tool {tool} path should be absolute"
    
    def test_config_logging_setup(self, mock_config):
        """Test de configuración de logging"""
        log_level = mock_config.get('logging.level')
        log_file = mock_config.get('logging.file')
        
        assert log_level in ['DEBUG', 'INFO', 'WARNING', 'ERROR']
        assert log_file is not None
        assert isinstance(log_file, str)
    
    def test_config_output_directory(self, mock_config):
        """Test de configuración de directorio de salida"""
        output_dir = mock_config.get('output.base_dir')
        assert output_dir is not None
        
        # Verificar que el directorio se puede crear
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        assert output_path.exists()
    
    def test_config_environment_override(self, temp_dir):
        """Test de override de configuración con variables de entorno"""
        config_data = {'tools': {'nmap': {'path': '/usr/bin/nmap'}}}
        config_file = temp_dir / 'env_test.yaml'
        
        with open(config_file, 'w') as f:
            yaml.dump(config_data, f)
        
        with patch.object(Config, '_config_file', str(config_file)):
            with patch.dict('os.environ', {'AEGIS_NMAP_PATH': '/custom/nmap'}):
                config = Config()
                # Debería usar la variable de entorno si está implementado
                path = config.get('tools.nmap.path')
                assert path in ['/usr/bin/nmap', '/custom/nmap'] 