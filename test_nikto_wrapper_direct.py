#!/usr/bin/env python3
"""
Script de prueba directa para el NiktoWrapper
Permite probar rápidamente las modificaciones sin ejecutar todo Aegis
"""

import asyncio
import sys
import os
from pathlib import Path

# Agregar el directorio padre al path para importar aegis_pentest
sys.path.insert(0, str(Path(__file__).parent))

from aegis_pentest.utils.config import Config
from aegis_pentest.tools.nikto_wrapper import NiktoWrapper
from aegis_pentest.utils.logger import get_logger
from rich.console import Console

async def test_nikto_wrapper(target="http://httpbin.org"):
    """Prueba directa del wrapper de Nikto"""
    console = Console()
    
    print("🧪 TEST DIRECTO DEL NIKTO WRAPPER")
    print("=" * 50)
    print(f"Target: {target}")
    print()
    
    try:
        # Inicializar configuración mínima
        console.print("📋 Inicializando configuración...", style="blue")
        config = Config()
        
        # Verificar que Nikto esté disponible
        if not config.is_tool_available('nikto'):
            console.print("❌ Nikto no está disponible", style="red")
            return
        
        console.print("✅ Nikto está disponible", style="green")
        
        # Inicializar wrapper
        console.print("🔧 Inicializando NiktoWrapper...", style="blue")
        nikto = NiktoWrapper(config)
        
        # Inicializar logger para capturar output
        logger = get_logger(console)
        
        console.print("🚀 Iniciando escaneo Nikto...", style="yellow")
        console.print(f"Comando aproximado: nikto -h {target} -maxtime 60 -timeout 5", style="dim")
        print()
        
        # Ejecutar escaneo con tiempo limitado para prueba rápida
        result = await nikto.scan(target)
        
        print()
        console.print("✅ Escaneo completado!", style="green")
        print("=" * 50)
        
        # Mostrar estadísticas
        stats = result.scan_stats
        console.print("📊 ESTADÍSTICAS:", style="bold cyan")
        console.print(f"  Target: {stats.get('target', 'N/A')}")
        console.print(f"  Vulnerabilidades encontradas: {stats.get('total_vulnerabilities', 0)}")
        console.print(f"  Escaneo completado: {stats.get('scan_completed', False)}")
        console.print(f"  Timeout interno: {stats.get('timeout_occurred', False)}")
        console.print(f"  Límite de errores: {stats.get('error_limit_reached', False)}")
        console.print(f"  Duración: {stats.get('scan_duration', 'N/A')}")
        print()
        
        # Mostrar vulnerabilidades encontradas
        if result.vulnerabilities:
            console.print("🔍 VULNERABILIDADES ENCONTRADAS:", style="bold red")
            for i, vuln in enumerate(result.vulnerabilities, 1):
                console.print(f"  [{i}] {vuln.get('description', 'Sin descripción')[:100]}...")
                console.print(f"      Severidad: {vuln.get('severity', 'unknown')}")
                console.print(f"      URI: {vuln.get('uri', 'N/A')}")
                print()
        else:
            console.print("ℹ️  No se encontraron vulnerabilidades", style="yellow")
        
        # Mostrar una muestra del output raw para verificar filtrado
        console.print("📄 MUESTRA DEL OUTPUT RAW (primeras 10 líneas):", style="bold blue")
        raw_lines = result.raw_output.splitlines()[:10]
        for line in raw_lines:
            console.print(f"  {line}", style="dim")
        if len(result.raw_output.splitlines()) > 10:
            console.print(f"  ... y {len(result.raw_output.splitlines()) - 10} líneas más", style="dim")
        
        print()
        console.print("🎯 ANÁLISIS DEL FILTRADO:", style="bold magenta")
        
        # Simular qué líneas se filtrarían vs qué se mantendría
        from aegis_pentest.utils.logger import ToolLogger
        test_logger = ToolLogger(console)
        
        kept_lines = []
        filtered_lines = []
        
        for line in result.raw_output.splitlines():
            if line.strip():
                filtered_result = test_logger._format_nikto_output(line)
                if filtered_result:
                    kept_lines.append(line)
                else:
                    filtered_lines.append(line)
        
        total_lines = len([l for l in result.raw_output.splitlines() if l.strip()])
        console.print(f"  Total líneas con contenido: {total_lines}")
        console.print(f"  Líneas mantenidas en logs: {len(kept_lines)} ({len(kept_lines)/total_lines*100:.1f}%)")
        console.print(f"  Líneas filtradas: {len(filtered_lines)} ({len(filtered_lines)/total_lines*100:.1f}%)")
        
        if kept_lines:
            console.print("\n🟢 LÍNEAS QUE SE GUARDAN EN LOGS:", style="green")
            for line in kept_lines[:5]:  # Solo mostrar primeras 5
                formatted = test_logger._format_nikto_output(line)
                console.print(f"  {formatted}")
            if len(kept_lines) > 5:
                console.print(f"  ... y {len(kept_lines) - 5} más")
        
        if filtered_lines:
            console.print("\n🔴 LÍNEAS QUE SE FILTRAN (no van a logs):", style="red")
            for line in filtered_lines[:3]:  # Solo mostrar primeras 3
                console.print(f"  {line}", style="dim")
            if len(filtered_lines) > 3:
                console.print(f"  ... y {len(filtered_lines) - 3} más", style="dim")
        
        return result
        
    except Exception as e:
        console.print(f"❌ Error en el test: {str(e)}", style="red")
        import traceback
        console.print(f"Traceback: {traceback.format_exc()}", style="dim red")
        return None

def main():
    """Función principal"""
    target = sys.argv[1] if len(sys.argv) > 1 else "http://httpbin.org"
    
    # Ejecutar test
    result = asyncio.run(test_nikto_wrapper(target))
    
    if result:
        print("\n🎉 Test completado exitosamente!")
        
        # Verificar archivo de logs para confirmar que se esté filtrando
        logger = get_logger()
        log_file = logger.get_log_file_path()
        print(f"📁 Archivo de logs: {log_file}")
        
        if log_file.exists():
            print(f"📏 Tamaño del archivo de logs: {log_file.stat().st_size} bytes")
            
            # Leer contenido del archivo de logs
            with open(log_file, 'r', encoding='utf-8') as f:
                log_content = f.read()
            
            nikto_sections = log_content.count('[NIKTO]')
            print(f"🔍 Entradas [NIKTO] en logs: {nikto_sections}")
            
            if nikto_sections > 0:
                print("✅ Los filtros están funcionando - se están guardando hallazgos")
            else:
                print("⚠️  No se encontraron entradas [NIKTO] en logs - revisar filtros")
        else:
            print("⚠️  No se encontró archivo de logs")
    else:
        print("\n❌ Test falló")

if __name__ == "__main__":
    main() 