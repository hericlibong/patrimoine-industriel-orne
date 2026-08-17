const SECTOR_LABELS = {
  agroalimentaire: "Agroalimentaire",
  bois_papier_imprimerie: "Bois, papier et imprimerie",
  chimie_caoutchouc_plastiques: "Chimie, caoutchouc et plastiques",
  energie: "Énergie",
  extraction: "Extraction",
  mecanique_electrique: "Mécanique et électricité",
  metallurgie_travail_metaux: "Métallurgie et travail des métaux",
  textile_habillement_cuir: "Textile, habillement et cuir",
  verre_ceramique_materiaux_construction:
    "Verre, céramique et matériaux de construction",
};

const PERIOD_LABELS = {
  avant_1789: "Avant 1789",
  revolution_premiere_industrialisation: "1789–1849",
  industrialisation_rail_vapeur: "1850–1913",
  guerres_entre_deux_guerres: "1914–1945",
  modernisation_apres_guerre: "1946–1975",
  mutations_reconversions: "1976–2000",
  periode_contemporaine: "Depuis 2001",
};

const PRECISION_LABELS = {
  point_approximatif: "Point approximatif",
  zone_documentaire: "Zone documentaire",
};

const CURRENT_LABELS = {
  conserve: "Site conservé",
  degrade: "Site dégradé",
  partiellement_conserve: "Site partiellement conservé",
  vestiges: "Vestiges",
  ruine: "Site en ruine",
  disparu: "Site disparu",
  inconnu: "Conservation inconnue",
};

const ACCESS_LABELS = {
  visite: "Visitable",
  visitable: "Visitable",
  partiellement_visitable: "Partiellement visitable",
  visible_espace_public: "Visible depuis l’espace public",
  prive_visible: "Propriété privée visible",
  prive_non_visible: "Propriété privée non visible",
  interdit: "Accès interdit",
  inconnu: "Accès non documenté",
};

const USE_LABELS = {
  activite_industrielle: "Activité industrielle",
  culture_musee: "Usage culturel ou muséal",
  tourisme_visite: "Accueil touristique ou visite",
  sans_usage: "Sans usage documenté",
  inconnu: "Usage non documenté",
};

const STORY_STATES = [
  {
    key: "all",
    label: "318 sites documentés",
    test: () => true,
  },
  {
    key: "textile",
    label: "Le textile dessine un réseau de lieux",
    test: (site) =>
      site.activities.some(
        (activity) => activity.sector === "textile_habillement_cuir",
      ),
  },
  {
    key: "water",
    label: "213 sites sont situés à moins de 100 mètres d’un cours d’eau",
    test: (site) =>
      ["moins_25_m", "moins_100_m"].includes(site.waterProximity),
  },
  {
    key: "multi",
    label: "73 lieux documentent plusieurs phases d’activité",
    test: (site) => site.activityCount > 1,
  },
  {
    key: "current",
    label: "La situation actuelle n’est documentée que pour une minorité de lieux",
    test: (site) => site.situationDocumented,
  },
  {
    key: "all",
    label: "L’exploration replace chaque lieu dans le corpus complet",
    test: () => true,
  },
];

const PLACE_CONTENT = {
  "oze-moulinex": {
    title: "Moulin d’Ozé — Moulinex",
    eyebrow: "Un lieu, plusieurs vies industrielles",
    question:
      "Comment un même lieu passe-t-il du moulin à la production industrielle ?",
    imageAlt:
      "Vue aérienne du site industriel d’Ozé à Alençon, à la fin des années 1980.",
    reading:
      "La photographie permet de lire l’emprise du site, son rapport aux voies et au tissu urbain. Elle ne sert pas seulement d’illustration : elle devient une pièce du récit, mise en regard des activités successives.",
    current:
      "La situation actuelle de ce site reste à documenter dans le corpus. Ce manque est affiché comme une information, sans déduire un état à partir de la photographie ancienne.",
  },
  abadie: {
    title: "Usine Abadie",
    eyebrow: "Un paysage façonné par l’industrie",
    question:
      "Que nous apprend cette image sur la place de l’usine dans son territoire ?",
    imageAlt:
      "Vue aérienne de l’ancienne usine Abadie au bord de l’Huisne, en 1988.",
    reading:
      "La rivière, les bâtiments, les voies et le bourg sont lus ensemble. Le lieu révèle ainsi une organisation territoriale : l’industrie n’est pas un point isolé, mais un système inscrit dans un paysage.",
    current:
      "La situation actuelle n’est pas suffisamment documentée pour être qualifiée. La fiche distingue donc clairement ce que les sources historiques établissent de ce qui reste à vérifier aujourd’hui.",
  },
  bohin: {
    title: "Établissements Bohin",
    eyebrow: "Une activité industrielle encore lisible",
    question:
      "Comment un site ancien peut-il conserver une activité et transmettre son histoire ?",
    imageAlt:
      "Vue aérienne du site Bohin à Saint-Sulpice-sur-Risle, au début des années 1980.",
    reading:
      "L’image replace les bâtiments industriels dans la vallée. La chronologie permet ensuite de suivre le passage d’un usage hydraulique à une activité métallurgique toujours associée au lieu.",
    current:
      "Le corpus documente ici une conservation du site, une activité industrielle et une ouverture à la visite. Ces informations actuelles sont présentées séparément de l’histoire du lieu.",
  },
};

