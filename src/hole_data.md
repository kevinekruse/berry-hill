```js
const berryhill_hole_averages = FileAttachment("/data/BerryHill_Hole_Averages.csv").csv({typed: true});
```

```js
const rounds_no_blind = await FileAttachment("/data/BerryHillScores_Rounds_NoBlind.csv").csv({typed: true});
```

<div>
  <h2>Hole Data</h2>
</div>

```js
let totalHolesPlayed = 0
let earliestTs = Infinity

for (const r of rounds_no_blind) {
  const d = r.date
  if (d) {
    const ts = Number(new Date(d))
    if (Number.isFinite(ts)) earliestTs = Math.min(earliestTs, ts)
  }

  for (let h = 1; h <= 9; h++) {
    const v = Number(r[`hole_score_${h}`])
    if (Number.isFinite(v)) totalHolesPlayed += 1
  }
}

const earliestDateStr = earliestTs === Infinity ? "N/A" : new Date(earliestTs).toISOString().slice(0, 10)
const holesStr = d3.format(",d")(totalHolesPlayed)

display(htl.html`<div style="margin:0 0 10px 0;color:#000000;">${holesStr} holes in data set played since ${earliestDateStr}</div>`)
```

```js
const Observable_Blue = "#4269D0"
```

```js
const Observable_Cyan = "#6CC5B0"
```

```js
const Observable_Purple = "#A463F2"
```

```js
const Observable_Orange = "#EFB118"
```

```js
const Observable_Green = "#3CA951"
```

```js
const Observable_Light_Blue = "#97BBF5"
```

```js
const Observable_Gray = "#9498A0"
```

```js
const Observable_Red = "#FF725C"
```

```js
const Observable_Pink = "#FF8AB7"
```

```js
const Observable_Brown = "#9C6B4E"
```

```js
const yearOptions = [
  "All Years",
  ...Array.from(new Set(berryhill_hole_averages.map(d => Number(d.season_year)).filter(Number.isFinite)))
    .sort((a, b) => b - a)
    .map(String)
]
const selected_year = view(Inputs.select(yearOptions, {label: "Season Year", value: "2026"}))
```

```js
let filtered_by_year_data

if (selected_year === "All Years") {
  const byHole = d3.group(berryhill_hole_averages, d => Number(d.hole))
  const rows = Array.from(byHole, ([hole, values]) => ({
    season_year: "All Years",
    hole,
    mens_par: values[0]?.mens_par,
    womens_par: values[0]?.womens_par,
    hole_handicap: values[0]?.hole_handicap,
    hole_score_average: d3.mean(values, d => Number(d.hole_score_average)),
    hole_delta_average: d3.mean(values, d => Number(d.hole_delta_average))
  })).sort((a, b) => a.hole - b.hole)

  const ranked = rows
    .slice()
    .sort((a, b) => b.hole_delta_average - a.hole_delta_average)
    .map((d, i) => ({hole: d.hole, rank: i + 1}))
  const rankMap = new Map(ranked.map(d => [d.hole, d.rank]))

  filtered_by_year_data = rows.map(d => ({...d, hole_delta_rank: rankMap.get(d.hole)}))
} else {
  filtered_by_year_data = berryhill_hole_averages.filter((d) => Number(d.season_year) == Number(selected_year))
}
```

