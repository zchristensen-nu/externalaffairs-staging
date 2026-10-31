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


NAV = [("Our expertise", "expertise/"), ("Team", "our-team/"), ("For media", "contact/#media"),
       ("Resources", [("Media policies", "https://brand.northeastern.edu/policies/"),
                      ("Media inquiries", "https://news.northeastern.edu/media-inquiries/"),
                      ("Northeastern Global News", "https://news.northeastern.edu/"),
                      ("Service opportunities", "https://csce.sites.northeastern.edu/how-to-find-the-programs-for-you/")]),
       ("Contact us", "contact/")]


def href(u, base):
    return u if u.startswith(("http", "mailto:", "tel:", "#")) else base + u


site = Site(ROOT, UNIT, "externalaffairs-staging", "externalaffairs.northeastern.edu", NAV,
            [("External Affairs", [("Our expertise", "expertise/"), ("Government relations", "public-policies/"), ("Team", "our-team/"), ("Leadership", "our-team/leadership/"), ("For media", "contact/#media"), ("Contact us", "contact/")]),
             ("Resources", [(l, t) for l, t in NAV[3][1] if t.startswith("http")])],
            address=ADDRESS, phone="617.373.5718")


def page(path, title, description, body, current="", over=False):
    hero, main = body if over else ("", body)
    site.page(path, title, description, main, current, hero)


def hero_title(h1, lead=None, crumbs=None, extra="", figure="", focus=None, here=None):
    """HeroTitle. figure: an image (markup) for the --figure variant: columns 11–12, capped to the title block, dropped below 960px."""
    bc = ""
    if crumbs:
        lis = "".join(f'<li><a class="nu-link" href="{u}">{l}</a>{i("chevron-right")}</li>' for l, u in crumbs)
        bc = f'<nav class="nu-breadcrumb" aria-label="Breadcrumb"><ol>{lis}<li><span aria-current="page">{here or h1}</span></li></ol></nav>'
    fig = ""
    if figure:
        st = f' style="--hero-title-focus:{focus}"' if focus else ""
        fig = f'<figure class="nu-hero-title__media"{st}>{figure}</figure>'
    return f'''<header class="nu-hero-title st-hero-title{" nu-hero-title--figure" if figure else ""}">
  <div class="nu-hero-title__main">
    {bc}
    <h1 class="nu-heading nu-heading--h1">{h1}</h1>
    {f'<p class="nu-text nu-text--lead">{lead}</p>' if lead else ""}
    {extra}
  </div>
  {fig}
  <hr class="nu-rule nu-hero-title__rule">
</header>'''


def img(name, alt="", ratio="3x2", extra=""):
    cls = "nu-image" if ratio == "natural" else f"nu-image nu-image--{ratio}"
    return f'<img class="{cls}" src="{{{{base}}}}assets/img/{name}" alt="{e(alt)}" loading="lazy"{extra}>'


def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower().replace("é", "e")).strip("-")


def tel(n):
    return "tel:+1" + re.sub(r"[^0-9]", "", n)


def inline_contact(tel_=None, email=None):
    """ContactItem --inline: icon and linked value on one line (no label), for headers and office leads."""
    out = ""
    if tel_:
        out += f'<span class="nu-contact-item nu-contact-item--inline">{i("phone")}<span class="u-vh">Phone </span><span class="nu-contact-item__value"><a class="nu-link" href="{tel(tel_)}">{tel_}</a></span></span>'
    if email:
        out += f'<span class="nu-contact-item nu-contact-item--inline">{i("mail")}<span class="u-vh">Email </span><span class="nu-contact-item__value"><a class="nu-link" href="mailto:{email}">{email}</a></span></span>'
    return out


