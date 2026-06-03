import hl7
import pandas as pd

# A sample HL7 ADT^A01 message (Patient Admission)
message = (
    'MSH|^~\\&|EPIC|HOSPITAL|RECEIVING|CLIENT|20240101120000||ADT^A01|MSG001|P|2.5\r'
    'PID|1||MRN123456^^^HOSPITAL^MR||DOE^JOHN^A||19800515|M|||123 MAIN ST^^NEW YORK^NY^10001||555-1234|||S\r'
    'PV1|1|I|WARD3^301^A^^^HOSPITAL||||DR456^SMITH^JAMES^DR|||MED||||ADM|||||VIS789|||||||||||||||||20240101110000\r'
    'NK1|1|DOE^JANE^|SPO|555-5678\r'
    'PD1|||CLINIC123^PRIMARY CARE CLINIC|DR789^JONES^MARY^DR\r'
)

# =============================================
# WAY 1 — Try/Except (most common in industry)
# Pros: simple, readable, handles any missing field
# Cons: hides errors silently if you are not careful
# =============================================
def get_field_try(segment, field_index, component_index=0, default=''):
    try:
        return str(segment[field_index][component_index])
    except (IndexError, KeyError):
        return default

# =============================================
# WAY 2 — Check length before accessing
# Pros: explicit, you know exactly why it failed
# Cons: more verbose, easy to forget a check
# =============================================
def get_field_check(segment, field_index, component_index=0, default=''):
    if field_index < len(segment):
        field = segment[field_index]
        if component_index < len(field):
            return str(field[component_index])
    return default

# Parse the message
parsed = hl7.parse(message)

pid = parsed['PID'][0]
pv1 = parsed['PV1'][0]
nk1 = parsed['NK1'][0]
pd1 = parsed['PD1'][0]

# Using Way 1 (try/except) — this is what most production code uses
data = {
    'mrn':              get_field_try(pid, 3,  0),
    'patient_name':     get_field_try(pid, 5,  0),
    'date_of_birth':    get_field_try(pid, 7,  0),
    'gender':           get_field_try(pid, 8,  0),
    'address':          get_field_try(pid, 11, 0),
    'phone':            get_field_try(pid, 13, 0),
    'visit_type':       get_field_try(pv1, 2,  0),
    'ward':             get_field_try(pv1, 3,  0),
    'attending_dr':     get_field_try(pv1, 7,  0),
    'admission_date':   get_field_try(pv1, 44, 0),
    'next_of_kin':      get_field_try(nk1, 2,  0),
    'nok_relationship': get_field_try(nk1, 3,  0),
    'pcp_clinic':       get_field_try(pd1, 3,  0),
    'pcp_doctor':       get_field_try(pd1, 4,  0),
}

# Load into Pandas DataFrame
df = pd.DataFrame([data])

# Print result
print("=== HL7 ADT^A01 Parsed Output ===")
print(df.to_string(index=False))

# Save to CSV
df.to_csv('parsed_hl7_output.csv', index=False)
print("\nSaved to parsed_hl7_output.csv")