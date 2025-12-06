#!/bin/bash

# Z-Image Turbo 필수 파일 다운로드 스크립트

MODEL_DIR="/home/beethoven/workspace/deeplearning/deeplearning-project/Z-Image/models/gguf"

echo "======================================================================="
echo "Z-Image Turbo 필수 파일 다운로드"
echo "======================================================================="
echo ""

# Hugging Face 저장소 (wbruna - VAE와 LLM 포함)
REPO="wbruna/Z-Image-Turbo-sdcpp-GGUF"
BASE_URL="https://huggingface.co/$REPO/resolve/main"

echo "다운로드 위치: $MODEL_DIR"
echo ""

# VAE 다운로드 (필수)
echo "[1/2] VAE (ae-f16.gguf) 다운로드 중..."
if [ ! -f "$MODEL_DIR/ae-f16.gguf" ]; then
    wget -c "$BASE_URL/ae-f16.gguf" -O "$MODEL_DIR/ae-f16.gguf"
    echo "✓ VAE 다운로드 완료"
else
    echo "✓ VAE 이미 존재함 ($(ls -lh $MODEL_DIR/ae-f16.gguf | awk '{print $5}'))"
fi
echo ""

# 텍스트 인코더 (LLM) 다운로드 (필수)
echo "[2/2] 텍스트 인코더 (Qwen 3 4B) 다운로드 중..."
if [ ! -f "$MODEL_DIR/qwen_3_4b-Q8_0.gguf" ]; then
    wget -c "$BASE_URL/qwen_3_4b-Q8_0.gguf" -O "$MODEL_DIR/qwen_3_4b-Q8_0.gguf"
    echo "✓ 텍스트 인코더 다운로드 완료"
else
    echo "✓ 텍스트 인코더 이미 존재함 ($(ls -lh $MODEL_DIR/qwen_3_4b-Q8_0.gguf | awk '{print $5}'))"
fi
echo ""

echo "======================================================================="
echo "다운로드 완료!"
echo "======================================================================="
echo ""

# 파일 확인
echo "현재 파일 상태:"
echo "  Diffusion: $(ls -lh $MODEL_DIR/z_image_turbo-Q8_0.gguf 2>/dev/null | awk '{print "("$5")"}' || echo "(없음)")"
echo "  VAE:       $(ls -lh $MODEL_DIR/ae-f16.gguf 2>/dev/null | awk '{print "("$5")"}' || echo "(없음)")"
echo "  LLM:       $(ls -lh $MODEL_DIR/qwen_3_4b-Q8_0.gguf 2>/dev/null | awk '{print "("$5")"}' || echo "(없음)")"
echo ""

if [ -f "$MODEL_DIR/z_image_turbo-Q8_0.gguf" ] && [ -f "$MODEL_DIR/ae-f16.gguf" ] && [ -f "$MODEL_DIR/qwen_3_4b-Q8_0.gguf" ]; then
    echo "✅ 모든 파일 준비 완료!"
    echo ""
    echo "이제 다음 명령어로 이미지 생성:"
    echo "  cd /home/beethoven/workspace/deeplearning/deeplearning-project/Z-Image/gencli"
    echo "  python generate_zimage.py \"The Beautiful girl\" --steps 8"
else
    echo "⚠️  일부 파일이 없습니다. 위의 다운로드를 확인하세요."
fi
echo ""
