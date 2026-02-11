# Proof of concept for Couchers email templating v3

## Problems solved

- Emails are not translatable
- Every email's mjml template includes some duplicated styling
- Every email's mjml requires prerendering as html
- Every email has separate plaintext and html versions
- The subject line is templated using a different system from the email bodies.

## Solution

- [templates/HostRequestReceived.jinja2](templates/HostRequestReceived.jinja2): Template for the "host request received" email, leveraging well-known sections like a user (includes avatar, name and age), or a clickable button, and strings from [en.json](en.json).
- [email_models.py](email_models.py): Defines `HostRequestReceived` dataclass providing arguments for the template.

## Inner workings

- Several jinja2 layout files define how to render a template as...
  - HTML, by templating args into HTML snippets
  - plaintext, by templating args as plaintext
  - a subject line, by ignoring args apart from the subject
- We render the email dataclass three times, one per layout, to get a subject/plaintext/html tuple.
- We'll have a single mjml file defining the HTML template. Its HTML will need minor postprocessing to put into a shape jinja2 can use (i.e. layout + macros files).