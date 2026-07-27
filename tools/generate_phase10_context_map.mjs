import fs from "node:fs";
import path from "node:path";

const root = path.resolve(import.meta.dirname, "..");
const designDir = path.join(root, "docs", "design", "phase10");
const communesPath = path.join(
  root,
  "data",
  "raw",
  "api_geo",
  "2026",
  "2026-07-22",
  "communes_orne_contours.geojson",
);
const sitesPath = path.join(
  root,
  "data",
  "exports",
  "sites_corpus_complet_v1.geojson",
);
const outlinePath = path.join(designDir, "map_orne_corpus_reel.svg");
const outputPath = path.join(designDir, "map_orne_context_reel.svg");
const prototypeOutputPath = path.join(
  root,
  "prototype",
  "phase10",
  "assets",
  "map-base.svg",
);

const width = 1000;
const height = 650;
const communes = JSON.parse(fs.readFileSync(communesPath, "utf8"));
const sites = JSON.parse(fs.readFileSync(sitesPath, "utf8"));
const outlineSvg = fs.readFileSync(outlinePath, "utf8");
const outlineMatch = outlineSvg.match(/<path d="([^"]+)" fill="#FCFAF5"/);
if (!outlineMatch) throw new Error("Contour de l'Orne introuvable");

const positions = [];
const collectPositions = (coordinates) => {
  if (typeof coordinates?.[0] === "number") {
    positions.push(coordinates);
    return;
  }
  for (const part of coordinates ?? []) collectPositions(part);
};
for (const feature of communes.features) {
  collectPositions(feature.geometry.coordinates);
}

let minLon = Number.POSITIVE_INFINITY;
let maxLon = Number.NEGATIVE_INFINITY;
let minLat = Number.POSITIVE_INFINITY;
let maxLat = Number.NEGATIVE_INFINITY;
for (const [longitude, latitude] of positions) {
  minLon = Math.min(minLon, longitude);
  maxLon = Math.max(maxLon, longitude);
  minLat = Math.min(minLat, latitude);
  maxLat = Math.max(maxLat, latitude);
}
const project = ([longitude, latitude]) => [
  ((longitude - minLon) / (maxLon - minLon)) * width,
  ((maxLat - latitude) / (maxLat - minLat)) * height,
];

const escapeXml = (value) =>
  String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");

const sampleRing = (ring, maximum = 90) => {
  if (ring.length <= maximum) return ring;
  const step = Math.ceil(ring.length / maximum);
  const sampled = ring.filter((_, index) => index % step === 0);
  sampled.push(ring.at(-1));
  return sampled;
};

const linePath = (line, maximum = 90, close = false) => {
  const points = sampleRing(line, maximum).map(project);
  if (points.length < 2) return "";
  return `${points
    .map(([x, y], index) => `${index ? "L" : "M"}${x.toFixed(1)} ${y.toFixed(1)}`)
    .join(" ")}${close ? " Z" : ""}`;
};

const geometryLines = (geometry) => {
  if (!geometry) return [];
  if (geometry.type === "LineString") return [geometry.coordinates];
  if (geometry.type === "MultiLineString") return geometry.coordinates;
  return [];
};

const geometryPolygons = (geometry) => {
  if (!geometry) return [];
  if (geometry.type === "Polygon") return [geometry.coordinates];
  if (geometry.type === "MultiPolygon") return geometry.coordinates;
  return [];
};

const ringArea = (ring) => {
  const points = ring.map(project);
  let area = 0;
  for (let index = 0; index < points.length; index += 1) {
    const current = points[index];
    const next = points[(index + 1) % points.length];
    area += current[0] * next[1] - next[0] * current[1];
  }
  return Math.abs(area / 2);
};

