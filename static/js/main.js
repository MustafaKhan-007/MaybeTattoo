/* ============================================================
   MAYBE TATTOO BERLIN — main.js
   Navbar, scroll animations, gallery, lightbox, stats,
   booking form, contact forms.
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {
  initYear();
  initNavbar();
  initMobileMenu();
  initScrollAnimations();
  initParallax();
  initStatsCounter();
  initGalleryTabs();
  initLightbox();
  initArtistFilter();
  initFlipCardsTouch();
  initBookingForm();
  initContactForms();
});

/* ---------- Footer year ---------- */
function initYear() {
  const el = document.getElementById('year');
  if (el) el.textContent = new Date().getFullYear();
}

/* ---------- Navbar scroll state ---------- */
function initNavbar() {
  const nav = document.getElementById('navbar');
  if (!nav) return;
  const onScroll = () => {
    if (window.scrollY > 80) nav.classList.add('scrolled');
    else nav.classList.remove('scrolled');
  };
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });
}

/* ---------- Mobile hamburger menu ---------- */
function initMobileMenu() {
  const burger = document.getElementById('hamburger');
  const links = document.getElementById('navLinks');
  if (!burger || !links) return;

  const toggle = () => {
    const open = links.classList.toggle('open');
    burger.classList.toggle('open', open);
    burger.setAttribute('aria-expanded', String(open));
    document.body.style.overflow = open ? 'hidden' : '';
  };

  burger.addEventListener('click', toggle);

  links.querySelectorAll('a').forEach((a) => {
    a.addEventListener('click', () => {
      if (links.classList.contains('open')) toggle();
    });
  });
}

/* ---------- Scroll-triggered animations ---------- */
function initScrollAnimations() {
  const els = document.querySelectorAll('.fade-in, .slide-left, .slide-right, .scale-in');
  if (!('IntersectionObserver' in window) || !els.length) {
    els.forEach((el) => el.classList.add('visible'));
    return;
  }
  const obs = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          obs.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12, rootMargin: '0px 0px -60px 0px' }
  );
  els.forEach((el) => obs.observe(el));
}

/* ---------- Hero parallax ---------- */
function initParallax() {
  const bg = document.querySelector('.hero-bg');
  if (!bg) return;
  let ticking = false;
  window.addEventListener(
    'scroll',
    () => {
      if (!ticking) {
        window.requestAnimationFrame(() => {
          const offset = window.scrollY * 0.5;
          bg.style.transform = `translateY(${offset}px)`;
          ticking = false;
        });
        ticking = true;
      }
    },
    { passive: true }
  );
}

/* ---------- Animated stat counters ---------- */
function initStatsCounter() {
  const nums = document.querySelectorAll('.stat-number[data-target]');
  if (!nums.length) return;

  const animate = (el) => {
    const target = parseInt(el.dataset.target, 10);
    const suffix = el.dataset.suffix || '';
    const duration = 1800;
    const start = performance.now();
    const step = (now) => {
      const p = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.floor(eased * target).toLocaleString('en-US') + suffix;
      if (p < 1) requestAnimationFrame(step);
      else el.textContent = target.toLocaleString('en-US') + suffix;
    };
    requestAnimationFrame(step);
  };

  const obs = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          animate(entry.target);
          obs.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.5 }
  );
  nums.forEach((n) => obs.observe(n));
}

/* ============================================================
   GALLERY IMAGE LOADING
   ============================================================ */
const categories = {
  grafik: 'tattoo,graphic,blackwork',
  realismus: 'tattoo,realism,portrait',
  mini: 'tattoo,minimalist,small',
  overlapping: 'tattoo,sleeve,layered',
  farbrealismus: 'tattoo,color,watercolor',
  polynesien: 'tattoo,polynesian,tribal',
};

/* Build an image URL. The legacy Unsplash Source endpoint is no
   longer reliable, so each <img> also gets an onerror fallback to
   a deterministic, always-available image (see createCard). */
function unsplashUrl(keywords, sig, w = 600, h = 800) {
  return `https://source.unsplash.com/${w}x${h}/?${encodeURIComponent(keywords)}&sig=${sig}`;
}

