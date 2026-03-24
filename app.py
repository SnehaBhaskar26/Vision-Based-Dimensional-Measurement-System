# import streamlit as st
# import cv2
# import numpy as np
# import pandas as pd
# from ultralytics import YOLO

# # -----------------------------
# # PAGE CONFIG
# # -----------------------------
# st.set_page_config(
#     page_title="Vision Inspection System",
#     layout="wide"
# )

# # -----------------------------
# # CUSTOM CSS
# # -----------------------------
# st.markdown("""
# <style>

# /* Uploader Container */
# div[data-testid="stFileUploader"] {
#     width: 600px !important;
#     margin: auto;
# }

# /* Make internal layout vertical */
# div[data-testid="stFileUploader"] > div {
#     display: flex !important;
#     flex-direction: column !important;
#     align-items: center !important;
#     text-align: center;
# }

# /* Drag text */
# div[data-testid="stFileUploader"] section {
#     text-align: center !important;
# }

# /* Move button BELOW */
# div[data-testid="stFileUploader"] button {
#     margin-top: 10px !important;
#     width: 150px;
# }

# /* Optional styling */
# div[data-testid="stFileUploader"] {
#     background-color: #18202a;
#     border: 2px dashed #00ffcc;
#     border-radius: 12px;
#     padding: 15px;
# }
            


# /* 🔥 Metric Value Bigger */
# div[data-testid="stMetricValue"] {
#     font-size: 25px !important;
#     font-weight: bold;
# }

# /* 🔥 Target (Delta) Bigger */
# div[data-testid="stMetricDelta"] {
#     font-size: 20px !important;
#     font-weight: bold;
#     color: #00ffcc !important;
# }

# /* 🔥 Table Styling */
# .big-table {
#     width: 100%;
#     border-collapse: collapse;
# }
            
# /* Metric Label (Inner_Body, Body, etc.) */
# div[data-testid="stMetricLabel"] {
#     font-size: 60px !important;   /* 🔥 change here */
#     font-weight: 600 !important;
#     font-weight: bold;
#     color: #ffffff !important;
# }

# /* Header */
# .big-table th {
#     font-size: 24px !important;
#     padding: 12px !important;
#     text-align: center !important;
#     background-color: #1c1f26;
# }

# /* Cells */
# .big-table td {
#     font-size: 22px !important;
#     padding: 10px !important;
#     text-align: center !important;
# }
# /* 🔥 Hide uploaded file name + size (FINAL FIX) */
# div[data-testid="stFileUploader"] ul {
#     display: none !important;
# }
# </style>
# """, unsafe_allow_html=True)

# # -----------------------------
# # TITLE
# # -----------------------------
# st.markdown(
#     "<h1 style='text-align: center; font-size: 50px;'>Vision-Based Dimensional Measurement System</h1>",
#     unsafe_allow_html=True
# )

# # -----------------------------
# # LOAD MODEL
# # -----------------------------
# model = YOLO("/home/sneha/projects/POC/poc_det_v3.pt")

# CLASS_SCALES = {
#     "Body": 56 / 600,
#     "Inner_Body": 46 / 500,
#     "Inner_Ring": 12.5 / 166,
#     "Middle_Ring": 25 / 308,
#     "Outer_Ring": 39 / 446
# }

# TARGET_CLASSES = list(CLASS_SCALES.keys())

# ACTUAL_MM = {
#     "Body": 56,
#     "Inner_Body": 46,
#     "Inner_Ring": 12.5,
#     "Middle_Ring": 25,
#     "Outer_Ring": 39,
#     "Neck": 10
# }

# # -----------------------------
# # FUNCTION
# # -----------------------------
# def process_image(img):
#     results = model(img)[0]

#     diameters_px = {}
#     diameters_mm = {}

#     for box in results.boxes:
#         cls_id = int(box.cls[0])
#         class_name = model.names[cls_id]

#         x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())

#         cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
#         cv2.putText(img, class_name, (x1, y1 - 5),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.5,
#                     (255, 255, 255), 2)

#         if class_name in TARGET_CLASSES:
#             px = int(x2 - x1)
#             diameters_px[class_name] = px
#             diameters_mm[class_name] = round(px * CLASS_SCALES[class_name], 2)

#     if "Body" in diameters_px and "Inner_Body" in diameters_px:
#         diameters_px["Neck"] = diameters_px["Body"] - diameters_px["Inner_Body"]
#         diameters_mm["Neck"] = round(
#             diameters_mm["Body"] - diameters_mm["Inner_Body"], 2
#         )

#     return diameters_px, diameters_mm, img


