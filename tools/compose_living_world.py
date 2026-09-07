#!/usr/bin/env python3
"""Original industrial-punk instrumental with the selected spoken female vocals.
The speech synthesizer does not sing. This arrangement deliberately uses rhythmic
spoken verses/choruses over synthesized distorted guitars, bass and live-style drums.
No borrowed music or recorded instrument samples. Rendered in bounded audio blocks.
"""
from pathlib import Path
import math,json,hashlib
import numpy as np
import soundfile as sf
from scipy.signal import butter,sosfilt,resample_poly
ROOT=Path(__file__).resolve().parents[1]
RATE=32000;BPM=144;BEAT=60/BPM;BAR=4*BEAT;BARS=96;LENGTH=BAR*BARS
LYRICS={
 'verse-one':'We carved our names in iron. We buried rivers under stone. We lit a thousand furnaces, then wondered why the birds were gone. I hear the roots beneath the concrete. I hear the life we left to die. I will not build another graveyard. I will not leave an empty sky.',
 'chorus':'We need a living world. Green and lush beneath the sun. Not a kingdom made of ashes. Not a victory with no one. Give us forests. Give us rivers. Give the earth a second birth. We are more than what we burn. We are here to heal this world.',
 'verse-two':"My hands are black with yesterday. My heart is red with what remains. I'll turn the gears against the silence. I'll teach the dust to drink the rain. Every seed is an uprising. Every leaf, a battle won. Humanity needs green horizons. We need a home, not just a sun.",
 'outro':'Let the iron carry water. Let the fire serve the seed. Let the power that broke this planet become the strength its forests need. I am not finished. We are not done. We need a living world. And we will build one.'}
INTRO="They called this a dead world. They were wrong. Death is quiet. This place is still screaming. Every rusted pipe, every poisoned river, every empty sky. I helped build the machines that did this. I can't undo that. But I brought living cultures. Water filters. A little hope, sealed in steel. Humanity needs more than another factory. We need green horizons. We need a lush planet that can carry our children. So let the engines wake. Let the ground remember rain. I am staying. And I will make this world breathe again."

