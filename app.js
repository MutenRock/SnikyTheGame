const canvas = document.getElementById('game');
const ctx = canvas.getContext('2d');

const scoreEl = document.getElementById('score');
const distanceEl = document.getElementById('distance');
const speedEl = document.getElementById('speed');
const comboEl = document.getElementById('combo');
const bestEl = document.getElementById('best');
const stateEl = document.getElementById('state');

const startBtn = document.getElementById('start');
const pauseBtn = document.getElementById('pause');
const resetBtn = document.getElementById('reset');

const bestScoreKey = 'sniky-runner-best-score';
let bestScore = Number(localStorage.getItem(bestScoreKey) || 0);
bestEl.textContent = bestScore;

const groundY = 296;
const gravity = 0.93;
const jumpForce = -15;

let player;
let obstacles;
let particles;
let score;
let distance;
let speed;
let dodgeCombo;
let obstacleTimer;
let lastTime;
let running;
let paused;
let frameId;
let worldTime;

const sprites = {
  runA: loadSprite('assets/sniky-run-1.svg'),
  runB: loadSprite('assets/sniky-run-2.svg'),
  jump: loadSprite('assets/sniky-jump.svg'),
  rock: loadSprite('assets/obstacle-rock.svg'),
  spike: loadSprite('assets/obstacle-spike.svg'),
  drone: loadSprite('assets/obstacle-drone.svg'),
};

function loadSprite(src) {
  const image = new Image();
  image.src = src;
  return image;
}

function newGame() {
  player = {
    x: 120,
    y: groundY - 58,
    w: 56,
    h: 58,
    vy: 0,
    onGround: true,
    animTimer: 0,
    animFrame: 0,
  };

  obstacles = [];
  particles = [];
  score = 0;
  distance = 0;
  speed = 5.2;
  dodgeCombo = 0;
  obstacleTimer = 0;
  lastTime = 0;
  worldTime = 0;
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
    createDust(9);
  }
}

function createDust(amount) {
  for (let i = 0; i < amount; i += 1) {
    particles.push({
      x: player.x + 18,
      y: groundY - 4,
      vx: -(Math.random() * 2.2 + 0.4),
      vy: -(Math.random() * 1.4 + 0.2),
      life: 16 + Math.random() * 10,
      size: 2 + Math.random() * 2,
    });
  }
}

function createObstacle() {
  const lane = Math.random();
  if (lane < 0.5) {
    obstacles.push({
      type: 'rock',
      x: canvas.width + 40,
      y: groundY - 48,
      w: 52,
      h: 48,
      passed: false,
      scoreValue: 10,
    });
    return;
  }

  if (lane < 0.85) {
    obstacles.push({
      type: 'spike',
      x: canvas.width + 30,
      y: groundY - 42,
      w: 54,
      h: 42,
      passed: false,
      scoreValue: 14,
    });
    return;
  }

  obstacles.push({
    type: 'drone',
    x: canvas.width + 80,
    y: groundY - 128,
    w: 80,
    h: 38,
    passed: false,
    scoreValue: 18,
  });
}

function collides(a, b) {
  const margin = 6;
  return (
    a.x + margin < b.x + b.w &&
    a.x + a.w - margin > b.x &&
    a.y + margin < b.y + b.h &&
    a.y + a.h - margin > b.y
  );
}

function update(dt) {
  const factor = dt / 16.67;
  worldTime += dt;

  speed += 0.0015 * dt;
  distance += (speed * dt) / 120;

  player.vy += gravity * factor;
  player.y += player.vy * factor;

  if (player.y + player.h >= groundY) {
    if (!player.onGround) {
      createDust(5);
    }
    player.y = groundY - player.h;
    player.vy = 0;
    player.onGround = true;
  }

  player.animTimer += dt;
  if (player.animTimer > 110) {
    player.animTimer = 0;
    player.animFrame = (player.animFrame + 1) % 2;
  }

  obstacleTimer += dt;
  const spawnDelay = Math.max(570, 1200 - speed * 62);
  if (obstacleTimer >= spawnDelay) {
    obstacleTimer = 0;
    createObstacle();
  }

  obstacles.forEach((obstacle) => {
    obstacle.x -= speed * factor;

    if (!obstacle.passed && obstacle.x + obstacle.w < player.x) {
      obstacle.passed = true;
      dodgeCombo += 1;
      score += obstacle.scoreValue + Math.min(20, dodgeCombo * 2);
    }

    if (collides(player, obstacle)) {
      gameOver();
    }
  });

  obstacles = obstacles.filter((obstacle) => obstacle.x + obstacle.w > -20);

  particles.forEach((particle) => {
    particle.x += particle.vx * factor;
    particle.y += particle.vy * factor;
    particle.vy += 0.14 * factor;
    particle.life -= factor;
  });
  particles = particles.filter((particle) => particle.life > 0);

  if (player.onGround && dodgeCombo > 0 && Math.random() < 0.012) {
    dodgeCombo -= 1;
  }

  updateHud('En cours');
}