# # -----------------------------
# # UPLOAD
# # -----------------------------
# st.markdown("<p style='text-align:center; font-size:30px; color:#00ffcc; font-weight:bold;'>Upload Image</p>", unsafe_allow_html=True)
# uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"])

# # ✅ SHOW SUCCESS MESSAGE
# if uploaded_file:
#     st.markdown(
#         """
#         <div style='text-align:center; font-size:22px; color:#00ffcc; margin-top:15px; font-weight:bold;'>
#             ✅ File Uploaded Successfully
#         </div>
#         <div style='text-align:center; font-size:35px; color:red;margin-top:15px;font-weight:bold;'>
#             Image ready for inspection
#         </div>
#         """,
#         unsafe_allow_html=True
#     )
# # -----------------------------
# # PROCESS
# # -----------------------------
# if uploaded_file:
#     file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
#     img = cv2.imdecode(file_bytes, 1)

#     original = img.copy()
#     diam_px, diam_mm, output = process_image(img)

#     original = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
#     output = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)

#     # KPI
#     st.markdown(
#         "<h2 style='text-align:left; margin-top:40px;'>📊 Key Measurements</h2>",
#         unsafe_allow_html=True
#     )

#     cols = st.columns(len(diam_mm))
#     for i, key in enumerate(diam_mm):
#         value = diam_mm[key]
#         target = ACTUAL_MM.get(key, "-")
        
#         html_code = f"""
#         <div style="
#             text-align:center; 
#             padding:10px; 
#             background-color:#1c1f26; 
#             border-radius:12px;
#         ">
#             <div style="font-size:25px; font-weight:700; color:white;">{key}</div>
#             <div style="font-size:25px; font-weight:bold; color:white;">{value} mm</div>
#             <div style="font-size:25px; font-weight:bold; color:#00ffcc;">Target: {target} mm</div>
#         </div>
#         """
#         cols[i].markdown(html_code, unsafe_allow_html=True)

#     # Images
#     st.markdown(
#         "<h2 style='text-align:left; margin-top:40px;'>🖼️ Inspection View</h2>",
#         unsafe_allow_html=True
#     )
#     col1, col2 = st.columns(2)
#     col1.image(original, use_container_width=True)
#     col1.markdown("<p style='text-align:center; font-size:24px;'>Original Image</p>", unsafe_allow_html=True)

#     col2.image(output, use_container_width=True)
#     col2.markdown("<p style='text-align:center; font-size:24px;'>Processed Image</p>", unsafe_allow_html=True)

#     # -----------------------------
#     # BIG TABLE
#     # -----------------------------
#      # KPI
#     st.markdown(
#         "<h2 style='text-align:left; margin-top:40px;'>📋 Detailed Measurements</h2>",
#         unsafe_allow_html=True
#     )

  

#     data = []
#     for k in diam_px:
#         data.append([
#             k,
#             diam_px[k],
#             diam_mm[k],
#             ACTUAL_MM.get(k, "-")
#         ])

#     df = pd.DataFrame(data, columns=[
#         "Part Name",
#         "Pixel Distance (px)",
#         "Measured (mm)",
#         "Actual (mm)"
#     ])

#     st.markdown(
#         df.to_html(classes="big-table", index=False),
#         unsafe_allow_html=True
#     )



import streamlit as st
import cv2
import numpy as np
import pandas as pd
from ultralytics import YOLO

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Vision Inspection System",
    layout="wide"
)

