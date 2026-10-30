"""Build the External Affairs staging site from the Northeastern Design System (NUEAC-413).

Pages are composed from the system's organisms and molecules; content is the live
externalaffairs.northeastern.edu content (scraped into build/content.json). Run from the repo root:
    python3 build/build.py            # writes docs/
"""
import html
import importlib.util
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "docs"
DS = Path.home() / "Projects/nu-homepage-prototype/design-system"
spec = importlib.util.spec_from_file_location("canvas", DS / "tools/canvas.py")
canvas = importlib.util.module_from_spec(spec)
spec.loader.exec_module(canvas)
C = json.loads((ROOT / "build/content.json").read_text())
UNIT = "External Affairs"
CUR = ' aria-current="page"'
ADDRESS = ["716 Columbus Avenue", "Suite 598", "Boston, MA 02120"]


def e(s):
    return html.escape(s, quote=True)


def i(name):
    return "{{i:%s}}" % name


NAV = [("Our expertise", "expertise/"), ("Team", "our-team/"),
       ("Resources", [("Brand governance", "https://brand.northeastern.edu/"),
                      ("Brand and media policies", "https://brand.northeastern.edu/policies/"),
                      ("Media inquiries", "https://news.northeastern.edu/media-inquiries/"),
                      ("Northeastern Global News", "https://news.northeastern.edu/"),
                      ("Public policy", "public-policies/"),
                      ("Service opportunities", "https://csce.sites.northeastern.edu/how-to-find-the-programs-for-you/"),
                      ("Student ambassadors", "https://brand.northeastern.edu/student-ambassadors/")]),
       ("Contact us", "contact/")]


def href(u, base):
    return u if u.startswith(("http", "mailto:", "tel:", "#")) else base + u


def header(base, current, over=False):
    items = []
    for label, target in NAV:
        if isinstance(target, list):
            cur = ' aria-current="true"' if current in [t for _, t in target] else ""
            sub = "".join(f'<li><a href="{href(t, base)}"{CUR if t == current else ""}>{e(l)}</a></li>' for l, t in target)
            items.append(f'<li class="nu-local-header__item"><button class="nu-nav-trigger" type="button" aria-expanded="false" aria-controls="ea-resources"{cur}>{label}{i("chevron-down")}</button>'
                         f'<ul class="nu-local-header__menu" id="ea-resources" hidden>{sub}</ul></li>')
        else:
            cur = ' aria-current="page"' if current == target else ""
            items.append(f'<li><a class="nu-nav-trigger" href="{base}{target}"{cur}>{label}</a></li>')
    flat = []
    for label, target in NAV:
        for l, t in (target if isinstance(target, list) else [(label, target)]):
            flat.append(f'<li><a href="{href(t, base)}"{CUR if t == current else ""}>{e(l)}</a></li>')
    return f'''<header class="nu-header-stack nu-header-stack--explore{" nu-header-stack--over-media" if over else ""}" data-mode="dark">
  <div class="nu-header-stack__strip">
    <a class="nu-header-stack__mono" href="https://www.northeastern.edu/" aria-label="Northeastern University">{{{{logo}}}}</a>
    <div class="nu-header-stack__actions"><button class="nu-nav-trigger nu-nav-trigger--sm nu-header-stack__explore" type="button" aria-expanded="false" aria-controls="ea-explore">Explore Northeastern{i("apps")}</button></div>
  </div>
  <div class="nu-header-stack__bar">
    <a class="nu-site-identity" href="{base}"><span class="nu-site-identity__name">{UNIT}</span></a>
    <nav class="nu-header-stack__nav" aria-label="{UNIT}"><ul>{"".join(items)}</ul></nav>
    <div class="nu-header-stack__actions ea-unit-menu"><button class="nu-icon-button nu-header-stack__menu" type="button" aria-label="Open the {UNIT} menu" aria-expanded="false" aria-controls="ea-unit-menu">{i("menu")}</button>
      <ul class="nu-local-header__menu ea-unit-menu__list" id="ea-unit-menu" hidden>{"".join(flat)}</ul></div>
  </div>
</header>'''


