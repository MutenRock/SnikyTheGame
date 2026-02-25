const canvas = document.getElementById('game');
const ctx = canvas.getContext('2d');

const scoreEl = document.getElementById('score');
const distanceEl = document.getElementById('distance');
const speedEl = document.getElementById('speed');
const bestEl = document.getElementById('best');
const stateEl = document.getElementById('state');

const startBtn = document.getElementById('start');
const pauseBtn = document.getElementById('pause');
const resetBtn = document.getElementById('reset');

const bestScoreKey = 'sniky-runner-best-score';
let bestScore = Number(localStorage.getItem(bestScoreKey) || 0);
bestEl.textContent = bestScore;

const groundY = 290;
const gravity = 0.85;
const jumpForce = -14;

let player;
let obstacles;
let particles;
let score;
let distance;
let speed;
let obstacleTimer;
let lastTime;
let running;
let paused;
let frameId;

function newGame() {
  player = { x: 120, y: groundY - 44, w: 42, h: 44, vy: 0, onGround: true };
  obstacles = [];
  particles = [];
  score = 0;
  distance = 0;
  speed = 5;
  obstacleTimer = 0;
  lastTime = 0;
  running = false;
  paused = false;
  updateHud('Prêt');
  draw();
}

function startGame() {
  if (running) return;
  running = true;
  paused = false;
  updateHud('En cours');
  lastTime = performance.now();
  frameId = requestAnimationFrame(loop);
}

function pauseGame() {
  if (!running) return;
  paused = !paused;

  if (paused) {
    updateHud('Pause');
    cancelAnimationFrame(frameId);
  } else {
    updateHud('En cours');
    lastTime = performance.now();
    frameId = requestAnimationFrame(loop);
  }
}

function gameOver() {
  running = false;
  paused = false;
  updateHud('Perdu');
  cancelAnimationFrame(frameId);

  if (score > bestScore) {
    bestScore = score;
    bestEl.textContent = bestScore;
    localStorage.setItem(bestScoreKey, String(bestScore));
  }
}

function jump() {
  if (!running) {
    startGame();
    return;
  }

  if (!paused && player.onGround) {
    player.vy = jumpForce;
    player.onGround = false;

    for (let i = 0; i < 5; i += 1) {
      particles.push({
        x: player.x + 8,
        y: groundY - 2,
        vx: -Math.random() * 2 - 1,
        vy: -Math.random() * 1.5,
        life: 14 + Math.random() * 8,
      });
    }
  }
}

function spawnObstacle() {
  const height = 28 + Math.random() * 30;
  const width = 22 + Math.random() * 20;
  obstacles.push({
    x: canvas.width + width,
    y: groundY - height,
    w: width,
    h: height,
    passed: false,
  });
}

function collides(a, b) {
  return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

function update(dt) {
  const factor = dt / 16.67;

  speed += 0.0016 * dt;
  distance += (speed * dt) / 120;

  player.vy += gravity * factor;
  player.y += player.vy * factor;

  if (player.y + player.h >= groundY) {
    player.y = groundY - player.h;
    player.vy = 0;
    player.onGround = true;
  }

  obstacleTimer += dt;
  const spawnDelay = Math.max(620, 1350 - speed * 60);
  if (obstacleTimer >= spawnDelay) {
    obstacleTimer = 0;
    spawnObstacle();
  }

  obstacles.forEach((obstacle) => {
    obstacle.x -= speed * factor;

    if (!obstacle.passed && obstacle.x + obstacle.w < player.x) {
      obstacle.passed = true;
      score += 10;
    }

    if (collides(player, obstacle)) gameOver();
  });

  obstacles = obstacles.filter((obstacle) => obstacle.x + obstacle.w > -10);

  particles.forEach((p) => {
    p.x += p.vx * factor;
    p.y += p.vy * factor;
    p.vy += 0.12 * factor;
    p.life -= factor;
  });
  particles = particles.filter((p) => p.life > 0);

  updateHud('En cours');
}

function drawBackground() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  const sky = ctx.createLinearGradient(0, 0, 0, groundY);
  sky.addColorStop(0, '#1b2c3f');
  sky.addColorStop(1, '#111821');
  ctx.fillStyle = sky;
  ctx.fillRect(0, 0, canvas.width, groundY);

  ctx.fillStyle = '#1a2532';
  ctx.fillRect(0, groundY, canvas.width, canvas.height - groundY);

  ctx.strokeStyle = 'rgba(255,255,255,0.1)';
  ctx.beginPath();
  ctx.moveTo(0, groundY);
  ctx.lineTo(canvas.width, groundY);
  ctx.stroke();
}

function drawPlayer() {
  ctx.fillStyle = '#75ff9b';
  ctx.fillRect(player.x, player.y, player.w, player.h);

  ctx.fillStyle = '#0f1319';
  ctx.fillRect(player.x + player.w - 14, player.y + 10, 6, 6);
}

function drawObstacles() {
  ctx.fillStyle = '#ff6b6b';
  obstacles.forEach((o) => {
    ctx.fillRect(o.x, o.y, o.w, o.h);
  });
}

function drawParticles() {
  ctx.fillStyle = '#ffb547';
  particles.forEach((p) => {
    ctx.globalAlpha = Math.max(0, p.life / 18);
    ctx.fillRect(p.x, p.y, 3, 3);
  });
  ctx.globalAlpha = 1;
}

function draw() {
  drawBackground();
  drawObstacles();
  drawPlayer();
  drawParticles();
}

function loop(timestamp) {
  if (!running || paused) return;

  const dt = Math.min(40, timestamp - lastTime || 16.67);
  lastTime = timestamp;

  update(dt);
  draw();

  if (running) frameId = requestAnimationFrame(loop);
}

function updateHud(stateText) {
  scoreEl.textContent = Math.floor(score);
  distanceEl.textContent = `${Math.floor(distance)} m`;
  speedEl.textContent = `${(speed / 5).toFixed(1)}x`;
  stateEl.textContent = stateText;
}

function handleActionKey(event) {
  const key = event.key.toLowerCase();
  if ([' ', 'arrowup', 'z', 'w'].includes(key)) {
    event.preventDefault();
    jump();
  }

  if (key === 'p') pauseGame();
}

document.addEventListener('keydown', handleActionKey);
startBtn.addEventListener('click', startGame);
pauseBtn.addEventListener('click', pauseGame);
resetBtn.addEventListener('click', () => {
  cancelAnimationFrame(frameId);
  newGame();
});

newGame();
