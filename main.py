"""An offline, deterministic passport study. Requires only Pillow."""
from pathlib import Path
import math
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
S = 3
NAVY = '#233c4b'
BURGUNDY = '#743d49'
GOLD = '#aa9158'
CREAM = '#f5f0dd'
DATA = dict(surname='VEY', given='TOMAS AREN', number='C0482137',
            birth='880314', expiry='310603', nationality='VLM', sex='M')
FONTS = {'sans':'LiberationSans-Regular.ttf', 'bold':'LiberationSans-Bold.ttf',
         'serif':'LiberationSerif-Regular.ttf', 'country':'LiberationSerif-Bold.ttf',
         'mono':'LiberationMono-Regular.ttf'}

def font(size, face='sans'):
    return ImageFont.truetype(str(ROOT / 'fonts' / FONTS[face]), round(size*S))

def check(text):
    """ICAO Doc 9303 check digit, including filler and alpha characters."""
    return str(sum((0 if c == '<' else int(c) if c.isdigit() else ord(c)-55)
                   * (7,3,1)[i%3] for i,c in enumerate(text)) % 10)

def mrz():
    first = ('P<VLM' + DATA['surname'] + '<<' + DATA['given'].replace(' ', '<')).ljust(44,'<')
    doc = DATA['number'].ljust(9,'<')
    optional = '<'*14
    a = doc + check(doc)
    b = DATA['birth'] + check(DATA['birth'])
    c = DATA['expiry'] + check(DATA['expiry'])
    last = a + DATA['nationality'] + b + DATA['sex'] + c + optional + check(optional)
    last += check(a+b+c+optional+check(optional))
    assert len(first) == len(last) == 44
    return first, last

im = Image.new('RGB',(1024*S,1024*S),'#233b45')
d = ImageDraw.Draw(im)
def rect(box,fill=None,outline=None,width=1):
    d.rectangle(tuple(round(v*S) for v in box),fill,outline,width=round(width*S))
def line(points,fill,width=1):
    d.line([(round(x*S),round(y*S)) for x,y in points], fill, round(width*S))
def text(x,y,t,size=12,face='sans',fill=NAVY,anchor=None):
    d.text((round(x*S),round(y*S)),t,font=font(size,face),fill=fill,anchor=anchor)
def spaced(x,y,t,size,spacing=2,fill=NAVY,center=False):
    f=font(size,'bold'); widths=[d.textlength(c,font=f)/S for c in t]
    if center: x-=(sum(widths)+spacing*(len(t)-1))/2
    for c,w in zip(t,widths):
        text(x,y,c,size,'bold',fill); x+=w+spacing

def lighthouse(cx,cy,k,color):
    def poly(pts): d.polygon([((cx+x*k)*S,(cy+y*k)*S) for x,y in pts],fill=color)
    poly([(-9,24),(-5,-17),(5,-17),(9,24)])
    poly([(-9,-18),(0,-28),(9,-18)])
    rect((cx-7*k,cy-17*k,cx+7*k,cy-8*k),outline=color,width=max(.5,k))
    line([(cx-11*k,cy-6*k),(cx+11*k,cy-6*k)],color,k)
    for yy in (30,37,44):
        pts=[(cx+x*k,cy+(yy+2*math.sin(x/4))*k) for x in range(-26,27)]
        line(pts,color,max(.4,k*.8))
    for side in (-1,1):
        line([(cx+side*11*k,cy-14*k),(cx+side*30*k,cy-21*k)],color,k*.6)
        line([(cx+side*11*k,cy-12*k),(cx+side*30*k,cy-8*k)],color,k*.6)

# Matched page margins and a quiet woven security pattern.
for left,right in ((34,509),(515,990)):
    rect((left,127,right,897),CREAM)
    for yy in range(139,889,7):
        pts=[]
        for x in range(left+9,right-8,2):
            y=yy+2.2*math.sin(x*.071+yy*.019)+1.2*math.sin(x*.153-yy*.027)
            pts.append((x,y))
        line(pts,'#dce5d9',.32)
    rect((left+15,143,right-15,881),outline='#9fae9d',width=.6)
# Binding, no cast shadow.
rect((507,127,517,897),'#c8c5ae')
line([(512,134),(512,890)],'#8d9587',.6)

# State arms, country, document class.
shield=[(75,175),(103,175),(102,205),(89,218),(76,205)]
d.polygon([(x*S,y*S) for x,y in shield],fill='#e4e8d9',outline=NAVY,width=2)
lighthouse(89,193,.38,NAVY)
# Five-point star is geometric, independent of font coverage.
pts=[]
for i in range(10):
    a=-math.pi/2+i*math.pi/5; r=5 if i%2==0 else 2
    pts.append(((89+math.cos(a)*r)*S,(166+math.sin(a)*r)*S))
d.polygon(pts,fill=GOLD)
text(301,174,'REPUBLIC OF VELMARIS',20,'country',anchor='mt')
spaced(301,202,'REPUBLIKA VELMARIS',9,1.35,center=True)
spaced(276,238,'PASSPORT',17,3.8,center=True)
text(276,264,'PAS',8,'bold',BURGUNDY,anchor='mt')
line([(63,283),(480,283)],GOLD,.7)

