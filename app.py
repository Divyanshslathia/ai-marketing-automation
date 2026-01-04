from agents.brief_agent import BriefAgent
from agents.copy_agent import CopyAgent
from agents.layout_agent import LayoutAgent
from agents.resize_agent import ResizeAgent
from agents.publisher_agent import PublisherAgent
from services.image_overlay import apply_text_overlay  

def main():
    print("Agent Project-skeleton ready")


    brief_agent = BriefAgent()
    copy_agent = CopyAgent()
    layout_agent = LayoutAgent()
    resize_agent = ResizeAgent()
    publisher_agent = PublisherAgent()
    headline = "Elevate Your Listening Experience"
    tone = "premium" 
    layout = layout_agent.run(headline, tone)
    apply_text_overlay(
        image_path="assets/sample.jpg",
        output_path="outputs/test_overlay.png",
        headline=headline,
        layout=layout,
    )

    print("Image generated: outputs/test_overlay.png")




if __name__ == "__main__":
    main()
