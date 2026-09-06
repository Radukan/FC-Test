#!/usr/bin/env python3
"""Generate original, deterministic RGBA mod art. No downloaded game assets are copied.
Pillow renders at 4x to keep 64px inventory icons crisp. Run only when editing art.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import math, random, hashlib
from catalog import MOD, ROOT, load_catalog, load_constants
S = 4
PAL = {
    "biodiversity": (154, 205, 102), "atmosphere": (116, 208, 202), "temperature": (239, 166, 87),
    "soil": (181, 143, 98), "water": (111, 169, 223), "toxicity": (210, 113, 140),
    "pressure": (227, 136, 85), "stability": (182, 219, 162), "stage": (233, 221, 172)
}
DARK = (31, 45, 43); EDGE = (56, 78, 69); GOLD = (205, 187, 139); LIGHT = (228, 232, 204)
def fade(c, f): return tuple(int(v*f) for v in c[:3])
def mix(c, d, a): return tuple(int(x*(1-a)+y*a) for x,y in zip(c[:3],d[:3]))
class Art:
    def __init__(self, size=(64,64), scale=S):
        self.s=scale; self.image=Image.new("RGBA",(size[0]*scale,size[1]*scale)); self.d=ImageDraw.Draw(self.image)
    def box(self,b): return tuple(round(x*self.s) for x in b)
    def ellipse(self,b,fill,outline=None,w=1): self.d.ellipse(self.box(b), fill, outline, max(1,round(w*self.s)))
    def rect(self,b,fill,outline=None,w=1,r=0):
        self.d.rounded_rectangle(self.box(b),radius=round(r*self.s),fill=fill,outline=outline,width=max(1,round(w*self.s)))
    def poly(self,p,fill,outline=None,w=1):
        p=[(round(x*self.s),round(y*self.s)) for x,y in p];self.d.polygon(p,fill)
        if outline:self.d.line(p+[p[0]],fill=outline,width=max(1,round(w*self.s)),joint="curve")
    def line(self,p,c,w=1):self.d.line([(round(x*self.s),round(y*self.s)) for x,y in p],fill=c,width=max(1,round(w*self.s)),joint="curve")
    def arc(self,b,start,end,c,w=1):self.d.arc(self.box(b),start,end,fill=c,width=max(1,round(w*self.s)))
    def leaf(self,x,y,scale=1,c=None):
        c=c or PAL['biodiversity']
        self.poly([(x-12*scale,y+3*scale),(x-8*scale,y-9*scale),(x+14*scale,y-14*scale),(x+10*scale,y+2*scale),(x,y+9*scale)],c,fade(c,.42),.8)
        self.line([(x-7*scale,y+5*scale),(x+9*scale,y-10*scale)],mix(c,LIGHT,.7),1)
    def shadow(self):
        shadow=Image.new('RGBA',self.image.size); d=ImageDraw.Draw(shadow)
        d.ellipse(self.box((10,45,59,61)),fill=(0,0,0,100)); self.image.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(2*self.s)))
    def vial(self,x,y,c,large=False):
        w,h=(18,36) if large else (13,27)
        self.rect((x,y+5,x+w,y+h), (81,113,111,240),DARK,1,r=3)
        self.rect((x+2,y+12,x+w-2,y+h-3),fade(c,.78),None,r=2)
        self.rect((x+3,y+13,x+w-3,y+h-8),c,None,r=2)
        self.rect((x-1,y,x+w+1,y+7),GOLD,DARK,1,r=1)
        self.line([(x+3,y+9),(x+3,y+h-5)],(209,238,220),1)
        self.ellipse((x+w-6,y+16,x+w-3,y+19),mix(c,LIGHT,.6))
    def cylinder(self,x,y,w,h,c):
        self.rect((x,y+3,x+w,y+h),fade(c,.62),DARK,1)
        self.rect((x+2,y+4,x+w*.47,y+h),c)
        self.ellipse((x,y+h-4,x+w,y+h+4),fade(c,.6),DARK,1)
        self.ellipse((x,y-3,x+w,y+5),mix(c,LIGHT,.15),DARK,1)
        self.ellipse((x+3,y-1,x+w-3,y+3),fade(c,.4))
    def save(self,path,size=None):
        path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
        size=size or (self.image.width//self.s,self.image.height//self.s)
        self.image.resize(size,Image.Resampling.LANCZOS).save(path,optimize=True)

def glyph(a,name,c,offset=0):
    if name in ('biodiversity','stability','second-nature','stage'):
        a.line([(30,50),(30,25),(36,19)],c,3);a.leaf(37,26,.75,c);a.leaf(23,38,.50,mix(c,LIGHT,.3))
    elif name=='atmosphere':
        for i in range(3):
            a.line([(15,22+i*10),(36+i*4,22+i*10)],c,2.5)
            a.arc((32+i*4,14+i*10,46+i*4,28+i*10),190,80,c,2.5)
    elif name=='water':
        a.poly([(32,12),(17,35),(17,44),(23,50),(39,50),(46,41),(44,33)],c,DARK,1)
        a.arc((21,31,41,47),20,160,LIGHT,2)
    elif name=='temperature':
        a.rect((27,13,35,42),GOLD,DARK,1,r=4);a.ellipse((22,37,40,55),c,DARK,1)
        a.line([(31,19),(31,43)],c,3)
        for i in range(3):a.line([(39,21+i*7),(45,21+i*7)],c,2)
    elif name=='soil':
        for y in (26,35,44):a.poly([(11,y),(30,y-8),(53,y),(34,y+8)],mix(c,LIGHT,(44-y)/60),DARK,1)
    elif name in ('toxicity','pressure'):
        a.poly([(32,12),(8,52),(56,52)],c,DARK,2)
        a.line([(32,26),(32,39)],DARK,4);a.ellipse((30,44,34,48),DARK)

def item_icon(name,family,color=None):
    a=Art();a.shadow();c=PAL.get(color or 'biodiversity')
    seed=int(hashlib.sha256(name.encode()).hexdigest()[:8],16);rng=random.Random(seed)
    if family=='science':
        a.poly([(24,7),(40,7),(40,12),(36,12),(36,26),(50,47),(48,56),(16,56),(14,47),(28,26),(28,12),(24,12)],(138,176,168,240),DARK,1.3)
        a.poly([(25,33),(39,33),(47,48),(45,52),(19,52),(17,48)],c,DARK,1)
        a.line([(25,29),(19,44),(19,48)],LIGHT,1.5);a.rect((24,6,40,11),GOLD,DARK,1,r=1)
        a.leaf(33,44,.35,LIGHT)
    elif name=='glass':
        a.vial(13,22,(111,188,189));a.vial(30,10,(172,215,217),True)
    elif family in ('filter',):
        a.rect((14,11,50,55),fade(c,.58),DARK,1.3,r=6)
        a.rect((19,13,45,54),(203,217,189),DARK,1,r=3)
        for x in range(22,45,5):a.line([(x,18),(x,49)],fade(c,.55),1.5)
        a.rect((11,12,53,19),GOLD,DARK,1,r=2);a.rect((11,47,53,54),GOLD,DARK,1,r=2)
        if name=='ceramic-membrane':
            a.rect((19,23,45,43),(154,195,200),DARK,1)
            for x in range(23,44,7):
                for y in range(27,43,7):a.ellipse((x-2,y-2,x+2,y+2),DARK)
    elif family=='waste':
        c=PAL['toxicity'];a.cylinder(15,16,34,36,(115,122,109))
        a.rect((12,19,51,24),GOLD,DARK,1,r=1);a.rect((12,44,51,49),GOLD,DARK,1,r=1)
        a.poly([(33,27),(23,43),(43,43)],c,DARK,1);a.line([(33,31),(33,37)],DARK,2);a.ellipse((32,39,34,41),DARK)
        if name=='heavy-metal-cake':
            a.poly([(10,48),(15,34),(32,30),(49,41),(45,53),(24,57)],(156,91,134),DARK,1)
            a.line([(15,34),(26,45),(49,41)],(218,151,175),1)
    elif family in ('culture','data'):
        if family=='data':
            c=PAL[{'ecological-data':'biodiversity','climate-data':'atmosphere','biosphere-data':'temperature'}[name]]
            a.rect((10,33,56,55),EDGE,DARK,1,r=3);a.vial(13,18,c);a.vial(33,12,c)
            a.rect((9,44,56,51),GOLD,DARK,1);a.line([(15,47),(32,47)],DARK,1)
        else:
            a.vial(21,10,c,True)
            a.leaf(42,42,.55,c)
            for i in range(5):
                x,y=rng.randint(26,34),rng.randint(28,42);a.ellipse((x,y,x+2,y+2),LIGHT)
    elif family=='leaf':
        for x,y,s in [(22,42,.8),(37,43,.9),(31,28,1)]:a.leaf(x,y,s,mix(c,EDGE,rng.random()*.3))
    elif family in ('soil','seed'):
        a.poly([(8,35),(31,22),(56,36),(55,51),(33,62),(9,50)],(116,92,68),DARK,1.2)
        a.poly([(8,35),(31,22),(56,36),(33,48)],(174,147,99),DARK,1)
        for i in range(12):
            x,y=rng.randint(16,47),rng.randint(34,45);a.ellipse((x,y,x+1.5,y+1.5),GOLD)
        a.line([(32,41),(32,23)],c,2);a.leaf(37,23,.6,c)
        if family=='seed':a.leaf(25,32,.45,LIGHT)
    elif family in ('mineral','carbon','crystal'):
        c= (66,80,77) if family=='carbon' else ((110,195,176) if family=='crystal' else (197,202,167))
        if name=='silica':c=(220,227,223)
        for i,(x,y,s) in enumerate([(20,43,1),(42,44,.85),(32,29,1.15)]):
            pts=[(x-12*s,y),(x-7*s,y-12*s),(x+5*s,y-15*s),(x+12*s,y-3*s),(x+7*s,y+9*s),(x-6*s,y+10*s)]
            a.poly(pts,c,DARK,1);a.poly([pts[1],pts[2],(x,y),pts[0]],mix(c,LIGHT,.27),DARK,.6)
            a.line([(x,y),pts[4]],fade(c,.63),1)
        if name in ('mineral-nutrients','neutralization-charge'):
            a.rect((16,46,48,56),GOLD,DARK,1,r=1);a.line([(23,51),(41,51)],EDGE,1.5)
        if family=='crystal':
            a.arc((10,9,57,52),-25,210,GOLD,2);a.leaf(34,32,.48,LIGHT)
    elif family=='thermal':
        a.cylinder(17,13,30,39,PAL['temperature']);a.rect((13,10,50,18),GOLD,DARK,1,r=2);a.rect((13,46,50,53),GOLD,DARK,1,r=2)
        a.rect((21,22,42,43),DARK,None,r=3)
        for i in range(3):a.line([(25,26+i*6),(39,26+i*6)],PAL['water'] if i>0 else PAL['temperature'],2)
    return a

def machine_icon(m):
    a=Art();a.shadow();c=PAL[m['color']];name=m['name']
    a.poly([(5,41),(31,26),(59,41),(33,58)],(77,94,82),DARK,1.2)
    a.poly([(5,41),(33,54),(59,41),(59,48),(33,62),(5,48)],(49,64,60),DARK,1)
    a.line([(7,44),(33,57),(56,44)],GOLD,1)
    if m['base'] in ('biochamber','cryogenic-plant') or name=='algae-vat':
        for x,y,w,h in [(12,30,17,16),(30,23,19,25)]:
            a.cylinder(x,y,w,h,(120,150,119))
            a.ellipse((x,y-11,x+w,y+7),fade(c,.55),DARK,1)
            a.ellipse((x+2,y-10,x+w-3,y+1),mix(c,LIGHT,.23),DARK,.5)
            a.arc((x+1,y-10,x+w-1,y+7),190,350,LIGHT,1)
            a.line([(x+w/2,y-10),(x+w/2,y+4)],GOLD,1)
            a.leaf(x+w/2,y-1,.28,c)
        a.line([(18,49),(18,40),(44,36)],GOLD,3);a.ellipse((42,35,48,41),c,DARK,1)
        if name=='planetary-beacon':
            a.line([(33,30),(33,7)],GOLD,2);a.ellipse((23,6,43,12),c,DARK,1);a.line([(26,5),(33,10),(40,5)],LIGHT,1)
    elif name in ('composter','pyrolyzer','materials-kiln','ecology-monitor'):
        a.poly([(9,26),(32,14),(54,27),(54,44),(31,55),(9,44)],(101,122,106),DARK,1)
        a.poly([(9,26),(32,14),(54,27),(31,39)],mix(c,GOLD,.4),DARK,1)
        a.poly([(31,39),(54,27),(54,44),(31,55)],fade(c,.5),DARK,1)
        a.rect((14,33,27,42),DARK,GOLD,.8,r=2)
        for i in range(3):a.line([(34,43+i*3),(48,36+i*3)],GOLD,.8)
        if name=='ecology-monitor':
            a.rect((17,21,43,37),DARK,GOLD,1,r=2);a.line([(21,31),(27,26),(30,32),(35,24),(40,28)],c,1.5)
        elif name=='composter':a.leaf(33,23,.65,PAL['biodiversity'])
        else:a.cylinder(39,6,10,24,(111,123,113));a.ellipse((38,7,50,11),c,DARK,1)
    else:
        a.cylinder(12,27,21,22,(124,143,119));a.cylinder(36,18,14,25,mix(c,GOLD,.15))
        a.line([(9,40),(9,31),(22,27)],GOLD,3);a.line([(27,45),(43,45),(43,40)],GOLD,3)
        a.rect((16,26,29,43),fade(c,.5),DARK,1,r=2);a.line([(19,29),(19,38)],mix(c,LIGHT,.6),1.5)
        a.cylinder(14,15,16,12,c)
        a.ellipse((38,8,48,17),c,DARK,1);a.line([(43,12),(43,8)],LIGHT,1)
        if name in ('seed-disperser','pheromone-dampener'):
            a.line([(28,28),(28,9)],GOLD,2);a.poly([(8,13),(28,8),(46,14),(29,18)],c,DARK,1)
        if name in ('thermal-exchanger','basalt-conditioner'):
            for i in range(3):a.line([(13,35+i*4),(23,29+i*4),(30,34+i*4)],GOLD,1.3)
    return a

def generate():
    k=load_catalog();out=MOD/'graphics/icons';out.mkdir(parents=True,exist_ok=True)
    for x in k['items']:item_icon(x['name'],x['family'],x.get('color')).save(out/(x['name']+'.png'))
    for x in k['fluids']:
        a=Art();a.shadow();c=tuple(int(v*255) for v in x['color']);a.vial(20,9,c,True);a.ellipse((38,36,55,53),c,DARK,1)
        a.arc((40,38,52,50),185,290,LIGHT,1);a.save(out/(x['name']+'.png'))
    for m in k['machines']:machine_icon(m).save(out/(m['name']+'.png'))
    for name,c in PAL.items():
        a=Art();a.shadow();a.ellipse((5,5,59,59),DARK,GOLD,1);glyph(a,name,c);a.save(out/('signal-'+name+'.png'))
        b=Art();b.ellipse((20,20,44,44),(*c,45),c,1);b.leaf(32,32,.46,(*c,210));b.save(out/('badge-'+name+'.png'))
    logo=Art();logo.ellipse((4,4,60,60),DARK,GOLD,1.4);logo.arc((10,10,54,54),35,285,PAL['biodiversity'],2);glyph(logo,'second-nature',PAL['biodiversity'])
    logo.save(out/'second-nature.png');logo.save(MOD/'thumbnail.png',(144,144))
    for name in ('rootbreaker','canopy-breaker','blight-spitter'):
        a=Art();a.shadow();c=PAL['biodiversity'] if name!='blight-spitter' else PAL['toxicity']
        for side in (-1,1):
            for i in range(3):a.line([(32+side*8,22+i*9),(32+side*(21+i),23+i*10),(32+side*24,34+i*8)],GOLD,3)
        for b in [(21,28,43,56),(23,18,41,40),(22,10,42,29)]:a.ellipse(b,fade(c,.65),DARK,1)
        a.ellipse((26,17,30,21),(255,207,125));a.ellipse((35,17,39,21),(255,207,125));a.line([(25,12),(21,5)],GOLD,2);a.line([(39,12),(43,5)],GOLD,2)
        a.save(out/(name+'.png'))
    tec=MOD/'graphics/technology';tec.mkdir(parents=True,exist_ok=True)
    machine_by_tech={
        'biofoundations':'algae-vat','composting':'composter','environmental-monitoring':'soil-enricher',
        'atmospheric-engineering':'air-scrubber','water-cycle':'watershed','reforestation':'seed-disperser','dirty-shortcuts':'forcing-tower',
        'thermal-engineering':'thermal-exchanger','closed-loops':'reclamation-plant','clean-chemistry':'electrolyzer',
        'planetary-ecology':'ecology-monitor','vulcanus-restoration':'basalt-conditioner','fulgora-remediation':'fulgoran-reclaimer',
        'gleba-symbiosis':'spore-tower','habitat-engineering':'sanctuary','climate-science':'thermal-exchanger','aquilo-habitats':'cryogenic-garden',
        'planetary-coordination':'planetary-beacon','living-worlds':'planetary-beacon','ecological-research':'sanctuary'
    }
    bymachine={m['name']:m for m in k['machines']}
    for index,t in enumerate(k['technologies']):
        m=bymachine[machine_by_tech.get(t['name'],'ecology-monitor')];c=PAL[m['color']];a=Art();
        pts=[(32+28*math.cos(math.pi/3*i-math.pi/2),32+28*math.sin(math.pi/3*i-math.pi/2)) for i in range(6)]
        a.poly(pts,(*DARK,240),GOLD,.6);a.arc((7,7,57,57),45,310,c,.7)
        icon=machine_icon(m).image.resize((196,196),Image.Resampling.LANCZOS);a.image.alpha_composite(icon,(30,26))
        for i in range(3):a.ellipse((25+i*6,53,27+i*6,55),c)
        a.save(tec/(t['name']+'.png'),(256,256))
    garden=Art((256,192),2)
    garden.ellipse((25,141,236,184),(0,0,0,50))
    for i in range(3):
        x=30+i*65;y=85-i*7
        garden.poly([(x,y),(x+27,y-17),(x+55,y),(x+55,y+40),(x+28,y+55),(x,y+39)],(55,79,76),GOLD,1)
        garden.ellipse((x,y-43,x+55,y+15),(75,135,127,170),PAL['atmosphere'],1.5)
        for j in range(3):garden.leaf(x+12+j*14,y-1-j%2*10,.8,PAL['biodiversity'])
        garden.arc((x,y-43,x+55,y+15),180,360,LIGHT,1.5);garden.line([(x+28,y-43),(x+28,y+14)],GOLD,1.5)
    garden.save(MOD/'graphics/garden.png')
    # Cover: an original technical field-station plate, not an in-game screenshot.
    W,H=1440,560;im=Image.new('RGB',(W,H),(14,31,29));d=ImageDraw.Draw(im)
    for x in range(0,W,32):d.line((x,0,x,H),fill=(22,43,39))
    for y in range(0,H,32):d.line((0,y,W,y),fill=(22,43,39))
    rng=random.Random(47)
    for radius in range(155,365,17):
        points=[]
        for i in range(181):
            angle=i*math.pi/90;r=radius+9*math.sin(angle*7+radius)+5*math.sin(angle*13)
            points.append((1030+math.cos(angle)*r,290+math.sin(angle)*r*.79))
        d.line(points,fill=(41,73,58),width=1)
    fontpath='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';boldpath='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
    font=lambda s,b=False:ImageFont.truetype(boldpath if b else fontpath,s)
    d.text((80,69),'PLANETARY RESTORATION / 01',font=font(17),fill=(173,199,164))
    d.text((74,120),'SECOND',font=font(76,True),fill=(233,236,212));d.text((74,205),'NATURE',font=font(76,True),fill=(162,204,122))
    d.text((80,318),'Build a factory. Grow a world.',font=font(25),fill=(203,214,192))
    d.text((80,417),'FIVE WORLDS   /   ONE LIVING SYSTEM',font=font(15),fill=(179,170,128))
    d.text((80,449),'A Factorio: Space Age overhaul',font=font(18),fill=(146,170,151))
    d.ellipse((851,94,1229,472),fill=(25,55,45),outline=(154,192,124),width=2)
    for n,(x,y,s) in enumerate([(917,170,130),(1031,157,154),(966,308,138),(1113,295,92)]):
        m=k['machines'][[0,9,19,20][n]];icon=machine_icon(m).image.resize((s,s),Image.Resampling.LANCZOS);im.paste(icon,(x,y),icon)
    d.arc((826,69,1254,497),-80,105,fill=(171,168,116),width=2)
    for n,c in enumerate(list(PAL.values())[:5]):
        x=917+n*52;d.ellipse((x,489,x+9,498),fill=c)
    (ROOT/'docs/assets').mkdir(parents=True,exist_ok=True);im.save(ROOT/'docs/assets/cover.png',optimize=True)
    # Inspect all inventory art at once without running the graphical client.
    names=sorted(out.glob('*.png'));sheet=Image.new('RGB',(640,math.ceil(len(names)/10)*84),(30,39,36));sd=ImageDraw.Draw(sheet)
    for i,path in enumerate(names):
        x,y=(i%10)*64,(i//10)*84;ic=Image.open(path);sheet.paste(ic,(x,y),ic)
        sd.text((x+2,y+63),path.stem[:10],fill=(202,213,193),font=font(8))
    cache=ROOT/'.cache';cache.mkdir(exist_ok=True);sheet.save(cache/'icon-contact-sheet.png')
    print(f"Generated {len(names)} inventory/interface icons, {len(k['technologies'])} research illustrations, garden sprite and branding.")
if __name__=='__main__':generate()
