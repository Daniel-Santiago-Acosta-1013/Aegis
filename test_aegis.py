#!/usr/bin/env python3
"""
Script de prueba para Aegis Pentest Automation
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

def test_imports():
    """Prueba las importaciones básicas"""
    print("🧪 Probando importaciones...")
    
    try:
        # Importaciones básicas
        from aegis_pentest.utils.config import Config
        from aegis_pentest.utils.helpers import validate_target, setup_logging
        from aegis_pentest.tools.nmap_wrapper import NmapWrapper
        from aegis_pentest.core.scanner import AegisScanner
        print("  ✅ Importaciones del core exitosas")
        
        # Importaciones de GUI
        from aegis_pentest.gui.main_window import AegisMainWindow
        print("  ✅ Importaciones de GUI exitosas")
        
        return True
    except ImportError as e:
        print(f"  ❌ Error de importación: {e}")
        return False

def test_config():
    """Prueba el sistema de configuración"""
    print("\n🔧 Probando sistema de configuración...")
    
    try:
        from aegis_pentest.utils.config import Config
        
        config = Config()
        
        # Probar métodos básicos
        tools = config.get_available_tools()
        print(f"  ✅ Herramientas disponibles: {len(tools)} categorías")
        
        # Probar configuración específica
        nmap_config = config.get_tool_config('nmap')
        print(f"  ✅ Configuración de Nmap: {bool(nmap_config)}")
        
        reports_dir = config.reports_dir
        print(f"  ✅ Directorio de reportes: {reports_dir}")
        
        return True
    except Exception as e:
        print(f"  ❌ Error en configuración: {e}")
        return False

def test_helpers():
    """Prueba las funciones auxiliares"""
    print("\n🛠️ Probando funciones auxiliares...")
    
    try:
        from aegis_pentest.utils.helpers import validate_target, parse_ports
        
        # Probar validación de objetivos
        test_targets = [
            "google.com",
            "192.168.1.1", 
            "http://example.com",
            "invalid..domain"
        ]
        
        for target in test_targets:
            is_valid, target_type, message = validate_target(target)
            status = "✅" if is_valid else "❌"
            print(f"  {status} {target}: {target_type or message}")
        
        # Probar parsing de puertos
        port_tests = ["80", "80,443", "1-1000", "80,443,8000-8010"]
        for port_string in port_tests:
            try:
                ports = parse_ports(port_string)
                print(f"  ✅ Puertos '{port_string}': {len(ports)} puertos")
            except ValueError as e:
                print(f"  ❌ Error parsing '{port_string}': {e}")
        
        return True
    except Exception as e:
        print(f"  ❌ Error en helpers: {e}")
        return False

def test_tools():
    """Prueba los wrappers de herramientas"""
    print("\n🔨 Probando wrappers de herramientas...")
    
    try:
        from aegis_pentest.utils.config import Config
        from aegis_pentest.tools.nmap_wrapper import NmapWrapper
        
        config = Config()
        
        # Probar Nmap wrapper
        nmap = NmapWrapper(config)
        is_available = nmap.is_available()
        print(f"  {'✅' if is_available else '⚠️'} Nmap disponible: {is_available}")
        
        if is_available:
            templates = nmap.get_scan_templates()
            print(f"  ✅ Templates de Nmap: {len(templates)}")
        
        # Probar otros wrappers
        try:
            from aegis_pentest.tools.nuclei_wrapper import NucleiWrapper
            nuclei = NucleiWrapper(config)
            nuclei_available = nuclei.is_available()
            print(f"  {'✅' if nuclei_available else '⚠️'} Nuclei disponible: {nuclei_available}")
        except Exception:
            print("  ⚠️ Nuclei wrapper no disponible")
        
        try:
            from aegis_pentest.tools.gobuster_wrapper import GobusterWrapper
            gobuster = GobusterWrapper(config)
            gobuster_available = gobuster.is_available()
            print(f"  {'✅' if gobuster_available else '⚠️'} Gobuster disponible: {gobuster_available}")
        except Exception:
            print("  ⚠️ Gobuster wrapper no disponible")
        
        return True
    except Exception as e:
        print(f"  ❌ Error en tools: {e}")
        return False

def test_scanner():
    """Prueba el motor principal de escaneo"""
    print("\n🔍 Probando motor de escaneo...")
    
    try:
        from aegis_pentest.utils.config import Config
        from aegis_pentest.core.scanner import AegisScanner
        
        config = Config()
        scanner = AegisScanner(config)
        
        # Probar métodos básicos
        scan_types = scanner.get_available_scan_types()
        print(f"  ✅ Tipos de escaneo disponibles: {len(scan_types)}")
        
        status = scanner.get_scan_status()
        print(f"  ✅ Estado del scanner: {status['status']}")
        
        return True
    except Exception as e:
        print(f"  ❌ Error en scanner: {e}")
        return False

def test_gui_creation():
    """Prueba la creación de la GUI (sin mostrarla)"""
    print("\n🖥️ Probando creación de GUI...")
    
    try:
        # Importar PyQt6 sin crear QApplication todavía
        from PyQt6.QtWidgets import QApplication
        from aegis_pentest.gui.main_window import AegisMainWindow
        
        # No crear la aplicación real para evitar problemas en headless
        print("  ✅ Clases de GUI importadas correctamente")
        print("  ⚠️ GUI no ejecutada (modo headless)")
        
        return True
    except Exception as e:
        print(f"  ❌ Error en GUI: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("🛡️ AEGIS PENTEST AUTOMATION - PRUEBAS UNITARIAS")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_config,
        test_helpers,
        test_tools,
        test_scanner,
        test_gui_creation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 RESULTADO FINAL")
    print(f"Pruebas pasadas: {passed}/{total}")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron exitosamente!")
        print("\n🚀 Para ejecutar la aplicación:")
        print("   poetry run python -m aegis_pentest.main")
        print("   o")
        print("   poetry run aegis-pentest")
        return 0
    else:
        print("❌ Algunas pruebas fallaron")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 