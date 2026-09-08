#!/usr/bin/env python3
"""Compose After the Ash, an original instrumental score. No sampled recordings.
Streaming synthesis keeps the authoring memory budget independent of track length.
Optional dependencies: numpy, scipy, soundfile. The game loads only the Ogg file.
"""
from pathlib import Path
import hashlib,json,math
import numpy as np
from scipy.signal import butter,sosfilt
import soundfile as sf
ROOT=Path(__file__).resolve().parents[1]
RATE=32000;BPM=80;BEAT=60/BPM;LENGTH=96.0

def frequency(note):return 440*2**((note-69)/12)

def compose():
    rng=np.random.default_rng(7404);events=[]
    def event(note,start,duration,gain,pan,kind):events.append((note,start,duration,gain,pan,kind))
    chords=[(38,50,57,64),(34,50,53,57),(41,48,55,64),(36,50,55,62)]
    for part,chord in enumerate(chords):
        for j,note in enumerate(chord):event(note,part*24,28,.070 if j==0 else .053,(j-1.5)*.28,'pad')
    motifs=[[(0,62),(3,65),(7,69),(11,64),(16,62),(21,60),(26,57)],
            [(0,65),(4,69),(9,67),(15,64),(20,62),(26,69)],
            [(0,67),(5,72),(10,69),(16,67),(22,64),(27,62)]]
    for part,notes in enumerate(motifs):
        for i,(beat,note) in enumerate(notes):event(note,(32+part*32+beat)*BEAT,6,.072,math.sin(i*1.7)*.42,'glass')
    for beat in range(16,120):
        if beat%2==0:event(0,beat*BEAT,.55,.115,0,'pulse')
        if beat%8==3:event(45+(beat//8)%3,beat*BEAT,2.5,.025,(-1 if beat%16<8 else 1)*.5,'metal')
    n=round(LENGTH*RATE);block=16000;folder=ROOT/'.cache/audio-work';folder.mkdir(parents=True,exist_ok=True)
    raw=np.memmap(folder/'score.f32',dtype='float32',mode='w+',shape=(n,2))
    room=np.zeros((RATE*4,2),dtype='float32');taps=[(.14,.20),(.29,.15),(.43,.12),(.71,.10),(1.07,.08),(1.67,.055),(2.3,.035),(3.1,.025)]
    filt=butter(2,[90,920],fs=RATE,btype='bandpass',output='sos');state=np.zeros((len(filt),2))
    square=0.;peak=0.
    for start in range(0,n,block):
        count=min(block,n-start);clock=(start+np.arange(count))/RATE
        sound=np.zeros((count,2),dtype='float64')
        for note,onset,length,gain,pan,kind in events:
            if onset>clock[-1] or onset+length<clock[0]:continue
            t=clock-onset;active=(t>=0)&(t<length);q=np.maximum(t,0);f=frequency(note)
            if kind=='pad':
                env=np.clip(q/3,0,1)*np.clip((length-q)/3,0,1)
                wave=(np.sin(2*np.pi*f*q+.08*np.sin(q*.71))+.35*np.sin(2*np.pi*f*1.0022*q)+.15*np.sin(4*np.pi*f*q))*env*(.82+.18*np.sin(q*.13))
            elif kind=='glass':
                wave=(1-np.exp(-q*100))*np.exp(-q*.72)*(np.sin(2*np.pi*f*q)+.29*np.sin(2*np.pi*f*2.003*q)*np.exp(-q*.6)+.1*np.sin(2*np.pi*f*3.991*q)*np.exp(-q*2))
            elif kind=='pulse':
                wave=np.sin(2*np.pi*(45*q+20*(1-np.exp(-q*18))/18))*np.exp(-q*10)*(1-np.exp(-q*160))
            else:
                wave=(1-np.exp(-q*70))*np.exp(-q*2.6)*(np.sin(2*np.pi*f*q)+.24*np.sin(2*np.pi*f*2.71*q)+.13*np.sin(2*np.pi*f*4.13*q))
            wave*=active*gain
            sound[:,0]+=wave*math.cos((pan+1)*math.pi/4);sound[:,1]+=wave*math.sin((pan+1)*math.pi/4)
        wind,state=sosfilt(filt,rng.normal(0,1,count),zi=state)
        wind*=.009*(.6+.25*np.sin(clock*.16)+.15*np.sin(clock*.047))
        sound[:,0]+=wind;sound[:,1]+=wind*.87
        indices=(start+np.arange(count))%len(room);room[indices]=sound
        for delay,gain in taps:
            sound+=room[(indices-round(delay*RATE))%len(room)]*gain
        fade=np.clip(clock/3.5,0,1)*np.clip((LENGTH-clock)/5.5,0,1)
        sound*=fade[:,None];raw[start:start+count]=sound
        peak=max(peak,float(np.max(np.abs(sound))));square+=float(np.sum(sound*sound))
    rms=math.sqrt(square/(2*n));gain=min(.092/max(rms,1e-9),.72/max(peak,1e-9))
    destination=ROOT/'second-nature/sound/music';destination.mkdir(parents=True,exist_ok=True);path=destination/'after-the-ash.ogg'
    with sf.SoundFile(path,mode='w',samplerate=RATE,channels=2,format='OGG',subtype='VORBIS') as output:
        for start in range(0,n,block):output.write(np.asarray(raw[start:start+block])*gain)
    del raw
    peak=square=0.;samples=0
    for data in sf.blocks(path,blocksize=block,dtype='float32'):
        peak=max(peak,float(np.max(np.abs(data))));square+=float(np.sum(data*data));samples+=len(data)
    report={'title':'After the Ash','source':'Original procedural composition; no sampled recordings','tempo_bpm':BPM,
      'duration_seconds':samples/RATE,'sample_rate':RATE,'channels':2,'decoded_peak':peak,'decoded_rms':math.sqrt(square/(2*samples)),
      'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    out=ROOT/'docs/art';out.mkdir(parents=True,exist_ok=True);(out/'menu-score.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2),flush=True);return path
if __name__=='__main__':compose()