const state = {
  sites: [],
  visibleSites: [],
  selectedSite: null,
  listOpen: false,
  mapLayers: new Set(["water", "rail", "forests", "communes"]),
  filters: {
    query: "",
    activity: "",
    period: "",
    current: "",
    precision: "",
  },
};

const dom = {};

function normalize(value = "") {
  return value
    .normalize("NFD")
    .replace(/\p{Diacritic}/gu, "")
    .toLowerCase()
    .trim();
}

function escapeHtml(value = "") {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function formatDate(value) {
  if (!value) return "date non renseignée";
  return value.replace(/^vers\s+/i, "vers ");
}

function activityDate(activity) {
  if (activity.start && activity.end) {
    return `${formatDate(activity.start)} — ${formatDate(activity.end)}`;
  }
  if (activity.start) return `à partir de ${formatDate(activity.start)}`;
  if (activity.end) return `jusqu’à ${formatDate(activity.end)}`;
  return "datation non renseignée";
}

async function loadMapBase() {
  const response = await fetch("./assets/map-base.svg");
  if (!response.ok) throw new Error("La carte de contexte n’a pas pu être chargée.");
  const svg = await response.text();
  document.querySelectorAll("[data-map-base]").forEach((container) => {
    container.innerHTML = svg;
  });
}

function cacheDom() {
  dom.views = [...document.querySelectorAll("[data-view]")];
  dom.navLinks = [...document.querySelectorAll("[data-route]")];
  dom.storyMap = document.querySelector("#story-map");
  dom.storyMarkers = document.querySelector("#story-markers");
  dom.storyCaption = document.querySelector("#story-map-caption");
  dom.storySteps = [...document.querySelectorAll("[data-story-state]")];
  dom.explorerMap = document.querySelector("#explorer-map");
  dom.explorerMarkers = document.querySelector("#explorer-markers");
  dom.resultCount = document.querySelector("#result-count");
  dom.resultList = document.querySelector("#result-list");
  dom.noResults = document.querySelector("#no-results");
  dom.drawer = document.querySelector("#site-drawer");
  dom.drawerContent = document.querySelector("#drawer-content");
  dom.listToggle = document.querySelector("#list-toggle");
  dom.resetFilters = document.querySelector("#reset-filters");
  dom.filtersForm = document.querySelector("#filters-form");
  dom.placePage = document.querySelector("#place-page");
}

function populateFilters() {
  const activitySelect = document.querySelector("#activity-filter");
  const periodSelect = document.querySelector("#period-filter");

  Object.entries(SECTOR_LABELS)
    .sort(([, a], [, b]) => a.localeCompare(b, "fr"))
    .forEach(([value, label]) => {
      activitySelect.add(new Option(label, value));
    });

  Object.entries(PERIOD_LABELS).forEach(([value, label]) => {
    periodSelect.add(new Option(label, value));
  });
}

function marker(site, interactive = false) {
  const element = document.createElement(interactive ? "button" : "span");
  element.className = "map-marker";
  element.classList.toggle("zone", site.precision === "zone_documentaire");
  element.style.left = `${site.x}%`;
  element.style.top = `${site.y}%`;
  element.dataset.siteId = site.id;
  element.title = `${site.name}, ${site.commune}`;

  if (interactive) {
    element.type = "button";
    element.tabIndex = -1;
    element.setAttribute("aria-label", `Voir ${site.name}, ${site.commune}`);
    element.addEventListener("click", () => openSite(site.id));
  } else {
    element.setAttribute("aria-hidden", "true");
  }
  return element;
}

function renderMarkers() {
  const storyFragment = document.createDocumentFragment();
  const explorerFragment = document.createDocumentFragment();
  state.sites.forEach((site) => {
    storyFragment.append(marker(site));
    explorerFragment.append(marker(site, true));
  });
  dom.storyMarkers.replaceChildren(storyFragment);
  dom.explorerMarkers.replaceChildren(explorerFragment);
}

function activateStoryStep(index) {
  const storyState = STORY_STATES[index] || STORY_STATES[0];
  dom.storySteps.forEach((step, stepIndex) => {
    step.classList.toggle("is-active", stepIndex === index);
  });
  dom.storyMarkers.querySelectorAll(".map-marker").forEach((item) => {
    const site = state.sites.find((candidate) => candidate.id === item.dataset.siteId);
    const active = site && storyState.test(site);
    item.classList.toggle("is-dimmed", !active);
    item.classList.toggle("is-highlighted", active && storyState.key !== "all");
  });
  dom.storyMap.dataset.state = storyState.key;
  dom.storyCaption.textContent = storyState.label;
}

function setupStoryObserver() {
  if (!("IntersectionObserver" in window)) {
    activateStoryStep(0);
    return;
  }

  const observer = new IntersectionObserver(
    (entries) => {
      const visible = entries
        .filter((entry) => entry.isIntersecting)
        .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
      if (!visible) return;
      activateStoryStep(Number(visible.target.dataset.storyState));
    },
    { rootMargin: "-30% 0px -45% 0px", threshold: [0.15, 0.45, 0.75] },
  );

  dom.storySteps.forEach((step) => observer.observe(step));
}

function siteMatches(site) {
  const { query, activity, period, current, precision } = state.filters;
  const queryHaystack = normalize(
    [
      site.name,
      site.commune,
      site.placeName,
      site.address,
      site.reference,
      ...site.activities.map((item) => SECTOR_LABELS[item.sector] || item.sector),
    ].join(" "),
  );

  if (query && !queryHaystack.includes(normalize(query))) return false;

  if (
    (activity || period) &&
    !site.activities.some(
      (item) =>
        (!activity || item.sector === activity) &&
        (!period || item.periods.includes(period)),
    )
  ) {
    return false;
  }

  if (current === "documented" && !site.situationDocumented) return false;
  if (current === "unknown" && site.situationDocumented) return false;
  if (precision && site.precision !== precision) return false;
  return true;
}

function filterLabel() {
  const labels = [];
  if (state.filters.activity) labels.push(SECTOR_LABELS[state.filters.activity]);
  if (state.filters.period) labels.push(PERIOD_LABELS[state.filters.period]);
  if (state.filters.current === "documented") labels.push("situation documentée");
  if (state.filters.current === "unknown") labels.push("situation non documentée");
  if (state.filters.precision) labels.push(PRECISION_LABELS[state.filters.precision]);
  if (state.filters.query) labels.push(`« ${state.filters.query} »`);
  return labels.join(", ");
}

function updateExplorer() {
  state.visibleSites = state.sites.filter(siteMatches);
  const visibleIds = new Set(state.visibleSites.map((site) => site.id));
  const hasFilters = Object.values(state.filters).some(Boolean);

  dom.explorerMarkers.querySelectorAll(".map-marker").forEach((item) => {
    item.hidden = !visibleIds.has(item.dataset.siteId);
    item.classList.toggle(
      "is-selected",
      item.dataset.siteId === state.selectedSite?.id,
    );
  });

  const suffix = hasFilters ? ` pour ${filterLabel()}` : " dans le corpus";
  dom.resultCount.textContent = `${state.visibleSites.length} ${
    state.visibleSites.length > 1 ? "sites" : "site"
  }${suffix}`;
  dom.resetFilters.hidden = !hasFilters;
  dom.noResults.hidden = state.visibleSites.length !== 0;
  renderResultList();

  if (
    state.selectedSite &&
    !visibleIds.has(state.selectedSite.id) &&
    !state.listOpen
  ) {
    closeDrawer();
  }
}

function renderResultList() {
  const fragment = document.createDocumentFragment();
  state.visibleSites.forEach((site) => {
    const item = document.createElement("li");
    const button = document.createElement("button");
    button.type = "button";
    button.className = "result-list__button";
    button.innerHTML = `
      <strong>${escapeHtml(site.name)}</strong>
      <span>${escapeHtml(site.commune)} · ${site.activityCount} ${
        site.activityCount > 1 ? "phases" : "phase"
      }</span>
    `;
    button.addEventListener("click", () => openSite(site.id));
    item.append(button);
    fragment.append(item);
  });
  dom.resultList.replaceChildren(fragment);
}

function currentStatusMarkup(site) {
  if (!site.situationDocumented) {
    return `
      <div class="status-box">
        <p><strong>Aujourd’hui</strong></p>
        <strong>Situation non documentée</strong>
        <p>Le corpus ne permet pas de qualifier l’état actuel de ce lieu.</p>
      </div>
    `;
  }

  const details = [
    CURRENT_LABELS[site.conservation] || site.conservation,
    ...site.uses.map((use) => USE_LABELS[use] || use),
    ACCESS_LABELS[site.accessibility] || site.accessibility,
  ].filter(Boolean);

  return `
    <div class="status-box">
      <p><strong>Aujourd’hui</strong></p>
      <strong>${escapeHtml(details[0] || "Situation documentée")}</strong>
      ${details
        .slice(1)
        .map((detail) => `<p>${escapeHtml(detail)}</p>`)
        .join("")}
    </div>
  `;
}

function sitePanelMarkup(site) {
  const feature = site.featured;
  const activities = site.activities
    .map(
      (activity) => `
        <li>
          <div>
            <strong>${escapeHtml(
              SECTOR_LABELS[activity.sector] || activity.sector,
            )}</strong>
            <small>${escapeHtml(activityDate(activity))}</small>
          </div>
        </li>
      `,
    )
    .join("");

  return `
    <div class="drawer-header">
      <p class="eyebrow">Fiche synthétique</p>
      <button type="button" class="icon-button" data-close-drawer aria-label="Fermer la fiche">×</button>
    </div>
    ${
      feature
        ? `<img class="drawer-image" src="./assets/${escapeHtml(
            feature.image,
          )}" alt="" loading="lazy">`
        : ""
    }
    <p class="eyebrow">${escapeHtml(site.commune)}</p>
    <h2>${escapeHtml(site.name)}</h2>
    <p class="drawer-lead">Un même lieu, ${site.activityCount} ${
      site.activityCount > 1 ? "phases d’activité documentées" : "phase d’activité documentée"
    }.</p>
    <ul class="activity-list">${activities}</ul>
    ${currentStatusMarkup(site)}
    <p class="precision-chip">${escapeHtml(
      PRECISION_LABELS[site.precision] || PRECISION_LABELS.inconnue,
    )}</p>
    <div class="drawer-actions">
      ${
        feature
          ? `<a class="button button--primary" href="#lieux/${escapeHtml(
              feature.slug,
            )}">Lire le récit du lieu</a>`
          : ""
      }
      ${
        site.sourceUrl
          ? `<a class="text-link" href="${escapeHtml(
              site.sourceUrl,
            )}" target="_blank" rel="noreferrer">Consulter la source patrimoniale</a>`
          : ""
      }
    </div>
  `;
}

function openDrawer() {
  dom.drawer.hidden = false;
  document.body.classList.add("drawer-open");
}

function closeDrawer() {
  state.selectedSite = null;
  state.listOpen = false;
  dom.drawer.hidden = false;
  dom.drawerContent.innerHTML = `
    <div class="drawer-empty">
      <p class="eyebrow">Aucun site sélectionné</p>
      <h2>Choisissez un point ou ouvrez la liste</h2>
      <p>Le détail apparaîtra ici sans vous faire perdre l’état de la carte.</p>
    </div>
  `;
  document.body.classList.remove("drawer-open");
  dom.listToggle.setAttribute("aria-expanded", "false");
  dom.listToggle.textContent = "Afficher la liste";
  updateExplorer();
}

function openSite(id) {
  const site = state.sites.find((candidate) => candidate.id === id);
  if (!site) return;
  state.selectedSite = site;
  state.listOpen = false;
  dom.listToggle.setAttribute("aria-expanded", "false");
  dom.listToggle.textContent = "Afficher la liste";
  dom.drawerContent.innerHTML = sitePanelMarkup(site);
  dom.drawerContent
    .querySelector("[data-close-drawer]")
    .addEventListener("click", closeDrawer);
  openDrawer();
  dom.drawerContent.querySelector("h2").setAttribute("tabindex", "-1");
  dom.drawerContent.querySelector("h2").focus();
  updateExplorer();
}

function toggleResultList() {
  state.listOpen = !state.listOpen;
  state.selectedSite = null;
  if (state.listOpen) {
    dom.drawerContent.innerHTML = `
      <div class="drawer-header">
        <p class="eyebrow">Alternative à la carte</p>
        <button type="button" class="icon-button" data-close-drawer aria-label="Fermer la liste">×</button>
      </div>
      <h2 tabindex="-1">${state.visibleSites.length} ${
        state.visibleSites.length > 1 ? "lieux" : "lieu"
      }</h2>
      <p>La liste donne accès aux mêmes résultats que la carte.</p>
      <ul class="result-list" data-drawer-list></ul>
    `;
    const drawerList = dom.drawerContent.querySelector("[data-drawer-list]");
    drawerList.replaceChildren(...[...dom.resultList.children].map((item) => item.cloneNode(true)));
    [...drawerList.querySelectorAll("button")].forEach((button, index) => {
      button.addEventListener("click", () => openSite(state.visibleSites[index].id));
    });
    dom.drawerContent
      .querySelector("[data-close-drawer]")
      .addEventListener("click", closeDrawer);
    openDrawer();
    dom.listToggle.setAttribute("aria-expanded", "true");
    dom.listToggle.textContent = "Masquer la liste";
    dom.drawerContent.querySelector("h2").focus();
  } else {
    closeDrawer();
  }
}

function setupExplorer() {
  dom.filtersForm.addEventListener("input", () => {
    state.filters.query = document.querySelector("#search-filter").value;
    state.filters.activity = document.querySelector("#activity-filter").value;
    state.filters.period = document.querySelector("#period-filter").value;
    state.filters.current = document.querySelector("#current-filter").value;
    state.filters.precision = document.querySelector("#precision-filter").value;
    updateExplorer();
  });

  dom.filtersForm.addEventListener("submit", (event) => event.preventDefault());
  dom.resetFilters.addEventListener("click", () => {
    dom.filtersForm.reset();
    Object.keys(state.filters).forEach((key) => {
      state.filters[key] = "";
    });
    updateExplorer();
  });
  dom.listToggle.addEventListener("click", toggleResultList);
  document.querySelector("#clear-empty-filters").addEventListener("click", () => {
    dom.filtersForm.reset();
    Object.keys(state.filters).forEach((key) => {
      state.filters[key] = "";
    });
    updateExplorer();
  });

  document.querySelectorAll("[data-layer]").forEach((control) => {
    control.addEventListener("change", () => {
      const layer = control.dataset.layer;
      if (control.checked) state.mapLayers.add(layer);
      else state.mapLayers.delete(layer);
      document
        .querySelector(`#explorer-map #layer-${layer}`)
        ?.classList.toggle("hidden-layer", !control.checked);
    });
  });
}

