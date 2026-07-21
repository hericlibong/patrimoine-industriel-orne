import fs from "node:fs/promises";
import { FileBlob, SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const outputPath = process.argv[2];
const previewDir = process.argv[3];
if (!outputPath || !previewDir) throw new Error("outputPath et previewDir requis");

if (process.argv[4] === "--verify") {
  const imported = await SpreadsheetFile.importXlsx(await FileBlob.load(outputPath));
  const check = await imported.inspect({
    kind: "workbook,sheet,table,formula",
    maxChars: 12000,
    tableMaxRows: 10,
    tableMaxCols: 14,
  });
  await fs.mkdir(previewDir, { recursive: true });
  await fs.writeFile(`${previewDir}/import_verification.ndjson`, check.ndjson, "utf8");
  for (const sheetName of ["Consignes", "Sources", "Personne A", "Personne B", "Vocabulaires", "Comparaison"]) {
    const preview = await imported.render({ sheetName, autoCrop: "all", scale: 1, format: "png" });
    await fs.writeFile(`${previewDir}/${sheetName.replaceAll(" ", "_")}_importee.png`, new Uint8Array(await preview.arrayBuffer()));
  }
  process.exit(0);
}

const workbook = Workbook.create();
const instructions = workbook.worksheets.add("Consignes");
const sourceSheet = workbook.worksheets.add("Sources");
const personA = workbook.worksheets.add("Personne A");
const personB = workbook.worksheets.add("Personne B");
const vocab = workbook.worksheets.add("Vocabulaires");
const comparison = workbook.worksheets.add("Comparaison");

const navy = "#18324A";
const blue = "#2F6B8A";
const paleBlue = "#EAF3F7";
const paleYellow = "#FFF5CC";
const paleGreen = "#E6F4EA";
const gray = "#667085";

for (const sheet of [instructions, sourceSheet, personA, personB, vocab, comparison]) {
  sheet.showGridLines = false;
}

instructions.mergeCells("A1:H2");
instructions.getRange("A1").values = [["Double classement indépendant — Phase 5"]];
instructions.getRange("A1:H2").format = {
  fill: navy,
  font: { bold: true, color: "#FFFFFF", size: 18 },
  verticalAlignment: "center",
};
instructions.getRange("A4:H4").merge();
instructions.getRange("A4").values = [["Objectif"]];
instructions.getRange("A4:H4").format = { fill: blue, font: { bold: true, color: "#FFFFFF" } };
instructions.getRange("A5:H6").merge();
instructions.getRange("A5").values = [[
  "Vérifier que deux personnes appliquent les mêmes règles aux mêmes sources. Chaque personne travaille sans consulter la feuille de l’autre.",
]];
instructions.getRange("A5:H6").format = { wrapText: true, verticalAlignment: "top" };
instructions.getRange("A8:H8").merge();
instructions.getRange("A8").values = [["Mode d’emploi"]];
instructions.getRange("A8:H8").format = { fill: blue, font: { bold: true, color: "#FFFFFF" } };
const steps = [
  ["1", "Attribuer le fichier à deux personnes différentes : A et B."],
  ["2", "Lire uniquement les notices de la feuille Sources et le vocabulaire autorisé."],
  ["3", "Remplir sa propre feuille. Ne pas consulter la feuille de l’autre personne."],
  ["4", "Pour plusieurs codes, les séparer par un point-virgule et les trier alphabétiquement."],
  ["5", "Une fois les deux feuilles remplies, consulter la feuille Comparaison."],
];
instructions.getRange("A9:B13").values = steps;
instructions.getRange("A9:A13").format = { fill: paleBlue, font: { bold: true }, horizontalAlignment: "center" };
instructions.getRange("B9:B13").format = { wrapText: true };
instructions.getRange("A15:H15").merge();
instructions.getRange("A15").values = [["Important"]];
instructions.getRange("A15:H15").format = { fill: "#B54708", font: { bold: true, color: "#FFFFFF" } };
instructions.getRange("A16:H18").merge();
instructions.getRange("A16").values = [[
  "Une divergence n’est pas une faute. Elle sert à repérer une définition trop vague, une chronologie difficile à interpréter ou une information insuffisamment sourcée.",
]];
instructions.getRange("A16:H18").format = { fill: paleYellow, wrapText: true, verticalAlignment: "center" };
instructions.getRange("A1:H18").format.font = { name: "Aptos", color: "#1D2939" };
instructions.getRange("A1:H2").format.font = { name: "Aptos Display", bold: true, color: "#FFFFFF", size: 18 };
instructions.getRange("A:A").format.columnWidth = 8;
instructions.getRange("B:B").format.columnWidth = 58;
instructions.getRange("C:H").format.columnWidth = 12;

const sources = [
  ["Référence", "Type", "Titre", "Source principale", "Source actuelle éventuelle", "Point de difficulté"],
  ["IA00060938", "Simple", "Centrale hydroélectrique de Rabodanges", "https://pop.culture.gouv.fr/notice/merimee/IA00060938", "https://www.edf.fr/barrage-rabodanges", "Activité unique"],
  ["IA00060915", "Simple", "Filature de la Planchette", "https://pop.culture.gouv.fr/notice/merimee/IA00060915", "", "Activité unique"],
  ["IA00061147", "Simple", "Cartonnerie", "https://pop.culture.gouv.fr/notice/merimee/IA00061147", "", "Activité unique"],
  ["IA00060965", "Ambigu", "Affinerie puis moulin à blé", "https://pop.culture.gouv.fr/notice/merimee/IA00060965", "", "Succession et rapprochements incertains"],
  ["IA00061155", "Ambigu", "Établissements Bohin", "https://pop.culture.gouv.fr/notice/merimee/IA00061155", "https://www.bohin.com/pages/organiser-sa-visite", "Activités complémentaires et usages multiples"],
  ["IA00061060", "Ambigu", "Moulin à papier et grosse forge", "https://pop.culture.gouv.fr/notice/merimee/IA00061060", "", "Cinq phases possibles"],
];
sourceSheet.getRange("A1:F7").values = sources;
sourceSheet.getRange("A1:F1").format = { fill: navy, font: { bold: true, color: "#FFFFFF" }, wrapText: true };
sourceSheet.getRange("A2:F7").format = { wrapText: true, verticalAlignment: "top" };
sourceSheet.getRange("B2:B7").conditionalFormats.add("containsText", { text: "Ambigu", format: { fill: paleYellow, font: { bold: true, color: "#8A3B12" } } });
sourceSheet.freezePanes.freezeRows(1);
sourceSheet.getRange("A:A").format.columnWidth = 15;
sourceSheet.getRange("B:B").format.columnWidth = 10;
sourceSheet.getRange("C:C").format.columnWidth = 30;
sourceSheet.getRange("D:E").format.columnWidth = 42;
sourceSheet.getRange("F:F").format.columnWidth = 34;

const headers = [
  "Personne", "Référence", "Nombre de phases", "Activités (codes)", "Secteurs (codes)",
  "Installations (codes)", "Mode chronologique", "Conservation", "Usages actuels",
  "Accessibilité", "Fiabilité", "Statut protection", "Commentaire",
];
const refs = sources.slice(1).map((row) => row[0]);
function setupPersonSheet(sheet, label) {
  sheet.getRange("A1:M1").values = [headers];
  sheet.getRange("A1:M1").format = { fill: navy, font: { bold: true, color: "#FFFFFF" }, wrapText: true, verticalAlignment: "center" };
  const rows = refs.map((reference) => [label, reference, null, "", "", "", "", "", "", "", "", "", ""]);
  sheet.getRange("A2:M7").values = rows;
  sheet.getRange("C2:M7").format = { fill: paleYellow, wrapText: true, verticalAlignment: "top" };
  sheet.getRange("A2:B7").format = { fill: paleBlue, font: { bold: true } };
  sheet.freezePanes.freezeRows(1);
  sheet.freezePanes.freezeColumns(2);
  sheet.getRange("C2:C7").dataValidation = { rule: { type: "whole", operator: "between", formula1: 1, formula2: 6 } };
  sheet.getRange("G2:G7").dataValidation = { rule: { type: "list", values: ["phase_unique", "successives", "simultanees", "simultanees_complementaires", "simultanees_puis_succession", "incertain"] } };
  sheet.getRange("H2:H7").dataValidation = { rule: { type: "list", values: ["conserve", "degrade", "partiellement_conserve", "vestiges", "ruine", "disparu", "inconnu"] } };
  sheet.getRange("J2:J7").dataValidation = { rule: { type: "list", values: ["visitable", "partiellement_visitable", "visible_espace_public", "prive_visible", "prive_non_visible", "inaccessible", "inconnu"] } };
  sheet.getRange("K2:K7").dataValidation = { rule: { type: "list", values: ["forte", "moyenne", "faible"] } };
  sheet.getRange("L2:L7").dataValidation = { rule: { type: "list", values: ["protege", "inventorie_sans_protection_identifiee", "aucune_protection_identifiee", "inconnu", "a_verifier"] } };
  sheet.getRange("A:A").format.columnWidth = 10;
  sheet.getRange("B:B").format.columnWidth = 16;
  sheet.getRange("C:C").format.columnWidth = 14;
  sheet.getRange("D:F").format.columnWidth = 30;
  sheet.getRange("G:L").format.columnWidth = 23;
  sheet.getRange("M:M").format.columnWidth = 38;
  sheet.getRange("1:1").format.rowHeight = 36;
  sheet.getRange("2:7").format.rowHeight = 30;
}
setupPersonSheet(personA, "A");
setupPersonSheet(personB, "B");

const vocabRows = [
  ["Catégorie", "Code", "Libellé / usage"],
  ["activité", "production_hydroelectricite", "Production hydroélectrique"],
  ["activité", "filature_textile", "Filature textile"],
  ["activité", "fabrication_carton", "Fabrication de carton"],
  ["activité", "affinage_metaux", "Affinage des métaux"],
  ["activité", "mouture_cereales", "Mouture de céréales"],
  ["activité", "fabrication_quincaillerie", "Fabrication de quincaillerie"],
  ["activité", "trefilage_metaux", "Tréfilage des métaux"],
  ["activité", "fabrication_papier", "Fabrication de papier"],
  ["activité", "forgeage", "Forgeage"],
  ["activité", "preparation_tan", "Préparation du tan"],
  ["activité", "transformation_lait", "Transformation du lait"],
  ["secteur", "energie", "Production d'énergie"],
  ["secteur", "textile_habillement_cuir", "Textile, habillement et cuir"],
  ["secteur", "bois_papier_imprimerie", "Bois, papier et imprimerie"],
  ["secteur", "metallurgie_travail_metaux", "Métallurgie et travail des métaux"],
  ["secteur", "agroalimentaire", "Agroalimentaire"],
  ["installation", "centrale_hydroelectrique", "Centrale hydroélectrique"],
  ["installation", "filature", "Filature"],
  ["installation", "cartonnerie", "Cartonnerie"],
  ["installation", "affinerie", "Affinerie"],
  ["installation", "moulin", "Moulin"],
  ["installation", "usine", "Usine"],
  ["installation", "papeterie", "Papeterie"],
  ["installation", "forge", "Forge"],
  ["installation", "fromagerie", "Fromagerie"],
  ["usage", "activite_industrielle", "Activité industrielle actuelle"],
  ["usage", "culture_musee", "Culture ou musée"],
  ["usage", "tourisme_visite", "Tourisme ou visite"],
  ["usage", "logement", "Logement"],
  ["usage", "vacant", "Vacant"],
  ["usage", "sans_usage", "Sans usage"],
  ["usage", "inconnu", "Usage inconnu"],
];
vocab.getRange(`A1:C${vocabRows.length}`).values = vocabRows;
vocab.getRange("A1:C1").format = { fill: navy, font: { bold: true, color: "#FFFFFF" } };
vocab.getRange(`A2:A${vocabRows.length}`).format = { fill: paleBlue, font: { bold: true } };
vocab.freezePanes.freezeRows(1);
vocab.getRange("A:A").format.columnWidth = 16;
vocab.getRange("B:B").format.columnWidth = 38;
vocab.getRange("C:C").format.columnWidth = 38;

const compareHeaders = ["Référence", "Phases", "Activités", "Secteurs", "Installations", "Chronologie", "Conservation", "Usages", "Accessibilité", "Fiabilité", "Protection", "Accord moyen"];
comparison.getRange("A1:L1").values = [compareHeaders];
comparison.getRange("A1:L1").format = { fill: navy, font: { bold: true, color: "#FFFFFF" }, wrapText: true };
comparison.getRange("A2:A7").values = refs.map((reference) => [reference]);
const personColumns = ["C", "D", "E", "F", "G", "H", "I", "J", "K", "L"];
for (let row = 2; row <= 7; row += 1) {
  const formulas = personColumns.map((column) => `=IF(OR('Personne A'!${column}${row}="",'Personne B'!${column}${row}=""),"",IF('Personne A'!${column}${row}='Personne B'!${column}${row},1,0))`);
  comparison.getRange(`B${row}:K${row}`).formulas = [formulas];
  comparison.getRange(`L${row}`).formulas = [[`=IF(COUNT(B${row}:K${row})=0,"",AVERAGE(B${row}:K${row}))`]];
}
comparison.getRange("A9:K9").merge();
comparison.getRange("A9").values = [["Accord global"]];
comparison.getRange("L9").formulas = [["=IF(COUNT(B2:K7)=0,\"\",AVERAGE(B2:K7))"]];
comparison.getRange("A9:L9").format = { fill: paleGreen, font: { bold: true } };
comparison.getRange("B2:K7").format.numberFormat = "0";
comparison.getRange("L2:L9").format.numberFormat = "0.0%";
comparison.getRange("B2:K7").conditionalFormats.addCustom("=AND(B2<>\"\",B2=0)", { fill: "#FDE8E8", font: { bold: true, color: "#B42318" } });
comparison.getRange("B2:K7").conditionalFormats.addCustom("=B2=1", { fill: paleGreen, font: { color: "#067647" } });
comparison.freezePanes.freezeRows(1);
comparison.getRange("A:A").format.columnWidth = 16;
comparison.getRange("B:K").format.columnWidth = 14;
comparison.getRange("L:L").format.columnWidth = 16;

for (const sheet of [sourceSheet, personA, personB, vocab, comparison]) {
  const used = sheet.getUsedRange();
  used.format.font = { name: "Aptos", color: "#1D2939", size: 10 };
  sheet.getRange("1:1").format.font = { name: "Aptos", bold: true, color: "#FFFFFF", size: 10 };
}
instructions.getRange("A4:H4").format.font = { name: "Aptos", bold: true, color: "#FFFFFF", size: 11 };
instructions.getRange("A8:H8").format.font = { name: "Aptos", bold: true, color: "#FFFFFF", size: 11 };
instructions.getRange("A15:H15").format.font = { name: "Aptos", bold: true, color: "#FFFFFF", size: 11 };
sourceSheet.getRange("A1:F1").format.font = { name: "Aptos", bold: true, color: "#FFFFFF", size: 10 };
personA.getRange("A1:M1").format.font = { name: "Aptos", bold: true, color: "#FFFFFF", size: 10 };
personB.getRange("A1:M1").format.font = { name: "Aptos", bold: true, color: "#FFFFFF", size: 10 };
vocab.getRange("A1:C1").format.font = { name: "Aptos", bold: true, color: "#FFFFFF", size: 10 };
comparison.getRange("A1:L1").format.font = { name: "Aptos", bold: true, color: "#FFFFFF", size: 10 };

await fs.mkdir(new URL(".", `file:///${outputPath.replaceAll("\\", "/")}`).pathname, { recursive: true }).catch(() => {});
await fs.mkdir(previewDir, { recursive: true });
for (const sheetName of ["Consignes", "Sources", "Personne A", "Personne B", "Vocabulaires", "Comparaison"]) {
  const preview = await workbook.render({ sheetName, autoCrop: "all", scale: 1, format: "png" });
  await fs.writeFile(`${previewDir}/${sheetName.replaceAll(" ", "_")}.png`, new Uint8Array(await preview.arrayBuffer()));
}
const inspection = await workbook.inspect({ kind: "table", range: "Comparaison!A1:L9", include: "values,formulas", tableMaxRows: 12, tableMaxCols: 14 });
await fs.writeFile(`${previewDir}/inspection.ndjson`, inspection.ndjson, "utf8");
const errors = await workbook.inspect({ kind: "match", searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A", options: { useRegex: true, maxResults: 100 }, summary: "formula errors" });
await fs.writeFile(`${previewDir}/errors.ndjson`, errors.ndjson, "utf8");
const output = await SpreadsheetFile.exportXlsx(workbook);
try {
  await output.save(outputPath);
} catch (error) {
  process.stderr.write(`${error?.stack || error}\n`);
  throw error;
}
