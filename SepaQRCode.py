# EPC (SEPA) QR Code Generator – Windows GUI with Help, Saved Payees & i18n (DE default)
# Requirements (install in CMD / PowerShell):
#   pip install PySide6 qrcode[pil]
# Run: python SepaQRCode.py

from PySide6.QtWidgets import (
    QApplication, QWidget, QFormLayout, QLineEdit, QHBoxLayout,
    QPushButton, QFileDialog, QMessageBox, QComboBox, QLabel, QVBoxLayout
)
from PySide6.QtCore import Qt
from datetime import datetime
from pathlib import Path
from typing import Optional
import sys
import re
import json
import os
import qrcode

APP_STATE = Path.home() / ".epc_qr_payees.json"
BASE_OUT = Path.home() / "Documents" / "EPC_QR"  # default output folder for PNGs

# ------------------ i18n dictionaries ------------------
I18N = {
    "de": {
        "app_title": "EPC (SEPA) QR Generator",
        "lang_label": "Sprache",
        "saved_payees": "Gespeicherte Empfänger",
        "btn_load": "Laden",
        "btn_save": "Speichern/Aktualisieren",
        "btn_delete": "Löschen",
        "lbl_name": "Name des Zahlungsempfängers *",
        "lbl_iban": "IBAN *",
        "lbl_bic": "BIC (optional in v002)",
        "lbl_amount": "Betrag (EUR) *",
        "lbl_purpose": "Verwendungszweck (optional, 4 Buchstaben)",
        "lbl_structured": "Strukturierte Referenz (RF…)",
        "lbl_unstructured": "Unstrukturierter Verwendungszweck",
        "lbl_info": "Zusatzinformation (optional)",
        "lbl_version": "Version",
        "lbl_charset": "Zeichensatz",
        "btn_save_png": "PNG speichern",
        "btn_preview_payload": "Payload anzeigen",
        "btn_copy_payload": "Payload kopieren",
        "btn_open_folder": "Ordner öffnen",
        "legend_required": "* Pflichtfelder",
        "ph_name": "z. B. Fabian Hiller",
        "ph_iban": "DE.. (ohne Leerzeichen)",
        "ph_bic": "z. B. DEUTDEFF (optional in v002)",
        "ph_amount": "10.00",
        "ph_purpose": "CHAR / GDDS / RENT…",
        "ph_structured": "RF… strukturierte Referenz (ISO 11649)",
        "ph_unstructured": "Freitext (≤140 Zeichen)",
        "ph_info": "Zusatzinfo (≤70 Zeichen)",
        "tt_name": "(Pflicht) Name des Zahlungsempfängers – max. 70 Zeichen.",
        "tt_iban": "(Pflicht) IBAN ohne Leerzeichen, 15–34 Zeichen.",
        "tt_bic": "BIC (8 oder 11 alphanumerisch). Nur für Version 001 erforderlich.",
        "tt_amount": "(Pflicht) Punkt als Dezimaltrennzeichen (z. B. 12.34). Muss > 0 sein.",
        "tt_purpose": "Optionaler ISO‑20022‑Code (4 Buchstaben). ? für Beispiele klicken.",
        "tt_structured": "Strukturierte Referenz (beginnt mit RF). Freitext leer lassen, wenn genutzt.",
        "tt_unstructured": "Freitext‑Alternative zur strukturierten Referenz. Max. ~140 Zeichen.",
        "tt_info": "Optionale Notiz an den Empfänger. Max. ~70 Zeichen.",
        "tt_version": "002 empfohlen (BIC optional). 001 erfordert BIC.",
        "tt_charset": "1 = UTF‑8 (empfohlen).",
        "dlg_validation": "Validierung",
        "err_name_req": "Name des Zahlungsempfängers ist erforderlich.",
        "err_iban_req": "IBAN ist erforderlich.",
        "err_iban_fmt": "IBAN-Format scheint ungültig.",
        "err_bic_req": "Version 001 erfordert eine BIC. Verwenden Sie 002 oder geben Sie eine BIC ein.",
        "err_amount_req": "Betrag ist erforderlich.",
        "err_amount_pos": "Betrag muss eine positive Zahl sein (z. B. 10 oder 10.00).",
        "err_purpose_fmt": "Verwendungszweck muss genau 4 Buchstaben haben (z. B. CHAR).",
        "err_name_len": "Name des Zahlungsempfängers darf höchstens 70 Zeichen haben.",
        "err_bic_fmt": "BIC muss 8 oder 11 alphanumerische Zeichen haben.",
        "err_text_len": "Unstrukturierter Verwendungszweck muss ≤ 140 Zeichen sein.",
        "err_info_len": "Zusatzinformation muss ≤ 70 Zeichen sein.",
        "qr_error": "QR-Fehler",
        "folder_error": "Ordnerfehler",
        "msg_folder_err": "Ordner konnte nicht erstellt werden:\n{path}\n{err}",
        "saved": "Gespeichert",
        "msg_saved_qr": "QR wurde gespeichert unter:\n{path}",
        "save_error": "Speicherfehler",
        "copied": "Kopiert",
        "msg_copied": "EPC-Payload in die Zwischenablage kopiert.",
        "open_folder_error": "Ordner öffnen",
        "msg_open_folder_err": "Ordner konnte nicht geöffnet werden:\n{path}\n{err}",
        "payload_preview": "EPC-Payload-Vorschau",
        "payload_length": "(Länge = {n} Zeichen)",
        "purpose_help_title": "Verwendungszweck-Codes",
        "purpose_help": (
            "Verwendungszweck (optional, 4 Buchstaben) klassifiziert die Zahlung.\n"
            "Er verwendet ISO 20022 Codes. Beispiele:\n\n"
            "  CHAR = Spende\n"
            "  GDDS = Waren/Dienstleistungen\n"
            "  RENT = Miete\n"
            "  SALA = Gehalt\n"
            "  PENS = Rente\n"
            "  DEPT = Einzahlung\n"
            "  BENE = Arbeitslosenunterstützung\n"
            "  MTUP = Handyaufladung\n"
            "  TRAD = Handel\n\n"
            "Leer lassen, wenn nicht benötigt. Viele Banking-Apps ignorieren es."
        ),
    },
    "en": {
        "app_title": "EPC (SEPA) QR Generator",
        "lang_label": "Language",
        "saved_payees": "Saved payees",
        "btn_load": "Load",
        "btn_save": "Save/Update",
        "btn_delete": "Delete",
        "lbl_name": "Creditor name *",
        "lbl_iban": "IBAN *",
        "lbl_bic": "BIC (optional in v002)",
        "lbl_amount": "Amount (EUR) *",
        "lbl_purpose": "Purpose (opt., 4 letters)",
        "lbl_structured": "Structured ref (RF…)",
        "lbl_unstructured": "Unstructured text",
        "lbl_info": "Additional info (opt.)",
        "lbl_version": "Version",
        "lbl_charset": "Charset",
        "btn_save_png": "Save PNG",
        "btn_preview_payload": "Preview Payload",
        "btn_copy_payload": "Copy Payload",
        "btn_open_folder": "Open Folder",
        "legend_required": "* Required fields",
        "ph_name": "e.g. Fabian Hiller",
        "ph_iban": "DE.. (no spaces)",
        "ph_bic": "e.g. DEUTDEFF (optional in v002)",
        "ph_amount": "10.00",
        "ph_purpose": "CHAR / GDDS / RENT…",
        "ph_structured": "RF… structured reference (ISO 11649)",
        "ph_unstructured": "Unstructured remittance text (≤140 chars)",
        "ph_info": "Additional info (≤70 chars)",
        "tt_name": "(Required) Payee (creditor) name – max 70 characters.",
        "tt_iban": "(Required) IBAN without spaces, 15–34 characters.",
        "tt_bic": "BIC (8 or 11 alphanumeric). Required only for Version 001.",
        "tt_amount": "(Required) Use dot as decimal separator (e.g., 12.34). Must be > 0.",
        "tt_purpose": "Optional 4-letter ISO 20022 purpose code. Click ? for examples.",
        "tt_structured": "Structured reference (starts with RF). Leave Unstructured text empty if you use this.",
        "tt_unstructured": "Free text alternative to structured reference. Max ~140 characters.",
        "tt_info": "Optional note to the recipient. Max ~70 characters.",
        "tt_version": "002 recommended (BIC optional). 001 requires BIC.",
        "tt_charset": "1 = UTF‑8 (recommended).",
        "dlg_validation": "Validation",
        "err_name_req": "Creditor name is required.",
        "err_iban_req": "IBAN is required.",
        "err_iban_fmt": "IBAN format looks invalid.",
        "err_bic_req": "Version 001 requires a BIC. Use 002 or enter a BIC.",
        "err_amount_req": "Amount is required.",
        "err_amount_pos": "Amount must be a positive number (e.g., 10 or 10.00).",
        "err_purpose_fmt": "Purpose must be exactly 4 letters (e.g., CHAR).",
        "err_name_len": "Creditor name must be at most 70 characters.",
        "err_bic_fmt": "BIC must be 8 or 11 alphanumeric characters.",
        "err_text_len": "Unstructured text must be ≤ 140 characters.",
        "err_info_len": "Additional info must be ≤ 70 characters.",
        "qr_error": "QR error",
        "folder_error": "Folder error",
        "msg_folder_err": "Could not create folder:\n{path}\n{err}",
        "saved": "Saved",
        "msg_saved_qr": "Saved QR to:\n{path}",
        "save_error": "Save error",
        "copied": "Copied",
        "msg_copied": "EPC payload copied to clipboard.",
        "open_folder_error": "Open Folder",
        "msg_open_folder_err": "Could not open folder:\n{path}\n{err}",
        "payload_preview": "EPC Payload Preview",
        "payload_length": "(len = {n} chars)",
        "purpose_help_title": "Purpose codes",
        "purpose_help": (
            "Purpose (optional, 4 letters) tells banks why the payment is made.\n"
            "It uses ISO 20022 purpose codes. Examples:\n\n"
            "  CHAR = Donation\n"
            "  GDDS = Goods/Services\n"
            "  RENT = Rent\n"
            "  SALA = Salary\n"
            "  PENS = Pension\n"
            "  DEPT = Deposit\n"
            "  BENE = Unemployment benefit\n"
            "  MTUP = Mobile top-up\n"
            "  TRAD = Trade\n\n"
            "Leave empty if you don't need it. Many banking apps ignore it."
        ),
    },
}

