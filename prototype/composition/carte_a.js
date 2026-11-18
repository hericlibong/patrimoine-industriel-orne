// Carte A′ « Gravure affinée », fond topographique — module commun aux deux
// expérimentations de composition (phase 10.E). Reprend tel quel le dessin retenu le
// 18 novembre 2026 dans prototype/recherche/carte.html : relief, forêts publiques,
// rivières par ordre, villes ; ensembles en cercles numérotés ; lieux hors ensemble en
// carrés bleu d'encre détourés un à un. S'y ajoutent les filtres et la descente dans
// les deux ensembles construits (Risle, Crulai), repris de l'esquisse D.
/* global d3 */
(function () {
  const C = window.CARTE, D = window.DONNEES, DEP = D.departement;
  const PAP = '#fbfaf6', ENCRE = '#1e3040', NOM_PILOTE = '#16242f', NOM = '#22323f';
  const T = {
    fond: '#e9ece6', hors: 'rgba(233,236,230,.72)',
    hypso: [[60, '#dfe6d8'], [150, '#e9e8d6'], [250, '#e4dcc6'], [420, '#d6c9ae']], ombre: 0.62,
    eau: '#3e7896', eauHalo: 'rgba(233,236,230,.9)',
    foret: 'rgba(122,150,112,.42)', foretTrait: 'rgba(84,112,76,.55)',
    contour: '#2a3640', contourL: 1.3,
    ville: '#22303a', villeTxt: '#22303a', halo: 'rgba(240,242,237,.9)', foretTxt: '#4f6a46', riviereTxt: '#2f6582'
  };
  const SERIF = "'Source Serif 4', Georgia, serif", SANS = "'Source Sans 3', system-ui, sans-serif";
  const DETAIL = D.ensembles; // les deux ensembles construits
  const ENS = DEP.ensembles;

  // tous les lieux : hors ensemble (toujours sur la carte) et lieux des ensembles construits
  const LIEUX = [];
  for (const s of DEP.autresLieux) LIEUX.push(Object.assign({}, s, DEP.complements[s.ref] || {}, { _ens: null }));
  for (const [code, e] of Object.entries(DETAIL)) for (const s of e.sites) if (s.lon != null) LIEUX.push(Object.assign({}, s, { _ens: code }));
  LIEUX.sort((a, b) => b.lat - a.lat); // du nord au sud : ordre de détourage
  const parRef = new Map(LIEUX.map((s) => [s.ref, s]));

  // projection équirectangulaire corrigée, identique à la carte seule
  const anneau = C.contour[0];
  const lon0 = d3.mean(anneau, (p) => p[0]), lat0 = d3.mean(anneau, (p) => p[1]);
  const kx = Math.cos(lat0 * Math.PI / 180);
  const px = (lon) => (lon - lon0) * kx, py = (lat) => -(lat - lat0);
  const R = C.relief;
  const zAt = (i, j) => R.z[Math.max(0, Math.min(R.ny - 1, j)) * R.nx + Math.max(0, Math.min(R.nx - 1, i))];
  const parOrdre = d3.sort(d3.groups(C.rivieres, (r) => r.ordre), (g) => g[0]);
  const rivieresNommees = [...d3.group(C.rivieres.filter((r) => r.ordre >= 5 && r.nom), (r) => r.nom)]
    .map(([nom, rs]) => [nom, d3.greatest(rs, (r) => r.pts.length)]).filter(([, r]) => r.pts.length >= 6);

  let imageRelief = null;
  function relief() {
    if (imageRelief) return imageRelief;
    const o = document.createElement('canvas'); o.width = R.nx; o.height = R.ny;
    const g = o.getContext('2d'), im = g.createImageData(R.nx, R.ny);
    const dxm = R.pas * 111320 * kx, dym = R.pas * 110570, ex = 4;
    const sources = [[315, 0.6], [270, 0.2], [0, 0.2]];
    const teinte = d3.scaleLinear().domain(T.hypso.map((h) => h[0])).range(T.hypso.map((h) => h[1])).clamp(true);
    for (let j = 0; j < R.ny; j++) for (let i = 0; i < R.nx; i++) {
      const dzdx = ex * (zAt(i + 1, j) - zAt(i - 1, j)) / (2 * dxm), dzdy = ex * (zAt(i, j - 1) - zAt(i, j + 1)) / (2 * dym);
      const pente = Math.atan(Math.hypot(dzdx, dzdy)), asp = Math.atan2(dzdy, -dzdx);
      let l = 0;
      for (const [az, w] of sources) {
        const a = (360 - az + 90) * Math.PI / 180, h = Math.PI / 4;
        l += w * Math.max(0, Math.sin(h) * Math.cos(pente) + Math.cos(h) * Math.sin(pente) * Math.cos(a - asp));
      }
      const k = (j * R.nx + i) * 4, c = d3.rgb(teinte(zAt(i, j))), f = 1 - T.ombre * (1 - l / Math.sin(Math.PI / 4));
      im.data[k] = c.r * f; im.data[k + 1] = c.g * f; im.data[k + 2] = c.b * f; im.data[k + 3] = 255;
    }
    g.putImageData(im, 0, 0);
    return (imageRelief = o);
  }

  function CarteA(conteneur, opts = {}) {
    const cv = document.createElement('canvas');
    cv.setAttribute('aria-hidden', 'true');
    cv.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;display:block;cursor:grab;touch-action:none';
    conteneur.appendChild(cv);
    const ctx = cv.getContext('2d');
    const cache = document.createElement('canvas'), cctx = cache.getContext('2d');
    let W = 0, H = 0, dpr = 1, base = null, transform = d3.zoomIdentity, cleCache = '';
    let marges = Object.assign({ g: 60, d: 60, h: 60, b: 60 }, opts.marges || {});
    const filtre = { metier: null, epoque: null };
    let vue = 'orne', choisi = null, cibleSurvol = null;

    const retenu = (s) => (!filtre.metier || (s.secteurs || []).includes(filtre.metier)) && (!filtre.epoque || (s.epoques || []).includes(filtre.epoque));
    const compteEnsemble = (e, m = filtre.metier, ep = filtre.epoque) =>
      m && ep ? e.sitesParMetierEpoque[`${m}|${ep}`] || 0 : m ? e.metiers[m] || 0 : ep ? e.sitesParEpoque[ep] || 0 : e.nbSites;

    // valeurs animées : opacité des lieux, effectif et visibilité des ensembles
    const etatLieu = new Map(LIEUX.map((s) => [s.ref, { a: s._ens ? 0 : 1 }]));
    const etatEns = new Map(ENS.map((e) => [e.code, { n: e.nbSites, v: 1 }]));
    const cibleLieu = (s) => (s._ens && s._ens !== vue ? 0 : retenu(s) ? 1 : 0.14);
    let minuterie = null;
    function animer(duree = 550) {
      const depart = { l: new Map([...etatLieu].map(([k, v]) => [k, v.a])), e: new Map([...etatEns].map(([k, v]) => [k, { ...v }])) };
      const arrivee = { l: new Map(LIEUX.map((s) => [s.ref, cibleLieu(s)])), e: new Map(ENS.map((e) => [e.code, { n: compteEnsemble(e), v: e.code === vue ? 0 : 1 }])) };
      if (minuterie) minuterie.stop();
      const pose = (t) => {
        for (const [k, v] of etatLieu) v.a = depart.l.get(k) + (arrivee.l.get(k) - depart.l.get(k)) * t;
        for (const [k, v] of etatEns) { const a = depart.e.get(k), b = arrivee.e.get(k); v.n = a.n + (b.n - a.n) * t; v.v = a.v + (b.v - a.v) * t; }
        dessiner();
      };
      if (!duree || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return pose(1);
      minuterie = d3.timer((ecoule) => { const t = Math.min(1, ecoule / duree); pose(d3.easeCubicInOut(t)); if (t === 1) minuterie.stop(); });
    }

    function cadrer() {
      const xs = anneau.map((p) => px(p[0])), ys = anneau.map((p) => py(p[1]));
      const [x0, x1] = d3.extent(xs), [y0, y1] = d3.extent(ys);
      const lw = W - marges.g - marges.d, lh = H - marges.h - marges.b;
      const s = Math.min(lw / (x1 - x0), lh / (y1 - y0));
      base = { s, tx: marges.g + lw / 2 - s * (x0 + x1) / 2, ty: marges.h + lh / 2 - s * (y0 + y1) / 2 };
    }
    const bx = (lon) => base.tx + base.s * px(lon), by = (lat) => base.ty + base.s * py(lat);
    const X = (lon) => transform.applyX(bx(lon)), Y = (lat) => transform.applyY(by(lat));
    const chemin = (g, pts, ferme) => { g.moveTo(X(pts[0][0]), Y(pts[0][1])); for (let k = 1; k < pts.length; k++) g.lineTo(X(pts[k][0]), Y(pts[k][1])); if (ferme) g.closePath(); };
    function texte(t, x, y, police, coul, halo, aligne = 'left') {
      ctx.font = police; ctx.textAlign = aligne; ctx.textBaseline = 'middle';
      if (halo) { ctx.lineWidth = 3.5; ctx.strokeStyle = halo; ctx.lineJoin = 'round'; ctx.strokeText(t, x, y); }
      ctx.fillStyle = coul; ctx.fillText(t, x, y);
    }
    function boite(x, y, w, h, prises) {
      for (const b of prises) if (x < b[2] && x + w > b[0] && y < b[3] && y + h > b[1]) return false;
      prises.push([x, y, x + w, y + h]); return true;
    }

    // fond sans étiquettes, mis en cache tant que le cadrage ne bouge pas
    function fond() {
      const cle = `${W}|${H}|${transform.k}|${transform.x}|${transform.y}`;
      if (cle === cleCache) return;
      cleCache = cle;
      const g = cctx, k = transform.k;
      g.setTransform(dpr, 0, 0, dpr, 0, 0);
      g.fillStyle = T.fond; g.fillRect(0, 0, W, H);
      g.imageSmoothingEnabled = true; g.imageSmoothingQuality = 'high';
      const x0 = X(R.x0 - R.pas / 2), y0 = Y(R.y1 + R.pas / 2), x1 = X(R.x0 + (R.nx - 0.5) * R.pas), y1 = Y(R.y1 - (R.ny - 0.5) * R.pas);
      g.drawImage(relief(), x0, y0, x1 - x0, y1 - y0);
      for (const f of C.forets) {
        g.beginPath(); for (const a of f.anneaux) chemin(g, a, true);
        g.fillStyle = T.foret; g.fill('evenodd'); g.strokeStyle = T.foretTrait; g.lineWidth = 0.6; g.stroke();
      }
      const largeur = (o) => Math.max(0.35, 0.42 * (o - 2.2)) * Math.pow(k, 0.45);
      const ordreMin = k > 2.2 ? 3 : 4;
      g.lineCap = 'round'; g.lineJoin = 'round';
      for (const [o, rs] of parOrdre) {
        if (o < ordreMin) continue;
        g.beginPath(); for (const r of rs) chemin(g, r.pts);
        if (o >= 5) { g.strokeStyle = T.eauHalo; g.lineWidth = largeur(o) + 2.2; g.stroke(); }
        g.strokeStyle = T.eau; g.globalAlpha = o <= 3 ? 0.55 : o === 4 ? 0.8 : 1; g.lineWidth = largeur(o); g.stroke(); g.globalAlpha = 1;
      }
      g.save(); g.beginPath(); g.rect(0, 0, W, H); for (const a of C.contour) chemin(g, a, true);
      g.fillStyle = T.hors; g.fill('evenodd'); g.restore();
      g.beginPath(); for (const a of C.contour) chemin(g, a, true);
      g.strokeStyle = T.contour; g.lineWidth = T.contourL; g.stroke();
    }

    let lieuxEcran = [], ensEcran = [];
    const rEns = (n) => (7 + 3 * Math.sqrt(n)) * Math.pow(transform.k, 0.35);
    function dessiner() {
      if (!base) return;
      fond();
      const k = transform.k;
      ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.drawImage(cache, 0, 0);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      const prises = [];

      // lieux : carré bleu d'encre, détouré un à un du nord au sud
      const ech = Math.min(1.7, Math.pow(k, 0.4)), cote = 3.3 * ech * Math.sqrt(Math.PI);
      lieuxEcran = [];
      ctx.lineJoin = 'miter';
      for (const s of LIEUX) {
        const a = etatLieu.get(s.ref).a;
        if (a < 0.01) continue;
        const x = X(s.lon), y = Y(s.lat);
        if (x < -10 || y < -10 || x > W + 10 || y > H + 10) continue;
        if (a > 0.5) lieuxEcran.push([x, y, s]);
        ctx.globalAlpha = a;
        ctx.beginPath(); ctx.rect(x - cote / 2, y - cote / 2, cote, cote);
        ctx.lineWidth = 2.2; ctx.strokeStyle = PAP; ctx.stroke();
        ctx.fillStyle = ENCRE; ctx.fill();
      }
      ctx.globalAlpha = 1;
      const sel = choisi && parRef.get(choisi);
      if (sel && etatLieu.get(sel.ref).a > 0.5) {
        ctx.beginPath(); ctx.rect(X(sel.lon) - cote / 2 - 4, Y(sel.lat) - cote / 2 - 4, cote + 8, cote + 8);
        ctx.lineWidth = 1.6; ctx.strokeStyle = ENCRE; ctx.stroke();
      }

      // ensembles : cercle à l'effectif filtré ; un filet garde la taille entière
      ensEcran = [];
      const noms = [];
      const ordre = [...ENS].sort((a, b) => !!DETAIL[a.code] - !!DETAIL[b.code]);
      for (const e of ordre) {
        const st = etatEns.get(e.code);
        if (st.v < 0.01) continue;
        const pilote = !!DETAIL[e.code], x = X(e.lon), y = Y(e.lat), r = st.n > 0.05 ? rEns(st.n) : 0, rT = rEns(e.nbSites);
        ctx.globalAlpha = st.v;
        if (st.n < e.nbSites - 0.05) {
          ctx.beginPath(); ctx.arc(x, y, rT, 0, 2 * Math.PI);
          ctx.lineWidth = 1; ctx.strokeStyle = 'rgba(30,48,64,.38)'; ctx.setLineDash([2, 2.5]); ctx.stroke(); ctx.setLineDash([]);
        }
        if (r > 0) {
          ctx.beginPath(); ctx.arc(x, y, r, 0, 2 * Math.PI);
          ctx.lineWidth = pilote ? 3 : 4.5; ctx.strokeStyle = PAP; ctx.stroke();
          ctx.fillStyle = pilote ? ENCRE : PAP; ctx.fill();
          if (!pilote) { ctx.lineWidth = 1.6; ctx.strokeStyle = ENCRE; ctx.stroke(); }
          ctx.fontVariantNumeric = 'lining-nums tabular-nums';
          texte(String(Math.round(st.n)), x, y + 0.5, `600 ${Math.max(11, r * 0.78)}px ${SERIF}`, pilote ? PAP : ENCRE, null, 'center');
        }
        ctx.globalAlpha = 1;
        const rp = Math.max(r, rT * 0.6);
        prises.push([x - rp - 3, y - rp - 3, x + rp + 3, y + rp + 3]);
        ensEcran.push([x, y, Math.max(rp, 10), e]);
        noms.push({ e, x, y, r: Math.max(r, 6), pilote, vide: st.n < 0.5, v: st.v });
      }
      noms.sort((a, b) => b.pilote - a.pilote);
      for (const { e, x, y, r, pilote, vide, v } of noms) {
        const police = `${pilote ? 600 : 400} ${pilote ? 15.5 : 13.5}px ${SERIF}`;
        ctx.font = police; const w = ctx.measureText(e.nom).width, h = 18;
        const essais = [[x + r + 7, y - h / 2], [x - r - 7 - w, y - h / 2], [x - w / 2, y + r + 4], [x - w / 2, y - r - 4 - h]];
        const [bx0, by0] = essais.find(([a, b]) => boite(a, b, w, h, prises)) || essais[0];
        ctx.globalAlpha = v * (vide ? 0.4 : 1);
        texte(e.nom, bx0, by0 + h / 2, police, pilote ? NOM_PILOTE : NOM, T.halo);
        ctx.globalAlpha = 1;
      }

      // étiquettes du fond, après les données pour les éviter
      const sans = SANS, serif = SERIF;
      for (const v of C.villes) {
        const grande = v.prefecture || v.sousPrefecture;
        if (!grande && v.pop < (k > 2 ? 2000 : k > 1.3 ? 3000 : 4500)) continue;
        const x = X(v.lon), y = Y(v.lat), taille = grande ? 15 : 12.5;
        ctx.font = `${grande ? 600 : 400} ${taille}px ${sans}`;
        const w = ctx.measureText(v.nom).width;
        if (!boite(x + 6, y - taille / 2, w + 4, taille, prises)) continue;
        ctx.beginPath(); ctx.rect(x - 2.5, y - 2.5, 5, 5); ctx.fillStyle = T.ville; ctx.fill();
        texte(v.nom, x + 7, y, `${grande ? 600 : 400} ${taille}px ${sans}`, T.villeTxt, T.halo);
      }
      for (const [nom, r] of rivieresNommees) {
        const m = Math.floor(r.pts.length / 2), a = r.pts[Math.max(0, m - 2)], b = r.pts[Math.min(r.pts.length - 1, m + 2)];
        if (!d3.polygonContains(anneau, r.pts[m])) continue;
        const x = X(r.pts[m][0]), y = Y(r.pts[m][1]);
        let ang = Math.atan2(Y(b[1]) - Y(a[1]), X(b[0]) - X(a[0]));
        if (ang > Math.PI / 2) ang -= Math.PI; if (ang < -Math.PI / 2) ang += Math.PI;
        if (!boite(x - 40, y - 8, 80, 16, prises)) continue;
        ctx.save(); ctx.translate(x, y); ctx.rotate(ang);
        texte(nom, 0, -7, `italic 400 12.5px ${serif}`, T.riviereTxt, T.halo, 'center');
        ctx.restore();
      }
      for (const f of C.forets) {
        const a = d3.greatest(f.anneaux, (q) => q.length).map((p) => [X(p[0]), Y(p[1])]);
        if (Math.abs(d3.polygonArea(a)) < 1800) continue;
        const c = d3.polygonCentroid(a);
        const nom = (f.nom || '').replace(/^Forêt (Domaniale|Communale|départementale)? ?(de |d'|des |du )?/i, '');
        const lib = 'forêt ' + (/^[AEIOUÉÈ]/.test(nom) ? "d'" : 'de ') + nom;
        ctx.font = `italic 400 12px ${serif}`;
        const w = ctx.measureText(lib).width;
        if (!boite(c[0] - w / 2, c[1] - 7, w, 14, prises)) continue;
        texte(lib, c[0], c[1], `italic 400 12px ${serif}`, T.foretTxt, T.halo, 'center');
      }
      if (opts.apresDessin) opts.apresDessin();
    }

    // zoom et désignation
    // opts.molette() peut refuser la molette (page qui défile : la carte ne doit pas la capturer)
    const zoom = d3.zoom().scaleExtent([0.8, 24])
      .filter((ev) => (!ev.ctrlKey || ev.type === 'wheel') && !ev.button && (ev.type !== 'wheel' || !opts.molette || opts.molette()))
      .on('zoom', (ev) => { transform = ev.transform; dessiner(); if (opts.surZoom) opts.surZoom(ev); });
    d3.select(cv).call(zoom).on('dblclick.zoom', null);
    function objetSous(mx, my) {
      for (const [x, y, r, e] of ensEcran.slice().reverse()) if ((x - mx) ** 2 + (y - my) ** 2 <= r * r) return { type: 'ensemble', e };
      let best = null, dmin = 81;
      for (const [x, y, s] of lieuxEcran) { const d = (x - mx) ** 2 + (y - my) ** 2; if (d < dmin) { dmin = d; best = s; } }
      return best ? { type: 'lieu', s: best } : null;
    }
    const coords = (ev) => { const r = cv.getBoundingClientRect(); return [ev.clientX - r.left, ev.clientY - r.top]; };
    cv.addEventListener('mousemove', (ev) => {
      const o = objetSous(...coords(ev));
      cv.style.cursor = o ? 'pointer' : 'grab';
      cibleSurvol = o;
      if (opts.survol) opts.survol(o, ev.clientX, ev.clientY);
    });
    cv.addEventListener('mouseleave', () => opts.survol && opts.survol(null));
    cv.addEventListener('click', (ev) => { const o = objetSous(...coords(ev)); if (opts.clic) opts.clic(o); });

    function cadrage(code) {
      if (code === 'orne') return d3.zoomIdentity;
      const pts = DETAIL[code].sites.filter((s) => s.lon != null).map((s) => [bx(s.lon), by(s.lat)]);
      const [x0, x1] = d3.extent(pts, (p) => p[0]), [y0, y1] = d3.extent(pts, (p) => p[1]);
      const lw = W - marges.g - marges.d - 80, lh = H - marges.h - marges.b - 80;
      const k = Math.min(lw / (x1 - x0 || 1), lh / (y1 - y0 || 1), 9);
      return d3.zoomIdentity.translate(marges.g + (W - marges.g - marges.d) / 2 - (x0 + x1) / 2 * k, marges.h + (H - marges.h - marges.b) / 2 - (y0 + y1) / 2 * k).scale(k);
    }
    const lent = () => window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    const api = {
      LIEUX, ENS, DETAIL, parRef, retenu, compteEnsemble,
      filtre: () => ({ ...filtre }),
      vue: () => vue,
      filtrer(f, anime = true) { Object.assign(filtre, f); animer(anime ? 550 : 0); },
      aller(code, anime = true) {
        vue = DETAIL[code] ? code : 'orne';
        animer(anime ? 900 : 0);
        d3.select(cv).transition().duration(anime && !lent() ? 1200 : 0).ease(d3.easeCubicInOut).call(zoom.transform, cadrage(vue));
      },
      voler(lon, lat, k = 4, anime = true) {
        const t = d3.zoomIdentity.translate(marges.g + (W - marges.g - marges.d) / 2 - bx(lon) * k, marges.h + (H - marges.h - marges.b) / 2 - by(lat) * k).scale(k);
        d3.select(cv).transition().duration(anime && !lent() ? 1000 : 0).ease(d3.easeCubicInOut).call(zoom.transform, t);
      },
      zoomPar(f) { d3.select(cv).transition().duration(350).call(zoom.scaleBy, f); },
      recentrer() { d3.select(cv).transition().duration(lent() ? 0 : 800).call(zoom.transform, cadrage(vue)); },
      choisir(ref) { choisi = ref; dessiner(); },
      ecran(lon, lat) { return [X(lon), Y(lat)]; },
      echelle: () => transform.k,
      marges(m) { Object.assign(marges, m); api.redimensionner(); },
      redimensionner() {
        const r = conteneur.getBoundingClientRect();
        dpr = window.devicePixelRatio || 1; W = r.width; H = r.height;
        cv.width = cache.width = Math.round(W * dpr); cv.height = cache.height = Math.round(H * dpr);
        cadrer(); cleCache = ''; dessiner();
      },
      dessiner
    };
    api.redimensionner();
    animer(0);
    new ResizeObserver(() => api.redimensionner()).observe(conteneur);
    return api;
  }

  window.CarteA = CarteA;
})();
