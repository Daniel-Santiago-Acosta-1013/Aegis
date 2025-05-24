"""
Tests unitarios para los wrappers de herramientas de pentesting
"""

import subprocess
from unittest.mock import patch, MagicMock

from aegis_pentest.tools.nmap_wrapper import NmapWrapper
from aegis_pentest.tools.nikto_wrapper import NiktoWrapper
from aegis_pentest.tools.gobuster_wrapper import GobusterWrapper
from aegis_pentest.tools.sqlmap_wrapper import SQLMapWrapper
from aegis_pentest.tools.nuclei_wrapper import NucleiWrapper
from aegis_pentest.tools.ssl_analyzer import SSLAnalyzer


class TestNmapWrapper:
    """Tests para NmapWrapper"""
    
    def test_nmap_initialization(self, mock_config):
        """Test de inicialización de NmapWrapper"""
        nmap = NmapWrapper(mock_config)
        assert nmap.config == mock_config
        assert nmap.tool_path == mock_config.get('tools.nmap.path')
    
    @patch('subprocess.run')
    def test_nmap_basic_scan(self, mock_run, mock_config, sample_target):
        """Test de escaneo básico con Nmap"""
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = """
            Starting Nmap 7.94
            Nmap scan report for example.com (93.184.216.34)
            Host is up (0.050s latency).
            PORT    STATE SERVICE
            80/tcp  open  http
            443/tcp open  https
        """
        mock_run.return_value.stderr = ""
        
        nmap = NmapWrapper(mock_config)
        result = nmap.run_scan(sample_target['ip'], ports="80,443")
        
        assert result['success'] is True
        assert result['exit_code'] == 0
        assert 'output' in result
        mock_run.assert_called_once()
    
    @patch('subprocess.run')
    def test_nmap_scan_failure(self, mock_run, mock_config):
        """Test de manejo de errores en escaneo Nmap"""
        mock_run.return_value.returncode = 1
        mock_run.return_value.stdout = ""
        mock_run.return_value.stderr = "Host seems down"
        
        nmap = NmapWrapper(mock_config)
        result = nmap.run_scan("192.168.1.1")
        
        assert result['success'] is False
        assert result['exit_code'] == 1
        assert result['error'] == "Host seems down"
    
    def test_nmap_command_building(self, mock_config):
        """Test de construcción de comandos Nmap"""
        nmap = NmapWrapper(mock_config)
        
        # Test comando básico
        cmd = nmap._build_command("192.168.1.1")
        assert "/usr/bin/nmap" in cmd
        assert "192.168.1.1" in cmd
        
        # Test con puertos específicos
        cmd = nmap._build_command("192.168.1.1", ports="80,443")
        assert "-p" in cmd
        assert "80,443" in cmd
    
    def test_nmap_timeout_handling(self, mock_config):
        """Test de manejo de timeout en Nmap"""
        nmap = NmapWrapper(mock_config)
        timeout = mock_config.get('tools.nmap.timeout', 300)
        
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = subprocess.TimeoutExpired("nmap", timeout)
            
            result = nmap.run_scan("192.168.1.1")
            assert result['success'] is False
            assert 'timeout' in result['error'].lower()


class TestNiktoWrapper:
    """Tests para NiktoWrapper"""
    
    def test_nikto_initialization(self, mock_config):
        """Test de inicialización de NiktoWrapper"""
        nikto = NiktoWrapper(mock_config)
        assert nikto.config == mock_config
        assert nikto.tool_path == mock_config.get('tools.nikto.path')
    
    @patch('subprocess.run')
    def test_nikto_scan(self, mock_run, mock_config, sample_target):
        """Test de escaneo web con Nikto"""
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = """
            + Target IP:          93.184.216.34
            + Target Hostname:    example.com
            + Target Port:        80
            + Server: ECS (sec/96EC)
            + The anti-clickjacking X-Frame-Options header is not present.
        """
        mock_run.return_value.stderr = ""
        
        nikto = NiktoWrapper(mock_config)
        result = nikto.run_scan(sample_target['url'])
        
        assert result['success'] is True
        assert result['exit_code'] == 0
        assert 'output' in result
        mock_run.assert_called_once()
    
    def test_nikto_command_building(self, mock_config):
        """Test de construcción de comandos Nikto"""
        nikto = NiktoWrapper(mock_config)
        
        cmd = nikto._build_command("https://example.com")
        assert "/usr/bin/nikto" in cmd
        assert "-h" in cmd
        assert "https://example.com" in cmd


