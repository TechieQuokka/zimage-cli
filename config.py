"""Z-Image configuration"""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    """Z-Image path configuration"""

    base_dir: Path = Path("/home/beethoven/workspace/deeplearning/deeplearning-project/Z-Image")

    @property
    def model_dir(self) -> Path:
        return self.base_dir / "models" / "gguf"

    @property
    def diffusion_model(self) -> Path:
        return self.model_dir / "z_image_turbo-Q8_0.gguf"

    @property
    def vae_model(self) -> Path:
        return self.model_dir / "ae-f16.gguf"

    @property
    def llm_model(self) -> Path:
        return self.model_dir / "qwen_3_4b-Q8_0.gguf"

    @property
    def sd_cpp_paths(self) -> list[Path]:
        return [
            self.base_dir / "stable-diffusion.cpp" / "build" / "bin" / "sd",
            self.base_dir / "stable-diffusion.cpp" / "bin" / "sd",
        ]


@dataclass
class GenerationParams:
    """Image generation parameters"""
    prompt: str
    output: str
    width: int = 512
    height: int = 512
    steps: int = 8
    cfg_scale: float = 1.0
    seed: int | None = None
    negative_prompt: str = ""
    batch_count: int = 1