def explore_sheet():
    mm = (DS / "components/organisms/mobile-menu.html").read_text()
    start = mm.find('<div class="nu-mobile-menu"')
    depth, end = 0, start
    for m in re.finditer(r"<div\b|</div>", mm[start:]):
        depth += 1 if m.group(0) == "<div" else -1
        if depth == 0:
            end = start + m.end()
            break
    sheet = mm[start:end].replace('id="mo1"', 'id="ea-explore" hidden', 1).replace('aria-label="Menu"', 'aria-label="Explore Northeastern"', 1)
    sheet = sheet.replace('aria-label="Close menu"', 'aria-label="Close Explore Northeastern" data-close', 1)
    return sheet.replace('href="#"', 'href="https://www.northeastern.edu/"')


def global_footer():
    s = (DS / "components/templates/unit-home.html").read_text()
    start = s.find('<footer class="nu-global-footer"')
    return s[start:s.find("</footer>", start) + 9].replace('href="#"', 'href="https://www.northeastern.edu/"')


def local_footer(base):
    links = "".join(f'<li><a class="nu-local-footer__link nu-nav-link" href="{base}{t}">{l}</a></li>' for l, t in
                    [("Our expertise", "expertise/"), ("Team", "our-team/"), ("Leadership", "our-team/leadership/"), ("Public policy", "public-policies/"), ("Contact us", "contact/")])
    res = "".join(f'<li><a class="nu-local-footer__link nu-nav-link" href="{t}">{l}</a></li>' for l, t in NAV[2][1] if t.startswith("http"))
    return f'''<footer class="nu-local-footer" aria-label="{UNIT}">
  <div class="nu-local-footer__inner">
    <div class="nu-local-footer__identity">
      <a class="nu-site-identity" href="{base}"><span class="nu-site-identity__name">{UNIT}</span></a>
      <ul class="nu-local-footer__contact">
        <li><address class="nu-contact-item">{i("location")}<span class="nu-contact-item__label">Address</span><span class="nu-contact-item__value">{"<br>".join(ADDRESS)}</span></address></li>
        <li><div class="nu-contact-item">{i("phone")}<span class="nu-contact-item__label">Phone</span><span class="nu-contact-item__value"><a class="nu-link" href="tel:+16173735718">617.373.5718</a></span></div></li>
      </ul>
    </div>
    <nav class="nu-local-footer__cols" aria-label="{UNIT}, more">
      <div class="nu-local-footer__col"><h2 class="nu-text nu-text--label">External Affairs</h2><ul class="nu-local-footer__links">{links}</ul></div>
      <div class="nu-local-footer__col"><h2 class="nu-text nu-text--label">Resources</h2><ul class="nu-local-footer__links">{res}</ul></div>
    </nav>
  </div>
</footer>'''


def page(path, title, description, body, current="", over=False, mode=None):
    depth = path.count("/") + (0 if not path or path.endswith(".html") else 1)
    # GitHub Pages serves 404.html at any missing path, so it needs root-absolute links.
    base = "/externalaffairs-staging/" if path == "404.html" else "../" * depth
    doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{e(title)}{"" if title == UNIT else " · " + UNIT} · Northeastern University</title>
<meta name="description" content="{e(description)}">
<link rel="icon" href="{base}assets/favicon.svg">
<link rel="stylesheet" href="{base}assets/nu-ds.css">
<link rel="stylesheet" href="{base}assets/site.css">
<script src="{base}assets/site.js" defer></script>
</head>
<body{f' data-mode="{mode}"' if mode else ""}>
{canvas.ICONS}
<a class="ea-skip nu-button nu-button--sm" href="#main">Skip to content</a>
<div class="ea-staging" role="note">Staging preview of externalaffairs.northeastern.edu on the Northeastern Design System. Not the live site.</div>
<div class="ea-top{" ea-top--over" if over else ""}">
{header(base, current, over)}
{body[0] if over else ""}
</div>
<main id="main">
{body[1] if over else body}
</main>
{local_footer(base)}
{global_footer()}
<div class="ea-sheet">{explore_sheet()}</div>
</body>
</html>'''
    doc = doc.replace("{{base}}", base)
    out = SITE / path / "index.html" if not path.endswith(".html") else SITE / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(canvas.expand(doc, "src"))


def hero_title(h1, lead=None, crumbs=None, extra=""):
    bc = ""
    if crumbs:
        lis = "".join(f'<li><a class="nu-link" href="{u}">{l}</a>{i("chevron-right")}</li>' for l, u in crumbs)
        bc = f'<nav class="nu-breadcrumb" aria-label="Breadcrumb"><ol>{lis}<li><span aria-current="page">{h1}</span></li></ol></nav>'
    return f'''<header class="nu-hero-title ea-hero-title">
  <div class="nu-hero-title__main">
    {bc}
    <h1 class="nu-heading nu-heading--h1">{h1}</h1>
    {f'<p class="nu-text nu-text--lead">{lead}</p>' if lead else ""}
    {extra}
  </div>
  <hr class="nu-rule nu-hero-title__rule">
