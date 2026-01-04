import json
import os
from datetime import datetime
from utils.logger import log


class PublisherAgent:
    """
    Publishes approved content.

    NOTE:
    For this prototype dry run, actual publishing and image uploads
    are intentionally disabled to keep the demo deterministic.
    """

    def run(
        self,
        creatives: dict,
        captions: dict,
        post_to_linkedin: bool = False,
        output_dir: str = "outputs",
    ) -> str:
        os.makedirs(output_dir, exist_ok=True)

        log("PublisherAgent", "Preparing publish manifest (dry run)")

        manifest = {
            "status": "approved",
            "timestamp": datetime.utcnow().isoformat(),
            "linkedin": {
                "local_image": creatives.get("linkedin"),
                "caption": captions.get("linkedin"),
            }
        }

        manifest_path = os.path.join(output_dir, "publish_manifest.json")
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)

        log(
            "PublisherAgent",
            f"Publishing skipped. Manifest written → {manifest_path}"
        )

        return manifest_path
