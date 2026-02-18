import requests

BASE = "http://127.0.0.1:8000"
LANGS = ["hi", "en", "bn", "te", "mr", "ta", "ur", "gu", "kn", "ml", "pa"]


def main() -> int:
    token_res = requests.post(
        f"{BASE}/v1/auth/token",
        json={"phone": "9999999999", "role": "flw"},
        timeout=5,
    )
    token_res.raise_for_status()
    token = token_res.json()["access_token"]

    ok = 0
    for lang in LANGS:
        r = requests.post(
            f"{BASE}/v1/voice/report",
            headers={"Authorization": f"Bearer {token}"},
            json={"claim_id": f"CLM-{lang}", "language": lang, "transcript": f"sample damage report {lang}"},
            timeout=5,
        )
        if r.status_code == 200:
            ok += 1

    print(f"validated={ok}/{len(LANGS)}")
    return 0 if ok == len(LANGS) else 2


if __name__ == "__main__":
    raise SystemExit(main())
