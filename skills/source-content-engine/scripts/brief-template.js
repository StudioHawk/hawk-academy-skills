/**
 * brief-template.js
 * Reusable document template for SEO Content Briefs (workshop version)
 *
 * Usage in a brief script:
 *   const docx = require('./node_modules/docx');
 *   const { buildBrief, p, bl } = require('./brief-template')(docx);
 *
 * Then call buildBrief(config) -- see CONFIG SCHEMA below.
 *
 * config.clientName controls the client name in the Details table.
 * config.refDocs (optional) adds reference document links.
 *
 * Visual format:
 *   Header cells:  #46b5ef (Picton Blue), Archivo Bold, white text
 *   Label cells:   #f3f3f3, Archivo Light
 *   Body cells:    white, Archivo
 *   Borders:       #BFBFBF, size 2, single
 *   Title:         Lato Black, 22pt (44 half-points), centred
 *
 * This workshop version does NOT render a logo above the title.
 */

module.exports = function createTemplate(docx) {
  const {
    Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
    AlignmentType, BorderStyle, WidthType, ShadingType, VerticalAlign,
    LevelFormat, ExternalHyperlink
  } = docx;

  // -- Palette ---------------------------------------------------------------
  const HEADER_BG  = "46b5ef"; // Picton Blue -- section header rows
  const HEADER_TXT = "ffffff";
  const ROW_BG     = "f3f3f3"; // Light grey -- label cells and keyword data rows
  const WHITE      = "ffffff";
  const BORDER_CLR = "BFBFBF"; // Light grey -- thin borders
  const BORDER_SZ  = 2;        // Thin border (2 = 0.25pt in docx units)

  // -- Layout constants (DXA) ------------------------------------------------
  const PAGE_W    = 9360;
  const COL_LBL   = 2200;
  const COL_BODY  = 7160;
  const COL_KW_L  = 2200; // keyword label column
  const COL_KW_M  = 5060; // keyword text column
  const COL_KW_R  = 2100; // keyword volume column
  const COL_SD    = 1800; // section design column
  const COL_CD    = 5360; // content direction column
  const COL_NFC   = 2200; // notes from client column

  // -- Border definitions ----------------------------------------------------
  const b = { style: BorderStyle.SINGLE, size: BORDER_SZ, color: BORDER_CLR };
  const borders = { top: b, bottom: b, left: b, right: b };

  // -- Cell builders ---------------------------------------------------------

  /** Blue header cell (section banner) -- white bold Archivo text */
  function hCell(text, w, opts = {}) {
    return new TableCell({
      borders,
      width: { size: w, type: WidthType.DXA },
      shading: { fill: HEADER_BG, type: ShadingType.CLEAR },
      margins: { top: 80, bottom: 80, left: 120, right: 120 },
      verticalAlign: VerticalAlign.CENTER,
      ...(opts.colSpan ? { columnSpan: opts.colSpan } : {}),
      children: [new Paragraph({
        alignment: opts.align || AlignmentType.LEFT,
        children: [new TextRun({ text, bold: true, color: HEADER_TXT, size: 20, font: "Archivo" })]
      })]
    });
  }

  /** Grey label cell -- Archivo Light */
  function lbl(text, w) {
    return new TableCell({
      borders,
      width: { size: w, type: WidthType.DXA },
      shading: { fill: ROW_BG, type: ShadingType.CLEAR },
      margins: { top: 80, bottom: 80, left: 120, right: 120 },
      verticalAlign: VerticalAlign.TOP,
      children: [new Paragraph({
        children: [new TextRun({ text, size: 20, font: "Archivo Light" })]
      })]
    });
  }

  /** Standard content cell -- Archivo */
  function cell(children, w, opts = {}) {
    return new TableCell({
      borders,
      width: { size: w, type: WidthType.DXA },
      shading: { fill: opts.bg || WHITE, type: ShadingType.CLEAR },
      margins: { top: 80, bottom: 80, left: 120, right: 120 },
      verticalAlign: VerticalAlign.TOP,
      ...(opts.colSpan ? { columnSpan: opts.colSpan } : {}),
      children
    });
  }

  // -- Paragraph builders ----------------------------------------------------

  /** Plain text paragraph */
  function p(text, opts = {}) {
    return new Paragraph({
      children: [new TextRun({
        text,
        size:    opts.size    || 20,
        font:    opts.font    || "Archivo",
        bold:    opts.bold    || false,
        color:   opts.color   || "000000",
        italics: opts.italic  || false,
      })],
      spacing: { before: opts.before || 40, after: opts.after || 40 },
      alignment: opts.align || AlignmentType.LEFT,
    });
  }

  /** Hyperlink paragraph */
  function linkP(label, url) {
    return new Paragraph({
      spacing: { before: 30, after: 30 },
      children: [
        new ExternalHyperlink({
          link: url,
          children: [new TextRun({ text: label, size: 20, font: "Archivo", color: "0563C1", underline: {} })]
        })
      ]
    });
  }

  /** Bullet paragraph */
  function bl(text, opts = {}) {
    return new Paragraph({
      numbering: { reference: "bullets", level: 0 },
      children: [new TextRun({
        text,
        size:    20,
        font:    "Archivo",
        bold:    opts.bold   || false,
        italics: opts.italic || false,
      })],
      spacing: { before: 20, after: 20 },
    });
  }

  // -- Section builders ------------------------------------------------------

  /** Standard two-column data row: grey label + white content */
  function twoColRow(labelText, contentChildren) {
    return new TableRow({
      children: [lbl(labelText, COL_LBL), cell(contentChildren, COL_BODY)]
    });
  }

  /** Empty spacer paragraph between tables */
  function spacer() {
    return new Paragraph({ children: [], spacing: { before: 120, after: 0 } });
  }

  // -- CONFIG SCHEMA ---------------------------------------------------------
  //
  // buildBrief(config) expects:
  //
  //  config.filename      {string}  Output .docx filename
  //  config.clientName    {string}  Client name
  //  config.topic         {string}  Topic/Category line
  //  config.refDocs       {Array}   Optional -- [{ label, url }] reference document links
  //
  //  SECTION 1 -- Brand and Context
  //  config.objective     {Paragraph[]}
  //  config.angle         {Paragraph[]}
  //  config.voiceAndStyle {Paragraph[]}
  //
  //  SECTION 2 -- Target Audience
  //  config.audience      {Paragraph[]}
  //  config.searchIntent  {Paragraph[]}
  //
  //  SECTION 3 -- Competitors
  //  config.contentReqs   {Paragraph[]}
  //  config.competitorUrls {Paragraph[]}
  //
  //  SECTION 4 -- Internal Linking
  //  config.linksOut      {Paragraph[]}
  //  config.linksIn       {Paragraph[]}
  //
  //  SECTION 5 -- Keywords
  //  config.primaryKw     { keyword: string, volume: string }
  //  config.secondaryKws  [{ keyword: string, volume: string }, ...]
  //
  //  SECTION 6 -- Page Metadata
  //  config.url           {string}
  //  config.titleTag      {string}
  //  config.metaDesc      {string}
  //  config.wordCount     {string}
  //
  //  SECTION 7 -- Section Design
  //  config.sections      Array of:
  //    { designNotes: Paragraph[], contentDirection: Paragraph[] }
  //

  function buildBrief(config) {
    const fs = require("fs");

    // Build Details table rows
    const detailRows = [
      new TableRow({ children: [hCell("Details", PAGE_W, { colSpan: 2, align: AlignmentType.CENTER })] }),
      new TableRow({ children: [lbl("Client Name:", COL_LBL), cell([p(config.clientName)], COL_BODY)] }),
      new TableRow({ children: [lbl("Topic/Category", COL_LBL), cell([p(config.topic, { italic: true })], COL_BODY)] }),
    ];

    // Add reference documents row if provided
    if (config.refDocs && config.refDocs.length > 0) {
      detailRows.push(new TableRow({ children: [
        lbl("Reference Documents", COL_LBL),
        cell(config.refDocs.map(d => linkP(d.label, d.url)), COL_BODY)
      ]}));
    }

    const doc = new Document({
      numbering: {
        config: [{
          reference: "bullets",
          levels: [{
            level: 0,
            format: LevelFormat.BULLET,
            text: "•",
            alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 540, hanging: 260 } } }
          }]
        }]
      },
      sections: [{
        properties: {
          page: {
            size:   { width: 12240, height: 15840 },
            margin: { top: 1080, right: 1080, bottom: 1080, left: 1080 }
          }
        },
        children: [

          // -- Document title (centred, Lato Black 22pt) ---------------------
          new Paragraph({
            alignment: AlignmentType.CENTER,
            spacing: { before: 0, after: 200 },
            children: [new TextRun({
              text: "VISUAL SEO CONTENT BRIEF",
              bold: true,
              size: 44,
              font: "Lato Black",
            })]
          }),

          // -- Table 1: Details ----------------------------------------------
          new Table({
            width: { size: PAGE_W, type: WidthType.DXA },
            columnWidths: [COL_LBL, COL_BODY],
            rows: detailRows
          }),

          spacer(),

          // -- Table 2: Brand and Context ------------------------------------
          new Table({
            width: { size: PAGE_W, type: WidthType.DXA },
            columnWidths: [COL_LBL, COL_BODY],
            rows: [
              new TableRow({ children: [hCell("Brand and Context", PAGE_W, { colSpan: 2, align: AlignmentType.CENTER })] }),
              twoColRow("Objective of the article", config.objective),
              twoColRow("Our angle",                config.angle),
              twoColRow("Voice and Style",          config.voiceAndStyle),
            ]
          }),

          spacer(),

          // -- Table 3a: Target Audience -------------------------------------
          new Table({
            width: { size: PAGE_W, type: WidthType.DXA },
            columnWidths: [COL_LBL, COL_BODY],
            rows: [
              new TableRow({ children: [hCell("Target Audience", PAGE_W, { colSpan: 2, align: AlignmentType.CENTER })] }),
              twoColRow("Who is the intended audience?",         config.audience),
              twoColRow("What solution are they searching for?", config.searchIntent),
            ]
          }),

          spacer(),

          // -- Table 3b: Competitors -----------------------------------------
          new Table({
            width: { size: PAGE_W, type: WidthType.DXA },
            columnWidths: [COL_LBL, COL_BODY],
            rows: [
              new TableRow({ children: [hCell("Competitors", PAGE_W, { colSpan: 2, align: AlignmentType.CENTER })] }),
              twoColRow("What does the content need to include to outrank competitors?", config.contentReqs),
              twoColRow("Competitor articles", config.competitorUrls),
            ]
          }),

          spacer(),

          // -- Table 3c: Internal Linking ------------------------------------
          new Table({
            width: { size: PAGE_W, type: WidthType.DXA },
            columnWidths: [COL_LBL, COL_BODY],
            rows: [
              new TableRow({ children: [hCell("Internal linking", PAGE_W, { colSpan: 2, align: AlignmentType.CENTER })] }),
              twoColRow("What internal URLs can this content link to?", config.linksOut),
              twoColRow("What internal URLs can link to this content?", config.linksIn),
            ]
          }),

          spacer(),

          // -- Table 4: Keyword Research -------------------------------------
          new Table({
            width: { size: PAGE_W, type: WidthType.DXA },
            columnWidths: [COL_KW_L, COL_KW_M, COL_KW_R],
            rows: [
              new TableRow({ children: [
                hCell("", COL_KW_L),
                hCell("Keyword Research", COL_KW_M),
                hCell("Search volume", COL_KW_R),
              ]}),
              new TableRow({ children: [
                cell([p("Primary Target keyword", { bold: false })], COL_KW_L, { bg: ROW_BG }),
                cell([p(config.primaryKw.keyword)],                  COL_KW_M, { bg: ROW_BG }),
                cell([p(config.primaryKw.volume)],                   COL_KW_R, { bg: ROW_BG }),
              ]}),
              ...config.secondaryKws.map((kw, i) => new TableRow({ children: [
                i === 0
                  ? cell([p("Secondary Keywords")], COL_KW_L, { bg: ROW_BG })
                  : cell([p("")],                   COL_KW_L, { bg: ROW_BG }),
                cell([p(kw.keyword)], COL_KW_M, { bg: ROW_BG }),
                cell([p(kw.volume)],  COL_KW_R, { bg: ROW_BG }),
              ]})),
            ]
          }),

          spacer(),

          // -- Table 5: Page Metadata ----------------------------------------
          new Table({
            width: { size: PAGE_W, type: WidthType.DXA },
            columnWidths: [COL_LBL, COL_BODY],
            rows: [
              new TableRow({ children: [lbl("URL:", COL_LBL),                          cell([p(config.url)],      COL_BODY)] }),
              new TableRow({ children: [lbl("Title Tag with primary keyword", COL_LBL), cell([p(config.titleTag)], COL_BODY)] }),
              new TableRow({ children: [lbl("Meta description", COL_LBL),              cell([p(config.metaDesc)], COL_BODY)] }),
              new TableRow({ children: [lbl("Word count", COL_LBL),                    cell([p(config.wordCount, { italic: true })], COL_BODY)] }),
            ]
          }),

          spacer(),

          // -- Table 6: Section Design ---------------------------------------
          new Table({
            width: { size: PAGE_W, type: WidthType.DXA },
            columnWidths: [COL_SD, COL_CD, COL_NFC],
            rows: [
              new TableRow({ children: [
                hCell("SECTION DESIGN",    COL_SD),
                hCell("CONTENT DIRECTION", COL_CD),
                hCell("NOTES FROM CLIENT", COL_NFC),
              ]}),
              ...config.sections.map(s => new TableRow({ children: [
                cell(s.designNotes || [p("")],  COL_SD),
                cell(s.contentDirection,        COL_CD),
                cell([p("")],                   COL_NFC),
              ]})),
            ]
          }),

        ] // end children
      }] // end sections
    });

    return Packer.toBuffer(doc).then(buffer => {
      fs.writeFileSync(config.filename, buffer);
      console.log("Done: " + config.filename);
    });
  }

  // -- Public API ------------------------------------------------------------
  return {
    buildBrief,
    p, bl, linkP, hCell, lbl, cell, spacer,
    HEADER_BG, ROW_BG, WHITE, BORDER_CLR, PAGE_W,
    COL_LBL, COL_BODY, COL_SD, COL_CD, COL_NFC,
  };
};
