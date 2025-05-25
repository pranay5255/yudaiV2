#!/usr/bin/env python3
"""
Yudai V2 dbt Orchestrator

This script orchestrates dbt commands (seed, run, test) using subprocesses
as specified in the README requirements.
"""

import subprocess
import sys
import os
import logging
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class DbtRunResult:
    """Result of a dbt command execution"""
    command: str
    success: bool
    stdout: str
    stderr: str
    return_code: int
    duration: float

class DbtOrchestrator:
    """Orchestrates dbt commands for Yudai V2"""
    
    def __init__(self, project_dir: Optional[str] = None, profiles_dir: Optional[str] = None):
        self.project_dir = Path(project_dir) if project_dir else Path.cwd()
        self.profiles_dir = Path(profiles_dir) if profiles_dir else Path.home() / ".dbt"
        self.dbt_project_path = self.project_dir / "dbt_project.yml"
        
        # Ensure dbt project exists
        if not self.dbt_project_path.exists():
            raise FileNotFoundError(f"dbt_project.yml not found at {self.dbt_project_path}")
        
        logger.info(f"Initialized dbt orchestrator for project: {self.project_dir}")
    
    def _run_dbt_command(self, command: List[str], timeout: int = 300) -> DbtRunResult:
        """Execute a dbt command and return the result"""
        start_time = datetime.now()
        
        # Prepare the full command
        full_command = ["dbt"] + command + [
            "--project-dir", str(self.project_dir),
            "--profiles-dir", str(self.profiles_dir)
        ]
        
        logger.info(f"Executing: {' '.join(full_command)}")
        
        try:
            result = subprocess.run(
                full_command,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=self.project_dir
            )
            
            duration = (datetime.now() - start_time).total_seconds()
            
            dbt_result = DbtRunResult(
                command=' '.join(command),
                success=result.returncode == 0,
                stdout=result.stdout,
                stderr=result.stderr,
                return_code=result.returncode,
                duration=duration
            )
            
            if dbt_result.success:
                logger.info(f"✅ Command succeeded: {dbt_result.command} (took {duration:.2f}s)")
            else:
                logger.error(f"❌ Command failed: {dbt_result.command} (return code: {result.returncode})")
                logger.error(f"STDERR: {result.stderr}")
            
            return dbt_result
            
        except subprocess.TimeoutExpired:
            duration = (datetime.now() - start_time).total_seconds()
            logger.error(f"❌ Command timed out after {timeout}s: {' '.join(command)}")
            return DbtRunResult(
                command=' '.join(command),
                success=False,
                stdout="",
                stderr=f"Command timed out after {timeout} seconds",
                return_code=-1,
                duration=duration
            )
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            logger.error(f"❌ Command failed with exception: {e}")
            return DbtRunResult(
                command=' '.join(command),
                success=False,
                stdout="",
                stderr=str(e),
                return_code=-1,
                duration=duration
            )
    
    def debug(self) -> DbtRunResult:
        """Run dbt debug to check configuration"""
        return self._run_dbt_command(["debug"])
    
    def deps(self) -> DbtRunResult:
        """Install dbt dependencies"""
        return self._run_dbt_command(["deps"])
    
    def seed(self, select: Optional[str] = None) -> DbtRunResult:
        """Run dbt seed to load CSV files"""
        command = ["seed"]
        if select:
            command.extend(["--select", select])
        return self._run_dbt_command(command)
    
    def run(self, select: Optional[str] = None, models: Optional[List[str]] = None) -> DbtRunResult:
        """Run dbt models"""
        command = ["run"]
        if select:
            command.extend(["--select", select])
        elif models:
            command.extend(["--models"] + models)
        return self._run_dbt_command(command)
    
    def test(self, select: Optional[str] = None) -> DbtRunResult:
        """Run dbt tests"""
        command = ["test"]
        if select:
            command.extend(["--select", select])
        return self._run_dbt_command(command)
    
    def snapshot(self, select: Optional[str] = None) -> DbtRunResult:
        """Run dbt snapshots"""
        command = ["snapshot"]
        if select:
            command.extend(["--select", select])
        return self._run_dbt_command(command)
    
    def run_pipeline(self, steps: List[str] = None, select: Optional[str] = None) -> Dict[str, DbtRunResult]:
        """Run a complete dbt pipeline with specified steps"""
        if steps is None:
            steps = ["seed", "run", "test"]
        
        results = {}
        
        logger.info(f"🚀 Starting dbt pipeline with steps: {steps}")
        
        for step in steps:
            if step == "seed":
                results[step] = self.seed(select=select)
            elif step == "run":
                results[step] = self.run(select=select)
            elif step == "test":
                results[step] = self.test(select=select)
            elif step == "snapshot":
                results[step] = self.snapshot(select=select)
            elif step == "deps":
                results[step] = self.deps()
            else:
                logger.warning(f"Unknown step: {step}")
                continue
            
            # Stop pipeline if step fails
            if not results[step].success:
                logger.error(f"❌ Pipeline failed at step: {step}")
                break
        
        # Log pipeline summary
        successful_steps = [step for step, result in results.items() if result.success]
        failed_steps = [step for step, result in results.items() if not result.success]
        
        if failed_steps:
            logger.error(f"❌ Pipeline completed with failures. Successful: {successful_steps}, Failed: {failed_steps}")
        else:
            logger.info(f"✅ Pipeline completed successfully. Steps: {successful_steps}")
        
        return results

