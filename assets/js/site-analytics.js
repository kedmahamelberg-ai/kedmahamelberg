(() => {
  'use strict';
  if (window.KHAnalytics) return;
  const id = document.currentScript?.dataset.measurementId || '';
  if (!/^G-[A-Z0-9]+$/.test(id) || !/^https?:$/.test(location.protocol)) return;
  const key = 'kh-analytics-consent-v1';
  let choice = 'allow', loaded = false;
  try {
    const saved = JSON.parse(localStorage.getItem(key));
    if (saved?.choice === 'deny') choice = 'deny';
  } catch {}
  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
  window.gtag('consent', 'default', {
    analytics_storage: choice === 'allow' ? 'granted' : 'denied', ad_storage: 'denied',
    ad_user_data: 'denied', ad_personalization: 'denied'
  });
  const cleanUrl = value => {
    try { const url = new URL(value); return /^https?:$/.test(url.protocol) ? url.origin + url.pathname : ''; }
    catch { return ''; }
  };
  function event(name, properties = {}) {
    if (choice !== 'allow' || !loaded) return;
    window.gtag('event', name, {
      ...properties, page_location: location.origin + location.pathname,
      page_title: document.title, page_referrer: cleanUrl(document.referrer)
    });
  }
  function load() {
    if (choice !== 'allow' || loaded) return;
    loaded = true;
    window['ga-disable-' + id] = false;
    window.gtag('consent', 'update', {analytics_storage: 'granted'});
    window.gtag('js', new Date());
    window.gtag('config', id, {
      send_page_view: false, allow_google_signals: false,
      allow_ad_personalization_signals: false,
      page_location: location.origin + location.pathname,
      page_referrer: cleanUrl(document.referrer)
    });
    const script = document.createElement('script');
    script.async = true;
    script.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(id);
    document.head.appendChild(script);
    event('page_view');
  }
  function clearCookies() {
    const names = document.cookie.split(';').map(c => c.trim().split('=')[0])
      .filter(n => /^_ga(?:_|$)|^_gid$|^_gat/.test(n));
    for (const name of names) {
      document.cookie = name + '=;Max-Age=0;path=/;SameSite=Lax';
      const domain = location.hostname.split('.');
      while (domain.length > 1) {
        document.cookie = name + '=;Max-Age=0;path=/;domain=.' + domain.join('.') + ';SameSite=Lax';
        domain.shift();
      }
    }
  }
  function choose(value) {
    choice = value === 'allow' ? 'allow' : 'deny';
    try { localStorage.setItem(key, JSON.stringify({choice, at: Date.now()})); } catch {}
    if (choice === 'allow') load();
    else {
      window['ga-disable-' + id] = true;
      clearCookies();
      if (loaded) location.reload();
    }
  }
  document.addEventListener('click', e => {
    const button = e.target.closest('[data-kh-choice]');
    if (button) { choose(button.dataset.khChoice); return; }
    const link = e.target.closest('a[href]');
    if (!link || choice !== 'allow') return;
    const raw = link.getAttribute('href');
    if (raw.startsWith('mailto:')) { event('contact_click'); return; }
    try {
      const url = new URL(raw, location.href);
      if (!/^https?:$/.test(url.protocol)) return;
      if (/\.(pdf|docx?)$/i.test(url.pathname)) {
        event('file_download', {file_name: url.pathname.split('/').pop(), link_domain: url.hostname});
      } else if (url.hostname !== location.hostname) {
        event('outbound_click', {link_domain: url.hostname, link_path: url.pathname});
      }
    } catch {}
  });
  window.KHAnalytics = {choose};
  load();
})();