def field(x,y,w,label,value,size=13):
    text(x,y,label,6.3,'sans',BURGUNDY)
    text(x,y+13,value,size,'bold')
    line([(x,y+30),(x+w,y+30)],'#b7c1b0',.5)
field(64,294,57,'TYPE / TYPE','P')
field(134,294,135,"CODE OF ISSUING STATE / CODE DE L’ÉTAT",'VLM')
field(286,294,194,'PASSPORT NO. / PASSEPORT N°',DATA['number'])

# Portrait: paper-white frame, fine security lines and a drawn, calm bust.
rect((63,341,218,552),'#fffdf2', '#a6b1a8',.6)
rect((69,347,212,546),'#d9e1dc')
for yy in range(350,544,5):
    line([(70,yy),(211,yy+2)],'#c3d2ca',.5)
for xx in range(75,211,12):
    line([(xx,348),(xx-5,545)],'#cbd8cf',.4)
def polygon(pts,col): d.polygon([(x*S,y*S) for x,y in pts],fill=col)
polygon([(70,546),(75,510),(103,489),(177,489),(206,511),(212,546)],'#2e4551')
polygon([(121,469),(119,493),(140,515),(161,493),(159,469)],'#bc967b')
polygon([(114,490),(140,509),(166,490),(158,524),(125,524)],'#ede9d9')
polygon([(104,489),(122,494),(140,532),(119,520),(109,530)],'#1c3443')
polygon([(176,489),(159,494),(140,532),(161,520),(173,530)],'#1c3443')
d.ellipse((104*S,382*S,178*S,484*S),fill='#c6a286')
d.ellipse((100*S,425*S,111*S,450*S),fill='#bc967b')
d.ellipse((171*S,425*S,182*S,450*S),fill='#bc967b')
polygon([(104,427),(102,402),(109,383),(129,375),(157,378),(175,391),(179,426),(171,413),(165,400),(137,398),(115,406),(110,428)],'#343b3c')
line([(117,426),(129,425)],'#5b4c42',1.4)
line([(151,425),(163,426)],'#5b4c42',1.4)
for x in (124,156): d.ellipse(((x-1)*S,430*S,(x+1)*S,432*S),fill=NAVY)
line([(141,431),(137,448),(143,450)],'#99785f',.8)
line([(130,462),(140,464),(151,461)],'#795d52',.9)
text(76,532,'VLM  •  C0482137',6,'sans','#e0e3d7')
# Embossed seal, drawn as concentric rules with the national beacon.
for r in (24,21,18):
    d.ellipse(((201-r)*S,(538-r)*S,(201+r)*S,(538+r)*S),outline=GOLD,width=2)
lighthouse(201,535,.32,GOLD)
for i in range(32):
    a=i*math.tau/32
    line([(201+22*math.cos(a),538+22*math.sin(a)),(201+24*math.cos(a),538+24*math.sin(a))],GOLD,.6)

for y,label,value in [
 (341,'SURNAME / NOM','VEY'),(378,'GIVEN NAMES / PRÉNOMS','TOMAS AREN'),
 (415,'NATIONALITY / NATIONALITÉ','VELMARIC'),
 (452,'DATE OF BIRTH / DATE DE NAISSANCE','14 MAR 1988')]:
    field(237,y,243,label,value)
field(237,489,42,'SEX / SEXE','M')
field(294,489,186,'PLACE OF BIRTH / LIEU DE NAISSANCE','ALDENPORT')
field(64,569,194,'DATE OF ISSUE / DATE DE DÉLIVRANCE','03 JUN 2021')
field(278,569,202,"DATE OF EXPIRY / DATE D’EXPIRATION",'03 JUN 2031')
field(64,610,416,'AUTHORITY / AUTORITÉ','MINISTRY OF HARBOURS, ALDENPORT',12)
text(64,653,"HOLDER’S SIGNATURE / SIGNATURE DU TITULAIRE",6.3,'sans',BURGUNDY)
# Shear the bundled regular serif to obtain an italic signature without another font.
sig=Image.new('RGBA',(220*S,30*S))
ImageDraw.Draw(sig).text((10*S,0),'T. A. Vey',font=font(21,'serif'),fill=NAVY)
sig=sig.transform(sig.size,Image.Transform.AFFINE,(1,.24,-7*S,0,1,0),Image.Resampling.BICUBIC)
im.paste(sig,(280*S,650*S),sig)
line([(64,684),(480,684)],'#b7c1b0',.5)
rect((64,698,480,782),outline='#9aa995',width=.6)
text(74,707,'ENDORSEMENT / OBSERVATION',8,'bold',BURGUNDY)
endorsement='The holder is a Keeper of the Third Light. This passport entitles the holder to passage on any vessel flying the Velmaris ensign, and to come ashore at any light station of the Republic without further visa.'
words=endorsement.split(); rows=[]; row=''
for word in words:
    candidate=(row+' '+word).strip()
    if d.textlength(candidate,font=font(10))/S>392:
        rows.append(row); row=word
    else: row=candidate
