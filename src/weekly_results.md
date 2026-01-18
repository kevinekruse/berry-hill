```js
const latest_scores = FileAttachment("/data/BH_Scores_Latest.json").json()
```

```js
  const latest_week_num = latest_scores.metadata.week_num
```

```js
  const files = [
    FileAttachment("/data/BH_Scores_2025_01.json"),
    FileAttachment("/data/BH_Scores_2025_02.json"),
    FileAttachment("/data/BH_Scores_2025_03.json"),
    FileAttachment("/data/BH_Scores_2025_04.json"),
    FileAttachment("/data/BH_Scores_2025_05.json"),
    FileAttachment("/data/BH_Scores_2025_06.json"),
    FileAttachment("/data/BH_Scores_2025_07.json"),
    FileAttachment("/data/BH_Scores_2025_08.json"),
    FileAttachment("/data/BH_Scores_2025_09.json"),
    FileAttachment("/data/BH_Scores_2025_10.json"),
    FileAttachment("/data/BH_Scores_2025_11.json"),
    FileAttachment("/data/BH_Scores_2025_12.json"),
    FileAttachment("/data/BH_Scores_2025_13.json"),
    FileAttachment("/data/BH_Scores_2025_14.json"),
    FileAttachment("/data/BH_Scores_2025_15.json"),
    FileAttachment("/data/BH_Scores_2025_16.json"),
    FileAttachment("/data/BH_Scores_2025_17.json"),
]
```

```js
const week_nums = [...Array(latest_week_num).keys()].map(x => x + 1)
```

```js
const scores = files[week_num-1].json()
//const scores = FileAttachment("/data/BH_Scores_2025_01.json").json()

```

```js
  const season_year = scores.metadata.season_year
```

```js
  const date = scores.metadata.date.substring(0,10)
```

<div>
  <h2>Results for Week ${week_num} (${date})</h2>
</div>

```js
const sentinal_large_int = 99998
```

```js
const sentinal_large_int2 = 99999
```

```js
Inputs.table(scores.data, {
  columns: [
    "team_num",
    "display_name",
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
    "net_score"
  ],
  header: {
    team_num: "Team",
    display_name: htl.html`<div style="text-align: right;">${"Hole".toLocaleString("en")}
                           <div style="text-align: center;">${"Name".toLocaleString("en")}
                           <div style="float: right; color: #027148;">${"Par".toLocaleString("en")}`,
    
    hole_score_1: htl.html`<div>${"1".toLocaleString("en")}
                           <div style="color: #027148;">${"5".toLocaleString("en")}`,
    hole_score_2: htl.html`<div>${"2".toLocaleString("en")}
                           <div style="color: #027148;">${"3".toLocaleString("en")}`, 
    hole_score_3: htl.html`<div>${"3".toLocaleString("en")}
                           <div style="color: #027148;">${"4".toLocaleString("en")}`, 
    hole_score_4: htl.html`<div>${"4".toLocaleString("en")}
                           <div style="color: #027148;">${"4".toLocaleString("en")}`, 
    hole_score_5: htl.html`<div>${"5".toLocaleString("en")}
                           <div style="color: #027148;">${"4".toLocaleString("en")}`, 
    hole_score_6: htl.html`<div>${"6".toLocaleString("en")}
                           <div style="color: #027148;">${"4".toLocaleString("en")}`, 
    hole_score_7: htl.html`<div>${"7".toLocaleString("en")}
                           <div style="color: #027148;">${"4/5".toLocaleString("en")}`, 
    hole_score_8: htl.html`<div>${"8".toLocaleString("en")}
                           <div style="color: #027148;">${"3".toLocaleString("en")}`, 
    hole_score_9: htl.html`<div>${"9".toLocaleString("en")}
                           <div style="color: #027148;">${"5".toLocaleString("en")}`, 

    gross_score: htl.html`<div style="white-space: pre-wrap;">${"Gross\nScore".toLocaleString("en")}`,
    round_index: htl.html`<div style="white-space: pre-wrap;">${"Round\nIndex".toLocaleString("en")}`,
    net_score:htl.html`<div style="white-space: pre-wrap;">${"Net\nScore".toLocaleString("en")}`,
  },
  sort: "team_num",
  rows: 50, // Should only be 32 + 8 Team + Average = 41 rows, but seems like this needs to be higher to avoid scroll bars
  layout: "auto",
  format: {
    team_num: (d,i,data) => format_team_num(d,i,data),
    display_name: (d,i,data) => format_display_name(d,i,data),
    hole_score_1: (d,i,data) => format_hole_score(d,i,data,0),
    hole_score_2: (d,i,data) => format_hole_score(d,i,data,1),
    hole_score_3: (d,i,data) => format_hole_score(d,i,data,2),
    hole_score_4: (d,i,data) => format_hole_score(d,i,data,3),
    hole_score_5: (d,i,data) => format_hole_score(d,i,data,4),
    hole_score_6: (d,i,data) => format_hole_score(d,i,data,5),
    hole_score_7: (d,i,data) => format_hole_score(d,i,data,6),
    hole_score_8: (d,i,data) => format_hole_score(d,i,data,7),
    hole_score_9: (d,i,data) => format_hole_score(d,i,data,8),
    gross_score: (d,i,data) => format_gross_score(d,i,data),
    round_index: (d,i,data) => format_round_index(d,i,data),
    net_score: (d,i,data) => format_net_score(d,i,data),
  },
  align: {
    team_num: "center",
    display_name: "center",
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
    net_score: "center"
  }
})
```