function placeTimeline(site) {
  return site.activities
    .map(
      (activity) => `
        <li>
          <p class="timeline__date">${escapeHtml(activityDate(activity))}</p>
          <h3>${escapeHtml(
            SECTOR_LABELS[activity.sector] || activity.sector,
          )}</h3>
          ${
            activity.label
              ? `<p>${escapeHtml(activity.label)}</p>`
              : "<p>Activité documentée dans le corpus.</p>"
          }
        </li>
      `,
    )
    .join("");
}

function renderPlace(slug) {
  const site = state.sites.find((candidate) => candidate.featured?.slug === slug);
  const content = PLACE_CONTENT[slug];
  if (!site || !content) {
    dom.placePage.innerHTML = `
      <div class="place-not-found">
        <p class="eyebrow">Les lieux</p>
        <h1>Ce récit de lieu n’existe pas dans le prototype.</h1>
        <a class="button button--primary" href="#explorer">Revenir à la carte</a>
      </div>
    `;
    return;
  }

  dom.placePage.innerHTML = `
    <article class="place-article">
      <header class="place-hero">
        <div class="place-hero__copy">
          <p class="eyebrow">${escapeHtml(content.eyebrow)}</p>
          <p class="place-hero__location">${escapeHtml(site.commune)}</p>
          <h1>${escapeHtml(content.title)}</h1>
          <p class="place-hero__source-name">${escapeHtml(site.name)}</p>
          <p class="place-hero__question">${escapeHtml(content.question)}</p>
          <div class="place-hero__links">
            <a href="#explorer" class="text-link">Retour à l’exploration</a>
            ${
              site.sourceUrl
                ? `<a href="${escapeHtml(
                    site.sourceUrl,
                  )}" class="text-link" target="_blank" rel="noreferrer">Source patrimoniale</a>`
                : ""
            }
          </div>
        </div>
        <figure class="place-hero__figure">
          <img src="./assets/${escapeHtml(
            site.featured.image,
          )}" alt="${escapeHtml(content.imageAlt)}">
          <figcaption>
            Document visuel conservé dans le corpus. Légende et crédit seront finalisés avec le texte éditorial.
          </figcaption>
        </figure>
      </header>

      <div class="place-grid">
        <section class="place-card place-card--reading" aria-labelledby="reading-title">
          <p class="place-card__number">01</p>
          <h2 id="reading-title">Lire le paysage</h2>
          <p>${escapeHtml(content.reading)}</p>
          <div class="reading-keys" aria-label="Clés de lecture de l’image">
            <span>eau</span><span>bâtiments</span><span>voies</span><span>bourg</span>
          </div>
        </section>

        <section class="place-card place-card--timeline" aria-labelledby="timeline-title">
          <p class="place-card__number">02</p>
          <h2 id="timeline-title">Les activités dans le temps</h2>
          <ol class="timeline">${placeTimeline(site)}</ol>
        </section>

        <section class="place-card place-card--current" aria-labelledby="current-title">
          <p class="place-card__number">03</p>
          <h2 id="current-title">Ce que l’on sait aujourd’hui</h2>
          <p>${escapeHtml(content.current)}</p>
          ${currentStatusMarkup(site)}
        </section>

        <section class="place-card place-card--location" aria-labelledby="location-title">
          <p class="place-card__number">04</p>
          <h2 id="location-title">Situer et vérifier</h2>
          <dl class="place-facts">
            <div><dt>Commune</dt><dd>${escapeHtml(site.commune)}</dd></div>
            <div><dt>Lieu-dit</dt><dd>${escapeHtml(
              site.placeName || "non renseigné",
            )}</dd></div>
            <div><dt>Référence</dt><dd>${escapeHtml(site.reference)}</dd></div>
            <div><dt>Position</dt><dd>${escapeHtml(
              PRECISION_LABELS[site.precision] || PRECISION_LABELS.inconnue,
            )}</dd></div>
          </dl>
          <a class="button button--secondary" href="#methode">Comprendre la méthode</a>
        </section>
      </div>
    </article>
  `;
}

function route() {
  const hash = window.location.hash || "#accueil";
  const [routeName, slug] = hash.slice(1).split("/");
  const viewName =
    routeName === "explorer"
      ? "explorer"
      : routeName === "methode"
        ? "method"
        : routeName === "lieux"
          ? "place"
          : "home";

  dom.views.forEach((view) => {
    view.hidden = view.dataset.view !== viewName;
  });

  dom.navLinks.forEach((link) => {
    const active =
      (routeName === "recit" && link.dataset.route === "recit") ||
      (routeName !== "recit" && link.dataset.route === viewName);
    if (active) link.setAttribute("aria-current", "page");
    else link.removeAttribute("aria-current");
  });

  if (viewName === "place") renderPlace(slug);
  if (viewName !== "explorer" && !dom.drawer.hidden) closeDrawer();

  window.requestAnimationFrame(() => {
    if (routeName === "recit") {
      document.querySelector("#recit")?.scrollIntoView({ behavior: "smooth" });
    } else {
      window.scrollTo({ top: 0, behavior: "instant" });
      const main = document.querySelector("#contenu");
      main.setAttribute("tabindex", "-1");
      main.focus({ preventScroll: true });
    }
  });
}

function setupGlobalEvents() {
  window.addEventListener("hashchange", route);
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && !dom.drawer.hidden) {
      closeDrawer();
      dom.listToggle.focus();
    }
  });
}

async function initialize() {
  cacheDom();
  populateFilters();
  const [sitesResponse] = await Promise.all([
    fetch("./data/sites.json"),
    loadMapBase(),
  ]);
  if (!sitesResponse.ok) throw new Error("Les données du prototype n’ont pas pu être chargées.");
  const payload = await sitesResponse.json();
  state.sites = payload.sites;
  state.visibleSites = payload.sites;

  renderMarkers();
  setupStoryObserver();
  setupExplorer();
  setupGlobalEvents();
  updateExplorer();
  activateStoryStep(0);
  route();
  document.documentElement.classList.add("is-ready");
}

initialize().catch((error) => {
  console.error(error);
  document.querySelector("#app-error").hidden = false;
});
