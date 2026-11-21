# Builds the one-page press sheet PDF for /press/.
# usage: python3 make_presssheet.py  -> /home/claude/kdg_scripts/press/kyle-daniel-gordon-press-sheet.pdf
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader, simpleSplit

OUT = '/home/claude/kdg_scripts/press'
os.makedirs(OUT, exist_ok=True)
PDF = os.path.join(OUT, 'kyle-daniel-gordon-press-sheet.pdf')
PHOTO = '/home/claude/kdg_web/kyle-daniel-gordon-orchestrator-portrait.jpg'

INK, MUTE, TANG, RULE = HexColor('#1b1a17'), HexColor('#6b655a'), HexColor('#e2581a'), HexColor('#cfc8ba')
W, H = letter
M = 50

c = canvas.Canvas(PDF, pagesize=letter)
c.setTitle('Kyle Daniel Gordon, orchestrator: press sheet')
c.setAuthor('Press Office of Kyle Daniel Gordon')
c.setSubject('Biography, credits and credit wording for press')

# header
c.setFillColor(INK)
c.setFont('Helvetica', 9)
c.drawString(M, H - M, 'PRESS SHEET  ·  KYLEDANIELGORDON.COM/PRESS')
c.setFont('Helvetica-Bold', 30)
c.drawString(M, H - M - 38, 'Kyle Daniel Gordon')
c.setFont('Helvetica', 13)
c.setFillColor(MUTE)
c.drawString(M, H - M - 58, 'Orchestrator, arranger and conductor  ·  Los Angeles')

# photo
from PIL import Image
import io
_im = Image.open(PHOTO).convert('RGB'); _im.thumbnail((620, 900)); _b = io.BytesIO(); _im.save(_b, 'JPEG', quality=84); _b.seek(0)
img = ImageReader(_b)
iw, ih = img.getSize()
pw = 150
ph = pw * ih / iw
c.drawImage(img, W - M - pw, H - M - 14 - ph, pw, ph)
c.setFont('Helvetica', 7)
c.drawString(W - M - pw, H - M - 26 - ph, 'Portrait. Hi-res download at kyledanielgordon.com/press')

def para(text, x, y, width, size=10.5, lead=14.5, font='Helvetica', color=INK):
    c.setFont(font, size)
    c.setFillColor(color)
    for line in simpleSplit(text, font, size, width):
        c.drawString(x, y, line)
        y -= lead
    return y

def head(label, y, width):
    c.setStrokeColor(INK)
    c.setLineWidth(1.2)
    c.line(M, y + 12, M + width, y + 12)
    c.setFont('Helvetica-Bold', 9)
    c.setFillColor(INK)
    c.drawString(M, y, label.upper())
    return y - 16

colw = W - 2 * M - pw - 24
y = H - M - 96
y = head('In one line', y, colw)
y = para('Kyle Daniel Gordon was the orchestrator on all 19 tracks of Rosalía’s LUX, recorded with the London Symphony '
         'Orchestra, and orchestrated Ludwig Göransson’s score for Oppenheimer.', M, y, colw, size=12, lead=16) - 12

y = head('Biography', y, colw)
bio = ('Kyle Daniel Gordon is an orchestrator, arranger and conductor based in Los Angeles. He was lead orchestrator on '
       'Rosalía’s LUX (2025), recorded with the London Symphony Orchestra at AIR Studios, which won six Latin Grammys including '
       'Album of the Year and is nominated for Album of the Year at the 69th Grammy Awards. In film and television he orchestrated '
       'Ludwig Göransson’s score for Oppenheimer and has worked on Frozen II, Star Wars: The Last Jedi, Black Panther: Wakanda '
       'Forever, The Mandalorian and The Gilded Age. At the BBC Proms he was lead orchestrator on Soul Revolution (2025) and arranged '
       'for Bond and Beyond (2026). His piece The Little Bird was premiered by the San Francisco Symphony in 2026. He holds a '
       'master’s in music from the University of North Texas.')
y = para(bio, M, y, colw) - 12

full = W - 2 * M
y = min(y, H - M - 14 - ph - 50)
y = head('Selected work', y, full)
rows = [('Rosalía, LUX (2025)', 'Orchestrator on all 19 tracks · London Symphony Orchestra · AIR Studios'),
        ('Oppenheimer (2023)', 'Orchestrator · score by Ludwig Göransson'),
        ('BBC Proms', 'Soul Revolution (2025, lead orchestrator) · Bond and Beyond (2026)'),
        ('San Francisco Symphony', 'The Little Bird, world premiere (2026), composer'),
        ('Baby Shark × LSO', 'Arranger and conductor · recorded at LSO St Luke’s')]
for a, b in rows:
    c.setFont('Helvetica-Bold', 10)
    c.setFillColor(INK)
    c.drawString(M, y, a)
    para(b, M + 170, y, full - 170, size=10)
    y -= 17
y -= 10

y = head('How to credit', y, full)
notes = ['Name: Kyle Daniel Gordon (older credits read “Kyle Gordon”). He is not the comedian Kyle Gordon.',
         'LUX: “orchestrator on LUX” or “orchestrated all 19 tracks of LUX”. Daníel Bjarnason conducted the LSO sessions, and other '
         'arrangers are credited on some tracks, including Caroline Shaw and Angélica Negrón.',
         'Grammys: LUX is nominated for Album of the Year. Please don’t describe Kyle as a Grammy nominee.',
         'Film and TV other than Oppenheimer: “worked on”, as part of the orchestration team.']
for n in notes:
    c.setFillColor(TANG)
    c.circle(M + 3, y + 3.5, 2, stroke=0, fill=1)
    y = para(n, M + 14, y, full - 14, size=10, lead=13.5) - 4
y -= 8

y = head('Interviews', y, full)
y = para('Available for interviews in English, in person in Los Angeles, by phone or video, or by email. Topics: how a full '
         'orchestra was built into a pop album; what an orchestrator actually does; film scoring vs. records; the BBC Proms.',
         M, y, full, size=10, lead=13.5) - 6
c.setFont('Helvetica-Bold', 11)
c.setFillColor(INK)
c.drawString(M, y, 'Press office: kyledanielgordon.press@gmail.com')
c.setFont('Helvetica', 10)
c.setFillColor(MUTE)
c.drawString(M, y - 15, 'Photos, bios and coverage: kyledanielgordon.com/press')

c.setFont('Helvetica', 7.5)
c.drawString(M, 30, 'Photos are free to use for editorial coverage of Kyle Daniel Gordon. For photographer credits, ask the press office.')
c.showPage()
c.save()
print(PDF, os.path.getsize(PDF))