```js
function format_team_num(d, i, data) {
    if (d == sentinal_large_int || d == sentinal_large_int2 ) {d=''}
      return htl.html`<div style="
        color: #000000;
        ">${d.toLocaleString("en")}`
}
```

```js
function format_hole_score(d, i, data) {
    var delta = data[i].hole_score_par_delta_array[arguments[3]]
    if (d == sentinal_large_int || d == sentinal_large_int2 ) {
        return htl.html`<div style="
        color: #000000;
        ">${''.toLocaleString("en")}`
    }
    else {
      if (data[i].display_name.includes("Average")) {
          return htl.html`<div style="
          color: #00008B;
          ">${d.toFixed(1).toLocaleString("en")}` 
      }
      else if (delta == -2) {
        return htl.html`<div style="
          color: #FF0000;
          border-width:4px;
          border-style:double;
          border-color:#FF0000;
          padding: 0em;
          border-radius: 50%;
          ">${d.toLocaleString("en")}🦅`
      }
      else if (delta == -1) {
        return htl.html`<div style="
          color: #FF0000;
          border-width:1px;
          border-style:solid;
          border-color:#FF0000;
          padding: 0em;
          border-radius: 50%;
          ">${d.toLocaleString("en")}`
      }
      else if (delta == 0) {
        return htl.html`<div style="
          color: #027148;
          background-color: #D1FFBD;
          border-radius: 40%;
          ">${d.toLocaleString("en")}`
      }
      else {
        return htl.html`<div style="
          color: #000000;
          ">${d.toLocaleString("en")}`
      }
    }
}
```

```js
function format_gross_score(d, i, data) {
    if (d == sentinal_large_int || d == sentinal_large_int2) {d=''}
    if (data[i].display_name.includes("Average")) {
        return htl.html`<div style="
        color: #00008B;
        ">${d.toLocaleString("en")}` 
    }
    else if (data[i].display_name.includes("Τeam")) { //T is greek character
        return htl.html`<div style="
        color: #000000;
        font-weight: bold;
        ">${d.toLocaleString("en")}` 
    }
    else if (data[i].low_gross_flag == true) {
        return htl.html`<div style="
        color: #000000;
        border-radius: 50%;
        background-color: #ADD8E6;
        background-image: radial-gradient(ellipse, #FFFFFF, #ADD8E6, #0000FF);
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
function format_round_index(d, i, data) {
    if (d != sentinal_large_int && d != sentinal_large_int2) {
        if (data[i].display_name.includes("Average")) {
          return htl.html`<div style="
          color: #00008B;
          ">${d.toFixed(1).toLocaleString("en")}` 
        }
        else if (data[i].display_name.includes("Τeam")) { //T is greek character
          return htl.html`<div style="
          color: #000000;
          font-weight: bold;
          ">${d.toFixed(1).toLocaleString("en")}` 
        }
        else {
          return htl.html`<div style="
          color: #000000;
          ">${d.toFixed(1).toLocaleString("en")}`
        }
    }
      else {
        return htl.html`<div style="
        color: #000000;
        ">${''.toLocaleString("en")}` 
      }
    }
```

```js
function format_net_score(d, i, data) {
    if (d == sentinal_large_int || d == sentinal_large_int2) {
      return htl.html`<div style="
        color: #000000;
        ">${''.toLocaleString("en")}`
    }
    else {
      if (data[i].display_name.includes("Average")) {
          return htl.html`<div style="
          color: #00008B;
          ">${d.toFixed(1).toLocaleString("en")}` 
      }
      else if (data[i].display_name.includes("Τeam")) { //T is greek character
          return htl.html`<div style="
          color: #000000;
          font-weight: bold;
          ">${d.toFixed(1).toLocaleString("en")}` 
      }
      else if (data[i].low_net_flag == true) {
          return htl.html`<div style="
          color: #000000;
          border-radius: 50%;
          background-color: 	#DA70D6;
          background-image: radial-gradient(ellipse, #FFFFFF, #FFFFFF, 	#DA70D6, 	#800080);
          ">${d.toFixed(1).toLocaleString("en")}`
      }
      else if (data[i].display_name == 'ΒLIND') {
          return htl.html`<div style="
          color: #808080;
          ">${d.toFixed(1).toLocaleString("en")}`
      }
      else {
        return htl.html`<div style="
          color: #000000;
          ">${d.toFixed(1).toLocaleString("en")}`
      }
    }
}
```

```js
function format_display_name(d, i, data) {
  if (d == "ΒLIND") { // Note B is Greek Character
    return htl.html`<div style="
        color: #808080;
        ">${d.toLocaleString("en")}`
  }
  else if (d.includes("Τeam")) { // Note T is Greek Character
      var rank_text = "(" + data[i].rank_text + ")"
      var highlight = "#FFFFFF"
      if (data[i].rank == 1) {highlight = "#D4AF37"}
      return htl.html`<div style="
        color: #000000;
        font-weight: bold;
        //text-align: right;
        border-radius: 10%;
        background-color: ${highlight};
        //border-top:1px solid #000;
        //border-bottom:1px solid #000;
        ">${d.toLocaleString("en")} ${rank_text}`
  }
  else if (d.includes("Average")) { 
      return htl.html`<div style="
        color: #00008B;
        ">${"Average".toLocaleString("en")}`
  }
  else {
    var event_text = '\n'
    if (data[i].event_info.event != "None") {
      var event_flag = true
      event_text = '\n' + data[i].event_info.event
    }
    if (event_flag || data[i].low_net_flag || data[i].low_gross_flag) {
      return htl.html`<div style="
        color: #000000;
        white-space: pre-wrap;
        ">🏌 ${d.toLocaleString("en")} ${event_text}`
    }
    else {
      return htl.html`<div style="
        color: #000000;
        ">${d.toLocaleString("en")}`
    }
  }
}
```

```js
const week_num = view(Inputs.radio(week_nums, {label: "Select Week", value: latest_week_num}))
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
