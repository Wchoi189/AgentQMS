#!/usr/bin/env python3
"""
Streamlit Process Manager for Korean Grammar Correction

This script provides proper process management for the Korean Grammar Correction Streamlit application
to prevent zombie processes and ensure clean startup/shutdown.
"""

import argparse
import contextlib
import importlib.util
import os
import re
import shutil
import signal
import socket
import subprocess
import sys
import time
from pathlib import Path

import psutil


def _load_bootstrap():
    if "scripts._bootstrap" in sys.modules:
        return sys.modules["scripts._bootstrap"]

    current_dir = Path(__file__).resolve().parent
    for directory in (current_dir, *tuple(current_dir.parents)):
        candidate = directory / "_bootstrap.py"
        if candidate.exists():
            spec = importlib.util.spec_from_file_location(
                "scripts._bootstrap", candidate
            )
            if spec is None or spec.loader is None:  # pragma: no cover - defensive
                continue
            module = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = module
            spec.loader.exec_module(module)
            return module
    raise RuntimeError("Could not locate scripts/_bootstrap.py")


_BOOTSTRAP = _load_bootstrap()
setup_project_paths = _BOOTSTRAP.setup_project_paths
get_path_resolver = _BOOTSTRAP.get_path_resolver

setup_project_paths()


class GrammarCorrectionProcessManager:
    """Manages the Korean Grammar Correction Streamlit process with proper lifecycle handling."""

    def __init__(self) -> None:
        self.resolver = get_path_resolver()
        self.project_root = self.resolver.config.project_root
        self.streamlit_app_dir = self.resolver.config.streamlit_dir

    def _get_main_app_path(self) -> Path:
        """Get the path to the main Streamlit app."""
        return Path(self.streamlit_app_dir) / "main.py"

    def _get_pid_file(self, port: int) -> Path:
        """Get the PID file path for the Streamlit process."""
        return Path(self.project_root) / f".grammar_correction_app_{port}.pid"

    def _write_pid_file(self, port: int, pid: int) -> None:
        """Write the PID file."""
        pid_file = self._get_pid_file(port)
        with open(pid_file, "w") as f:
            f.write(str(pid))

    def _read_pid_file(self, port: int) -> int | None:
        """Read the PID file."""
        pid_file = self._get_pid_file(port)
        if pid_file.exists():
            try:
                with open(pid_file) as f:
                    return int(f.read().strip())
            except (ValueError, OSError):
                return None
        return None

    def _get_log_files(self, port: int) -> tuple[Path, Path]:
        """Get the log file paths for the Streamlit process."""
        log_dir = self.resolver.config.logs_dir / "streamlit"
        log_dir.mkdir(parents=True, exist_ok=True)
        stdout_log = log_dir / f"grammar_correction_app_{port}.out"
        stderr_log = log_dir / f"grammar_correction_app_{port}.err"
        return stdout_log, stderr_log

    def _remove_pid_file(self, port: int) -> None:
        """Remove the PID file."""
        pid_file = self._get_pid_file(port)
        if pid_file.exists():
            pid_file.unlink()

    def _is_process_running(self, pid: int) -> bool:
        """Check if a process is running."""
        return bool(psutil.pid_exists(pid))

    def _is_port_available(self, port: int) -> bool:
        """Check if a port is available."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(("localhost", port))
            sock.close()
            return result != 0  # Port is available if connect fails
        except Exception:
            return True  # Assume available if we can't check

    def _find_project_processes(self) -> list[psutil.Process]:
        """Find all Streamlit processes related to this project."""
        project_processes = []
        for proc in psutil.process_iter(["pid", "name", "cmdline"]):
            try:
                if not proc.info["cmdline"]:
                    continue  # Skip processes with empty cmdline
                cmd_str = " ".join(proc.info["cmdline"])
                # Check if it's a streamlit process for our project
                if (
                    "streamlit" in cmd_str
                    and "run" in cmd_str
                    and str(self.project_root) in cmd_str
                    and "main.py" in cmd_str
                ):
                    project_processes.append(proc)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return project_processes

    def _find_existing_streamlit_processes(self) -> list[tuple[int, int]]:
        """Find existing Streamlit processes and their ports."""
        processes = []
        for proc in self._find_project_processes():
            cmd_str = " ".join(proc.info["cmdline"])
            port = self._extract_port_from_command(cmd_str)
            if port:
                processes.append((proc.pid, port))
        return processes

    def _extract_port_from_command(self, cmd: str) -> int | None:
        """Extract port number from streamlit command line."""
        patterns = [
            r"--server\.port\s+(\d+)",
            r"--port\s+(\d+)",
            r"--server\.port=(\d+)",
            r"--port=(\d+)",
        ]
        for pattern in patterns:
            match = re.search(pattern, cmd)
            if match:
                try:
                    return int(match.group(1))
                except ValueError:
                    continue
        return None

    def _cleanup_orphaned_processes(self) -> None:
        """Clean up any orphaned Streamlit processes related to this project."""
        for proc in self._find_project_processes():
            print(f"Found orphaned Streamlit process (PID: {proc.pid})... terminating.")
            try:
                proc.terminate()
                proc.wait(timeout=3.0)
            except psutil.TimeoutExpired:
                print(f"Graceful shutdown failed for {proc.pid}, forcing kill.")
                proc.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

    def start(
        self,
        port: int = 8501,
        background: bool = True,
        enable_logging: bool = True,
        restart: bool = False,
    ) -> int | None:
        """Start the Korean Grammar Correction Streamlit process."""
        app_path = self._get_main_app_path()

        # First, check for existing Streamlit processes
        existing_processes = self._find_existing_streamlit_processes()
        if existing_processes:
            for pid, actual_port in existing_processes:
                if actual_port == port:
                    if restart:
                        print(
                            f"Restarting Korean Grammar Correction app on port {port} (stopping PID: {pid})...",
                        )
                        self.stop(port)
                    else:
                        print(
                            f"Korean Grammar Correction app is already running on port {port} (PID: {pid})",
                        )
                        # Create PID file for the existing process
                        self._write_pid_file(port, pid)
                        return pid
                else:
                    print(
                        f"Found existing Streamlit process on port {actual_port} (PID: {pid}). "
                        f"Requested port {port} may be different."
                    )

        # Check if already running via PID file
        existing_pid = self._read_pid_file(port)
        if existing_pid:
            if self._is_process_running(existing_pid):
                if restart:
                    print(
                        f"Restarting Korean Grammar Correction app on port {port} (stopping PID: {existing_pid})...",
                    )
                    self.stop(port)
                else:
                    print(
                        f"Korean Grammar Correction app is already running on port {port} (PID: {existing_pid})",
                    )
                    return existing_pid
            else:
                # Clean up stale PID file
                self._remove_pid_file(port)

        # Clean up any orphaned Streamlit processes
        self._cleanup_orphaned_processes()

        # Check if port is available
        if not self._is_port_available(port):
            print(f"Port {port} is already in use")
            return None

        # Find uv binary - check common locations
        uv_binary = shutil.which("uv")
        if not uv_binary:
            # Try common installation locations
            for path in [
                os.path.expanduser("~/.local/bin/uv"),
                os.path.expanduser("~/.cargo/bin/uv"),
                "/usr/local/bin/uv",
            ]:
                if os.path.exists(path):
                    uv_binary = path
                    break
        if not uv_binary:
            raise RuntimeError(
                "Could not find 'uv' binary. Please ensure uv is installed and in PATH."
            )

        # Build command
        cmd = [
            uv_binary,
            "run",
            "streamlit",
            "run",
            str(app_path),
            "--server.port",
            str(port),
            "--server.headless",
            "true",
            "--server.runOnSave",
            "false",
        ]

        print(f"Starting Korean Grammar Correction app on port {port}...")

        # Prepare environment with PATH including uv location
        env = os.environ.copy()
        uv_dir = os.path.dirname(uv_binary)
        if uv_dir not in env.get("PATH", ""):
            env["PATH"] = f"{uv_dir}:{env.get('PATH', '')}"

        if background:
            # Start in background with proper process group management
            if enable_logging:
                stdout_log, stderr_log = self._get_log_files(port)
                print(f"Logs will be written to: {stdout_log} and {stderr_log}")
                with (
                    open(stdout_log, "w") as stdout_handle,
                    open(stderr_log, "w") as stderr_handle,
                ):
                    process = subprocess.Popen(
                        cmd,
                        stdout=stdout_handle,
                        stderr=stderr_handle,
                        preexec_fn=os.setsid,  # Create new process group
                        cwd=self.project_root,
                        env=env,
                    )
            else:
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    preexec_fn=os.setsid,  # Create new process group
                    cwd=self.project_root,
                    env=env,
                )

            # Poll for startup instead of fixed sleep
            print("Waiting for app to start...")
            start_time = time.time()
            timeout = 15
            is_up = False
            while time.time() - start_time < timeout:
                if not self._is_port_available(port):
                    is_up = True
                    break
                if not self._is_process_running(process.pid):
                    print("Process terminated unexpectedly during startup.")
                    is_up = False
                    break
                time.sleep(0.5)

            if is_up:
                self._write_pid_file(port, process.pid)
                print(
                    f"Started Korean Grammar Correction app (PID: {process.pid}) on port {port}"
                )
                return process.pid
            else:
                print("Failed to start Korean Grammar Correction app.")
                if self._is_process_running(process.pid):
                    print("Cleaning up failed startup process...")
                    with contextlib.suppress(OSError):
                        os.killpg(os.getpgid(process.pid), signal.SIGKILL)
                return None
        else:
            # Run in foreground
            try:
                subprocess.run(cmd, cwd=self.project_root, env=env)
            except KeyboardInterrupt:
                print("\nStopped Korean Grammar Correction app")
            return None

    def stop(self, port: int = 8501) -> bool:
        """Stop the Korean Grammar Correction Streamlit process."""
        pid = self._read_pid_file(port)

        if not pid or not self._is_process_running(pid):
            # ... (your existing logic for no PID or not running) ...
            # Make sure to run cleanup here
            self._cleanup_orphaned_processes()
            return True

        print(f"Stopping Korean Grammar Correction app (PID: {pid})...")

        try:
            # Get the process group ID. Since we use os.setsid, pid == pgid
            pgid = os.getpgid(pid)

            # 1. Try graceful shutdown of the *entire group*
            print(f"Sending SIGTERM to process group {pgid}...")
            os.killpg(pgid, signal.SIGTERM)

            # Wait for it to die
            time.sleep(3)

            if not self._is_process_running(pid):
                print("Process group terminated gracefully.")
            else:
                # 2. Forceful shutdown of the *entire group*
                print(
                    f"Process {pid} still running. Sending SIGKILL to process group {pgid}..."
                )
                os.killpg(pgid, signal.SIGKILL)
                time.sleep(1)

            # 3. Final check
            if self._is_process_running(pid):
                print(f"Failed to stop process {pid}.")
                return False
            else:
                print("Stopped Korean Grammar Correction app.")
                self._remove_pid_file(port)
                # Also run general cleanup just in case
                self._cleanup_orphaned_processes()
                return True

        except (OSError, ProcessLookupError) as e:
            print(f"Error stopping process {pid}: {e}")
            if isinstance(e, ProcessLookupError):
                self._remove_pid_file(port)
                return True
            return False

    def status(self, port: int = 8501) -> bool:
        """Check the status of the Korean Grammar Correction Streamlit process."""
        # First check for existing processes
        existing_processes = self._find_existing_streamlit_processes()
        if existing_processes:
            print("Found existing Streamlit processes:")
            for pid, actual_port in existing_processes:
                status = "Running" if self._is_process_running(pid) else "Stopped"
                print(f"  PID: {pid}, Port: {actual_port}, Status: {status}")

            # Check if any match the requested port
            for pid, actual_port in existing_processes:
                if actual_port == port and self._is_process_running(pid):
                    print(
                        f"Korean Grammar Correction app: Running (PID: {pid}, Port: {port})"
                    )
                    return True

        # Check PID file
        pid = self._read_pid_file(port)  # type: ignore[assignment]
        if not pid:
            print("Korean Grammar Correction app: Not managed (no PID file)")
            return False

        if self._is_process_running(pid):
            print(f"Korean Grammar Correction app: Running (PID: {pid}, Port: {port})")
            return True
        else:
            print(f"Korean Grammar Correction app: Stopped (stale PID file: {pid})")
            self._remove_pid_file(port)
            return False

    def view_logs(
        self,
        port: int = 8501,
        lines: int = 50,
        follow: bool = False,
    ) -> None:
        """View logs for the Korean Grammar Correction Streamlit process."""
        stdout_log, stderr_log = self._get_log_files(port)

        existing_logs = []
        if stdout_log.exists():
            existing_logs.append(str(stdout_log))
        if stderr_log.exists():
            existing_logs.append(str(stderr_log))

        if not existing_logs:
            print(f"No log files found for port {port}")
            return

        print(f"=== Logs for Korean Grammar Correction app on port {port} ===")

        cmd = ["tail"]
        if follow:
            cmd.append("-f")

        cmd.extend([f"-n{lines}"])
        cmd.extend(existing_logs)

        try:
            # Use subprocess.run, which will stream output
            # This cleanly passes control to 'tail'
            subprocess.run(cmd)
        except KeyboardInterrupt:
            print("\nStopped following logs.")
        except FileNotFoundError:
            print("Error: 'tail' command not found. This feature requires 'tail'.")

    def clear_logs(self, port: int = 8501) -> None:
        """Clear log files for the Korean Grammar Correction Streamlit process."""
        stdout_log, stderr_log = self._get_log_files(port)

        cleared = []
        if stdout_log.exists():
            stdout_log.unlink()
            cleared.append(str(stdout_log))

        if stderr_log.exists():
            stderr_log.unlink()
            cleared.append(str(stderr_log))

        if cleared:
            print(f"Cleared log files: {', '.join(cleared)}")
        else:
            print("No log files found for Korean Grammar Correction app")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Korean Grammar Correction Streamlit Process Manager",
    )
    parser.add_argument(
        "action",
        choices=["start", "stop", "status", "logs", "clear-logs", "cleanup"],
        help="Action to perform",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8501,
        help="Port number (default: 8501)",
    )
    parser.add_argument(
        "--foreground",
        action="store_true",
        help="Run in foreground (only for start action)",
    )
    parser.add_argument(
        "--no-logging",
        action="store_true",
        help="Disable logging to files (only for start action)",
    )
    parser.add_argument(
        "--restart",
        action="store_true",
        help="Restart the app if it's already running (only for start action)",
    )
    parser.add_argument(
        "--lines",
        type=int,
        default=50,
        help="Number of log lines to show (default: 50)",
    )
    parser.add_argument(
        "--follow",
        action="store_true",
        help="Follow log files in real-time (only for logs action)",
    )

    args = parser.parse_args()

    manager = GrammarCorrectionProcessManager()

    if args.action == "start":
        background = not args.foreground
        enable_logging = not args.no_logging
        manager.start(args.port, background, enable_logging, args.restart)

    elif args.action == "stop":
        manager.stop(args.port)

    elif args.action == "status":
        manager.status(args.port)

    elif args.action == "logs":
        manager.view_logs(args.port, args.lines, args.follow)

    elif args.action == "clear-logs":
        manager.clear_logs(args.port)

    elif args.action == "cleanup":
        print("Cleaning up orphaned Streamlit processes...")
        manager._cleanup_orphaned_processes()
        print("Cleanup completed.")


if __name__ == "__main__":
    main()
