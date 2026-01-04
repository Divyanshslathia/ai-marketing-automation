import streamlit as st
import tempfile
from datetime import datetime
import time

# Note: BriefAgent is removed as it is now consolidated into CopyAgent
from agents.copy_agent import CopyAgent
from agents.layout_agent import LayoutAgent
from agents.resize_agent import ResizeAgent
from agents.publisher_agent import PublisherAgent


st.set_page_config(page_title="AI Marketing Automation", layout="centered")

st.title("AI-First Marketing Automation Prototype")

# ----------------------------
# Step 1: User Inputs
# ----------------------------

st.header("1. Product Inputs")

uploaded_image = st.file_uploader("Upload product image", type=["jpg", "png", "jpeg"])

product_name = st.text_input("Product name")
features = st.text_area("Key features (comma-separated)")
tone = st.selectbox("Brand tone", ["premium", "playful", "minimal", "luxury"])

generate_clicked = st.button("Generate Marketing Creatives")

# ----------------------------
# Step 2: Generate
# ----------------------------

if generate_clicked:
    if not uploaded_image or not product_name or not features:
        st.error("Please fill all fields and upload an image.")
    else:
        with st.spinner("Running AI pipeline..."):

            # Save uploaded image to temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                tmp.write(uploaded_image.read())
                image_path = tmp.name

            inputs = {
                "product_name": product_name,
                "features": [f.strip() for f in features.split(",")],
                "tone": tone,
            }

            # Run consolidated agent to get both brief and copy in one call
            # This saves API quota and reduces latency
            marketing_data = CopyAgent().run(inputs)
            
            # Artificial delay to prevent rapid-fire API hits
            time.sleep(1)

            st.session_state["image_path"] = image_path
            st.session_state["brief"] = marketing_data.get("brief", {})
            st.session_state["copy"] = marketing_data  # Contains headlines and captions

# ----------------------------
# Step 3: Review & Approval
# ----------------------------

if "copy" in st.session_state:
    st.divider()
    st.header("2. Review & Approve")
    
    # Display brief for context
    if "brief" in st.session_state:
        with st.expander("View Campaign Strategy"):
            st.write(f"**Target Audience:** {st.session_state['brief'].get('target_audience')}")
            st.write(f"**Value Prop:** {st.session_state['brief'].get('key_value_prop')}")

    copy = st.session_state["copy"]

    selected_headline = st.radio(
        "Select headline",
        copy.get("headlines", ["Error: No headlines generated"])
    )

    st.subheader("Captions")

    selected_captions = {}
    # Use .get() to avoid KeyErrors if the AI response is malformed
    for platform, options in copy.get("captions", {}).items():
        selected_captions[platform] = st.radio(
            f"{platform.capitalize()} caption",
            options,
            key=platform
        )

    approve = st.button("Approve & Continue")

    if approve:
        st.session_state["headline"] = selected_headline
        st.session_state["captions"] = selected_captions
        st.success("Approved! Proceed to Publish step below.")

# ----------------------------
# Step 4: Publish Options
# ----------------------------

if "headline" in st.session_state:
    st.divider()
    st.header("3. Publish")

    publish_mode = st.radio(
        "When do you want to publish?",
        ["Publish now", "Schedule for later"]
    )

    scheduled_time = None
    if publish_mode == "Schedule for later":
        scheduled_time = st.datetime_input("Select date & time")

    publish_clicked = st.button("Publish")

    if publish_clicked:
        with st.spinner("Generating creatives and publishing..."):

            # Step 4a: Decide layout rules based on chosen headline
            layout = LayoutAgent().run(
                st.session_state["headline"],
                tone
            )

            # Step 4b: Create the visual assets
            creatives = ResizeAgent().run(
                base_image_path=st.session_state["image_path"],
                headline=st.session_state["headline"],
                layout=layout,
            )

            # Step 4c: Post/Export
            PublisherAgent().run(
                creatives=creatives,
                captions=st.session_state["captions"]
            )

        if publish_mode == "Publish now":
            st.success("Published successfully! Assets exported to /outputs.")
        else:
            st.success(f"Scheduled for {scheduled_time}")