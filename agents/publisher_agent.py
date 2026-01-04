import json
import os
from datetime import datetime


class PublisherAgent:
    """
    Final agent responsible for publishing or exporting creatives.
    In MVP mode, this exports assets and logs publish intent.
    """

    def run(
        self,
        creatives: dict,
        captions: dict,
        output_dir: str = "outputs",
    ) -> str:
        os.makedirs(output_dir, exist_ok=True)

        manifest = {
            "status": "exported",
            "timestamp": datetime.utcnow().isoformat(),
            "platforms": {}
        }

        for platform, image_path in creatives.items():
            caption = captions.get(platform)

            manifest["platforms"][platform] = {
                "image": image_path,
                "caption": caption
            }

            print(f"[PublisherAgent] Ready for {platform}")
            print(f"  Image: {image_path}")
            print(f"  Caption: {caption}\n")

        manifest_path = os.path.join(output_dir, "publish_manifest.json")

        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)

        print(f"[PublisherAgent] Export complete → {manifest_path}")

        return manifest_path
