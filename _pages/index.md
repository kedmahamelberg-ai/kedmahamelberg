---
layout: single
title: "Welcome"
permalink: /
author_profile: true
header:
  overlay_image: "/assets/images/KedmaHamelberg1092-a.jpg"
  overlay_filter: 0.5
  actions:
    - label: "Get in touch"
      url: "mailto:kedma@hamelberg-ai.com"
---
<div id="scholar-widget"></div>
<script>
fetch('/scholar-data.json')
  .then(r => r.json())
  .then(d => {
    document.getElementById('scholar-widget').innerHTML = `
    <div style="display:inline-flex;gap:1.5rem;align-items:center;padding:.6rem 1rem;border:1px solid #e1e4e8;border-radius:6px;background:#f6f8fa;margin-bottom:1.5rem">
      <a href="${d.profile_url}" target="_blank" style="text-decoration:none;display:flex;align-items:center;gap:.4rem">
        <span style="font-size:1.3rem;font-weight:700;color:#1a73e8">${d.stats.total_citations}</span>
        <span style="font-size:.7rem;font-weight:500;color:#57606a;text-transform:uppercase;letter-spacing:.05em">citations</span>
      </a>
      <span style="color:#d0d7de">|</span>
      <a href="${d.profile_url}" target="_blank" style="text-decoration:none;display:flex;align-items:center;gap:.4rem">
        <span style="font-size:1.3rem;font-weight:700;color:#1a73e8">${d.stats.h_index}</span>
        <span style="font-size:.7rem;font-weight:500;color:#57606a;text-transform:uppercase;letter-spacing:.05em">h-index</span>
      </a>
      <span style="color:#d0d7de">|</span>
      <a href="${d.profile_url}" target="_blank" style="font-size:.75rem;color:#1a73e8;text-decoration:none;font-weight:500">Google Scholar →</a>
    </div>`;
  });
</script>


I build **AI systems** that decode how organisations and consumers communicate in digital environments. My work combines **machine learning, natural language processing, prediction and causal inference** to analyse large-scale data, from 13+ million social media posts to thousands of news articles, and turn it into actionable insight.

My research focuses on corporate and brand communication during critical societal moments: CEO messaging during geopolitical crisis, consumer responses to AI, and how digital platforms shape public narratives around sustainability and inclusion. Published in the Journal of Public Policy & Marketing and presented at EMAC and AMS, my work bridges computational social science with marketing strategy and organisational decision-making.

I also design AI education for professionals. My Applied AI for Marketing course at the University of Amsterdam (rated 4.9/5.0) equips executives and graduate students with **hands-on skills in Python, LLMs, and responsible AI deployment, grounded in the EU AI Act.**

Open to research collaborations, applied AI partnerships, and opportunities where rigorous analysis meets real-world impact.


---


  📬 [Get in touch](mailto:kedma@hamelberg-ai.com)

---

### 🔍 Explore

- 👉 [Research](/research/)
- 👉 [Teaching](/teaching/)
- 👉 [Download CV](/cv/)
