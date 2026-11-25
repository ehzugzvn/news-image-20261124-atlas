#!/usr/bin/env python3
"""ATLAS flagship renderer for news-image-20261124.
Draws the whole 1024x1024 page in code (PIL vector-style illustration).
Facts ONLY from STORIES.md (24 Nov 2026, verified pack)."""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024

NAVY = (13, 32, 64)
NAVY2 = (24, 52, 96)
RED = (178, 24, 28)
RED2 = (200, 40, 40)
GOLD = (184, 134, 11)
TEAL = (14, 110, 110)
GREEN = (28, 120, 60)
ORANGE = (200, 100, 10)
PURPLE = (96, 60, 140)
INK = (18, 18, 18)
GREY = (90, 90, 90)
LIGHT = (240, 242, 245)
LIGHT2 = (232, 236, 242)
WHITE = (255, 255, 255)
CREAM = (250, 244, 228)
SEA = (120, 180, 215)
SEA2 = (70, 140, 190)
SAND = (222, 200, 150)

def F(name, size):
    return ImageFont.truetype(os.path.join(HERE, "fonts", name), size)

FB = lambda s: F("LiberationSans-Bold.ttf", s)
FR = lambda s: F("LiberationSans-Regular.ttf", s)
SERB = lambda s: F("LiberationSerif-Bold.ttf", s)

def tw(draw, text, font):
    b = draw.textbbox((0, 0), text, font=font)
    return b[2] - b[0]

