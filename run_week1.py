#!/usr/bin/env python3
"""
Week 1 Foundations Launcher Script

This script launches the Week 1 Foundations implementation with proper Python path setup.
"""
import sys
import os
import subprocess
from pathlib import Path

def main():
    """Launch Week 1 Foundations application"""
    
    # Get the directory containing this script
    script_dir = Path(__file__).parent
    src_dir = script_dir / "src"
    
    # Add src directory to Python path
    env = os.environ.copy()
    current_pythonpath = env.get('PYTHONPATH', '')
    if current_pythonpath:
        env['PYTHONPATH'] = f"{src_dir}:{current_pythonpath}"
    else:
        env['PYTHONPATH'] = str(src_dir)
    
    # Build command
    cmd = [
        "uv", "run", "python", 
        str(src_dir / "week1_foundations" / "app.py")
    ]
    
    # Add any command line arguments passed to this script
    cmd.extend(sys.argv[1:])
    
    print("🚀 Launching Week 1 Foundations - Advanced AI Agent System")
    print(f"📂 Working directory: {script_dir}")
    print(f"🐍 Python path includes: {src_dir}")
    print(f"⚡ Command: {' '.join(cmd)}")
    print("="*60)
    
    # Execute the command
    try:
        subprocess.run(cmd, cwd=script_dir, env=env, check=True)
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error running application: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print(f"\n👋 Application stopped by user")
        sys.exit(0)

if __name__ == "__main__":
    main() 