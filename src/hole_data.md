```js
const berryhill_hole_averages = FileAttachment("/data/BerryHill_Hole_Averages.csv").csv({typed: true});
```

<div>
  <h2>Hole Average Data</h2>
</div>

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
const selected_year = view(Inputs.range([2020,2025], {label: "Season Year", step: 1, value: 2025, stroke: Observable_Gray}))
```

```js
const filtered_by_year_data = berryhill_hole_averages.filter((d) => d.season_year == selected_year)
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

    Plot.text(["Average League Hole Data for " + `${selected_year}`], { frameAnchor: "top", lineAnchor: "bottom"}),

    Plot.ruleY([0], {stroke: Observable_Gray})
  ]
})
```