import json, sys, urllib.request, urllib.parse, pathlib

out = pathlib.Path(sys.argv[1])
api = 'http://localhost:3001/api/v2/docs'
DEFAULT = 'es'
CATEGORY_ORDER = ['ads', 'social', 'analytics', 'ecommerce', 'crm']
DESCRIPTIONS_DIR = pathlib.Path(__file__).parent / 'descriptions'
DATA_DIR = pathlib.Path(__file__).parent / 'data'
LOCAL_ONLY = sys.argv[3] if len(sys.argv) > 3 and sys.argv[2] == '--local' else None
ONLY = set(sys.argv[2].split(',')) if len(sys.argv) > 2 and not LOCAL_ONLY else None
LOCAL = {path.stem: json.loads(path.read_text()) for path in sorted(DATA_DIR.glob('*.json'))}
T = {
 'es': dict(overview='Resumen', catalog='Catálogo de campos',
   catalog_desc='Explora todas las métricas y dimensiones disponibles para cada fuente de datos',
   intro='Cada fuente de datos conectada a Master Metrics expone un conjunto de campos que puedes usar en tus dashboards, reportes y conversaciones con IA. Los campos son de dos tipos:',
   m_def='los números que mides, como impresiones, alcance, pedidos o ingresos.',
   d_def='las categorías por las que agrupas, como fecha, país, tipo de contenido o producto.',
   usage='Usa este catálogo para encontrar los campos exactos disponibles en cada fuente. Cada campo muestra su nombre, su nombre de campo y una breve descripción, además de si se puede consultar desde la integración MCP para herramientas de IA.',
   metrics='Métricas', dimensions='Dimensiones', trouble='Solución de problemas',
   m_sub='Referencia completa de las métricas de {s} en Master Metrics', d_sub='Referencia completa de las dimensiones de {s} en Master Metrics',
   t_sub='Qué revisar al conectar o usar la integración de {s}',
   m_intro='Esta referencia cubre las {n} métricas disponibles de {s} en Master Metrics. Úsala para entender qué datos puedes obtener y cómo se llama cada campo.',
   d_intro='Esta referencia cubre las {n} dimensiones disponibles de {s} en Master Metrics. Úsala para entender cómo puedes segmentar tus datos y cómo se llama cada campo.',
   m_hint='Las métricas son los valores numéricos que puedes medir y agregar a partir de tus datos de {s}.',
   d_hint='Las dimensiones son los atributos que puedes usar para segmentar y agrupar tus datos de {s}.',
   updated='Última actualización', available='Disponible en', dest='Dashboards · Reportes · Asistente de IA',
   field='Nombre del campo', type='Tipo', m_type='métrica', d_type='dimensión', mcp_yes='Disponible', mcp_no='No disponible',
   deprecated='Métricas deprecadas', dep_hint='Estas métricas fueron retiradas por la plataforma. Se mantienen como referencia histórica y no están disponibles en el MCP.',
   related='Relacionado', browse='Ver todas las fuentes', ads='Publicidad', social='Redes sociales', analytics='Analítica web', ecommerce='E-commerce', crm='CRM y email', web='Sitio web', login='Ingresar'),
 'en': dict(overview='Overview', catalog='Fields catalog',
   catalog_desc='Browse all the metrics and dimensions available for each data source',
   intro='Every data source connected to Master Metrics exposes a set of fields you can use in your dashboards, reports and AI conversations. Fields come in two types:',
   m_def='the numbers you measure, such as impressions, reach, orders or revenue.',
   d_def='the categories you group by, such as date, country, content type or product.',
   usage='Use this catalog to find the exact fields available for each source. Every field lists its name, its field name and a short description, plus whether it can be queried through the MCP integration for AI tools.',
   metrics='Metrics', dimensions='Dimensions', trouble='Troubleshooting',
   m_sub='Complete reference of the {s} metrics in Master Metrics', d_sub='Complete reference of the {s} dimensions in Master Metrics',
   t_sub='What to check when connecting or using the {s} integration',
   m_intro='This reference covers the {n} metrics available for {s} in Master Metrics. Use it to understand which data you can pull and how each field is named.',
   d_intro='This reference covers the {n} dimensions available for {s} in Master Metrics. Use it to understand how you can segment your data and how each field is named.',
   m_hint='Metrics are the numeric values you can measure and aggregate from your {s} data.',
   d_hint='Dimensions are the attributes you can use to segment and group your {s} data.',
   updated='Last updated', available='Available in', dest='Dashboards · Reports · AI assistant',
   field='Field name', type='Type', m_type='metric', d_type='dimension', mcp_yes='Available', mcp_no='Not available',
   deprecated='Deprecated metrics', dep_hint='These metrics were retired by the platform. They are kept for historical reference and are not available in the MCP.',
   related='Related', browse='Browse all sources', ads='Advertising', social='Social', analytics='Web analytics', ecommerce='E-commerce', crm='CRM & email', web='Website', login='Log in'),
 'pt': dict(overview='Visão geral', catalog='Catálogo de campos',
   catalog_desc='Explore todas as métricas e dimensões disponíveis para cada fonte de dados',
   intro='Cada fonte de dados conectada ao Master Metrics expõe um conjunto de campos que você pode usar em seus dashboards, relatórios e conversas com IA. Os campos são de dois tipos:',
   m_def='os números que você mede, como impressões, alcance, pedidos ou receita.',
   d_def='as categorias pelas quais você agrupa, como data, país, tipo de conteúdo ou produto.',
   usage='Use este catálogo para encontrar os campos exatos disponíveis em cada fonte. Cada campo mostra seu nome, seu nome de campo e uma breve descrição, além de indicar se pode ser consultado pela integração MCP para ferramentas de IA.',
   metrics='Métricas', dimensions='Dimensões', trouble='Solução de problemas',
   m_sub='Referência completa das métricas de {s} no Master Metrics', d_sub='Referência completa das dimensões de {s} no Master Metrics',
   t_sub='O que verificar ao conectar ou usar a integração de {s}',
   m_intro='Esta referência cobre as {n} métricas disponíveis de {s} no Master Metrics. Use-a para entender quais dados você pode obter e como cada campo se chama.',
   d_intro='Esta referência cobre as {n} dimensões disponíveis de {s} no Master Metrics. Use-a para entender como você pode segmentar seus dados e como cada campo se chama.',
   m_hint='As métricas são os valores numéricos que você pode medir e agregar a partir dos seus dados de {s}.',
   d_hint='As dimensões são os atributos que você pode usar para segmentar e agrupar seus dados de {s}.',
   updated='Última atualização', available='Disponível em', dest='Dashboards · Relatórios · Assistente de IA',
   field='Nome do campo', type='Tipo', m_type='métrica', d_type='dimensão', mcp_yes='Disponível', mcp_no='Não disponível',
   deprecated='Métricas descontinuadas', dep_hint='Estas métricas foram retiradas pela plataforma. São mantidas como referência histórica e não estão disponíveis no MCP.',
   related='Relacionado', browse='Ver todas as fontes', ads='Publicidade', social='Redes sociais', analytics='Análise web', ecommerce='E-commerce', crm='CRM e e-mail', web='Site', login='Entrar'),
}

