{%- extends 'null.tpl' -%}

{% block header -%}
# coding: utf-8
{%- endblock header %}

{%- block in_prompt -%}{%- endblock in_prompt -%}

{% block input -%}{{ cell.source | remove_ipython_specific }}{%- endblock input %}

{%- block markdowncell scoped -%}{{- cell.source | keep_only_headlines -}}{%- endblock markdowncell -%}
