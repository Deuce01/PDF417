from pdf417gen import encode, render_image

def generate_dynamic_ca_barcode(data):
    # --- STEP 1: PREPARE DATA SUBFILES ---
    
    # DL Subfile (Standard Data)
    # Note: We use \n as the terminator for each field.
    dl_data = (
        f"DL" # Subfile Type
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
    # ZC often contains the digital signature or internal pointers
    zc_data = "ZCDAJCA\n"

    # --- STEP 2: CALCULATE HEADERS & OFFSETS ---
    
    # The AAMVA header is fixed length:
    # Header Identifier: 19 bytes ("@\n\x1e\rANSI 6360140100")
    # DL Pointer: 10 bytes ("DL" + 4 offset + 4 length)
    # ZC Pointer: 10 bytes ("ZC" + 4 offset + 4 length)
    # Total Header Length = 19 + 10 + 10 = 39 bytes (assuming 2 subfiles)
    
    header_len = 39
    
    # Calculate Offsets
    # DL starts immediately after the header
    dl_offset = header_len
    dl_length = len(dl_data)
    
    # ZC starts immediately after DL
    zc_offset = dl_offset + dl_length
    zc_length = len(zc_data)
    
    # Construct the Header String
    # 0102 below = AAMVA Version 01, Jurisdiction Version 02 (Common for CA)
    # %04d formats the number to 4 digits (e.g. 41 -> 0041)
    header = (
        "@\n\x1e\rANSI 636014010202"  # Magic word + IIN + Vers + Number of Subfiles (02)
        f"DL{dl_offset:04d}{dl_length:04d}"
        f"ZC{zc_offset:04d}{zc_length:04d}"
    )
    
    full_payload = header + dl_data + zc_data

    # --- STEP 3: RENDER WITH DIMENSION CONTROL ---
    
    # COLUMNS: Controls the aspect ratio.
    # 9 columns = Tall/Narrow
    # 16 columns = Short/Wide (Matches your image)
    # Security Level 5 is MANDATORY for ID cards.
    codes = encode(full_payload, columns=16, security_level=5)
    
    # SCALE: Controls pixel density (dots per module).
    # RATIO: Controls the height of rows. 
    # Standard PDF417 row height is 3x to 5x the width (ratio=3).
    img = render_image(codes, scale=2, ratio=3) 
    
    img.save("ca_compliant_barcode.png")
    print(f"Barcode Generated.")
    print(f"Total Bytes: {len(full_payload)}")
    print(f"DL Offset: {dl_offset}, Length: {dl_length}")

# Use the data from your previous upload
user_data = {
    "dl_number": "Z4830439",
    "first_name": "WES",
    "last_name": "MCCORMACK",
    "address": "1523 NOB HILL DR",
    "city": "ESCONDIDO",
    "zip_code": "92026",
    "class": "C",
    "sex_code": "1",
    "dob": "05201986",
    "issue_date": "08142022",
    "expiry_date": "05202027",
    "dd_number": "08/14/202200270/AAFD/27", 
    "icn": "22226Z48304390401",
    "height_in": "069",
    "weight": "169",
    "eye_color": "BRO",
    "hair_color": "BLK",
}

generate_dynamic_ca_barcode(user_data)