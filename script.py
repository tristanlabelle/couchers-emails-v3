from datetime import date
from pathlib import Path

import email_models
from render import render

email_model = email_models.HostRequestReceived(
    user_name="Alice",
    surfer=email_models.UserInfo(name="Bob", age=42, city="Tokyo", avatar_url="https://example.com/avatar"),
    from_date=date(2000, 1, 1),
    to_date=date(2000, 1, 2),
    text="Please host me",
    view_url="https://example.com/requests",
    quick_decline_url="https://example.com/quick-decline",
)

rendered_email = render(email_model)

out_dir = Path(__file__).parent / "out"
print(f"HostRequestReceived subject: {rendered_email.subject}")
(out_dir / "HostRequestReceived.txt").write_text(rendered_email.body_plaintext)
(out_dir / "HostRequestReceived.html").write_text(rendered_email.body_html)