<div>
  <h2>All Team Scores (without Blinds)</h2>
</div>

```js
// load full CSV
const all = await FileAttachment("data/BerryHillScores_All_Latest.csv").csv({typed: true})
```

```js
// aggregate team net score by week and team across all seasons
function parseYear(dateStr) {
  if (!dateStr) return NaN
  const d = new Date(dateStr)
  if (Number.isNaN(d.getTime())) return NaN
  return d.getFullYear()
}

function isValidNumber(v) { return Number.isFinite(v) }

function isBlindPlayer(name) {
  if (!name) return false
  const s = String(name).toUpperCase()
  return s.includes('BLIND') || s.includes('\u0392LIND')
}

const map = new Map()
for (const r of all) {
  const dateStr = r.date || r.score_date || ''
  const year = parseYear(String(dateStr))
  // skip bad placeholder dates (e.g., 1900)
  if (year === 1900) continue

  const week = Number(r.week_num)
  const team = Number(r.team_num)
  const net = (r.net_score === undefined || r.net_score === null) ? NaN : Number(r.net_score)

  // skip rows missing required numeric values
  if (!isValidNumber(week) || !isValidNumber(team) || !isValidNumber(net)) continue

  const season = Number(r.season_year) || NaN
  const key = `${season}-${week}-${team}`
  if (!map.has(key)) {
    const date = (dateStr && String(dateStr).length >= 10) ? String(dateStr).substring(0,10) : ''
    map.set(key, {date: date, week: week, team: team, net_sum: 0, gross_sum: 0, count: 0, has_blind: false})
  }
  const entry = map.get(key)
  entry.net_sum += net
  const gross = (r.gross_score === undefined || r.gross_score === null) ? NaN : Number(r.gross_score)
  if (Number.isFinite(gross)) entry.gross_sum += gross
  entry.count += 1
  // mark if any member is a blind placeholder
  const display = r.display_name || r.display || ''
  if (isBlindPlayer(display)) entry.has_blind = true
}

const team_rows = Array.from(map.values()).map(e => ({
  date: e.date,
  week: e.week,
  team: e.team,
  team_gross: e.gross_sum,
  team_net: e.net_sum,
  has_blind: e.has_blind || false,
  team_net_display: e.has_blind ? htl.html`<span style="color:#c00;font-weight:600">${Number(e.net_sum).toFixed(1)}</span>` : Number(e.net_sum).toFixed(1)
}))

// filter out small team nets and any teams that include a BLIND player
const filtered_team_rows = team_rows.filter(d => {
  const v = (d.team_net === undefined || d.team_net === null) ? NaN : Number(d.team_net)
  return Number.isFinite(v) && v >= 5 && !d.has_blind
})

// diagnostics: rows for a specific date (example)
const diagnostic_date = '2021-05-11'
const rows_for_diagnostic_date = filtered_team_rows.filter(d => d.date && d.date.startsWith(diagnostic_date))
```

```js
Inputs.table(filtered_team_rows, {
  columns: ["date", "week", "team", "team_gross", "team_net_display"],
  header: {
    date: "Date",
    week: "Week",
    team: "Team",
    team_gross: htl.html`<div style="text-align:center">Team Gross Score</div>`,
    team_net_display: htl.html`<div style="white-space: pre-wrap; text-align:center">${"Team\nNet Score".toLocaleString("en")}`
  },
  sort: "team_net",
  reverse: false, // ascending: lowest at top
  rows: Math.max(filtered_team_rows.length, 20),
  layout: "auto",
  format: {
    team_gross: d => (d === undefined || d === null ? '' : Number(d).toFixed(1)),
    team_net_display: d => d
  },
  align: {
    date: "center",
    week: "center",
    team: "center",
    team_gross: "center",
    team_net_display: "center"
  }
})
```

<style>
.hero { display: flex; flex-direction: column; align-items: center; font-family: var(--sans-serif); margin: 4rem 0 8rem; text-wrap: balance; text-align: center; }
.hero h2 { margin: 0; max-width: 34em; font-size: 20px; font-weight: 500; color: var(--theme-foreground-muted); }
</style>
