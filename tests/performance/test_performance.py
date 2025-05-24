"""
Tests de rendimiento y carga para Aegis Pentest Automation
"""

import pytest
import time
import threading
import asyncio
import psutil
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from unittest.mock import patch

from aegis_pentest.core.scanner import Scanner
from aegis_pentest.core.project_manager import ProjectManager
from aegis_pentest.tools.nmap_wrapper import NmapWrapper


@pytest.mark.performance
class TestPerformance:
    """Tests de rendimiento del sistema"""
    
    def test_memory_usage_during_scan(self, mock_config, temp_dir, sample_target, mock_subprocess):
        """Test de uso de memoria durante escaneo"""
        # Obtener uso de memoria inicial
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        project_manager = ProjectManager(str(temp_dir), mock_config)
        project_manager.create_project("memory_test")
        
        scanner = Scanner(mock_config, project_manager)
        
        # Ejecutar escaneo y monitorear memoria
        memory_samples = []
        
        def monitor_memory():
            for _ in range(10):
                memory_samples.append(process.memory_info().rss / 1024 / 1024)
                time.sleep(0.1)
        
        # Iniciar monitoreo en hilo separado
        monitor_thread = threading.Thread(target=monitor_memory)
        monitor_thread.start()
        
        # Ejecutar escaneo
        results = scanner.run_full_scan(sample_target)
        
        monitor_thread.join()
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        max_memory = max(memory_samples)
        memory_increase = max_memory - initial_memory
        
        # Verificar que el aumento de memoria sea razonable (menos de 100MB)
        assert memory_increase < 100, f"Memory increase too high: {memory_increase:.2f}MB"
        assert results['status'] in ['completed', 'completed_with_errors']
    
    @pytest.mark.slow
    def test_scan_performance_benchmarks(self, mock_config, temp_dir, sample_target, mock_subprocess):
        """Test de benchmarks de rendimiento de escaneo"""
        project_manager = ProjectManager(str(temp_dir), mock_config)
        project_manager.create_project("benchmark_test")
        
        scanner = Scanner(mock_config, project_manager)
        
        # Medir tiempo de ejecución
        start_time = time.time()
        results = scanner.run_full_scan(sample_target)
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        # El escaneo mock debería completarse en menos de 10 segundos
        assert execution_time < 10, f"Scan took too long: {execution_time:.2f}s"
        assert results['status'] in ['completed', 'completed_with_errors']
        
        # Verificar que todos los componentes se ejecutaron
        expected_components = ['nmap', 'ssl_analysis', 'web_scan']
        for component in expected_components:
            assert component in results, f"Missing component: {component}"
    
    def test_concurrent_scans_performance(self, mock_config, temp_dir, sample_target, mock_subprocess):
        """Test de rendimiento con múltiples escaneos concurrentes"""
        project_manager = ProjectManager(str(temp_dir), mock_config)
        
        # Configurar múltiples proyectos
        num_concurrent = 5
        projects = [f"concurrent_perf_{i}" for i in range(num_concurrent)]
        
        for project in projects:
            project_manager.create_project(project)
        
        # Función para ejecutar escaneo individual
        def run_scan(project_name):
            scanner = Scanner(mock_config, project_manager)
            start_time = time.time()
            results = scanner.run_full_scan(sample_target)
            end_time = time.time()
            return {
                'project': project_name,
                'duration': end_time - start_time,
                'status': results['status']
            }
        
        # Ejecutar escaneos concurrentes
        start_total = time.time()
        
        with ThreadPoolExecutor(max_workers=num_concurrent) as executor:
            futures = [executor.submit(run_scan, project) for project in projects]
            results = [future.result() for future in as_completed(futures)]
        
        end_total = time.time()
        total_time = end_total - start_total
        
        # Verificar que todos completaron exitosamente
        assert len(results) == num_concurrent
        assert all(r['status'] in ['completed', 'completed_with_errors'] for r in results)
        
        # El tiempo total debería ser menor que la suma de tiempos individuales
        # (indicando paralelización efectiva)
        individual_times = sum(r['duration'] for r in results)
        assert total_time < individual_times, "No parallelization benefit detected"
        
        # Ningún escaneo individual debería tomar más de 15 segundos
        max_individual_time = max(r['duration'] for r in results)
        assert max_individual_time < 15, f"Individual scan too slow: {max_individual_time:.2f}s"
    
    @pytest.mark.asyncio
    async def test_async_performance(self, mock_config, temp_dir, sample_target):
        """Test de rendimiento de operaciones asíncronas"""
        project_manager = ProjectManager(str(temp_dir), mock_config)
        project_manager.create_project("async_perf_test")
        
        scanner = Scanner(mock_config, project_manager)
        
        # Mock de métodos asíncronos
        async def mock_async_scan(target):
            await asyncio.sleep(0.1)  # Simular trabajo asíncrono
            return {'success': True, 'duration': 0.1}
        
        with patch.object(scanner, '_run_nmap_async', side_effect=mock_async_scan), \
             patch.object(scanner, '_run_web_scan_async', side_effect=mock_async_scan), \
             patch.object(scanner, '_run_ssl_analysis_async', side_effect=mock_async_scan):
            
            start_time = time.time()
            
            # Ejecutar múltiples operaciones asíncronas
            tasks = [
                scanner._run_nmap_async(sample_target),
                scanner._run_web_scan_async(sample_target),
                scanner._run_ssl_analysis_async(sample_target)
            ]
            
            results = await asyncio.gather(*tasks)
            
            end_time = time.time()
            total_time = end_time - start_time
            
            # Debería tomar aproximadamente 0.1s (paralelo) no 0.3s (secuencial)
            assert total_time < 0.2, f"Async operations not parallel: {total_time:.3f}s"
            assert len(results) == 3
            assert all(r['success'] for r in results)
    
    def test_large_output_handling(self, mock_config, temp_dir, sample_target):
        """Test de manejo de outputs grandes"""
        project_manager = ProjectManager(str(temp_dir), mock_config)
        project_manager.create_project("large_output_test")
        
        # Simular output muy grande (1MB de texto)
        large_output = "Test line with scan results\n" * 50000  # ~1MB
        
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = large_output
            mock_run.return_value.stderr = ""
            
            scanner = Scanner(mock_config, project_manager)
            
            start_time = time.time()
            results = scanner.run_full_scan(sample_target)
            end_time = time.time()
            
            processing_time = end_time - start_time
            
            # Debería procesar output grande en tiempo razonable
            assert processing_time < 30, f"Large output processing too slow: {processing_time:.2f}s"
            assert results['status'] in ['completed', 'completed_with_errors']
    
    def test_project_scaling(self, mock_config, temp_dir, mock_subprocess):
        """Test de escalabilidad con muchos proyectos"""
        project_manager = ProjectManager(str(temp_dir), mock_config)
        
        # Crear muchos proyectos
        num_projects = 50
        project_names = [f"scale_test_{i}" for i in range(num_projects)]
        
        start_time = time.time()
        
        # Crear proyectos
        for project_name in project_names:
            project_manager.create_project(project_name)
        
        # Listar proyectos
        project_list = project_manager.list_projects()
        
        # Verificar existencia de algunos proyectos
        sample_projects = project_names[::10]  # Cada 10mo proyecto
        for project_name in sample_projects:
            assert project_manager.project_exists(project_name)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Las operaciones de proyecto deberían ser rápidas
        assert total_time < 10, f"Project operations too slow: {total_time:.2f}s"
        assert len(project_list) >= num_projects