def get(path, locale):
    return json.load(urllib.request.urlopen(f'{api}{path}?locale={locale}'))

def local_summary(slug, locale):
    data = LOCAL[slug]
    content = data['locales'][locale]
    return {'slug': slug, 'name': data['name'], 'category': data['category'], 'mcpEnabled': data['mcpEnabled'],
            'metricsCount': len(content['metrics']), 'dimensionsCount': len(content['dimensions']),
            'hasTroubleshooting': bool(content['notes'] or content['videos'])}

def local_source(slug, locale):
    data = LOCAL[slug]
    return {'slug': slug, 'name': data['name'], 'category': data['category'], 'updatedAt': data['updatedAt'],
            'mcpEnabled': data['mcpEnabled'], **json.loads(json.dumps(data['locales'][locale]))}

def card(summary, prefix, t):
    return [f'  <Card title="{q(summary["name"])}" href="{prefix}/{summary["slug"]}/metrics">',
            f'    {summary["metricsCount"]} {t["metrics"].lower()} · {summary["dimensionsCount"]} {t["dimensions"].lower()}' + (' · MCP' if summary['mcpEnabled'] else ''),
            '  </Card>']

def write_source(summary, sources, base, prefix, page, locale, t):
    slug = summary['slug']
    (base / slug).mkdir(parents=True, exist_ok=True)
    src = get_source(slug, locale)
    fields_page(src, sources, 'metrics', base, prefix, t)
    fields_page(src, sources, 'dimensions', base, prefix, t)
    pages = [page(f'{slug}/metrics'), page(f'{slug}/dimensions')]
    if summary['hasTroubleshooting']:
        trouble_page(src, sources, base, prefix, t)
        pages.append(page(f'{slug}/troubleshooting'))
    return {'group': summary['name'], 'pages': pages}