# ------------------ EPC payload builder ------------------
def build_epc_payload(
    name: str,
    iban: str,
    amount_eur: Optional[str],
    bic: Optional[str],
    purpose_code: Optional[str],
    remittance_ref: Optional[str],
    remittance_text: Optional[str],
    info: Optional[str],
    version: str = "002",
    charset: str = "1",
) -> str:
    def v(x):
        return "" if x is None else str(x)

    amt = ""
    if amount_eur:
        try:
            val = round(float(str(amount_eur).replace(",", ".")), 2)
            if val <= 0:
                raise ValueError
            amt = f"EUR{val:.2f}"
        except Exception:
            raise ValueError("Amount must be a positive number (e.g., 10.00)")

    ref = (remittance_ref or "").strip()
    txt = (remittance_text or "").strip()
    if ref and txt:
        txt = ""

    lines = [
        "BCD",
        version,
        charset,
        "SCT",
        v((bic or "").upper()),
        v(name).strip(),
        v(iban).replace(" ", "").upper(),
        amt,
        v((purpose_code or "").upper()),
        ref,
        txt,
        v(info),
    ]
    return "\n".join(lines)

# ------------------ Saved Payees ------------------
class PayeeStore:
    def __init__(self, path: Path):
        self.path = path
        self.data = {"payees": []}
        self.load()

    def load(self):
        try:
            if self.path.exists():
                self.data = json.loads(self.path.read_text(encoding="utf-8"))
            else:
                self.save()
        except Exception:
            self.data = {"payees": []}

    def save(self):
        try:
            self.path.write_text(
                json.dumps(self.data, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
        except Exception as e:
            QMessageBox.warning(
                None, "Save error",
                f"Could not save payees to {self.path}:\n{e}"
            )

    def list_names(self):
        return [p.get("name", "") for p in self.data.get("payees", [])]

    def get(self, name: str):
        for p in self.data.get("payees", []):
            if p.get("name", "") == name:
                return p
        return None

    def upsert(self, payee: dict):
        existing = self.get(payee.get("name", ""))
        if existing is not None:
            existing.update(payee)
        else:
            self.data.setdefault("payees", []).append(payee)
        self.save()

    def delete(self, name: str):
        self.data["payees"] = [
            p for p in self.data.get("payees", []) if p.get("name", "") != name
        ]
        self.save()

# ------------------ GUI ------------------
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.lang = "de"  # default language
        self.t = I18N[self.lang]
        self.setWindowTitle(self.t["app_title"])
        self.setMinimumWidth(640)

        self.store = PayeeStore(APP_STATE)

        layout = QVBoxLayout(self)

        # Language selector row
        lang_row = QHBoxLayout()
        lang_row.addWidget(QLabel(self.t["lang_label"]))
        self.lang_box = QComboBox(); self.lang_box.addItems(["Deutsch", "English"])
        self.lang_box.setCurrentIndex(0)  # Deutsch default
        lang_row.addWidget(self.lang_box)
        lang_row.addStretch(1)
        layout.addLayout(lang_row)

        form = QFormLayout()
        layout.addLayout(form)

        # Saved payees row
        saved_row = QHBoxLayout()
        self.saved = QComboBox(); self.refresh_saved()
        self.btn_load = QPushButton(self.t["btn_load"])
        self.btn_save = QPushButton(self.t["btn_save"])
        self.btn_delete = QPushButton(self.t["btn_delete"])
        saved_row.addWidget(QLabel(self.t["saved_payees"]))
        saved_row.addWidget(self.saved, 1)
        saved_row.addWidget(self.btn_load)
        saved_row.addWidget(self.btn_save)
        saved_row.addWidget(self.btn_delete)
        layout.addLayout(saved_row)

        # Inputs
        self.name = QLineEdit(); self.name.setPlaceholderText(self.t["ph_name"]) 
        self.iban = QLineEdit(); self.iban.setPlaceholderText(self.t["ph_iban"]) 
        self.bic = QLineEdit(); self.bic.setPlaceholderText(self.t["ph_bic"]) 
        self.amount = QLineEdit(); self.amount.setPlaceholderText(self.t["ph_amount"]) 
        self.purpose = QLineEdit(); self.purpose.setMaxLength(4); self.purpose.setPlaceholderText(self.t["ph_purpose"]) 
        self.ref = QLineEdit(); self.ref.setPlaceholderText(self.t["ph_structured"]) 
        self.text = QLineEdit(); self.text.setPlaceholderText(self.t["ph_unstructured"]) 
        self.info = QLineEdit(); self.info.setPlaceholderText(self.t["ph_info"]) 

        # Tooltips
        self.name.setToolTip(self.t["tt_name"]) 
        self.iban.setToolTip(self.t["tt_iban"]) 
        self.bic.setToolTip(self.t["tt_bic"]) 
        self.amount.setToolTip(self.t["tt_amount"]) 
        self.purpose.setToolTip(self.t["tt_purpose"]) 
        self.ref.setToolTip(self.t["tt_structured"]) 
        self.text.setToolTip(self.t["tt_unstructured"]) 
        self.info.setToolTip(self.t["tt_info"]) 

        self.version = QComboBox(); self.version.addItems(["002", "001"])  # 002 recommended
        self.version.setToolTip(self.t["tt_version"]) 
        self.charset = QComboBox(); self.charset.addItems(["1"])  # UTF-8
        self.charset.setToolTip(self.t["tt_charset"]) 

        # Purpose with help button
        purpose_row = QHBoxLayout()
        purpose_row.addWidget(self.purpose, 1)
        self.btn_purpose_help = QPushButton("?"); self.btn_purpose_help.setFixedWidth(28)
        purpose_row.addWidget(self.btn_purpose_help)

        # Labels (store to update on language change)
        self.lbl_name = QLabel(self.t["lbl_name"]) 
        self.lbl_iban = QLabel(self.t["lbl_iban"]) 
        self.lbl_bic = QLabel(self.t["lbl_bic"]) 
        self.lbl_amount = QLabel(self.t["lbl_amount"]) 
        self.lbl_purpose = QLabel(self.t["lbl_purpose"]) 
        self.lbl_structured = QLabel(self.t["lbl_structured"]) 
        self.lbl_unstructured = QLabel(self.t["lbl_unstructured"]) 
        self.lbl_info = QLabel(self.t["lbl_info"]) 

        form.addRow(self.lbl_name, self.name)
        form.addRow(self.lbl_iban, self.iban)
        form.addRow(self.lbl_bic, self.bic)
        form.addRow(self.lbl_amount, self.amount)
        form.addRow(self.lbl_purpose, purpose_row)
        form.addRow(self.lbl_structured, self.ref)
        form.addRow(self.lbl_unstructured, self.text)
        form.addRow(self.lbl_info, self.info)

        adv_row = QHBoxLayout(); 
        self.lbl_version = QLabel(self.t["lbl_version"]) 
        self.lbl_charset = QLabel(self.t["lbl_charset"]) 
        adv_row.addWidget(self.lbl_version); adv_row.addWidget(self.version)
        adv_row.addWidget(self.lbl_charset); adv_row.addWidget(self.charset)
        form.addRow(adv_row)

        # Action buttons + legend
        btns = QHBoxLayout()
        self.btn_preview = QPushButton(self.t["btn_save_png"]) 
        self.btn_preview_payload = QPushButton(self.t["btn_preview_payload"]) 
        self.btn_copy = QPushButton(self.t["btn_copy_payload"]) 
        self.btn_open_folder = QPushButton(self.t["btn_open_folder"]) 
        btns.addWidget(self.btn_preview)
        btns.addWidget(self.btn_preview_payload)
        btns.addWidget(self.btn_copy)
        btns.addWidget(self.btn_open_folder)
        layout.addLayout(btns)

        self.legend = QLabel(self.t["legend_required"]) 
        self.legend.setStyleSheet("color: gray;")
        layout.addWidget(self.legend)

        # Wire up
        self.btn_preview.clicked.connect(self.save_png)
        self.btn_preview_payload.clicked.connect(self.show_payload_preview)
        self.btn_copy.clicked.connect(self.copy_payload)
        self.btn_purpose_help.clicked.connect(self.show_purpose_help)
        self.btn_load.clicked.connect(self.load_selected_payee)
        self.btn_save.clicked.connect(self.save_current_payee)
        self.btn_delete.clicked.connect(self.delete_selected_payee)
        self.btn_open_folder.clicked.connect(self.open_output_folder)
        self.lang_box.currentIndexChanged.connect(self.change_language)

    # ---------- i18n helpers ----------
    def change_language(self):
        self.lang = "de" if self.lang_box.currentIndex() == 0 else "en"
        self.t = I18N[self.lang]
        self.apply_i18n()

    def apply_i18n(self):
        self.setWindowTitle(self.t["app_title"]) 
        # Top rows
        self.btn_load.setText(self.t["btn_load"]) 
        self.btn_save.setText(self.t["btn_save"]) 
        self.btn_delete.setText(self.t["btn_delete"]) 
        # Labels
        self.lbl_name.setText(self.t["lbl_name"]) 
        self.lbl_iban.setText(self.t["lbl_iban"]) 
        self.lbl_bic.setText(self.t["lbl_bic"]) 
        self.lbl_amount.setText(self.t["lbl_amount"]) 
        self.lbl_purpose.setText(self.t["lbl_purpose"]) 
        self.lbl_structured.setText(self.t["lbl_structured"]) 
        self.lbl_unstructured.setText(self.t["lbl_unstructured"]) 
        self.lbl_info.setText(self.t["lbl_info"]) 
        self.lbl_version.setText(self.t["lbl_version"]) 
        self.lbl_charset.setText(self.t["lbl_charset"]) 
        # Placeholders & tooltips
        self.name.setPlaceholderText(self.t["ph_name"]) 
        self.iban.setPlaceholderText(self.t["ph_iban"]) 
        self.bic.setPlaceholderText(self.t["ph_bic"]) 
        self.amount.setPlaceholderText(self.t["ph_amount"]) 
        self.purpose.setPlaceholderText(self.t["ph_purpose"]) 
        self.ref.setPlaceholderText(self.t["ph_structured"]) 
        self.text.setPlaceholderText(self.t["ph_unstructured"]) 
        self.info.setPlaceholderText(self.t["ph_info"]) 
        self.name.setToolTip(self.t["tt_name"]) 
        self.iban.setToolTip(self.t["tt_iban"]) 
        self.bic.setToolTip(self.t["tt_bic"]) 
        self.amount.setToolTip(self.t["tt_amount"]) 
        self.purpose.setToolTip(self.t["tt_purpose"]) 
        self.ref.setToolTip(self.t["tt_structured"]) 
        self.text.setToolTip(self.t["tt_unstructured"]) 
        self.info.setToolTip(self.t["tt_info"]) 
        self.version.setToolTip(self.t["tt_version"]) 
        self.charset.setToolTip(self.t["tt_charset"]) 
        # Buttons & legend
        self.btn_preview.setText(self.t["btn_save_png"]) 
        self.btn_preview_payload.setText(self.t["btn_preview_payload"]) 
        self.btn_copy.setText(self.t["btn_copy_payload"]) 
        self.btn_open_folder.setText(self.t["btn_open_folder"]) 
        self.legend.setText(self.t["legend_required"]) 

    # ---------- Saved payees helpers ----------
    def refresh_saved(self):
        self.saved = getattr(self, 'saved', QComboBox())
        names = self.store.list_names()
        self.saved.clear()
        if names:
            self.saved.addItems(names)
        else:
            self.saved.addItem("(none)")

    def current_payee_from_fields(self) -> dict:
        return {
            "name": self.name.text().strip(),
            "iban": self.iban.text().replace(" ", "").upper().strip(),
            "bic": self.bic.text().upper().strip(),
        }

    def load_selected_payee(self):
        name = self.saved.currentText()
        p = self.store.get(name)
        if not p:
            QMessageBox.information(self, self.t["saved_payees"], "No saved payee selected." if self.lang=="en" else "Kein gespeicherter Empfänger ausgewählt.")
            return
        self.name.setText(p.get("name", ""))
        self.iban.setText(p.get("iban", ""))
        self.bic.setText(p.get("bic", ""))

    def save_current_payee(self):
        p = self.current_payee_from_fields()
        if not p["name"] or not p["iban"]:
            QMessageBox.warning(self, self.t["saved_payees"], "Name and IBAN are required to save a payee." if self.lang=="en" else "Name und IBAN sind zum Speichern erforderlich.")
            return
        self.store.upsert(p)
        self.refresh_saved()
        QMessageBox.information(self, self.t["saved"], (f"Saved/updated '{p['name']}'.\nFile: {APP_STATE}" if self.lang=="en" else f"Gespeichert/Aktualisiert: '{p['name']}'.\nDatei: {APP_STATE}"))

    def delete_selected_payee(self):
        name = self.saved.currentText()
        p = self.store.get(name)
        if not p:
            QMessageBox.information(self, self.t["saved_payees"], "No saved payee selected." if self.lang=="en" else "Kein gespeicherter Empfänger ausgewählt.")
            return
        self.store.delete(name)
        self.refresh_saved()
        QMessageBox.information(self, self.t["saved"], (f"Deleted '{name}'." if self.lang=="en" else f"Gelöscht: '{name}'."))

    # ---------- Core features ----------
    def validate(self) -> tuple[bool, str]:
        t = self.t
        name = self.name.text().strip()
        iban = self.iban.text().replace(" ", "").upper().strip()
        if not name:
            return False, t["err_name_req"]
        if not iban:
            return False, t["err_iban_req"]
        if not re.fullmatch(r"[A-Z]{2}[0-9A-Z]{13,32}", iban):
            return False, t["err_iban_fmt"]
        if self.version.currentText() == "001" and not self.bic.text().strip():
            return False, t["err_bic_req"]
        amt = self.amount.text().strip()
        if not amt:
            return False, t["err_amount_req"]
        try:
            val = float(amt.replace(",", "."))
            if val <= 0:
                raise ValueError
        except Exception:
            return False, t["err_amount_pos"]
        purp = self.purpose.text().strip()
        if purp and not re.fullmatch(r"[A-Za-z]{4}", purp):
            return False, t["err_purpose_fmt"]
        if len(name) > 70:
            return False, t["err_name_len"]
        # optional BIC format check
        bic = self.bic.text().strip()
        if bic and not re.fullmatch(r"[A-Za-z0-9]{8}([A-Za-z0-9]{3})?", bic):
            return False, t["err_bic_fmt"]
        if len(self.text.text()) > 140:
            return False, t["err_text_len"]
        if len(self.info.text()) > 70:
            return False, t["err_info_len"]
        return True, ""

    def current_payload(self) -> str:
        return build_epc_payload(
            name=self.name.text(),
            iban=self.iban.text(),
            amount_eur=self.amount.text(),
            bic=self.bic.text() or None,
            purpose_code=self.purpose.text() or None,
            remittance_ref=self.ref.text() or None,
            remittance_text=self.text.text() or None,
            info=self.info.text() or None,
            version=self.version.currentText(),
            charset=self.charset.currentText(),
        )

    def save_png(self):
        ok, msg = self.validate()
        if not ok:
            QMessageBox.warning(self, self.t["dlg_validation"], msg)
            return
        payload = self.current_payload()
        try:
            qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M)
            qr.add_data(payload)
            qr.make(fit=True)
            img = qr.make_image()
        except Exception as e:
            QMessageBox.critical(self, self.t["qr_error"], str(e))
            return

        # Ensure output folder exists
        try:
            BASE_OUT.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            QMessageBox.critical(self, self.t["folder_error"], self.t["msg_folder_err"].format(path=BASE_OUT, err=e))
            return

        # Build auto filename: <amount>_<last10digitsIBAN>_<YYYY-MM-DD>.png
        amt_txt = self.amount.text().strip()
        if amt_txt:
            try:
                val = float(amt_txt.replace(",", "."))
                amt_part = f"{val:.2f}"
            except Exception:
                amt_part = "NA"
        else:
            amt_part = "NA"

        iban_raw = self.iban.text()
        digits = ''.join(ch for ch in iban_raw if ch.isdigit())
        last10 = digits[-10:] if digits else iban_raw.replace(' ', '')[-10:]

        date_part = datetime.now().strftime("%Y-%m-%d")
        fname = f"{amt_part}_{last10}_{date_part}.png"

        safe_name = ''.join(c for c in fname if c not in '\\/:*?"<>|')
        out_path = BASE_OUT / safe_name

        try:
            img.save(str(out_path))
            QMessageBox.information(self, self.t["saved"], self.t["msg_saved_qr"].format(path=out_path))
        except Exception as e:
            QMessageBox.critical(self, self.t["save_error"], str(e))

    def copy_payload(self):
        ok, msg = self.validate()
        if not ok:
            QMessageBox.warning(self, self.t["dlg_validation"], msg)
            return
        payload = self.current_payload()
        QApplication.clipboard().setText(payload)
        QMessageBox.information(self, self.t["copied"], self.t["msg_copied"])

    def open_output_folder(self):
        try:
            BASE_OUT.mkdir(parents=True, exist_ok=True)
            if sys.platform.startswith('win'):
                os.startfile(str(BASE_OUT))
            elif sys.platform == 'darwin':
                os.system(f'open "{BASE_OUT}"')
            else:
                os.system(f'xdg-open "{BASE_OUT}"')
        except Exception as e:
            QMessageBox.warning(self, self.t["open_folder_error"], self.t["msg_open_folder_err"].format(path=BASE_OUT, err=e))

    def show_payload_preview(self):
        ok, msg = self.validate()
        if not ok:
            QMessageBox.warning(self, self.t["dlg_validation"], msg)
            return
        payload = self.current_payload()
        lines = payload.split("\n")
        preview = "\n".join(f"{i+1:02d}: {ln}" for i, ln in enumerate(lines))
        preview += f"\n\n" + self.t["payload_length"].format(n=len(payload))
        QMessageBox.information(self, self.t["payload_preview"], preview)

    def show_purpose_help(self):
        QMessageBox.information(self, self.t["purpose_help_title"], self.t["purpose_help"])


def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
