#!/usr/bin/env python3
"""Idempotent site updater: WhatsApp bubble, favicon, gift cards, FlexPay, QA fixes."""
import os, re, glob

REPO = os.getcwd()
PHONE = '19193486268'
OG_IMG = 'https://destinaratravel.com/assets/img/photo-1507525428034-b723cf961d3e-aa86893f.jpg'
FAVICON = '<link rel="icon" type="image/png" href="/destinara-logo.png">'

WA_MSG = 'Hi%20Destinara%2C%20I%27d%20like%20help%20planning%20a%20trip'
WA_BUBBLE = (
'<!-- wa-bubble -->'
'<style>#wa-bubble{position:fixed;right:20px;bottom:20px;z-index:9998;display:flex;align-items:center;justify-content:center;width:58px;height:58px;border-radius:50%;background:#25D366;box-shadow:0 4px 14px rgba(0,0,0,.25);transition:transform .2s,box-shadow .2s;text-decoration:none}'
'#wa-bubble:hover{transform:scale(1.08);box-shadow:0 6px 20px rgba(0,0,0,.3)}'
'@media(max-width:768px){#wa-bubble{width:52px;height:52px;right:16px;bottom:16px}}</style>'
'<a id="wa-bubble" href="https://wa.me/' + PHONE + '?text=' + WA_MSG + '" target="_blank" rel="noopener noreferrer" aria-label="Chat with us on WhatsApp" title="Chat on WhatsApp">'
'<svg viewBox="0 0 32 32" width="32" height="32" fill="#fff" aria-hidden="true"><path d="M16 .5C7.4.5.5 7.4.5 16c0 2.8.7 5.5 2.1 7.9L.3 31.5l7.8-2.3c2.3 1.3 4.9 1.9 7.6 1.9h.3c8.6 0 15.5-6.9 15.5-15.5S24.6.5 16 .5zm0 28.3c-2.4 0-4.7-.6-6.7-1.8l-.5-.3-4.6 1.4 1.4-4.5-.3-.5C4.2 20.7 3.5 18.4 3.5 16 3.5 9 9 3.5 16 3.5S28.5 9 28.5 16 23 28.8 16 28.8zm7-9.4c-.4-.2-2.3-1.1-2.6-1.3-.3-.1-.6-.2-.8.2-.2.4-.9 1.3-1.2 1.5-.2.2-.4.3-.8.1-.4-.2-1.6-.6-3.1-1.9-1.1-1-1.9-2.3-2.2-2.7-.2-.4 0-.6.2-.8.2-.2.4-.4.6-.7.2-.2.3-.4.4-.7.1-.3.1-.5 0-.7-.1-.2-.8-2-1.1-2.7-.3-.7-.6-.6-.8-.6h-.7c-.2 0-.6.1-.9.4-.3.4-1.2 1.2-1.2 2.9s1.2 3.4 1.4 3.6c.2.2 2.4 3.7 5.9 5.2.8.4 1.5.6 2 .8.8.3 1.6.2 2.2.1.7-.1 2.3-.9 2.6-1.8.3-.9.3-1.6.2-1.8-.1-.2-.3-.3-.7-.5z"/></svg></a>'
'<!-- /wa-bubble -->'
)

def html_files():
    return (glob.glob(os.path.join(REPO,'*.html')) +
            glob.glob(os.path.join(REPO,'destinations','*.html')) +
            glob.glob(os.path.join(REPO,'blog','*.html')))

def read(p):
    with open(p, encoding='utf-8') as f: return f.read()
def write(p, s):
    with open(p,'w',encoding='utf-8') as f: f.write(s)

log = []

