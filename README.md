# Z-Image Turbo Generator

Text-to-image generation CLI optimized for RTX 3060 12GB

## Architecture

```
"a beautiful sunset"
        │
        ▼
┌───────────────────┐
│  LLM (Qwen 3 4B)  │  Text Encoder
│  qwen_3_4b-Q8_0   │  Prompt → Embedding
└───────────────────┘
        │
        ▼
┌───────────────────┐
│  Diffusion Model  │  Denoising
│  z_image_turbo    │  Noise → Latent
└───────────────────┘
        │
        ▼
┌───────────────────┐
│   VAE Decoder     │  Decoder
│   ae-f16.gguf     │  Latent → RGB
└───────────────────┘
        │
        ▼
    output.png
```

## Requirements

- Python 3.10+
- [stable-diffusion.cpp](https://github.com/leejet/stable-diffusion.cpp) (CUDA build)
- GGUF model files

## Installation

```bash
# 1. Build stable-diffusion.cpp
cd /path/to/Z-Image
git clone --recursive https://github.com/leejet/stable-diffusion.cpp
cd stable-diffusion.cpp
mkdir build && cd build
cmake .. -DSD_CUBLAS=ON
cmake --build . --config Release

# 2. Download models
cd ../gencli
bash download_zimage_files.sh
```

## Usage

```bash
# Basic usage
python generate_zimage.py "a beautiful sunset"

# With options
python generate_zimage.py "cat on the sofa" \
    -W 768 -H 768 \      # Resolution
    --steps 8 \          # Inference steps (4-8)
    --seed 42 \          # Seed
    -n "blurry"          # Negative prompt
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `-W`, `--width` | Image width | 512 |
| `-H`, `--height` | Image height | 512 |
| `-s`, `--steps` | Inference steps | 8 |
| `-g`, `--cfg-scale` | CFG scale | 1.0 |
| `--seed` | Random seed | random |
| `-n`, `--negative` | Negative prompt | - |
| `-o`, `--output` | Output filename | auto |
| `-b`, `--batch` | Batch count | 1 |

## Project Structure

```
gencli/
├── config.py            # Path and parameter configuration
├── generator.py         # ZImageGenerator class
├── cli.py               # CLI interface
├── generate_zimage.py   # Entry point
├── download_zimage_files.sh
├── requirements.txt
└── outputs/             # Generated images
```

## Model Files

```
models/gguf/
├── z_image_turbo-Q8_0.gguf   # Diffusion (Q8 quantized)
├── ae-f16.gguf               # VAE (FP16)
└── qwen_3_4b-Q8_0.gguf       # Text Encoder (Q8 quantized)
```

## Performance

| Metric | Value |
|--------|-------|
| Resolution | 512x512 |
| Inference steps | 4-8 |
| Generation time | ~2-4s |
| VRAM usage | ~8-10GB |

## License

Educational and research purposes only.