def contact_items(l, phone_label="Phone", lg=False):
    out = ""
    cls = "nu-contact-item nu-contact-item--lg" if lg else "nu-contact-item"
    if l.get("tel"):
        out += f'<div class="{cls}">{i("phone")}<span class="nu-contact-item__label">{phone_label}</span><span class="nu-contact-item__value"><a class="nu-link" href="{tel(l["tel"])}">{l["tel"]}</a></span></div>'
    if l.get("email"):
        shown = l["email"].replace("@", "@<wbr>") if lg else l["email"]
        out += f'<div class="{cls}">{i("mail")}<span class="nu-contact-item__label">Email</span><span class="nu-contact-item__value"><a class="nu-link" href="mailto:{l["email"]}">{shown}</a></span></div>'
    return out


LEADERS = {l["name"]: l for l in C["leaders"]}
MEDIA = next(d for d in C["contact"]["depts"] if d["id"] == "comms")

def surname(n):
    return n.replace(", PhD", "").replace(" Jr.", "").split()[-1]


# Offices by area of expertise (ea-02, regrouped on review): the three on Our expertise plus the SVP's office; alphabetical by surname.
# The live roster has no office field, so the grouping is read from the titles.
GROUPS = [(g, sorted(names, key=surname)) for g, names in [
    ("Office of the senior vice president", ["Michael Armini", "Caitlin O'Donnell", "Diane Hubbard", "Anna Huang", "Natalie Matthews"]),
    ("City and community engagement", ["John Tobin", "Chimel Idiokitas", "David Isberg", "Elizabeth Enright", "Joseph Regan, PhD", "Monée Vance", "Jorge Dias"]),
    ("Communications", ["Renata Nyul", "Ed Gavaghan", "Belle Brody", "Maedot Kassa", "Jackie Loring", "Rachel Gouhin",
                        "Ann M. Simmons", "Efrain Hernandez Jr.", "Tanner Stening", "Katya Poltorak", "Cesareo Contreras", "Cynthia Hibbert",
                        "Rich McKay", "Hannah Morse", "Cyrus Moulton", "Peter Rubinstein",
                        "Matthew Modoono", "Alyssa Stone", "Neely Coe", "Glenn Pike", "Cameron Sleeper", "Taijai Slaughter", "Rachel Vogel", "Victoria Partika", "Jay Whitehead",
                        "Stephanie Sim", "Elizabeth Bolaji", "Xristopher Anderton", "Alex Zelenchuck", "Court Smith", "Marin Carroll", "Thara Messeroux", "Zach Christensen",
                        "Denis Skarep", "Renee Zhang"]),
    ("Government relations", ["Jack Cline", "Michael Ferrari", "Jesse Poon", "Abigail Robbins", "Maddy Brogan"]),
]]
TEAM = {n: (t, f) for n, t, f in C["team"]}
assert sorted(sum((g for _, g in GROUPS), [])) == sorted(TEAM), set(TEAM) ^ set(sum((g for _, g in GROUPS), []))
GROUP_OF = {n: g for g, names in GROUPS for n in names}


def team_link(name, base, cls="nu-arrow-link"):
    """Leaders point to their office on the team page in place of personal phone and email."""
    g = GROUP_OF[name]
    label = g if g.startswith("Office") else g + " team"
    return f'<a class="{cls}" href="{base}#team-{slug(g)}">{label} {i("arrow")}</a>'


def person_href(name, base):
    """Leaders link to their bios; everyone else to their card on the team page."""
    return f'{base}our-team/leadership/bio/{LEADERS[name]["slug"]}/' if name in LEADERS else f"{base}our-team/#{slug(name)}"


# Each office's lead and what it handles (ea-03). Lists are the office's own copy broken into its parts.
OFFICES = {
    "city-and-community-engagement": {"lead": "John Tobin", "handles": ["Partnerships with Boston neighborhoods", "Community events", "Volunteer opportunities", "Off-campus student liaison"]},
    "communications": {"lead": "Renata Nyul", "handles": ["Media inquiries", "Public relations", "Northeastern Global News", "Media policies"]},
    "government-relations": {"lead": "Jack Cline", "handles": ["Federal research funding", "Faculty expertise for Congress and funding agencies", "Global research partnerships", "Liaison on policy issues"]},
}


