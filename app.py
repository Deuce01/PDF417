import streamlit as st
from pdf417gen import encode, render_image
import io
from datetime import datetime

def generate_ca_barcode(data):
    # DL Subfile (Standard Data)
    dl_data = (
        f"DL"
        f"DAQ{data['dl_number']}\n"
        f"DCS{data['last_name']}\n"
        f"DDE{data.get('suffix', 'NONE')}\n"
        f"DAC{data['first_name']}\n"
        f"DDFN\n"
        f"DAD{data.get('middle_name', 'NONE')}\n"
        f"DDGN\n"
        f"DCA{data['class']}\n"
        f"DCB{data.get('restrictions', 'NONE')}\n"
        f"DCD{data.get('endorsements', 'NONE')}\n"
        f"DBD{data['issue_date']}\n"
        f"DBB{data['dob']}\n"
        f"DBA{data['expiry_date']}\n"
        f"DBC{data['sex_code']}\n"
        f"DAU{data['height_in']} IN\n"
        f"DAY{data['eye_color']}\n"
        f"DAG{data['address']}\n"
        f"DAI{data['city']}\n"
        f"DAJCA\n"
        f"DAK{data['zip_code']}\n"
        f"DCF{data['dd_number']}\n"
        f"DCGUSA\n"
        f"DAW{data['weight']}\n"
        f"DAZ{data['hair_color']}\n"
        f"DCK{data['icn']}\n"
        f"DDB{data.get('revision_date', '01012022')}\n"
    )

    # ZC Subfile (California Specific Data)
    zc_data = "ZCDAJCA\n"

    # Calculate Headers & Offsets
    header_len = 39
    
    dl_offset = header_len
    dl_length = len(dl_data)
    
    zc_offset = dl_offset + dl_length
    zc_length = len(zc_data)
    
    # Construct the Header String
    header = (
        "@\n\x1e\rANSI 636014010202"
        f"DL{dl_offset:04d}{dl_length:04d}"
        f"ZC{zc_offset:04d}{zc_length:04d}"
    )
    
    full_payload = header + dl_data + zc_data
    
    codes = encode(full_payload, columns=16, security_level=5)
    img = render_image(codes, scale=2, ratio=3)
    
    img_buffer = io.BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    return img_buffer

st.title("CA Driver's License Barcode Generator")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Personal Information")
    dl_number = st.text_input("DL Number", "Z4830439")
    first_name = st.text_input("First Name", "WES")
    last_name = st.text_input("Last Name", "MCCORMACK")
    middle_name = st.text_input("Middle Name (optional)", "")
    suffix = st.text_input("Suffix (optional)", "")
    
    st.subheader("Physical Details")
    sex = st.selectbox("Sex", ["M", "F"])
    sex_code = "1" if sex == "M" else "2"
    height_ft = st.number_input("Height (feet)", min_value=3, max_value=8, value=5)
    height_in = st.number_input("Height (inches)", min_value=0, max_value=11, value=9)
    height_total = f"{height_ft * 12 + height_in:03d}"
    weight = st.number_input("Weight (lbs)", min_value=50, max_value=500, value=169)
    eye_color = st.selectbox("Eye Color", ["BRO", "BLU", "GRN", "HAZ", "GRY", "BLK"])
    hair_color = st.selectbox("Hair Color", ["BLK", "BRO", "BLD", "GRY", "RED", "WHI"])

with col2:
    st.subheader("Address")
    address = st.text_input("Street Address", "1523 NOB HILL DR")
    city = st.text_input("City", "ESCONDIDO")
    zip_code = st.text_input("ZIP Code", "92026")
    
    st.subheader("License Details")
    license_class = st.selectbox("Class", ["C", "A", "B", "M"])
    restrictions = st.text_input("Restrictions (optional)", "")
    endorsements = st.text_input("Endorsements (optional)", "")
    
    st.subheader("Dates")
    dob = st.date_input("Date of Birth", datetime(1986, 5, 20))
    issue_date = st.date_input("Issue Date", datetime(2022, 8, 14))
    expiry_date = st.date_input("Expiry Date", datetime(2027, 5, 20))
    
    st.subheader("System Fields")
    dd_number = st.text_input("DD Number", "08/14/202200270/AAFD/27")
    icn = st.text_input("ICN", "22226Z48304390401")

if st.button("Generate Barcode", type="primary"):
    data = {
        "dl_number": dl_number,
        "first_name": first_name.upper(),
        "last_name": last_name.upper(),
        "middle_name": middle_name.upper() if middle_name else "NONE",
        "suffix": suffix.upper() if suffix else "NONE",
        "address": address.upper(),
        "city": city.upper(),
        "zip_code": zip_code,
        "class": license_class,
        "sex_code": sex_code,
        "dob": dob.strftime("%m%d%Y"),
        "issue_date": issue_date.strftime("%m%d%Y"),
        "expiry_date": expiry_date.strftime("%m%d%Y"),
        "dd_number": dd_number,
        "icn": icn,
        "height_in": height_total,
        "weight": str(weight),
        "eye_color": eye_color,
        "hair_color": hair_color,
        "restrictions": restrictions.upper() if restrictions else "NONE",
        "endorsements": endorsements.upper() if endorsements else "NONE"
    }
    
    try:
        img_buffer = generate_ca_barcode(data)
        st.success("Barcode generated successfully!")
        st.image(img_buffer, caption="CA Driver's License Barcode")
        st.download_button(
            label="Download Barcode",
            data=img_buffer,
            file_name="ca_license_barcode.png",
            mime="image/png"
        )
    except Exception as e:
        st.error(f"Error generating barcode: {str(e)}")