</header>'''


def img(name, alt="", ratio="3x2", extra=""):
    cls = "nu-image" if ratio == "natural" else f"nu-image nu-image--{ratio}"
    return f'<img class="{cls}" src="{{{{base}}}}assets/img/{name}" alt="{e(alt)}" loading="lazy"{extra}>'


# ---------- pages ----------
def home():
    h = C["home"]
    top = f'''<section class="nu-hero-page ea-home-hero" data-mode="dark">
  <div class="nu-hero-page__media">
    <img class="nu-image nu-image--fill" src="{{{{base}}}}assets/img/Hero-Steps.jpg" alt="">
    <span class="nu-scrim nu-scrim--left"></span><span class="nu-scrim nu-scrim--scene"></span><span class="nu-scrim nu-scrim--grain"></span><span class="nu-scrim nu-scrim--full nu-hero-page__phone-scrim"></span>
  </div>
  <div class="nu-hero-page__copy">
    <h1 class="nu-heading nu-heading--h1">{h["h1"]}</h1>
    <a class="nu-button" href="expertise/">Our expertise {i("arrow")}</a>
  </div>
</section>'''
    cards = "".join(f'''<li><article class="nu-story-card">
  <span class="nu-story-card__media">{img(c["img"])}</span>
  <div class="nu-story-card__body">
    <h3 class="nu-heading nu-heading--h4 nu-story-card__title"><a class="nu-story-card__link" href="{c["url"]}">{c["title"]}</a></h3>
    <ul class="nu-meta-list nu-meta-list--inline"><li>{c["source"]}</li></ul>
  </div>
</article></li>''' for c in h["highlights"])
    rows = "".join(f'''<article class="nu-link-row">
  <h3 class="nu-heading nu-heading--h3 nu-link-row__title"><a class="nu-link-row__link" href="expertise/#{x["id"]}">{x["name"]}</a></h3>
  <div class="nu-link-row__body"><p class="nu-text">{x["summary"]}</p>
    <span class="nu-arrow-link nu-arrow-link--sm nu-link-row__cue" aria-hidden="true">More on {x["short"]} {i("arrow")}</span></div>
</article>''' for x in C["expertise"]["areas"])
    main = f'''<section class="ea-band" aria-labelledby="ea-highlights">
<div class="nu-card-grid">
  <div class="nu-card-grid__head"><div class="nu-card-grid__intro"><h2 class="nu-heading nu-heading--h2" id="ea-highlights">Highlights</h2></div></div>
  <ul class="nu-card-grid__items" role="list">{cards}</ul>
</div>
</section>
<section class="ea-band ea-band--sunken" aria-labelledby="ea-what">
  <header class="nu-section-header nu-section-header--split">
    <h2 class="nu-heading nu-heading--h2" id="ea-what">What we do</h2>
    <div class="nu-section-header__body"><p class="nu-text nu-text--lead">Our approach is collaborative and strategic, with the goal of positioning Northeastern as the world leader in experiential learning and an engine for global impact.</p>
      <a class="nu-arrow-link" href="expertise/">Our expertise {i("arrow")}</a></div>
  </header>
  <div class="ea-rows">{rows}</div>
</section>
<section class="nu-media-text nu-media-text--reverse ea-about">
  <figure class="nu-media-text__media">{img("AboutUs-4.5.2022.jpg", "Portraits of members of the External Affairs team", "natural")}</figure>
  <div class="nu-media-text__copy">
    <h2 class="nu-heading nu-heading--h2">About us</h2>
    <p class="nu-text">{h["about"]}</p>
    <div class="nu-media-text__actions"><a class="nu-button" href="our-team/">Meet our team</a><a class="nu-arrow-link" href="contact/">Contact us {i("arrow")}</a></div>
  </div>
