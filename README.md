# Z-Image Turbo Generator

RTX 3060 12GB에 최적화된 텍스트-이미지 생성 CLI

## 아키텍처

```
"a beautiful sunset"
        │
        ▼
┌───────────────────┐
│  LLM (Qwen 3 4B)  │  Text Encoder
│  qwen_3_4b-Q8_0   │  프롬프트 → 임베딩
└───────────────────┘
        │
        ▼
┌───────────────────┐
│  Diffusion Model  │  Denoising
│  z_image_turbo    │  노이즈 → Latent
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

## 요구사항

- Python 3.10+
- [stable-diffusion.cpp](https://github.com/leejet/stable-diffusion.cpp) (CUDA 빌드)
- GGUF 모델 파일

## 설치

```bash
# 1. stable-diffusion.cpp 빌드
cd /path/to/Z-Image
git clone --recursive https://github.com/leejet/stable-diffusion.cpp
cd stable-diffusion.cpp
mkdir build && cd build
cmake .. -DSD_CUBLAS=ON
cmake --build . --config Release

# 2. 모델 다운로드
cd ../gencli
bash download_zimage_files.sh
```

## 사용법

```bash
# 기본 사용
python generate_zimage.py "a beautiful sunset"

# 옵션
python generate_zimage.py "cat on the sofa" \
    -W 768 -H 768 \      # 해상도
    --steps 8 \          # 추론 스텝 (4-8)
    --seed 42 \          # 시드
    -n "blurry"          # 네거티브 프롬프트
```

### 옵션

| 옵션 | 설명 | 기본값 |
|------|------|--------|
| `-W`, `--width` | 이미지 너비 | 512 |
| `-H`, `--height` | 이미지 높이 | 512 |
| `-s`, `--steps` | 추론 스텝 | 8 |
| `-g`, `--cfg-scale` | CFG 스케일 | 1.0 |
| `--seed` | 랜덤 시드 | random |
| `-n`, `--negative` | 네거티브 프롬프트 | - |
| `-o`, `--output` | 출력 파일명 | auto |
| `-b`, `--batch` | 배치 수 | 1 |

## 프로젝트 구조

```
gencli/
├── config.py            # 경로 및 파라미터 설정
├── generator.py         # ZImageGenerator 클래스
├── cli.py               # CLI 인터페이스
├── generate_zimage.py   # 진입점
├── download_zimage_files.sh
├── requirements.txt
└── outputs/             # 생성된 이미지
```

## 모델 파일

```
models/gguf/
├── z_image_turbo-Q8_0.gguf   # Diffusion (Q8 양자화)
├── ae-f16.gguf               # VAE (FP16)
└── qwen_3_4b-Q8_0.gguf       # Text Encoder (Q8 양자화)
```

## 성능

| 항목 | 값 |
|------|-----|
| 해상도 | 512x512 |
| 추론 스텝 | 4-8 |
| 생성 시간 | ~2-4초 |
| VRAM 사용 | ~8-10GB |

## 라이선스

Educational and research purposes only.