NGN_MARK = (ROOT / "build/ngn-wordmark.svg").read_text().strip()


def reel(sid, hid, head, noun, label, stories, mod=""):
    """Carousel ("st-reel", site.js): a scroll-snap row of stories with previous/next. A story without a photo shows its outlet as type."""
    items = ""
    for n, d in enumerate(stories, 1):
        media = (f'<span class="st-proof-media">{img(d["img"])}</span>\n      <span class="st-reel__kind">{d["kind"]}</span>' if d.get("img")
                 else f'<span class="st-proof-media st-proof-media--type"><span>{d["kind"]}</span></span>')
        items += f'''<li class="st-reel__item" aria-roledescription="slide" aria-label="{n} of {len(stories)}"><a class="nu-proof-point st-story" href="{d["url"]}" target="_blank" rel="noopener">
      {media}
      <span class="nu-heading nu-heading--h4 st-story__title">{d["title"]}</span>
      <span class="nu-text nu-text--meta nu-proof-point__meta"><span>{d["by"]}</span>{i("external")}</span>
      <span class="u-vh"> (opens in a new tab)</span></a></li>'''
    btn = '<button class="nu-icon-button nu-icon-button--outline" type="button" data-reel-{} aria-label="{} {}">{}</button>'
    return f'''<section class="st-band st-reel{mod}" id="{sid}" aria-labelledby="{hid}" aria-roledescription="carousel">
  <div class="st-reel__head">{head}<div class="st-reel__controls">{btn.format("prev", "Previous", noun, i("arrow-left"))}{btn.format("next", "Next", noun, i("arrow"))}</div></div>
  <ul class="st-reel__track" tabindex="0" aria-label="{label}">{items}</ul>
</section>'''


