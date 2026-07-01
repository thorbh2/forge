"""Seed FORGE with real build ideas on studionet (AI review)."""
from pathlib import Path

from gltest_cli.config.general import get_general_config
from gltest_cli.config.user import load_user_config
from gltest import get_contract_factory, get_default_account

ROOT = Path(__file__).resolve().parents[1]
ADDR = "0x4Cb98B53d879D3cF6e9886431918466BEf999Ff9"
W = "https://en.wikipedia.org/api/rest_v1/page/summary/"

cfg = load_user_config(str(ROOT / "gltest.config.yaml"))
get_general_config().user_config = cfg
factory = get_contract_factory(contract_file_path=str(ROOT / "contracts" / "forge.py"))
c = factory.build_contract(ADDR, account=get_default_account())

IDEAS = [
    ("QR-code generator CLI", "A small command line tool that turns any text or URL into a scannable QR code image.", W + "QR_code", True),
    ("Self-hosted RSS reader", "A lightweight web app that subscribes to feeds and shows new articles in a clean reader.", W + "RSS", True),
    ("Perpetual-motion power app", "An app that runs a device producing more energy than it consumes, forever, with no input.", W + "Perpetual_motion", True),
    ("Faster-than-light messenger", "A chat network that delivers messages faster than the speed of light across galaxies.", W + "Faster-than-light", True),
    ("Daily habit tracker", "A simple app to check off daily habits and keep streaks.", "https://example.com", False),
]


def main():
    if c.get_idea_count().call() == 0:
        for (t, p, url, _) in IDEAS:
            c.pitch(args=[t, p, url]).transact()
            print("pitched:", t)

    for iid in range(c.get_idea_count().call()):
        do = IDEAS[iid][3] if iid < len(IDEAS) else False
        it = c.get_idea(args=[iid]).call()
        if do and int(it["status"]) == 0:
            print("reviewing (AI):", it["title"])
            try:
                c.review(args=[iid]).transact()
            except Exception as e:
                print("  review ->", e)

    print("stats:", c.get_stats().call())
    for iid in range(c.get_idea_count().call()):
        it = c.get_idea(args=[iid]).call()
        print(iid, ["PITCHED", "GREENLIT", "SHELVED"][int(it["status"])], "score=%s" % it["score"], "|", it["title"], "|", (it["rationale"] or "")[:40])


if __name__ == "__main__":
    main()