# ---------- 1. GIFT CARDS PAGE ----------
GIFT_MAIN = '''<section id="main-content" class="page-hero" style="background:linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-light) 100%);padding:120px 0 60px;text-align:center">
<div class="container">
<p class="section-label" style="color:var(--color-accent)">&#127873; The Gift of Unforgettable Travel</p>
<h1 style="font-family:var(--font-display);font-size:2.8rem;color:var(--color-white);margin:10px 0 16px">Destinara Travel Gift Cards</h1>
<p style="color:rgba(255,255,255,.9);max-width:680px;margin:0 auto;font-size:1.1rem;line-height:1.6">Give someone the journey of a lifetime. A Destinara gift card can be applied toward any cruise, vacation, honeymoon, or curated experience &mdash; redeemable with a personal travel advisor who plans every detail.</p>
</div>
</section>
<section style="padding:60px 20px;background:var(--color-bg,#faf8f5)">
<div style="max-width:1000px;margin:0 auto">
<div style="display:flex;flex-wrap:wrap;gap:22px;justify-content:center;margin-bottom:50px">
<div style="flex:1 1 260px;max-width:300px;background:#fff;border-radius:14px;padding:28px;box-shadow:0 6px 20px rgba(0,0,0,.06);text-align:center">
<div style="font-size:2rem;margin-bottom:10px">&#128176;</div>
<h3 style="font-family:var(--font-display);color:var(--color-primary,#0D5C5C);font-size:1.2rem;margin:0 0 8px">Any Amount</h3>
<p style="color:#555;line-height:1.55;margin:0">Choose any value from $100 to $10,000+. Perfect for weddings, honeymoons, anniversaries, milestone birthdays, or corporate gifting.</p>
</div>
<div style="flex:1 1 260px;max-width:300px;background:#fff;border-radius:14px;padding:28px;box-shadow:0 6px 20px rgba(0,0,0,.06);text-align:center">
<div style="font-size:2rem;margin-bottom:10px">&#9992;&#65039;</div>
<h3 style="font-family:var(--font-display);color:var(--color-primary,#0D5C5C);font-size:1.2rem;margin:0 0 8px">Redeem on Anything</h3>
<p style="color:#555;line-height:1.55;margin:0">Applies to cruises, resort stays, tours, honeymoons, VIP sports trips &mdash; any journey Destinara plans. No blackout dates on planning.</p>
</div>
<div style="flex:1 1 260px;max-width:300px;background:#fff;border-radius:14px;padding:28px;box-shadow:0 6px 20px rgba(0,0,0,.06);text-align:center">
<div style="font-size:2rem;margin-bottom:10px">&#128140;</div>
<h3 style="font-family:var(--font-display);color:var(--color-primary,#0D5C5C);font-size:1.2rem;margin:0 0 8px">A Personal Touch</h3>
<p style="color:#555;line-height:1.55;margin:0">Add a custom message and we&rsquo;ll deliver a beautifully presented gift card &mdash; digital or printed &mdash; on your chosen date.</p>
</div>
</div>
<div style="max-width:640px;margin:0 auto;background:#fff;border-radius:16px;padding:36px;box-shadow:0 10px 30px rgba(0,0,0,.08)">
<h2 style="font-family:var(--font-display);color:var(--color-primary,#0D5C5C);font-size:1.6rem;text-align:center;margin:0 0 6px">Request a Gift Card</h2>
<p style="text-align:center;color:#666;margin:0 0 24px">Tell us a few details and we&rsquo;ll be in touch within one business day to arrange it.</p>
<form action="https://formsubmit.co/info@destinaratravel.com" method="POST">
<input type="hidden" name="_subject" value="New Gift Card request &mdash; Destinara Travel">
<input type="hidden" name="_next" value="https://destinaratravel.com/thank-you.html">
<input type="hidden" name="_captcha" value="false">
<input type="text" name="_honey" style="display:none">
<div style="display:grid;grid-template-columns:1fr 1fr;gap:14px">
<div style="grid-column:1/-1"><label style="display:block;font-weight:600;color:#333;margin-bottom:5px">Your Name *</label><input type="text" name="Purchaser Name" required style="width:100%;padding:12px;border:1px solid #ddd;border-radius:8px;font-size:1rem"></div>
<div><label style="display:block;font-weight:600;color:#333;margin-bottom:5px">Your Email *</label><input type="email" name="Email" required style="width:100%;padding:12px;border:1px solid #ddd;border-radius:8px;font-size:1rem"></div>
<div><label style="display:block;font-weight:600;color:#333;margin-bottom:5px">Phone</label><input type="tel" name="Phone" style="width:100%;padding:12px;border:1px solid #ddd;border-radius:8px;font-size:1rem"></div>
<div><label style="display:block;font-weight:600;color:#333;margin-bottom:5px">Gift Amount *</label><select name="Gift Amount" required style="width:100%;padding:12px;border:1px solid #ddd;border-radius:8px;font-size:1rem;background:#fff"><option value="">Select an amount</option><option>$100</option><option>$250</option><option>$500</option><option>$1,000</option><option>$2,500</option><option>$5,000</option><option>Other (tell us below)</option></select></div>
<div><label style="display:block;font-weight:600;color:#333;margin-bottom:5px">Delivery</label><select name="Delivery" style="width:100%;padding:12px;border:1px solid #ddd;border-radius:8px;font-size:1rem;background:#fff"><option>Digital (email)</option><option>Printed (mail)</option><option>Not sure yet</option></select></div>
<div style="grid-column:1/-1"><label style="display:block;font-weight:600;color:#333;margin-bottom:5px">Recipient Name</label><input type="text" name="Recipient Name" style="width:100%;padding:12px;border:1px solid #ddd;border-radius:8px;font-size:1rem"></div>
<div style="grid-column:1/-1"><label style="display:block;font-weight:600;color:#333;margin-bottom:5px">Personal Message / Notes</label><textarea name="Message" rows="3" style="width:100%;padding:12px;border:1px solid #ddd;border-radius:8px;font-size:1rem;resize:vertical"></textarea></div>
</div>
<button type="submit" style="width:100%;margin-top:18px;background:var(--color-accent,#C4956B);color:#fff;border:none;padding:15px;border-radius:30px;font-size:1.05rem;font-weight:600;cursor:pointer">Request My Gift Card &rarr;</button>
<p style="text-align:center;font-size:.8rem;color:#888;margin:14px 0 0">Prefer to talk it through? Call <a href="tel:+19193486268" style="color:var(--color-primary,#0D5C5C)">(919) 348-6268</a> or <a href="/consultation.html" style="color:var(--color-primary,#0D5C5C)">book a free call</a>.</p>
</form>
</div>
</div>
</section>
'''

