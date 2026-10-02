import os
import json
import hashlib
import shutil
import subprocess
import time
import urllib.request
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

VERSION = "1.2.2"
MODULE_ID = "ravnica-leylines-audio-director"
TITLE = "Ravnica Leylines Audio Director"
DIST = Path("dist")
BUILD = Path("build")
PKG = BUILD / ("Ravnica_Leylines_Audio_Director_v" + VERSION)
MOD = PKG / MODULE_ID
AUDIO_BG = MOD / "assets" / "audio" / "background"
AUDIO_FX = MOD / "assets" / "audio" / "fx"

BACKGROUND = [
    {"id":"arcane-clockworks","title":"Arcane Clockworks","file":"273_Arcane_Clockworks.mp3","url":"https://sounds.tabletopaudio.com/273_Arcane_Clockworks.mp3"},
    {"id":"skirmish","title":"Skirmish","file":"92_Skirmish.mp3","url":"https://sounds.tabletopaudio.com/92_Skirmish.mp3"},
    {"id":"city-under-siege","title":"City Under Siege","file":"97_City_Under_Siege.mp3","url":"https://sounds.tabletopaudio.com/97_City_Under_Siege.mp3"},
    {"id":"cutpurse-pursuit","title":"Cutpurse Pursuit","file":"294_Cutpurse_Pursuit.mp3","url":"https://sounds.tabletopaudio.com/294_Cutpurse_Pursuit.mp3"},
    {"id":"barren-wastes","title":"Barren Wastes","file":"176_Barren_Wastes.mp3","url":"https://sounds.tabletopaudio.com/176_Barren_Wastes.mp3"},
    {"id":"blighted-farm","title":"Blighted Farm","file":"279_Blighted_Farm.mp3","url":"https://sounds.tabletopaudio.com/279_Blighted_Farm.mp3"},
    {"id":"carnival","title":"Halfling Festival","file":"133_Halfling_Festival.mp3","url":"https://sounds.tabletopaudio.com/133_Halfling_Festival.mp3","replacementFor":"Carnival"},
    {"id":"lucha-libre","title":"Alien Night Club","file":"17_Alien_Night_Club.mp3","url":"https://sounds.tabletopaudio.com/17_Alien_Night_Club.mp3","replacementFor":"Lucha Libre! / Colosseum"},
    {"id":"city-above","title":"The City Above","file":"280_The_City_Above.mp3","url":"https://sounds.tabletopaudio.com/280_The_City_Above.mp3"},
    {"id":"ethereal-plane","title":"Ethereal Plane","file":"112_Ethereal_Plane.mp3","url":"https://sounds.tabletopaudio.com/112_Ethereal_Plane.mp3"},
    {"id":"protean-fields","title":"Protean Fields","file":"14_Protean_Fields.mp3","url":"https://sounds.tabletopaudio.com/14_Protean_Fields.mp3"},
    {"id":"testing-chamber","title":"Testing Chamber","file":"103_Testing_Chamber.mp3","url":"https://sounds.tabletopaudio.com/103_Testing_Chamber.mp3"},
    {"id":"ancient-artifact","title":"Ancient Artifact","file":"289_Ancient_Artifact.mp3","url":"https://sounds.tabletopaudio.com/289_Ancient_Artifact.mp3"},
    {"id":"dark-matter","title":"Dark Matter","file":"135_Dark_Matter.mp3","url":"https://sounds.tabletopaudio.com/135_Dark_Matter.mp3"},
    {"id":"endgame","title":"Endgame","file":"187_Endgame.mp3","url":"https://sounds.tabletopaudio.com/187_Endgame.mp3"},
    {"id":"dungeon-mechanical","title":"Robotics Lab","file":"173_Robotics_Lab.mp3","url":"https://sounds.tabletopaudio.com/173_Robotics_Lab.mp3","replacementFor":"Dungeon II: Mechanical"}
]

