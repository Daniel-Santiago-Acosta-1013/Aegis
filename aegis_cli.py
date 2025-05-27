#!/usr/bin/env python3
"""
Punto de entrada principal para Aegis Pentest Automation
Manejo automático de privilegios, dependencias y ejecución
Comando único: poetry run python aegis_cli.py
"""

import os
import sys
import subprocess
import platform
import asyncio
from pathlib import Path


def print_banner():
    """Muestra el banner de inicio optimizado"""
    banner = """
    ╔═══════════════════════════════════════╗
    ║     🛡️  AEGIS PENTEST AUTOMATION  🛡️     ║
    ╠═══════════════════════════════════════╣
    ║  Automatización de Pentesting Web    ║
    ║     Comando único optimizado         ║
    ╚═══════════════════════════════════════╝
    """
    print(banner)


def check_python_version():
    """Verifica la versión de Python"""
    if sys.version_info < (3, 9):
        print("❌ Python 3.9+ requerido")
        print(f"   Versión actual: {sys.version}")
        return False
    return True


def check_dependencies():
    """Verifica las dependencias están instaladas"""
    try:
        # Intentar importar las dependencias principales
        import rich
        import yaml
        import nmap
        print("✅ Dependencias principales verificadas")
        return True
    except ImportError as e:
        print(f"❌ Dependencia faltante: {e}")
        print("💡 Ejecuta: poetry install")
        return False


def check_permissions():
    """Verifica y maneja los permisos del sistema"""
    system = platform.system().lower()
    
    if system in ['linux', 'darwin']:  # Linux o macOS
        is_root = os.getuid() == 0
        has_sudo = subprocess.run(['which', 'sudo'], capture_output=True).returncode == 0
        
        return {
            'is_root': is_root,
            'has_sudo': has_sudo,
            'system': system
        }
    else:
        # Windows - implementación básica
        try:
            import ctypes
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
            return {
                'is_root': is_admin,
                'has_sudo': False,
                'system': 'windows'
            }
        except:
            return {
                'is_root': False,
                'has_sudo': False,
                'system': 'windows'
            }


def handle_privilege_escalation(perms):
    """Maneja la escalación de privilegios si es necesaria"""
    if perms['is_root']:
        print("🔐 Ejecutándose como administrador/root")
        return True
    
    if perms['has_sudo'] and perms['system'] != 'windows':
        print("🔑 Usuario normal detectado - privilegios sudo disponibles")
        print("💡 Aegis manejará la elevación automáticamente cuando sea necesario")
        return True
    
    if perms['system'] in ['linux', 'darwin']:
        print("⚠️  Sin privilegios de administrador detectados")
        try:
            choice = input("\n¿Intentar reejecutar con sudo? (s/N): ").lower().strip()
            if choice in ['s', 'si', 'sí', 'y', 'yes']:
                print("🔑 Relanzando con sudo...")
                # Reejecutar con sudo
                os.execvp('sudo', ['sudo'] + sys.argv)
        except KeyboardInterrupt:
            print("\n👋 Cancelado por el usuario")
            return False
    
    print("⚠️  Continuando con privilegios limitados")
    print("   Algunas funcionalidades pueden no estar disponibles")
    return True


def check_tools_availability():
    """Verifica herramientas básicas están disponibles"""
    tools = ['nmap']
    available = []
    missing = []
    
    for tool in tools:
        if subprocess.run(['which', tool], capture_output=True).returncode == 0:
            available.append(tool)
        else:
            missing.append(tool)
    
    if available:
        print(f"✅ Herramientas disponibles: {', '.join(available)}")
    
    if missing:
        print(f"⚠️  Herramientas faltantes: {', '.join(missing)}")
        print("💡 Algunas funcionalidades estarán limitadas")
        print("   Instala con: brew install nmap (macOS) o sudo apt install nmap (Linux)")
    
    return len(available) > 0


async def run_aegis():
    """Ejecuta la aplicación principal"""
    try:
        # Importar y ejecutar el CLI principal
        from aegis_pentest.cli.main_cli import AegisCLI
        
        print("\n🚀 Iniciando Aegis Pentest Automation...")
        
        # Crear y ejecutar la aplicación
        cli = AegisCLI()
        await cli.run()
        
        return True
        
    except ImportError as e:
        print(f"\n❌ Error importando módulos: {e}")
        print("💡 Verifica que el proyecto esté instalado correctamente")
        return False
    except KeyboardInterrupt:
        print("\n\n👋 Aegis interrumpido por el usuario")
        return True
    except Exception as e:
        print(f"\n💥 Error ejecutando Aegis: {e}")
        import traceback
        print("🔧 Traceback para debug:")
        traceback.print_exc()
        return False


def main():
    """Función principal optimizada"""
    print_banner()
    
    # Verificaciones iniciales
    print("🔍 Verificando sistema...")
    
    # 1. Verificar Python
    if not check_python_version():
        return 1
    print("✅ Versión de Python correcta")
    
    # 2. Verificar dependencias
    if not check_dependencies():
        return 1
    
    # 3. Verificar permisos
    perms = check_permissions()
    if not handle_privilege_escalation(perms):
        return 1
    
    # 4. Verificar herramientas (opcional, no bloquea ejecución)
    check_tools_availability()
    
    # 5. Todo listo para ejecutar
    print("\n" + "="*50)
    print("🎯 Sistema verificado - Iniciando Aegis")
    print("="*50)
    
    try:
        # Ejecutar la aplicación
        success = asyncio.run(run_aegis())
        
        if success:
            print("\n✅ Aegis finalizado correctamente")
            return 0
        else:
            print("\n❌ Aegis finalizado con errores")
            return 1
            
    except KeyboardInterrupt:
        print("\n\n👋 Programa interrumpido por el usuario")
        return 0
    except Exception as e:
        print(f"\n💥 Error crítico: {e}")
        return 1


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n👋 Programa interrumpido por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n💥 Error crítico inesperado: {e}")
        sys.exit(1) 