function fallbackUrl(category, sig, w = 600, h = 800) {
  // Lorem Picsum is highly reliable and keeps images loading.
  return `https://picsum.photos/seed/${category}-${sig}/${w}/${h}`;
}

function createCard(category, keywords, sig, w, h) {
  const card = document.createElement('div');
  card.className = 'gallery-card';

  const img = document.createElement('img');
  img.loading = 'lazy';
  img.alt = `${category} tattoo ${sig}`;
  img.classList.add('gallery-img');
  img.src = unsplashUrl(keywords, sig, w, h);
  img.dataset.fallback = fallbackUrl(category, sig, w, h);
  img.addEventListener('error', function onErr() {
    img.removeEventListener('error', onErr);
    img.src = img.dataset.fallback;
  });

  const overlay = document.createElement('div');
  overlay.className = 'overlay';
  overlay.innerHTML = '<span class="plus">+</span>';

  card.appendChild(img);
  card.appendChild(overlay);
  return card;
}

function loadGalleryImages(category, count, gridId) {
  const grid = document.getElementById(gridId || 'gallery-grid');
  if (!grid) return;
  const keywords = categories[category] || 'tattoo';
  const w = parseInt(grid.dataset.w, 10) || 600;
  const h = parseInt(grid.dataset.h, 10) || 800;

  grid.style.opacity = '0';
  setTimeout(() => {
    grid.innerHTML = '';
    for (let i = 1; i <= count; i++) {
      grid.appendChild(createCard(category, keywords, i, w, h));
    }
    grid.style.transition = 'opacity 0.4s ease';
    grid.style.opacity = '1';
    if (window.__galleryLightboxRefresh) window.__galleryLightboxRefresh();
  }, 300);
}

function initGalleryTabs() {
  document.querySelectorAll('[data-gallery-tabs]').forEach((tabWrap) => {
    const gridId = tabWrap.dataset.grid;
    const grid = document.getElementById(gridId);
    const count = parseInt(grid?.dataset.count, 10) || 6;
    const tabs = tabWrap.querySelectorAll('.tab');
    const useHash = tabWrap.dataset.hash === 'true';

    const activate = (tab, pushHash) => {
      tabs.forEach((t) => t.classList.remove('active'));
      tab.classList.add('active');
      const cat = tab.dataset.category;
      loadGalleryImages(cat, count, gridId);
      if (useHash && pushHash) {
        history.replaceState(null, '', '#' + cat);
      }
    };

    tabs.forEach((tab) => {
      tab.addEventListener('click', () => activate(tab, true));
    });

    // Honor URL hash on load (shareable gallery links)
    let initial = tabs[0];
    if (useHash && location.hash) {
      const hashCat = location.hash.replace('#', '');
      const match = [...tabs].find((t) => t.dataset.category === hashCat);
      if (match) initial = match;
    }
    if (initial) activate(initial, false);
  });
}

/* ============================================================
   LIGHTBOX (pure JS)
   ============================================================ */
function initLightbox() {
  const lb = document.getElementById('lightbox');
  if (!lb) return;
  const lbImg = lb.querySelector('img');
  let imgs = [];
  let idx = 0;

  const refresh = () => {
    imgs = [...document.querySelectorAll('#gallery-grid .gallery-img')];
  };
  window.__galleryLightboxRefresh = refresh;
  refresh();

  const open = (i) => {
    idx = i;
    lbImg.src = imgs[idx].src;
    lb.classList.add('open');
    document.body.style.overflow = 'hidden';
  };
  const close = () => {
    lb.classList.remove('open');
    document.body.style.overflow = '';
  };
  const show = (delta) => {
    if (!imgs.length) return;
    idx = (idx + delta + imgs.length) % imgs.length;
    lbImg.src = imgs[idx].src;
  };

  document.addEventListener('click', (e) => {
    const card = e.target.closest('#gallery-grid .gallery-card');
    if (card) {
      refresh();
      const cardImg = card.querySelector('.gallery-img');
      const i = imgs.indexOf(cardImg);
      if (i > -1) open(i);
    }
  });

  lb.querySelector('.lb-close').addEventListener('click', close);
  lb.querySelector('.lb-prev').addEventListener('click', () => show(-1));
  lb.querySelector('.lb-next').addEventListener('click', () => show(1));
  lb.addEventListener('click', (e) => {
    if (e.target === lb) close();
  });
  document.addEventListener('keydown', (e) => {
    if (!lb.classList.contains('open')) return;
    if (e.key === 'Escape') close();
    if (e.key === 'ArrowLeft') show(-1);
    if (e.key === 'ArrowRight') show(1);
  });
}

