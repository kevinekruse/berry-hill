<div>
  <h2>All Time Records</h2>
</div>

```js
// load CSV (await required so `all` is the parsed array)
const all = await FileAttachment("data/BerryHillScores_All_Latest.csv").csv({typed: true})
```

```js
// helper to normalize date string
const shortDate = d => (d && String(d.date).length >= 10) ? String(d.date).substring(0,10) : String(d.date || "")

// exclude sentinel values and ignore scores below 1
const isValidScore = v => Number.isFinite(v) && v >= 1 && v < 99000

// helper to detect BLIND/placeholder players (common variants)
const isBlindPlayer = name => {
  if (!name) return false
  const s = String(name).toUpperCase()
  return s.includes('BLIND') || s.includes('\u0392LIND') || s.includes('\u0392LIND'.toUpperCase())
}

// Diagnostic: counts and sample rows to help debug missing data in the built page
const totalRows = all.length
const sampleRows = all.slice(0,6).map(d => ({date: d.date, display_name: d.display_name, gross_score: d.gross_score, net_score: d.net_score, team_num: d.team_num}))
```

```js
htl.html`<div style="color:var(--theme-foreground-muted);">Rows: ${totalRows}&nbsp;—&nbsp;Sample: ${JSON.stringify(sampleRows)}</div>`

```

```js
// Lowest gross score (may be ties) — exclude BLIND/placeholder players
const grossRows = all.filter(d => isValidScore(Number(d.gross_score)) && !isBlindPlayer(d.display_name))
let lowestGrossRecords = []
if (grossRows.length > 0) {
  const minGross = Math.min(...grossRows.map(d => Number(d.gross_score)))
  lowestGrossRecords = grossRows.filter(d => Number(d.gross_score) === minGross).map(d => ({
    date: shortDate(d),
    player: d.display_name || d.player || "",
    gross: Number(d.gross_score)
  }))
}

// Lowest net score (may be ties) — exclude BLIND/placeholder players
const netRows = all.filter(d => isValidScore(Number(d.net_score)) && !isBlindPlayer(d.display_name))
let lowestNetRecords = []
if (netRows.length > 0) {
  const minNet = Math.min(...netRows.map(d => Number(d.net_score)))
  lowestNetRecords = netRows.filter(d => Number(d.net_score) === minNet).map(d => ({
    date: shortDate(d),
    player: d.display_name || d.player || "",
    net: Number(d.net_score)
  }))
}

// Lowest team net: aggregate per season-week-team (same approach as Team Scores page)
const teamMap = new Map()
for (const r of all) {
  // skip BLIND/placeholder players and invalid nets
  if (isBlindPlayer(r.display_name)) continue
  const net = (r.net_score === undefined || r.net_score === null) ? NaN : Number(r.net_score)
  if (!isValidScore(net)) continue
  const season = r.season_year || ''
  const week = r.week_num || ''
  const team = r.team_num || ''
  const key = `${season}-${week}-${team}`
  if (!teamMap.has(key)) {
    const date = (r.date && String(r.date).length >= 10) ? String(r.date).substring(0,10) : ''
    teamMap.set(key, {date: date, season: season, week: week, team: team, net_sum: 0, count: 0})
  }
  const entry = teamMap.get(key)
  entry.net_sum += net
  entry.count += 1
}

const teamRows = Array.from(teamMap.values()).map(e => ({
  date: e.date,
  season: e.season,
  week: e.week,
  team: e.team,
  team_net: e.net_sum
}))

let lowestTeamRecords = []
if (teamRows.length > 0) {
  const minTeamNet = Math.min(...teamRows.map(d => Number(d.team_net)))
  lowestTeamRecords = teamRows.filter(d => Number(d.team_net) === minTeamNet).map(d => ({
    date: d.date,
    season: d.season,
    week: d.week,
    team: d.team,
    team_net: Number(d.team_net)
  }))
}

// Diagnostic info for debugging what's computed
const diagnostic = {
  totalRows: all.length,
  grossRowsCount: grossRows.length,
  netRowsCount: netRows.length,
  teamRowsCount: teamRows.length,
  minGross: grossRows.length ? Math.min(...grossRows.map(d => Number(d.gross_score))) : null,
  minNet: netRows.length ? Math.min(...netRows.map(d => Number(d.net_score))) : null,
  minTeamNet: teamRows.length ? Math.min(...teamRows.map(d => Number(d.team_net))) : null,
  lowestGrossRecordsSample: lowestGrossRecords.slice(0,5),
  lowestNetRecordsSample: lowestNetRecords.slice(0,5),
  lowestTeamRecordsSample: lowestTeamRecords.slice(0,5)
}
```