# ---------- pages ----------
def home():
    h = C["home"]
    # ea-05: the unit's name is the H1 and the mission sentence the lead. Hero is the 2026 Fenway convocation (Northeastern Global News); the stadium sits right of the copy.
    top = f'''<section class="nu-hero-page nu-hero-page--display st-hero" data-mode="dark">
  <div class="nu-hero-page__media" style="--hero-page-focus:70% 55%;--hero-page-focus-phone:62% 55%">
    <img class="nu-image nu-image--fill" src="{{{{base}}}}assets/img/Fenway-Convocation.jpg" alt="">
    <span class="nu-scrim nu-scrim--left"></span><span class="nu-scrim nu-scrim--scene"></span><span class="nu-scrim nu-scrim--grain"></span><span class="nu-scrim nu-scrim--full nu-hero-page__phone-scrim"></span>
  </div>
  <div class="nu-hero-page__copy">
    <h1 class="nu-heading nu-heading--display-xl">{UNIT}</h1>
    <p class="nu-text nu-text--lead">{h["h1"]}</p>
    <a class="nu-button" href="expertise/">Our expertise {i("arrow")}</a>
  </div>
</section>'''
    cards = "".join(f'''<li><a class="st-office-card" href="expertise/#{x["id"]}">
    <span class="st-office-card__media"><img class="nu-image" src="{{{{base}}}}assets/img/{x["img"]}" alt="" loading="lazy"></span>
    <h3 class="nu-heading nu-heading--h3">{x["name"]}</h3>
    <p class="nu-text">{x["card"]}</p>
    <span class="nu-arrow-link nu-arrow-link--sm st-office-card__cue" aria-hidden="true">More on {x["short"]} {i("arrow")}</span></a></li>''' for x in C["expertise"]["areas"])
    faces = "".join(f'''<li><a class="nu-portrait-wall__face" href="{person_href(n, "")}"><img class="nu-image nu-image--1x1" src="{{{{base}}}}assets/img/team/{f}" alt="" loading="lazy"><span class="nu-portrait-wall__name">{n}<span class="u-vh">, {t}</span></span></a></li>'''
                    for n, t, f in C["team"])
    main = f'''<section class="st-band st-band--tight ea-media" id="media" aria-labelledby="ea-media-h">
<div class="nu-contact-block">
  <div class="nu-contact-block__label"><h2 class="nu-heading nu-heading--h2" id="ea-media-h">For media</h2><p class="nu-text nu-text--small">{MEDIA["desc"]}</p><a class="nu-arrow-link nu-arrow-link--external" href="https://news.northeastern.edu/media-inquiries/">Media inquiries and experts {i("external")}</a></div>
  <div class="nu-contact-block__body"><div class="nu-contact-block__items">{contact_items(MEDIA, lg=True)}</div></div>
</div>
</section>
{reel("in-the-news", "ea-press-h", '<h2 class="nu-heading nu-heading--h2" id="ea-press-h">In the news</h2>', "press story", "Press coverage", h["press"])}
{reel("ngn", "ea-ngn-h", f'<h2 class="st-reel__brand" id="ea-ngn-h"><a class="st-ngn-link" href="https://news.northeastern.edu/"><span class="u-vh">Northeastern Global News</span>{NGN_MARK}</a></h2>',
      "NGN story", "Northeastern Global News: university stories", h["ngn"], " st-reel--ngn")}
<section class="st-band st-band--sunken" aria-labelledby="st-what">
  <header class="nu-section-header nu-section-header--split">
    <h2 class="nu-heading nu-heading--h2" id="st-what">What we do</h2>
    <div class="nu-section-header__body"><p class="nu-text nu-text--lead">Our approach is collaborative and strategic, with the goal of positioning Northeastern as the world leader in experiential learning and an engine for global impact.</p>
      <a class="nu-arrow-link" href="expertise/">Our expertise {i("arrow")}</a></div>
  </header>
  <ul class="st-office-cards">{cards}</ul>
</section>
<section class="nu-portrait-wall" aria-labelledby="ea-about">
  <div class="nu-portrait-wall__head">
    <h2 class="nu-heading nu-heading--h2" id="ea-about">About us</h2>
    <p class="nu-text">{h["about"]}</p>
    <a class="nu-arrow-link" href="our-team/">Meet our team {i("arrow")}</a>
  </div>
  <ul class="nu-portrait-wall__grid" data-mode="dark">{faces}</ul>
</section>'''
    page("", UNIT, h["h1"], (top, main), "", over=True)


def expertise():
    x = C["expertise"]
    lead = x["lead"].split(". ")[0] + "."
    cur = ' aria-current="location"'
    links = "".join(f'<li><a class="nu-in-page-nav__link nu-nav-link" href="#{a["id"]}"{cur if n == 0 else ""}>{a["name"]}</a></li>' for n, a in enumerate(x["areas"]))
    nav = f'''<nav class="nu-in-page-nav st-quick" aria-label="On this page" data-toc>
  <div class="nu-in-page-nav__inner">
    <p class="nu-text nu-text--label nu-in-page-nav__label" aria-hidden="true">On this page</p>
    <ul class="nu-in-page-nav__list">{links}</ul>
  </div>
</nav>'''
    blocks = ""
    for n, a in enumerate(x["areas"]):
        o = OFFICES[a["id"]]
        last = n == len(x["areas"]) - 1
        link = a["link"]
        ext = link[1].startswith("http")
        cue = f'<a class="nu-arrow-link{" nu-arrow-link--external" if ext else ""}" href="{href(link[1], "../")}">{link[0]} {i("external" if ext else "arrow")}</a>'
        if a["id"] == "government-relations":
            cue = f'<a class="nu-arrow-link" href="../public-policies/">Government relations and policy briefs {i("arrow")}</a>'
        media = "" if last else f'<figure class="nu-office-profile__media">{img(a["img"], a["alt"], "natural")}</figure>'
        blocks += f'''<article class="nu-office-profile" id="{a["id"]}" aria-labelledby="{a["id"]}-h">
  <div class="nu-office-profile__head">
    <h2 class="nu-heading nu-heading--h2" id="{a["id"]}-h">{a["name"]}</h2>
    <a class="nu-arrow-link st-office-team" href="../our-team/#team-{a["id"]}">Meet the {" ".join(w if w == "and" else w.capitalize() for w in a["name"].split())} team {i("arrow")}</a>
  </div>
  <div class="nu-office-profile__body">
    {"".join(f'<p class="nu-text nu-text--lead">{p}</p>' for p in a["body"])}
    <div class="nu-office-profile__handles">
      <h3 class="nu-heading nu-heading--h5">What we handle</h3>
      <ul class="nu-office-profile__list">{"".join(f"<li>{h}</li>" for h in o["handles"])}</ul>
    </div>
    {cue}
  </div>
  {media}
</article>'''
    body = hero_title("Our expertise", lead, [(UNIT, "../")]) + nav + f'<div class="st-band ea-offices">{blocks}</div>'
    page("expertise", "Our expertise", x["lead"], body, "expertise/")


