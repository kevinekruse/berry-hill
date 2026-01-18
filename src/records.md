```js
const scores = FileAttachment("/data/BerryHillRecords_Latest.csv").csv({typed: true});
```

<div>
  <h2>2025 Records</h2>
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
Inputs.table(scores, {
  columns: [
    "display_name",
    "rounds_in_2025",
    "season_low_gross",
    "season_low_net",
    "season_pars",
    "season_birdies",
    "season_eagles",
  ],
  header: {
    display_name:htl.html`<div style="white-space: pre-wrap;">${"Player\nName".toLocaleString("en")}`,
    rounds_in_2025:htl.html`<div style="white-space: pre-wrap;">${"Season\nRounds".toLocaleString("en")}`,
    season_low_gross:htl.html`<div style="white-space: pre-wrap;">${"Season\n Low Gross".toLocaleString("en")}`,
    season_low_net:htl.html`<div style="white-space: pre-wrap;">${"Season\n Low Net".toLocaleString("en")}`,
    season_pars:htl.html`<div style="white-space: pre-wrap;">${"Season\n Pars".toLocaleString("en")}`,
    season_birdies:htl.html`<div style="white-space: pre-wrap;">${"Season\n Birdies".toLocaleString("en")}`,
    season_eagles:htl.html`<div style="white-space: pre-wrap;">${"Season\n Eagles".toLocaleString("en")}`,
  },
  sort: "display_name",
  reverse: false,
  rows: 100,
  layout: "auto",
  format: {
    display_name: (d,i,data) => format_display_name(d,i,data),
    season_low_gross: (d,i,data) => format_season_low_gross(d,i,data),
    season_low_net: (d,i,data) => format_season_low_net(d,i,data),
    season_pars: (d,i,data) => format_season_pars(d,i,data),
    season_birdies: (d,i,data) => format_season_birdies(d,i,data),
    season_eagles: (d,i,data) => format_season_eagles(d,i,data),
  },
  align: {
    display_name: "center",
    rounds_in_2025: "center",
    season_low_gross: "center",
    season_low_net: "center",
    season_pars: "center",
    season_birdies: "center",
    season_eagles: "center",
  }
})
```

```js
function format_display_name(d, i, data) {
  if (data[i].captain == "y") {
    return htl.html`<div style="
        ">${d.toLocaleString("en")} (Captain)`
  }
  else {
    return htl.html`<div style="
        ">${d.toLocaleString("en")}`
  }
}
```

```js
function format_season_pars (d, i, data) {
    if (data[i].season_pars_max_flag == "True") {
      return htl.html`<div style="
          color: #027148;
          background-color: #D1FFBD;
          border-radius: 40%;
          ">${d.toLocaleString("en")}`
    }
    else {
      return htl.html`<div style="
        color: #000000
        ">${d.toLocaleString("en")}`
    }
}
```

```js
function format_season_birdies (d, i, data) {
    if (data[i].season_birdies_max_flag == "True") {
      return htl.html`<div style="
          color: #FF0000;
          border-width:1px;
          border-style:solid;
          border-color:#FF0000;
          padding: 0em;
          border-radius: 50%;
          ">${d.toLocaleString("en")}`
    }
    else {
      return htl.html`<div style="
        color: #000000
        ">${d.toLocaleString("en")}`
    }
}
```

```js
function format_season_eagles (d, i, data) {
    if (data[i].season_eagles_max_flag == "True") {
      return htl.html`<div style="
          color: #FF0000;
          border-width:4px;
          border-style:double;
          border-color:#FF0000;
          padding: 0em;
          border-radius: 50%;
          ">${d.toLocaleString("en")}🦅`
    }
    else {
      return htl.html`<div style="
        color: #000000
        ">${d.toLocaleString("en")}`
    }
}
```

```js
function format_season_low_gross (d, i, data) {
    if (data[i].season_low_gross_flag == "True") {
      return htl.html`<div style="
        color: #000000;
        border-radius: 50%;
        background-color: #ADD8E6;
        background-image: radial-gradient(ellipse, #FFFFFF, #ADD8E6, #0000FF);
        ">${d.toLocaleString("en")}`
    }
    else {
      return htl.html`<div style="
        color: #000000
        ">${d.toLocaleString("en")}`
    }
}
```

```js
function format_season_low_net (d, i, data) {
    if (data[i].season_low_net_flag == "True") {
      return htl.html`<div style="
          color: #000000;
          border-radius: 50%;
          background-color: 	#DA70D6;
          background-image: radial-gradient(ellipse, #FFFFFF, #FFFFFF, 	#DA70D6, 	#800080);
          ">${d.toFixed(1).toLocaleString("en")}`
    }
    else {
      return htl.html`<div style="
        color: #000000
        ">${d.toLocaleString("en")}`
    }
}
```