def wrap(draw, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if tw(draw, t, font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines

def centre(draw, x, y, w, text, font, fill):
    draw.text((x + (w - tw(draw, text, font)) / 2, y), text, font=font, fill=fill)

def badge(draw, x, y, text, font, bg, fg=WHITE, pad=7):
    w_ = tw(draw, text, font) + pad * 2
    h_ = font.size + 9
    draw.rounded_rectangle([x, y, x + w_, y + h_], radius=5, fill=bg)
    draw.text((x + pad, y + 4), text, font=font, fill=fg)
    return w_

def tag_badge(draw, x, y, tag):
    col = {"CONFIRMED": GREEN, "OFFICIAL": NAVY2, "REPORTED": ORANGE,
           "CLAIM": RED}.get(tag, GREY)
    return badge(draw, x, y, tag, FB(11), col)

img = Image.new("RGB", (W, H), WHITE)
d = ImageDraw.Draw(img)
MX = 24
CW = W - 2 * MX  # 976

# ---- top red bar + eyebrow ----
d.rectangle([0, 0, W, 9], fill=RED)
centre(d, 0, 16, W, "THE  WORLD  IN  ONE  PAGE", FB(17), NAVY)
# ---- GIANT DATE (largest element on the page) ----
centre(d, 0, 38, W, "TUESDAY 24 NOVEMBER 2026", FB(66), NAVY)
d.rectangle([MX, 116, W - MX, 118], fill=GOLD)
# ---- sub-strip ----
d.rectangle([MX, 122, W - MX, 148], fill=NAVY)
centre(d, MX, 129, CW, "30 STORIES  ·  6 REGIONS  ·  9 FIELDS  ·  EVERY ONE FROM THIS TUESDAY",
       FB(19), WHITE)

# ---- UTC TIMELINE ----
d.rectangle([MX, 154, W - MX, 188], fill=LIGHT)
d.text((MX + 8, 158), "UTC TIMELINE — WHEN THE DAY BROKE", font=FB(14), fill=NAVY)
tl = [("00:00", "HORMUZ"), ("02:09", "EL CHAPO"), ("08:14", "UKRAINE SHIPS"),
      ("11:45", "VILLAVICENCIO"), ("14:27", "PIF TOWER"), ("17:35", "CARTAGENA"),
      ("20:41", "HUAWEI")]
x0, x1 = MX + 10, W - MX - 10
d.line([(x0, 174), (x1, 174)], fill=NAVY2, width=2)
for i, (t, lab) in enumerate(tl):
    x = x0 + i * (x1 - x0) // (len(tl) - 1)
    d.ellipse([x - 4, 170, x + 4, 178], fill=RED)
    if i == 0:
        d.text((x0, 179), t, font=FB(10), fill=NAVY)
    elif i == len(tl) - 1:
        d.text((x1 - 28, 179), t, font=FB(10), fill=NAVY)
    else:
        centre(d, x - 34, 179, 68, t, FB(10), NAVY)

# ---- DAY IN NUMBERS ----
d.text((MX, 190), "THE DAY IN NUMBERS", font=FB(14), fill=NAVY)
nums = [("4", "tankers hit"), ("25", "hostages"), ("11", "wounded Riyadh"),
        ("10/12", "Huawei counts"), ("272", "Gaza cases"), ("700,000+", "dead or missing")]
bw = (CW - 5 * 8) // 6
for i, (n, lab) in enumerate(nums):
    x = MX + i * (bw + 8)
    d.rounded_rectangle([x, 208, x + bw, 244], radius=6, fill=LIGHT2)
    centre(d, x, 211, bw, n, FB(19), RED)
    centre(d, x, 231, bw, lab, FR(11), NAVY)

# ---- LEADS: 2x2 grid ----
d.text((MX, 252), "THE FOUR LEADS", font=FB(15), fill=NAVY)
LW, LH = (CW - 12) // 2, 140
LY = 272

def lead_cell(x, y, num, kicker, headline, summary, accent):
    d.rounded_rectangle([x, y, x + LW, y + LH], radius=8, outline=NAVY, width=2)
    d.rounded_rectangle([x, y, x + 34, y + 30], radius=8, fill=RED)
    d.text((x + 11, y + 4), str(num), font=FB(20), fill=WHITE)
    d.text((x + 42, y + 5), kicker, font=FB(13), fill=accent)
    return x, y

def lead_text(x, y, headline, summary):
    lines = wrap(d, headline, FB(19), LW - 16)
    yy = y + 72
    for ln in lines[:2]:
        d.text((x + 8, yy), ln, font=FB(19), fill=INK)
        yy += 21
    sl = wrap(d, summary, FR(13), LW - 16)
    for ln in sl[:2]:
        d.text((x + 8, yy), ln, font=FR(13), fill=(50, 50, 50))
        yy += 15

# L1 Huawei courtroom
x, y = MX, LY
lead_cell(x, y, 1, "HUAWEI GUILTY  ·  20:41 UTC", "", "", RED)
d.rectangle([x + 2, y + 32, x + LW - 2, y + 68], fill=NAVY2)
for cx in (x + 60, x + 238, x + 416):
    d.rectangle([cx - 7, y + 38, cx + 7, y + 68], fill=CREAM)
d.rectangle([x + 2, y + 32, x + LW - 2, y + 36], fill=GOLD)
# gavel: head + handle
d.rectangle([x + 300, y + 44, x + 352, y + 56], fill=(120, 72, 20))
d.line([(x + 352, y + 50), (x + 392, y + 62)], fill=(120, 72, 20), width=6)
d.ellipse([x + 388, y + 58, x + 398, y + 66], fill=(120, 72, 20))
badge(d, x + 8, y + 38, "10 OF 12 COUNTS", FB(12), RED)
lead_text(x, y, "Huawei guilty on 10 of 12 counts",
          "US jury: trade-secret theft + bank fraud. Racketeering: acquitted. Appeal planned.")

# L2 Hormuz strait map
x, y = MX + LW + 12, LY
lead_cell(x, y, 2, "HORMUZ IN FLAMES  ·  00:00 UTC", "", "", RED)
d.rectangle([x + 2, y + 32, x + LW - 2, y + 68], fill=SEA)
d.polygon([(x + 2, y + 32), (x + 200, y + 32), (x + 150, y + 68), (x + 2, y + 68)], fill=SAND)
d.polygon([(x + 300, y + 32), (x + LW - 2, y + 32), (x + LW - 2, y + 68), (x + 340, y + 68)], fill=SAND)
for tx in (x + 210, x + 260, x + 310):
    d.rectangle([tx, y + 52, tx + 34, y + 62], fill=(40, 40, 40))
    d.polygon([(tx + 8, y + 52), (tx + 14, y + 42), (tx + 20, y + 52)], fill=RED2)
    d.ellipse([tx + 44, y + 52, tx + 50, y + 58], fill=NAVY)
badge(d, x + 8, y + 38, "4 TANKERS HIT — CLAIM UNCONFIRMED", FB(11), RED)
lead_text(x, y, "Four tankers hit by mines in Hormuz",
          "Iran claims mines; maritime centre: unconfirmed. IRGC also hit a container ship.")

# L3 Ukraine sea map
x, y = MX, LY + LH + 10
lead_cell(x, y, 3, "UKRAINE HITS RUSSIAN SHIPS  ·  08:14 UTC", "", "", NAVY2)
d.rectangle([x + 2, y + 32, x + LW - 2, y + 68], fill=SEA)
d.polygon([(x + 2, y + 32), (x + 180, y + 32), (x + 150, y + 68), (x + 2, y + 68)], fill=(190, 220, 190))
d.polygon([(x + 330, y + 32), (x + LW - 2, y + 32), (x + LW - 2, y + 68), (x + 360, y + 68)], fill=SAND)
d.rectangle([x + 300, y + 52, x + 352, y + 62], fill=(40, 40, 40))
d.text((x + 304, y + 53), "SPARTA II", font=FB(9), fill=WHITE)
d.ellipse([x + 390, y + 48, x + 402, y + 60], fill=NAVY)
d.line([(x + 396, y + 48), (x + 396, y + 40)], fill=NAVY, width=2)
d.line([(x + 386, y + 40), (x + 406, y + 40)], fill=NAVY, width=2)
badge(d, x + 8, y + 38, "SPARTA II HIT · CORVETTE CLAIMED SUNK", FB(11), NAVY2)
lead_text(x, y, "Drones strike Sparta II and a corvette",
          "Cargo ship hit in Gulf of Finland; 16 crew evacuated. Corvette hit off Libya.")

# L4 Cartagena storefront
x, y = MX + LW + 12, LY + LH + 10
lead_cell(x, y, 4, "CARTAGENA HOSTAGES  ·  17:35 UTC", "", "", NAVY2)
d.rectangle([x + 2, y + 32, x + LW - 2, y + 68], fill=(210, 225, 240))
d.rectangle([x + 120, y + 38, x + 360, y + 68], fill=(200, 60, 60))
for i in range(6):
    ax = x + 120 + i * 40
    d.polygon([(ax, y + 44), (ax + 20, y + 44), (ax + 20, y + 68), (ax, y + 68)],
              fill=WHITE if i % 2 == 0 else (200, 60, 60))
d.rectangle([x + 220, y + 56, x + 260, y + 68], fill=NAVY)
badge(d, x + 8, y + 38, "25 HELD · 5 FREED", FB(12), RED)
lead_text(x, y, "25 held hostage in Cartagena shop",
          "Armed men seized a supermarket; 5 older women freed. Airport landings paused.")

# ---- TIER-2 ----
TY = LY + 2 * LH + 10 + 12
d.text((MX, TY), "ALSO TODAY — TEN MORE, EACH CHECKED", font=FB(15), fill=NAVY)
tier = [
    ("PIF TOWER HIT, RIYADH", "Houthi drone: 11 wounded. 2nd hit in a week.", "CONFIRMED", "Saudi authorities"),
    ("HOUTHIS 60 KM FROM ADEN", "Fighters near the temporary capital; defence line built.", "OFFICIAL", "Yemen military"),
    ("SENEGAL AFCON CHAMPIONS", "Reinstated as 2025 winners after court appeal.", "CONFIRMED", "Court of Arbitration"),
    ("EL CHAPO ISIDRO CAPTURED", "US drone helped Sinaloa arrest; 20 killed in firefight.", "OFFICIAL", "Mexican AG"),
    ("TURKISH HELICOPTER CRASH", "AS-532 down after take-off; 5 crew killed.", "OFFICIAL", "Defence Ministry"),
    ("VILLAVICENCIO CAR BOMB", "Blast outside government offices; 23 injured.", "REPORTED", "Wire reports"),
    ("HAMAS SECURITY CHIEF KILLED", "Israeli strike kills Brig. Gen. Abu Nahel in Gaza.", "REPORTED", "Wire reports"),
    ("HANOI BLAST", "Hot-pot restaurant explosion; 6 killed, 10+ hurt.", "REPORTED", "Wire reports"),
    ("MEGASPEED BLACKLISTED", "US Entity List: 7 SE Asian firms; Nvidia GPUs curbed.", "OFFICIAL", "US BIS"),
    ("MALAYSIA RETURNS MIGRANTS", "6,803 to Myanmar: 1,500 by ship, 5,303 by air.", "OFFICIAL", "PM Anwar Ibrahim"),
]
# pictogram colours
pcol = [NAVY2, RED, GOLD, PURPLE, TEAL, ORANGE, NAVY, RED2, GREEN, SEA2]
TW2 = (CW - 12) // 2
for i, (title, det, tag, src) in enumerate(tier):
    col = i % 2
    row = i // 2
    x = MX + col * (TW2 + 12)
    y = TY + 22 + row * 30
    d.rounded_rectangle([x, y, x + TW2, y + 28], radius=5, fill=LIGHT)
    d.ellipse([x + 4, y + 2, x + 30, y + 28], fill=pcol[i])
    d.text((x + 12, y + 7), str(i + 1), font=FB(15), fill=WHITE)
    d.text((x + 36, y + 1), title, font=FB(13), fill=INK)
    d.text((x + 36, y + 15), det + "  ·  " + src, font=FR(11), fill=GREY)
    tag_badge(d, x + TW2 - 92, y + 3, tag)

# ---- NUMBERED-PIN WORLD MAP ----
MY = TY + 22 + 5 * 30 + 8
d.text((MX, MY), "WHERE IT HAPPENED — NUMBERED PINS MATCH THE LEADS", font=FB(14), fill=NAVY)
d.rounded_rectangle([MX, MY + 18, W - MX, MY + 74], radius=6, fill=(225, 238, 245))
# rough continents
d.polygon([(MX + 40, MY + 26), (MX + 190, MY + 24), (MX + 210, MY + 46), (MX + 120, MY + 58), (MX + 50, MY + 48)], fill=(170, 200, 150))  # N America
d.polygon([(MX + 200, MY + 52), (MX + 250, MY + 50), (MX + 245, MY + 68), (MX + 215, MY + 68)], fill=(170, 200, 150))  # S America
d.polygon([(MX + 430, MY + 26), (MX + 520, MY + 24), (MX + 540, MY + 46), (MX + 470, MY + 58), (MX + 440, MY + 44)], fill=(170, 200, 150))  # Europe/Africa
d.polygon([(MX + 560, MY + 24), (MX + 760, MY + 22), (MX + 800, MY + 42), (MX + 660, MY + 56), (MX + 570, MY + 46)], fill=(170, 200, 150))  # Asia
d.polygon([(MX + 820, MY + 50), (MX + 880, MY + 48), (MX + 885, MY + 62), (MX + 830, MY + 64)], fill=(170, 200, 150))  # Australia
pins = [(1, MX + 185, MY + 36, "BROOKLYN"), (2, MX + 585, MY + 42, "HORMUZ"),
        (3, MX + 480, MY + 32, "FINLAND / LIBYA"), (4, MX + 225, MY + 58, "CARTAGENA")]
for n, px, py, lab in pins:
    d.ellipse([px - 11, py - 11, px + 11, py + 11], fill=RED, outline=WHITE, width=2)
    d.text((px - 3, py - 8), str(n), font=FB(13), fill=WHITE)
    d.text((px + 14, py - 7), lab, font=FB(11), fill=NAVY)

# ---- BRIEFS ----
BY = MY + 82
d.text((MX, BY), "IN BRIEF — 20 MORE STORIES FROM THE SAME TUESDAY", font=FB(15), fill=NAVY)
briefs = [
    ("GAZA MENINGITIS:", "272 cases in Oct, 8x normal; 15 dead this year."),
    ("SAUDI STRIKES YEMEN:", "25 dead or missing in Lahj; 6 wounded."),
    ("IRAQ TAKES KURD OILFIELDS:", "Federal control ordered; Barzani objects."),
    ("DR CONGO PLANE MISSING:", "Cessna 208 lost; 4 aboard."),
    ("HAFTAR IN TURKEY:", "Libyan commander visits Ankara; meets Erdogan."),
    ("UK SANCTIONS HOUTHIS:", "Asset freezes + travel bans; 4 officials."),
    ("ULLEUNGDO SHELTER ORDER:", "Russian jets enter S. Korea ADIZ; fighters up."),
    ("INDONESIA VP RACE:", "Prabowo names 2 nominees; vote by 11 Dec."),
    ("HASINA TO RETURN:", "Ex-PM plans 16 Dec return from exile."),
    ("CHINA DEATH SENTENCE:", "Official Ma: spying, 35 secrets, ~$150,000."),
    ("NATO SPACE WARNING:", "Rutte vows defence; 'Sputnik-S' reports denied."),
    ("PENTAGON REBUKES CANADA:", "Only 41.9% of air fleet serviceable."),
    ("ZELENSKY URGES TALKS:", "Wants 4-party meeting ASAP; repeats NATO call."),
    ("HAITI:", "3 Salvadoran soldiers killed in accidental blast."),
    ("NEPAL QUAKE:", "Magnitude 5.6 near the China border."),
    ("N. KOREA:", "Demands Switzerland close Pyongyang office."),
    ("SOLOMON ISLANDS:", "Names Australia primary security partner."),
    ("US TARIFFS COMING:", "Tariffs eyed on China, EU over subsidies."),
    ("MARKETS:", "Nvidia -7%; Nikkei +3.9%; Brent $86.7 (-3%)."),
    ("QUASAR RECORD:", "Quasar found 630m years after the Big Bang."),
]
BW2 = (CW - 3 * 10) // 4
for i, (lead, rest) in enumerate(briefs):
    col, row = i % 4, i // 4
    x = MX + col * (BW2 + 10)
    y = BY + 20 + row * 26
    lines = wrap(d, lead + " " + rest, FB(12), BW2)
    # bold lead on line 1, rest regular: draw line1 bold+regular split approx
    d.text((x, y), lead, font=FB(12), fill=INK)
    lx = tw(d, lead, FB(12))
    rest1 = rest
    # if rest fits on line 1, put it there; else wrap rest onto line 2
    if tw(d, lead + " " + rest, FB(12)) <= BW2:
        d.text((x + lx + 3, y), rest, font=FR(12), fill=(50, 50, 50))
    else:
        # split rest into words fitting remainder + second line
        words = rest.split()
        l1, l2, cur = "", "", ""
        rem = BW2 - lx - 3
        for w_ in words:
            t = (cur + " " + w_).strip()
            if tw(d, t, FR(12)) <= rem and not l2:
                cur = t
            else:
                if l2 == "" and cur:
                    l1, cur = cur, w_
                    l2 = "x"
                else:
                    cur = (cur + " " + w_).strip() if cur else w_
        # simpler: re-wrap whole text to 2 lines with regular font measure
        all_lines = wrap(d, lead + " " + rest, FR(12), BW2)
        for j, ln in enumerate(all_lines[:2]):
            if j == 0:
                d.text((x, y), ln, font=FB(12), fill=INK)
            else:
                d.text((x, y + 12), ln, font=FR(12), fill=(50, 50, 50))

# ---- FOOTER: date check + how sure ----
FY = BY + 20 + 5 * 26 + 4
d.rectangle([MX, FY, W - MX, FY + 2], fill=GOLD)
d.text((MX, FY + 6), "DATE CHECK — NOT 24 NOV, SO NOT HERE:  ICJ Myanmar ruling was 19 Nov  ·  Shenzhou-24 flew 25 Nov  ·  Guterres AI call was 23 Nov  ·  FARC anniversary is 25 Nov",
       font=FB(12), fill=RED)
d.text((MX, FY + 22), "HOW SURE:  CONFIRMED = 2+ outlets or official record  ·  OFFICIAL = on the record  ·  REPORTED = one outlet  ·  CLAIM = one side's account",
       font=FR(12), fill=NAVY)

img.save(os.path.join(HERE, "entry.png"), optimize=True)
print("saved entry.png", img.size)