# Brief dates are the PDFs' own (creation date); covers are each PDF's first page.
BRIEFS = {
    "Optimism-Anxiety-Northeastern-Gallup-Policy-Brief": ("2018-01", "January 2018", "Read the survey", "PDF, 20 MB"),
    "Federal-Work-Study-Policy-Brief": ("2022-04", "April 2022", "Read the brief", "PDF, 117 KB"),
    "Lifelong-Learning-Policy-Brief": ("2022-03", "March 2022", "Read the brief", "PDF, 805 KB"),
}


def policy():
    p = C["policy"]
    briefs = sorted(p["briefs"], key=lambda d: (not d["url"].endswith("Gallup-Policy-Brief.pdf"), [-int(x) for x in BRIEFS[d["url"].rsplit("/", 1)[1][:-4]][0].split("-")]))
    items = ""
    for n, d in enumerate(briefs):
        key = d["url"].rsplit("/", 1)[1][:-4]
        dt, when, action, fmt = BRIEFS[key]
        summary = d["desc"].rsplit(" · ", 1)[0]
        feat = n == 0
        items += f'''<li class="nu-publication-list__item{" nu-publication-list__item--featured" if feat else ""}">
      <span class="nu-publication-list__cover">{img(key + "-pdf.jpg", "", "4x5")}</span>
      <div class="nu-publication-list__body">
        <h3 class="nu-heading nu-heading--{"h2" if feat else "h3"}"><a class="nu-publication-list__link" href="{d["url"]}">{d["title"]}<span class="u-vh">, {fmt}</span></a></h3>
        <p class="nu-text nu-text--meta"><time datetime="{dt}">{when}</time>{" · with Gallup" if feat else ""}</p>
        <p class="nu-text{" nu-text--lead" if feat else ""}">{summary}</p>
        <span class="nu-arrow-link{"" if feat else " nu-arrow-link--sm"} nu-publication-list__cue" aria-hidden="true">{action} <span class="nu-publication-list__format">{fmt}</span>{i("arrow")}</span>
      </div>
    </li>'''
    gr = next(d for d in C["contact"]["depts"] if d["id"] == "gr")
    team = [(n, TEAM[n][0]) for n in ["Jack Cline", "Jesse Poon", "Abigail Robbins", "Maddy Brogan"]]  # the federal and state relations staff, not the whole office
    rows = "".join(f'''<li><article class="nu-person-card nu-person-card--compact">
  <span class="nu-person-card__media">{img("team/" + TEAM[n][1], "", "1x1")}</span>
  <div class="nu-person-card__body"><h3 class="nu-heading nu-heading--h5">{f'<a class="nu-person-card__link" href="{person_href(n, "../")}">{n}</a>' if n in LEADERS else n}</h3><p class="nu-text nu-text--small nu-person-card__title">{t}</p></div>
</article></li>''' for n, t in team)
    body = hero_title("Government relations", p["lead"], [(UNIT, "../"), ("Our expertise", "../expertise/")]) + f'''<section class="st-band st-band--first">
<div class="nu-publication-list">
  <header class="nu-publication-list__head">
    <h2 class="nu-heading nu-heading--h2" id="ea-briefs">Policy briefs</h2>
    <p class="nu-text nu-text--lead">{p["intro"]}</p>
  </header>
  <ol class="nu-publication-list__items">{items}</ol>
</div>
</section>
<section class="st-band ea-gr-team" aria-labelledby="ea-gr-h">
<div class="nu-card-grid nu-card-grid--grouped">
  <section class="nu-card-grid__group" aria-labelledby="ea-gr-h">
    <div class="nu-card-grid__group-head"><h2 class="nu-heading nu-heading--h3" id="ea-gr-h">Talk to our government relations team</h2>
      <p class="nu-text">{gr["desc"]}</p>
      <div class="ea-reach">{inline_contact(gr["tel"], gr["email"])}</div></div>
    <ul class="nu-card-grid__items" role="list">{rows}</ul>
  </section>
</div>
</section>'''
    page("public-policies", "Government relations", p["lead"], body, "expertise/")


