"""Build the External Affairs staging site from the Northeastern Design System (NUEAC-413).

Pages are composed from the system's organisms and molecules; content is the live
externalaffairs.northeastern.edu content (scraped into build/content.json). Run from the repo root:
    python3 build/build.py            # writes docs/
"""
import html
import sys
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "docs"
sys.path.insert(0, str(Path.home() / "Projects/nu-site-kit"))
from kit import Site  # noqa: E402  (shared page shell: header, footers, Explore sheet, assets)
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


site = Site(ROOT, UNIT, "externalaffairs-staging", "externalaffairs.northeastern.edu", NAV,
            [("External Affairs", [("Our expertise", "expertise/"), ("Team", "our-team/"), ("Leadership", "our-team/leadership/"), ("Public policy", "public-policies/"), ("Contact us", "contact/")]),
             ("Resources", [(l, t) for l, t in NAV[2][1] if t.startswith("http")])],
            address=ADDRESS, phone="617.373.5718")


def page(path, title, description, body, current="", over=False):
    hero, main = body if over else ("", body)
    site.page(path, title, description, main, current, hero)


def hero_title(h1, lead=None, crumbs=None, extra=""):
    bc = ""
    if crumbs:
        lis = "".join(f'<li><a class="nu-link" href="{u}">{l}</a>{i("chevron-right")}</li>' for l, u in crumbs)
        bc = f'<nav class="nu-breadcrumb" aria-label="Breadcrumb"><ol>{lis}<li><span aria-current="page">{h1}</span></li></ol></nav>'
    return f'''<header class="nu-hero-title st-hero-title">
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
    top = f'''<section class="nu-hero-page st-hero" data-mode="dark">
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
    main = f'''<section class="st-band" aria-labelledby="st-highlights">
<div class="nu-card-grid">
  <div class="nu-card-grid__head"><div class="nu-card-grid__intro"><h2 class="nu-heading nu-heading--h2" id="st-highlights">Highlights</h2></div></div>
  <ul class="nu-card-grid__items" role="list">{cards}</ul>
</div>
</section>
<section class="st-band st-band--sunken" aria-labelledby="st-what">
  <header class="nu-section-header nu-section-header--split">
    <h2 class="nu-heading nu-heading--h2" id="st-what">What we do</h2>
    <div class="nu-section-header__body"><p class="nu-text nu-text--lead">Our approach is collaborative and strategic, with the goal of positioning Northeastern as the world leader in experiential learning and an engine for global impact.</p>
      <a class="nu-arrow-link" href="expertise/">Our expertise {i("arrow")}</a></div>
  </header>
  <div class="st-rows">{rows}</div>
</section>
<section class="nu-media-text nu-media-text--reverse st-about">
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
        blocks += f'''<section class="nu-media-text{" nu-media-text--reverse" if n % 2 else ""} st-tight" id="{a["id"]}" aria-labelledby="{a["id"]}-h">
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
    body = hero_title("Government relations", p["lead"], [(UNIT, "../")]) + f'''<section class="st-band">
<div class="nu-document-list">
  <div class="nu-document-list__group">
    <div class="nu-document-list__label"><h2 class="nu-heading nu-heading--h4">Policy briefs</h2><p class="nu-text nu-text--small">{p["intro"]}</p></div>
    <ul class="nu-document-list__files">{files}</ul>
  </div>
</div>
</section>
<section class="nu-media-text st-after-list">
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
    return '<nav class="st-tabs" aria-label="Our team">' + "".join(
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
    body = hero_title("Our team", "The people who tell Northeastern’s story: media and public relations, government affairs, city and community engagement, and marketing.", [(UNIT, "../")], team_tabs("Team", "../")) + f'''<section class="st-band st-band--first">
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
      <div class="st-contact-inline">{contact_items(l)}</div>
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
<div class="nu-profile__body st-profile-body">
  <section class="nu-profile__areas" aria-labelledby="pr-contact"><h2 class="nu-heading nu-heading--h4" id="pr-contact">Contact</h2><div class="st-contact-stack">{contact_items(l)}</div></section>
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
    fig = f'<figure class="st-hero-figure">{img("contact_collage_m.png", "The Northeastern University seal, fall on the Boston campus, and a Huskies mural", "natural")}</figure>'
    body = hero_title("Contact us", c["lead"], [(UNIT, "../")]).replace('<header class="nu-hero-title st-hero-title">', '<header class="nu-hero-title st-hero-title st-hero-title--figure">').replace("  <hr class", fig + "\n  <hr class") + f'''<section class="st-band st-contact">
  <div class="st-contact__blocks">{blocks}</div>
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
    body = f'''<section class="st-band st-404">
  <h1 class="nu-heading nu-heading--h1">We couldn’t find that page.</h1>
  <p class="nu-text nu-text--lead">It may have moved when External Affairs moved to the new site. Try one of these instead.</p>
  <div class="st-rows">''' + "".join(f'''<article class="nu-link-row"><h2 class="nu-heading nu-heading--h3 nu-link-row__title"><a class="nu-link-row__link" href="{{{{base}}}}{u}">{l}</a></h2>
    <div class="nu-link-row__body"><span class="nu-arrow-link nu-arrow-link--sm nu-link-row__cue" aria-hidden="true">Go {i("arrow")}</span></div></article>''' for l, u in
        [("Home", ""), ("Our expertise", "expertise/"), ("Our team", "our-team/"), ("Contact us", "contact/")]) + "</div></section>"
    for l, d in [("Home", "External Affairs at Northeastern University."), ("Our expertise", "City and community engagement, communications, and government relations."),
                 ("Our team", "The External Affairs team and its leadership."), ("Contact us", "Phone and email for each department.")]:
        body = body.replace(f">{l}</a></h2>\n    <div class=\"nu-link-row__body\"><span", f">{l}</a></h2>\n    <div class=\"nu-link-row__body\"><p class=\"nu-text\">{d}</p><span", 1)
    body = body.replace(">Go ", ">Open ")
    page("404.html", "Page not found", "Page not found.", body)


def main():
    for fn in (home, expertise, policy, team, leadership, bios, contact, not_found):
        fn()
    site.finish()


if __name__ == "__main__":
    main()
