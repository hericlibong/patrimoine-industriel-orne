// Vue propre d'un ensemble construit (Risle, Crulai et Chandai), proposition « édition ».
// Ce n'est pas un zoom sur la carte départementale : c'est une autre carte, à l'échelle
// du territoire de l'ensemble, reprise de l'esquisse D (communes, eau orientée, bourgs,
// relations documentées, cadrage borné) et redessinée dans la grammaire de la carte A′
// (même ombrage, mêmes teintes, même signe des lieux).
// Le courant de la rivière, repris de l'esquisse B, n'est animé que si la vue le demande.
/* global d3 */
(function () {
  const C = window.CARTE, D = window.DONNEES;
  const ENCRE = '#1e3040', EAU = '#3e7896', LIEN = '#a24e2c', ACCENT = '#b0482a';
  const SERIF = "'Source Serif 4', Georgia, serif", SANS = "'Source Sans 3', system-ui, sans-serif";
  const lent = () => matchMedia('(prefers-reduced-motion: reduce)').matches;

  function altitude(r, lon, lat) {
    const i = Math.round((lon - r.x0) / r.pas), j = Math.round((r.y1 - lat) / r.pas);
    return r.z[Math.max(0, Math.min(r.ny - 1, j)) * r.nx + Math.max(0, Math.min(r.nx - 1, i))];
  }

  function CarteEnsemble(conteneur, opts = {}) {
    const PAGE = opts.page || '#efede6';
    const mk = (z) => { const c = document.createElement('canvas'); c.setAttribute('aria-hidden', 'true'); c.style.cssText = `position:absolute;inset:0;width:100%;height:100%;display:block;touch-action:none;z-index:${z}`; conteneur.appendChild(c); return c; };
    const cv = mk(1), flux = mk(2);
    flux.style.pointerEvents = 'none';
    cv.style.cursor = 'default';
    const ctx = cv.getContext('2d'), fctx = flux.getContext('2d');
    const cache = document.createElement('canvas'), cctx = cache.getContext('2d');
    const marges = Object.assign({ g: 60, d: 60, h: 60, b: 60 }, opts.marges || {});
    let W = 0, H = 0, dpr = 1, transform = d3.zoomIdentity, cleCache = '';
    let ens = null, code = null, base = null, img = null, rect = null, troncons = [], particules = [], sites = [], parRef = new Map();
    let filtre = { metier: null, epoque: null }, choisi = null, survole = null, lienVif = null, curseur = null, actif = false;
    const etat = new Map();
    let ondes = [], tOnde = 1, minuterie = null;

    const retenu = (s) => (!filtre.metier || (s.secteurs || []).includes(filtre.metier)) && (!filtre.epoque || (s.epoques || []).includes(filtre.epoque));

    function construire(c) {
      code = c; ens = D.ensembles[c];
      sites = ens.sites.filter((s) => s.lon != null);
      parRef = new Map(sites.map((s) => [s.ref, s]));
      etat.clear(); sites.forEach((s) => etat.set(s.ref, retenu(s) ? 1 : 0));
      img = window.ombrageA(ens.relief, window.paletteA);
      choisi = survole = lienVif = curseur = null;
      cadrer();
      // eau orientée vers l'aval d'après le relief (esquisse D)
      troncons = ens.eau.map((e) => {
        const p = e.points.slice();
        if (altitude(ens.relief, ...p[0]) < altitude(ens.relief, ...p[p.length - 1])) p.reverse();
        const xy = p.map((q) => [bx(q[0]), by(q[1])]), cum = [0];
        for (let i = 1; i < xy.length; i++) cum.push(cum[i - 1] + Math.hypot(xy[i][0] - xy[i - 1][0], xy[i][1] - xy[i - 1][1]));
        return { pts: p, xy, cum, long: cum[cum.length - 1], principale: e.categorie === 'principale' };
      });
      particules = [];
      troncons.forEach((t) => { const n = Math.max(1, Math.round(t.long / (t.principale ? 10 : 30))); for (let i = 0; i < n; i++) particules.push({ t, d: Math.random() * t.long, v: (t.principale ? 0.42 : 0.24) * (0.7 + Math.random() * 0.6) }); });
      ordonner();
    }

    // projection propre à l'ensemble, cadrée sur ses lieux et les communes qui en portent
    let lat0, kx;
    function cadrer() {
      const pts = sites.map((s) => [s.lon, s.lat]).concat(ens.communes.filter((c) => c.porteUnLieu).flatMap((c) => c.anneaux.flat()));
      lat0 = d3.mean(pts, (p) => p[1]); kx = Math.cos(lat0 * Math.PI / 180);
      const [x0, x1] = d3.extent(pts, (p) => p[0] * kx), [y0, y1] = d3.extent(pts, (p) => -p[1]);
      const lw = W - marges.g - marges.d, lh = H - marges.h - marges.b;
      const s = Math.min(lw / (x1 - x0), lh / (y1 - y0));
      base = { s, tx: marges.g + lw / 2 - s * (x0 + x1) / 2, ty: marges.h + lh / 2 - s * (y0 + y1) / 2 };
      const r = ens.relief;
      rect = [bx(r.x0 - r.pas / 2), by(r.y1 + r.pas / 2), bx(r.x0 + (r.nx - 0.5) * r.pas), by(r.y1 - (r.ny - 0.5) * r.pas)];
      // la navigation reste bornée au territoire de l'ensemble
      zoom.scaleExtent([1, 16]).translateExtent([[Math.min(rect[0], 0), Math.min(rect[1], 0)], [Math.max(rect[2], W), Math.max(rect[3], H)]]);
    }
    const bx = (lon) => base.tx + base.s * lon * kx, by = (lat) => base.ty - base.s * lat;
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

    function fond() {
      const cle = `${code}|${W}|${H}|${transform.k}|${transform.x}|${transform.y}`;
      if (cle === cleCache) return;
      cleCache = cle;
      const g = cctx, k = transform.k;
      g.setTransform(dpr, 0, 0, dpr, 0, 0);
      g.fillStyle = PAGE; g.fillRect(0, 0, W, H);
      const [a0, b0] = [transform.applyX(rect[0]), transform.applyY(rect[1])], [a1, b1] = [transform.applyX(rect[2]), transform.applyY(rect[3])];
      g.imageSmoothingEnabled = true; g.imageSmoothingQuality = 'high';
      g.drawImage(img, a0, b0, a1 - a0, b1 - b0);
      g.save(); g.beginPath(); g.rect(a0, b0, a1 - a0, b1 - b0); g.clip();
      for (const f of C.forets) {
        g.beginPath(); for (const a of f.anneaux) chemin(g, a, true);
        g.fillStyle = 'rgba(122,150,112,.38)'; g.fill('evenodd'); g.strokeStyle = 'rgba(84,112,76,.5)'; g.lineWidth = 0.6; g.stroke();
      }
      // le territoire de l'ensemble reste en pleine lumière ; le reste passe sous un voile
      g.beginPath(); g.rect(a0, b0, a1 - a0, b1 - b0);
      for (const c of ens.communes) if (c.porteUnLieu) for (const a of c.anneaux) chemin(g, a, true);
      g.fillStyle = d3.color(PAGE).copy({ opacity: 0.58 }).formatRgb(); g.fill('evenodd');
      g.beginPath(); for (const c of ens.communes) for (const a of c.anneaux) chemin(g, a, true);
      g.setLineDash([2, 3]); g.lineWidth = 0.8; g.strokeStyle = 'rgba(30,48,64,.28)'; g.stroke(); g.setLineDash([]);
      g.beginPath(); for (const c of ens.communes) if (c.porteUnLieu) for (const a of c.anneaux) chemin(g, a, true);
      g.lineWidth = 1; g.strokeStyle = 'rgba(30,48,64,.45)'; g.stroke();
      // eau
      g.lineCap = 'round'; g.lineJoin = 'round';
      for (const principale of [false, true]) {
        g.beginPath(); for (const t of troncons) if (t.principale === principale) chemin(g, t.pts);
        const l = (principale ? 2.8 : 1) * Math.pow(k, 0.35);
        g.strokeStyle = 'rgba(240,242,237,.85)'; g.lineWidth = l + 2; g.stroke();
        g.strokeStyle = EAU; g.globalAlpha = principale ? 1 : 0.75; g.lineWidth = l; g.stroke(); g.globalAlpha = 1;
      }
      g.restore();
      // bords fondus dans la page : la carte n'a pas de cadre
      const fondu = 70;
      for (const [x, y, w, h, gx0, gy0, gx1, gy1] of [
        [a0, b0, fondu, b1 - b0, a0, 0, a0 + fondu, 0], [a1 - fondu, b0, fondu, b1 - b0, a1, 0, a1 - fondu, 0],
        [a0, b0, a1 - a0, fondu, 0, b0, 0, b0 + fondu], [a0, b1 - fondu, a1 - a0, fondu, 0, b1, 0, b1 - fondu]]) {
        const gr = g.createLinearGradient(gx0, gy0, gx1, gy1);
        gr.addColorStop(0, PAGE); gr.addColorStop(1, d3.color(PAGE).copy({ opacity: 0 }).formatRgb());
        g.fillStyle = gr; g.fillRect(x, y, w, h);
      }
    }

    let lieuxEcran = [], coteCourant = 8.5;
    function dessiner() {
      if (!ens || !W) return;
      fond();
      const k = transform.k;
      ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.drawImage(cache, 0, 0);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      const prises = [];
      // relations documentées
      ens.liens.forEach((l, i) => {
        const a = parRef.get(l.de), b = parRef.get(l.vers);
        if (!a || !b) return;
        const x1 = X(a.lon), y1 = Y(a.lat), x2 = X(b.lon), y2 = Y(b.lat);
        const mx = (x1 + x2) / 2 - (y2 - y1) * 0.3, my = (y1 + y2) / 2 + (x2 - x1) * 0.3;
        ctx.beginPath(); ctx.moveTo(x1, y1); ctx.quadraticCurveTo(mx, my, x2, y2);
        ctx.strokeStyle = LIEN; ctx.lineWidth = lienVif === i ? 2.4 : 1.3; ctx.globalAlpha = lienVif == null || lienVif === i ? 1 : 0.35;
        ctx.setLineDash(lienVif === i ? [] : [5, 4]); ctx.stroke(); ctx.setLineDash([]); ctx.globalAlpha = 1;
      });
      // bourgs
      for (const b of ens.bourgs) {
        const x = X(b.lon), y = Y(b.lat);
        ctx.beginPath(); ctx.rect(x - 2.5, y - 2.5, 5, 5); ctx.fillStyle = '#22303a'; ctx.fill();
        ctx.font = `600 13.5px ${SANS}`; const w = ctx.measureText(b.nom).width;
        boite(x + 6, y - 8, w + 4, 16, prises);
        texte(b.nom, x + 7, y, `600 13.5px ${SANS}`, '#22303a', 'rgba(240,242,237,.92)');
      }
      // lieux
      const cote = 8.5 * Math.min(1.5, Math.pow(k, 0.3));
      coteCourant = cote;
      lieuxEcran = [];
      for (const s of sites) {
        const a = etat.get(s.ref), x = X(s.lon), y = Y(s.lat);
        if (a > 0.5) lieuxEcran.push([x, y, s]);
        const c = 2 + (cote - 2) * a;
        ctx.globalAlpha = 0.42 + 0.58 * a;
        ctx.beginPath(); ctx.rect(x - c / 2, y - c / 2, c, c);
        if (a > 0.3) { ctx.lineWidth = 2.4 * a; ctx.strokeStyle = PAGE; ctx.stroke(); }
        ctx.fillStyle = ENCRE; ctx.fill();
        prises.push([x - c / 2 - 2, y - c / 2 - 2, x + c / 2 + 2, y + c / 2 + 2]);
      }
      ctx.globalAlpha = 1;
      if (tOnde < 1) for (const s of ondes) {
        const x = X(s.lon), y = Y(s.lat), c = cote + 26 * d3.easeCubicOut(tOnde);
        ctx.globalAlpha = 0.75 * (1 - tOnde);
        ctx.beginPath(); ctx.rect(x - c / 2, y - c / 2, c, c); ctx.lineWidth = 1.2; ctx.strokeStyle = ENCRE; ctx.stroke();
      }
      ctx.globalAlpha = 1;
      // noms : le lieu choisi, survolé ou proche du curseur de descente, puis les autres si la place le permet
      const enAvant = [choisi, survole, curseur && curseur.ref].filter(Boolean);
      const nommer = (s, fort) => {
        const nom = s.nomCourt || s.nom, x = X(s.lon) + cote / 2 + 6, y = Y(s.lat);
        const police = `${fort ? 600 : 400} ${fort ? 14 : 12.5}px ${SANS}`;
        ctx.font = police; const w = ctx.measureText(nom).width;
        if (!boite(x, y - 9, w + 4, 18, prises) && !fort) return;
        texte(nom, x, y, police, ENCRE, 'rgba(250,249,244,.95)');
      };
      for (const ref of enAvant) {
        const s = parRef.get(ref); if (!s) continue;
        ctx.beginPath(); ctx.rect(X(s.lon) - cote / 2 - 4, Y(s.lat) - cote / 2 - 4, cote + 8, cote + 8);
        ctx.lineWidth = ref === choisi ? 1.8 : 1.1; ctx.strokeStyle = ENCRE; ctx.stroke();
        if (curseur && ref === curseur.ref) {
          ctx.beginPath(); ctx.arc(X(s.lon), Y(s.lat), cote + 9, 0, 2 * Math.PI);
          ctx.lineWidth = 2.2; ctx.strokeStyle = ACCENT; ctx.stroke();
        }
        nommer(s, true);
      }
      if (k >= 1.6) for (const s of sites) if (etat.get(s.ref) > 0.5 && !enAvant.includes(s.ref)) nommer(s, false);
      // communes qui portent un lieu
      for (const c of ens.communes) {
        if (!c.porteUnLieu) continue;
        const a = d3.greatest(c.anneaux, (q) => q.length).map((p) => [X(p[0]), Y(p[1])]);
        const [cx, cy] = d3.polygonCentroid(a);
        ctx.font = `italic 400 13.5px ${SERIF}`; const w = ctx.measureText(c.nom).width;
        if (!boite(cx - w / 2, cy - 8, w, 16, prises)) continue;
        texte(c.nom, cx, cy, `italic 400 13.5px ${SERIF}`, 'rgba(30,48,64,.72)', 'rgba(240,242,237,.8)', 'center');
      }
    }

    // le courant : particules qui suivent l'eau vers l'aval
    let boucle = null;
    function couler() {
      boucle = null;
      if (!actif) return;
      fctx.setTransform(1, 0, 0, 1, 0, 0); fctx.clearRect(0, 0, flux.width, flux.height);
      if (opts.courant && opts.courant(code) && !lent()) {
        fctx.setTransform(dpr * transform.k, 0, 0, dpr * transform.k, dpr * transform.x, dpr * transform.y);
        fctx.lineCap = 'round';
        const [a0, b0, a1, b1] = rect;
        for (const p of particules) {
          p.d = (p.d + p.v) % p.t.long;
          const { xy, cum } = p.t;
          let i = d3.bisectRight(cum, p.d) - 1; i = Math.max(0, Math.min(xy.length - 2, i));
          const r = (p.d - cum[i]) / (cum[i + 1] - cum[i] || 1);
          const x = xy[i][0] + (xy[i + 1][0] - xy[i][0]) * r, y = xy[i][1] + (xy[i + 1][1] - xy[i][1]) * r;
          if (x < a0 + 30 || x > a1 - 30 || y < b0 + 30 || y > b1 - 30) continue;
          const dx = xy[i + 1][0] - xy[i][0], dy = xy[i + 1][1] - xy[i][1], n = Math.hypot(dx, dy) || 1;
          const l = (p.t.principale ? 5 : 3) / Math.sqrt(transform.k);
          fctx.strokeStyle = p.t.principale ? 'rgba(232,246,250,.95)' : 'rgba(225,242,247,.8)';
          fctx.lineWidth = (p.t.principale ? 1.5 : 0.8) / transform.k;
          fctx.beginPath(); fctx.moveTo(x - (dx / n) * l, y - (dy / n) * l); fctx.lineTo(x, y); fctx.stroke();
        }
      }
      boucle = requestAnimationFrame(couler);
    }

    // l'axe de la vallée, de l'amont vers l'aval (esquisse B) : support de la descente
    let axe = null, ordre = [];
    function ordonner() {
      const xy = sites.map((s) => [bx(s.lon), by(s.lat)]);
      const mx = d3.mean(xy, (q) => q[0]), my = d3.mean(xy, (q) => q[1]);
      let sxx = 0, syy = 0, sxy = 0;
      xy.forEach(([x, y]) => { sxx += (x - mx) ** 2; syy += (y - my) ** 2; sxy += (x - mx) * (y - my); });
      const ang = 0.5 * Math.atan2(2 * sxy, sxx - syy), ux = Math.cos(ang), uy = Math.sin(ang);
      const a = sites.map((s, i) => (xy[i][0] - mx) * ux + (xy[i][1] - my) * uy);
      const ext = d3.extent(a);
      const bout = (v) => d3.mean(sites.filter((s, i) => Math.abs(a[i] - v) < (ext[1] - ext[0]) * 0.15), (s) => altitude(ens.relief, s.lon, s.lat));
      const signe = bout(ext[0]) < bout(ext[1]) ? -1 : 1;
      const e2 = d3.extent(a, (v) => v * signe);
      ordre = sites.map((s, i) => ({ s, t: (a[i] * signe - e2[0]) / (e2[1] - e2[0]) })).sort((p, q) => p.t - q.t);
      const pas = d3.range(0, 1.0001, 0.02).map((t) => {
        const w = ordre.map((o) => Math.exp(-(((o.t - t) / 0.07) ** 2))), sw = d3.sum(w) || 1;
        return [d3.sum(ordre, (o, i) => bx(o.s.lon) * w[i]) / sw, d3.sum(ordre, (o, i) => by(o.s.lat) * w[i]) / sw];
      });
      axe = (t) => { const f = t * (pas.length - 1), i = Math.min(pas.length - 2, Math.floor(f)), r = f - i; return [pas[i][0] + (pas[i + 1][0] - pas[i][0]) * r, pas[i][1] + (pas[i + 1][1] - pas[i][1]) * r]; };
    }

    // le double clic rapproche (comportement d3 par défaut) ; la page suit chaque mouvement
    // pendant un glisser, le survol se tait et le curseur dit qu'on tient la carte
    let glisse = false, signature = '';
    const zoom = d3.zoom().filter((ev) => (!ev.ctrlKey || ev.type === 'wheel') && !ev.button)
      .on('start', (ev) => { if (ev.sourceEvent && ev.sourceEvent.type === 'mousedown') { glisse = true; cv.style.cursor = 'grabbing'; annoncer([]); } })
      .on('zoom', (ev) => { transform = ev.transform; dessiner(); if (opts.surTransform) opts.surTransform(); })
      .on('end', () => { if (glisse) { glisse = false; cv.style.cursor = 'default'; } });
    d3.select(cv).call(zoom);
    // tous les sites sous le pointeur : un seul, ou un groupe de sites superposés
    const objetsSous = (mx, my) => {
      const r = Math.max(9, coteCourant / 2 + 5), proches = [];
      for (const [x, y, s] of lieuxEcran) { const d = Math.hypot(x - mx, y - my); if (d <= r) proches.push([d, s]); }
      return proches.sort((a, b) => a[0] - b[0]).map((p) => p[1]);
    };
    // coordonnées dans le repère de dessin, même si la page agrandit ou réduit la carte en CSS
    const coords = (ev) => { const r = cv.getBoundingClientRect(), e = cv.clientWidth / (r.width || 1); return [(ev.clientX - r.left) * e, (ev.clientY - r.top) * e]; };
    // la page n'est prévenue que lorsque ce qui est sous le pointeur change
    function annoncer(l) {
      const sig = l.map((s) => s.ref).join('|');
      if (sig === signature) return;
      signature = sig;
      const id = l.length ? l[0].ref : null;
      if (id !== survole) { survole = id; dessiner(); }
      if (opts.survol) opts.survol(l);
    }
    cv.addEventListener('mousemove', (ev) => {
      if (glisse) return;
      const l = objetsSous(...coords(ev));
      cv.style.cursor = l.length ? 'pointer' : 'default';
      annoncer(l);
    });
    cv.addEventListener('mouseleave', () => { if (!glisse) cv.style.cursor = 'default'; annoncer([]); });
    cv.addEventListener('click', (ev) => { if (opts.clic) opts.clic(objetsSous(...coords(ev))); });

    function animer(duree) {
      const avant = new Map(etat), apres = new Map(sites.map((s) => [s.ref, retenu(s) ? 1 : 0]));
      ondes = sites.filter((s) => avant.get(s.ref) < 0.5 && apres.get(s.ref) === 1);
      if (minuterie) minuterie.stop();
      const pose = (t) => { for (const s of sites) etat.set(s.ref, avant.get(s.ref) + (apres.get(s.ref) - avant.get(s.ref)) * t); dessiner(); };
      if (!duree || lent()) { tOnde = 1; return pose(1); }
      const total = duree + 700;
      minuterie = d3.timer((e) => { tOnde = Math.min(1, e / total); pose(d3.easeCubicInOut(Math.min(1, e / duree))); if (e >= total) { minuterie.stop(); tOnde = 1; dessiner(); } });
    }
    const centre = (x, y, k) => d3.zoomIdentity.translate(marges.g + (W - marges.g - marges.d) / 2 - x * k, marges.h + (H - marges.h - marges.b) / 2 - y * k).scale(k);

    const api = {
      code: () => code,
      ensemble: () => ens,
      sites: () => sites,
      ordre: () => ordre,
      parRef: () => parRef,
      retenu,
      // ouvrir la vue : l'arrivée (léger rapprochement) est portée par la page, en CSS
      ouvrir(c, f) {
        filtre = { ...f };
        construire(c);
        cleCache = '';
        d3.select(cv).interrupt().call(zoom.transform, d3.zoomIdentity);
        api.activer(true);
      },
      activer(v) { actif = v; if (v && !boucle) boucle = requestAnimationFrame(couler); if (!v) { fctx.setTransform(1, 0, 0, 1, 0, 0); fctx.clearRect(0, 0, flux.width, flux.height); } },
      // un filtre change ce qui est visible : le survol en cours est oublié
      filtrer(f, anime = true) { filtre = { ...f }; signature = ''; survole = null; animer(anime ? 650 : 0); },
      choisir(ref) { choisi = ref; dessiner(); },
      lien(i) { lienVif = i; dessiner(); },
      montrerLieu(ref, k = 2.2) {
        const s = parRef.get(ref); if (!s) return;
        d3.select(cv).transition().duration(lent() ? 0 : 900).ease(d3.easeCubicInOut).call(zoom.transform, centre(bx(s.lon), by(s.lat), Math.max(k, transform.k)));
      },
      // descente au fil de l'eau : t de 0 (amont) à 1 (aval)
      descendre(t, immediat) {
        const [x, y] = axe(t);
        curseur = d3.least(ordre, (o) => Math.abs(o.t - t))?.s || null;
        const sel = d3.select(cv);
        (immediat || lent() ? sel.interrupt() : sel.transition().duration(450)).call(zoom.transform, centre(x, y, 2.4));
        dessiner();
        return curseur;
      },
      ecran(ref) { const s = parRef.get(ref); return s ? [X(s.lon), Y(s.lat)] : null; },
      cote: () => coteCourant,
      echelle: () => transform.k,
      // amène un site dans le cadre ; dx décale vers la gauche pour laisser la place à sa bulle
      allerVers(ref, k, duree = 900, dx = 0) {
        const s = parRef.get(ref); if (!s) return Promise.resolve();
        const cible = centre(bx(s.lon), by(s.lat), k || Math.max(2.6, transform.k)).translate(dx / (k || Math.max(2.6, transform.k)), 0);
        return new Promise((ok) => {
          setTimeout(ok, (lent() ? 0 : duree) + 80);
          d3.select(cv).transition('aller').duration(lent() ? 0 : duree).ease(d3.easeCubicInOut).call(zoom.transform, cible).on('end interrupt', ok);
        });
      },
      // rapproche sur un groupe de sites superposés, sans les déplacer
      deplier(refs) {
        // assez près pour que les deux sites les plus proches du groupe ne se recouvrent plus
        const pts = refs.map((r) => parRef.get(r)).filter(Boolean).map((s) => [bx(s.lon), by(s.lat)]);
        let dmin = Infinity;
        for (let i = 0; i < pts.length; i++) for (let j = i + 1; j < pts.length; j++) dmin = Math.min(dmin, Math.hypot(pts[i][0] - pts[j][0], pts[i][1] - pts[j][1]));
        const k = Math.min(16, Math.max(transform.k * 1.6, (8.5 * 1.5 + 8) / Math.max(dmin, 0.01)));
        const [cx, cy] = [d3.mean(pts, (p) => p[0]), d3.mean(pts, (p) => p[1])];
        d3.select(cv).transition().duration(lent() ? 0 : 800).ease(d3.easeCubicInOut).call(zoom.transform, centre(cx, cy, k));
      },
      parcours(ref) { curseur = ref ? parRef.get(ref) || null : null; dessiner(); },
      finDescente() { curseur = null; d3.select(cv).transition().duration(lent() ? 0 : 900).call(zoom.transform, d3.zoomIdentity); },
      zoomPar(f) { d3.select(cv).transition().duration(350).call(zoom.scaleBy, f); },
      recentrer() { d3.select(cv).transition().duration(lent() ? 0 : 800).call(zoom.transform, d3.zoomIdentity); },
      redimensionner() {
        // taille de mise en page, pas taille affichée : un effet de zoom CSS en cours
        // (arrivée dans un ensemble) ne doit pas fausser la surface de dessin
        dpr = window.devicePixelRatio || 1; W = conteneur.clientWidth; H = conteneur.clientHeight;
        if (!W || !H) return;
        cv.width = flux.width = cache.width = Math.round(W * dpr); cv.height = flux.height = cache.height = Math.round(H * dpr);
        if (ens) construire(code);
        cleCache = ''; dessiner();
      },
      dessiner
    };
    api.redimensionner();
    new ResizeObserver(() => api.redimensionner()).observe(conteneur);
    return api;
  }

  window.CarteEnsemble = CarteEnsemble;
})();
