```js
const scores = FileAttachment("/data/BerryHillRoster_Latest.csv").csv({typed: true});
```

<div>
  <h2>2025 Roster</h2>
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
    "team_num",
    "display_name",
    "tee",
    "rounds_in_2023",
    "rounds_in_2024",
    "rounds_in_2025",
    "handicap_type",
    "handicap"
  ],
  header: {
    team_num:htl.html`<div style="white-space: pre-wrap;">${"Team\nNumber".toLocaleString("en")}`,
    display_name:htl.html`<div style="white-space: pre-wrap;">${"Player\nName".toLocaleString("en")}`,
    tee:htl.html`<div style="white-space: pre-wrap;">${"Tee".toLocaleString("en")}`,
    rounds_in_2023:htl.html`<div style="white-space: pre-wrap;">${"2023\nRounds".toLocaleString("en")}`,
    rounds_in_2024:htl.html`<div style="white-space: pre-wrap;">${"2024\nRounds".toLocaleString("en")}`,
    rounds_in_2025:htl.html`<div style="white-space: pre-wrap;">${"2025\nRounds".toLocaleString("en")}`,
    handicap_type:htl.html`<div style="white-space: pre-wrap;">${"Handicap\nType".toLocaleString("en")}`,
    handicap:htl.html`<div style="white-space: pre-wrap; color: ${Observable_Orange}">${"Handicap".toLocaleString("en")}`,
  },
  sort: "team_num",
  reverse: false,
  rows: 100,
  layout: "auto",
  format: {
    display_name: (d,i,data) => format_display_name(d,i,data),
    handicap: (d,i,data) => format_handicap_index(d,i,data),
  },
  align: {
    team_num: "center",
    display_name: "center",
    tee: "center",
    rounds_in_2023: "center",
    rounds_in_2024: "center",
    rounds_in_2025: "center",
    handicap_type: "center",
    handicap: "center",
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
function format_handicap_index(d, i, data) {
    if (d == '') {
        return htl.html`<div style="
        ">${"".toLocaleString("en")}` 
    }
    else {
      return htl.html`<div style="
        color: ${Observable_Orange};
        ">${d.toFixed(2).toLocaleString("en")}`
    }
}
```