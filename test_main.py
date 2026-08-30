from datetime import datetime, timezone
from unittest.mock import patch, MagicMock

import issoverhead


class FrozenDateTime(datetime):
    current = datetime(2026, 1, 2, 0, 30, tzinfo=timezone.utc)

    @classmethod
    def now(cls, tz=None):
        if tz is not None:
            return cls.current.astimezone(tz)
        return cls.current


def test_is_dark_before_sunrise_after_midnight(monkeypatch):
    issoverhead.sunrise_dt = datetime(2026, 1, 1, 6, 0, tzinfo=timezone.utc)
    issoverhead.sunset_dt = datetime(2026, 1, 1, 18, 0, tzinfo=timezone.utc)
    FrozenDateTime.current = datetime(2026, 1, 2, 0, 30, tzinfo=timezone.utc)
    monkeypatch.setattr(issoverhead, "datetime", FrozenDateTime)

    assert issoverhead.is_dark() is True


def test_is_dark_is_false_during_day(monkeypatch):
    issoverhead.sunrise_dt = datetime(2026, 1, 2, 6, 0, tzinfo=timezone.utc)
    issoverhead.sunset_dt = datetime(2026, 1, 2, 18, 0, tzinfo=timezone.utc)
    FrozenDateTime.current = datetime(2026, 1, 2, 12, 0, tzinfo=timezone.utc)
    monkeypatch.setattr(issoverhead, "datetime", FrozenDateTime)

    assert issoverhead.is_dark() is False


def test_is_dark_requires_data():
    issoverhead.sunrise_dt = None
    issoverhead.sunset_dt = None

    assert issoverhead.is_dark() is False


def test_sends_email_when_iss_close_and_dark(monkeypatch):
    # Force proximity/darkness checks to True regardless of real data
    monkeypatch.setattr(issoverhead, "iss_is_close", lambda: True)
    monkeypatch.setattr(issoverhead, "is_dark", lambda: True)

    # Fake API responses so main() never touches the network
    fake_iss_response = MagicMock()
    fake_iss_response.raise_for_status.return_value = None
    fake_iss_response.json.return_value = {
        "iss_position": {"latitude": "41.9", "longitude": "-87.6"}
    }

    fake_sun_response = MagicMock()
    fake_sun_response.raise_for_status = lambda: None
    fake_sun_response.json.return_value = {
        "results": {
            "sunrise": "2026-01-02T06:00:00+00:00",
            "sunset": "2026-01-02T18:00:00+00:00",
        }
    }

    fake_session = MagicMock()
    fake_session.get.side_effect = [fake_iss_response, fake_sun_response]
    monkeypatch.setattr(issoverhead, "get_session_with_retries", lambda: fake_session)

    # Provide explicit credentials/addresses so the test validates arguments, not just call counts
    monkeypatch.setattr(issoverhead, "MY_EMAIL", "sender@example.com")
    monkeypatch.setattr(issoverhead, "PASSWORD", "password")
    monkeypatch.setattr(issoverhead, "PERSONAL", "recipient@example.com")

    with patch("issoverhead.smtplib.SMTP") as mock_smtp:
        mock_connection = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_connection

        issoverhead.main()

        mock_smtp.assert_called_once_with("smtp.gmail.com", port=587)
        mock_connection.starttls.assert_called_once()
        mock_connection.login.assert_called_once_with(user="sender@example.com", password="password")
        mock_connection.sendmail.assert_called_once_with(
            from_addr="sender@example.com",
            to_addrs="recipient@example.com",
            msg="Subject:ISS IS OVERHEAD\n\nISS is overhead! See if you can spot it!",
        )
