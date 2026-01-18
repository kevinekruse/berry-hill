<div>
  <h2>Standings for ${selected_season_year}</h2>
</div>

```js
const standings_session_1 = FileAttachment("data/BerryHill_Team_Latest_Session_1.csv").csv({typed: true});
```

```js
const standings_session_2 = FileAttachment("data/BerryHill_Team_Latest_Session_2.csv").csv({typed: true});
```

```js
const standings_session_3 = FileAttachment("data/BerryHill_Team_Latest_Session_3.csv").csv({typed: true});
```

```js
//const selected_season_year = parseInt(view(Inputs.radio(["2020","2021","2022","2023","2024","2025"], {label: "Select Year", value: "2025"})))
//const selected_season_year = view(Inputs.radio([2020,2021,2022,2023,2024,2025], {label: "Select Year", value: 2025, format: x => String(x)}))
const selected_season_year = 2025
```

```js
const selected_standings_session_1 = standings_session_1.filter((d) => selected_season_year == d.season_year)
```

```js
const selected_standings_session_2 = standings_session_2.filter((d) => selected_season_year == d.season_year)
```

```js
const selected_standings_session_3 = standings_session_3.filter((d) => selected_season_year == d.season_year)
```
<div>
  <h2>Session 1</h2>
</div>

```js
Inputs.table(selected_standings_session_1, {
  columns: [
  'team_num',
  'session_net_sum',
  //'session_blinds_sum',
  'session_rank_sum',
  'rank_01',
  'rank_02',
  'rank_03',
  'rank_04',
  'rank_05',
  'rank_06',
  'rank_07',
  'rank_08'
  ],
  header: {
    team_num: "Team",
    session_net_sum: htl.html`<div style="white-space: pre-wrap;">${"Session\nNet Score".toLocaleString("en")}`,
    //session_blinds_sum: htl.html`<div style="white-space: pre-wrap;">${"Session\nBlinds".toLocaleString("en")}`,
    session_rank_sum: htl.html`<div style="white-space: pre-wrap;">${"Session\nPoints".toLocaleString("en")}`,
    rank_01: htl.html`<div style="white-space: pre-wrap;">${"Week 1\nPoints".toLocaleString("en")}`,
    rank_02: htl.html`<div style="white-space: pre-wrap;">${"Week 2\nPoints".toLocaleString("en")}`,
    rank_03: htl.html`<div style="white-space: pre-wrap;">${"Week 3\nPoints".toLocaleString("en")}`,
    rank_04: htl.html`<div style="white-space: pre-wrap;">${"Week 4\nPoints".toLocaleString("en")}`,
    rank_05: htl.html`<div style="white-space: pre-wrap;">${"Week 5\nPoints".toLocaleString("en")}`,
    rank_06: htl.html`<div style="white-space: pre-wrap;">${"Week 6\nPoints".toLocaleString("en")}`,
    rank_07: htl.html`<div style="white-space: pre-wrap;">${"Week 7\nPoints".toLocaleString("en")}`,
    rank_08: htl.html`<div style="white-space: pre-wrap;">${"Week 8\nPoints".toLocaleString("en")}`
  },
  sort: "team_num",
  reverse: false,
  rows: 10,
  layout: "auto",
  
  format: {
    team_num: (d,i,data) => format_team_num_session_1(d,i,data),
    //session_blinds_sum: (d,i,data) => format_num_blinds(d,i,data),

  },

  align: {
    team_num: "center",
    session_net_sum: "center",
    //session_blinds_sum: "center",
    session_rank_sum: "center",
    rank_01: "center",
    rank_02: "center",
    rank_03: "center",
    rank_04: "center",
    rank_05: "center",
    rank_06: "center",
    rank_07: "center",
    rank_08: "center"
  }
})
```
<div>
  <h2>Session 2</h2>
</div>

```js
Inputs.table(selected_standings_session_2, {
  columns: [
  'team_num',
  'session_net_sum',
  //session_blinds_sum',
  'session_rank_sum',
  'rank_09',
  'rank_10',
  'rank_11',
  'rank_12',
  'rank_13',
  'rank_14',
  'rank_15',
  'rank_16'
  ],
  header: {
    team_num: "Team",
    session_net_sum: htl.html`<div style="white-space: pre-wrap;">${"Session\nNet Score".toLocaleString("en")}`,
    //session_blinds_sum: htl.html`<div style="white-space: pre-wrap;">${"Session\nBlinds".toLocaleString("en")}`,
    session_rank_sum: htl.html`<div style="white-space: pre-wrap;">${"Session\nPoints".toLocaleString("en")}`,
    rank_09: htl.html`<div style="white-space: pre-wrap;">${"Week 9\nPoints".toLocaleString("en")}`,
    rank_10: htl.html`<div style="white-space: pre-wrap;">${"Week 10\nPoints".toLocaleString("en")}`,
    rank_11: htl.html`<div style="white-space: pre-wrap;">${"Week 11\nPoints".toLocaleString("en")}`,
    rank_12: htl.html`<div style="white-space: pre-wrap;">${"Week 12\nPoints".toLocaleString("en")}`,
    rank_13: htl.html`<div style="white-space: pre-wrap;">${"Week 13\nPoints".toLocaleString("en")}`,
    rank_14: htl.html`<div style="white-space: pre-wrap;">${"Week 14\nPoints".toLocaleString("en")}`,
    rank_15: htl.html`<div style="white-space: pre-wrap;">${"Week 15\nPoints".toLocaleString("en")}`,
    rank_16: htl.html`<div style="white-space: pre-wrap;">${"Week 16\nPoints".toLocaleString("en")}`
  },
  sort: "team_num",
  reverse: false,
  rows: 12,
  layout: "auto",
  
  format: {
    team_num: (d,i,data) => format_team_num_session_2(d,i,data),
    //session_blinds_sum: (d,i,data) => format_num_blinds(d,i,data),

  },

  align: {
    team_num: "center",
    session_net_sum: "center",
    //session_blinds_sum: "center",
    session_rank_sum: "center",
    rank_09: "center",
    rank_10: "center",
    rank_11: "center",
    rank_12: "center",
    rank_13: "center",
    rank_14: "center",
    rank_15: "center",
    rank_16: "center"
  }
})
```
<div>
  <h2>Playoffs</h2>
