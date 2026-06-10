#!/usr/bin/env python3
"""Customise the Hawk Academy GTM starter container for an attendee.

Reads the starter template, swaps {{GA4_MEASUREMENT_ID}} for the attendee's
actual Measurement ID, and writes a ready-to-import JSON to the output path.

Stdlib only.

Usage:
  python3 customise_gtm.py \\
    --template <skill-dir>/templates/gtm-starter.json \\
    --measurement-id G-XXXXXXXXXX \\
    --out ~/Downloads/hawk-academy-gtm.json

Output:
  A valid GTM container JSON the attendee can import via GTM Admin → Import Container.
"""
import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path


MEASUREMENT_ID_PATTERN = re.compile(r"^G-[A-Z0-9]{8,12}$")


def validate_measurement_id(mid):
    """GA4 Measurement IDs look like G-XXXXXXXXXX (G-, then 8-12 alphanumeric)."""
    if not MEASUREMENT_ID_PATTERN.match(mid.upper()):
        return False, (
            f"'{mid}' doesn't look like a valid GA4 Measurement ID.\n"
            f"Expected format: G-XXXXXXXXXX (starts with G-, then 8-12 letters/digits).\n"
            f"Find yours at analytics.google.com → Admin → Data Streams → click your web stream → top-right of the panel."
        )
    return True, None


def main(argv):
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--template", required=True,
                    help="Path to the GTM starter container template")
    ap.add_argument("--measurement-id", required=True,
                    help="Attendee's GA4 Measurement ID (G-XXXXXXXXXX)")
    ap.add_argument("--out", required=True,
                    help="Where to write the customised container JSON")
    args = ap.parse_args(argv)

    # Validate
    measurement_id = args.measurement_id.strip().upper()
    ok, err = validate_measurement_id(measurement_id)
    if not ok:
        print(f"❌ {err}", file=sys.stderr)
        return 1

    template_path = Path(args.template).expanduser()
    if not template_path.exists():
        print(f"❌ Template not found: {template_path}", file=sys.stderr)
        return 1

    out_path = Path(args.out).expanduser()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Read template, swap, write
    template_text = template_path.read_text()
    if "{{GA4_MEASUREMENT_ID}}" not in template_text:
        print(f"⚠️  Template doesn't contain {{GA4_MEASUREMENT_ID}} placeholder.", file=sys.stderr)
        print(f"    Writing template as-is to {out_path}.", file=sys.stderr)

    customised = template_text.replace("{{GA4_MEASUREMENT_ID}}", measurement_id)

    # Update exportTime to current
    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    customised = customised.replace("2026-05-15 00:00:00", today)

    # Validate it's still valid JSON after swap
    try:
        json.loads(customised)
    except json.JSONDecodeError as e:
        print(f"❌ Customised container failed JSON validation: {e}", file=sys.stderr)
        return 1

    out_path.write_text(customised)

    print(f"✓ Wrote customised GTM container: {out_path}")
    print(f"  Measurement ID: {measurement_id}")
    print()
    print("Next: in Google Tag Manager:")
    print(f"  1. Admin (top-right) → Import Container")
    print(f"  2. Choose container file → select {out_path}")
    print(f"  3. Workspace: New → name it 'Hawk Academy Setup'")
    print(f"  4. Import option: Merge")
    print(f"  5. Click Confirm")
    print(f"  6. Top-right: Submit → name it 'Hawk Academy initial setup' → Publish")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
