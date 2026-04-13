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

<style>
.page__hero--overlay {
  padding: 6em 0;
}
.page__lead {
  font-size: 1.2em;
  line-height: 1.6;
}
</style>

<div style="margin:2rem 0;padding:1.5rem;border:1px solid #e1e4e8;border-radius:8px;background:linear-gradient(135deg,#fafbfc,#f0f2f5)">
<h3 style="margin:0 0 1rem;font-size:1.05rem;color:#24292f">📖 Research Impact</h3>
<div style="display:flex;gap:1rem;margin-bottom:1rem">
<a href="https://scholar.google.com/citations?user=M8TAlNwAAAAJ&hl=en" target="_blank" style="flex:1;text-align:center;padding:1rem;background:#fff;border:1px solid #e1e4e8;border-radius:6px;text-decoration:none">
<span style="font-size:1.75rem;font-weight:700;color:#1a73e8;display:block">{{ site.data.scholar.stats.total_citations }}</span>
<span style="font-size:.75rem;font-weight:500;color:#57606a;text-transform:uppercase;letter-spacing:.06em">Citations</span>
</a>
<a href="https://scholar.google.com/citations?user=M8TAlNwAAAAJ&hl=en" target="_blank" style="flex:1;text-align:center;padding:1rem;background:#fff;border:1px solid #e1e4e8;border-radius:6px;text-decoration:none">
<span style="font-size:1.75rem;font-weight:700;color:#1a73e8;display:block">{{ site.data.scholar.stats.h_index }}</span>
<span style="font-size:.75rem;font-weight:500;color:#57606a;text-transform:uppercase;letter-spacing:.06em">h-index</span>
</a>
</div>
{% for pub in site.data.scholar.publications limit:3 %}
<div style="padding:.5rem 0;border-top:1px solid #eef0f3">
<a href="{{ pub.url }}" target="_blank" style="font-size:.9rem;font-weight:500;color:#1a73e8;text-decoration:none">{{ pub.title }}</a>
<div style="font-size:.78rem;color:#656d76">{{ pub.authors }} · <em>{{ pub.venue }}</em>{% if pub.citations > 0 %} · Cited {{ pub.citations }}×{% endif %}</div>
</div>
{% endfor %}
<p style="margin:.75rem 0 0;font-size:.8rem;color:#656d76;border-top:1px solid #e1e4e8;padding-top:.75rem">
<a href="{{ site.data.scholar.profile_url }}" target="_blank" style="color:#1a73e8;text-decoration:none;font-weight:500">View full profile on Google Scholar →</a><br>
<small style="color:#8b949e">Auto-updated · Last sync: {{ site.data.scholar.last_updated_human }}</small>
</p>
</div>

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
