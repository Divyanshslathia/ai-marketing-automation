import streamlit as st
import tempfile
import time

from agents.copy_agent import CopyAgent
from agents.layout_agent import LayoutAgent
from agents.resize_agent import ResizeAgent
from agents.publisher_agent import PublisherAgent  # kept for intent


st.set_page_config(page_title="AI Marketing Automation", layout="centered")
st.title("AI-First Marketing Automation Prototype")

# ----------------------------
# Step 1: Product Inputs
# ----------------------------

st.header("1. Product Inputs")

uploaded_image = st.file_uploader(
    "Upload product image",
    type=["jpg", "png", "jpeg"]
)

product_name = st.text_input("Product name")
features = st.text_area("Key features (comma-separated)")
tone = st.selectbox(
    "Brand tone",
    ["premium", "playful", "minimal", "luxury"]
)

generate_clicked = st.button("Generate Marketing Creatives")

# ----------------------------
# Step 2: Generate (AI)
# ----------------------------

if generate_clicked:
    if not uploaded_image or not product_name or not features:
        st.error("Please fill all fields and upload an image.")
    else:
        with st.spinner("Running AI pipeline..."):

            # Save uploaded image
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                tmp.write(uploaded_image.read())
                image_path = tmp.name

            inputs = {
                "product_name": product_name,
                "features": [f.strip() for f in features.split(",")],
                "tone": tone,
            }

            # Consolidated AI call (reduced quota usage)
            marketing_data = CopyAgent().run(inputs)

            time.sleep(1)  # gentle throttle

            st.session_state["image_path"] = image_path
            st.session_state["copy"] = marketing_data

# ----------------------------
# Step 3: Review & Approve
# ----------------------------

if "copy" in st.session_state:
    st.divider()
    st.header("2. Review & Approve")

    copy = st.session_state["copy"]

    # Headline selection
    selected_headline = st.radio(
        "Select headline",
        copy.get("headlines", [])
    )

    # --- NEW: captions for all platforms ---
    st.subheader("Captions (Choose one per platform)")

    selected_captions = {}

    captions_by_platform = copy.get("captions", {})

    for platform, options in captions_by_platform.items():
        if not options:
            continue

        selected_captions[platform] = st.radio(
            f"{platform.capitalize()} caption",
            options,
            key=f"caption_{platform}"
        )

    approve_clicked = st.button("Approve & Continue")

    if approve_clicked:
        st.session_state["headline"] = selected_headline
        st.session_state["captions"] = selected_captions
        st.success("Approved. Proceed to creative generation.")

# ----------------------------
# Step 4: Generate Creatives (Dry Run)
# ----------------------------

if "headline" in st.session_state:
    st.divider()
    st.header("3. Generate Creatives (Dry Run)")

    publish_clicked = st.button("Generate Final Images")

    if publish_clicked:
        with st.spinner("Generating platform creatives..."):

            # Layout decision
            layout = LayoutAgent().run(
                st.session_state["headline"],
                tone
            )

            # Generate resized + overlaid images
            creatives = ResizeAgent().run(
                base_image_path=st.session_state["image_path"],
                headline=st.session_state["headline"],
                layout=layout,
            )

            # --- INTENTIONAL, KEPT FOR INTERVIEW ---
            # Publishing intentionally disabled for demo stability
            # PublisherAgent().run(
            #     creatives={"linkedin": creatives.get("linkedin")},
            #     captions={"linkedin": st.session_state["captions"].get("linkedin")},
            #     post_to_linkedin=True
            # )

        st.success(
            "Creatives generated successfully! "
            "Check the /outputs folder for final images."
        )
