"""Z-Image generator core"""

import subprocess
from pathlib import Path

from config import Config, GenerationParams


class ZImageGenerator:
    """Z-Image Turbo image generator using stable-diffusion.cpp"""

    def __init__(self, config: Config | None = None):
        self.config = config or Config()
        self._sd_executable: Path | None = None

    # -------------------------------------------------------------------------
    # Validation
    # -------------------------------------------------------------------------

    def find_executable(self) -> Path | None:
        """Find stable-diffusion.cpp executable"""
        if self._sd_executable:
            return self._sd_executable

        for path in self.config.sd_cpp_paths:
            if path.exists():
                self._sd_executable = path
                return path
        return None

    def validate_models(self) -> list[tuple[str, Path]]:
        """Check for missing model files. Returns list of (name, path) tuples."""
        models = {
            "Diffusion Model": self.config.diffusion_model,
            "VAE": self.config.vae_model,
            "Text Encoder (LLM)": self.config.llm_model,
        }
        return [(name, path) for name, path in models.items() if not path.exists()]

    def validate(self) -> bool:
        """Validate all requirements. Returns True if ready."""
        if not self.find_executable():
            self._print_install_instructions()
            return False

        missing = self.validate_models()
        if missing:
            self._print_missing_models(missing)
            return False

        return True

    # -------------------------------------------------------------------------
    # Generation
    # -------------------------------------------------------------------------

    def build_command(self, params: GenerationParams) -> list[str]:
        """Build sd.cpp command from parameters"""
        cmd = [
            str(self.find_executable()),
            "--diffusion-model", str(self.config.diffusion_model),
            "--vae", str(self.config.vae_model),
            "--llm", str(self.config.llm_model),
            "-p", params.prompt,
            "-o", params.output,
            "--steps", str(params.steps),
            "--cfg-scale", str(params.cfg_scale),
            "-W", str(params.width),
            "-H", str(params.height),
        ]

        if params.seed is not None:
            cmd.extend(["--seed", str(params.seed)])

        if params.negative_prompt:
            cmd.extend(["-n", params.negative_prompt])

        if params.batch_count > 1:
            cmd.extend(["-b", str(params.batch_count)])

        return cmd

    def generate(self, params: GenerationParams) -> bool:
        """Generate image with given parameters. Returns True on success."""
        if not self.validate():
            return False

        cmd = self.build_command(params)

        print("\nExecuting:")
        print(" ".join(cmd))
        print()

        try:
            subprocess.run(cmd, check=True)
            print(f"\n✓ Image generated: {params.output}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"\n✗ Generation failed: {e}")
            return False
        except Exception as e:
            print(f"\n✗ Unexpected error: {e}")
            return False

    # -------------------------------------------------------------------------
    # Error Messages
    # -------------------------------------------------------------------------

    def _print_install_instructions(self):
        """Print sd.cpp installation instructions"""
        print("✗ stable-diffusion.cpp not found!")
        print("\nInstall:")
        print(f"  cd {self.config.base_dir}")
        print("  git clone --recursive https://github.com/leejet/stable-diffusion.cpp")
        print("  cd stable-diffusion.cpp && mkdir build && cd build")
        print("  cmake .. -DSD_CUBLAS=ON")
        print("  cmake --build . --config Release")

    def _print_missing_models(self, missing: list[tuple[str, Path]]):
        """Print missing model information"""
        print("\n✗ Missing model files:\n")
        for name, path in missing:
            print(f"  - {name}: {path}")
        print("\nDownload:")
        print("  bash download_zimage_files.sh")
        print("  # or: https://huggingface.co/leejet/Z-Image-Turbo-GGUF")
