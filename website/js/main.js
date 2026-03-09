/* CTF Zero to Hero — main.js
   Three features: mobile nav, copy buttons, active nav
*/

(function () {
  'use strict';

  /* ── 1. ACTIVE NAV LINK ─────────────────────────────────────── */
  function setActiveNav() {
    var filename = window.location.pathname.split('/').pop() || 'index.html';
    var links = document.querySelectorAll('.nav-links a');
    links.forEach(function (link) {
      var href = link.getAttribute('href');
      if (!href) return;
      var linkFile = href.split('/').pop();
      if (linkFile === filename) {
        link.classList.add('active');
      }
    });
  }

  /* ── 2. MOBILE NAV TOGGLE ───────────────────────────────────── */
  function initMobileNav() {
    var navbar = document.querySelector('.navbar');
    var hamburger = document.querySelector('.hamburger');
    if (!navbar || !hamburger) return;

    hamburger.setAttribute('aria-label', 'Toggle navigation');
    hamburger.setAttribute('aria-expanded', 'false');

    function openNav() {
      navbar.classList.add('nav-open');
      hamburger.setAttribute('aria-expanded', 'true');
    }

    function closeNav() {
      navbar.classList.remove('nav-open');
      hamburger.setAttribute('aria-expanded', 'false');
    }

    hamburger.addEventListener('click', function () {
      if (navbar.classList.contains('nav-open')) {
        closeNav();
      } else {
        openNav();
      }
    });

    // Close on outside click
    document.addEventListener('click', function (e) {
      if (navbar.classList.contains('nav-open') && !navbar.contains(e.target)) {
        closeNav();
      }
    });

    // Close on Escape
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && navbar.classList.contains('nav-open')) {
        closeNav();
        hamburger.focus();
      }
    });

    // Close when a nav link is clicked (mobile)
    var navLinks = navbar.querySelectorAll('.nav-links a');
    navLinks.forEach(function (link) {
      link.addEventListener('click', function () {
        closeNav();
      });
    });
  }

  /* ── 3. COPY BUTTONS FOR CODE BLOCKS ────────────────────────── */
  function initCopyButtons() {
    var codeBlocks = document.querySelectorAll('.code-block');
    codeBlocks.forEach(function (block) {
      var btn = block.querySelector('.copy-btn');
      var pre = block.querySelector('pre');
      if (!btn || !pre) return;

      btn.addEventListener('click', function () {
        var text = pre.textContent || '';
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(text).then(function () {
            showCopied(btn);
          }).catch(function () {
            fallbackCopy(text, btn);
          });
        } else {
          fallbackCopy(text, btn);
        }
      });
    });
  }

  function showCopied(btn) {
    var original = btn.textContent;
    btn.textContent = 'Copied!';
    btn.classList.add('copied');
    setTimeout(function () {
      btn.textContent = original;
      btn.classList.remove('copied');
    }, 2000);
  }

  function fallbackCopy(text, btn) {
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.focus();
    ta.select();
    try {
      document.execCommand('copy');
      showCopied(btn);
    } catch (e) {
      // silently fail
    }
    document.body.removeChild(ta);
  }

  /* ── INIT ───────────────────────────────────────────────────── */
  document.addEventListener('DOMContentLoaded', function () {
    setActiveNav();
    initMobileNav();
    initCopyButtons();
  });
}());