@pytest.mark.performance
class TestStressTests:
    """Tests de estrés del sistema"""
    
    def test_rapid_scan_requests(self, mock_config, temp_dir, sample_target, mock_subprocess):
        """Test de múltiples solicitudes de escaneo rápidas"""
        project_manager = ProjectManager(str(temp_dir), mock_config)
        
        # Configurar mock para respuesta rápida
        mock_subprocess.return_value.returncode = 0
        mock_subprocess.return_value.stdout = "Quick scan result"
        mock_subprocess.return_value.stderr = ""
        
        num_requests = 20
        results = []
        
        start_time = time.time()
        
        for i in range(num_requests):
            project_name = f"rapid_test_{i}"
            project_manager.create_project(project_name)
            scanner = Scanner(mock_config, project_manager)
            result = scanner.run_full_scan(sample_target)
            results.append(result)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Verificar que todas las solicitudes completaron
        assert len(results) == num_requests
        assert all(r['status'] in ['completed', 'completed_with_errors'] for r in results)
        
        # Tiempo promedio por solicitud debería ser razonable
        avg_time = total_time / num_requests
        assert avg_time < 2, f"Average request time too high: {avg_time:.2f}s"
    
    def test_memory_leak_detection(self, mock_config, temp_dir, sample_target, mock_subprocess):
        """Test de detección de fugas de memoria"""
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        project_manager = ProjectManager(str(temp_dir), mock_config)
        
        # Ejecutar múltiples ciclos de escaneo
        for i in range(10):
            project_name = f"leak_test_{i}"
            project_manager.create_project(project_name)
            scanner = Scanner(mock_config, project_manager)
            
            # Ejecutar escaneo
            results = scanner.run_full_scan(sample_target)
            
            # Limpiar explícitamente
            del scanner
            del results
            
            # Forzar garbage collection
            import gc
            gc.collect()
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # El aumento de memoria debería ser mínimo después de múltiples ciclos
        assert memory_increase < 50, f"Potential memory leak detected: {memory_increase:.2f}MB increase"
    
    @pytest.mark.slow
    def test_long_running_stability(self, mock_config, temp_dir, sample_target, mock_subprocess):
        """Test de estabilidad en ejecución prolongada"""
        project_manager = ProjectManager(str(temp_dir), mock_config)
        
        # Simular ejecución prolongada con múltiples operaciones
        duration_minutes = 1  # 1 minuto para el test
        end_time = time.time() + (duration_minutes * 60)
        
        operation_count = 0
        errors = []
        
        while time.time() < end_time:
            try:
                project_name = f"stability_test_{operation_count}"
                project_manager.create_project(project_name)
                scanner = Scanner(mock_config, project_manager)
                
                # Alternar entre diferentes tipos de operaciones
                if operation_count % 3 == 0:
                    results = scanner.run_full_scan(sample_target)
                elif operation_count % 3 == 1:
                    # Operación de listado de proyectos
                    projects = project_manager.list_projects()
                else:
                    # Operación de verificación de configuración
                    config_valid = mock_config.get('tools.nmap.path') is not None
                    assert config_valid
                
                operation_count += 1
                
                # Pequeña pausa para evitar saturar el sistema
                time.sleep(0.1)
                
            except Exception as e:
                errors.append(f"Operation {operation_count}: {str(e)}")
        
        # Verificar que se ejecutaron suficientes operaciones sin errores críticos
        assert operation_count > 100, f"Too few operations completed: {operation_count}"
        assert len(errors) < operation_count * 0.05, f"Too many errors: {len(errors)}/{operation_count}"