def team_tabs(active, base):
    tabs = [("Team", "our-team/"), ("Leadership", "our-team/leadership/")]
    return '<nav class="nu-section-nav nu-section-nav--horizontal ea-sibling" aria-label="Our team"><ul class="nu-section-nav__list">' + "".join(
        f'<li><a class="nu-section-nav__link nu-nav-link" href="{base}{u}"{CUR if l == active else ""}>{l}</a></li>' for l, u in tabs) + "</ul></nav>"


def team():
    groups = ""
    for g, names in GROUPS:
        gid = "team-" + slug(g)
        cards = ""
        for n in names:
            t, f = TEAM[n]
            name = f'<a class="nu-person-card__link" href="leadership/bio/{LEADERS[n]["slug"]}/">{n}</a>' if n in LEADERS else n
            cards += f'''<li id="{slug(n)}"><article class="nu-person-card nu-person-card--compact">
  <span class="nu-person-card__media">{img("team/" + f, "", "1x1")}</span>
  <div class="nu-person-card__body"><h4 class="nu-heading nu-heading--h5">{name}</h4><p class="nu-text nu-text--small nu-person-card__title">{t}</p></div>
</article></li>'''
        groups += f'''<section class="nu-card-grid__group" aria-labelledby="{gid}">
    <div class="nu-card-grid__group-head"><h3 class="nu-heading nu-heading--h3" id="{gid}">{g}</h3></div>
    <ul class="nu-card-grid__items" role="list">{cards}</ul>
  </section>'''
    body = hero_title("Our team", "The people who tell Northeastern’s story: media and public relations, government affairs, and city and community engagement.", [(UNIT, "../")]) + team_tabs("Team", "../") + f'''<section class="st-band st-band--first ea-team" aria-label="Our team by office">
<div class="nu-card-grid nu-card-grid--grouped">{groups}</div>
</section>'''
    page("our-team", "Our team", "Meet the External Affairs team at Northeastern University.", body, "our-team/")


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
    <div class="nu-featured-person__name"><h2 class="nu-heading nu-heading--h2" id="ld-{l["slug"]}"><a href="bio/{l["slug"]}/">{l["name"]}</a></h2><p class="nu-text nu-text--small nu-featured-person__title">{l["title"]}</p></div>
    <div class="nu-featured-person__about"><p class="nu-text">{l["fullbio"][0]}</p>
      <div class="nu-featured-person__actions"><a class="nu-arrow-link" href="bio/{l["slug"]}/">Full bio<span class="u-vh">, {l["name"]}</span>{i("arrow")}</a>{team_link(l["name"], "../")}</div></div>
  </div>
