import pytest
from pydantic import ValidationError

from resolver.records import HostName, MXRecord, TXTRecord


@pytest.mark.parametrize("name", ["github.com", "mx.example.co.uk", "example.com."])
def test_hostname_accepts_valid(name):
    assert HostName(name=name).name == name


@pytest.mark.parametrize("name", ["", "no-tld", "-bad.com", "sp ace.com"])
def test_hostname_rejects_invalid(name):
    with pytest.raises(ValidationError):
        HostName(name=name)


def test_mx_priority_bounds():
    assert MXRecord(priority=0, host=HostName(name="a.example.com")).priority == 0
    with pytest.raises(ValidationError):
        MXRecord(priority=65536, host=HostName(name="a.example.com"))


def test_txt_total_length_validator():
    # each chunk is under the 255 per-string cap, but the total exceeds 65535
    with pytest.raises(ValidationError, match="65535 bytes"):
        TXTRecord(text=["x" * 255] * 258)


def test_records_are_frozen():
    record = HostName(name="github.com")
    with pytest.raises(ValidationError):
        record.name = "other.com"


def test_unknown_fields_are_rejected():
    with pytest.raises(ValidationError):
        HostName(name="github.com", ttl=300)
