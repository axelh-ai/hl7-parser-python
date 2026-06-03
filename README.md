# HL7 ADT^A01 Parser

A Python parser for HL7 v2 ADT messages that extracts 
clinical data into structured Pandas DataFrames.

## What it parses
- MSH — Message header
- PID — Patient demographics (MRN, name, DOB, gender)
- PV1 — Visit info (ward, attending doctor, admission date)
- NK1 — Next of kin
- PD1 — Primary care provider

## Tech stack
- Python 3.11
- pandas
- hl7

## How to run
```bash
conda activate hl7-parser
python hl7_parser.py
```