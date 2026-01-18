```js
const scores = FileAttachment("/data/BerryHillScores_Latest.csv").csv({typed: true});
```

<div>
  <h2>${selected_player}</h2>

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
const scores_with_typed_date = scores.map((element) => ({
  ...element, // spread syntax will tell Javascript to leave everything else unchanged
  date: new Date(element.date.substring(0,19)),
  }))
```

```js
const player_list = [...new Set(scores_with_typed_date.map((d) => d.display_name))].sort();
```

```js
const player_list_without_blind =  player_list.filter(element => element != "BLIND")
```

```js
const selected_player = view(Inputs.select(player_list_without_blind , {label: "Select Player"}))
```

```js
const player_data = scores_with_typed_date.filter(obj => obj.display_name == selected_player);
```

```js
const player_data_no_average = player_data.filter(obj => obj.row_type != 'average')
```

```js
Inputs.table(player_data, {
  columns: [
    "date",
    "hole_score_1",
    "hole_score_2",
    "hole_score_3",
    "hole_score_4",
    "hole_score_5",
    "hole_score_6",
    "hole_score_7",
    "hole_score_8",
    "hole_score_9",
    "gross_score",
    "round_index",
    "net_score",
    "adjusted_gross_score",
    "differential",
    "postround_handicap_index_unlimited",
  ],
  header: {
    date: htl.html`<div style="text-align: right;">${"Hole".toLocaleString("en")}
                           <div style="text-align: center;">${"Date".toLocaleString("en")}
                           <div style="float: right; color: ${Observable_Green};">${"Par".toLocaleString("en")}`,
    hole_score_1: htl.html`<div>${"1".toLocaleString("en")}
                           <div style="color: ${Observable_Green};">${"5".toLocaleString("en")}`,
    hole_score_2: htl.html`<div>${"2".toLocaleString("en")}
                           <div style="color: ${Observable_Green};">${"3".toLocaleString("en")}`, 
    hole_score_3: htl.html`<div>${"3".toLocaleString("en")}
                           <div style="color: ${Observable_Green};">${"4".toLocaleString("en")}`, 
    hole_score_4: htl.html`<div>${"4".toLocaleString("en")}
                           <div style="color: ${Observable_Green};">${"4".toLocaleString("en")}`, 
    hole_score_5: htl.html`<div>${"5".toLocaleString("en")}
                           <div style="color: ${Observable_Green};">${"4".toLocaleString("en")}`, 
    hole_score_6: htl.html`<div>${"6".toLocaleString("en")}
                           <div style="color: ${Observable_Green};">${"4".toLocaleString("en")}`, 
    hole_score_7: htl.html`<div>${"7".toLocaleString("en")}
                           <div style="color: ${Observable_Green};">${"4/5".toLocaleString("en")}`, 
    hole_score_8: htl.html`<div>${"8".toLocaleString("en")}
                           <div style="color: ${Observable_Green};">${"3".toLocaleString("en")}`, 
    hole_score_9: htl.html`<div>${"9".toLocaleString("en")}
                           <div style="color: ${Observable_Green};">${"5".toLocaleString("en")}`, 
    gross_score: htl.html`<div style="white-space: pre-wrap;color: ${Observable_Brown};">${"Gross\nScore".toLocaleString("en")}`,
    round_index: htl.html`<div style="white-space: pre-wrap;">${"Round\nIndex".toLocaleString("en")}`,
    net_score:htl.html`<div style="white-space: pre-wrap; color: ${Observable_Light_Blue};">${"Net\nScore".toLocaleString("en")}`,
    adjusted_gross_score:htl.html`<div style="white-space: pre-wrap;color: ${Observable_Blue}">${"Adjusted\nGross".toLocaleString("en")}`,
    differential:htl.html`<div style="white-space: pre-wrap;">${"Score\nDifferential".toLocaleString("en")}`,
    postround_handicap_index_unlimited:htl.html`<div style="white-space: pre-wrap;color: ${Observable_Orange}">${"Handicap\nIndex\n(After Round)".toLocaleString("en")}`,
  },
  sort: "date",
  reverse: true,
  rows: 20,
  layout: "auto",
  format: {
    date: (d,i,data) => format_date(d,i,data),
    hole_score_1: (d,i,data) => format_hole_score(d,i,data,0),
    hole_score_2: (d,i,data) => format_hole_score(d,i,data,1),
    hole_score_3: (d,i,data) => format_hole_score(d,i,data,2),
    hole_score_4: (d,i,data) => format_hole_score(d,i,data,3),
    hole_score_5: (d,i,data) => format_hole_score(d,i,data,4),
    hole_score_6: (d,i,data) => format_hole_score(d,i,data,5),
    hole_score_7: (d,i,data) => format_hole_score(d,i,data,6),
    hole_score_8: (d,i,data) => format_hole_score(d,i,data,7),
    hole_score_9: (d,i,data) => format_hole_score(d,i,data,8),
    gross_score: (d,i,data) => format_gross(d,i,data),
    round_index: (d,i,data) => format_net_or_round_index(d,i,data),
    net_score: (d,i,data) => format_net_or_round_index(d,i,data),
    adjusted_gross_score: (d,i,data) => format_gross(d,i,data),
    differential: (d,i,data) => format_differential(d,i,data),
    postround_handicap_index_unlimited: (d,i,data) => format_handicap_index(d,i,data),
  },
  align: {
    date: "center",
    hole_score_1: "center",
    hole_score_2: "center",
    hole_score_3: "center",
    hole_score_4: "center",
    hole_score_5: "center",
    hole_score_6: "center",
    hole_score_7: "center",
    hole_score_8: "center",
    hole_score_9: "center",
    gross_score: "center",
    round_index: "center",
    net_score: "center",
    adjusted_gross_score: "center",
    differential: "center",
    postround_handicap_index_unlimited: "center",
  }
})
```
```js
Plot.plot({
  grid: true,
  axis: null,
  x: {type: "band"},
  marks: [
    Plot.ruleY([0]),
    Plot.axisY({color: Observable_Gray, tickColor: Observable_Gray}),
    Plot.gridY({stroke: Observable_Gray, strokeWidth:1, strokeOpacity: .3}),
    Plot.rectY(player_data_no_average, {fill: Observable_Brown, x: "date", y: "gross_score"}),
    Plot.rectY(player_data_no_average, {fill: Observable_Blue, x: "date", y: "adjusted_gross_score"}),
    Plot.tickY(player_data_no_average, {strokeWidth: 3, stroke: Observable_Light_Blue, x: "date", y: "net_score"}),
    Plot.rectY(player_data_no_average, {fill: (d,i,data) => differential_color(d,i,data), x: "date", y: "differential"}),
    Plot.lineY(player_data_no_average, {strokeWidth: 1, stroke: Observable_Orange, x: "date", y: "postround_handicap_index_unlimited"}),
    Plot.dotY(player_data_no_average, {r: 3, fill: Observable_Orange, Observable_Orange: "red", x: "date", y: "postround_handicap_index_unlimited"}),

    Plot.tip(player_data_no_average, 
      Plot.pointer({
        x: "date",
        y: "differential",
        title: (d) => [d.date.toLocaleDateString("en-CA") + "\nDifferential: "+ d.differential].join("\n"),
    })),
    Plot.tip(player_data_no_average, 
      Plot.pointer({
        x: "date",
        y: "net_score",
        title: (d) => [d.date.toLocaleDateString("en-CA") + "\nNet: "+ d.net_score].join("\n"),
    })),
    Plot.tip(player_data_no_average, 
      Plot.pointer({
        x: "date",
        y: "gross_score",
        title: (d) => [d.date.toLocaleDateString("en-CA") + "\nGross: "+ d.gross_score].join("\n"),
    })),
  ]
})
```

```js
function format_hole_score(d, i, data) {
    var hole_par = 0
    var hole_num_index = arguments[3]
    if(data[i].tee == "Red") {
      hole_par = red_par_array[hole_num_index]
    }
    else {
      hole_par = white_par_array[hole_num_index]
    }
    var delta = d - hole_par
  
    var max_legitimate_score = 0;
    if (data[i].max_stroke_per_hole == "DB"){
          max_legitimate_score = hole_par + 2
    }
    else {
          max_legitimate_score = data[i].max_stroke_per_hole
    }
  
    if (data[i].row_type == 'average') {
        return htl.html`<div style="
        color: ${Observable_Pink};
        ">${d.toFixed(1).toLocaleString("en")}` 
    }
    else if (d > max_legitimate_score) {        
      return htl.html`<div style="
        color: ${Observable_Brown};
        ">${d.toLocaleString("en")}`      
    }
    else if (delta == -2) {
      return htl.html`<div style="
        color: ${Observable_Red};
        border-width:4px;
        border-style:double;
        border-color:${Observable_Red};
        padding: 0em;
        border-radius: 50%;
        ">${d.toLocaleString("en")}🦅`
    }
    else if (delta == -1) {
      return htl.html`<div style="
        color: ${Observable_Red};
        border-width:1px;
        border-style:solid;
        border-color:${Observable_Red};
        padding: 0em;
        border-radius: 50%;
        ">${d.toLocaleString("en")}`
    }
    else if (delta == 0) {
      return htl.html`<div style="
        color: ${Observable_Green};
        background-color: rgba(60, 169, 81, 0.2);
        border-radius: 40%;
        ">${d.toLocaleString("en")}`
    }
    else {
      return htl.html`<div style="
        color: #000000;
        ">${d.toLocaleString("en")}`
    }
}
```

```js
function format_date(d, i, data) {
  const date = new Date(d)
  if (data[i].row_type == 'average') { 
      return htl.html`<div style="
        color: ${Observable_Pink};
        ">${"Average".toLocaleString("en")}`
  }
  else if (data[i].row_type == 'backlog') {
      return htl.html`<div style="
        color: #000000;
        ">${"Backlog".toLocaleString("en")}`
  }
  else {
      return htl.html`<div style="
        color: #000000;
        ">${d.toLocaleDateString("en-CA")}` // Using CA for Canada because this puts year first .toLocaleDateString("en-CA")
    }
}
```

```js
function format_gross(d, i, data) {
    if (data[i].row_type == 'average') {
        return htl.html`<div style="
        color: ${Observable_Pink};
        ">${d.toFixed(1).toLocaleString("en")}` 
    }
    else {
      return htl.html`<div style="
        color: #000000;
        ">${d.toLocaleString("en")}`
    }
}
```

```js
function format_net_or_round_index(d, i, data) {
    if (data[i].row_type == 'average') {
        return htl.html`<div style="
        color: ${Observable_Pink};
        ">${d.toFixed(1).toLocaleString("en")}` 
    }
    else {
      return htl.html`<div style="
        color: #000000;
        ">${d.toFixed(1).toLocaleString("en")}`
    }
}
```

```js
function format_handicap_index(d, i, data) {
    if (data[i].row_type == 'average') {
        return htl.html`<div style="
        color: ${Observable_Pink} ;
        ">${"".toLocaleString("en")}` 
    }
    else {
      return htl.html`<div style="
        color: ${Observable_Orange};
        ">${d.toFixed(2).toLocaleString("en")}`
    }
}
```

```js
function format_differential (d, i, data) {
    var handicap_index = data[0].postround_handicap_index_unlimited
    if (data[i].row_type == 'average') {
        return htl.html`<div style="
        color: ${Observable_Purple};
        background-color:rgba(255, 138, 183, 0.2);
        border-radius: 0%;
        ">${handicap_index.toFixed(1).toLocaleString("en")}` 
    }
    else if (data[i].part_of_backlog != "True") {
        return htl.html`<div style="
        color: ${Observable_Gray};
        text-decoration: line-through;
        ">${d.toFixed(1).toLocaleString("en")}`
    }
    else if (data[i].differential_used == "True") {
        return htl.html`<div style="
        color: ${Observable_Purple};
        ">${d.toFixed(1).toLocaleString("en")}`
    }
    else {
        return htl.html`<div style="
        color: #000000;
        ">${d.toFixed(1).toLocaleString("en")}`
    }
}
```

```js
function differential_color(d, i, data) {
    if (data[i].part_of_backlog != "True") {
        return Observable_Gray
    }
    else if (data[i].differential_used == "True") {
        return Observable_Purple
    }
    else {
        return "black"
    }
}
```

```js
const sentinal_large_int = 99998
```

```js
const sentinal_large_int2 = 99999
```

```js
const white_par_array = [5,3,4,4,4,4,4,3,5]
```

```js
const red_par_array = [5,3,4,4,4,4,5,3,5]
```


<style>

.hero {
  display: flex;
  flex-direction: column;
  align-items: center;
  font-family: var(--sans-serif);
  margin: 4rem 0 8rem;
  text-wrap: balance;
  text-align: center;
}

.hero h1 {
  margin: 1rem 0;
  padding: 1rem 0;
  max-width: none;
  font-size: 14vw;
  font-weight: 900;
  line-height: 1;
  background: linear-gradient(green, white);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero h2 {
  margin: 0;
  max-width: 34em;
  font-size: 20px;
  font-style: initial;
  font-weight: 500;
  line-height: 1.5;
  color: var(--theme-foreground-muted);
}

@media (min-width: 640px) {
  .hero h1 {
    font-size: 90px;
  }
}

</style>
