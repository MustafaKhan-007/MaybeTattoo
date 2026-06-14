/* ============================================================
   MaybeTattoo Berlin — interactions
   ============================================================ */
(function () {
  "use strict";

  /* ---------------- i18n toggle ---------------- */
  const I18N = window.I18N || {};
  let lang = window.CURRENT_LANG || "en";

  function applyLang(next) {
    if (!I18N[next]) return;
    lang = next;
    document.documentElement.lang = next;
    document.body.dataset.lang = next;

    document.querySelectorAll("[data-i18n]").forEach((el) => {
      const key = el.getAttribute("data-i18n");
      const val = I18N[next][key];
      if (val !== undefined) el.textContent = val;
    });
    // review + bio dynamic fields
    document.querySelectorAll("[data-i18n-review-" + next + "]").forEach((el) => {
      el.textContent = el.getAttribute("data-i18n-review-" + next);
    });
    document.querySelectorAll("[data-i18n-bio-" + next + "]").forEach((el) => {
      el.textContent = el.getAttribute("data-i18n-bio-" + next);
    });

    document.querySelectorAll("[data-lang-btn]").forEach((b) => {
      b.classList.toggle("active", b.getAttribute("data-lang-btn") === next);
    });
    try { localStorage.setItem("mt_lang", next); } catch (e) {}
    // keep server cookie in sync without reload via querystring on next nav
    document.cookie = "lang=" + next + ";path=/;max-age=31536000;samesite=Lax";
  }

  document.querySelectorAll("[data-lang-btn]").forEach((btn) => {
    btn.addEventListener("click", () => applyLang(btn.getAttribute("data-lang-btn")));
  });

  // restore saved language preference
  try {
    const saved = localStorage.getItem("mt_lang");
    if (saved && saved !== lang) applyLang(saved);
  } catch (e) {}

  /* ---------------- navbar scroll + mobile ---------------- */
  const navbar = document.getElementById("navbar");
  const onScroll = () => {
    if (navbar) navbar.classList.toggle("scrolled", window.scrollY > 40);
    // parallax hero
    document.querySelectorAll("[data-parallax]").forEach((el) => {
      el.style.transform = "scale(1.1) translateY(" + window.scrollY * 0.3 + "px)";
    });
  };
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  const burger = document.getElementById("navBurger");
  const navMobile = document.getElementById("navMobile");
  if (burger && navMobile) {
    burger.addEventListener("click", () => navMobile.classList.toggle("open"));
    navMobile.querySelectorAll("a").forEach((a) =>
      a.addEventListener("click", () => navMobile.classList.remove("open"))
    );
  }

  /* ---------------- scroll reveal ---------------- */
  const revealObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          revealObserver.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12 }
  );
  document.querySelectorAll(".reveal").forEach((el) => revealObserver.observe(el));

  /* ---------------- animated counters ---------------- */
  const countObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        const el = entry.target;
        const target = parseInt(el.getAttribute("data-count"), 10) || 0;
        const suffix = el.getAttribute("data-suffix") || "";
        const dur = 1800;
        const start = performance.now();
        const tick = (now) => {
          const p = Math.min((now - start) / dur, 1);
          const eased = 1 - Math.pow(1 - p, 3);
          el.textContent = Math.floor(eased * target).toLocaleString() + (p === 1 ? suffix : "");
          if (p < 1) requestAnimationFrame(tick);
        };
        requestAnimationFrame(tick);
        countObserver.unobserve(el);
      });
    },
    { threshold: 0.5 }
  );
  document.querySelectorAll("[data-count]").forEach((el) => countObserver.observe(el));

  /* ---------------- video placeholder ---------------- */
  const vph = document.getElementById("videoPlaceholder");
  if (vph) {
    vph.addEventListener("click", () => {
      alert("Demo placeholder — the studio's intro video would play here.");
    });
  }

  /* ---------------- artist booking accordion ---------------- */
  document.querySelectorAll(".book-toggle").forEach((btn) => {
    btn.addEventListener("click", () => {
      const panel = document.getElementById(btn.getAttribute("data-target"));
      if (!panel) return;
      const open = !panel.hidden;
      panel.hidden = open;
      if (!open) panel.scrollIntoView({ behavior: "smooth", block: "nearest" });
    });
  });

  /* ---------------- booking form (artists page) ---------------- */
  document.querySelectorAll("[data-booking-form]").forEach((form) => {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const fd = Object.fromEntries(new FormData(form).entries());
      fd.source = "artist_page";
      await postBooking(fd);
      const ok = form.querySelector(".form-success");
      if (ok) ok.hidden = false;
      form.querySelectorAll("input,textarea,button").forEach((i) => (i.disabled = true));
    });
  });

  async function postBooking(payload) {
    try {
      const res = await fetch("/api/book", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      return await res.json();
    } catch (err) {
      console.error("Booking failed", err);
      return { ok: false };
    }
  }

  /* ---------------- gallery filter ---------------- */
  const grid = document.getElementById("galleryGrid");
  if (grid) {
    const buttons = document.querySelectorAll(".filter-btn");
    const filter = (cat) => {
      buttons.forEach((b) => b.classList.toggle("active", b.getAttribute("data-filter") === cat));
      grid.querySelectorAll(".masonry-item").forEach((item) => {
        const show = cat === "all" || item.getAttribute("data-category") === cat;
        item.style.display = show ? "" : "none";
      });
      buildLightboxList();
    };
    buttons.forEach((b) => b.addEventListener("click", () => {
      const cat = b.getAttribute("data-filter");
      filter(cat);
      history.replaceState(null, "", cat === "all" ? location.pathname : "?category=" + cat);
    }));
    const initialCat =
      new URLSearchParams(location.search).get("category") ||
      (document.querySelector(".filter-btn.active") || {}).dataset?.filter;
    if (initialCat && initialCat !== "all") filter(initialCat);
  }

  /* ---------------- lightbox ---------------- */
  const lightbox = document.getElementById("lightbox");
  let lbItems = [];
  let lbIndex = 0;

  function buildLightboxList() {
    lbItems = Array.from(document.querySelectorAll("[data-lightbox]")).filter(
      (el) => el.style.display !== "none"
    );
  }

  function openLightbox(i) {
    if (!lightbox) return;
    lbIndex = (i + lbItems.length) % lbItems.length;
    const el = lbItems[lbIndex];
    const img = document.getElementById("lightboxImg");
    const cat = document.getElementById("lightboxCat");
    img.src = el.getAttribute("href");
    const catKey = el.getAttribute("data-category");
    cat.textContent = (I18N[lang] && I18N[lang]["cat_" + catKey]) || catKey;
    lightbox.hidden = false;
    document.body.style.overflow = "hidden";
  }
  function closeLightbox() {
    if (!lightbox) return;
    lightbox.hidden = true;
    document.body.style.overflow = "";
  }

  if (lightbox) {
    buildLightboxList();
    document.addEventListener("click", (e) => {
      const trigger = e.target.closest("[data-lightbox]");
      if (trigger) {
        e.preventDefault();
        buildLightboxList();
        openLightbox(lbItems.indexOf(trigger));
      }
    });
    document.getElementById("lightboxClose").addEventListener("click", closeLightbox);
    document.getElementById("lightboxNext").addEventListener("click", () => openLightbox(lbIndex + 1));
    document.getElementById("lightboxPrev").addEventListener("click", () => openLightbox(lbIndex - 1));
    lightbox.addEventListener("click", (e) => { if (e.target === lightbox) closeLightbox(); });
    document.addEventListener("keydown", (e) => {
      if (lightbox.hidden) return;
      if (e.key === "Escape") closeLightbox();
      if (e.key === "ArrowRight") openLightbox(lbIndex + 1);
      if (e.key === "ArrowLeft") openLightbox(lbIndex - 1);
    });
  }

  /* ---------------- contact wizard ---------------- */
  const wizard = document.getElementById("wizardForm");
  if (wizard) {
    let step = 1;
    const panes = wizard.querySelectorAll(".wizard-pane");
    const indicators = document.querySelectorAll(".wizard-step");
    const labels = {
      sketch: "q_sketch", placement: "q_placement", size: "q_size",
      name: "form_name", contact_handle: "q_contact_handle",
      contact_method: "q_contact_method", date: "form_date",
    };

    const show = (n) => {
      step = Math.max(1, Math.min(3, n));
      panes.forEach((p) => p.classList.toggle("active", +p.dataset.step === step));
      indicators.forEach((ind) => {
        const s = +ind.dataset.stepIndicator;
        ind.classList.toggle("active", s === step);
        ind.classList.toggle("done", s < step);
      });
      if (step === 3) buildSummary();
    };

    const tr = (key) => (I18N[lang] && I18N[lang][key]) || key;

    const buildSummary = () => {
      const list = document.getElementById("summaryList");
      const fd = new FormData(wizard);
      list.innerHTML = "";
      Object.keys(labels).forEach((field) => {
        let val = fd.get(field);
        if (!val) return;
        // translate option values where applicable
        const optMap = {
          have_sketch: "opt_have_sketch", have_idea: "opt_have_idea", need_consult: "opt_need_consult",
          hand: "place_hand", leg: "place_leg", neck: "place_neck", back: "place_back",
          chest: "place_chest", other: "place_other",
          s: "size_s", m: "size_m", l: "size_l",
          whatsapp: "method_whatsapp", telegram: "method_telegram",
          instagram: "method_instagram", phone: "method_phone",
        };
        if (optMap[val]) val = tr(optMap[val]);
        const li = document.createElement("li");
        li.innerHTML = "<span>" + tr(labels[field]) + "</span><span>" + val + "</span>";
        list.appendChild(li);
      });
    };

    wizard.querySelectorAll("[data-next]").forEach((b) =>
      b.addEventListener("click", () => show(step + 1)));
    wizard.querySelectorAll("[data-back]").forEach((b) =>
      b.addEventListener("click", () => show(step - 1)));

    wizard.addEventListener("submit", async (e) => {
      e.preventDefault();
      const fd = Object.fromEntries(new FormData(wizard).entries());
      fd.source = "contact_wizard";
      await postBooking(fd);
      const ok = document.getElementById("wizardSuccess");
      if (ok) ok.hidden = false;
      wizard.querySelectorAll("input,textarea,button").forEach((i) => (i.disabled = true));
    });

    show(1);
  }

  /* ---------------- cookie banner ---------------- */
  const cookieBanner = document.getElementById("cookieBanner");
  if (cookieBanner) {
    let consent = null;
    try { consent = localStorage.getItem("mt_cookie"); } catch (e) {}
    if (!consent) cookieBanner.hidden = false;
    const close = (v) => {
      try { localStorage.setItem("mt_cookie", v); } catch (e) {}
      cookieBanner.hidden = true;
    };
    document.getElementById("cookieAccept").addEventListener("click", () => close("accepted"));
    document.getElementById("cookieDecline").addEventListener("click", () => close("declined"));
  }
})();