/* ============================================================
   ARTIST FILTER (artists page)
   ============================================================ */
function initArtistFilter() {
  const filterBar = document.querySelector('[data-artist-filter]');
  if (!filterBar) return;
  const tabs = filterBar.querySelectorAll('.tab');
  const cards = document.querySelectorAll('.flip-card');

  tabs.forEach((tab) => {
    tab.addEventListener('click', () => {
      tabs.forEach((t) => t.classList.remove('active'));
      tab.classList.add('active');
      const filter = tab.dataset.filter;
      cards.forEach((card) => {
        const styles = (card.dataset.styles || '').toLowerCase();
        const match = filter === 'all' || styles.includes(filter.toLowerCase());
        if (match) {
          card.classList.remove('hidden');
          card.style.opacity = '0';
          requestAnimationFrame(() => {
            card.style.opacity = '1';
          });
        } else {
          card.classList.add('hidden');
        }
      });
    });
  });
}

/* ---------- Flip cards: tap-to-flip on touch devices ---------- */
function initFlipCardsTouch() {
  if (!window.matchMedia('(hover: none)').matches) return;
  document.querySelectorAll('.flip-card').forEach((card) => {
    card.addEventListener('click', (e) => {
      if (e.target.closest('a')) return;
      card.classList.toggle('flipped');
    });
  });
}

/* ============================================================
   BOOKING — multi-step form
   ============================================================ */
function initBookingForm() {
  const form = document.getElementById('bookingForm');
  if (!form) return;

  const steps = form.querySelectorAll('.form-step');
  const progSteps = form.querySelectorAll('.progress-step');
  const successMsg = document.getElementById('bookingSuccess');
  let current = 0;

  const priceMap = {
    'Up to 10cm': 'from €150',
    '10–20cm': 'from €300',
    '20cm+': 'from €600',
    'Not sure yet': 'Free consultation',
  };

  const showStep = (n) => {
    steps.forEach((s, i) => s.classList.toggle('active', i === n));
    progSteps.forEach((p, i) => {
      p.classList.toggle('active', i === n);
      p.classList.toggle('done', i < n);
    });
    current = n;
    form.scrollIntoView({ behavior: 'smooth', block: 'start' });
  };

  // option pills (single-select per group)
  form.querySelectorAll('.option-grid').forEach((group) => {
    group.querySelectorAll('.option-pill').forEach((pill) => {
      pill.addEventListener('click', () => {
        group.querySelectorAll('.option-pill').forEach((p) => p.classList.remove('selected'));
        pill.classList.add('selected');

        if (group.dataset.field === 'size') {
          const priceEl = document.getElementById('priceValue');
          if (priceEl) priceEl.textContent = priceMap[pill.dataset.value] || 'from €150';
        }
      });
    });
  });

  form.querySelectorAll('[data-next]').forEach((btn) => {
    btn.addEventListener('click', () => {
      if (current < steps.length - 1) showStep(current + 1);
    });
  });
  form.querySelectorAll('[data-prev]').forEach((btn) => {
    btn.addEventListener('click', () => {
      if (current > 0) showStep(current - 1);
    });
  });

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    form.style.display = 'none';
    if (successMsg) successMsg.classList.add('show');
  });

  showStep(0);
}

/* ============================================================
   CONTACT / quick forms — inline success
   ============================================================ */
function initContactForms() {
  document.querySelectorAll('[data-inline-form]').forEach((form) => {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const msg = form.querySelector('.inline-success');
      form.querySelectorAll('input, textarea, select, button').forEach((el) => (el.disabled = true));
      if (msg) {
        msg.style.display = 'block';
        msg.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    });
  });
}
