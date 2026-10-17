from pathlib import Path
p=Path(__file__).with_name('index.html')
s=p.read_text(encoding='utf-8-sig')
s=s.replace('BRINESPACE / MOTION STUDY 02','BRINESPACE / MOTION STUDY 03').replace('Separate alien inhabitants in quiet, empty tank artwork.','Larger solitary swimmers above sand, rocks and swaying sea plants.')
s=s.replace('> Growth</label>','> Sea plants</label><label><input id="habitat" type="checkbox" checked> Sand & rocks</label>')
s=s.replace('<span>Plated driftling</span><span>Spiral frond</span><span>Fan colony</span>','<span>Swaying spiral sea plants</span>')
s=s.replace("Math.sin(phase)*.035","Math.sin(phase)*.075")
start=s.index('function tank(t,index)')
end=s.index('\nfunction render()',start)
s=s[:start]+'''function tank(t,index){
 ctx.save();ctx.translate(t.x,t.y);ctx.scale(t.scale,t.scale);
 ctx.drawImage(images.tanks,...t.crop,0,0,t.crop[2],t.crop[3]);
 const [x,y,w,h]=t.window;ctx.save();ctx.beginPath();
 if(t.round)ctx.roundRect(x,y,w,h,[8,8,50,50]);else ctx.rect(x,y,w,h);ctx.clip();
 if(ui('habitat').checked){const bedW=w*1.06,bedH=bedW*332/1923;ctx.drawImage(images.habitat,33,309,1923,332,x-w*.03,y+h-bedH+5,bedW,bedH)}
 if(ui('growth').checked){const plantW=h*.31,plantH=plantW*sprites[3].height/sprites[3].width;body(3,x+w*.20,y+h*.92-plantH/2,plantW,time*.55+index,1,true)}
 if(ui('life').checked){if(index===0){const p=time*.22;body(0,x+w*(.52+.20*Math.sin(p)),y+h*(.32+.06*Math.sin(p*1.7)),w*.34,time*1.6,Math.cos(p)>=0?-1:1)}else{body(1,x+w*(.57+.10*Math.sin(time*.30)),y+h*(.37+.07*Math.sin(time*.65)),w*.52,time*1.0)}}
 ctx.fillStyle='rgba(30,55,65,.09)';ctx.fillRect(x,y,w,h);ctx.restore();ctx.restore();
}'''+s[end:]
s=s.replace("species:sprites.length,view:","species:sprites.length,visibleSwimmers:ui('life').checked?2:0,visiblePlants:ui('growth').checked?2:0,habitat:ui('habitat').checked,view:")
s=s.replace("load('life','../alien-life.png')","load('life','../alien-life.png'),load('habitat','sand-rocks.png')")
s=s.replace('Five separate life sprites · two tank windows','One swimmer per tank · separate habitat layers')
p.write_text(s,encoding='utf-8')