def build_gift_cards():
    path = os.path.join(REPO,'gift-cards.html')
    donor = read(os.path.join(REPO,'vacations.html'))
    cut = donor.index('<section id="main-content"')
    head_nav = donor[:cut]
    tail = donor[donor.index('<footer'):]
    # fix head metadata
    head_nav = re.sub(r'<title>.*?</title>', '<title>Travel Gift Cards | Destinara Travel</title>', head_nav, count=1, flags=re.S)
    head_nav = re.sub(r'<meta name="description" content="[^"]*">',
                      '<meta name="description" content="Give the gift of travel with a Destinara Travel gift card &mdash; redeemable toward any cruise, vacation, or honeymoon, planned by a personal advisor. Request yours today.">',
                      head_nav, count=1)
    head_nav = re.sub(r'<link rel="canonical"[^>]*>', '<link rel="canonical" href="https://destinaratravel.com/gift-cards.html">', head_nav, count=1)
    head_nav = re.sub(r'<meta property="og:title"[^>]*>', '<meta property="og:title" content="Travel Gift Cards | Destinara Travel">', head_nav, count=1)
    head_nav = re.sub(r'<meta property="og:url"[^>]*>', '<meta property="og:url" content="https://destinaratravel.com/gift-cards.html">', head_nav, count=1)
    head_nav = re.sub(r'<meta property="og:description"[^>]*>', '<meta property="og:description" content="Give the gift of travel &mdash; a Destinara gift card redeemable toward any journey.">', head_nav, count=1)
    write(path, head_nav + GIFT_MAIN + tail)
    log.append('built gift-cards.html')

