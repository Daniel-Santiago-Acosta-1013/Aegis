#!/usr/bin/env python3
"""
Script principal para ejecutar todos los tests de Aegis con Poetry

Este es el punto de entrada único para ejecutar toda la suite de tests
cuando se usa el comando: poetry run test
"""

import sys
import subprocess
import os
from pathlib import Path


def main():
    """Función principal que ejecuta todos los tests"""
    print("🚀 Iniciando suite completa de tests para Aegis Pentest Automation")
    print("=" * 70)
    
    # Configurar directorio de trabajo
    project_root = Path(__file__).parent.parent.parent
    os.chdir(project_root)
    
    # Comando completo de pytest con todas las opciones
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/",
        "-v",
        "--cov=aegis_pentest",
        "--cov-report=html:tests/coverage_html",
        "--cov-report=term-missing",
        "--cov-report=xml:tests/coverage.xml",
        "--junit-xml=tests/test_results.xml",
        "--tb=short"
    ]
    
    print(f"🔍 Ejecutando comando: {' '.join(cmd)}")
    print("-" * 70)
    
    try:
        # Ejecutar pytest
        result = subprocess.run(cmd, check=False)
        
        print("\n" + "=" * 70)
        if result.returncode == 0:
            print("🎉 ¡Todos los tests pasaron exitosamente!")
            print("\n📊 Reportes generados:")
            print("   • Cobertura HTML: tests/coverage_html/index.html")
            print("   • Cobertura XML:  tests/coverage.xml")
            print("   • Resultados:     tests/test_results.xml")
        else:
            print("💥 Algunos tests fallaron. Revisa el output anterior.")
            print("\n📋 Para más detalles:")
            print("   • Ejecuta tests específicos: python -m pytest tests/unit/ -v")
            print("   • Ver logs detallados: python -m pytest tests/ -v -s --tb=long")
        
        return result.returncode
        
    except KeyboardInterrupt:
        print("\n⚠️  Tests interrumpidos por el usuario")
        return 130
    except Exception as e:
        print(f"\n❌ Error ejecutando tests: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 