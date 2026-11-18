// Mécanique commune aux deux compositions, reprise de l'esquisse D sans la modifier :
// état partagé par l'adresse, comptes par époque et par métier, recherche, contenu des
// fiches. Chaque page n'apporte que sa mise en page.
/* global d3 */
(function () {
  const D = window.DONNEES, DEP = D.departement;
  const EPOQUES = D.epoques, METIERS = D.libelles.metiers;
  const M = (window.M = { EPOQUES, METIERS, DEP });

  M.echapper = (t) => String(t ?? '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]);
  M.pluriel = (n, un, plus) => `${n.toLocaleString('fr-FR')} ${n > 1 ? plus : un}`;

  // état partagé : vue, métier, époque, lieu
  M.lireAdresse = (carte) => {
    const h = new URLSearchParams(location.hash.slice(1));
    return {
      vue: carte.DETAIL[h.get('vue')] ? h.get('vue') : 'orne',
      metier: METIERS[h.get('metier')] ? h.get('metier') : null,
      epoque: EPOQUES.some((e) => e.code === h.get('epoque')) ? h.get('epoque') : null,
      lieu: carte.parRef.has(h.get('lieu')) ? h.get('lieu') : null
    };
  };
  M.ecrireAdresse = (carte, lieu) => {
    const f = carte.filtre(), h = new URLSearchParams();
    if (carte.vue() !== 'orne') h.set('vue', carte.vue());
    if (f.metier) h.set('metier', f.metier);
    if (f.epoque) h.set('epoque', f.epoque);
    if (lieu) h.set('lieu', lieu);
    const s = h.toString();
    history.replaceState(null, '', s ? '#' + s : location.pathname);
  };

  // comptes, dans la vue courante (comme dans l'esquisse D)
  M.compte = (carte, m, ep) => {
    const ok = (s) => (!m || (s.secteurs || []).includes(m)) && (!ep || (s.epoques || []).includes(ep));
    if (carte.vue() !== 'orne') return carte.DETAIL[carte.vue()].sites.filter(ok).length;
    return d3.sum(carte.ENS, (e) => carte.compteEnsemble(e, m, ep)) + DEP.autresLieux.filter(ok).length;
  };
  M.metiersPresents = (carte, ep, garder) =>
    Object.keys(METIERS).map((m) => [m, M.compte(carte, m, ep)]).filter(([m, n]) => n > 0 || m === garder).sort((a, b) => b[1] - a[1]);

  // phrase calculée sur la sélection : ce que la carte montre, dit en texte
  M.phrase = (carte) => {
    const { metier, epoque } = carte.filtre(), n = M.compte(carte, metier, epoque);
    const ep = EPOQUES.find((e) => e.code === epoque);
    const quand = ep ? (ep.debut == null ? 'avant 1789' : `entre ${ep.debut} et ${ep.fin}`) : null;
    const quoi = metier ? METIERS[metier].toLowerCase() : null;
    if (carte.vue() !== 'orne') {
      const e = carte.DETAIL[carte.vue()];
      if (!metier && !epoque) return `${M.pluriel(e.sites.length, 'lieu documenté', 'lieux documentés')} dans cet ensemble.`;
      return `${M.pluriel(n, 'lieu', 'lieux')} de l'ensemble${quoi ? ` en ${quoi}` : ''}${quand ? `, rattaché${n > 1 ? 's' : ''} par les sources à la période ${quand}` : ''}.`;
    }
    if (!metier && !epoque) {
      const isoles = DEP.autresLieux.length;
      return `${DEP.nbLieux} lieux de production recensés : ${carte.ENS.length} ensembles en réunissent ${DEP.nbLieux - isoles}, ${isoles} sont isolés.`;
    }
    const isoles = DEP.autresLieux.filter(carte.retenu).length;
    const premier = d3.greatest(carte.ENS, (e) => carte.compteEnsemble(e));
    const tete = premier && carte.compteEnsemble(premier) > 0 ? ` Le plus fourni des ensembles : ${premier.nom} (${carte.compteEnsemble(premier)}).` : '';
    return `${M.pluriel(n, 'lieu', 'lieux')}${quoi ? ` en ${quoi}` : ''}${quand ? `, rattaché${n > 1 ? 's' : ''} par les sources à la période ${quand}` : ''}, dont ${isoles} hors ensemble.${tete}`;
  };

  // recherche : ensembles puis lieux, sans accents ni casse
  const normal = (t) => (t || '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
  M.chercher = (carte, q) => {
    q = normal(q.trim());
    if (q.length < 2) return [];
    const ens = carte.ENS.filter((e) => normal(e.nom).includes(q)).map((e) => ({ t: e.nom, s: `ensemble · ${e.nbSites} lieux`, ensemble: e }));
    const lx = carte.LIEUX.filter((s) => normal(`${s.nomCourt || ''} ${s.nom} ${s.commune} ${METIERS[(s.secteurs || [])[0]] || ''}`).includes(q))
      .map((s) => ({ t: s.nomCourt || s.nom, s: `${s.commune}${s._ens ? ' · ' + carte.DETAIL[s._ens].nom : ''}`, lieu: s }));
    return ens.concat(lx).slice(0, 10);
  };

  // fiches volontairement sommaires : leur forme n'est pas l'objet de l'expérimentation
  M.ficheLieu = (s) => {
    const m = (s.secteurs || [])[0];
    const texte = (s.histoireEditoriale || s.histoire || '').replace(/^"|"$/g, '').trim();
    const court = texte.length > 300 ? texte.slice(0, texte.lastIndexOf(' ', 280)) + '…' : texte;
    const prec = s.precision ? (D.libelles.precision?.[s.precision] || s.precision) : '';
    return `<div class="f-kicker">${M.echapper(METIERS[m] || 'Secteur inconnu')}</div>
      <h3>${M.echapper(s.nomCourt || s.nom)}</h3>
      <div class="f-ou">${M.echapper(s.commune || '')}${s.lieuDit ? ' — ' + M.echapper(s.lieuDit) : ''}</div>
      <div class="f-eps">${EPOQUES.map((e) => `<span class="${(s.epoques || []).includes(e.code) ? 'on' : ''}">${e.dates}</span>`).join('')}</div>
      ${court ? `<p>${M.echapper(court)}</p>` : ''}
      ${prec ? `<p class="f-note">Localisation : ${M.echapper(prec.toLowerCase())}.</p>` : ''}
      ${s.url ? `<a href="${M.echapper(s.url)}" target="_blank" rel="noopener">Dossier d'inventaire</a>` : ''}`;
  };
  M.ficheEnsemble = (e, construit) => `<div class="f-kicker">Ensemble · ${e.nbSites} lieux</div>
      <h3>${M.echapper(e.nom)}</h3>
      <div class="f-ou">${e.nomDeTravail ? M.echapper(e.nomDeTravail) + ' · ' : ''}autour de ${M.echapper(e.communePrincipale || '')}</div>
      ${e.presentationCourte ? `<p>${M.echapper(e.presentationCourte)}</p>` : ''}
      <div class="f-eps">${Object.entries(e.metiers).sort((a, b) => b[1] - a[1]).map(([m, n]) => `<span>${M.echapper(METIERS[m])} ${n}</span>`).join('')}</div>
      ${construit ? '' : '<p class="f-note">La vue détaillée de cet ensemble n\'est pas encore construite : seules la Risle et Crulai le sont.</p>'}`;
})();