# ---------- 2. FLEXPAY SECTION (cruises) ----------
FLEXPAY = '''<section id="financing" style="padding:60px 20px;background:linear-gradient(135deg,#0D5C5C,#0a4a4a)">
<div style="max-width:920px;margin:0 auto;text-align:center;color:#fff">
<p style="text-transform:uppercase;letter-spacing:2px;font-size:.8rem;color:#C4956B;margin:0 0 8px">Cruise Now, Pay Over Time</p>
<h2 style="font-family:var(--font-display,'Playfair Display',serif);font-size:2.1rem;margin:0 0 14px;color:#fff">Flexible Cruise Financing with FlexPay</h2>
<p style="max-width:700px;margin:0 auto 30px;color:rgba(255,255,255,.85);line-height:1.65">Spread the cost of your dream cruise into manageable monthly payments with FlexPay. Lock in today&rsquo;s fare, reserve your stateroom with a low deposit, and pay the balance over time &mdash; so you can sail sooner without straining your budget.</p>
<div style="display:flex;flex-wrap:wrap;gap:18px;justify-content:center;margin-bottom:34px">
<div style="flex:1 1 220px;max-width:260px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.15);border-radius:12px;padding:22px"><div style="font-size:1.8rem;margin-bottom:8px">&#129534;</div><h3 style="font-size:1.1rem;color:#fff;margin:0 0 6px;font-family:var(--font-display,serif)">Low Deposit to Book</h3><p style="color:rgba(255,255,255,.8);font-size:.92rem;line-height:1.5;margin:0">Reserve your cabin now and secure current pricing and perks.</p></div>
<div style="flex:1 1 220px;max-width:260px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.15);border-radius:12px;padding:22px"><div style="font-size:1.8rem;margin-bottom:8px">&#128197;</div><h3 style="font-size:1.1rem;color:#fff;margin:0 0 6px;font-family:var(--font-display,serif)">Easy Monthly Payments</h3><p style="color:rgba(255,255,255,.8);font-size:.92rem;line-height:1.5;margin:0">Pay the balance over time on a schedule that fits your budget.</p></div>
<div style="flex:1 1 220px;max-width:260px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.15);border-radius:12px;padding:22px"><div style="font-size:1.8rem;margin-bottom:8px">&#9989;</div><h3 style="font-size:1.1rem;color:#fff;margin:0 0 6px;font-family:var(--font-display,serif)">No Surprises</h3><p style="color:rgba(255,255,255,.8);font-size:.92rem;line-height:1.5;margin:0">Your advisor explains the terms up front &mdash; clear, simple, transparent.</p></div>
</div>
<a href="/consultation.html" style="display:inline-block;background:#C4956B;color:#fff;text-decoration:none;padding:14px 34px;border-radius:30px;font-weight:600;font-size:1.02rem">Ask Us About FlexPay &rarr;</a>
<p style="font-size:.78rem;color:rgba(255,255,255,.6);margin:16px auto 0;max-width:640px">FlexPay availability and terms vary by cruise line and itinerary. Your Destinara advisor will walk you through the options and eligibility.</p>
</div>
</section>
'''

# ---------- 3. HOMEPAGE PROMO STRIP (gift cards + financing) ----------
HOME_PROMO = '''<section id="give-travel" style="padding:56px 20px;background:var(--color-bg,#faf8f5)">
<div style="max-width:1000px;margin:0 auto;display:flex;flex-wrap:wrap;gap:22px;justify-content:center">
<div style="flex:1 1 320px;max-width:460px;background:#fff;border-radius:16px;padding:32px;box-shadow:0 8px 24px rgba(0,0,0,.07);text-align:center">
<div style="font-size:2.2rem;margin-bottom:10px">&#127873;</div>
<h3 style="font-family:var(--font-display,'Playfair Display',serif);color:var(--color-primary,#0D5C5C);font-size:1.4rem;margin:0 0 10px">Give the Gift of Travel</h3>
<p style="color:#555;line-height:1.6;margin:0 0 18px">A Destinara gift card turns any occasion into the start of an unforgettable journey &mdash; redeemable toward any trip we plan.</p>
<a href="/gift-cards.html" style="display:inline-block;background:var(--color-accent,#C4956B);color:#fff;text-decoration:none;padding:12px 28px;border-radius:30px;font-weight:600">Explore Gift Cards &rarr;</a>
</div>
<div style="flex:1 1 320px;max-width:460px;background:#fff;border-radius:16px;padding:32px;box-shadow:0 8px 24px rgba(0,0,0,.07);text-align:center">
<div style="font-size:2.2rem;margin-bottom:10px">&#128181;</div>
<h3 style="font-family:var(--font-display,'Playfair Display',serif);color:var(--color-primary,#0D5C5C);font-size:1.4rem;margin:0 0 10px">Cruise Now, Pay Over Time</h3>
<p style="color:#555;line-height:1.6;margin:0 0 18px">Book your cruise with a low deposit and spread the balance into easy monthly payments with FlexPay financing.</p>
<a href="/cruises.html#financing" style="display:inline-block;background:var(--color-accent,#C4956B);color:#fff;text-decoration:none;padding:12px 28px;border-radius:30px;font-weight:600">About FlexPay &rarr;</a>
</div>
</div>
</section>
'''

