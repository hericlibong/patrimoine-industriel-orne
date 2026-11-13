// Outils communs aux esquisses de direction artistique (phase 10.E).
// Aucune donnée n'est inventée ici : tout vient de donnees.js, extrait de la
// vue de référence, plus la grille d'altitude IGN.
/* global d3, DONNEES */

const E = (window.E = {});

E.TYPES = Object.assign({}, DONNEES.libelles.evenements, {
  cessation: 'cessation',
  indetermine: 'fait daté',
});

E.ensemble = (code) => DONNEES.ensembles[code];

E.codeDepuisAdresse = () => (location.hash.includes('crulai') ? 'crulai' : 'risle');

// Projection équirectangulaire corrigée de la latitude : suffisante à
// l'échelle d'une vallée, et linéaire, ce qui permet d'y poser le relief tel quel.
E.projection = (ens, largeur, hauteur, marge = 40) => {
  const pts = ens.eau.flatMap((e) => e.points).concat(
    ens.sites.filter((s) => s.lon != null).map((s) => [s.lon, s.lat]),
  );
  const lat0 = d3.mean(pts, (p) => p[1]);
  const k = Math.cos((lat0 * Math.PI) / 180);
  const xs = pts.map((p) => p[0] * k);
  const ys = pts.map((p) => p[1]);
  const [x0, x1] = d3.extent(xs);
  const [y0, y1] = d3.extent(ys);
  const echelle = Math.min((largeur - 2 * marge) / (x1 - x0), (hauteur - 2 * marge) / (y1 - y0));
  const dx = (largeur - (x1 - x0) * echelle) / 2;
  const dy = (hauteur - (y1 - y0) * echelle) / 2;
  const f = (lon, lat) => [dx + (lon * k - x0) * echelle, dy + (y1 - lat) * echelle];
  f.kmEnPx = (echelle * 1) / 111.2; // 1 km en pixels
  return f;
};

E.cheminLigne = (proj, points) =>
  'M' + points.map((p) => proj(p[0], p[1]).map((v) => v.toFixed(1)).join(',')).join('L');

// Relief : contours et ombrage calculés depuis la grille IGN.
E.grille = (ens) => ens.relief;

E.versCarte = (proj, r) =>
  d3.geoTransform({
    point(i, j) {
      const [x, y] = proj(r.x0 + i * r.pas, r.y1 - j * r.pas);
      this.stream.point(x, y);
    },
  });

E.contours = (ens, proj, pas = 10) => {
  const r = ens.relief;
  const [zmin, zmax] = d3.extent(r.z);
  const seuils = d3.range(Math.ceil(zmin / pas) * pas, zmax, pas);
  const lisse = d3.blur2({ data: Float64Array.from(r.z), width: r.nx }, 1).data;
  const gen = d3.contours().size([r.nx, r.ny]).thresholds(seuils);
  const chemin = d3.geoPath(E.versCarte(proj, r));
  return gen(lisse).map((c) => ({ valeur: c.value, d: chemin(c) }));
};

// Ombrage : renvoie un canevas de la taille de la grille (une case = un pixel)
// et le rectangle où le poser une fois projeté.
E.ombrage = (ens, proj, couleur) => {
  const r = ens.relief;
  const c = document.createElement('canvas');
  c.width = r.nx;
  c.height = r.ny;
  const ctx = c.getContext('2d');
  const img = ctx.createImageData(r.nx, r.ny);
  const z = (i, j) => r.z[Math.max(0, Math.min(r.ny - 1, j)) * r.nx + Math.max(0, Math.min(r.nx - 1, i))];
  const cell = r.pas * 111200; // mètres, approximatif
  for (let j = 0; j < r.ny; j++) {
    for (let i = 0; i < r.nx; i++) {
      const dzdx = (z(i + 1, j) - z(i - 1, j)) / (2 * cell * 0.66);
      const dzdy = (z(i, j + 1) - z(i, j - 1)) / (2 * cell);
      const exag = 6;
      const nx = -dzdx * exag;
      const ny = dzdy * exag;
      const n = Math.hypot(nx, ny, 1);
      const lum = (nx * -0.6 + ny * 0.6 + 0.55) / n; // lumière du nord-ouest
      const v = couleur(lum, z(i, j));
      const o = (j * r.nx + i) * 4;
      img.data[o] = v[0];
      img.data[o + 1] = v[1];
      img.data[o + 2] = v[2];
      img.data[o + 3] = v[3];
    }
  }
  ctx.putImageData(img, 0, 0);
  const [a0, b0] = proj(r.x0 - r.pas / 2, r.y1 + r.pas / 2);
  const [a1, b1] = proj(r.x0 + (r.nx - 0.5) * r.pas, r.y1 - (r.ny - 0.5) * r.pas);
  return { canevas: c, x: a0, y: b0, l: a1 - a0, h: b1 - b0 };
};

// Chronologie d'un lieu, triée, avec ses bornes.
E.chrono = (ens, ref) => (ens.chronologie[ref] || []).slice().sort((a, b) => a.min - b.min);
E.bornes = (ens, ref) => {
  const ev = E.chrono(ens, ref);
  if (!ev.length) return null;
  const fin = ev.filter((e) => e.type === 'cessation' || e.type === 'destruction');
  return { debut: ev[0].min, fin: fin.length ? d3.max(fin, (e) => e.max) : null, dernier: d3.max(ev, (e) => e.max) };
};

E.metier = (s) => DONNEES.libelles.metiers[s.secteurs[0]] || 'Secteur inconnu';

E.nettoyer = (t) => (t || '').replace(/^"|"$/g, '').trim();

E.texteLieu = (s) => E.nettoyer(s.histoireEditoriale || s.histoire);

E.dateEv = (e) => (e.min === e.max ? `${e.min}` : `${e.min}–${e.max}`);

E.echapper = (t) =>
  String(t ?? '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]);

// Lieux rendus focalisables au clavier : Entrée ou Espace ouvre.
E.rendreActivable = (sel, ouvrir) =>
  sel
    .attr('tabindex', 0)
    .attr('role', 'button')
    .attr('aria-label', (s) => `${s.nomCourt}, ${s.commune}. Ouvrir ce lieu.`)
    .on('click', (ev, s) => ouvrir(s))
    .on('keydown', (ev, s) => {
      if (ev.key === 'Enter' || ev.key === ' ') {
        ev.preventDefault();
        ouvrir(s);
      }
    });

E.moinsDeMouvement = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