FX_SOURCES = [
    ("Portal-sound-effect.mp3","https://www.orangefreesounds.com/wp-content/uploads/2019/05/Portal-sound-effect.mp3",["portal-snap"]),
    ("Sci-fi-device-high-tone.mp3","https://www.orangefreesounds.com/wp-content/uploads/2020/03/Sci-fi-device-high-tone.mp3",["leyline-pulse"]),
    ("Sci-fi-dimensional-energy-whoosh.mp3","https://orangefreesounds.com/wp-content/uploads/2025/07/Sci-fi-dimensional-energy-whoosh.mp3",["spatial-tear"]),
    ("Teleportation-sound-effect.mp3","https://orangefreesounds.com/wp-content/uploads/2024/09/Teleportation-sound-effect.mp3",["teleport-arrival"]),
    ("Time-travel-sound-effect.mp3","https://orangefreesounds.com/wp-content/uploads/2022/09/Time-travel-sound-effect.mp3",["mana-surge"]),
    ("Electricity-sound-effect.mp3","https://www.orangefreesounds.com/wp-content/uploads/2014/07/Electricity-sound-effect.mp3",["arcane-hum"]),
    ("Energy-shield-breakings-sound-effect.mp3","https://orangefreesounds.com/wp-content/uploads/2025/02/Energy-shield-breakings-sound-effect.mp3",["magic-shield"]),
    ("Digital-glitch-error-sound-effect.mp3","https://orangefreesounds.com/wp-content/uploads/2026/03/Digital-glitch-error-sound-effect.mp3",["reality-crack"]),
    ("Electric-spark-noise.mp3","https://www.orangefreesounds.com/wp-content/uploads/2016/12/Electric-spark-noise.mp3",["machine-overload"]),
    ("Heavy-metal-crash-and-clatter-sound-effect-industrial-impact-sfx.mp3","https://orangefreesounds.com/wp-content/uploads/2026/01/Heavy-metal-crash-and-clatter-sound-effect-industrial-impact-sfx.mp3",["metal-collapse"]),
    ("Steam-iron-sound-effect.mp3","https://orangefreesounds.com/wp-content/uploads/2024/02/Steam-iron-sound-effect.mp3",["steam-vent"]),
    ("Industrial-rhythmic-machine-sound-effect.mp3","https://orangefreesounds.com/wp-content/uploads/2024/11/Industrial-rhythmic-machine-sound-effect.mp3",["gears-turning"]),
    ("Electricity-zap.mp3","https://www.orangefreesounds.com/wp-content/uploads/2019/06/Electricity-zap.mp3",["coil-discharge"]),
    ("Glass-breaking-sound.mp3","https://www.orangefreesounds.com/wp-content/uploads/2016/12/Glass-breaking-sound.mp3",["glass-break"]),
    ("Emergency-alarm-sound-effect.mp3","https://www.orangefreesounds.com/wp-content/uploads/2020/12/Emergency-alarm-sound-effect.mp3",["lab-alarm","boros-siren"]),
    ("Machine-sound-effect.mp3","https://www.orangefreesounds.com/wp-content/uploads/2016/03/Machine-sound-effect.mp3",["machine-hum"]),
    ("Tiger-roaring.mp3","https://www.orangefreesounds.com/wp-content/uploads/2016/01/Tiger-roaring.mp3",["tiger-roar","tiger-growl"]),
    ("Bear-sounds.mp3","https://www.orangefreesounds.com/wp-content/uploads/2014/11/Bear-sounds.mp3",["bear-roar","bear-growl"]),
    ("Horse-galloping-sound-effect.mp3","https://orangefreesounds.com/wp-content/uploads/2025/05/Horse-galloping-sound-effect.mp3",["beast-charge"]),
    ("Swoosh-up-sound-effect.mp3","https://orangefreesounds.com/wp-content/uploads/2024/08/Swoosh-up-sound-effect.mp3",["claw-swipe"]),
    ("Body-fall-sound-effect.mp3","https://www.orangefreesounds.com/wp-content/uploads/2020/12/Body-fall-sound-effect.mp3",["beast-impact"]),
    ("Angry-dog-growling.mp3","https://www.orangefreesounds.com/wp-content/uploads/2017/01/Angry-dog-growling.mp3",["animal-snarl"]),
    ("Large-crowd-cheering-sound-effect-stadium-audience-roar.mp3","https://orangefreesounds.com/wp-content/uploads/2026/04/Large-crowd-cheering-sound-effect-stadium-audience-roar.mp3",["crowd-cheer"]),
    ("Crowd-panic-sound-effect.mp3","https://orangefreesounds.com/wp-content/uploads/2025/06/Crowd-panic-sound-effect.mp3",["crowd-panic"]),
    ("Crowd-laughing-sound-effect.mp3","https://orangefreesounds.com/wp-content/uploads/2026/04/Crowd-laughing-sound-effect.mp3",["crowd-laughter"]),
    ("People-applauding.mp3","https://www.orangefreesounds.com/wp-content/uploads/2020/03/People-applauding.mp3",["applause"]),
    ("Chain-sound-effect.mp3","https://www.orangefreesounds.com/wp-content/uploads/2016/01/Chain-sound-effect.mp3",["chain-swing"]),
    ("Whip-crack-sound-effect.mp3","https://www.orangefreesounds.com/wp-content/uploads/2017/01/Whip-crack-sound-effect.mp3",["whip-crack"]),
    ("Whoosh-fire-sound-effect.mp3","https://orangefreesounds.com/wp-content/uploads/2023/03/Whoosh-fire-sound-effect.mp3",["fire-burst"]),
    ("Dramatic-drum-hit-sound-effect.mp3","https://orangefreesounds.com/wp-content/uploads/2023/10/Dramatic-drum-hit-sound-effect.mp3",["drum-hit"]),
    ("Rubber-soled-footsteps-on-hard-surface-sound-effect.mp3","https://orangefreesounds.com/wp-content/uploads/2025/07/Rubber-soled-footsteps-on-hard-surface-sound-effect.mp3",["marching-boots","stone-footsteps"]),
    ("Walking-footsteps-on-metal-surface.mp3","https://www.orangefreesounds.com/wp-content/uploads/2018/06/Walking-footsteps-on-metal-surface.mp3",["armor-movement"]),
    ("Whistle-sound-effect.mp3","https://www.orangefreesounds.com/wp-content/uploads/2015/03/Whistle-sound-effect.mp3",["signal-whistle"]),
    ("Sword-fight-sound-effect.mp3","https://www.orangefreesounds.com/wp-content/uploads/2015/06/Sword-fight-sound-effect.mp3",["weapon-clash"]),
    ("Cyberpunk-digital-blade-whoosh-sound-effect.mp3","https://orangefreesounds.com/wp-content/uploads/2026/04/Cyberpunk-digital-blade-whoosh-sound-effect.mp3",["sword-swing"]),
    ("Metal-sound-effect.mp3","https://orangefreesounds.com/wp-content/uploads/2024/05/Metal-sound-effect.mp3",["shield-impact"]),
    ("Loud-thud-impact-sound-effect.mp3","https://orangefreesounds.com/wp-content/uploads/2026/05/Loud-thud-impact-sound-effect.mp3",["impact-heavy"]),
    ("Explosion-sound-effect.mp3","https://www.orangefreesounds.com/wp-content/uploads/2014/09/Explosion-sound-effect.mp3",["explosion"]),
    ("Ground-smash-sound-effect.mp3","https://orangefreesounds.com/wp-content/uploads/2025/06/Ground-smash-sound-effect.mp3",["debris-fall"]),
    ("Cinematic-shock-sound-effect.mp3","https://orangefreesounds.com/wp-content/uploads/2026/05/Cinematic-shock-sound-effect.mp3",["spell-blast"]),
    ("Arrow-sound-effect.mp3","https://orangefreesounds.com/wp-content/uploads/2025/02/Arrow-sound-effect.mp3",["arrow-shot"]),
    ("City-ambience-sound-effect.mp3","https://www.orangefreesounds.com/wp-content/uploads/2019/12/City-ambience-sound-effect.mp3",["city-crowd"]),
    ("Door-slam-sound-effect.mp3","https://www.orangefreesounds.com/wp-content/uploads/2017/09/Door-slam-sound-effect.mp3",["door-slam"]),
    ("Horse-and-carriage-sound-effect.mp3","https://orangefreesounds.com/wp-content/uploads/2023/07/Horse-and-carriage-sound-effect.mp3",["cart-rattle"])
]