def publish_local(slug):
    cfg_path = out / 'docs.json'
    cfg = json.loads(cfg_path.read_text())
    for language in cfg['navigation']['languages']:
        locale = language['language']
        t = T[locale]
        prefix = '' if locale == DEFAULT else f'/{locale}'
        base = out if locale == DEFAULT else out / locale
        page = lambda path: path if locale == DEFAULT else f'{locale}/{path}'
        summary = local_summary(slug, locale)
        others = [{'slug': item['pages'][0].split('/')[-2], 'name': item['group']}
                  for group in language['groups'] for item in group['pages'] if isinstance(item, dict)]
        entry = write_source(summary, [summary] + [o for o in others if o['slug'] != slug], base, prefix, page, locale, t)
        title = t.get(summary['category'], summary['category'])
        group = next((g for g in language['groups'] if g['group'] == title), None)
        if group is None:
            group = {'group': title, 'pages': []}
            language['groups'].insert(1, group)
        group['pages'] = [entry] + [item for item in group['pages'] if not (isinstance(item, dict) and item['group'] == summary['name'])]
        index_path = base / 'index.mdx'
        lines = index_path.read_text().split('\n')
        href = f'href="{prefix}/{slug}/metrics"'
        if not any(href in line for line in lines):
            if f'## {title}' not in lines:
                at = next(i for i, line in enumerate(lines) if line.startswith('## '))
                lines[at:at] = [f'## {title}', '', '<CardGroup cols={2}>', '</CardGroup>', '']
            start = lines.index('<CardGroup cols={2}>', lines.index(f'## {title}'))
            lines[start + 1:start + 1] = card(summary, prefix, t)
            index_path.write_text('\n'.join(lines))
    cfg_path.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + '\n')
    print('ok local', slug)

def get_source(slug, locale):
    src = local_source(slug, locale) if slug in LOCAL else get(f'/{slug}', locale)
    path = DESCRIPTIONS_DIR / f'{slug}.json'
    extra = json.loads(path.read_text()) if path.exists() else {}
    for field in src['metrics'] + src['dimensions']:
        if not field.get('description'):
            field['description'] = extra.get(field['name'], {}).get(locale)
    return src

def esc(text):
    return (text or '').replace('\\', '\\\\').replace('{', '\\{').replace('}', '\\}').replace('<', '&lt;').replace('>', '&gt;').replace('|', '\\|').replace('\n', ' ')

def q(text):
    return text.replace('"', '\\"')

def table(fields, kind, with_mcp, t):
    rows = ['| | |', '|---|---|']
    for f in fields:
        detail = esc(f.get('description'))
        meta = f"**{t['field']}:** `{f['name']}`<br/>**{t['type']}:** {kind}"
        if with_mcp:
            meta += f"<br/>**MCP:** {t['mcp_yes'] if f.get('mcp') else t['mcp_no']}"
        rows.append(f"| {esc(f['label'])} | {detail + '<br/><br/>' if detail else ''}{meta} |")
    return '\n'.join(rows)

def related(src, sources, prefix, t):
    cards = [f'  <Card title="{q(t["catalog"])}" href="{prefix}/">', f'    {t["browse"]}', '  </Card>']
    for other in [s for s in sources if s['slug'] != src['slug']][:3]:
        cards += [f'  <Card title="{q(other["name"])}" href="{prefix}/{other["slug"]}/metrics">', f'    {t["metrics"]} & {t["dimensions"]}', '  </Card>']
    return [f'## {t["related"]}', '', '<CardGroup cols={2}>', *cards, '</CardGroup>', '']

