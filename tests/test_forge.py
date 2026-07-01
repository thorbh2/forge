"""Tests for FORGE (direct runner). AI review() validated live on studionet."""
from pathlib import Path

CONTRACT = str(Path(__file__).resolve().parents[1] / "contracts" / "forge.py")
PITCHED = 0; GREENLIT = 1; SHELVED = 2


def _pitch(f, vm, who, title="A QR code CLI", pitch="A command line tool that generates QR codes", url="https://example.com"):
    vm.sender = who
    return f.pitch(title, pitch, url)


def test_pitch(deploy, direct_vm, direct_alice):
    f = deploy(CONTRACT)
    iid = _pitch(f, direct_vm, direct_alice)
    assert iid == 0
    it = f.get_idea(0)
    assert it["status"] == PITCHED
    assert it["title"] == "A QR code CLI"
    assert it["score"] == 0


def test_requires_title(deploy, direct_vm, direct_alice):
    f = deploy(CONTRACT)
    direct_vm.sender = direct_alice
    with direct_vm.expect_revert("a title is required"):
        f.pitch("", "p", "https://x.com")


def test_requires_pitch(deploy, direct_vm, direct_alice):
    f = deploy(CONTRACT)
    direct_vm.sender = direct_alice
    with direct_vm.expect_revert("a pitch is required"):
        f.pitch("t", "  ", "https://x.com")


def test_requires_spec(deploy, direct_vm, direct_alice):
    f = deploy(CONTRACT)
    direct_vm.sender = direct_alice
    with direct_vm.expect_revert("a spec URL is required"):
        f.pitch("t", "p", "")


def test_review_requires_pitched(deploy, direct_vm, direct_alice):
    f = deploy(CONTRACT)
    _pitch(f, direct_vm, direct_alice)
    with direct_vm.expect_revert("no such idea"):
        f.review(9)


def test_stats(deploy, direct_vm, direct_alice):
    f = deploy(CONTRACT)
    _pitch(f, direct_vm, direct_alice, title="A")
    _pitch(f, direct_vm, direct_alice, title="B")
    s = f.get_stats()
    assert s["total"] == 2
    assert s["pitched"] == 2


def test_multiple(deploy, direct_vm, direct_alice):
    f = deploy(CONTRACT)
    _pitch(f, direct_vm, direct_alice, title="One")
    _pitch(f, direct_vm, direct_alice, title="Two")
    assert f.get_idea_count() == 2
    assert f.get_idea(1)["title"] == "Two"
