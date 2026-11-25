(function () {
  'use strict';

  var overlay;
  var imgEl;
  var captionEl;
  var counterEl;
  var closeBtn;
  var prevBtn;
  var nextBtn;
  var items = [];
  var current = 0;
  var lastFocus = null;
  var isOpen = false;
  var loadGen = 0;
  var scrollY = 0;
  var touchStartX = 0;
  var touchStartY = 0;
  var swiped = false;

  function svgIcon(path) {
    return '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">' + path + '</svg>';
  }

  function buildUI() {
    if (overlay) return;

    overlay = document.createElement('div');
    overlay.className = 'site-lightbox';
    overlay.setAttribute('role', 'dialog');
    overlay.setAttribute('aria-modal', 'true');
    overlay.setAttribute('aria-label', 'Photo viewer');
    overlay.hidden = true;
    overlay.innerHTML =
      '<div class="site-lightbox__backdrop" data-lightbox-close="true"></div>' +
      '<button type="button" class="site-lightbox__close" aria-label="Close photos">' +
        svgIcon('<path d="M6 6l12 12M18 6L6 18"/>') +
      '</button>' +
      '<button type="button" class="site-lightbox__nav site-lightbox__nav--prev" aria-label="Previous photo">' +
        svgIcon('<path d="M15 5l-7 7 7 7"/>') +
      '</button>' +
      '<button type="button" class="site-lightbox__nav site-lightbox__nav--next" aria-label="Next photo">' +
        svgIcon('<path d="M9 5l7 7-7 7"/>') +
      '</button>' +
      '<div class="site-lightbox__stage">' +
        '<img class="site-lightbox__img" alt="" decoding="async">' +
        '<div class="site-lightbox__meta">' +
          '<p class="site-lightbox__caption"></p>' +
          '<p class="site-lightbox__counter" aria-live="polite"></p>' +
        '</div>' +
      '</div>';

    document.body.appendChild(overlay);

    imgEl = overlay.querySelector('.site-lightbox__img');
    captionEl = overlay.querySelector('.site-lightbox__caption');
    counterEl = overlay.querySelector('.site-lightbox__counter');
    closeBtn = overlay.querySelector('.site-lightbox__close');
    prevBtn = overlay.querySelector('.site-lightbox__nav--prev');
    nextBtn = overlay.querySelector('.site-lightbox__nav--next');

    closeBtn.addEventListener('click', closeLightbox);
    prevBtn.addEventListener('click', showPrev);
    nextBtn.addEventListener('click', showNext);

    overlay.addEventListener('click', function (e) {
      if (e.target && e.target.getAttribute('data-lightbox-close') === 'true') {
        closeLightbox();
      }
    });

    overlay.addEventListener('touchstart', onTouchStart, { passive: true });
    overlay.addEventListener('touchend', onTouchEnd, { passive: true });

    overlay.addEventListener('keydown', onTrapTab);
  }

  function collect(gallery) {
    return Array.prototype.slice.call(gallery.querySelectorAll('a[href]')).map(function (anchor) {
      var img = anchor.querySelector('img');
      return {
        trigger: anchor,
        src: anchor.getAttribute('href'),
        alt: (img && img.getAttribute('alt')) || ''
      };
    }).filter(function (item) {
      return !!item.src;
    });
  }

  function preload(src) {
    if (!src) return;
    var image = new Image();
    image.decoding = 'async';
    image.src = src;
  }

  function preloadNeighbors() {
    if (!items.length) return;
    var prev = items[(current - 1 + items.length) % items.length];
    var next = items[(current + 1) % items.length];
    preload(prev.src);
    if (next.src !== prev.src) preload(next.src);
  }

  function show(index) {
    if (!items.length) return;
    current = (index + items.length) % items.length;
    var item = items[current];
    var gen = ++loadGen;
    var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    imgEl.style.opacity = reduced ? '1' : '0';
    imgEl.alt = item.alt;
    captionEl.textContent = item.alt;
    counterEl.textContent = (current + 1) + ' / ' + items.length;
    overlay.setAttribute('aria-label', 'Photo viewer, ' + (current + 1) + ' of ' + items.length);

    function reveal() {
      if (gen !== loadGen) return;
      imgEl.style.opacity = '1';
    }

    imgEl.onload = reveal;
    imgEl.onerror = reveal;

    if (imgEl.getAttribute('src') === item.src && imgEl.complete) {
      reveal();
    } else {
      imgEl.src = item.src;
    }

    preloadNeighbors();
  }

  function lockScroll() {
    scrollY = window.scrollY || window.pageYOffset || 0;
    document.body.style.overflow = 'hidden';
    document.documentElement.style.overflow = 'hidden';
    document.body.style.position = 'fixed';
    document.body.style.top = '-' + scrollY + 'px';
    document.body.style.left = '0';
    document.body.style.right = '0';
    document.body.style.width = '100%';
  }

  function unlockScroll() {
    document.body.style.overflow = '';
    document.documentElement.style.overflow = '';
    document.body.style.position = '';
    document.body.style.top = '';
    document.body.style.left = '';
    document.body.style.right = '';
    document.body.style.width = '';
    window.scrollTo(0, scrollY);
  }

  function openLightbox(list, index, trigger) {
    items = list;
    if (!items.length) return;
    lastFocus = trigger || document.activeElement;
    buildUI();
    overlay.hidden = false;
    isOpen = true;
    lockScroll();
    show(index);
    closeBtn.focus();
  }

  function closeLightbox() {
    if (!isOpen) return;
    isOpen = false;
    loadGen += 1;
    overlay.hidden = true;
    if (imgEl) {
      imgEl.removeAttribute('src');
      imgEl.alt = '';
    }
    unlockScroll();
    if (lastFocus && typeof lastFocus.focus === 'function') {
      lastFocus.focus();
    }
    lastFocus = null;
  }

  function showPrev() {
    if (!isOpen) return;
    show(current - 1);
  }

  function showNext() {
    if (!isOpen) return;
    show(current + 1);
  }

  function onTouchStart(e) {
    if (!e.touches || !e.touches.length) return;
    touchStartX = e.touches[0].clientX;
    touchStartY = e.touches[0].clientY;
    swiped = false;
  }

  function onTouchEnd(e) {
    if (!isOpen || !e.changedTouches || !e.changedTouches.length) return;
    var dx = e.changedTouches[0].clientX - touchStartX;
    var dy = e.changedTouches[0].clientY - touchStartY;
    if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy)) {
      swiped = true;
      if (dx < 0) showNext();
      else showPrev();
    }
  }

  function focusables() {
    return [closeBtn, prevBtn, nextBtn].filter(function (el) {
      return el && !el.disabled;
    });
  }

  function onTrapTab(e) {
    if (!isOpen || e.key !== 'Tab') return;
    var list = focusables();
    if (!list.length) return;
    var first = list[0];
    var last = list[list.length - 1];
    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      first.focus();
    }
  }

  function onKeydown(e) {
    if (!isOpen) return;
    if (e.key === 'Escape') {
      e.preventDefault();
      closeLightbox();
    } else if (e.key === 'ArrowLeft') {
      e.preventDefault();
      showPrev();
    } else if (e.key === 'ArrowRight') {
      e.preventDefault();
      showNext();
    }
  }

  function onGalleryClick(e) {
    var gallery = e.currentTarget;
    var anchor = e.target.closest('a[href]');
    if (!anchor || !gallery.contains(anchor)) return;
    if (swiped) {
      e.preventDefault();
      return;
    }
    var list = collect(gallery);
    var index = -1;
    for (var i = 0; i < list.length; i++) {
      if (list[i].trigger === anchor) {
        index = i;
        break;
      }
    }
    if (index < 0) return;
    e.preventDefault();
    openLightbox(list, index, anchor);
  }

  function init() {
    var galleries = document.querySelectorAll('[data-lightbox]');
    if (!galleries.length) return;
    buildUI();
    Array.prototype.forEach.call(galleries, function (gallery) {
      gallery.addEventListener('click', onGalleryClick);
    });
    document.addEventListener('keydown', onKeydown);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
