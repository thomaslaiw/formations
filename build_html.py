import json, random

with open('C:/Users/user/hermes_output/layers_b64.json') as f:
    layers = json.load(f)

order = list(range(1, len(layers)))  # skip layer 0 (all-shapes)
random.shuffle(order)
flips = [(i % 3 == 2) for i in range(len(order))]  # flip x-axis every 3rd map

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=no">
<title>5 Boards</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#1a1a1a;overflow:hidden;touch-action:manipulation;font-family:'Segoe UI','PingFang HK',system-ui,sans-serif;user-select:none;-webkit-user-select:none}}
#wrap{{width:100vw;height:100vh;display:flex;align-items:center;justify-content:center}}
#board{{position:relative;max-width:100vw;max-height:100vh}}
#board img{{display:block;max-width:100vw;max-height:100vh;object-fit:contain}}

#panel{{position:absolute;top:8px;left:50%;transform:translateX(-50%);z-index:20;
  background:rgba(255,255,255,.85);padding:4px 16px;border-radius:6px;
  color:#000;font-size:20px;font-weight:800;letter-spacing:1px;pointer-events:none}}

.timer{{position:absolute;top:4px;z-index:20;
  width:56px;height:56px;border-radius:50%;display:flex;align-items:center;justify-content:center;
  font-size:28px;font-weight:900;pointer-events:none;
  background:transparent;color:#000;border:3px solid #000}}
.timer.urgent{{color:#c00;border-color:#c00}}
.timer.hold{{color:#c00;border-color:#c00;font-size:16px}}
#timerL{{left:4px}} #timerR{{right:4px}}

/* Big circles */
.bigcircle{{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);z-index:30;
  width:180px;height:180px;border-radius:50%;border:4px solid #000;
  display:flex;align-items:center;justify-content:center;
  font-size:24px;font-weight:900;pointer-events:none;
  transition:opacity .4s;opacity:0}}
#redCircle{{
  background:radial-gradient(circle at 35% 30%, #f88 0%, #d44 30%, #a11 60%, #500 100%);
  color:#fff; text-shadow:0 2px 4px rgba(0,0,0,.4);
}}
#startCircle{{
  background:radial-gradient(circle at 35% 30%, #8f8 0%, #4a4 30%, #1a1 60%, #050 100%);
  color:#fff; text-shadow:0 2px 4px rgba(0,0,0,.4);
}}
#clearCircle{{
  background:radial-gradient(circle at 35% 30%, #ff8 0%, #ee0 30%, #ca0 60%, #880 100%);
  color:#fff; text-shadow:0 2px 4px rgba(0,0,0,.4);
}}

/* Clear decorations */
#clearDeco{{position:absolute;top:0;left:0;right:0;bottom:0;z-index:29;pointer-events:none;opacity:0}}
.ring{{position:absolute;border-radius:50%;border:2px solid #000;top:50%;left:50%;transform:translate(-50%,-50%)}}
.ring.r1{{width:220px;height:220px;animation:ringOut1 2s ease-out infinite}}
@keyframes ringOut1{{0%{{width:190px;height:190px;opacity:.8}}100%{{width:380px;height:380px;opacity:0}}}}
.sparkle{{position:absolute;width:10px;height:10px;background:#000;transform:rotate(45deg)}}
.sparkle.s1{{top:calc(50% - 130px);left:calc(50% - 150px);animation:spark1 2s ease-out infinite}}
.sparkle.s2{{top:calc(50% - 160px);left:calc(50% + 140px);animation:spark2 2s ease-out .4s infinite}}
.sparkle.s3{{top:calc(50% + 120px);left:calc(50% - 160px);animation:spark3 2s ease-out .7s infinite}}
.sparkle.s4{{top:calc(50% + 150px);left:calc(50% + 130px);animation:spark4 2s ease-out 1s infinite}}
@keyframes spark1{{0%{{opacity:0;transform:rotate(45deg) scale(0)}}30%{{opacity:1;transform:rotate(45deg) scale(1)}}100%{{opacity:0;transform:rotate(45deg) scale(0) translateY(-40px)}}}}
@keyframes spark2{{0%{{opacity:0;transform:rotate(45deg) scale(0)}}30%{{opacity:1;transform:rotate(45deg) scale(1)}}100%{{opacity:0;transform:rotate(45deg) scale(0) translateY(-30px)}}}}
@keyframes spark3{{0%{{opacity:0;transform:rotate(45deg) scale(0)}}30%{{opacity:1;transform:rotate(45deg) scale(1)}}100%{{opacity:0;transform:rotate(45deg) scale(0) translateY(-50px)}}}}
@keyframes spark4{{0%{{opacity:0;transform:rotate(45deg) scale(0)}}30%{{opacity:1;transform:rotate(45deg) scale(1)}}100%{{opacity:0;transform:rotate(45deg) scale(0) translateY(-35px)}}}}
</style>
</head>
<body>
<div id="wrap">
  <div id="board">
    <img id="img" src="" alt="board">

    <div id="clearDeco">
      <div class="ring r1"></div>
      <div class="sparkle s1"></div><div class="sparkle s2"></div><div class="sparkle s3"></div><div class="sparkle s4"></div>
    </div>

    <div id="panel">tap to start</div>
    <div class="timer" id="timerL">8</div>
    <div class="timer" id="timerR">8</div>
    <div class="bigcircle" id="redCircle">TUTORIAL</div>
    <div class="bigcircle" id="startCircle">START</div>
    <div class="bigcircle" id="clearCircle">CLEAR</div>
  </div>
</div>
<script>
var IMGS = {json.dumps([f"data:image/jpeg;base64,{layers[i]}" for i in order])};
var FLIPS = {json.dumps(flips)};
var round=0, timeLeft=8, marks=0, gameOver=false, started=false, holding=false, ticker=null;
var phase="red"; // red → blank → green → game → clear
var img=document.getElementById("img"), panel=document.getElementById("panel");
var timerL=document.getElementById("timerL"), timerR=document.getElementById("timerR");
var redCircle=document.getElementById("redCircle");
var startCircle=document.getElementById("startCircle");
var clearCircle=document.getElementById("clearCircle");
var clearDeco=document.getElementById("clearDeco");

function setTimer(t,urgent,hold){{
  timerL.textContent=t; timerR.textContent=t;
  timerL.className=(hold?"timer hold":urgent?"timer urgent":"timer");
  timerR.className=(hold?"timer hold":urgent?"timer urgent":"timer");
}}

function startCountdown(){{
  clearInterval(ticker);
  ticker=setInterval(function(){{
    timeLeft--;
    setTimer(timeLeft, timeLeft<=1, false);
    if(timeLeft<=0){{ clearInterval(ticker); doNextRound(); }}
  }},1000);
}}

function show(i){{
  img.src=IMGS[i];
  img.style.transform=FLIPS[i]?'scaleX(-1)':'';
}}

function doNextRound(){{
  if(gameOver)return;
  round++;
  updatePanel();
  show(round%IMGS.length);
  timeLeft=8; setTimer(8,false,false);
  holding=false;
  startCountdown();
}}
function updatePanel(){{ panel.textContent="mark: "+marks+"/8"; }}
function ownerTap(){{
  if(holding)return;
  holding=true;
  clearInterval(ticker);
  if(marks<8){{ marks++; }}
  updatePanel();
  if(marks>=8){{
    setTimer("✓",false,false);
    clearCircle.style.opacity=1;
    clearDeco.style.opacity=1;
    gameOver=true; phase="clear";
    return;
  }}
  setTimer("HOLD",false,true);
  setTimeout(function(){{ if(!gameOver) doNextRound(); }},1000);
}}

document.getElementById("wrap").onclick=function(){{
  // Phase: red → blank → green → game
  if(phase==="red"){{
    redCircle.style.opacity=0;
    panel.textContent="";
    phase="blank";
    return;
  }}
  if(phase==="blank"){{
    startCircle.style.opacity=1;
    panel.textContent="tap to start";
    phase="green";
    return;
  }}
  if(phase==="green"){{
    started=true;
    startCircle.style.opacity=0;
    marks=0; round=0;
    updatePanel();
    doNextRound();
    phase="game";
    return;
  }}
  if(phase==="clear"){{
    round=0; marks=0; gameOver=false; started=false; holding=false;
    clearInterval(ticker);
    clearCircle.style.opacity=0;
    clearDeco.style.opacity=0;
    redCircle.style.opacity=1;
    panel.textContent=""; setTimer(8,false,false);
    show(0);
    phase="red";
    return;
  }}
  // phase === "game"
  if(!started){{
    started=true;
    startCircle.style.opacity=0;
    marks=0; round=0;
    updatePanel();
    doNextRound();
    return;
  }}
  ownerTap();
}};

show(0); setTimer(8,false,false);
redCircle.style.opacity=1; panel.textContent="";
</script>
</body>
</html>'''

with open('C:/Users/user/hermes_output/formations.html','w',encoding='utf-8') as f:
    f.write(html)
print('Done')
