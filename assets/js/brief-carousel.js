(() => {
  const region = document.querySelector('.kh-news-carousel');
  if (!region) return;
  const track = region.querySelector('.kh-news-track'), status = region.querySelector('.kh-carousel-status'), pause = region.querySelector('[data-carousel="pause"]');
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  let playing = !motion.matches, hovering = false, visible = false;
  const safeURL = value => {
    try { const url = new URL(value); return url.protocol === 'https:' && url.hostname === 'brief.hamelberg-ai.com' ? url.href : null; } catch { return null; }
  };
  function update() {
    const width = track.firstElementChild?.getBoundingClientRect().width || 1;
    status.textContent = `Story ${Math.round(track.scrollLeft / (width + 22)) + 1} of ${track.children.length}`;
    pause.textContent = playing ? 'Pause' : 'Play';
    pause.setAttribute('aria-label', `${playing ? 'Pause' : 'Start'} automatic story rotation`);
  }
  function advance(direction) {
    const step = (track.firstElementChild?.getBoundingClientRect().width || track.clientWidth) + 22, end = track.scrollWidth - track.clientWidth;
    let left = track.scrollLeft + direction * step;
    if (direction > 0 && track.scrollLeft >= end - 4) left = 0;
    else if (left < -4) left = end;
    track.scrollTo({left, behavior: motion.matches ? 'instant' : 'smooth'});
  }
  region.querySelector('[data-carousel="previous"]').addEventListener('click', () => advance(-1));
  region.querySelector('[data-carousel="next"]').addEventListener('click', () => advance(1));
  pause.addEventListener('click', () => { playing = !playing; update(); });
  region.addEventListener('mouseenter', () => { hovering = true; });
  region.addEventListener('mouseleave', () => { hovering = false; });
  track.addEventListener('scroll', update, {passive:true});
  track.addEventListener('keydown', event => { if (event.target !== track || !['ArrowLeft','ArrowRight'].includes(event.key)) return; event.preventDefault(); advance(event.key === 'ArrowLeft' ? -1 : 1); });
  motion.addEventListener('change', () => { if (motion.matches) playing = false; update(); });
  new IntersectionObserver(([entry]) => { visible = entry.isIntersecting; }, {threshold:.25}).observe(region);
  const timer = setInterval(() => { if (playing && visible && !document.hidden && !hovering && !region.contains(document.activeElement)) advance(1); }, 7000);
  window.addEventListener('pagehide', () => clearInterval(timer), {once:true});
  update();
  const element = (tag, className, text) => { const el = document.createElement(tag); if (className) el.className = className; if (text) el.textContent = text; return el; };
  async function load() {
    try {
      const response = await fetch('https://brief.hamelberg-ai.com/data/spotlight.json', {credentials:'omit', signal:AbortSignal.timeout(7000)});
      if (!response.ok) return;
      const data = await response.json(); if (data.version !== 1 || !Array.isArray(data.items)) return;
      const cards = [];
      for (const item of data.items.slice(0,8)) {
        const url = safeURL(item.url), image = safeURL(item.image);
        if (!url || !image || typeof item.headline !== 'string') continue;
        const article = element('article','kh-news-card'), picture = element('a','kh-news-image'); picture.href = url; picture.tabIndex = -1; picture.setAttribute('aria-hidden','true');
        const img = element('img'); img.src = image; img.alt = item.image_alt || ''; img.width = 600; img.height = 400; img.loading = 'lazy'; img.title = item.image_credit ? `Photograph: ${item.image_credit}. Geographic illustration.` : ''; picture.append(img);
        const copy = element('div','kh-news-copy'); copy.append(element('p','kh-news-market', `${item.market || 'World'} · AI news`));
        const heading = element('h3'), link = element('a','',item.headline); link.href = url; heading.append(link); copy.append(heading);
        copy.append(element('p','kh-news-summary',typeof item.summary === 'string' ? item.summary : ''));
        const read = element('a','kh-news-read','Read the story ↗'); read.href = url; copy.append(read); article.append(picture,copy); cards.push(article);
      }
      if (cards.length >= 3 && !region.contains(document.activeElement)) { track.replaceChildren(...cards); track.scrollLeft = 0; update(); }
    } catch { /* Keep the original linked stories if the live feed is unavailable. */ }
  }
  load();
})();
