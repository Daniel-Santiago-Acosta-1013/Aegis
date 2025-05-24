#!/usr/bin/env python3
"""
Script para ejecutar tests de Aegis con diferentes configuraciones

Este script permite ejecutar distintos tipos de tests:
- Tests unitarios rápidos
- Tests de integración
- Tests de rendimiento
- Tests end-to-end completos
- Verificación de instalación
"""

import sys
import argparse
import subprocess
import time
from pathlib import Path

def run_command(cmd, description):
    """Ejecuta un comando y muestra el resultado"""
    print(f"\n🔍 {description}")
    print(f"Command: {' '.join(cmd)}")
    print("-" * 60)
    
    start_time = time.time()
    result = subprocess.run(cmd, capture_output=False)
    end_time = time.time()
    
    duration = end_time - start_time
    
    if result.returncode == 0:
        print(f"✅ {description} completed successfully in {duration:.2f}s")
    else:
        print(f"❌ {description} failed in {duration:.2f}s")
    
    return result.returncode

def run_unit_tests():
    """Ejecuta tests unitarios"""
    cmd = [
        "python", "-m", "pytest", 
        "tests/unit/",
        "-v",
        "--tb=short"
    ]
    return run_command(cmd, "Unit Tests")

def run_integration_tests():
    """Ejecuta tests de integración"""
    cmd = [
        "python", "-m", "pytest",
        "tests/integration/",
        "-v",
        "--tb=short",
        "-m", "integration"
    ]
    return run_command(cmd, "Integration Tests")

def run_performance_tests():
    """Ejecuta tests de rendimiento"""
    cmd = [
        "python", "-m", "pytest",
        "tests/performance/",
        "-v",
        "--tb=short",
        "-m", "performance"
    ]
    return run_command(cmd, "Performance Tests")

def run_e2e_tests():
    """Ejecuta tests end-to-end"""
    cmd = [
        "python", "-m", "pytest",
        "tests/e2e/",
        "-v",
        "--tb=short",
        "-m", "e2e"
    ]
    return run_command(cmd, "End-to-End Tests")

def run_installation_tests():
    """Ejecuta tests de instalación"""
    cmd = [
        "python", "-m", "pytest",
        "tests/installation/",
        "-v",
        "--tb=short"
    ]
    return run_command(cmd, "Installation Tests")

def run_quick_tests():
    """Ejecuta tests rápidos (sin performance ni e2e)"""
    cmd = [
        "python", "-m", "pytest",
        "tests/unit/",
        "tests/installation/",
        "-v",
        "--tb=short",
        "-m", "not slow"
    ]
    return run_command(cmd, "Quick Tests (Unit + Installation)")

def run_all_tests():
    """Ejecuta todos los tests"""
    cmd = [
        "python", "-m", "pytest",
        "tests/",
        "-v",
        "--tb=short"
    ]
    return run_command(cmd, "All Tests")

def run_coverage_report():
    """Ejecuta tests con reporte de cobertura"""
    cmd = [
        "python", "-m", "pytest",
        "tests/",
        "--cov=aegis_pentest",
        "--cov-report=html:tests/coverage_html",
        "--cov-report=term-missing",
        "--cov-report=xml:tests/coverage.xml"
    ]
    return run_command(cmd, "Coverage Report")

def run_tests_with_output():
    """Ejecuta tests guardando output en archivos"""
    cmd = [
        "python", "-m", "pytest",
        "tests/",
        "-v",
        "--tb=short",
        "--junit-xml=tests/test_results.xml",
        "--html=tests/test_report.html",
        "--self-contained-html"
    ]
    return run_command(cmd, "Tests with Output Files")

def run_parallel_tests():
    """Ejecuta tests en paralelo (requiere pytest-xdist)"""
    try:
        import pytest_xdist
        cmd = [
            "python", "-m", "pytest",
            "tests/",
            "-v",
            "--tb=short",
            "-n", "auto"  # Usar todos los cores disponibles
        ]
        return run_command(cmd, "Parallel Tests")
    except ImportError:
        print("⚠️  pytest-xdist not installed. Running sequential tests instead.")
        return run_all_tests()

def run_specific_test(test_path):
    """Ejecuta un test específico"""
    cmd = [
        "python", "-m", "pytest",
        test_path,
        "-v",
        "--tb=long"
    ]
    return run_command(cmd, f"Specific Test: {test_path}")

def validate_environment():
    """Valida que el entorno esté configurado correctamente"""
    print("🔍 Validating test environment...")
    
    # Verificar pytest
    try:
        import pytest
        print(f"✅ pytest version: {pytest.__version__}")
    except ImportError:
        print("❌ pytest not installed")
        return False
    
    # Verificar que el paquete se puede importar
    try:
        import aegis_pentest
        print("✅ aegis_pentest package can be imported")
    except ImportError as e:
        print(f"❌ Cannot import aegis_pentest: {e}")
        return False
    
    # Verificar estructura de tests
    test_dirs = ['unit', 'integration', 'performance', 'e2e', 'installation']
    for test_dir in test_dirs:
        test_path = Path(f"tests/{test_dir}")
        if test_path.exists():
            print(f"✅ Test directory exists: {test_dir}")
        else:
            print(f"⚠️  Test directory missing: {test_dir}")
    
    return True

def main():
    parser = argparse.ArgumentParser(description="Aegis Test Runner")
    parser.add_argument(
        "test_type",
        choices=[
            "unit", "integration", "performance", "e2e", "installation",
            "quick", "all", "coverage", "output", "parallel", "validate"
        ],
        help="Type of tests to run"
    )
    parser.add_argument(
        "--specific",
        help="Run a specific test file or test function"
    )
    parser.add_argument(
        "--no-validation",
        action="store_true",
        help="Skip environment validation"
    )
    
    args = parser.parse_args()
    
    # Validar entorno (a menos que se skip)
    if not args.no_validation and not validate_environment():
        print("\n❌ Environment validation failed!")
        sys.exit(1)
    
    print(f"\n🚀 Starting {args.test_type} tests for Aegis Pentest Automation")
    print("=" * 60)
    
    # Ejecutar tests específicos si se proporciona
    if args.specific:
        exit_code = run_specific_test(args.specific)
    elif args.test_type == "unit":
        exit_code = run_unit_tests()
    elif args.test_type == "integration":
        exit_code = run_integration_tests()
    elif args.test_type == "performance":
        exit_code = run_performance_tests()
    elif args.test_type == "e2e":
        exit_code = run_e2e_tests()
    elif args.test_type == "installation":
        exit_code = run_installation_tests()
    elif args.test_type == "quick":
        exit_code = run_quick_tests()
    elif args.test_type == "all":
        exit_code = run_all_tests()
    elif args.test_type == "coverage":
        exit_code = run_coverage_report()
    elif args.test_type == "output":
        exit_code = run_tests_with_output()
    elif args.test_type == "parallel":
        exit_code = run_parallel_tests()
    elif args.test_type == "validate":
        exit_code = 0 if validate_environment() else 1
    else:
        print(f"❌ Unknown test type: {args.test_type}")
        exit_code = 1
    
    print("\n" + "=" * 60)
    if exit_code == 0:
        print("🎉 All tests completed successfully!")
    else:
        print("💥 Some tests failed!")
    
    sys.exit(exit_code)

if __name__ == "__main__":
    main() 