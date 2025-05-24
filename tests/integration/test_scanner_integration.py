"""
Tests de integración para el sistema de escaneo completo
"""

import pytest
from unittest.mock import patch
from pathlib import Path

from aegis_pentest.core.scanner import Scanner
from aegis_pentest.core.project_manager import ProjectManager
from aegis_pentest.core.report_generator import ReportGenerator


@pytest.mark.integration
class TestScannerIntegration:
    """Tests de integración para el Scanner principal"""
    
    def test_full_scan_workflow(self, mock_config, temp_dir, sample_target, mock_subprocess):
        """Test del flujo completo de escaneo"""
        # Configurar project manager
        project_manager = ProjectManager(str(temp_dir), mock_config)
        project_manager.create_project("test_project")
        
        # Configurar scanner
        scanner = Scanner(mock_config, project_manager)
        
        # Ejecutar escaneo completo
        results = scanner.run_full_scan(sample_target)
        
        assert 'nmap' in results
        assert 'ssl_analysis' in results
        assert 'web_scan' in results
        assert results['status'] == 'completed'
    
    @pytest.mark.asyncio
    async def test_async_scan_workflow(self, mock_config, temp_dir, sample_target):
        """Test del flujo de escaneo asíncrono"""
        project_manager = ProjectManager(str(temp_dir), mock_config)
        project_manager.create_project("async_test")
        
        scanner = Scanner(mock_config, project_manager)
        
        # Mock de herramientas asíncronas
        with patch.object(scanner, '_run_nmap_async') as mock_nmap, \
             patch.object(scanner, '_run_web_scan_async') as mock_web:
            
            mock_nmap.return_value = {'success': True, 'ports': [80, 443]}
            mock_web.return_value = {'success': True, 'vulnerabilities': []}
            
            results = await scanner.run_async_scan(sample_target)
            
            assert results['success'] is True
            mock_nmap.assert_called_once()
            mock_web.assert_called_once()
    
    def test_scan_with_project_persistence(self, mock_config, temp_dir, sample_target, mock_subprocess):
        """Test de escaneo con persistencia de proyecto"""
        project_manager = ProjectManager(str(temp_dir), mock_config)
        project_name = "persistence_test"
        project_manager.create_project(project_name)
        
        scanner = Scanner(mock_config, project_manager)
        
        # Ejecutar escaneo
        results = scanner.run_full_scan(sample_target)
        
        # Verificar que los resultados se guardaron
        project_dir = temp_dir / project_name
        assert project_dir.exists()
        
        # Verificar archivos de resultados
        results_files = list(project_dir.glob("*.json"))
        assert len(results_files) > 0
    
    def test_scan_error_handling(self, mock_config, temp_dir, mock_subprocess):
        """Test de manejo de errores durante el escaneo"""
        project_manager = ProjectManager(str(temp_dir), mock_config)
        project_manager.create_project("error_test")
        
        scanner = Scanner(mock_config, project_manager)
        
        # Simular error en herramienta
        mock_subprocess.return_value.returncode = 1
        mock_subprocess.return_value.stderr = "Connection refused"
        
        invalid_target = {'url': 'https://nonexistent.local', 'ip': '192.168.1.999'}
        results = scanner.run_full_scan(invalid_target)
        
        assert results['status'] == 'completed_with_errors'
        assert any('error' in tool_result for tool_result in results.values() if isinstance(tool_result, dict))
    
    def test_scan_timeout_handling(self, mock_config, temp_dir, sample_target):
        """Test de manejo de timeouts en escaneo"""
        project_manager = ProjectManager(str(temp_dir), mock_config)
        project_manager.create_project("timeout_test")
        
        scanner = Scanner(mock_config, project_manager)
        
        # Configurar timeout muy bajo
        scanner.timeout = 1
        
        with patch('subprocess.run') as mock_run:
            import subprocess
            mock_run.side_effect = subprocess.TimeoutExpired("nmap", 1)
            
            results = scanner.run_full_scan(sample_target)
            
            # Verificar que el timeout se manejó correctamente
            assert results['status'] in ['completed_with_errors', 'timeout']