</section>'''
    page("", UNIT, h["h1"], (top, main), "", over=True)


def expertise():
    x = C["expertise"]
    blocks = ""
    for n, a in enumerate(x["areas"]):
        paras = "".join(f'<p class="nu-text">{p}</p>' for p in a["body"])
        blocks += f'''<section class="nu-media-text{" nu-media-text--reverse" if n % 2 else ""} ea-tight" id="{a["id"]}" aria-labelledby="{a["id"]}-h">
  <figure class="nu-media-text__media">{img(a["img"], a["alt"])}</figure>
  <div class="nu-media-text__copy">
    <h2 class="nu-heading nu-heading--h2" id="{a["id"]}-h">{a["name"]}</h2>
    {paras}
    <div class="nu-media-text__actions"><a class="nu-arrow-link" href="{href(a["link"][1], "../")}">{a["link"][0]} {i("arrow")}</a></div>
  </div>
</section>'''
    page("expertise", "Our expertise", x["lead"], hero_title("Our expertise", x["lead"]) + blocks, "expertise/")


def policy():
    p = C["policy"]
    files = "".join(f'''<li><a class="nu-file-link" href="{d["url"]}">
  <span class="nu-file-link__icon">{i("file")}</span>
  <span class="nu-file-link__text"><span class="nu-file-link__name">{d["title"]}</span><span class="nu-text nu-text--meta">{d["desc"]} · PDF</span></span>
  <span class="nu-icon-button nu-icon-button--outline nu-file-link__action" aria-hidden="true">{i("download")}</span>
</a></li>''' for d in p["briefs"])
    body = hero_title("Government relations", p["lead"], [(UNIT, "../")]) + f'''<section class="ea-band">
<div class="nu-document-list">
  <div class="nu-document-list__group">
    <div class="nu-document-list__label"><h2 class="nu-heading nu-heading--h4">Policy briefs</h2><p class="nu-text nu-text--small">{p["intro"]}</p></div>
    <ul class="nu-document-list__files">{files}</ul>
  </div>
</div>
</section>
<section class="nu-media-text ea-after-list">
  <figure class="nu-media-text__media">{img("101623_AS_EXP_Grand_Opening_167.jpeg", "A speaker at the podium in front of the Northeastern seal")}</figure>
  <div class="nu-media-text__copy">
    <h2 class="nu-heading nu-heading--h2">Talk to our government relations team</h2>
    <p class="nu-text">{C["contact"]["depts"][4]["desc"]}</p>
    <div class="nu-media-text__actions"><a class="nu-button" href="../contact/">Contact us</a><a class="nu-arrow-link" href="../our-team/leadership/">Leadership {i("arrow")}</a></div>
  </div>
</section>'''
    page("public-policies", "Government relations", p["lead"], body, "public-policies/")


def team_tabs(active, base):
    tabs = [("Team", "our-team/"), ("Leadership", "our-team/leadership/")]
    return '<nav class="ea-tabs" aria-label="Our team">' + "".join(
        f'<a class="nu-chip" href="{base}{u}"{CUR if l == active else ""}>{l}</a>' for l, u in tabs) + "</nav>"


def team():
    leaders = {l["name"]: l["slug"] for l in C["leaders"]}
    cards = ""
    for n, t, f in C["team"]:
        link = f'<a class="nu-person-card__link" href="leadership/bio/{leaders[n]}/">{n}</a>' if n in leaders else n
        cards += f'''<li><article class="nu-person-card">
  <span class="nu-person-card__media">{img("team/" + f, "", "4x5")}</span>
  <div class="nu-person-card__body"><h3 class="nu-heading nu-heading--h4">{link}</h3><p class="nu-text nu-text--small nu-person-card__title">{t}</p></div>
</article></li>'''
    body = hero_title("Our team", "The people who tell Northeastern’s story: media and public relations, government affairs, city and community engagement, and marketing.", [(UNIT, "../")], team_tabs("Team", "../")) + f'''<section class="ea-band ea-band--first">
<div class="nu-card-grid nu-card-grid--people">
  <ul class="nu-card-grid__items" role="list">{cards}</ul>