const readGeojsonDirectory = (name) => {
  const directory = path.join(root, "data", "raw", name, "2026", "2026-07-23");
  const features = new Map();
  for (const filename of fs.readdirSync(directory)) {
    if (!filename.endsWith(".geojson")) continue;
    const payload = JSON.parse(
      fs.readFileSync(path.join(directory, filename), "utf8"),
    );
    for (const feature of payload.features ?? []) {
      const identifier =
        feature.id ??
        feature.properties?.cleabs ??
        feature.properties?.id ??
        JSON.stringify(feature.geometry);
      if (!features.has(identifier)) features.set(identifier, feature);
    }
  }
  return [...features.values()];
};

const forests = readGeojsonDirectory("forets");
const hydrography = readGeojsonDirectory("hydrographie");
const rail = readGeojsonDirectory("rail");

const forestPaths = [];
for (const feature of forests) {
  for (const polygon of geometryPolygons(feature.geometry)) {
    const outerRing = polygon[0];
    if (ringArea(outerRing) < 12) continue;
    forestPaths.push(`<path d="${linePath(outerRing, 55, true)}"/>`);
  }
}

const hydroPaths = [];
for (const feature of hydrography) {
  const properties = feature.properties ?? {};
  const isMain =
    properties.reseau_principal_coulant === true &&
    Boolean(properties.cpx_toponyme_de_cours_d_eau) &&
    Number(properties.numero_d_ordre ?? 0) >= 3;
  if (!isMain) continue;
  for (const line of geometryLines(feature.geometry)) {
    hydroPaths.push(`<path d="${linePath(line, 55)}"/>`);
  }
}

const railPaths = [];
for (const feature of rail) {
  if (feature.properties?.nature === "Voie de service") continue;
  for (const line of geometryLines(feature.geometry)) {
    railPaths.push(`<path d="${linePath(line, 55)}"/>`);
  }
}

const communePaths = [];
for (const feature of communes.features) {
  for (const polygon of geometryPolygons(feature.geometry)) {
    communePaths.push(`<path d="${linePath(polygon[0], 70, true)}"/>`);
  }
}

const siteMarks = sites.features
  .map((feature) => {
    const [x, y] = project(feature.geometry.coordinates);
    const precision = feature.properties.precision_geographique_code;
    return precision === "zone_documentaire"
      ? `<rect x="${(x - 2.2).toFixed(1)}" y="${(y - 2.2).toFixed(
          1,
        )}" width="4.4" height="4.4" rx="0.8"/>`
      : `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="1.8"/>`;
  })
  .join("");

const cities = [
  ["Alençon", -0.092, 48.432],
  ["Argentan", -0.018, 48.744],
  ["Flers", -0.569, 48.748],
  ["L'Aigle", 0.628, 48.764],
  ["Mortagne-au-Perche", 0.547, 48.521],
  ["Domfront", -0.648, 48.592],
];
const cityMarks = cities
  .map(([name, longitude, latitude]) => {
    const [x, y] = project([longitude, latitude]);
    return `<g transform="translate(${x.toFixed(1)} ${y.toFixed(
      1,
    )})"><circle r="3.2"/><text x="7" y="-5">${escapeXml(name)}</text></g>`;
  })
  .join("");

