import os
import re
from string import Formatter

class TemplateRenderer:
    """Render {context_key} and ${ENVIRONMENT_VARIABLE} placeholders."""
    _env_pattern = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")

    def render(self, template_string, context):
        if not isinstance(template_string, str):
            return template_string
        def replace_env(match):
            return os.getenv(match.group(1), match.group(0))
        rendered = self._env_pattern.sub(replace_env, template_string)
        try:
            return _SafeFormatter().vformat(rendered, (), _SafeContext(context))
        except (ValueError, IndexError) as exc:
            raise ValueError(f"Cannot render template {template_string!r}: {exc}") from exc

class _SafeFormatter(Formatter):
    def get_field(self, field_name, args, kwargs):
        try:
            return kwargs[field_name], field_name
        except (KeyError, AttributeError, IndexError, TypeError):
            return super().get_field(field_name, args, kwargs)

    def format_field(self, value, format_spec):
        try:
            return super().format_field(value, format_spec)
        except ValueError:
            return str(value)

class _SafeContext(dict):
    def __missing__(self, key):
        # Support dotted paths and numeric list indexes, e.g. {attachments_meta.0.filepath}.
        current = self
        for part in key.split('.'):
            if isinstance(current, (list, tuple)):
                try:
                    current = current[int(part)]
                except (IndexError, ValueError):
                    return '{' + key + '}'
            elif isinstance(current, dict):
                if part in current:
                    current = current[part]
                else:
                    return '{' + key + '}'
            else:
                return '{' + key + '}'
        return current