</div>
</section>'''
    page("our-team", "Our team", "Meet the External Affairs team at Northeastern University.", body, "our-team/")


def contact_items(l, phone_label="Phone"):
    out = ""
    if l.get("tel"):
        out += f'<div class="nu-contact-item">{i("phone")}<span class="nu-contact-item__label">{phone_label}</span><span class="nu-contact-item__value"><a class="nu-link" href="tel:+1{re.sub(r"[^0-9]", "", l["tel"])}">{l["tel"]}</a></span></div>'
    if l.get("email"):
        out += f'<div class="nu-contact-item">{i("mail")}<span class="nu-contact-item__label">Email</span><span class="nu-contact-item__value"><a class="nu-link" href="mailto:{l["email"]}">{l["email"]}</a></span></div>'
    return out


def leadership():
    L = C["leaders"]
    first, rest = L[0], L[1:]
    feat = f'''<div class="nu-leadership__feature" data-mode="dark">
<section class="nu-featured-person" aria-labelledby="ld-{first["slug"]}">
  <span class="nu-featured-person__media">{img(first["photo"], "", "4x5")}</span>
  <div class="nu-featured-person__body">
    <div class="nu-featured-person__name"><h2 class="nu-heading nu-heading--h1" id="ld-{first["slug"]}">{first["name"]}</h2><p class="nu-text nu-text--meta">{first["title"]}</p></div>
    <p class="nu-text nu-text--lead">{first["fullbio"][0]}</p>
    <a class="nu-arrow-link" href="bio/{first["slug"]}/">Read full bio<span class="u-vh">, {first["name"]}</span>{i("arrow")}</a>
  </div>
</section>
</div>'''
    rows = "".join(f'''<article class="nu-featured-person nu-featured-person--row" aria-labelledby="ld-{l["slug"]}">
  <span class="nu-featured-person__media">{img(l["photo"], "", "4x5")}</span>
  <div class="nu-featured-person__body">
    <div class="nu-featured-person__name"><h2 class="nu-heading nu-heading--h2" id="ld-{l["slug"]}">{l["name"]}</h2><p class="nu-text nu-text--small nu-featured-person__title">{l["title"]}</p></div>
    <div class="nu-featured-person__about"><p class="nu-text">{l["fullbio"][0]}</p>
      <div class="ea-contact-inline">{contact_items(l)}</div>
      <div class="nu-featured-person__actions"><a class="nu-button nu-button--sm" href="bio/{l["slug"]}/">Full bio<span class="u-vh">, {l["name"]}</span></a></div></div>
  </div>
</article>''' for l in rest)
    body = f'''{hero_title("Leadership", "The leaders of Northeastern’s central marketing, communications, and city, state and federal government relations teams.", [(UNIT, "../../"), ("Our team", "../")], team_tabs("Leadership", "../../"))}
<div class="nu-leadership">{feat}<div class="nu-leadership__rows">{rows}</div></div>'''
    page("our-team/leadership", "Leadership", "Leadership of External Affairs at Northeastern University.", body, "our-team/")


def bios():
    L = C["leaders"]
    for n, l in enumerate(L):
        nxt = L[(n + 1) % len(L)]
        prose = "".join(f"<p>{p}</p>" for p in l["fullbio"])
        body = f'''<div class="nu-profile">
<div class="nu-profile__top">
<header class="nu-profile-header">
  <div class="nu-profile-header__media">{img(l["photo"], l["name"], "4x5")}</div>
  <div class="nu-profile-header__body">
    <div class="nu-profile-header__intro">
      <a class="nu-arrow-link nu-arrow-link--back nu-arrow-link--sm" href="../../">{i("arrow-left")}Leadership</a>
      <h1 class="nu-heading nu-heading--h1">{l["name"]}</h1>
      <p class="nu-text nu-text--lead nu-profile-header__role">{l["title"]}</p>
    </div>
    <div class="nu-profile-header__next"><a class="nu-arrow-link" href="../{nxt["slug"]}/">Next profile: {nxt["name"]}{i("arrow")}</a></div>
  </div>
</header>
</div>
<div class="nu-profile__body ea-profile-body">
  <section class="nu-profile__areas" aria-labelledby="pr-contact"><h2 class="nu-heading nu-heading--h4" id="pr-contact">Contact</h2><div class="ea-contact-stack">{contact_items(l)}</div></section>
  <div class="nu-profile__main"><div class="nu-prose"><h2>About</h2>{prose}</div></div>