# ---------- global passes ----------
def global_passes():
    for p in html_files():
        h = read(p); orig = h
        # favicon
        if 'rel="icon"' not in h:
            h = h.replace('<head>', '<head>\n' + FAVICON, 1)
        # whatsapp bubble
        if 'id="wa-bubble"' not in h and '</body>' in h:
            h = h.replace('</body>', WA_BUBBLE + '\n</body>', 1)
        # footer gift cards link
        anchor = '<div class="footer-links" aria-label="Footer navigation">'
        if anchor in h and '>Gift Cards</a>' not in h:
            h = h.replace(anchor, anchor + '<a href="/gift-cards.html">Gift Cards</a>', 1)
        if h != orig:
            write(p, h); log.append('global: ' + os.path.relpath(p, REPO))

# ---------- targeted edits ----------
def edit_find_my_vacation():
    p = os.path.join(REPO,'find-my-vacation.html'); h = read(p); orig = h
    if 'og:image' not in h:
        h = h.replace('<meta property="og:url" content="https://destinaratravel.com/find-my-vacation.html">',
            '<meta property="og:url" content="https://destinaratravel.com/find-my-vacation.html">\n'
            '<meta property="og:image" content="' + OG_IMG + '">\n'
            '<meta property="og:type" content="website">\n'
            '<meta name="twitter:card" content="summary_large_image">\n'
            '<meta name="twitter:image" content="' + OG_IMG + '">', 1)
    if '_ac=new AbortController' not in h:
        h = h.replace("fetch('/api/estimate', {\nmethod: 'POST',",
                      "var _ac=new AbortController();var _to=setTimeout(function(){try{_ac.abort();}catch(e){}},20000);\nfetch('/api/estimate', {\nsignal: _ac.signal,\nmethod: 'POST',", 1)
        h = h.replace('.then(data => { clearInterval(msgInterval);', '.then(data => { clearTimeout(_to); clearInterval(msgInterval);', 1)
        h = h.replace('.catch(err => {\nclearInterval(msgInterval);', '.catch(err => {\nclearTimeout(_to);\nclearInterval(msgInterval);', 1)
    if h != orig:
        write(p, h); log.append('edited find-my-vacation.html (og + timeout)')

def edit_cruises():
    p = os.path.join(REPO,'cruises.html'); h = read(p); orig = h
    if 'id="financing"' not in h:
        # insert before the travel-protection callout section
        marker = '<section style="padding:36px 20px 56px"><div style="max-width:780px;margin:0 auto;background:var(--color-bg,#faf8f5);border:1px solid rgba(13,92,92,0.12);border-left:4px solid var(--color-accent,#C4956B)'
        if marker in h:
            h = h.replace(marker, FLEXPAY + marker, 1)
        else:
            h = h.replace('<footer>', FLEXPAY + '<footer>', 1)
    if h != orig:
        write(p, h); log.append('edited cruises.html (FlexPay)')

