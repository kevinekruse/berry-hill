```js
// Load all rounds CSV and hole par data
const all = await FileAttachment("data/BerryHillScores_All_Latest.csv").csv({typed: true})
const holeAverages = await FileAttachment("data/BerryHill_Hole_Averages.csv").csv({typed: true})
```

```js
// helpers
const shortDate = d => (d && String(d.date).length >= 10) ? String(d.date).substring(0,10) : String(d.date || "")
const isBlindPlayer = name => {
  if (!name) return false
  const s = String(name).toUpperCase()
  return s.includes('BLIND') || s.includes('\u0392LIND')
}
const isBacklog = v => (v === true) || (String(v).toLowerCase() === 'true')

// build hole par lookup: key = `${season}|${hole}|${sex}` -> par
const holeParMap = new Map()
for (const r of holeAverages) {
  const season = String(r.season_year)
  const hole = String(r.hole)
  holeParMap.set(`${season}|${hole}|M`, Number(r.mens_par))
  holeParMap.set(`${season}|${hole}|F`, Number(r.womens_par))
}

// determine hole columns present in the CSV
const holeCols = Object.keys(all[0] || {}).filter(k => k.startsWith('hole_score_'))
holeCols.sort((a,b)=> Number(a.split('_').pop()) - Number(b.split('_').pop()))

// filter rows: only 'round' rows, exclude blinds and backlog entries
const rows = all.filter(r => (String(r.row_type || '').toLowerCase() === 'round')
  && !isBlindPlayer(r.display_name)
  && !isBacklog(r.part_of_backlog))

// map and prepare per-row hole delta arrays
const tableRows = rows.map(r => {
  const season = String(r.season_year || '')
  const sex = (r.sex && String(r.sex).toUpperCase().startsWith('F')) ? 'F' : 'M'
  const hole_pars = holeCols.map(c => {
    const n = c.split('_').pop()
    const par = holeParMap.get(`${season}|${n}|${sex}`)
    return par === undefined ? null : par
  })
  const hole_deltas = holeCols.map((c,i) => {
    const s = Number(r[c])
    const par = hole_pars[i]
    if (!Number.isFinite(s) || s === 0) return null
    if (!Number.isFinite(par)) return null
    return s - par
  })
  const out = {
    date: shortDate(r),
    week_num: r.week_num,
    team_num: r.team_num,
    player: r.display_name,
    gross_score: Number(r.gross_score),
    round_index: Number(r.round_index),
    net_score: Number(r.net_score),
    hole_pars: hole_pars,
    hole_deltas: hole_deltas
  }
  // include each hole column, but convert 0 to null so formatting hides it
  for (const c of holeCols) {
    const v = Number(r[c])
    out[c] = (Number.isFinite(v) && v !== 0) ? v : null
  }
  return out
})

// export for introspection if needed
tableRows
```

