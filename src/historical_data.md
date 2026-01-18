---
toc: true
---

<div class="hero">
  <h1>Historical Scoring Data</h1>
</div>

```js
const score_data_cleaned = FileAttachment("score_data_cleaned.csv").csv({typed: false});
```

```js
const team_list = [...new Set(score_data_cleaned.map((d) => d.team_code))].sort(); 
```

```js
const selected_teams = view(Inputs.checkbox(team_list, {label: "Team(s)", value: team_list.filter((d) => (d != "09" && d != "10"))}));
```

```js
const player_list = [...new Set(score_data_cleaned.map((d) => d.player_name))].sort();
```

```js
const selected_players = view(Inputs.select([...new Set(score_data_cleaned.filter((d) => selected_teams.includes(d.team_code)).map((d) => d.player_name))].sort(),
  {
    multiple: true,
    label: "Player(s)",
    value: [...new Set(score_data_cleaned.filter((d) => selected_teams.includes(d.team_code)).map((d) => d.player_name))]
  }
)
```

```js
const score_type = view(Inputs.radio(["gross_score", "net_score"], {label: "Score Type", value: "gross_score"}))
```

```js
const color_code_choice = view(Inputs.radio(["team_code", "player_name"], {label: "Color By", value: "team_code"}))
```

```js
const filtered_dataset = score_data_cleaned.filter((d) => selected_teams.includes(d.team_code)).filter((d) => selected_players.includes(d.player_name))
```

```js
const filtered_gross_score_array = [...filtered_dataset.map((d) => Number(d.gross_score))]
```

```js
const filtered_net_score_array = [...filtered_dataset.map((d) => Number(d.net_score))]
```

```js
function scoresPlot({width} = {}) {
  return Plot.plot({
  marginRight: 80,
  marginLeft: 20,
  height: 600,
  grid: true,
  aspectRatio: 0.5,
  x: {type: "linear", domain: [0, 20], ticks: 4},
  y: {domain: [24,74], ticks: 50, axis: "left"},
  style: {fontSize: 11},
  color: {type: "ordinal",  legend: true, label: "Team", sort: true, scheme: "Observable10"},
  marks: [
    Plot.frame(),
    // Plot Scores for all selected players
    Plot.dot(filtered_dataset, {
      x: "week_number",
      fx: "season_year",
      y: score_type, 
      stroke: color_code_choice,
      }),
    // Interactive tip to show info when hovering
    Plot.tip(filtered_dataset, 
      Plot.pointer({
        x: "week_number",
        fx: "season_year",
        y: score_type,
        title: (d) => [d.player_name, "Team " + d.team_code, "Gross " + d.gross_score, "Net " + d.net_score].join("\n"),
    })),
    // Identify the average of the active data
    Plot.text(["<-Mean: " + Number((filtered_gross_score_array.reduce((a, b) => a + b) / filtered_gross_score_array.length).toPrecision(3)).toString()], {
      fontSize: "small",
      x: 21,
      y: Number((filtered_gross_score_array.reduce((a, b) => a + b) / filtered_gross_score_array.length).toPrecision(3)),
      textAnchor: "start",
      fx: ["2024"],
      opacity: score_type == "gross_score" ? 1 : 0
    }),
    Plot.text(["<-Mean " + Number((filtered_net_score_array.reduce((a, b) => a + b) / filtered_net_score_array.length).toPrecision(3)).toString()], {
      fontSize: "small",
      x: 21,
      y: Number((filtered_net_score_array.reduce((a, b) => a + b) / filtered_net_score_array.length).toPrecision(3)),
      textAnchor: "start",
      fx: ["2024"],
      opacity: score_type == "net_score" ? 1 : 0
    }),
    
    // Identify the max of the active data
    Plot.text(["<-Max: " + Number((filtered_gross_score_array.reduce((a, b) => Math.max(a,b))).toPrecision(3)).toString()],{
      fontSize: "small",
      x: 21,
      y: Number((filtered_gross_score_array.reduce((a, b) => Math.max(a,b))).toPrecision(3)),
      textAnchor: "start",
      fx: ["2024"],
      opacity: score_type == "gross_score" ? 1 : 0
    }),
    Plot.text(["<-Max " + Number((filtered_net_score_array.reduce((a, b) => Math.max(a,b))).toPrecision(3)).toString()], {
      fontSize: "small",
      x: 21,
      y: Number((filtered_net_score_array.reduce((a, b) => Math.max(a,b))).toPrecision(3)),
      textAnchor: "start",
      fx: ["2024"],
      opacity: score_type == "net_score" ? 1 : 0
    }),

    // Identify the min of the active data
    Plot.text(["<-Min: " + Number((filtered_gross_score_array.reduce((a, b) => Math.min(a,b))).toPrecision(3)).toString()],{
      fontSize: "small",
      x: 21,
      y: Number((filtered_gross_score_array.reduce((a, b) => Math.min(a,b))).toPrecision(3)),
      textAnchor: "start",
      fx: ["2024"],
      opacity: score_type == "gross_score" ? 1 : 0
    }),
    Plot.text(["<-Min " + Number((filtered_net_score_array.reduce((a, b) => Math.min(a,b))).toPrecision(3)).toString()], {
      x: 21,
      y: Number((filtered_net_score_array.reduce((a, b) => Math.min(a,b))).toPrecision(3)),
      textAnchor: "start",
      fx: ["2024"],
      opacity: score_type == "net_score" ? 1 : 0,
      fontSize: "small",
    }),
  ]
  
});
}
```

<div class="grid grid-cols-2">
  <div class="card">${resize((width) => scoresPlot({width}))}</div>
</div>