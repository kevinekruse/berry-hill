<div>
  <h2>All Scores Summary</h2>
</div>

```js
// load filtered rounds CSV (no blinds)
const all = await FileAttachment("data/BerryHillScores_Rounds_NoBlind.csv").csv({typed: true})
```

```js
function isValidNumber(v) { return Number.isFinite(v) }

function isBlindPlayer(name) {
  if (!name) return false
  const s = String(name).toUpperCase()
  return s.includes('BLIND') || s.includes('\u0392LIND')
}

// collect gross scores for individual rounds (skip team aggregates and blinds)
const grossValues = []
for (const r of all) {
  const rowType = (r.row_type || r.row || '').toString().toLowerCase()
  if (rowType !== 'round') continue
  const display = r.display_name || r.display || ''
  if (isBlindPlayer(display)) continue
  const gross = (r.gross_score === undefined || r.gross_score === null) ? NaN : Number(r.gross_score)
  if (!isValidNumber(gross)) continue
  grossValues.push(gross)
}

grossValues.sort((a,b)=>a-b)
```

```js
import * as Plot from "@observablehq/plot"
import {bin, ticks} from "d3-array"

const Observable_Brown = "#9C6B4E"
const Observable_Light_Blue = "#97BBF5"
const Observable_Gray = "#9498A0"

// make integer-width bins (width = 1) across the observed gross score range
const xMinInt = Math.floor(Math.min(...grossValues))
const xMaxInt = Math.ceil(Math.max(...grossValues))
const thresholds = []
for (let t = xMinInt; t <= xMaxInt + 1; t++) thresholds.push(t)
const bins = bin().thresholds(thresholds)(grossValues)
const binsData = bins.map(b => ({x0: b.x0, x1: b.x1, mid: (b.x0 + b.x1) / 2, count: b.length}))

if (grossValues.length === 0 || binsData.length === 0) {
  display(htl.html`<div style="color:var(--theme-foreground-muted);">No histogram data available (${grossValues.length} values)</div>`)
} else {
  // compute horizontal grid tick positions only
  const yMin = 0
  const yMax = Math.max(...binsData.map(d => d.count))
  const yTicks = ticks(yMin, yMax, 6)

  // x-axis labels: integer ticks across observed gross range
  const xTicks = []
  for (let v = xMinInt; v <= xMaxInt; v++) xTicks.push(v)

  const plot = Plot.plot({
  height: 360,
  marginTop: 8,
  marginLeft: 60,
  style: {border: `2px solid ${Observable_Gray}`},
    x: {label: null, tickValues: xTicks, tickFormat: (d,i) => { if (typeof i === 'number' && xTicks[i] !== undefined && Number.isFinite(xTicks[i])) return String(xTicks[i]); const n = Number(d); return Number.isFinite(n) ? String(Math.round(n)) : '' }, tickSize: 6, tickPadding: 4},
    y: {label: "Count"},
    marks: [
      // horizontal gridlines only
      Plot.ruleY(yTicks, {stroke: "#000", strokeWidth: 1, strokeOpacity: 0.12}),
      // bars (integer-width bins)
      Plot.barY(binsData, {x: d => [d.x0, d.x1], y: "count", fill: Observable_Brown})
    ]
  })
  // compute summary: total rounds and earliest date from the filtered rows
  let earliestTs = Infinity
  for (const r of all) {
    const rowType = (r.row_type || r.row || '').toString().toLowerCase()
    if (rowType !== 'round') continue
    const displayName = r.display_name || r.display || ''
    if (isBlindPlayer(displayName)) continue
    const d = r.date
    if (!d) continue
    const ts = Number(new Date(d))
    if (Number.isFinite(ts)) earliestTs = Math.min(earliestTs, ts)
  }
  const earliestDateStr = earliestTs === Infinity ? 'N/A' : new Date(earliestTs).toISOString().slice(0,10)
  const totalRounds = grossValues.length

  display(htl.html`<div style="margin-bottom:6px;color:#000000;">${totalRounds} rounds played since ${earliestDateStr}</div>`)
  const grossAvg = grossValues.length ? (grossValues.reduce((s,v)=>s+v,0) / grossValues.length) : NaN
  const grossAvgStr = Number.isFinite(grossAvg) ? grossAvg.toFixed(1) : 'N/A'
  display(htl.html`<div style="margin-bottom:10px;color:#000000;">Gross score average: ${grossAvgStr}</div>`)

  display(htl.html`<div style="display:flex;justify-content:flex-start;width:100%"><div style="display:inline-block;text-align:center"><div style="font-weight:700;font-size:18px;margin-bottom:6px">Gross Scores</div>${plot}</div></div>`)

  // --- Net Scores histogram (below Gross Scores)
  const netValues = []
  for (const r of all) {
    const rowType = (r.row_type || r.row || '').toString().toLowerCase()
    if (rowType !== 'round') continue
    const display = r.display_name || r.display || ''
    if (isBlindPlayer(display)) continue
    const net = (r.net_score === undefined || r.net_score === null) ? NaN : Number(r.net_score)
    if (!isValidNumber(net)) continue
    netValues.push(net)
  }
  netValues.sort((a,b)=>a-b)

    if (netValues.length > 0) {
    const xMinNet = Math.floor(Math.min(...netValues))
    const xMaxNet = Math.ceil(Math.max(...netValues))
    const thresholdsNet = []
    for (let t = xMinNet; t <= xMaxNet + 1; t++) thresholdsNet.push(t)
    // integer tick values for net plot (one per integer in observed range)
    const xTicksNet = []
    for (let v = xMinNet; v <= xMaxNet; v++) xTicksNet.push(v)
    const binsNet = bin().thresholds(thresholdsNet)(netValues)
    const binsDataNet = binsNet.map(b => ({x0: b.x0, x1: b.x1, mid: (b.x0 + b.x1) / 2, count: b.length}))

    const yMaxNet = Math.max(...binsDataNet.map(d => d.count))
    const yTicksNet = ticks(0, yMaxNet, 6)

    // (debug output removed)

    const netPlot = Plot.plot({
      height: 320,
      marginTop: 8,
      marginLeft: 60,
      style: {border: `2px solid ${Observable_Gray}`},
      x: {label: null, tickValues: xTicksNet, tickFormat: (d,i) => { if (typeof i === 'number' && xTicksNet[i] !== undefined) return String(xTicksNet[i]); const n = Number(d); return Number.isFinite(n) ? String(Math.round(n)) : '' }, tickSize: 6, tickPadding: 4},
      y: {label: "Count"},
      marks: [
        Plot.ruleY(yTicksNet, {stroke: "#000", strokeWidth: 1, strokeOpacity: 0.12}),
        Plot.barY(binsDataNet, {x: d => [d.x0, d.x1], y: "count", fill: Observable_Light_Blue})
      ]
    })

    display(htl.html`<div style="display:flex;justify-content:flex-start;width:100%"><div style="display:inline-block;text-align:center;margin-top:18px"><div style="font-weight:700;font-size:18px;margin-bottom:6px">Net Scores</div>${netPlot}</div></div>`)
  }
}
```

<style>
.hero { display: flex; flex-direction: column; align-items: center; font-family: var(--sans-serif); margin: 2rem 0 3rem; text-wrap: balance; text-align: center; }
.hero h2 { margin: 0; max-width: 34em; font-size: 20px; font-weight: 500; color: var(--theme-foreground-muted); }
</style>