# -----------------------------
# CUSTOM CSS
# -----------------------------
st.markdown("""
<style>
/* Uploader Container */
div[data-testid="stFileUploader"] {
    width: 600px !important;
    margin: auto;
    background-color: #18202a;
    border: 2px dashed #00ffcc;
    border-radius: 12px;
    padding: 15px;
}
div[data-testid="stFileUploader"] > div {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    text-align: center;
}
div[data-testid="stFileUploader"] section {
    text-align: center !important;
}
div[data-testid="stFileUploader"] button {
    margin-top: 10px !important;
    width: 150px;
}
div[data-testid="stFileUploader"] ul {
    display: none !important;
}

/* Metric Styling */
div[data-testid="stMetricValue"] {
    font-size: 25px !important;
    font-weight: bold;
}
div[data-testid="stMetricDelta"] {
    font-size: 20px !important;
    font-weight: bold;
    color: #00ffcc !important;
}
div[data-testid="stMetricLabel"] {
    font-size: 60px !important;
    font-weight: bold;
    color: #ffffff !important;
}

/* Table Styling */
.big-table {
    width: 100%;
    border-collapse: collapse;
}
.big-table th {
    font-size: 24px !important;
    padding: 12px !important;
    text-align: center !important;
    background-color: #1c1f26;
    color: white;
}
.big-table td {
    font-size: 22px !important;
    padding: 10px !important;
    text-align: center !important;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# TITLE
# -----------------------------
st.markdown(
    "<h1 style='text-align: center; font-size: 50px;'>Vision-Based Dimensional Measurement System</h1>",
    unsafe_allow_html=True
)

# -----------------------------
# LOAD MODEL
# -----------------------------
model = YOLO("/home/sneha/projects/POC/poc_det_v3.pt")

CLASS_SCALES = {
    "Body": 56 / 600,
    "Inner_Body": 46 / 500,
    "Inner_Ring": 12.5 / 166,
    "Middle_Ring": 25 / 308,
    "Outer_Ring": 39 / 446
}

TARGET_CLASSES = list(CLASS_SCALES.keys())

ACTUAL_MM = {
    "Body": 56,
    "Inner_Body": 46,
    "Inner_Ring": 12.5,
    "Middle_Ring": 25,
    "Outer_Ring": 39,
    "Neck": 10
}

# -----------------------------
# FUNCTION TO PROCESS IMAGE
# -----------------------------
def process_image(img):
    results = model(img)[0]

    diam_px = {}
    diam_mm = {}

    for box in results.boxes:
        cls_id = int(box.cls[0])
        class_name = model.names[cls_id]

        x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(img, class_name, (x1, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (255, 255, 255), 2)

        if class_name in TARGET_CLASSES:
            px = x2 - x1
            diam_px[class_name] = px
            diam_mm[class_name] = round(px * CLASS_SCALES[class_name], 2)

    if "Body" in diam_px and "Inner_Body" in diam_px:
        diam_px["Neck"] = diam_px["Body"] - diam_px["Inner_Body"]
        diam_mm["Neck"] = round(diam_mm["Body"] - diam_mm["Inner_Body"], 2)

    return diam_px, diam_mm, img

# -----------------------------
# UPLOAD IMAGE
# -----------------------------
st.markdown("<p style='text-align:center; font-size:30px; color:#00ffcc; font-weight:bold;'>Upload Image</p>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"])

if uploaded_file:
    st.markdown(
        "<div style='text-align:center; font-size:22px; color:#00ffcc; margin-top:15px; font-weight:bold;'>✅ File Uploaded Successfully</div>"
        "<div style='text-align:center; font-size:35px; color:red; margin-top:15px; font-weight:bold;'>Image ready for inspection</div>",
        unsafe_allow_html=True
    )

# -----------------------------
# PROCESS IMAGE
# -----------------------------
if uploaded_file:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)

    original = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2RGB)
    diam_px, diam_mm, output = process_image(img)
    output = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)

    # -----------------------------
    # KPI METRICS
    # -----------------------------
    st.markdown("<h2 style='text-align:left; margin-top:40px;'>📊 Key Measurements</h2>", unsafe_allow_html=True)
    cols = st.columns(len(diam_mm))
    for i, key in enumerate(diam_mm):
        value = diam_mm[key]
        target = ACTUAL_MM.get(key, "-")
        html_code = f"""
        <div style='text-align:center; padding:10px; background-color:#1c1f26; border-radius:12px;'>
            <div style="font-size:25px; font-weight:700; color:white;">{key}</div>
            <div style="font-size:25px; font-weight:bold; color:white;">{value} mm</div>
            <div style="font-size:25px; font-weight:bold; color:#00ffcc;">Target: {target} mm</div>
        </div>
        """
        cols[i].markdown(html_code, unsafe_allow_html=True)

    # -----------------------------
    # IMAGE DISPLAY
    # -----------------------------
    st.markdown("<h2 style='text-align:left; margin-top:40px;'>🖼️ Inspection View</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    col1.image(original, use_container_width=True)
    col1.markdown("<p style='text-align:center; font-size:24px;'>Original Image</p>", unsafe_allow_html=True)
    col2.image(output, use_container_width=True)
    col2.markdown("<p style='text-align:center; font-size:24px;'>Processed Image</p>", unsafe_allow_html=True)

    # -----------------------------
    # DETAILED TABLE
    # -----------------------------
    st.markdown("<h2 style='text-align:left; margin-top:40px;'>📋 Detailed Measurements</h2>", unsafe_allow_html=True)
    data = [[k, diam_px[k], diam_mm[k], ACTUAL_MM.get(k, "-")] for k in diam_px]
    df = pd.DataFrame(data, columns=["Part Name", "Pixel Distance (px)", "Measured (mm)", "Actual (mm)"])
    st.markdown(df.to_html(classes="big-table", index=False), unsafe_allow_html=True)