def main():
    """CLI interface for the dbt orchestrator"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Yudai V2 dbt Orchestrator")
    parser.add_argument("command", choices=["debug", "deps", "seed", "run", "test", "snapshot", "pipeline"], 
                       help="dbt command to execute")
    parser.add_argument("--select", help="dbt selector for models/tests")
    parser.add_argument("--models", nargs="+", help="specific models to run")
    parser.add_argument("--steps", nargs="+", default=["seed", "run", "test"], 
                       help="pipeline steps (for pipeline command)")
    parser.add_argument("--project-dir", help="dbt project directory")
    parser.add_argument("--profiles-dir", help="dbt profiles directory")
    parser.add_argument("--json", action="store_true", help="output results as JSON")
    
    args = parser.parse_args()
    
    try:
        orchestrator = DbtOrchestrator(
            project_dir=args.project_dir,
            profiles_dir=args.profiles_dir
        )
        
        if args.command == "debug":
            result = orchestrator.debug()
        elif args.command == "deps":
            result = orchestrator.deps()
        elif args.command == "seed":
            result = orchestrator.seed(select=args.select)
        elif args.command == "run":
            result = orchestrator.run(select=args.select, models=args.models)
        elif args.command == "test":
            result = orchestrator.test(select=args.select)
        elif args.command == "snapshot":
            result = orchestrator.snapshot(select=args.select)
        elif args.command == "pipeline":
            results = orchestrator.run_pipeline(steps=args.steps, select=args.select)
            if args.json:
                print(json.dumps({
                    step: {
                        "success": result.success,
                        "command": result.command,
                        "return_code": result.return_code,
                        "duration": result.duration
                    } for step, result in results.items()
                }, indent=2))
            sys.exit(0 if all(r.success for r in results.values()) else 1)
        
        if args.json:
            print(json.dumps({
                "success": result.success,
                "command": result.command,
                "return_code": result.return_code,
                "duration": result.duration,
                "stdout": result.stdout,
                "stderr": result.stderr
            }, indent=2))
        
        sys.exit(0 if result.success else 1)
        
    except Exception as e:
        logger.error(f"❌ Orchestrator failed: {e}")
        if args.json:
            print(json.dumps({"error": str(e)}, indent=2))
        sys.exit(1)

if __name__ == "__main__":
    main() 