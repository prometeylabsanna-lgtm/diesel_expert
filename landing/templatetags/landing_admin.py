from django import template

register = template.Library()


def _spec_key(spec):
    return getattr(spec, "field_path", None) or getattr(spec, "parameter_name", None)


def _options_for(cl, spec):
    options = getattr(cl.model_admin, "list_filter_options", None) or {}
    return options.get(_spec_key(spec)) or {}


def _apply_label(cl, spec):
    label = _options_for(cl, spec).get("label")
    if label:
        spec.title = label
    return spec


def _is_horizontal(cl, spec):
    option = _options_for(cl, spec).get("horizontal")
    if option is None:
        return True
    return bool(option)


@register.filter
def unfold_horizontal_filters(cl):
    return [_apply_label(cl, spec) for spec in cl.filter_specs if _is_horizontal(cl, spec)]


@register.filter
def unfold_vertical_filters(cl):
    return [
        _apply_label(cl, spec)
        for spec in cl.filter_specs
        if not _is_horizontal(cl, spec)
    ]