@pytest.mark.integration
class TestReportIntegration:
    """Tests de integración para generación de reportes"""
    
    def test_report_generation_from_scan(self, mock_config, temp_dir, sample_target, mock_subprocess):
        """Test de generación de reporte a partir de resultados de escaneo"""
        # Ejecutar escaneo
        project_manager = ProjectManager(str(temp_dir), mock_config)
        project_manager.create_project("report_test")
        
        scanner = Scanner(mock_config, project_manager)
        results = scanner.run_full_scan(sample_target)
        
        # Generar reporte
        report_generator = ReportGenerator(mock_config)
        report_path = report_generator.generate_report(results, str(temp_dir / "test_report.html"))
        
        assert Path(report_path).exists()
        assert Path(report_path).stat().st_size > 0
    
    def test_multiple_format_reports(self, mock_config, temp_dir, sample_target, mock_subprocess):
        """Test de generación de reportes en múltiples formatos"""
        project_manager = ProjectManager(str(temp_dir), mock_config)
        project_manager.create_project("multi_format_test")
        
        scanner = Scanner(mock_config, project_manager)
        results = scanner.run_full_scan(sample_target)
        
        report_generator = ReportGenerator(mock_config)
        
        # Generar reportes en diferentes formatos
        formats = ['html', 'json', 'pdf']
        generated_reports = []
        
        for fmt in formats:
            try:
                report_path = report_generator.generate_report(
                    results, 
                    str(temp_dir / f"test_report.{fmt}"),
                    format=fmt
                )
                if Path(report_path).exists():
                    generated_reports.append(fmt)
            except Exception as e:
                # PDF podría no estar disponible en el entorno de test
                if fmt != 'pdf':
                    raise e
        
        # Al menos HTML y JSON deberían generarse
        assert 'html' in generated_reports
        assert 'json' in generated_reports
    
    def test_report_with_custom_template(self, mock_config, temp_dir, sample_target, mock_subprocess):
        """Test de generación de reporte con template personalizado"""
        project_manager = ProjectManager(str(temp_dir), mock_config)
        project_manager.create_project("custom_template_test")
        
        scanner = Scanner(mock_config, project_manager)
        results = scanner.run_full_scan(sample_target)
        
        # Crear template personalizado
        custom_template = temp_dir / "custom_template.html"
        custom_template.write_text("""
        <!DOCTYPE html>
        <html>
        <head><title>Custom Report</title></head>
        <body>
            <h1>Custom Aegis Report</h1>
            <div>Target: {{ target.url }}</div>
            <div>Scan Results: {{ results | length }}</div>
        </body>
        </html>
        """)
        
        report_generator = ReportGenerator(mock_config)
        report_path = report_generator.generate_report(
            results,
            str(temp_dir / "custom_report.html"),
            template_path=str(custom_template)
        )
        
        assert Path(report_path).exists()
        
        # Verificar contenido personalizado
        content = Path(report_path).read_text()
        assert "Custom Aegis Report" in content


@pytest.mark.integration  
class TestProjectWorkflow:
    """Tests de integración para el flujo completo de proyecto"""
    
    def test_complete_project_lifecycle(self, mock_config, temp_dir, sample_target, mock_subprocess):
        """Test del ciclo de vida completo de un proyecto"""
        project_manager = ProjectManager(str(temp_dir), mock_config)
        project_name = "lifecycle_test"
        
        # 1. Crear proyecto
        project_path = project_manager.create_project(project_name)
        assert Path(project_path).exists()
        
        # 2. Ejecutar escaneo
        scanner = Scanner(mock_config, project_manager)
        results = scanner.run_full_scan(sample_target)
        
        # 3. Guardar resultados
        project_manager.save_scan_results(project_name, results)
        
        # 4. Generar reporte
        report_generator = ReportGenerator(mock_config)
        report_path = project_manager.get_project_path(project_name) / "report.html"
        report_generator.generate_report(results, str(report_path))
        
        # 5. Verificar estructura final del proyecto
        project_dir = Path(project_path)
        assert (project_dir / "scan_results.json").exists()
        assert (project_dir / "report.html").exists()
        assert (project_dir / "project_info.yaml").exists()
        
        # 6. Cargar proyecto existente
        loaded_results = project_manager.load_scan_results(project_name)
        assert loaded_results is not None
        assert loaded_results['status'] == results['status']
    
    def test_project_backup_and_restore(self, mock_config, temp_dir, sample_target, mock_subprocess):
        """Test de backup y restauración de proyectos"""
        project_manager = ProjectManager(str(temp_dir), mock_config)
        original_project = "backup_test"
        
        # Crear y ejecutar proyecto original
        project_manager.create_project(original_project)
        scanner = Scanner(mock_config, project_manager)
        results = scanner.run_full_scan(sample_target)
        project_manager.save_scan_results(original_project, results)
        
        # Crear backup
        backup_path = temp_dir / "backup.tar.gz"
        project_manager.backup_project(original_project, str(backup_path))
        assert backup_path.exists()
        
        # Eliminar proyecto original
        project_manager.delete_project(original_project)
        assert not project_manager.project_exists(original_project)
        
        # Restaurar desde backup
        restored_project = "restored_test"
        project_manager.restore_project(str(backup_path), restored_project)
        
        # Verificar restauración
        assert project_manager.project_exists(restored_project)
        restored_results = project_manager.load_scan_results(restored_project)
        assert restored_results['status'] == results['status']
    
    def test_concurrent_scans(self, mock_config, temp_dir, sample_target, mock_subprocess):
        """Test de múltiples escaneos concurrentes"""
        project_manager = ProjectManager(str(temp_dir), mock_config)
        
        # Crear múltiples proyectos
        projects = ["concurrent_1", "concurrent_2", "concurrent_3"]
        scanners = []
        
        for project_name in projects:
            project_manager.create_project(project_name)
            scanner = Scanner(mock_config, project_manager)
            scanners.append((project_name, scanner))
        
        # Ejecutar escaneos concurrentes (simulado)
        results = {}
        for project_name, scanner in scanners:
            # En un entorno real, esto sería con threading/asyncio
            scan_results = scanner.run_full_scan(sample_target)
            project_manager.save_scan_results(project_name, scan_results)
            results[project_name] = scan_results
        
        # Verificar que todos los proyectos completaron correctamente
        for project_name in projects:
            assert project_manager.project_exists(project_name)
            loaded_results = project_manager.load_scan_results(project_name)
            assert loaded_results is not None
            assert loaded_results['status'] in ['completed', 'completed_with_errors'] 