</div>

```js
Inputs.table(selected_standings_session_3, {
  columns: [
  'team_num',
  'session_net_sum',
  //'session_blinds_sum'
  ],
  header: {
    team_num: "Team",
    session_net_sum: htl.html`<div style="white-space: pre-wrap;">${"Week 17 \nNet Score".toLocaleString("en")}`,
    //session_blinds_sum: htl.html`<div style="white-space: pre-wrap;">${"Week 17 \nBlinds".toLocaleString("en")}`,
    session_rank_sum: htl.html`<div style="white-space: pre-wrap;">${"Week 17 \nPoints".toLocaleString("en")}`,
    rank_01: htl.html`<div style="white-space: pre-wrap;">${"Week 1\nPoints".toLocaleString("en")}`,
    rank_02: htl.html`<div style="white-space: pre-wrap;">${"Week 2\nPoints".toLocaleString("en")}`,
    rank_03: htl.html`<div style="white-space: pre-wrap;">${"Week 3\nPoints".toLocaleString("en")}`,
    rank_04: htl.html`<div style="white-space: pre-wrap;">${"Week 4\nPoints".toLocaleString("en")}`,
    rank_05: htl.html`<div style="white-space: pre-wrap;">${"Week 5\nPoints".toLocaleString("en")}`,
    rank_06: htl.html`<div style="white-space: pre-wrap;">${"Week 6\nPoints".toLocaleString("en")}`,
    rank_07: htl.html`<div style="white-space: pre-wrap;">${"Week 7\nPoints".toLocaleString("en")}`,
    rank_08: htl.html`<div style="white-space: pre-wrap;">${"Week 8\nPoints".toLocaleString("en")}`
  },
  sort: "team_num",
  reverse: false,
  rows: 10,
  layout: "auto",
  
  format: {
    team_num: (d,i,data) => format_team_num_finals(d,i,data),
    //session_blinds_sum: (d,i,data) => format_num_blinds(d,i,data),

  },

  align: {
    team_num: "center",
    session_net_sum: "center",
    //session_blinds_sum: "center",
    session_rank_sum: "center",
    rank_01: "center",
    rank_02: "center",
    rank_03: "center",
    rank_04: "center",
    rank_05: "center",
    rank_06: "center",
    rank_07: "center",
    rank_08: "center"
  }
})
```

```js
const session_1_rank = ["8th", "1st", "2nd", "3rd", "4th", "6th", "7th", "5th"];
```

```js
function format_team_num_session_1(d, i, data) {
      var num = Number(d);
      var rank_text = "(" + session_1_rank[i] + ")"
      var highlight = "#FFFFFF"
      if (session_1_rank[i] == "1st") {highlight = "#D4AF37"}
      return htl.html`<div style="
        color: #000000;
        background-color: ${highlight};
        ">${num.toLocaleString("en")} ${rank_text}`

}
```

```js
const session_2_rank = ["6th", "5th", "3rd", "4th", "2nd", "1st", "8th", "7th"];
```

```js
function format_team_num_session_2(d, i, data) {
      var num = Number(d);
      var rank_text = "(" + session_2_rank[i] + ")"
      var highlight = "#FFFFFF"
      if (session_2_rank[i] == "1st") {highlight = "#D4AF37"}
      return htl.html`<div style="
        color: #000000;
        background-color: ${highlight};
        ">${num.toLocaleString("en")} ${rank_text}`

}
```

```js
const finals_rank = ["8th", "Champions", "3rd", "5th", "4th", "2nd", "7th", "6th"];
```

```js
function format_team_num_finals(d, i, data) {
      var num = Number(d);
      var rank_text = "(Season " + finals_rank[i] + ")"
      var highlight = "#FFFFFF"
      if (finals_rank[i] == "Champions") {highlight = "#D4AF37"}
      return htl.html`<div style="
        color: #000000;
        background-color: ${highlight};
        ">${num.toLocaleString("en")} ${rank_text}`

}
```

```js
function format_num_blinds(d, i, data) {
      var num = Number(d);
      return htl.html`<div style="
        color: #000000;
        ">${num.toLocaleString("en")}`
}
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
