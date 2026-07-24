import re
from datetime import datetime


class DocumentValidator:

    def validate(self, document: dict):

        doc_type = document.get("document_type")
        data = document.get("extracted_data", {})

        if doc_type == "PAN Card":
            document["validation"] = self._validate_pan(data)

        elif doc_type == "Aadhaar Card":
            document["validation"] = self._validate_aadhaar(data)

        elif doc_type == "FSSAI License":
            document["validation"] = self._validate_fssai(data)

        elif doc_type == "GST Certificate":
            document["validation"] = self._validate_gst(data)

        else:
            document["validation"] = {}

        return document

    # --------------------------------------------------
    # PAN CARD
    # --------------------------------------------------

    def _validate_pan(self, data):

        validation = {}

        pan = data.get("pan_number", "").strip().upper()

        pattern = r"^[A-Z]{5}[0-9]{4}[A-Z]$"

        validation["pan_number"] = {
            "valid": bool(re.fullmatch(pattern, pan)),
            "message": "Valid PAN Number"
            if re.fullmatch(pattern, pan)
            else "Invalid PAN Number"
        }

        dob = data.get("date_of_birth", "").strip()

        validation["date_of_birth"] = self._validate_date(dob)

        return validation

    # --------------------------------------------------
    # AADHAAR
    # --------------------------------------------------

    def _validate_aadhaar(self, data):

        validation = {}

        aadhaar = (
            data.get("aadhaar_number", "")
            .replace(" ", "")
            .strip()
        )

        validation["aadhaar_number"] = {
            "valid": bool(re.fullmatch(r"\d{12}", aadhaar)),
            "message": "Valid Aadhaar Number"
            if re.fullmatch(r"\d{12}", aadhaar)
            else "Invalid Aadhaar Number"
        }

        return validation

    # --------------------------------------------------
    # FSSAI
    # --------------------------------------------------

    def _validate_fssai(self, data):

        validation = {}

        license_number = (
            data.get("license_number")
            or data.get("fssai_license_number")
            or ""
        ).strip()

        validation["license_number"] = {
            "valid": bool(re.fullmatch(r"\d{14}", license_number)),
            "message": "Valid FSSAI License Number"
            if re.fullmatch(r"\d{14}", license_number)
            else "Invalid FSSAI License Number"
        }

        valid_from = (
            data.get("valid_from")
            or data.get("issue_date")
            or data.get("date_of_issue")
            or ""
        ).strip()

        if valid_from:
            validation["valid_from"] = self._validate_date(valid_from)

        valid_upto = (
            data.get("valid_upto")
            or data.get("valid_up_to")
            or data.get("valid_till")
            or data.get("expiry_date")
            or data.get("validity")
            or ""
        ).strip()

        validation["valid_upto"] = self._validate_expiry(valid_upto)

        return validation

    # --------------------------------------------------
    # GST CERTIFICATE
    # --------------------------------------------------

    def _validate_gst(self, data):

        validation = {}

        gstin = (
            data.get("gstin")
            or data.get("gst_number")
            or data.get("gst_registration_number")
            or ""
        ).strip().upper()

        gst_pattern = r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][1-9A-Z]Z[0-9A-Z]$"

        validation["gstin"] = {
            "valid": bool(re.fullmatch(gst_pattern, gstin)),
            "message": "Valid GSTIN"
            if re.fullmatch(gst_pattern, gstin)
            else "Invalid GSTIN"
        }

        # Validate PAN inside GSTIN

        if len(gstin) >= 12:

            pan = gstin[2:12]

            pan_pattern = r"^[A-Z]{5}[0-9]{4}[A-Z]$"

            validation["pan_in_gstin"] = {
                "valid": bool(re.fullmatch(pan_pattern, pan)),
                "message": "Valid PAN embedded in GSTIN"
                if re.fullmatch(pan_pattern, pan)
                else "Invalid PAN embedded in GSTIN"
            }

        registration_date = (
            data.get("registration_date")
            or data.get("date_of_registration")
            or ""
        ).strip()

        if registration_date:

            validation["registration_date"] = self._validate_date(
                registration_date
            )

        status = (
            data.get("status")
            or ""
        ).strip().lower()

        if status:

            validation["status"] = {
                "valid": status in ["active", "cancelled", "suspended"],
                "message": f"GST Status: {status.title()}"
            }

        return validation

    # --------------------------------------------------
    # GENERIC DATE VALIDATOR
    # --------------------------------------------------

    def _validate_date(self, date_string):

        formats = [
            "%d/%m/%Y",
            "%d-%m-%Y",
            "%Y-%m-%d",
            "%d.%m.%Y"
        ]

        for fmt in formats:

            try:

                datetime.strptime(date_string, fmt)

                return {
                    "valid": True,
                    "message": "Valid Date"
                }

            except ValueError:
                continue

        return {
            "valid": False,
            "message": "Invalid Date"
        }

    # --------------------------------------------------
    # EXPIRY DATE VALIDATOR
    # --------------------------------------------------

    def _validate_expiry(self, date_string):

        if not date_string:

            return {
                "valid": False,
                "message": "Expiry date not found"
            }

        formats = [
            "%d/%m/%Y",
            "%d-%m-%Y",
            "%Y-%m-%d",
            "%d.%m.%Y"
        ]

        for fmt in formats:

            try:

                expiry = datetime.strptime(
                    date_string,
                    fmt
                ).date()

                today = datetime.today().date()

                if expiry >= today:

                    return {
                        "valid": True,
                        "message": f"Valid until {date_string}"
                    }

                return {
                    "valid": False,
                    "message": f"Expired on {date_string}"
                }

            except ValueError:
                continue

        return {
            "valid": False,
            "message": "Invalid expiry date format"
        }