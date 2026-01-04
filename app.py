from agents.copy_agent import CopyAgent
from agents.layout_agent import LayoutAgent
from agents.resize_agent import ResizeAgent
from agents.publisher_agent import PublisherAgent

def main():
    print("Running full marketing pipeline (Consolidated Flow)...\n")

    inputs = {
        "product_name": "Aura Wireless Headphones",
        "features": [
            "Active noise cancellation",
            "40-hour battery life",
            "Premium aluminum build"
        ],
        "tone": "premium"
    }

    # 1. Generate Strategy & Copy (Consolidated Brief + Copy)
    # The new CopyAgent now returns both the 'brief' and 'copy' content in one call
    copy_agent = CopyAgent()
    marketing_data = copy_agent.run(inputs)

    # Extracting the headline and captions from the consolidated response
    headline = marketing_data["headlines"][0]
    
    # Mapping captions correctly from the new JSON structure
    captions = {
        "linkedin": marketing_data["captions"]["linkedin"][0],
        "instagram_post": marketing_data["captions"]["instagram"][0],
        "instagram_story": marketing_data["captions"]["instagram"][1] if len(marketing_data["captions"]["instagram"]) > 1 else marketing_data["captions"]["instagram"][0],
    }

    print(f"[System] Strategy Generated: {marketing_data['brief']['key_value_prop']}")
    print(f"[System] Selected Headline: {headline}\n")

    # 2. Layout (Decide where text goes)
    layout_agent = LayoutAgent()
    layout = layout_agent.run(headline, inputs["tone"])

    # 3. Resize / Creatives (Image processing)
    # Ensure assets/sample.jpg exists in your directory
    resize_agent = ResizeAgent()
    creatives = resize_agent.run(
        base_image_path="assets/sample.jpg",
        headline=headline,
        layout=layout,
    )

    # 4. Publish (Export manifest)
    publisher = PublisherAgent()
    publisher.run(creatives, captions)

if __name__ == "__main__":
    main()