def fields_page(src, sources, key, base, prefix, t):
    is_metrics = key == 'metrics'
    title = t['metrics'] if is_metrics else t['dimensions']
    p = 'm' if is_metrics else 'd'
    fields = src[key]
    active = [f for f in fields if not f.get('deprecated')]
    deprecated = [f for f in fields if f.get('deprecated')]
    groups = {}
    for f in active:
        groups.setdefault(f['group'], []).append(f)
    name = src['name']
    parts = ['---', f'title: "{q(name)}: {title}"', f'description: "{q(t[p + "_sub"].format(s=name))}"', '---', '',
             f'<Info>**{t["updated"]}:** {src["updatedAt"]}</Info>', '',
             t[p + '_intro'].format(n=len(fields), s=name), '',
             f'**{t["available"]}:** {t["dest"]}' + (' · MCP' if src['mcpEnabled'] else ''), '',
             f'## {title}', '', t[p + '_hint'].format(s=name), '']
    for group, items in groups.items():
        parts += [f'### {esc(group)}', '', table(items, t[p + '_type'], is_metrics, t), '']
    if deprecated:
        parts += [f'## {t["deprecated"]}', '', t['dep_hint'], '', table(deprecated, t[p + '_type'], is_metrics, t), '']
    parts += related(src, sources, prefix, t)
    (base / src['slug'] / f'{key}.mdx').write_text('\n'.join(parts))

def trouble_page(src, sources, base, prefix, t):
    name = src['name']
    parts = ['---', f'title: "{q(name)}: {t["trouble"]}"', f'description: "{q(t["t_sub"].format(s=name))}"', '---', '',
             f'<Info>**{t["updated"]}:** {src["updatedAt"]}</Info>', '']
    for note in src['notes']:
        parts += [f'## {esc(note["title"])}', '', esc(note['body']), '']
    for video in src['videos']:
        embed = video['url'].replace('/share/', '/embed/')
        parts += [f'## {esc(video["title"])}', '', f'<iframe className="w-full aspect-video rounded-xl" src="{embed}" title="{q(video["title"])}" allowFullScreen></iframe>', '']
    parts += related(src, sources, prefix, t)
    (base / src['slug'] / 'troubleshooting.mdx').write_text('\n'.join(parts))

if LOCAL_ONLY:
    publish_local(LOCAL_ONLY)
    sys.exit(0)

languages = []
for locale, t in T.items():
    prefix = '' if locale == DEFAULT else f'/{locale}'
    base = out if locale == DEFAULT else out / locale
    page = lambda path: path if locale == DEFAULT else f'{locale}/{path}'
    sources = [local_summary(slug, locale) for slug in LOCAL] + get('', locale)['sources']
    sources = [s for s in sources if ONLY is None or s['slug'] in ONLY]
    found = list(dict.fromkeys(s['category'] for s in sources))
    categories = [c for c in CATEGORY_ORDER if c in found] + [c for c in found if c not in CATEGORY_ORDER]
    index = ['---', f'title: "{t["catalog"]}"', f'description: "{t["catalog_desc"]}"', '---', '', t['intro'], '',
             f'- **{t["metrics"]}**: {t["m_def"]}', f'- **{t["dimensions"]}**: {t["d_def"]}', '', t['usage'], '']
    groups = [{'group': t['overview'], 'pages': [page('index')]}]
    for category in categories:
        index += [f'## {t.get(category, category)}', '', '<CardGroup cols={2}>']
        nav = []
        for summary in [s for s in sources if s['category'] == category]:
            nav.append(write_source(summary, sources, base, prefix, page, locale, t))
            index += card(summary, prefix, t)
        index += ['</CardGroup>', '']
        groups.append({'group': t.get(category, category), 'pages': nav})
    (base / 'index.mdx').write_text('\n'.join(index))
    languages.append({'language': locale, 'groups': groups})

cfg_path = out / 'docs.json'
cfg = json.loads(cfg_path.read_text())
cfg['navigation'] = {'languages': languages}
cfg_path.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + '\n')
print('ok', [(l['language'], sum(len(g['pages']) for g in l['groups'])) for l in languages])
