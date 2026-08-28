# The report

The artifact `what-it-took` produces: a single self-contained HTML file, opened
from disk, thrown away once the decisions in it are taken or dismissed.

## Where it lands

`/tmp/what-it-took/<repo>-<session-id-first-8>-<genid>.html`

- The session id keeps the report tied to the session it diagnoses.
- `<genid>` is a short random id baked at generation time (`openssl rand -hex 2`),
  so every run is a new file and a fresh read.

## Written in plain Spanish, for someone who has read none of this

The reader is a developer who wants to know why their session got expensive.
They have not read this skill, the aggregator, or any vocabulary invented along
the way. Write as you would explain it out loud to a colleague.

The words below are the analysis's working vocabulary, and they stay in the
analysis. On the page, use the plain phrase:

| Working word | On the page |
| --- | --- |
| toll / peaje | lo que se carga solo, antes de empezar a trabajar |
| resident / footprint | lo que ocupa la ventana ahora mismo |
| turn | paso — explica una vez que un paso es cada ida y vuelta con el modelo |
| payload | lo que devolvieron las herramientas |
| locate / comprehend | buscar dónde está algo / leer qué hace |
| reprocess | material que entró dos veces |
| lost in the middle | material enterrado: entró hace mucho y ha quedado lejos del final |
| ground / behaviour | arreglar el proyecto / trabajar distinto |

**Every figure says what it is made of.** A number the reader cannot decompose
is a number they cannot act on: `36.773 de instrucciones que se cargan siempre`
means nothing until it reads `de los cuales ~3.700 son 22 servidores MCP que
este repo nunca usa`. This applies to the headline figures, to every segment of
the chart, and to every saving in the decisions block.

## Three blocks and a closing

**1. La foto.** What thirty seconds buys. Three figures, each with the sentence
that makes it mean something: what the window holds now, how much of it was
already in before the session produced anything, and how much loads on its own
on every single step.

The visual is the window as one stacked bar by origin. Its legend is where most
of the value sits, so give each segment its size **and what is inside it** —
"instrucciones que se cargan siempre (36.773): descripciones de skills, 22
servidores MCP conectados, CLAUDE.md del repo". A legend of bare labels leaves
the reader looking at coloured boxes.

Two honesty markers belong here, in plain words: how much of the window the
breakdown actually accounts for, and — when a compaction was detected — that
figures from before the cut no longer compare.

**2. De dónde salió.** The evidence, without which the decisions are just opinion.

Each zoomed stretch told as what it was — "doce búsquedas de `authorizer` hasta
encontrarlo en un directorio que no lleva ese nombre" — followed by its
cheaper-way answer: the document that would have made the loading unnecessary,
named with its exact home.

Then **material enterrado**, which answers a different question from all the
above: not how much came in, but how far the important things have drifted from
the end of the window. Name the documents and their distance in plain terms —
"la spec del ticket entró hace 131.000 tokens, el 77% de la ventana atrás: los
últimos cincuenta pasos se trabajaron con ella muy lejos". Include what was
edited long after it was read, and anything that had to be brought back in.

Then the instruction files that were paid for whole and used in part: for each
one, the sections that never bore on the work and what they cost, summed. Name
the document, the sections and the total, and say how many steps carried them.
This is the figure that prices loading the whole context up front.

Close the block with the searched terms you judged to be real domain words,
presented as what they are: **el vocabulario del repo que no está escrito en
ninguna parte**, and the ready-made input for a `grill-me-with-docs` session. A
regex fragment listed as vocabulary costs the report its credibility.

**3. Decisiones.** Two lists, kept apart because they are different kinds of
decision:

- **Arreglar el proyecto** — se hace una vez y sirve para todas las sesiones que
  vengan.
- **Trabajar distinto** — gratis desde la próxima sesión, y se olvida si no se
  escribe en alguna instrucción.

Two columns each: what to do, and how much window it would have saved. Where a
skill genuinely does that work, name it inside the sentence — "el glosario lo
escribes con `/grill-me-with-docs`" — rather than as a column of its own.

Every saving is visibly an estimate, and the list is ordered by it, descending.

When the session was healthy, this block says so in one sentence and lists
nothing. An empty prescription is a valid result and reads as confidence.

**Cierre: qué no se miró.** The stretches left outside the zoom budget and their
size, plus anything the aggregator warned about. This is what keeps the report
from reading as total coverage when it is a sample.

## Visuals earn their place

Every chart, table or badge replaces a paragraph that would otherwise have to be
written. That is the whole rule; picking what fits *this* session is the work.
The stacked bar in block 1 earns it. A second chart usually does not.

Everything renders offline from a `file://` page: inline SVG, native CSS, no
external library, font or request.

## Built to be read

- A reading measure, generous line height, real typographic hierarchy.
- Light and dark, following the system.
- Wide content (tables, code) scrolls inside its own container; the page never
  scrolls sideways.
- Figures are right-aligned and thousands-separated, so columns compare by eye.