class TestGobusterWrapper:
    """Tests para GobusterWrapper"""
    
    def test_gobuster_initialization(self, mock_config):
        """Test de inicialización de GobusterWrapper"""
        gobuster = GobusterWrapper(mock_config)
        assert gobuster.config == mock_config
        assert gobuster.tool_path == mock_config.get('tools.gobuster.path')
    
    @patch('subprocess.run')
    def test_gobuster_dir_scan(self, mock_run, mock_config, sample_target, temp_dir):
        """Test de escaneo de directorios con Gobuster"""
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = """
            /admin                (Status: 301) [Size: 194] [--> /admin/]
            /login                (Status: 200) [Size: 1234]
            /config               (Status: 403) [Size: 1045]
        """
        mock_run.return_value.stderr = ""
        
        # Crear wordlist temporal
        wordlist = temp_dir / "wordlist.txt"
        wordlist.write_text("admin\nlogin\nconfig\n")
        
        gobuster = GobusterWrapper(mock_config)
        result = gobuster.run_dir_scan(sample_target['url'], str(wordlist))
        
        assert result['success'] is True
        assert result['exit_code'] == 0
        assert 'output' in result
        mock_run.assert_called_once()
    
    def test_gobuster_command_building(self, mock_config, temp_dir):
        """Test de construcción de comandos Gobuster"""
        wordlist = temp_dir / "wordlist.txt"
        wordlist.write_text("test\n")
        
        gobuster = GobusterWrapper(mock_config)
        cmd = gobuster._build_dir_command("https://example.com", str(wordlist))
        
        assert "/usr/bin/gobuster" in cmd
        assert "dir" in cmd
        assert "-u" in cmd
        assert "https://example.com" in cmd
        assert "-w" in cmd
        assert str(wordlist) in cmd


class TestSQLMapWrapper:
    """Tests para SQLMapWrapper"""
    
    def test_sqlmap_initialization(self, mock_config):
        """Test de inicialización de SQLMapWrapper"""
        sqlmap = SQLMapWrapper(mock_config)
        assert sqlmap.config == mock_config
        assert sqlmap.tool_path == mock_config.get('tools.sqlmap.path')
    
    @patch('subprocess.run')
    def test_sqlmap_basic_scan(self, mock_run, mock_config):
        """Test de escaneo básico con SQLMap"""
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = """
            [INFO] testing connection to the target URL
            [INFO] checking if the target is protected by some kind of WAF/IPS
            [INFO] testing if the target URL content is stable
            [WARNING] target URL content is not stable
        """
        mock_run.return_value.stderr = ""
        
        sqlmap = SQLMapWrapper(mock_config)
        result = sqlmap.run_scan("https://example.com/page?id=1")
        
        assert result['success'] is True
        assert result['exit_code'] == 0
        assert 'output' in result
        mock_run.assert_called_once()
    
    def test_sqlmap_command_building(self, mock_config):
        """Test de construcción de comandos SQLMap"""
        sqlmap = SQLMapWrapper(mock_config)
        
        cmd = sqlmap._build_command("https://example.com/page?id=1")
        assert "/usr/bin/sqlmap" in cmd
        assert "-u" in cmd
        assert "https://example.com/page?id=1" in cmd
        assert "--batch" in cmd  # Para evitar interacción manual