```js
Plot.plot({
  style: {stroke:  "#0000000", fontSize: "12px", fontStyle: "normal", fontWeight: "light"},
  
  y: {
    grid: true,
    tickSpacing: 20,
    label: "Strokes Above Par",
    domain: [0,3.7],
  },
  x: {
    grid: false,
    axis: null,
    domain: [0,1,2,3,4,5,6,7,8,9],
  },
  marks: [
    Plot.barY(filtered_by_year_data, {x: "hole", y: "hole_delta_average", stroke: Observable_Gray, fill: Observable_Gray}),
    Plot.text(filtered_by_year_data, {x: "hole", y: (d) => d.hole_delta_average + 0.1, text: (d) => d3.format("0.2f")(d.hole_delta_average)}),

    Plot.text(filtered_by_year_data, {x: 0, y: 3.5, text: (d) => "Hole", textAnchor: "middle"}),
    Plot.text(filtered_by_year_data, {x: "hole", y: 3.5, text: (d) => d.hole}),

    Plot.text(filtered_by_year_data, {x: 0, y: 3.3, text: (d) => "Par", textAnchor: "middle"}),
    Plot.text(filtered_by_year_data, {x: "hole", y: 3.3, text: (d) => d.mens_par + "/" + d.womens_par}),

    Plot.text(filtered_by_year_data, {x: 0, y: 3.1, text: (d) => "Handicap", textAnchor: "middle"}),
    Plot.text(filtered_by_year_data, {x: "hole", y: 3.1, text: (d) => d.hole_handicap}),
    
    Plot.text(filtered_by_year_data, {x: 0, y: 2.9, text: (d) => "League Rank", textAnchor: "middle"}),
    Plot.text(filtered_by_year_data, {x: "hole", y: 2.9, text: (d) => d.hole_delta_rank}),

    Plot.text([`Average League Hole Data for ${selected_year}`], { frameAnchor: "top", lineAnchor: "bottom"}),

    Plot.ruleY([0], {stroke: Observable_Gray})
  ]
})
```

```js
const baseYears = Array.from(new Set(berryhill_hole_averages.map(d => Number(d.season_year)).filter(Number.isFinite))).sort((a, b) => a - b)
const seriesOrder = baseYears.map(String)

const allYearsByHole = Array.from(
  d3.group(berryhill_hole_averages, d => Number(d.hole)),
  ([hole, values]) => ({
    hole,
    season_label: "All Years",
    hole_delta_average: d3.mean(values, d => Number(d.hole_delta_average))
  })
)

const allYearsMap = new Map(allYearsByHole.map(d => [d.hole, d.hole_delta_average]))

const byYearRows = berryhill_hole_averages.map(d => ({
  hole: Number(d.hole),
  season_label: String(Number(d.season_year)),
  hole_delta_average: Number(d.hole_delta_average)
}))

const groupedRows = byYearRows.map(d => ({
  ...d,
  hole_delta_relative: d.hole_delta_average - (allYearsMap.get(d.hole) ?? 0)
}))

const yMinRelative = d3.min(groupedRows, d => d.hole_delta_relative) ?? 0
const yMaxRelative = d3.max(groupedRows, d => d.hole_delta_relative) ?? 0
const yPad = 0.1
const yDomainRelative = [Math.min(yMinRelative - yPad, 0), Math.max(yMaxRelative + yPad, 0)]

const barWidth = 0.11
const centeredIndex = (seriesOrder.length - 1) / 2
const offsetBySeason = new Map(seriesOrder.map((s, i) => [s, (i - centeredIndex) * barWidth]))

display(htl.html`<h3 style="margin:20px 0 8px 0;">Hole-by-Hole Multi-Year Comparison</h3>`)

const multiYearPlot = Plot.plot({
  style: {stroke: "#0000000", fontSize: "12px", fontStyle: "normal", fontWeight: "light"},
  marginLeft: 58,
  marginRight: 20,
  height: 420,
  y: {
    grid: true,
    tickSpacing: 24,
    label: "Relative to All Years (Strokes)",
    domain: yDomainRelative
  },
  x: {
    label: "Hole",
    domain: [0.5, 9.5],
    tickFormat: d => Number(d)
  },
  color: {
    legend: true,
    domain: seriesOrder,
    range: [
      Observable_Blue,
      Observable_Cyan,
      Observable_Purple,
      Observable_Orange,
      Observable_Green,
      Observable_Light_Blue,
      Observable_Red,
      Observable_Brown
    ]
  },
  marks: [
    Plot.rectY(groupedRows, {
      x1: d => d.hole + offsetBySeason.get(d.season_label) - (barWidth / 2),
      x2: d => d.hole + offsetBySeason.get(d.season_label) + (barWidth / 2),
      y1: 0,
      y2: d => d.hole_delta_relative,
      fill: "season_label",
      stroke: Observable_Gray,
      tip: true
    }),
    Plot.ruleY([0], {stroke: Observable_Gray}),
    Plot.text(["Hole-by-Hole Comparison: Relative to All Years Average"], {frameAnchor: "top", lineAnchor: "bottom"})
  ]
})

display(multiYearPlot)
```