def edit_index():
    p = os.path.join(REPO,'index.html'); h = read(p); orig = h
    if 'id="give-travel"' not in h:
        h = h.replace('<footer><div class="footer-newsletter"', HOME_PROMO + '<footer><div class="footer-newsletter"', 1)
    if h != orig:
        write(p, h); log.append('edited index.html (gift/financing promo)')

def edit_blog_canonicals():
    for slug in ['amalfi-coast-guide','costa-rica-adventure','santorini-guide']:
        p = os.path.join(REPO,'blog', slug + '.html'); h = read(p); orig = h
        h = h.replace('href="https://destinaratravel.com/blog/' + slug + '"', 'href="https://destinaratravel.com/blog/' + slug + '.html"')
        if h != orig:
            write(p, h); log.append('canonical fixed: ' + slug)

def edit_titles_descriptions():
    repl = [
      ('destinations/nuremberg-christmas-market.html',
        '<title>Nuremberg Christmas Market Destination Guide | Destinara Travel</title>',
        '<title>Nuremberg Christmas Market Guide | Destinara Travel</title>'),
      ('destinations/strasbourg-christmas-market.html',
        '<title>Strasbourg Christmas Market Destination Guide | Destinara Travel</title>',
        '<title>Strasbourg Christmas Market Guide | Destinara Travel</title>'),
      ("blog/charleston-sc-guide.html",
        "<title>Charleston, SC: The South's Most Charming City | Destinara Travel</title>",
        "<title>Charleston, SC Travel Guide | Destinara Travel</title>"),
      ('blog/santorini-guide.html',
        '<title>Santorini, Greece: The Complete Island Guide | Destinara Travel</title>',
        '<title>Santorini, Greece Island Guide | Destinara Travel</title>'),
      ('destinations/bali-indonesia.html',
        '<meta name="description" content="The Island of the Gods — Temples, Rice Terraces &amp; Spiritual Serenity…"',
        '<meta name="description" content="The Island of the Gods &mdash; explore Bali&rsquo;s sacred temples, emerald rice terraces, world-class resorts and spiritual serenity. Plan your luxury Bali escape with Destinara."'),
      ('destinations/hawaii.html',
        '<meta name="description" content="Island Paradise — Volcanoes, Waterfalls &amp; Aloha Spirit…"',
        '<meta name="description" content="Island paradise &mdash; discover Hawaii&rsquo;s volcanoes, waterfalls, black-sand beaches and aloha spirit across every island. Plan your luxury Hawaii vacation with Destinara."'),
      ('destinations/iceland.html',
        '<meta name="description" content="Land of Fire &amp; Ice — Northern Lights &amp; Volcanic Wonders…"',
        '<meta name="description" content="Land of fire and ice &mdash; chase Iceland&rsquo;s Northern Lights, glaciers, waterfalls and volcanic wonders. Plan your luxury Iceland adventure with Destinara."'),
    ]
    for fn, old, new in repl:
        p = os.path.join(REPO, fn)
        if not os.path.exists(p): continue
        h = read(p)
        if old in h:
            write(p, h.replace(old, new, 1)); log.append('meta updated: ' + fn)

def edit_sitemap():
    p = os.path.join(REPO,'sitemap.xml'); h = read(p); orig = h
    # remove trip-estimator url block
    h = re.sub(r'\s*<url>\s*<loc>https://destinaratravel\.com/trip-estimator\.html</loc>.*?</url>', '', h, flags=re.S)
    # add gift-cards before </urlset> if missing
    if 'gift-cards.html' not in h:
        entry = ('    <url>\n          <loc>https://destinaratravel.com/gift-cards.html</loc>\n'
                 '          <lastmod>2026-06-19</lastmod>\n          <changefreq>monthly</changefreq>\n'
                 '          <priority>0.7</priority>\n    </url>\n')
        h = h.replace('</urlset>', entry + '</urlset>', 1)
    if h != orig:
        write(p, h); log.append('sitemap updated')

build_gift_cards()
edit_find_my_vacation()
edit_cruises()
edit_index()
edit_blog_canonicals()
edit_titles_descriptions()
edit_sitemap()
global_passes()

print('\n'.join(log))
print('TOTAL ACTIONS:', len(log))
