/* ========== 平滑滚动 ========== */
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    const targetId = this.getAttribute('href');
    if (targetId === '#') return;
    const target = document.querySelector(targetId);
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});

/* ========== 滚动揭示动画 ========== */
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry, idx) => {
    if (entry.isIntersecting) {
      // 同级卡片错峰出现
      setTimeout(() => {
        entry.target.classList.add('is-visible');
      }, idx * 80);
      revealObserver.unobserve(entry.target);
    }
  });
}, {
  threshold: 0.1,
  rootMargin: '0px 0px -50px 0px'
});

document.querySelectorAll('.project-card, .stat-card, .highlight, .about-content, .section-header').forEach(el => {
  el.classList.add('reveal');
  revealObserver.observe(el);
});

/* ========== 数字滚动动画 ========== */
const animateNumber = (el, target, suffix = '', duration = 1800) => {
  const start = 0;
  const startTime = performance.now();

  const update = (now) => {
    const elapsed = now - startTime;
    const progress = Math.min(elapsed / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3); // easeOutCubic
    const current = start + (target - start) * eased;

    if (target % 1 === 0) {
      el.firstChild.nodeValue = current.toFixed(0) + suffix;
    } else {
      el.firstChild.nodeValue = current.toFixed(2) + suffix;
    }

    if (progress < 1) requestAnimationFrame(update);
  };
  requestAnimationFrame(update);
};

const statsObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const numEl = entry.target.querySelector('.stat-number');
      const target = parseFloat(numEl.dataset.animate);
      const suffix = numEl.dataset.suffix || '';
      if (!isNaN(target)) {
        animateNumber(numEl, target, suffix);
      }
      statsObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.5 });

document.querySelectorAll('.stat-card').forEach(card => statsObserver.observe(card));

/* ========== 导航高亮 ========== */
const sections = document.querySelectorAll('section[id]');
const navLinks = document.querySelectorAll('.nav-links a');

const navObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const id = entry.target.id;
      navLinks.forEach(link => {
        link.style.color = link.getAttribute('href') === `#${id}`
          ? 'var(--text-primary)'
          : '';
      });
    }
  });
}, { threshold: 0.3, rootMargin: '-80px 0px -50% 0px' });

sections.forEach(section => navObserver.observe(section));

/* ========== 背景光晕 (额外一层青色) ========== */
const orb = document.createElement('div');
orb.className = 'bg-orb-3';
document.body.appendChild(orb);

/* ========== Hero 标题渐入 ========== */
window.addEventListener('load', () => {
  const hero = document.querySelector('.hero-content');
  if (hero) hero.style.animation = 'fadeUp 0.8s ease-out';
});

/* ========== Console Signature ========== */
console.log(
  '%c方逸之 · AI 产品工程师',
  'color:#667eea;font-size:18px;font-weight:bold;'
);
console.log(
  '%c联系我 → frank-fangyz@139.com',
  'color:#48bb78;font-size:13px;'
);