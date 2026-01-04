import os
from PIL import Image
from services.image_overlay import apply_text_overlay
from config import PLATFORM_SIZES
from utils.logger import log


class ResizeAgent:
    """
    Generates platform-specific creatives.
    """

    def run(
        self,
        base_image_path: str,
        headline: str,
        layout: dict,
        output_dir: str = "outputs",
    ) -> dict:
        os.makedirs(output_dir, exist_ok=True)
        results = {}

        log(
            "ResizeAgent",
            f"Starting creative generation for headline: '{headline}'"
        )

        base_img = Image.open(base_image_path)

        for platform, size in PLATFORM_SIZES.items():
            log(
                "ResizeAgent",
                f"Resizing image for platform='{platform}' size={size}"
            )

            resized = base_img.resize(size, Image.LANCZOS)

            final_img = apply_text_overlay(
                img=resized,
                headline=headline,
                layout=layout,
            )

            output_path = os.path.join(output_dir, f"{platform}.png")
            final_img.save(output_path, format="PNG")

            results[platform] = output_path

            log(
                "ResizeAgent",
                f"Creative generated → {output_path}"
            )

        log("ResizeAgent", "All platform creatives generated")

        return results