```js
// Build a container with a diagnostic header and the table so the page always shows something
const container = document.createElement('div')
const diag = document.createElement('div')
diag.style.color = 'var(--theme-foreground-muted)'
diag.style.marginBottom = '0.5rem'
diag.innerHTML = `Rows total: ${all.length} · Filtered rows: ${rows.length} · Table rows: ${tableRows.length} · Holes: ${holeCols.length}`
container.appendChild(diag)

const columns = ['date','week_num','team_num','player', ...holeCols, 'gross_score','round_index','net_score']

// show first 5 rows as JSON for debugging (always visible)
const preview = document.createElement('pre')
preview.style.background = 'var(--theme-background-muted)'
preview.style.padding = '0.5rem'
preview.style.borderRadius = '4px'
preview.style.maxHeight = '10rem'
preview.style.overflow = 'auto'
try {
  const sample = tableRows.slice(0,5).map(r => ({date:r.date, week_num:r.week_num, team_num:r.team_num, player:r.player, gross_score:r.gross_score, round_index:r.round_index, net_score:r.net_score}))
  preview.textContent = JSON.stringify(sample, null, 2)
} catch (e) {
  preview.textContent = 'preview error: ' + String(e)
}
container.appendChild(preview)

// try rendering Inputs.table but catch runtime errors so page still shows diagnostics
try {
  const tableNode = Inputs.table(tableRows, {
    columns: columns,
    header: Object.fromEntries(columns.map(c => [c, c.replace(/_/g,' ').replace(/hole score /i,'Hole ').replace(/gross score/i,'Gross Score').replace(/net score/i,'Net Score')])),
    format: Object.fromEntries(holeCols.map((c,i)=>[c, (d,idx,data)=>format_hole_score(d,idx,data,i)]).concat([
      ['gross_score',(d)=>format_default_number(d)],
      ['round_index',(d)=>format_default_number(d)],
      ['net_score',(d)=>format_default_number(d)]
    ])),
    align: Object.fromEntries(columns.map(c=>[c, 'center'])),
    rows: 200,
    layout: 'auto'
  })
  container.appendChild(tableNode)
} catch (e) {
  const err = document.createElement('pre')
  err.textContent = 'Table render error: ' + String(e)
  container.appendChild(err)
}
// Also render a simple plain-HTML table of the first 20 rows so it's visible without Inputs
try {
  const plain = document.createElement('div')
  plain.style.marginTop = '0.5rem'
  const tbl = document.createElement('table')
  tbl.style.borderCollapse = 'collapse'
  tbl.style.width = '100%'
  const hdr = tbl.createTHead().insertRow()
  const sampleCols = ['date','week_num','team_num','player','gross_score','round_index','net_score']
  for (const c of sampleCols) {
    const th = document.createElement('th')
    th.textContent = c.replace(/_/g,' ')
    th.style.border = '1px solid #ccc'
    th.style.padding = '4px'
    th.style.textAlign = 'center'
    hdr.appendChild(th)
  }
  const tbody = tbl.createTBody()
  for (const r of tableRows.slice(0,20)) {
    const row = tbody.insertRow()
    for (const c of sampleCols) {
      const cell = row.insertCell()
      cell.textContent = String(r[c] == null ? '' : r[c])
      cell.style.border = '1px solid #eee'
      cell.style.padding = '4px'
      cell.style.textAlign = 'center'
    }
  }
  plain.appendChild(tbl)
  container.appendChild(plain)
} catch (e) {
  const err2 = document.createElement('pre')
  err2.textContent = 'Plain table error: ' + String(e)
  container.appendChild(err2)
}
container
```

```js
// formatting helpers (adapted from weekly_results)
const sentinal_large_int = 99998
const sentinal_large_int2 = 99999

function format_hole_score(d,i,data,idx) {
  // d: value for the cell, idx: hole index (0-based)
  if (d === null || d === undefined) return ''
  if (d == sentinal_large_int || d == sentinal_large_int2) return ''
  const delta = (data[i].hole_deltas && data[i].hole_deltas[idx] != null) ? data[i].hole_deltas[idx] : null
  if (String(data[i].player || '').includes('Average')) {
    return htl.html`<div style="color: #00008B;">${d.toLocaleString("en")}`
  }
  else if (delta === -2) {
    return htl.html`<div style="color: #FF0000; border-width:4px; border-style:double; border-color:#FF0000; padding: 0em; border-radius: 50%;">${d.toLocaleString("en")}🦅`
  }
  else if (delta === -1) {
    return htl.html`<div style="color: #FF0000; border-width:1px; border-style:solid; border-color:#FF0000; padding: 0em; border-radius: 50%;">${d.toLocaleString("en")}`
  }
  else if (delta === 0) {
    return htl.html`<div style="color: #027148; background-color: #D1FFBD; border-radius: 40%;">${d.toLocaleString("en")}`
  }
  else {
    return htl.html`<div style="color: #000000;">${d.toLocaleString("en")}`
  }
}

function format_default_number(d) {
  if (d === null || d === undefined) return ''
  if (!Number.isFinite(d)) return ''
  return d.toLocaleString('en')
}
```

```js
// table is rendered above inside the container cell
```

<style>
.hero { display:flex; flex-direction:column; align-items:center; }
</style>