```js
const trendRows = berryhill_hole_averages
  .map(d => ({
    season_year: Number(d.season_year),
    hole: Number(d.hole),
    hole_delta_average: Number(d.hole_delta_average)
  }))
  .filter(d => Number.isFinite(d.season_year) && Number.isFinite(d.hole) && Number.isFinite(d.hole_delta_average))

const trendYears = Array.from(new Set(trendRows.map(d => d.season_year))).sort((a, b) => a - b)
const holeDomain = [1, 2, 3, 4, 5, 6, 7, 8, 9]

display(htl.html`<h3 style="margin:20px 0 8px 0;">Strokes Above Par by Hole Over Time</h3>`)

const holeTrendPlot = Plot.plot({
  style: {stroke: "#0000000", fontSize: "12px", fontStyle: "normal", fontWeight: "light"},
  marginLeft: 58,
  marginRight: 20,
  height: 440,
  y: {
    grid: true,
    tickSpacing: 24,
    label: "Strokes Above Par",
    domain: [0, 3.7]
  },
  x: {
    label: "Year",
    tickValues: trendYears,
    tickFormat: d => String(d)
  },
  color: {
    legend: true,
    domain: holeDomain,
    range: [
      Observable_Blue,
      Observable_Cyan,
      Observable_Purple,
      Observable_Orange,
      Observable_Green,
      Observable_Light_Blue,
      Observable_Red,
      Observable_Pink,
      Observable_Brown
    ]
  },
  marks: [
    Plot.line(trendRows, {
      x: "season_year",
      y: "hole_delta_average",
      stroke: "hole",
      marker: true,
      strokeWidth: 2,
      tip: true
    }),
    Plot.dot(trendRows, {
      x: "season_year",
      y: "hole_delta_average",
      fill: "hole",
      r: 3,
      tip: true
    }),
    Plot.ruleY([0], {stroke: Observable_Gray})
  ]
})

display(holeTrendPlot)
```

```js
const percentRows = berryhill_hole_averages
  .map(d => {
    const season_year = Number(d.season_year)
    const hole = Number(d.hole)
    const hole_score_average = Number(d.hole_score_average)
    const hole_delta_average = Number(d.hole_delta_average)
    const average_par = hole_score_average - hole_delta_average
    const percent_above_par = average_par > 0
      ? (hole_delta_average / average_par) * 100
      : NaN
    return {season_year, hole, percent_above_par}
  })
  .filter(d => Number.isFinite(d.season_year) && Number.isFinite(d.hole) && Number.isFinite(d.percent_above_par))

const percentYears = Array.from(new Set(percentRows.map(d => d.season_year))).sort((a, b) => a - b)
const percentMin = d3.min(percentRows, d => d.percent_above_par) ?? 0
const percentMax = d3.max(percentRows, d => d.percent_above_par) ?? 0
const percentPad = 2

display(htl.html`<h3 style="margin:20px 0 8px 0;">Percentage Above Par by Hole Over Time</h3>`)

const holePercentTrendPlot = Plot.plot({
  style: {stroke: "#0000000", fontSize: "12px", fontStyle: "normal", fontWeight: "light"},
  marginLeft: 64,
  marginRight: 20,
  height: 440,
  y: {
    grid: true,
    tickSpacing: 24,
    label: "Percentage Above Par",
    domain: [Math.max(0, percentMin - percentPad), percentMax + percentPad],
    tickFormat: d => `${d.toFixed(0)}%`
  },
  x: {
    label: "Year",
    tickValues: percentYears,
    tickFormat: d => String(d)
  },
  color: {
    legend: true,
    domain: holeDomain,
    range: [
      Observable_Blue,
      Observable_Cyan,
      Observable_Purple,
      Observable_Orange,
      Observable_Green,
      Observable_Light_Blue,
      Observable_Red,
      Observable_Pink,
      Observable_Brown
    ]
  },
  marks: [
    Plot.line(percentRows, {
      x: "season_year",
      y: "percent_above_par",
      stroke: "hole",
      marker: true,
      strokeWidth: 2,
      tip: true
    }),
    Plot.dot(percentRows, {
      x: "season_year",
      y: "percent_above_par",
      fill: "hole",
      r: 3,
      tip: true
    }),
    Plot.ruleY([0], {stroke: Observable_Gray})
  ]
})

display(holePercentTrendPlot)
```