class TestNucleiWrapper:
    """Tests para NucleiWrapper"""
    
    def test_nuclei_initialization(self, mock_config):
        """Test de inicialización de NucleiWrapper"""
        nuclei = NucleiWrapper(mock_config)
        assert nuclei.config == mock_config
        assert nuclei.tool_path == mock_config.get('tools.nuclei.path')
    
    @patch('subprocess.run')
    def test_nuclei_scan(self, mock_run, mock_config, sample_target):
        """Test de escaneo con Nuclei"""
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = """
            [ssl-dns-names] [dns] example.com
            [tech-detect] [http] example.com [nginx]
            [http-missing-security-headers] [http] example.com
        """
        mock_run.return_value.stderr = ""
        
        nuclei = NucleiWrapper(mock_config)
        result = nuclei.run_scan(sample_target['url'])
        
        assert result['success'] is True
        assert result['exit_code'] == 0
        assert 'output' in result
        mock_run.assert_called_once()
    
    def test_nuclei_command_building(self, mock_config):
        """Test de construcción de comandos Nuclei"""
        nuclei = NucleiWrapper(mock_config)
        
        cmd = nuclei._build_command("https://example.com")
        assert "/usr/bin/nuclei" in cmd
        assert "-target" in cmd
        assert "https://example.com" in cmd


class TestSSLAnalyzer:
    """Tests para SSLAnalyzer"""
    
    def test_ssl_analyzer_initialization(self, mock_config):
        """Test de inicialización de SSLAnalyzer"""
        ssl_analyzer = SSLAnalyzer(mock_config)
        assert ssl_analyzer.config == mock_config
    
    @patch('ssl.create_default_context')
    @patch('socket.create_connection')
    def test_ssl_certificate_analysis(self, mock_socket, mock_ssl_context, mock_config):
        """Test de análisis de certificado SSL"""
        # Mock del certificado SSL
        mock_cert = {
            'subject': ((('commonName', 'example.com'),),),
            'issuer': ((('organizationName', 'Test CA'),),),
            'notBefore': 'Jan  1 00:00:00 2024 GMT',
            'notAfter': 'Dec 31 23:59:59 2024 GMT',
            'serialNumber': '123456789',
            'version': 3
        }
        
        mock_ssl_socket = MagicMock()
        mock_ssl_socket.getpeercert.return_value = mock_cert
        mock_ssl_context.return_value.wrap_socket.return_value = mock_ssl_socket
        
        ssl_analyzer = SSLAnalyzer(mock_config)
        result = ssl_analyzer.analyze_certificate("example.com", 443)
        
        assert result['success'] is True
        assert 'certificate' in result
        assert result['certificate']['subject']['commonName'] == 'example.com'
    
    def test_ssl_analyzer_connection_error(self, mock_config):
        """Test de manejo de errores de conexión SSL"""
        ssl_analyzer = SSLAnalyzer(mock_config)
        
        with patch('socket.create_connection') as mock_socket:
            mock_socket.side_effect = ConnectionRefusedError("Connection refused")
            
            result = ssl_analyzer.analyze_certificate("nonexistent.local", 443)
            assert result['success'] is False
            assert 'error' in result
    
    def test_ssl_protocol_check(self, mock_config):
        """Test de verificación de protocolos SSL/TLS"""
        ssl_analyzer = SSLAnalyzer(mock_config)
        
        # Mock para diferentes versiones de TLS
        with patch.object(ssl_analyzer, '_check_tls_version') as mock_check:
            mock_check.return_value = {
                'tls_1_0': False,
                'tls_1_1': False,
                'tls_1_2': True,
                'tls_1_3': True
            }
            
            result = ssl_analyzer.check_protocols("example.com", 443)
            assert result['success'] is True
            assert result['protocols']['tls_1_2'] is True
            assert result['protocols']['tls_1_3'] is True 