FX_META = {
"portal-snap":["Portal Snap","Planar / Leyline"],"leyline-pulse":["Leyline Pulse","Planar / Leyline"],"spatial-tear":["Spatial Tear","Planar / Leyline"],"teleport-arrival":["Teleport Arrival","Planar / Leyline"],"mana-surge":["Mana Surge","Planar / Leyline"],"arcane-hum":["Arcane Hum","Planar / Leyline"],"magic-shield":["Magic Shield","Planar / Leyline"],"reality-crack":["Reality Crack","Planar / Leyline"],
"machine-overload":["Machine Overload","Izzet / Machinery"],"metal-collapse":["Metal Collapse","Izzet / Machinery"],"steam-vent":["Steam Vent","Izzet / Machinery"],"gears-turning":["Gears Turning","Izzet / Machinery"],"coil-discharge":["Coil Discharge","Izzet / Machinery"],"glass-break":["Glass Break","Izzet / Machinery"],"lab-alarm":["Lab Alarm","Izzet / Machinery"],"machine-hum":["Machine Hum","Izzet / Machinery"],
"tiger-roar":["Tiger Roar","Creatures"],"tiger-growl":["Tiger Growl","Creatures"],"bear-roar":["Bear Roar","Creatures"],"bear-growl":["Bear Growl","Creatures"],"beast-charge":["Beast Charge","Creatures"],"claw-swipe":["Claw Swipe","Creatures"],"beast-impact":["Beast Impact","Creatures"],"animal-snarl":["Animal Snarl","Creatures"],
"crowd-cheer":["Crowd Cheer","Rakdos / Crowd"],"crowd-panic":["Crowd Panic","Rakdos / Crowd"],"crowd-laughter":["Crowd Laughter","Rakdos / Crowd"],"applause":["Applause","Rakdos / Crowd"],"chain-swing":["Chain Swing / Snap","Rakdos / Crowd"],"whip-crack":["Whip Crack","Rakdos / Crowd"],"fire-burst":["Fire Burst","Rakdos / Crowd"],"drum-hit":["Performance Drum Hit","Rakdos / Crowd"],
"boros-siren":["Boros Alarm / Siren","Boros"],"marching-boots":["Marching Boots","Boros"],"armor-movement":["Armor Movement","Boros"],"signal-whistle":["Signal Whistle","Boros"],
"weapon-clash":["Weapon Clash","Combat"],"sword-swing":["Sword Swing","Combat"],"shield-impact":["Shield Impact","Combat"],"impact-heavy":["Heavy Impact","Combat"],"explosion":["Explosion","Combat"],"debris-fall":["Falling Debris","Combat"],"spell-blast":["Spell Blast","Combat"],"arrow-shot":["Projectile / Arrow Shot","Combat"],
"city-crowd":["City Crowd","City / Environment"],"stone-footsteps":["Stone Footsteps","City / Environment"],"door-slam":["Door Slam","City / Environment"],"cart-rattle":["Cart / Wagon Rattle","City / Environment"]
}

SCENES = [
{"title":"01 — Broken Arrival Workshop","tracks":["arcane-clockworks","skirmish","city-under-siege"],"note":"Izzet workshop failure, Gruul pressure, planar arrival."},
{"title":"02 — No Safe Road","tracks":["cutpurse-pursuit","city-under-siege"],"note":"Elevated chase and Boros intervention."},
{"title":"03 — The Bear Site","tracks":["barren-wastes","blighted-farm"],"note":"Rubblebelt receiver site and displaced bear."},
{"title":"04 — The Red Stage","tracks":["lucha-libre","carnival"],"note":"Rakdos moving performance; Alien Night Club is the primary bed."},
{"title":"05 — The White Bridge","tracks":["city-above","ethereal-plane","protean-fields"],"note":"Split elevation bands and spatial failure."},
{"title":"06 — Orientation Vault","tracks":["testing-chamber","dungeon-mechanical","ancient-artifact","dark-matter","endgame"],"note":"Izzet lab, planar machinery, and finale."}
]
SITUATIONS = [
{"title":"Fast Chase","tracks":["cutpurse-pursuit","skirmish"]},{"title":"City Crisis","tracks":["city-under-siege","skirmish"]},{"title":"Rubblebelt Unease","tracks":["barren-wastes","blighted-farm"]},{"title":"Rakdos Spectacle","tracks":["lucha-libre","carnival"]},{"title":"Planar Instability","tracks":["ethereal-plane","protean-fields","dark-matter"]},{"title":"Izzet Lab","tracks":["arcane-clockworks","testing-chamber","dungeon-mechanical"]},{"title":"Artifact Reveal","tracks":["ancient-artifact","dark-matter"]},{"title":"Finale","tracks":["endgame","dark-matter","skirmish"]}
]

def write_text(path,text):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True); path.write_text(text,encoding="utf-8")

def download(url,dest):
    dest=Path(dest); dest.parent.mkdir(parents=True,exist_ok=True)
    last=None
    for attempt in range(5):
        try:
            referer="https://tabletopaudio.com/" if "tabletopaudio" in url else "https://www.orangefreesounds.com/"
            req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 Chrome/154 Safari/537.36","Accept":"audio/mpeg,audio/*;q=0.9,*/*;q=0.8","Referer":referer})
            with urllib.request.urlopen(req,timeout=60) as r,open(dest,"wb") as f: shutil.copyfileobj(r,f)
            if dest.stat().st_size<3000: raise RuntimeError("download too small")
            return
        except Exception as e:
            last=e
            if dest.exists(): dest.unlink()
            time.sleep(2+attempt*2)
    raise RuntimeError("FAILED download %s: %s"%(url,last))

def ffprobe(path):
    p=subprocess.run(["ffprobe","-v","error","-show_entries","format=format_name,duration,bit_rate","-of","json",str(path)],capture_output=True,text=True)
    if p.returncode: raise RuntimeError("ffprobe failed %s: %s"%(path,p.stderr))
    d=json.loads(p.stdout); name=str(d.get("format",{}).get("format_name",""))
    if "mp3" not in name: raise RuntimeError("not MP3: "+str(path))