</div>
</div>'''
        page(f"our-team/leadership/bio/{l['slug']}", l["name"], f'{l["name"]}, {l["title"]}, Northeastern University.', body, "our-team/")


def contact():
    c = C["contact"]
    blocks = ""
    for d in c["depts"]:
        items = ""
        if d.get("address"):
            items += f'<address class="nu-contact-item">{i("location")}<span class="nu-contact-item__label">Address</span><span class="nu-contact-item__value">{"<br>".join(ADDRESS)}</span></address>'
        items += contact_items(d)
        blocks += f'''<section class="nu-contact-block" aria-labelledby="ct-{d["id"]}">
  <div class="nu-contact-block__label"><h2 class="nu-heading nu-heading--h4" id="ct-{d["id"]}">{d["name"]}</h2><p class="nu-text nu-text--small">{d["desc"]}</p></div>
  <div class="nu-contact-block__body"><div class="nu-contact-block__items">{items}</div></div>
</section>'''
    fig = f'<figure class="ea-hero-figure">{img("contact_collage_m.png", "The Northeastern University seal, fall on the Boston campus, and a Huskies mural", "natural")}</figure>'
    body = hero_title("Contact us", c["lead"], [(UNIT, "../")]).replace('<header class="nu-hero-title ea-hero-title">', '<header class="nu-hero-title ea-hero-title ea-hero-title--figure">').replace("  <hr class", fig + "\n  <hr class") + f'''<section class="ea-band ea-contact">
  <div class="ea-contact__blocks">{blocks}</div>
</section>
<section class="nu-action-band" data-mode="dark" aria-labelledby="ct-expertise">
  <div class="nu-action-band__inner">
    <div class="nu-action-band__copy"><h2 class="nu-heading nu-heading--h1" id="ct-expertise">Our expertise</h2>
      <p class="nu-text nu-text--lead">{C["expertise"]["lead"]}</p></div>
    <div class="nu-action-band__actions"><a class="nu-button" href="../expertise/">Learn more</a></div>
  </div>
</section>'''
    page("contact", "Contact us", c["lead"], body, "contact/")


def not_found():
    body = f'''<section class="ea-band ea-404">
  <h1 class="nu-heading nu-heading--h1">We couldn’t find that page.</h1>
  <p class="nu-text nu-text--lead">It may have moved when External Affairs moved to the new site. Try one of these instead.</p>
  <div class="ea-rows">''' + "".join(f'''<article class="nu-link-row"><h2 class="nu-heading nu-heading--h3 nu-link-row__title"><a class="nu-link-row__link" href="{{{{base}}}}{u}">{l}</a></h2>
    <div class="nu-link-row__body"><span class="nu-arrow-link nu-arrow-link--sm nu-link-row__cue" aria-hidden="true">Go {i("arrow")}</span></div></article>''' for l, u in
        [("Home", ""), ("Our expertise", "expertise/"), ("Our team", "our-team/"), ("Contact us", "contact/")]) + "</div></section>"
    for l, d in [("Home", "External Affairs at Northeastern University."), ("Our expertise", "City and community engagement, communications, and government relations."),
                 ("Our team", "The External Affairs team and its leadership."), ("Contact us", "Phone and email for each department.")]:
        body = body.replace(f">{l}</a></h2>\n    <div class=\"nu-link-row__body\"><span", f">{l}</a></h2>\n    <div class=\"nu-link-row__body\"><p class=\"nu-text\">{d}</p><span", 1)
    body = body.replace(">Go ", ">Open ")
    page("404.html", "Page not found", "Page not found.", body)


def main():
    assets = SITE / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    canvas.bundle()
    shutil.copy(DS / "dist/nu-ds.css", assets / "nu-ds.css")
    for f in ("site.css", "site.js", "favicon.svg"):
        shutil.copy(ROOT / "build" / f, assets / f)
    (SITE / ".nojekyll").write_text("")
    for fn in (home, expertise, policy, team, leadership, bios, contact, not_found):
        fn()
    print("built", sum(1 for _ in SITE.rglob("*.html")), "pages")


if __name__ == "__main__":
    main()
