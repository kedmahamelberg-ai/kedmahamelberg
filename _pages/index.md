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


I develop **responsible AI systems** that predict how consumers respond to marketing in digital environments—analyzing 13+ million social media posts to understand what drives engagement, emotion, and action.

My research combines **machine learning, natural language processing, and causal inference** to decode brand communication during critical moments: from CEO messaging during war to consumer behavior towards AI. Published in the *Journal of Public Policy & Marketing* and presented at EMAC and AMS, my work bridges computational social science and marketing strategy.

I translate these insights into the classroom, teaching **Applied AI for Marketing** and **Digital Marketing Analytics** to MSc students (rated 4.9/5.0). My courses equip future marketers with hands-on skills in Python, machine learning, and AI-powered consumer analytics.

**Currently seeking tenure-track positions in digital marketing & AI**.
Open to research collaborations and AI education partnerships.


---


  📬 [Get in touch](mailto:kedma@hamelberg-ai.com)

---

### 🔍 Explore

- 👉 [Research](/research/)
- 👉 [Teaching](/teaching/)
- 👉 [Download CV](/cv/)