function drawBackground() {
  const sky = ctx.createLinearGradient(0, 0, 0, groundY);
  sky.addColorStop(0, '#1f3046');
  sky.addColorStop(1, '#121b27');
  ctx.fillStyle = sky;
  ctx.fillRect(0, 0, canvas.width, groundY);

  drawParallaxLayer(48, 0.18, '#27384c', 80, 18);
  drawParallaxLayer(64, 0.35, '#32465f', 116, 24);

  ctx.fillStyle = '#1a2736';
  ctx.fillRect(0, groundY, canvas.width, canvas.height - groundY);

  ctx.strokeStyle = 'rgba(255, 255, 255, 0.12)';
  ctx.beginPath();
  ctx.moveTo(0, groundY);
  ctx.lineTo(canvas.width, groundY);
  ctx.stroke();

  const roadOffset = -((worldTime * speed * 0.04) % 44);
  ctx.fillStyle = '#40566f';
  for (let x = roadOffset; x < canvas.width + 50; x += 44) {
    ctx.fillRect(x, groundY + 24, 20, 4);
  }
}

function drawParallaxLayer(baseY, ratio, color, width, minHeight) {
  const offset = -((worldTime * speed * ratio) % width);
  ctx.fillStyle = color;
  for (let x = offset; x < canvas.width + width; x += width) {
    const shapeHeight = minHeight + ((x / width) % 3) * 10;
    ctx.fillRect(x, groundY - baseY - shapeHeight, width - 8, shapeHeight);
  }
}

function drawPlayer() {
  let image = sprites.runA;
  if (!player.onGround) {
    image = sprites.jump;
  } else {
    image = player.animFrame === 0 ? sprites.runA : sprites.runB;
  }

  if (image.complete) {
    ctx.drawImage(image, player.x, player.y, player.w, player.h);
  } else {
    ctx.fillStyle = '#74ffab';
    ctx.fillRect(player.x, player.y, player.w, player.h);
  }
}

function drawObstacles() {
  obstacles.forEach((obstacle) => {
    const image = sprites[obstacle.type];
    if (image && image.complete) {
      ctx.drawImage(image, obstacle.x, obstacle.y, obstacle.w, obstacle.h);
      return;
    }

    ctx.fillStyle = obstacle.type === 'drone' ? '#8f96ff' : '#ff6e6e';
    ctx.fillRect(obstacle.x, obstacle.y, obstacle.w, obstacle.h);
  });
}

function drawParticles() {
  particles.forEach((particle) => {
    ctx.globalAlpha = Math.max(0, particle.life / 26);
    ctx.fillStyle = '#ffd786';
    ctx.fillRect(particle.x, particle.y, particle.size, particle.size);
  });
  ctx.globalAlpha = 1;
}

function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
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

  if (running) {
    frameId = requestAnimationFrame(loop);
  }
}

function updateHud(stateText) {
  scoreEl.textContent = Math.floor(score);
  distanceEl.textContent = `${Math.floor(distance)} m`;
  speedEl.textContent = `${(speed / 5).toFixed(1)}x`;
  comboEl.textContent = `x${dodgeCombo}`;
  stateEl.textContent = stateText;
}

function handleActionKey(event) {
  const key = event.key.toLowerCase();
  if ([' ', 'arrowup', 'z', 'w'].includes(key)) {
    event.preventDefault();
    jump();
  }

  if (key === 'p') {
    pauseGame();
  }
}

document.addEventListener('keydown', handleActionKey);
startBtn.addEventListener('click', startGame);
pauseBtn.addEventListener('click', pauseGame);
resetBtn.addEventListener('click', () => {
  cancelAnimationFrame(frameId);
  newGame();
});

newGame();
