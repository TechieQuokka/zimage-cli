"""Z-Image CLI interface"""

import argparse
import random
import time
from pathlib import Path

from config import GenerationParams
from generator import ZImageGenerator


class CLI:
    """Command-line interface for Z-Image generator"""

    def __init__(self):
        self.generator = ZImageGenerator()
        self.output_dir = Path("outputs")

    def parse_args(self) -> argparse.Namespace:
        """Parse command-line arguments"""
        parser = argparse.ArgumentParser(
            description="Z-Image Turbo Generator",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  python generate_zimage.py "a beautiful sunset"
  python generate_zimage.py "cat" -W 768 -H 768 --steps 8
  python generate_zimage.py "forest" --seed 42 -o forest.png
  python generate_zimage.py "city" -n "blurry, low quality"
""")

        parser.add_argument("prompt", help="Text description of image")
        parser.add_argument("-o", "--output", help="Output filename")
        parser.add_argument("-W", "--width", type=int, default=512)
        parser.add_argument("-H", "--height", type=int, default=512)
        parser.add_argument("-s", "--steps", type=int, default=8, help="Inference steps (4-8)")
        parser.add_argument("-g", "--cfg-scale", type=float, default=1.0)
        parser.add_argument("--seed", type=int, help="Random seed")
        parser.add_argument("-n", "--negative", default="", help="Negative prompt")
        parser.add_argument("-b", "--batch", type=int, default=1, help="Batch count")
        parser.add_argument("-c", "--count", type=int, default=1, help="Generate multiple images with different seeds")

        return parser.parse_args()

    def generate_output_path(self, prompt: str, batch: int, index: int | None = None) -> str:
        """Generate output file path from prompt

        Args:
            prompt: Text prompt
            batch: Batch count (for sd.cpp internal batching)
            index: Image index for --count option (1-based)
        """
        self.output_dir.mkdir(exist_ok=True)

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        safe_prompt = "".join(c if c.isalnum() else "_" for c in prompt[:30])

        if batch > 1:
            filename = f"zimage_{safe_prompt}_%d_{timestamp}.png"
        elif index is not None:
            filename = f"zimage_{safe_prompt}_{index:03d}_{timestamp}.png"
        else:
            filename = f"zimage_{safe_prompt}_{timestamp}.png"

        return str(self.output_dir / filename)

    def print_header(self, params: GenerationParams, current: int | None = None, total: int | None = None):
        """Print generation configuration header"""
        print("=" * 60)
        if current is not None and total is not None:
            print(f"Z-Image Turbo Generator [{current}/{total}]")
        else:
            print("Z-Image Turbo Generator")
        print("=" * 60)
        print(f"Prompt:    {params.prompt}")
        print(f"Size:      {params.width}x{params.height}")
        print(f"Steps:     {params.steps}")
        print(f"CFG Scale: {params.cfg_scale}")
        print(f"Seed:      {params.seed}")
        if params.negative_prompt:
            print(f"Negative:  {params.negative_prompt}")
        if params.batch_count > 1:
            print(f"Batch:     {params.batch_count}")
        print(f"Output:    {params.output}")
        print("=" * 60)

    def run(self) -> int:
        """Run CLI. Returns exit code."""
        args = self.parse_args()
        count = args.count
        success_count = 0

        for i in range(count):
            # Generate unique seed for each iteration
            seed = args.seed if args.seed is not None else random.randint(1, 2**31 - 1)
            # If user provided seed and count > 1, increment seed for each image
            if args.seed is not None and count > 1:
                seed = args.seed + i

            # Generate unique output path for each image
            if args.output:
                output = args.output if count == 1 else f"{Path(args.output).stem}_{i+1:03d}{Path(args.output).suffix}"
            else:
                index = i + 1 if count > 1 else None
                output = self.generate_output_path(args.prompt, args.batch, index)

            params = GenerationParams(
                prompt=args.prompt,
                output=output,
                width=args.width,
                height=args.height,
                steps=args.steps,
                cfg_scale=args.cfg_scale,
                seed=seed,
                negative_prompt=args.negative,
                batch_count=args.batch,
            )

            if count > 1:
                self.print_header(params, i + 1, count)
            else:
                self.print_header(params)

            if self.generator.generate(params):
                success_count += 1

        if count > 1:
            print(f"\n{'='*60}")
            print(f"Completed: {success_count}/{count} images generated")
            print(f"{'='*60}")

        return 0 if success_count == count else 1