const scaledOutline = `scale(${(width / 620).toFixed(8)} ${(height / 400).toFixed(
  8,
)})`;
const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}" role="img" aria-label="Carte contextuelle réelle de l'Orne, avec communes, forêts, cours d'eau, rail actuel et 318 sites documentés">
  <defs>
    <clipPath id="orne-clip"><path d="${outlineMatch[1]}" transform="${scaledOutline}"/></clipPath>
    <pattern id="zone-pattern" width="4" height="4" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="4" stroke="#7B5B8E" stroke-width="1"/></pattern>
  </defs>
  <rect width="${width}" height="${height}" fill="#E9EFEA"/>
  <g clip-path="url(#orne-clip)">
    <rect width="${width}" height="${height}" fill="#FBFAF6"/>
    <g fill="#D4E3D4" fill-opacity="0.82" stroke="none">${forestPaths.join("")}</g>
    <g fill="none" stroke="#D7D2C9" stroke-width="0.55" stroke-linejoin="round">${communePaths.join("")}</g>
    <g fill="none" stroke="#4F89A8" stroke-width="1.35" stroke-linecap="round" stroke-opacity="0.82">${hydroPaths.join("")}</g>
    <g fill="none" stroke="#3E4542" stroke-width="1.25" stroke-dasharray="5 3" stroke-linecap="round" stroke-opacity="0.78">${railPaths.join("")}</g>
    <g fill="#E45240" fill-opacity="0.84">${siteMarks}</g>
  </g>
  <path d="${outlineMatch[1]}" transform="${scaledOutline}" fill="none" stroke="#173F35" stroke-width="3" vector-effect="non-scaling-stroke"/>
  <g fill="#173F35" font-family="Inter, Arial, sans-serif" font-size="14" font-weight="650">${cityMarks}</g>
  <g transform="translate(28 598)" font-family="Inter, Arial, sans-serif" font-size="12" fill="#354942">
    <rect width="944" height="38" rx="19" fill="#FCFAF5" fill-opacity="0.94"/>
    <circle cx="24" cy="19" r="3" fill="#E45240"/><text x="34" y="23">site documenté</text>
    <rect x="166" y="15" width="8" height="8" rx="1" fill="url(#zone-pattern)" stroke="#7B5B8E"/><text x="182" y="23">zone documentaire</text>
    <line x1="335" y1="19" x2="363" y2="19" stroke="#4F89A8" stroke-width="2"/><text x="372" y="23">cours d'eau</text>
    <rect x="480" y="13" width="13" height="12" fill="#D4E3D4"/><text x="501" y="23">forêt actuelle</text>
    <line x1="622" y1="19" x2="653" y2="19" stroke="#3E4542" stroke-width="1.5" stroke-dasharray="5 3"/><text x="662" y="23">rail actuel</text>
    <text x="784" y="23" fill="#6D756F">Contexte IGN · limites communales</text>
  </g>
</svg>`;

fs.writeFileSync(outputPath, svg, "utf8");

const prototypeSvg = `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}" aria-hidden="true" focusable="false">
  <defs>
    <clipPath id="prototype-orne-clip"><path d="${outlineMatch[1]}" transform="${scaledOutline}"/></clipPath>
  </defs>
  <rect width="${width}" height="${height}" fill="#E9EFEA"/>
  <g clip-path="url(#prototype-orne-clip)">
    <rect width="${width}" height="${height}" fill="#FBFAF6"/>
    <g id="layer-forests" fill="#D4E3D4" fill-opacity="0.82" stroke="none">${forestPaths.join("")}</g>
    <g id="layer-communes" fill="none" stroke="#D7D2C9" stroke-width="0.55" stroke-linejoin="round">${communePaths.join("")}</g>
    <g id="layer-water" fill="none" stroke="#4F89A8" stroke-width="1.35" stroke-linecap="round" stroke-opacity="0.82">${hydroPaths.join("")}</g>
    <g id="layer-rail" fill="none" stroke="#3E4542" stroke-width="1.25" stroke-dasharray="5 3" stroke-linecap="round" stroke-opacity="0.78">${railPaths.join("")}</g>
  </g>
  <path d="${outlineMatch[1]}" transform="${scaledOutline}" fill="none" stroke="#173F35" stroke-width="3" vector-effect="non-scaling-stroke"/>
  <g fill="#173F35" font-family="Inter, Arial, sans-serif" font-size="14" font-weight="650">${cityMarks}</g>
</svg>`;

fs.mkdirSync(path.dirname(prototypeOutputPath), { recursive: true });
fs.writeFileSync(prototypeOutputPath, prototypeSvg, "utf8");
console.log(
  JSON.stringify(
    {
      output: path.relative(root, outputPath),
      prototype_output: path.relative(root, prototypeOutputPath),
      sites: sites.features.length,
      forests: forestPaths.length,
      hydrography: hydroPaths.length,
      rail: railPaths.length,
      communes: communePaths.length,
    },
    null,
    2,
  ),
);
