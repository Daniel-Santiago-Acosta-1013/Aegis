#!/usr/bin/env python3
"""
🛡️ Aegis Pentest Automation - CLI Interactiva
Interfaz de línea de comandos completamente interactiva para automatización de pentesting

Uso:
    python aegis_cli.py
    poetry run python aegis_cli.py
"""

import sys
import asyncio
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

from aegis_pentest.cli.main_cli import AegisCLI


async def run_cli():
    """Función asíncrona para ejecutar la CLI"""
    try:
        cli_app = AegisCLI()
        await cli_app.run()
    except KeyboardInterrupt:
        cli_app.console.print("\n[yellow]👋 Sesión interrumpida por el usuario[/yellow]")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error fatal: {str(e)}")
        sys.exit(1)


def main():
    """Punto de entrada principal para Poetry scripts"""
    asyncio.run(run_cli())


if __name__ == '__main__':
    main() 