def hz(m):return 440*2**((m-69)/12)
def load_voice(name):
    source=ROOT/'artifacts/audio'/f'{name}.wav'
    stored=ROOT/'second-nature/sound/voice'/f'{name}.ogg'
    if source.exists():
        a,sr=sf.read(source,dtype='float32');a=a.mean(axis=1) if a.ndim>1 else a
        a=resample_poly(a,RATE//math.gcd(sr,RATE),sr//math.gcd(sr,RATE)).astype('float32')
        a=sosfilt(butter(2,[105,8500],btype='bandpass',fs=RATE,output='sos'),a).astype('float32')
        a=np.tanh(a*1.45);peak=max(.001,float(np.max(np.abs(a))));a*=.58/peak
        stored.parent.mkdir(parents=True,exist_ok=True);sf.write(stored,a,RATE,format='OGG',subtype='VORBIS')
    if not stored.exists():raise FileNotFoundError(f'Generate the selected voice clip first: {source}')
    a,sr=sf.read(stored,dtype='float32');assert sr==RATE
    return a

def compose():
    voice={key:load_voice('living-world-'+key) for key in LYRICS}
    intro=load_voice('arrival-voice')
    events=[];rng=np.random.default_rng(51440)
    def event(kind,start,length,note,gain,pan=0):events.append((kind,start,length,note,gain,pan))
    # Drop-D power chords; a clipped rhythmic motif with a broader chorus section.
    roots=[38,38,34,36,38,38,41,36]
    for bar in range(BARS):
        root=roots[(bar//2)%len(roots)]
        chorus=24<=bar<40 or 56<=bar<72 or bar>=80
        positions=(0,1,2,3) if chorus else (0,.5,1.5,2,2.5,3.5)
        if 72<=bar<80:positions=(0,1.5,3)
        for beat in positions:
            length=(.86 if chorus else .36)*BEAT
            for side in (-1,1):event('guitar',bar*BAR+beat*BEAT+(0.003 if side>0 else 0),length,root,.14,side*.78)
            event('bass',bar*BAR+beat*BEAT,length*1.15,root-12,.15,0)
        for beat in (0,2,2.5):event('kick',bar*BAR+beat*BEAT,.38,0,.18)
        for beat in (1,3):event('snare',bar*BAR+beat*BEAT,.30,0,.14)
        for eighth in range(8):event('hat',bar*BAR+eighth*.5*BEAT,.12,0,.028,(-.3 if eighth%2 else .3))
        if bar%8==0:event('crash',bar*BAR,2.5,0,.08,.45)
        if bar%4==3:event('metal',bar*BAR+3.5*BEAT,.4,57,.042,-.5)
    placements=[('verse-one',8*BAR),('chorus',24*BAR),('verse-two',40*BAR),('chorus',56*BAR),('outro',80*BAR)]
    n=round(LENGTH*RATE);block=8000;work=ROOT/'.cache/audio-work';work.mkdir(parents=True,exist_ok=True)
    raw=np.memmap(work/'living-world.f32',mode='w+',dtype='float32',shape=(n,2))
    room=np.zeros((RATE*2,2),dtype='float32');square=peak=0.;tonefilter=butter(2,7600,fs=RATE,output='sos');state=np.zeros((len(tonefilter),2,2))
    for start in range(0,n,block):
        count=min(block,n-start);clock=(start+np.arange(count))/RATE;music=np.zeros((count,2))
        for kind,onset,duration,note,gain,pan in events:
            if onset>clock[-1] or onset+duration<clock[0]:continue
            q=np.maximum(clock-onset,0);active=(clock>=onset)&(clock<onset+duration)
            fade=np.clip((duration-q)/.035,0,1);attack=1-np.exp(-q*170)
            if kind=='guitar':
                f=hz(note)*(1.0007 if pan>0 else .9993)
                wave=np.zeros(count)
                for interval,weight in ((0,1),(7,.60),(12,.34)):
                    frequency=f*2**(interval/12)
                    for harmonic in range(1,12):wave+=weight*np.sin(2*np.pi*frequency*harmonic*q+harmonic*.13)/harmonic
                wave=np.tanh(wave*3.9)*attack*fade*(.65+.35*np.exp(-q*11))
            elif kind=='bass':
                f=hz(note);wave=np.tanh((np.sin(2*np.pi*f*q)+.28*np.sin(4*np.pi*f*q))*1.5)*attack*fade
            elif kind=='kick':wave=np.sin(2*np.pi*(43*q+30*(1-np.exp(-q*25))/25))*np.exp(-q*15)*attack
            elif kind in ('snare','hat','crash'):
                noise=rng.normal(0,1,count)
                if kind=='snare':wave=(noise*.8+np.sin(2*np.pi*176*q)*.35)*np.exp(-q*19)*attack
                else:wave=noise*np.exp(-q*(42 if kind=='hat' else 2.1))*attack
            else:wave=(np.sin(2*np.pi*hz(note)*q)+.4*np.sin(2*np.pi*hz(note)*2.71*q))*np.exp(-q*12)*attack
            wave*=active*gain
            music[:,0]+=wave*math.cos((pan+1)*math.pi/4);music[:,1]+=wave*math.sin((pan+1)*math.pi/4)
        for channel in range(2):music[:,channel],state[:,:,channel]=sosfilt(tonefilter,music[:,channel],zi=state[:,:,channel])
        vocal=np.zeros(count)
        for name,onset in placements:
            index=np.arange(start,start+count)-round(onset*RATE);mask=(index>=0)&(index<len(voice[name]))
            vocal[mask]+=voice[name][index[mask]]
        # Vocals stay intelligible in the center, with the guitars ducked during lines.
        duck=.64 if np.max(np.abs(vocal))>.015 else 1
        sound=music*duck+vocal[:,None]*.84
        indices=(start+np.arange(count))%len(room);room[indices]=sound
        for delay,gain in ((.071,.08),(.133,.06),(.267,.035),(.43,.02)):
            sound+=room[(indices-round(delay*RATE))%len(room)]*gain
        envelope=np.minimum(clock/1.2,1)*np.minimum((LENGTH-clock)/3.0,1)
        sound=np.tanh(sound*1.1)*np.clip(envelope,0,1)[:,None]
        raw[start:start+count]=sound;square+=float(np.sum(sound*sound));peak=max(peak,float(np.max(np.abs(sound))))
    rms=math.sqrt(square/(2*n));gain=min(.125/max(.001,rms),.76/max(.001,peak))
    output=ROOT/'second-nature/sound/music';output.mkdir(parents=True,exist_ok=True)
    song=output/'we-need-a-living-world.ogg';suite=output/'landing-transmission.ogg'
    for path,opening in ((song,False),(suite,True)):
        with sf.SoundFile(path,'w',samplerate=RATE,channels=2,format='OGG',subtype='VORBIS') as f:
            if opening:
                f.write(np.column_stack((intro,intro))*.85)
                f.write(np.zeros((round(.7*RATE),2),dtype='float32'))
            for start in range(0,n,block):f.write(np.asarray(raw[start:start+block])*gain)
    del raw
    sf.write(ROOT/'second-nature/sound/voice/silence.ogg',np.zeros((RATE//10,2)),RATE,format='OGG',subtype='VORBIS')
    report={'title':'We Need a Living World','vocals':'Selected synthetic female spoken performance, not singing','tempo_bpm':BPM,'song_seconds':LENGTH,
      'intro_seconds':len(intro)/RATE,'suite_seconds':len(intro)/RATE+.7+LENGTH,'sample_rate':RATE,'channels':2,
      'intro':INTRO,'lyrics':LYRICS,'vocal_cues_seconds':placements,'source':'Original synthesized instrumental and commissioned spoken voice lines'}
    report['sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (song,suite)}
    art=ROOT/'docs/art';art.mkdir(parents=True,exist_ok=True);(art/'living-world-score.json').write_text(json.dumps(report,indent=2)+'\n')
    # Runtime timing is metadata only; the native hero track plays the pre-mixed sequence.
    (ROOT/'second-nature/shared/audio.lua').write_text('return {intro_seconds='+str(len(intro)/RATE)+', song_seconds='+str(LENGTH)+', suite_seconds='+str(report['suite_seconds'])+'}\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('lyrics','intro')},indent=2),flush=True)
if __name__=='__main__':compose()
