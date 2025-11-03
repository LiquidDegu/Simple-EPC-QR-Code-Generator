# SEPA QR Code Generator (EPC QR) – Windows / macOS / Linux

The SEPA QR Code Generator is a simple desktop application that creates **EPC QR codes** for **SEPA credit transfers**. 
With a clean GUI available in **German and English**, it helps you generate a **SEPA QR Code** (also known as an **EPC QR**) that your banking app can scan to pre‑fill a transfer with **IBAN**, optional **BIC**, amount, and remittance details. 
It supports **ISO 20022 purpose codes**, the **RF structured reference**, and unstructured text, so it’s ideal for use cases like invoices, rent, and donations. 
The app saves QR codes as PNG images and lets you preview the exact EPC payload before you copy or export it, making it a practical **SEPA QR Code generator** for everyday payments on Windows, macOS, and Linux.

> Default language: German (switchable to English in the app)

---

## Features

- EPC QR (SCT) compliant payload (newline-separated, ECC M, UTF-8)
- Version 002 (BIC optional) or 001 (BIC required)
- Required fields: Name, IBAN, Amount
- Optional fields: BIC, Purpose code (4 letters), Structured RF reference or Unstructured text, Additional info
- Language selector: Deutsch / English
- Saved payees: store, load, delete (local only)
- Payload Preview: shows the 12 EPC lines with numbering
- Purpose codes help (ISO 20022 examples)
- PNG export to `~/Documents/EPC_QR/` with smart filenames
- Copy payload to clipboard
- Open output folder button

---

## What You Can Enter

| Field (DE) | Field (EN) | Required | Notes |
|---|---|---|---|
| Name des Zahlungsempfängers | Creditor name | Yes | Max 70 characters |
| IBAN | IBAN | Yes | No spaces; 15–34 characters |
| BIC | BIC | Only if Version = 001 | 8 or 11 alphanumeric |
| Betrag (EUR) | Amount (EUR) | Yes | Dot decimal (e.g., `12.34`), must be > 0 |
| Verwendungszweck (4 Buchstaben) | Purpose (4 letters) | No | ISO 20022 codes (e.g., `CHAR`, `GDDS`, `RENT`, `SALA`) |
| Strukturierte Referenz (RF…) | Structured reference (RF…) | No | ISO 11649; use either this or Unstructured text |
| Unstrukturierter Verwendungszweck | Unstructured text | No | Free text (≈ ≤140 chars). Leave empty if RF used |
| Zusatzinfo | Additional info | No | Optional note (≈ ≤70 chars). Some apps ignore it |
| Version | Version | — | `002` recommended (BIC optional) |
| Zeichensatz | Charset | — | `1 = UTF-8` |

### Purpose Code Examples

`CHAR` (Donation), `GDDS` (Goods/Services), `RENT` (Rent), `SALA` (Salary),  
`PENS` (Pension), `DEPT` (Deposit), `BENE` (Unemployment benefit),  
`MTUP` (Mobile top-up), `TRAD` (Trade)

---

## Saving and Filenames

- All QR images (PNG) are saved to: `~/Documents/EPC_QR/`
- Filename pattern: `"<amount>_<last10_IBAN_digits>_<YYYY-MM-DD>.png"`  
  Example: `12.34_1234567890_2025-11-03.png`

---

## EPC Payload Layout (SCT)

The payload consists of exactly 12 lines:

```
1  BCD
2  002             # or 001
3  1               # UTF-8
4  SCT
5  <BIC or empty>  # empty allowed on 002
6  <Name>
7  <IBAN>
8  <EUR12.34 or empty>
9  <PURPOSE or empty>
10 <RF... or empty>
11 <Unstructured or empty>
12 <Additional info or empty>
```

Use the in-app Payload Preview to see these 12 lines with numbering.

---

## Download

- Windows: Portable `.exe` or installer (see Releases)
- macOS: `.app` (zipped) or `.dmg` (Gatekeeper may require right-click → Open)
- Linux: `tar.gz` folder or AppImage (if provided)

The application runs locally; no data is sent to external services.

---

## Privacy and Safety

- Saved payees (Name, IBAN, BIC) are stored locally in your user profile.
- PNG filenames may include amount and last 10 IBAN digits; consider this before sharing.
- If publishing QR codes publicly, you may omit amount and reference text.

---

## Troubleshooting

- QR won’t scan: Use Payload Preview; ensure each field is on its own line and the BIC line (5) is empty on Version 002 if no BIC.
- Amount invalid: Use dot decimal (`12.34`) and a value greater than zero.
- IBAN invalid: Remove spaces; ensure correct length and format.
- Reference clash: Fill either Structured RF or Unstructured text, not both.
- PNG not saved: Check permissions for `~/Documents/EPC_QR/`.

---

## Licenses

This application bundles third-party components. A small licenses file is included.  
Key components:
- PySide6 / Qt — LGPL-3.0  
- qrcode — BSD-3-Clause  

---

## Keywords

SEPA QR Code, EPC QR, SEPA QR Code Generator, EPC QR Generator, SEPA Credit Transfer QR, SCT QR, IBAN QR Code, BIC QR, RF Reference, ISO 20022 Purpose Code, German Banking QR, Banking QR App, QR Code Zahlung, Spenden QR, Miete QR, Rechnung QR, Zahlungs QR Code, SEPA Überweisung QR, IBAN QR Code Generator, EPC QR PNG, PySide6 Qt QR

---

## Feedback

Found a bug or have a feature request? Please open an issue on the project page.