</article>''' for l in rest)
    body = f'''{hero_title("Leadership", "The leaders of Northeastern’s communications, city and community engagement, and government relations teams.", [(UNIT, "../../"), ("Our team", "../")])}
{team_tabs("Leadership", "../../")}
<div class="nu-leadership ea-leaders">{feat}<div class="nu-leadership__rows">{rows}</div></div>'''
    page("our-team/leadership", "Leadership", "Leadership of External Affairs at Northeastern University.", body, "our-team/")


def bios():
    L = C["leaders"]
    for n, l in enumerate(L):
        prv, nxt = L[(n - 1) % len(L)], L[(n + 1) % len(L)]
        prose = "".join(f"<p>{p}</p>" for p in l["fullbio"])
        body = f'''<div class="nu-profile">
<div class="nu-profile__top">
<header class="nu-profile-header nu-profile-header--contact">
  <div class="nu-profile-header__media">{img(l["photo"], l["name"], "4x5")}</div>
  <div class="nu-profile-header__body">
    <div class="nu-profile-header__intro">
      <a class="nu-arrow-link nu-arrow-link--back nu-arrow-link--sm" href="../../">{i("arrow-left")}Leadership</a>
      <h1 class="nu-heading nu-heading--h1">{l["name"]}</h1>
      <p class="nu-text nu-text--lead nu-profile-header__role">{l["title"]}</p>
      {team_link(l["name"], "../../../")}
    </div>
  </div>
</header>
</div>
<div class="nu-profile__body">
  <div class="nu-profile__main"><div class="nu-prose">{prose}</div>
    <nav class="nu-profile-header__pager" aria-label="Leadership profiles">
      <a class="nu-arrow-link nu-arrow-link--back" href="../{prv["slug"]}/">{i("arrow-left")}Previous: {prv["name"]}</a>
      <a class="nu-arrow-link" href="../{nxt["slug"]}/">Next: {nxt["name"]}{i("arrow")}</a>
    </nav></div>
</div>
</div>'''
        page(f"our-team/leadership/bio/{l['slug']}", l["name"], f'{l["name"]}, {l["title"]}, Northeastern University.', body, "our-team/")


def contact():
    c = C["contact"]
    blocks = ""
    for d in c["depts"]:
        items = ""
        if d.get("address"):
            items += f'<address class="nu-contact-item">{i("location")}<span class="nu-contact-item__label">Address</span><span class="nu-contact-item__value">{"<br>".join(ADDRESS)}<br><a class="nu-link" href="https://www.google.com/maps/search/?api=1&amp;query=716+Columbus+Avenue+Boston+MA+02120">Map</a></span></address>'
        items += contact_items(d)
        hid = "media" if d["id"] == "comms" else d["id"]
        extra = f'<a class="nu-arrow-link nu-arrow-link--sm nu-arrow-link--external" href="https://news.northeastern.edu/media-inquiries/">Media inquiries and experts {i("external")}</a>' if d["id"] == "comms" else ""
        blocks += f'''<section class="nu-contact-block" id="{hid}" aria-labelledby="ct-{d["id"]}">
  <div class="nu-contact-block__label"><h2 class="nu-heading nu-heading--h4" id="ct-{d["id"]}">{d["name"]}</h2><p class="nu-text nu-text--small">{d["desc"]}</p></div>
  <div class="nu-contact-block__body"><div class="nu-contact-block__items">{items}</div>{extra}</div>
</section>'''
    lead = c["lead"].split(". ")[-1]
    body = hero_title("Contact us", lead, [(UNIT, "../")]) + f'''<section class="st-band st-contact">
  <div class="st-contact__blocks">{blocks}</div>
</section>'''
    page("contact", "Contact us", "Contact External Affairs at Northeastern University: communications and media relations, city and community engagement, and government relations.", body, "contact/")


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
