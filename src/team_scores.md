<div>
  <h2>2026 Team Scores</h2>
</div>

```js
const all = FileAttachment("data/BerryHillScores_All_Latest.csv").csv({typed: true})
```

```js
// filter to 2026 rows
const rows2026 = all.filter(d => Number(d.season_year) === 2026)

// aggregate team net score by week and team
const map = new Map()
for (const r of rows2026) {
  const week = r.week_num
  const team = r.team_num
  const net = (r.net_score === undefined || r.net_score === null) ? NaN : Number(r.net_score)
  if (Number.isFinite(net) === false) continue
  const key = `${week}-${team}`
  if (!map.has(key)) {
    const date = (r.date && String(r.date).length >= 10) ? String(r.date).substring(0,10) : ''
    map.set(key, {date: date, week: week, team: team, net_sum: 0, count: 0})
  }
  const entry = map.get(key)
  entry.net_sum += net
  entry.count += 1
}

const team_rows = Array.from(map.values()).map(e => ({
  date: e.date,
  week: e.week,
  team: e.team,
  team_net: e.net_sum
}))

// filter out small team nets
const filtered_team_rows = team_rows.filter(d => {
  const v = (d.team_net === undefined || d.team_net === null) ? NaN : Number(d.team_net)
  return Number.isFinite(v) && v >= 5
})
```

```js
Inputs.table(filtered_team_rows, {
  columns: ["date", "week", "team", "team_net"],
  header: {
    date: "Date",
    week: "Week",
    team: "Team",
    team_net: htl.html`<div style="white-space: pre-wrap;">${"Team\nNet Score".toLocaleString("en")}`
  },
  sort: "team_net",
  reverse: false, // ascending: lowest at top
  rows: Math.max(filtered_team_rows.length, 20),
  layout: "auto",
  format: {
    team_net: d => (d === undefined || d === null ? '' : Number(d).toFixed(1))
  },
  align: {
    date: "center",
    week: "center",
    team: "center",
    team_net: "center"
  }
})
```

```js
import * as Plot from "@observablehq/plot"
import {bin} from "d3-array"

// histogram of team_net values (bin with d3 and draw bars with Plot)
const values = filtered_team_rows.map(d => (d.team_net === undefined || d.team_net === null) ? NaN : Number(d.team_net)).filter(v => Number.isFinite(v))
const bins = bin().thresholds(20)(values)
const binsData = bins.map(b => ({
  x0: b.x0,
  x1: b.x1,
  mid: (b.x0 + b.x1) / 2,
  count: b.length
}))

let hist
if (values.length === 0 || binsData.length === 0) {
  hist = htl.html`<div style="color:var(--theme-foreground-muted);">No histogram data available (${values.length} values)</div>`
} else {
  hist = Plot.plot({
  height: 320,
  marginLeft: 60,
  x: {label: "Team Net Score"},
  y: {label: "Count"},
  marks: [
    Plot.barY(binsData, {x: d => [d.x0, d.x1], y: "count", fill: "#027148"}),
    Plot.ruleX([0], {stroke: "#000", strokeWidth: 1, strokeDasharray: "4 2"})
  ]
  })
}

hist
```

<style>
.hero { display: flex; flex-direction: column; align-items: center; font-family: var(--sans-serif); margin: 4rem 0 8rem; text-wrap: balance; text-align: center; }
.hero h2 { margin: 0; max-width: 34em; font-size: 20px; font-weight: 500; color: var(--theme-foreground-muted); }
</style>