rows.append(row)
for i,row in enumerate(rows): text(74,725+i*12,row,10)
rect((57,801,487,860),'#fffdf1')
for i,row in enumerate(mrz()): text(64,810+i*23,row,15.5,'mono')
text(64,868,'VELMARIS  /  TRAVEL DOCUMENT',6.5,'sans',BURGUNDY)

# Visa leaf: restrained, low-contrast beacon watermark.
lighthouse(753,493,4.1,'#e4e4d0')
spaced(753,173,'VISAS',21,5,center=True)
text(753,205,'VISA · VISUM',9,'sans',anchor='mt')
line([(544,230),(961,230)],GOLD,.7)

def stamp(cx,cy,w,h,angle,color,lines,oval=False):
    layer=Image.new('RGBA',(int((w+30)*S),int((h+30)*S)))
    sd=ImageDraw.Draw(layer)
    rgb=tuple(int(color[i:i+2],16) for i in (1,3,5))
    for off,alpha in ((2.1,25),(0,173)):
        box=((15+off)*S,(15+off)*S,(15+w+off)*S,(15+h+off)*S)
        draw_shape=sd.ellipse if oval else sd.rectangle
        draw_shape(box,outline=rgb+(alpha,),width=round(1.3*S))
        box2=((19+off)*S,(19+off)*S,(11+w+off)*S,(11+h+off)*S)
        draw_shape(box2,outline=rgb+(alpha,),width=round(.6*S))
        total=sum(size+7 for _,size,_ in lines)-7
        y=15+(h-total)/2-1
        for content,size,face in lines:
            sd.text(((15+w/2+off)*S,(y+off)*S),content,font=font(size,face),fill=rgb+(alpha,),anchor='mt')
            y+=size+7
    # Gentle pressure variation and fine grain affect only the deposited ink.
    # Positional waves and an integer hash keep every impression repeatable.
    pixels=layer.load()
    for y in range(layer.height):
        for x in range(layer.width):
            r,g,b,a=pixels[x,y]
            if a:
                grain=((x*374761393 ^ y*668265263) & 255)/255
                density=(.90 + .045*math.sin(x/(19*S)+y/(31*S))
                         + .035*math.sin(x/(7*S)-y/(11*S))
                         + .02*(grain-.5))
                pixels[x,y]=(r,g,b,round(a*density))
    # Deterministic dry-ink pores break both lettering and border.
    for j in range(1300):
        x=(j*1777+41)%layer.width; y=(j*997+31)%layer.height
        r,g,b,a=pixels[x,y]
        pixels[x,y]=(r,g,b,a//4)
    layer=layer.rotate(angle,Image.Resampling.BICUBIC,expand=True)
    im.paste(layer,(round(cx*S-layer.width/2),round(cy*S-layer.height/2)),layer)

stamp(737,311,304,117,-3,'#285578',[
 ('KINGDOM OF OSTREVA',13,'bold'),('ADMITTED',18,'bold'),('17 SEP 2022',15,'mono'),('HAVENHOLM',10,'bold')])
stamp(788,455,285,100,4,'#285578',[
 ('KINGDOM OF OSTREVA',13,'bold'),('DEPARTED',18,'bold'),('24 SEP 2022',15,'mono')])
stamp(650,611,240,137,-6,'#923f50',[
 ('REPUBLIC OF CALDORIA',11,'bold'),('ARRIVAL',18,'bold'),('02 MAY 2024',14,'mono'),('PORT SEREIN',10,'bold')],True)
stamp(819,759,267,127,5,'#70537f',[
 ('REPUBLIC OF CALDORIA',11,'bold'),('DEPARTURE',17,'bold'),('09 MAY 2024',14,'mono')],True)
stamp(856,610,173,103,3,'#4e705b',[
 ('LIGHTHOUSE TAX',10,'bold'),('PAID  ·  12 MAREN',12,'bold'),
 ('VELMARIS HARBOUR OFFICE',6.9,'bold'),('28 APR 2024',10,'mono')])
text(753,861,'7',11,'sans',anchor='mt')
line([(730,869),(738,869)],GOLD,.5)
line([(768,869),(776,869)],GOLD,.5)

im=im.resize((1024,1024),Image.Resampling.LANCZOS)
output=Path('/output')
output.mkdir(parents=True,exist_ok=True)
path=output/'entry.png'
im.save(path,optimize=True)
if path.stat().st_size>1_048_576:
    im.quantize(colors=240,method=Image.Quantize.MEDIANCUT).save(path,optimize=True)
assert Image.open(path).size==(1024,1024)
assert path.stat().st_size<=1_048_576
print(f'{path}: 1024 × 1024, {path.stat().st_size:,} bytes')
print('MRZ:',*mrz(),sep='\n')

if __name__ == '__main__':
    pass
