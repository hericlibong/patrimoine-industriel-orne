// Carte départementale de la proposition « édition » (phase 10.E, 18 novembre 2026).
// Dessin repris de la carte A′ « Gravure affinée » retenue à titre provisoire : relief
// topographique, forêts publiques, rivières par ordre, villes ; ensembles en cercles
// numérotés ; lieux hors ensemble en carrés bleu d'encre détourés un à un.
// Deux différences avec le module des compositions précédentes, qui reste intact :
//  - la carte ne montre que l'échelle départementale : les lieux d'un ensemble ouvert
//    vivent dans sa propre vue (carte_ensemble.js), pas sur ce fond ;
//  - un lieu écarté par la sélection ne s'efface pas : il se réduit à une trace, et un
//    lieu qui entre dans la sélection est signalé par une onde brève.
// Le fond extérieur au département prend la couleur de la page : la carte n'a pas de cadre.
/* global d3 */
(function () {
  const C = window.CARTE, D = window.DONNEES, DEP = D.departement;
  const ENCRE = '#1e3040', NOM_PILOTE = '#16242f', NOM = '#22323f';
  const T = {
    hypso: [[60, '#dfe6d8'], [150, '#e9e8d6'], [250, '#e4dcc6'], [420, '#d6c9ae']], ombre: 0.62,
    eau: '#3e7896', eauHalo: 'rgba(233,236,230,.9)',
    foret: 'rgba(122,150,112,.42)', foretTrait: 'rgba(84,112,76,.55)',
    contour: '#2a3640', contourL: 1.2,
    ville: '#22303a', villeTxt: '#22303a', halo: 'rgba(240,242,237,.9)', foretTxt: '#4f6a46', riviereTxt: '#2f6582'
  };
  const SERIF = "'Source Serif 4', Georgia, serif", SANS = "'Source Sans 3', system-ui, sans-serif";
  const DETAIL = D.ensembles, ENS = DEP.ensembles;

  const LIEUX = DEP.autresLieux.filter((s) => s.lon != null).map((s) => Object.assign({}, s, DEP.complements[s.ref] || {}));
  LIEUX.sort((a, b) => b.lat - a.lat); // du nord au sud : ordre de détourage
  const parRef = new Map(LIEUX.map((s) => [s.ref, s]));

  const anneau = C.contour[0];
  const lon0 = d3.mean(anneau, (p) => p[0]), lat0 = d3.mean(anneau, (p) => p[1]);
  const kx = Math.cos(lat0 * Math.PI / 180);
  const px = (lon) => (lon - lon0) * kx, py = (lat) => -(lat - lat0);
  const R = C.relief;
  const zAt = (i, j) => R.z[Math.max(0, Math.min(R.ny - 1, j)) * R.nx + Math.max(0, Math.min(R.nx - 1, i))];
  const parOrdre = d3.sort(d3.groups(C.rivieres, (r) => r.ordre), (g) => g[0]);
  const rivieresNommees = [...d3.group(C.rivieres.filter((r) => r.ordre >= 5 && r.nom), (r) => r.nom)]
    .map(([nom, rs]) => [nom, d3.greatest(rs, (r) => r.pts.length)]).filter(([, r]) => r.pts.length >= 6);

  // ombrage multidirectionnel et teintes hypsométriques, identiques à la carte seule
  function ombrage(r, palette = T) {
    const z = (i, j) => r.z[Math.max(0, Math.min(r.ny - 1, j)) * r.nx + Math.max(0, Math.min(r.nx - 1, i))];
    const o = document.createElement('canvas'); o.width = r.nx; o.height = r.ny;
    const g = o.getContext('2d'), im = g.createImageData(r.nx, r.ny);
    const k = Math.cos(((r.y1 - r.ny * r.pas / 2) * Math.PI) / 180);
    const dxm = r.pas * 111320 * k, dym = r.pas * 110570, ex = 4;
    const sources = [[315, 0.6], [270, 0.2], [0, 0.2]];
    const teinte = d3.scaleLinear().domain(palette.hypso.map((h) => h[0])).range(palette.hypso.map((h) => h[1])).clamp(true);
    for (let j = 0; j < r.ny; j++) for (let i = 0; i < r.nx; i++) {
      const dzdx = ex * (z(i + 1, j) - z(i - 1, j)) / (2 * dxm), dzdy = ex * (z(i, j - 1) - z(i, j + 1)) / (2 * dym);
      const pente = Math.atan(Math.hypot(dzdx, dzdy)), asp = Math.atan2(dzdy, -dzdx);
      let l = 0;
      for (const [az, w] of sources) {
        const a = (360 - az + 90) * Math.PI / 180, h = Math.PI / 4;
        l += w * Math.max(0, Math.sin(h) * Math.cos(pente) + Math.cos(h) * Math.sin(pente) * Math.cos(a - asp));
      }
      const q = (j * r.nx + i) * 4, c = d3.rgb(teinte(z(i, j))), f = 1 - palette.ombre * (1 - l / Math.sin(Math.PI / 4));
      im.data[q] = c.r * f; im.data[q + 1] = c.g * f; im.data[q + 2] = c.b * f; im.data[q + 3] = 255;
    }
    g.putImageData(im, 0, 0);
    return o;
  }
  let imageRelief = null;
  const relief = () => imageRelief || (imageRelief = ombrage(R));

  function CarteDepartement(conteneur, opts = {}) {
    const PAGE = opts.page || '#efede6';
    const cv = document.createElement('canvas');
    cv.setAttribute('aria-hidden', 'true');
    cv.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;display:block;cursor:grab;touch-action:none';
    conteneur.appendChild(cv);
    const ctx = cv.getContext('2d');
    const cache = document.createElement('canvas'), cctx = cache.getContext('2d');
    let W = 0, H = 0, dpr = 1, base = null, transform = d3.zoomIdentity, cleCache = '';
    const marges = Object.assign({ g: 60, d: 60, h: 60, b: 60 }, opts.marges || {});
    const filtre = { metier: null, epoque: null };
    let choisi = null, survole = null, ouvert = null;

    const retenu = (s) => (!filtre.metier || (s.secteurs || []).includes(filtre.metier)) && (!filtre.epoque || (s.epoques || []).includes(filtre.epoque));
    const compteEnsemble = (e, m = filtre.metier, ep = filtre.epoque) =>
      m && ep ? e.sitesParMetierEpoque[`${m}|${ep}`] || 0 : m ? e.metiers[m] || 0 : ep ? e.sitesParEpoque[ep] || 0 : e.nbSites;

    // valeurs animées : présence des lieux (1 = retenu, 0 = trace), effectif des ensembles
    const etatLieu = new Map(LIEUX.map((s) => [s.ref, 1]));
    const etatEns = new Map(ENS.map((e) => [e.code, e.nbSites]));
    let ondes = [], tOnde = 1, minuterie = null;
    // quand un filtre est actif, les sites retenus grossissent un peu : ils tiennent face aux traces
    let ampl = 1;
    function animer(duree = 650) {
      const avant = new Map(etatLieu), avantE = new Map(etatEns), amplA = ampl, amplB = filtre.metier || filtre.epoque ? 1.22 : 1;
      const apres = new Map(LIEUX.map((s) => [s.ref, retenu(s) ? 1 : 0]));
      ondes = LIEUX.filter((s) => avant.get(s.ref) < 0.5 && apres.get(s.ref) === 1);
      if (minuterie) minuterie.stop();
      const pose = (t) => {
        for (const s of LIEUX) etatLieu.set(s.ref, avant.get(s.ref) + (apres.get(s.ref) - avant.get(s.ref)) * t);
        for (const e of ENS) etatEns.set(e.code, avantE.get(e.code) + (compteEnsemble(e) - avantE.get(e.code)) * t);
        ampl = amplA + (amplB - amplA) * t;
        dessiner();
      };
      if (!duree || matchMedia('(prefers-reduced-motion: reduce)').matches) { tOnde = 1; return pose(1); }
      const total = duree + 700;
      minuterie = d3.timer((ecoule) => {
        tOnde = Math.min(1, ecoule / total);
        pose(d3.easeCubicInOut(Math.min(1, ecoule / duree)));
        if (ecoule >= total) { minuterie.stop(); tOnde = 1; dessiner(); }
      });
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
      g.fillStyle = PAGE; g.fillRect(0, 0, W, H);
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
      // hors du département : la page, avec un souvenir du relief voisin
      g.save(); g.beginPath(); g.rect(0, 0, W, H); for (const a of C.contour) chemin(g, a, true);
      g.fillStyle = d3.color(PAGE).copy({ opacity: 0.86 }).formatRgb(); g.fill('evenodd'); g.restore();
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

      // lieux : carré d'encre détouré ; écarté, il se réduit à une trace
      const ech = Math.min(1.7, Math.pow(k, 0.4)), cote = 3.6 * ech * Math.sqrt(Math.PI) * ampl;
      lieuxEcran = [];
      ctx.lineJoin = 'miter';
      for (const s of LIEUX) {
        const a = etatLieu.get(s.ref);
        const x = X(s.lon), y = Y(s.lat);
        if (x < -10 || y < -10 || x > W + 10 || y > H + 10) continue;
        if (a > 0.5) lieuxEcran.push([x, y, s]);
        const c = 1.7 + (cote - 1.7) * a;
        ctx.globalAlpha = 0.34 + 0.66 * a;
        ctx.beginPath(); ctx.rect(x - c / 2, y - c / 2, c, c);
        if (a > 0.3) { ctx.lineWidth = 2.2 * a; ctx.strokeStyle = PAGE; ctx.stroke(); }
        ctx.fillStyle = ENCRE; ctx.fill();
      }
      ctx.globalAlpha = 1;
      // onde : un lieu qui entre dans la sélection se signale une fois
      if (tOnde < 1) for (const s of ondes) {
        const x = X(s.lon), y = Y(s.lat), c = cote + 22 * d3.easeCubicOut(tOnde);
        ctx.globalAlpha = 0.75 * (1 - tOnde);
        ctx.beginPath(); ctx.rect(x - c / 2, y - c / 2, c, c); ctx.lineWidth = 1.2; ctx.strokeStyle = ENCRE; ctx.stroke();
      }
      ctx.globalAlpha = 1;
      for (const ref of [choisi, survole]) {
        const s = ref && parRef.get(ref);
        if (!s) continue;
        ctx.beginPath(); ctx.rect(X(s.lon) - cote / 2 - 4, Y(s.lat) - cote / 2 - 4, cote + 8, cote + 8);
        ctx.lineWidth = ref === choisi ? 1.6 : 1; ctx.strokeStyle = ENCRE; ctx.stroke();
        const nom = s.nomCourt || s.nom;
        texte(nom, X(s.lon) + cote / 2 + 8, Y(s.lat), `600 13px ${SANS}`, ENCRE, 'rgba(250,249,244,.95)');
        ctx.font = `600 13px ${SANS}`;
        prises.push([X(s.lon) + cote / 2 + 6, Y(s.lat) - 9, X(s.lon) + cote / 2 + 10 + ctx.measureText(nom).width, Y(s.lat) + 9]);
      }

      // ensembles : cercle à l'effectif filtré ; un filet garde la taille entière
      ensEcran = [];
      const noms = [];
      const ordre = [...ENS].sort((a, b) => !!DETAIL[a.code] - !!DETAIL[b.code]);
      for (const e of ordre) {
        const n = etatEns.get(e.code);
        const pilote = !!DETAIL[e.code], x = X(e.lon), y = Y(e.lat), r = n > 0.05 ? rEns(n) : 0, rT = rEns(e.nbSites);
        if (n < e.nbSites - 0.05) {
          ctx.beginPath(); ctx.arc(x, y, rT, 0, 2 * Math.PI);
          ctx.lineWidth = 1; ctx.strokeStyle = 'rgba(30,48,64,.42)'; ctx.setLineDash([2, 2.5]); ctx.stroke(); ctx.setLineDash([]);
        }
        if (r > 0) {
          ctx.beginPath(); ctx.arc(x, y, r, 0, 2 * Math.PI);
          ctx.lineWidth = pilote ? 3 : 4.5; ctx.strokeStyle = PAGE; ctx.stroke();
          ctx.fillStyle = pilote ? ENCRE : PAGE; ctx.fill();
          if (!pilote) { ctx.lineWidth = 1.6; ctx.strokeStyle = ENCRE; ctx.stroke(); }
          ctx.fontVariantNumeric = 'lining-nums tabular-nums';
          texte(String(Math.round(n)), x, y + 0.5, `600 ${Math.max(11, r * 0.78)}px ${SERIF}`, pilote ? PAGE : ENCRE, null, 'center');
        }
        if (ouvert === e.code || survole === e.code) {
          ctx.beginPath(); ctx.arc(x, y, Math.max(r, rT) + 5, 0, 2 * Math.PI); ctx.lineWidth = 1; ctx.strokeStyle = ENCRE; ctx.stroke();
        }
        const rp = Math.max(r, rT * 0.6);
        prises.push([x - rp - 3, y - rp - 3, x + rp + 3, y + rp + 3]);
        ensEcran.push([x, y, Math.max(rp, 11), e]);
        noms.push({ e, x, y, r: Math.max(r, 6), pilote, vide: n < 0.5 });
      }
      noms.sort((a, b) => b.pilote - a.pilote);
      for (const { e, x, y, r, pilote, vide } of noms) {
        const police = `${pilote ? 600 : 400} ${pilote ? 15.5 : 13.5}px ${SERIF}`;
        ctx.font = police; const w = ctx.measureText(e.nom).width, h = 18;
        const essais = [[x + r + 7, y - h / 2], [x - r - 7 - w, y - h / 2], [x - w / 2, y + r + 4], [x - w / 2, y - r - 4 - h]];
        const [bx0, by0] = essais.find(([a, b]) => boite(a, b, w, h, prises)) || essais[0];
        ctx.globalAlpha = vide ? 0.4 : 1;
        texte(e.nom, bx0, by0 + h / 2, police, pilote ? NOM_PILOTE : NOM, T.halo);
        ctx.globalAlpha = 1;
      }

      // étiquettes du fond, après les données pour les éviter
      for (const v of C.villes) {
        const grande = v.prefecture || v.sousPrefecture;
        if (!grande && v.pop < (k > 2 ? 2000 : k > 1.3 ? 3000 : 4500)) continue;
        const x = X(v.lon), y = Y(v.lat), taille = grande ? 14.5 : 12.5;
        ctx.font = `${grande ? 600 : 400} ${taille}px ${SANS}`;
        const w = ctx.measureText(v.nom).width;
        if (!boite(x + 6, y - taille / 2, w + 4, taille, prises)) continue;
        ctx.beginPath(); ctx.rect(x - 2.5, y - 2.5, 5, 5); ctx.fillStyle = T.ville; ctx.fill();
        texte(v.nom, x + 7, y, `${grande ? 600 : 400} ${taille}px ${SANS}`, T.villeTxt, T.halo);
      }
      for (const [nom, r] of rivieresNommees) {
        const m = Math.floor(r.pts.length / 2), a = r.pts[Math.max(0, m - 2)], b = r.pts[Math.min(r.pts.length - 1, m + 2)];
        if (!d3.polygonContains(anneau, r.pts[m])) continue;
        const x = X(r.pts[m][0]), y = Y(r.pts[m][1]);
        let ang = Math.atan2(Y(b[1]) - Y(a[1]), X(b[0]) - X(a[0]));
        if (ang > Math.PI / 2) ang -= Math.PI; if (ang < -Math.PI / 2) ang += Math.PI;
        if (!boite(x - 40, y - 8, 80, 16, prises)) continue;
        ctx.save(); ctx.translate(x, y); ctx.rotate(ang);
        texte(nom, 0, -7, `italic 400 12.5px ${SERIF}`, T.riviereTxt, T.halo, 'center');
        ctx.restore();
      }
      for (const f of C.forets) {
        const a = d3.greatest(f.anneaux, (q) => q.length).map((p) => [X(p[0]), Y(p[1])]);
        if (Math.abs(d3.polygonArea(a)) < 1800) continue;
        const c = d3.polygonCentroid(a);
        const nom = (f.nom || '').replace(/^Forêt (Domaniale|Communale|départementale)? ?(de |d'|des |du )?/i, '');
        const lib = 'forêt ' + (/^[AEIOUÉÈ]/.test(nom) ? "d'" : 'de ') + nom;
        ctx.font = `italic 400 12px ${SERIF}`;
        const w = ctx.measureText(lib).width;
        if (!boite(c[0] - w / 2, c[1] - 7, w, 14, prises)) continue;
        texte(lib, c[0], c[1], `italic 400 12px ${SERIF}`, T.foretTxt, T.halo, 'center');
      }
    }

    const lent = () => matchMedia('(prefers-reduced-motion: reduce)').matches;
    const zoom = d3.zoom().scaleExtent([0.8, 14])
      .filter((ev) => (!ev.ctrlKey || ev.type === 'wheel') && !ev.button)
      .on('zoom', (ev) => { transform = ev.transform; dessiner(); });
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
      const id = o ? (o.type === 'lieu' ? o.s.ref : o.e.code) : null;
      if (id !== survole) { survole = id; dessiner(); if (opts.survol) opts.survol(o); }
    });
    cv.addEventListener('mouseleave', () => { if (survole) { survole = null; dessiner(); if (opts.survol) opts.survol(null); } });
    cv.addEventListener('click', (ev) => { if (opts.clic) opts.clic(objetSous(...coords(ev))); });

    const centrer = (lon, lat, k) => d3.zoomIdentity
      .translate(marges.g + (W - marges.g - marges.d) / 2 - bx(lon) * k, marges.h + (H - marges.h - marges.b) / 2 - by(lat) * k).scale(k);

    const api = {
      LIEUX, ENS, DETAIL, parRef, retenu, compteEnsemble,
      filtre: () => ({ ...filtre }),
      filtrer(f, anime = true) { Object.assign(filtre, f); animer(anime ? 650 : 0); },
      // plonger : la carte s'enfonce vers l'ensemble avant de céder la place à sa vue
      plonger(e, duree = 750) {
        // la promesse se tient même si le navigateur suspend l'animation (onglet caché)
        return new Promise((ok) => {
          setTimeout(ok, (lent() ? 0 : duree) + 120);
          d3.select(cv).transition().duration(lent() ? 0 : duree).ease(d3.easeCubicIn)
            .call(zoom.transform, centrer(e.lon, e.lat, 4.5)).on('end interrupt', ok);
        });
      },
      remonter(e, duree = 900) {
        if (e) d3.select(cv).call(zoom.transform, centrer(e.lon, e.lat, 4.5));
        d3.select(cv).transition().duration(lent() ? 0 : duree).ease(d3.easeCubicOut).call(zoom.transform, d3.zoomIdentity);
      },
      voler(lon, lat, k = 3) { d3.select(cv).transition().duration(lent() ? 0 : 1000).ease(d3.easeCubicInOut).call(zoom.transform, centrer(lon, lat, k)); },
      zoomPar(f) { d3.select(cv).transition().duration(350).call(zoom.scaleBy, f); },
      recentrer() { d3.select(cv).transition().duration(lent() ? 0 : 800).call(zoom.transform, d3.zoomIdentity); },
      choisir(ref) { choisi = ref; dessiner(); },
      ouvrirEnsemble(code) { ouvert = code; dessiner(); },
      echelle: () => transform.k,
      redimensionner() {
        const r = conteneur.getBoundingClientRect();
        dpr = window.devicePixelRatio || 1; W = r.width; H = r.height;
        if (!W || !H) return;
        cv.width = cache.width = Math.round(W * dpr); cv.height = cache.height = Math.round(H * dpr);
        cadrer(); cleCache = ''; dessiner();
      },
      dessiner
    };
    api.redimensionner();
    new ResizeObserver(() => api.redimensionner()).observe(conteneur);
    return api;
  }

  window.CarteDepartement = CarteDepartement;
  window.ombrageA = ombrage;
  window.paletteA = T;
})();