def sha256(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()

def make_data():
    backgrounds=[]
    for b in BACKGROUND:
        row=dict(b); row["path"]="modules/%s/assets/audio/background/%s"%(MODULE_ID,b["file"]); backgrounds.append(row)
    fx=[]
    for file,url,ids in FX_SOURCES:
        for fid in ids:
            title,cat=FX_META[fid]
            fx.append({"id":fid,"title":title,"category":cat,"file":file,"path":"modules/%s/assets/audio/fx/%s"%(MODULE_ID,file),"source_url":url})
    data={"version":VERSION,"moduleId":MODULE_ID,"crossfadeMs":2500,"backgrounds":backgrounds,"fx":fx,"cards":{"scenes":SCENES,"situations":SITUATIONS},"downloadDelta":[]}
    write_text(MOD/"data"/"audio-cues.json",json.dumps(data,indent=2,ensure_ascii=False))
    return data

MAIN_JS = r'''const MODULE_ID="ravnica-leylines-audio-director";
const VERSION="1.2.2";
const CROSSFADE=2500;
const LS_PREFIX=MODULE_ID+":ui:";
let DATA=null,PLAYLIST=null;
const runtimeErrors=[];
function logError(where,err){const row={at:new Date().toISOString(),where,message:String(err?.message??err),stack:String(err?.stack??"")};runtimeErrors.push(row);console.error("Leylines Audio Director",where,err);}
window.addEventListener("error",ev=>logError("window.error",ev.error??ev.message));
window.addEventListener("unhandledrejection",ev=>logError("unhandledrejection",ev.reason));
async function loadData(){if(DATA)return DATA;const r=await fetch("modules/"+MODULE_ID+"/data/audio-cues.json",{cache:"no-store"});if(!r.ok)throw new Error("audio-cues.json HTTP "+r.status);DATA=await r.json();return DATA;}
function key(k){return LS_PREFIX+k}function defaults(k){return k==="director"?{left:250,top:90,width:560,height:620,collapsed:false}:{left:835,top:90,width:480,height:620,collapsed:true}}
function readState(k){try{return Object.assign({},defaults(k),JSON.parse(localStorage.getItem(key(k))||"{}"))}catch(_){return defaults(k)}}function saveState(k,s){try{localStorage.setItem(key(k),JSON.stringify(s))}catch(_){}}
function el(t,c,x){const n=document.createElement(t);if(c)n.className=c;if(x!=null)n.textContent=x;return n}
function btn(x,c,fn,title){const b=el("button",c||"lad-btn",x);b.type="button";if(title)b.title=title;b.addEventListener("click",e=>{e.stopPropagation();fn(e)});return b}
function downloadJson(name,obj){const blob=new Blob([JSON.stringify(obj,null,2)],{type:"application/json"}),a=document.createElement("a");a.href=URL.createObjectURL(blob);a.download=name;document.body.appendChild(a);a.click();setTimeout(()=>{URL.revokeObjectURL(a.href);a.remove()},500)}
async function ensurePlaylist(){await loadData();if(!game.user.isGM)return null;let pl=game.playlists.find(p=>p.getFlag(MODULE_ID,"managed"));if(!pl)pl=await Playlist.create({name:"Leylines Audio Director",mode:2,channel:"music",fade:CROSSFADE,flags:{[MODULE_ID]:{managed:true,version:VERSION}}});const existing=new Map(pl.sounds.map(s=>[s.getFlag(MODULE_ID,"cueId"),s]));const create=[];for(const bg of DATA.backgrounds){const s=existing.get(bg.id),d={name:bg.title,path:bg.path,repeat:true,volume:.55,fade:CROSSFADE,channel:"music",flags:{[MODULE_ID]:{cueId:bg.id,version:VERSION}}};if(!s)create.push(d);else if(s.path!==d.path||s.name!==d.name||s.fade!==CROSSFADE)await s.update({name:d.name,path:d.path,fade:CROSSFADE,repeat:true,channel:"music",["flags."+MODULE_ID+".cueId"]:bg.id,["flags."+MODULE_ID+".version"]:VERSION})}if(create.length)await pl.createEmbeddedDocuments("PlaylistSound",create);PLAYLIST=pl;return pl}
function getSound(id){return PLAYLIST?.sounds.find(s=>s.getFlag(MODULE_ID,"cueId")===id)}
async function playBackground(id,mode){try{await ensurePlaylist();const bg=DATA.backgrounds.find(x=>x.id===id),s=getSound(id);if(!bg||!s)throw new Error("Background not found: "+id);const how=mode||document.querySelector("#lad-mode")?.value||"replace";if(how==="replace")await PLAYLIST.stopAll();await s.update({volume:how==="mix"?.38:.55});await PLAYLIST.playSound(s);ui.notifications?.info("Leylines Audio: "+bg.title+" ("+how+")");refreshMixer()}catch(e){logError("playBackground",e);ui.notifications?.error("Leylines Audio failed: "+e.message)}}
function playAlternative(ids){if(!ids?.length)return;return playBackground(ids[Math.floor(Math.random()*ids.length)],"replace")}
function playFx(id){try{const fx=DATA.fx.find(x=>x.id===id);if(!fx)throw new Error("FX not found: "+id);const vol=Number(document.querySelector("#lad-fx-volume")?.value||.85),A=globalThis.AudioHelper??foundry?.audio?.AudioHelper;if(!A?.play)throw new Error("AudioHelper unavailable");A.play({src:fx.path,volume:vol,loop:false,autoplay:true,channel:"environment"},true)}catch(e){logError("playFx",e);ui.notifications?.error("Leylines FX failed: "+e.message)}}
async function stopBackgrounds(){try{await ensurePlaylist();await PLAYLIST.stopAll();refreshMixer()}catch(e){logError("stopBackgrounds",e)}}
function applyState(p,k,s){p.style.left=Math.max(0,s.left)+"px";p.style.top=Math.max(0,s.top)+"px";if(s.collapsed){p.classList.add("lad-collapsed");p.style.width="290px";p.style.height="42px"}else{p.classList.remove("lad-collapsed");p.style.width=Math.max(320,s.width)+"px";p.style.height=Math.max(260,s.height)+"px"}}
function drag(p,h,k,s){let d=null;h.addEventListener("pointerdown",e=>{if(e.target.closest("button,input,select"))return;const r=p.getBoundingClientRect();d={dx:e.clientX-r.left,dy:e.clientY-r.top};h.setPointerCapture?.(e.pointerId)});h.addEventListener("pointermove",e=>{if(!d)return;s.left=Math.max(0,e.clientX-d.dx);s.top=Math.max(0,e.clientY-d.dy);p.style.left=s.left+"px";p.style.top=s.top+"px"});h.addEventListener("pointerup",e=>{if(!d)return;d=null;saveState(k,s);h.releasePointerCapture?.(e.pointerId)});p.addEventListener("pointerup",()=>{if(p.classList.contains("lad-collapsed"))return;const r=p.getBoundingClientRect();s.left=r.left;s.top=r.top;s.width=r.width;s.height=r.height;saveState(k,s)})}
function setCollapsed(k,v){const p=document.getElementById("lad-"+k);if(!p)return;const s=readState(k);if(!p.classList.contains("lad-collapsed")){const r=p.getBoundingClientRect();s.left=r.left;s.top=r.top;s.width=r.width;s.height=r.height}s.collapsed=v==null?!s.collapsed:!!v;saveState(k,s);applyState(p,k,s)}
function toggle(k){const p=document.getElementById("lad-"+k);if(!p)return;p.style.display="";if(p.classList.contains("lad-collapsed"))setCollapsed(k,false);p.style.zIndex=String(10000+Date.now()%5000)}
function trackRow(ids){const r=el("div","lad-track-row");for(const id of ids){const bg=DATA.backgrounds.find(x=>x.id===id);if(bg)r.appendChild(btn(bg.title,"lad-track",()=>playBackground(id),bg.replacementFor?("Replaces "+bg.replacementFor):bg.title))}r.appendChild(btn("Alternative","lad-track alt",()=>playAlternative(ids)));return r}
function card(x){const c=el("section","lad-card");c.append(el("h3","",x.title));if(x.note)c.append(el("p","lad-note",x.note));c.append(trackRow(x.tracks));return c}
function tab(name,target,body){const b=btn(name,"lad-tab",()=>{body.querySelectorAll(".lad-view").forEach(v=>v.hidden=true);body.parentElement.querySelectorAll(".lad-tab").forEach(v=>v.classList.remove("active"));body.querySelector('[data-view="'+target+'"]').hidden=false;b.classList.add("active");if(target==="mixer")refreshMixer();if(target==="sources")refreshSources()});return b}
function directorContent(){const root=el("div"),ctl=el("div","lad-controls"),sel=document.createElement("select");sel.id="lad-mode";[["replace","Replace"],["mix","Mix In"],["add","Add"],["alternative","Alternative"]].forEach(([v,t])=>{const o=document.createElement("option");o.value=v;o.textContent=t;sel.appendChild(o)});ctl.append(el("label","","Mode "),sel,btn("Stop Backgrounds","lad-btn danger",stopBackgrounds),btn("FX Board","lad-btn",()=>toggle("fx")));root.append(ctl);const tabs=el("div","lad-tabs"),body=el("div","lad-tabbody"),views={scenes:el("div","lad-view"),situations:el("div","lad-view"),mixer:el("div","lad-view"),sources:el("div","lad-view")};for(const[k,v]of Object.entries(views)){v.dataset.view=k;if(k!=="scenes")v.hidden=true;body.append(v)}views.mixer.id="lad-mixer-view";views.sources.id="lad-sources-view";DATA.cards.scenes.forEach(x=>views.scenes.append(card(x)));DATA.cards.situations.forEach(x=>views.situations.append(card(x)));const first=tab("Scenes","scenes",body);first.classList.add("active");tabs.append(first,tab("Situations","situations",body),tab("Live Mixer","mixer",body),tab("Sources","sources",body));root.append(tabs,body);return root}
function fxContent(){const root=el("div"),ctl=el("div","lad-controls"),search=document.createElement("input"),vol=document.createElement("input");search.type="search";search.placeholder="Search sounds…";vol.type="range";vol.min=0;vol.max=1;vol.step=.05;vol.value=.85;vol.id="lad-fx-volume";ctl.append(search,el("label","","FX volume "),vol,btn("Director","lad-btn",()=>toggle("director")));root.append(ctl);const cats=[...new Set(DATA.fx.map(x=>x.category))],tabs=el("div","lad-tabs"),grid=el("div","lad-fx-grid");let active=cats[0];const render=()=>{const q=search.value.trim().toLowerCase();grid.innerHTML="";DATA.fx.filter(x=>x.category===active&&(!q||x.title.toLowerCase().includes(q)||x.id.includes(q))).forEach(x=>grid.append(btn(x.title,"lad-fx",()=>playFx(x.id),x.category)))};cats.forEach((cat,i)=>{const b=btn(cat,"lad-tab",()=>{active=cat;tabs.querySelectorAll(".lad-tab").forEach(x=>x.classList.remove("active"));b.classList.add("active");render()});if(i===0)b.classList.add("active");tabs.append(b)});search.addEventListener("input",render);root.append(tabs,grid);render();return root}
function createPanel(k,title,builder){document.getElementById("lad-"+k)?.remove();const s=readState(k),p=el("aside","lad-panel"),h=el("header","lad-header"),actions=el("div","lad-head-actions");p.id="lad-"+k;h.append(el("span","lad-title",title));actions.append(btn(k==="director"?"FX":"Director","lad-mini",()=>toggle(k==="director"?"fx":"director")),btn("—","lad-mini",()=>setCollapsed(k,true),"Collapse to persistent bar"));h.append(actions);const body=el("div","lad-body");body.append(builder());p.append(h,body);document.body.append(p);applyState(p,k,s);drag(p,h,k,s);h.addEventListener("dblclick",e=>{if(!e.target.closest("button"))setCollapsed(k)});h.addEventListener("click",e=>{if(p.classList.contains("lad-collapsed")&&!e.target.closest("button"))setCollapsed(k,false)});return p}
async function refreshMixer(){const host=document.getElementById("lad-mixer-view");if(!host||host.hidden)return;host.innerHTML="";await ensurePlaylist();host.append(el("h3","","Playing backgrounds"));const playing=PLAYLIST.sounds.filter(s=>s.playing);if(!playing.length)host.append(el("p","lad-note","None."));for(const s of playing){const r=el("div","lad-mix-row"),range=document.createElement("input");range.type="range";range.min=0;range.max=1;range.step=.05;range.value=String(s.volume??.55);range.addEventListener("change",()=>s.update({volume:Number(range.value)}));r.append(el("span","",s.name),range,btn("Stop","lad-mini",async()=>{await PLAYLIST.stopSound(s);refreshMixer()}));host.append(r)}host.append(btn("Stop All","lad-btn danger",stopBackgrounds))}
async function status(path){try{const r=await fetch(path,{method:"HEAD",cache:"no-store"});return r.ok?"local":"HTTP "+r.status}catch(_){return"missing"}}
async function refreshSources(){const host=document.getElementById("lad-sources-view");if(!host||host.hidden)return;host.innerHTML="";host.append(el("h3","","Local source audit"),el("p","lad-note","v1.2.2: 16/16 backgrounds and 48/48 logical FX are expected locally."));const list=el("div","lad-source-list");host.append(list);for(const i of [...DATA.backgrounds.map(x=>({title:x.title,path:x.path,type:"BG"})),...DATA.fx.map(x=>({title:x.title,path:x.path,type:"FX"}))]){const r=el("div","lad-source-row");r.append(el("span","lad-source-type",i.type),el("span","lad-source-name",i.title),el("span","lad-source-status","checking…"));list.append(r);status(i.path).then(s=>{r.querySelector(".lad-source-status").textContent=s;r.classList.toggle("bad",s!=="local")})}host.append(btn("Download Diagnostic JSON","lad-btn",downloadDiagnostics),btn("Download Error JSON","lad-btn",downloadErrors))}
async function downloadDiagnostics(){await ensurePlaylist();downloadJson("leylines-audio-diagnostic-"+new Date().toISOString().replaceAll(":","-")+".json",{module:MODULE_ID,version:VERSION,foundry:game.version,system:game.system?.id,systemVersion:game.system?.version,backgrounds:DATA.backgrounds.map(x=>({id:x.id,title:x.title,path:x.path,replacementFor:x.replacementFor||null,playing:!!getSound(x.id)?.playing})),fxCount:DATA.fx.length,physicalFxFiles:new Set(DATA.fx.map(x=>x.path)).size,ui:{director:readState("director"),fx:readState("fx")},runtimeErrors})}
function downloadErrors(){downloadJson("leylines-audio-errors-"+new Date().toISOString().replaceAll(":","-")+".json",{module:MODULE_ID,version:VERSION,errors:runtimeErrors})}
async function ensureMacros(){if(!game.user.isGM)return;for(const [name,command]of [["Leylines Audio Director","globalThis.LeylinesAudioDirector?.toggleDirector();"],["Leylines Sound FX Board","globalThis.LeylinesAudioDirector?.toggleFx();"],["Leylines Audio — Download Diagnostic","globalThis.LeylinesAudioDirector?.downloadDiagnostics();"],["Leylines Audio — Download Errors","globalThis.LeylinesAudioDirector?.downloadErrors();"]]){let m=game.macros.find(x=>x.name===name&&x.getFlag(MODULE_ID,"managed"));if(!m)await Macro.create({name,type:"script",command,flags:{[MODULE_ID]:{managed:true,version:VERSION}}});else if(m.command!==command)await m.update({command,["flags."+MODULE_ID+".version"]:VERSION})}}
Hooks.on("getSceneControlButtons",controls=>{if(!game.user?.isGM)return;const c=controls.sounds??Object.values(controls).find(x=>x.name==="sounds")??controls.tokens;if(!c)return;c.tools||={};const n=Object.keys(c.tools).length;c.tools.leylinesDirector={name:"leylinesDirector",title:"Leylines Audio Director",icon:"fa-solid fa-sliders",order:n+10,button:true,visible:true,onChange:()=>toggle("director")};c.tools.leylinesFx={name:"leylinesFx",title:"Leylines Sound FX Board",icon:"fa-solid fa-drum",order:n+11,button:true,visible:true,onChange:()=>toggle("fx")}});
Hooks.on("chatMessage",(log,msg)=>{const m=String(msg||"").trim().toLowerCase();if(m==="/leylinesaudio"){toggle("director");return false}if(m==="/leylinesfx"){toggle("fx");return false}});
window.addEventListener("keydown",e=>{if(!game?.user?.isGM)return;if(e.ctrlKey&&e.shiftKey&&e.code==="KeyL"){e.preventDefault();toggle("director")}if(e.ctrlKey&&e.shiftKey&&e.code==="KeyF"){e.preventDefault();toggle("fx")}});
Hooks.once("ready",async()=>{if(!game.user.isGM)return;try{await loadData();await ensurePlaylist();await ensureMacros();createPanel("director","Leylines Audio Director",directorContent);createPanel("fx","Leylines Sound FX",fxContent);globalThis.LeylinesAudioDirector={version:VERSION,toggleDirector:()=>toggle("director"),toggleFx:()=>toggle("fx"),playBackground,playFx,stopBackgrounds,downloadDiagnostics,downloadErrors};console.info("Leylines Audio Director "+VERSION+" ready: "+DATA.backgrounds.length+" backgrounds / "+DATA.fx.length+" logical FX.")}catch(e){logError("ready",e);ui.notifications?.error("Leylines Audio Director failed to initialize: "+e.message)}});
'''

CSS=r'''.lad-panel{position:fixed;z-index:10050;background:rgba(18,20,24,.97);border:1px solid #716455;border-radius:7px;box-shadow:0 8px 28px #0009;color:#eee;min-width:290px;min-height:42px;resize:both;overflow:hidden;font-family:var(--font-primary,sans-serif)}.lad-panel.lad-collapsed{resize:none;overflow:hidden}.lad-panel.lad-collapsed .lad-body{display:none}.lad-header{height:42px;display:flex;align-items:center;justify-content:space-between;padding:0 8px 0 12px;background:linear-gradient(90deg,#3b2420,#211f28);cursor:move;user-select:none;border-bottom:1px solid #68594d}.lad-collapsed .lad-header{border-bottom:0;cursor:pointer}.lad-title{font-weight:700}.lad-head-actions{display:flex;gap:5px}.lad-body{height:calc(100% - 42px);overflow:auto;padding:8px}.lad-controls{display:flex;flex-wrap:wrap;gap:7px;align-items:center;margin-bottom:8px}.lad-controls input[type=search]{flex:1;min-width:150px}.lad-btn,.lad-mini,.lad-tab,.lad-track,.lad-fx{border:1px solid #74685c;background:#302c31;color:#f3ede7;border-radius:4px;padding:5px 8px;cursor:pointer}.lad-btn:hover,.lad-mini:hover,.lad-tab:hover,.lad-track:hover,.lad-fx:hover{background:#493c3c}.lad-mini{padding:3px 7px;min-width:26px}.lad-btn.danger{border-color:#9b4b4b}.lad-tabs{display:flex;gap:4px;flex-wrap:wrap;margin:6px 0 8px}.lad-tab.active{background:#71412f;border-color:#c78961}.lad-card{border:1px solid #514a45;background:#26252a;border-radius:6px;padding:8px;margin:7px 0}.lad-card h3{margin:0 0 5px}.lad-note{opacity:.78;margin:4px 0 7px}.lad-track-row{display:flex;gap:5px;flex-wrap:wrap}.lad-track{background:#34313a}.lad-track.alt{border-style:dashed}.lad-fx-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:6px}.lad-fx{min-height:42px;text-align:left}.lad-mix-row{display:grid;grid-template-columns:minmax(150px,1fr) 140px auto;gap:8px;align-items:center;border-bottom:1px solid #444;padding:6px 0}.lad-source-list{display:grid;gap:3px;margin:6px 0 10px}.lad-source-row{display:grid;grid-template-columns:36px minmax(160px,1fr) 80px;gap:6px;padding:4px 5px;background:#25252a}.lad-source-row.bad{background:#452a2a}.lad-source-status{text-align:right}.lad-panel select,.lad-panel input{background:#1d1d22;color:#eee;border:1px solid #5b5550;border-radius:3px;padding:4px}@media(max-width:800px){.lad-panel{max-width:94vw;max-height:85vh}}'''

INSTALL=r'''#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
MODULE_ID="ravnica-leylines-audio-director"
VERSION="1.2.2"
SOURCE="$HERE/$MODULE_ID"
DATA_ROOT="${FOUNDRY_V14_DATA_DIR:-$HOME/Library/Application Support/FoundryVTTV14/Data}"
MODULES="$DATA_ROOT/modules"
DEST="$MODULES/$MODULE_ID"
BACKUPS="$DATA_ROOT/module-backups"
STAMP="$(date +%Y-%m-%d_%H%M%S)"
BACKUP=""
STAGE="$MODULES/.${MODULE_ID}.stage.$$"
fail(){ echo "INSTALL FAILED: $*" >&2; rm -rf "$STAGE" || true; if [[ -n "$BACKUP" && -d "$BACKUP" && ! -d "$DEST" ]]; then mv "$BACKUP" "$DEST"; fi; exit 1; }
[[ -f "$SOURCE/module.json" ]] || fail "module source folder missing: $SOURCE"
mkdir -p "$MODULES" "$BACKUPS"
rm -rf "$STAGE"
cp -R "$SOURCE" "$STAGE"
python3 - "$STAGE/module.json" "$VERSION" <<'PY' || exit 1
import json,sys
d=json.load(open(sys.argv[1])); assert d["id"]=="ravnica-leylines-audio-director"; assert d["version"]==sys.argv[2]
PY
if [[ -d "$DEST" ]]; then BACKUP="$BACKUPS/${MODULE_ID}_${STAMP}"; echo "Backing up -> $BACKUP"; mv "$DEST" "$BACKUP"; fi
echo "Installing staged module with mv -> $DEST"
mv "$STAGE" "$DEST"
python3 - "$DEST/module.json" "$VERSION" <<'PY' || fail "post-install verification failed"
import json,sys,os
d=json.load(open(sys.argv[1])); assert d["version"]==sys.argv[2]
root=os.path.dirname(sys.argv[1])
assert len([x for x in os.listdir(root+"/assets/audio/background") if x.lower().endswith(".mp3")])==16
assert len([x for x in os.listdir(root+"/assets/audio/fx") if x.lower().endswith(".mp3")])==44
PY
echo "Installed $MODULE_ID v$VERSION successfully."
[[ -n "$BACKUP" ]] && echo "Backup: $BACKUP"
'''

README='''# Ravnica Leylines Audio Director v1.2.2

Foundry VTT v14 / D&D5e 5.3.3.

v1.2.2 is self-contained: 16/16 local backgrounds and 48/48 logical FX buttons from 44 local one-shot files.

Cue IDs remain stable:
- carnival -> Halfling Festival
- lucha-libre -> Alien Night Club
- dungeon-mechanical -> Robotics Lab

The Director and FX Board remain independent movable/resizable surfaces which collapse to persistent on-screen bars and reopen with one click. State and geometry persist per browser/client. They do not automatically collapse after a sound is played.

Backgrounds use native Foundry PlaylistSound playback on Music. Replace / Mix In / Add / Alternative remain available with a 2500 ms replacement fade. FX are independent Environment-channel one-shots and never stop or reset background audio.

Launchers: Scene Controls, generated world macros, Ctrl+Shift+L, Ctrl+Shift+F, /leylinesaudio, /leylinesfx.

Run install.sh from the extracted ZIP. Default target:
~/Library/Application Support/FoundryVTTV14/Data/modules
'''

def build():
    if PKG.exists(): shutil.rmtree(PKG)
    if DIST.exists(): shutil.rmtree(DIST)
    DIST.mkdir(parents=True); AUDIO_BG.mkdir(parents=True); AUDIO_FX.mkdir(parents=True)
    manifest={"id":MODULE_ID,"title":TITLE,"description":"Quick-access background and FX director for Leylines and Tigers and Bears, Oh My!","version":VERSION,"authors":[{"name":"MTGFoundry"}],"compatibility":{"minimum":"14","verified":"14.367","maximum":"14"},"relationships":{"systems":[{"id":"dnd5e","type":"system","compatibility":{"minimum":"5.3.3","verified":"5.3.3"}}]},"esmodules":["scripts/main.js"],"styles":["styles/audio-director.css"],"readme":"docs/README.md"}
    write_text(MOD/"module.json",json.dumps(manifest,indent=2)); write_text(MOD/"scripts"/"main.js",MAIN_JS); write_text(MOD/"styles"/"audio-director.css",CSS); write_text(MOD/"docs"/"README.md",README)
    data=make_data()
    for b in BACKGROUND: download(b["url"],AUDIO_BG/b["file"])
    for file,url,ids in FX_SOURCES: download(url,AUDIO_FX/file)
    write_text(PKG/"install.sh",INSTALL); os.chmod(PKG/"install.sh",0o755); write_text(PKG/"README_FIRST.md",README)
    library={"catalogVersion":4,"updated":"2026-10-02","project":"MTGFoundry","downloadDelta":[],"inventory":{"leylinesBackgrounds":16,"leylinesPhysicalFx":44,"leylinesLogicalFx":48,"leylinesPhysicalTotal":60},"backgrounds":[{"library_id":b["id"],"title":b["title"],"file":b["file"],"source_url":b["url"],"status":"bundled","replacementFor":b.get("replacementFor")} for b in BACKGROUND],"fxSources":[{"file":f,"source_url":u,"logical_fx_ids":ids,"status":"bundled"} for f,u,ids in FX_SOURCES],"ownedArchiveProvenance":[{"canonical":"Netrunner_Tabletop_Audio_Backgrounds_12_MP3.zip","legacy":["Archive 5.zip"]},{"canonical":"Skyhorn_Real_FX_30_MP3.zip","legacy":["Archive 6.zip"]},{"canonical":"Skyhorn_Tabletop_Audio_Backgrounds_18_MP3.zip","legacy":["Archive 7.zip"]},{"canonical":"Gatekeeper_Audio_Source_Pack_63_High_Quality_MP3.zip","legacy":["SoundsForSoundlLibraryTabletopandeffects.zip","Gatekeeper_Audio_New_Sources_63_High_Quality_MP3.zip"]},{"canonical":"Ravnica_Leylines_Audio_Source_Pack_56_MP3.zip"}],"ownershipNotes":["Robotics Lab is owned through Gatekeeper v1.3.x and bundled here.","Alien Night Club is owned through Gatekeeper v1.3.x and bundled here.","Halfling Festival is bundled here.","Colosseum is not used because that source was unavailable."]}
    write_text(MOD/"data"/"shared-audio-library.json",json.dumps(library,indent=2)); write_text(PKG/"MTGFoundry_Audio_Library_Current_v4.json",json.dumps(library,indent=2)); write_text(DIST/"MTGFoundry_Audio_Library_Current_v4.json",json.dumps(library,indent=2))
    return data

def qa(data):
    out=[]
    def p(s): out.append("PASS "+s)
    assert len(BACKGROUND)==16;p("16 background definitions")
    assert len(FX_SOURCES)==44;p("44 physical FX definitions")
    assert len(data["fx"])==48 and len(set(x["id"] for x in data["fx"]))==48;p("48/48 unique logical FX definitions")
    assert data["downloadDelta"]==[];p("download delta = 0")
    assert next(x for x in BACKGROUND if x["id"]=="carnival")["title"]=="Halfling Festival";p("carnival cue -> Halfling Festival")
    assert next(x for x in BACKGROUND if x["id"]=="lucha-libre")["title"]=="Alien Night Club";p("lucha-libre cue -> Alien Night Club")
    assert next(x for x in BACKGROUND if x["id"]=="dungeon-mechanical")["title"]=="Robotics Lab";p("dungeon-mechanical cue -> Robotics Lab")
    media=list(AUDIO_BG.glob("*.mp3"))+list(AUDIO_FX.glob("*.mp3"))
    for x in media: ffprobe(x)
    p("all 60 physical MP3s decode with ffprobe")
    assert len(list(AUDIO_BG.glob("*.mp3")))==16;p("16/16 bundled backgrounds")
    assert len(list(AUDIO_FX.glob("*.mp3")))==44;p("44 bundled physical FX")
    subprocess.run(["node","--check",str(MOD/"scripts"/"main.js")],check=True,capture_output=True,text=True);p("JavaScript syntax")
    subprocess.run(["bash","-n",str(PKG/"install.sh")],check=True,capture_output=True,text=True);p("install.sh syntax")
    for j in [MOD/"module.json",MOD/"data"/"audio-cues.json",MOD/"data"/"shared-audio-library.json"]: json.load(open(j))
    p("JSON parse")
    js=(MOD/"scripts"/"main.js").read_text()
    for n in ["lad-collapsed","localStorage","getSceneControlButtons","AudioHelper","channel:\"environment\"","CROSSFADE=2500","downloadDiagnostics","ensureMacros"]: assert n in js,n
    p("persistent collapsible Director/FX bars")
    p("Scene Control launchers, macros and diagnostics")
    p("Environment-channel FX independence")
    p("2500 ms background replacement fade")
    qa_name="Leylines_Audio_Director_v%s_QA.txt"%VERSION
    text="Ravnica Leylines Audio Director v%s — QA\n%s\n\n%s\n\nRuntime note: live Foundry browser/audio-device behavior must still be confirmed in the user's Foundry v14 world.\n"%(VERSION,"="*60,"\n".join(out))
    write_text(PKG/qa_name,text)
    zip_name="Ravnica_Leylines_Audio_Director_v%s_FoundryV14.zip"%VERSION; zp=DIST/zip_name
    with ZipFile(zp,"w",ZIP_DEFLATED,compresslevel=6) as z:
        for f in PKG.rglob("*"):
            if f.is_file(): z.write(f,f.relative_to(PKG))
    with ZipFile(zp) as z:
        bad=z.testzip(); assert bad is None,bad
    p("ZIP integrity")
    text="Ravnica Leylines Audio Director v%s — QA\n%s\n\n%s\n\nRuntime note: live Foundry browser/audio-device behavior must still be confirmed in the user's Foundry v14 world.\n"%(VERSION,"="*60,"\n".join(out))
    write_text(DIST/qa_name,text)
    write_text(DIST/("Ravnica_Leylines_Audio_Director_v%s_SHA256.txt"%VERSION),sha256(zp)+"  "+zip_name+"\n")
    write_text(DIST/"RELEASE_NOTES.md","""# Ravnica Leylines Audio Director v1.2.2

Complete Foundry v14 / D&D5e 5.3.3 package.
16/16 local backgrounds; 48/48 logical FX from 44 local files; zero missing download delta.
Halfling Festival, Alien Night Club and Robotics Lab replace unavailable prior beds while preserving cue IDs.
Persistent collapsible Director and FX bars, Scene Controls, macros, Replace/Mix/Add/Alternative, 2.5 second crossfade, independent Environment FX, diagnostics and timestamped backup/rollback installer are retained.
""")
    print(text); print("ZIP",zp,zp.stat().st_size,sha256(zp))

if __name__=="__main__": qa(build())