**Lowest Gross Scores**

```js
// Show all individual gross scores below 40 (exclude BLINDs and year 1900)
const lowGrossRows = all
  .filter(d => isValidScore(Number(d.gross_score)) && !isBlindPlayer(d.display_name))
  .filter(d => Number(d.gross_score) < 40)
  .filter(d => !(String(d.date || '').startsWith('1900')))
  .map(d => ({
    date: shortDate(d),
    player: d.display_name || d.player || '',
    team: d.team_num || '',
    gross: Number(d.gross_score)
  }))


// Build a container with the Inputs.table (if any) and a JSON fallback
const container = document.createElement('div')
if (lowGrossRows.length === 0) {
  const msg = document.createElement('div')
  msg.style.color = 'var(--theme-foreground-muted)'
  msg.textContent = 'No gross scores under 40 found.'
  container.appendChild(msg)
} else {
  const tableNode = Inputs.table(lowGrossRows, {
    columns: ["date","player","team","gross"],
    header: {date: "Date", player: "Player", team: "Team", gross: "Gross"},
    rows: lowGrossRows.length,
    format: {gross: d => (d === undefined || d === null ? '' : Number(d).toFixed(0))},
    align: {date: "center", player: "left", team: "center", gross: "center"}
  })
  container.appendChild(tableNode)
}

const pre = document.createElement('pre')
pre.style.whiteSpace = 'pre-wrap'
pre.style.color = 'var(--theme-foreground-muted)'
pre.textContent = `Count: ${lowGrossRows.length}\n` + JSON.stringify(lowGrossRows.slice(0,10),null,2)
container.appendChild(pre)
container
```

```js
// show diagnostics
htl.html`<div style="color:var(--theme-foreground-muted);font-size:90%;">Diagnostics: <pre style="white-space:pre-wrap">${JSON.stringify(diagnostic,null,2)}</pre></div>`
```

**Lowest Net Score**

```js
if (lowestNetRecords.length === 0) {
  htl.html`<div style="color:var(--theme-foreground-muted);">No valid net score records found.</div>`
} else {
  Inputs.table(lowestNetRecords, {
    columns: ["date","player","net"],
    header: {date: "Date", player: "Player", net: "Net"},
    rows: lowestNetRecords.length,
    format: {net: d => (d === undefined || d === null ? '' : Number(d).toFixed(0))},
    align: {date: "center", player: "left", net: "center"}
  })
}
```

**Lowest Team Net Score**

```js
if (lowestTeamRecords.length === 0) {
  htl.html`<div style="color:var(--theme-foreground-muted);">No valid team net records found.</div>`
} else {
  Inputs.table(lowestTeamRecords, {
    columns: ["date","season","week","team","team_net"],
    header: {date: "Date", season: "Season", week: "Week", team: "Team", team_net: "Team Net"},
    rows: lowestTeamRecords.length,
    format: {team_net: d => (d === undefined || d === null ? '' : Number(d).toFixed(0))},
    align: {date: "center", season: "center", week: "center", team: "center", team_net: "center"}
  })
}
```

<style>
.hero { display: flex; flex-direction: column; align-items: center; font-family: var(--sans-serif); margin: 2rem 0 4rem; text-wrap: balance; text-align: center; }
.hero h2 { margin: 0; max-width: 34em; font-size: 20px; font-weight: 500; color: var(--theme-foreground-muted); }
</style>
