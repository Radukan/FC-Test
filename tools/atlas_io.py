"""Read ordinary or striped native sprite atlases without assembling giant sheets."""
from PIL import Image
from catalog import MOD


def parts(spec):
    if 'stripes' in spec:
        return spec['stripes']
    return [{'filename':spec['filename'],'width_in_frames':spec.get('line_length',spec.get('frame_count',1)),
             'height_in_frames':None,'x':0,'y':0}]


def paths(spec):
    return [MOD/p['filename'].split('__second-nature__/')[1] for p in parts(spec)]


class Atlas:
    def __init__(self,spec):
        self.spec=spec;self.image=None;self.loaded=None
    def frame(self,direction=0,frame=0):
        s=self.spec;n=direction*s.get('frame_count',1)+frame
        for p in parts(s):
            columns=p['width_in_frames']
            count=columns*p['height_in_frames'] if p.get('height_in_frames') else 10**9
            if n>=count:n-=count;continue
            path=MOD/p['filename'].split('__second-nature__/')[1]
            if self.loaded!=path:
                self.close();self.image=Image.open(path);self.loaded=path
            x=p.get('x',0)+(n%columns)*s['width'];y=p.get('y',0)+(n//columns)*s['height']
            return self.image.crop((x,y,x+s['width'],y+s['height']))
        raise IndexError((direction,frame))
    def close(self):
        if self.image:self.image.close()
        self.image=None;self.loaded=None
