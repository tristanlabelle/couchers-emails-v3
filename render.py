from dataclasses import dataclass
from typing import Any
import jinja2
import json
from pathlib import Path
import re

@dataclass
class RenderedEmail:
    subject: str
    body_plaintext: str
    body_html: str


def render(email_model: Any) -> RenderedEmail:
    jinja_loader = jinja2.FileSystemLoader(Path(__file__).parent / "templates")
    jinja_env = jinja2.Environment(loader=jinja_loader, trim_blocks=True)
    jinja_env.filters["translate"] = _filter_translate

    email_template = jinja_env.get_template(f"{email_model.__class__.__name__}.jinja2")

    def render_template(layout_filename: str, macros_filename: str) -> str:
        layout_template = jinja_env.get_template(f"include/{layout_filename}")
        macros_template = jinja_env.get_template(f"include/{macros_filename}")

        template_args = {
            "_layout": layout_template,
            "_sections": macros_template,
            **email_model.__dict__
        }
        return email_template.render(template_args)
    
    return RenderedEmail(
        subject=render_template("subject_layout.jinja2", "subject_macros.jinja2"),
        body_plaintext=render_template("body_plaintext_layout.jinja2", "body_plaintext_macros.jinja2"),
        body_html=render_template("body_html_layout.jinja2", "body_html_macros.jinja2"),
    )


@jinja2.pass_context
def _filter_translate(context: jinja2.runtime.Context, key: str, **kwargs) -> str:
    strings_dict = json.loads((Path(__file__).parent / "en.json").read_text())
    value = strings_dict[key]
    return re.sub(r"\{\{\s*(\w+)\s*\}\}", lambda match: str(kwargs[match.group(1)]), value)
