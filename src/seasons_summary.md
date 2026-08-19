<div>
  <h2>Seasons Summary</h2>
</div>

```js
const seasonAverages = await FileAttachment("data/season_averages.csv").csv({typed: true})
const seasonRainoutsBlinds = await FileAttachment("data/season_rainouts_blinds.csv").csv({typed: true})
```

```js
const rainoutBySeason = new Map(
  seasonRainoutsBlinds.map(r => {
    const season = String(r.season_year || r.season || '').replace(/,/g, '')
    const weatherCancels = r.weeks_cancelled_due_to_weather !== undefined && r.weeks_cancelled_due_to_weather !== null && r.weeks_cancelled_due_to_weather !== ''
      ? Number(r.weeks_cancelled_due_to_weather)
      : null
    const blinds = r.extra_blinds !== undefined && r.extra_blinds !== null && r.extra_blinds !== ''
      ? Number(r.extra_blinds)
      : null
    const blindPerentage = r.blind_perentage !== undefined && r.blind_perentage !== null && r.blind_perentage !== ''
      ? Number(r.blind_perentage)
      : null
    const avgHighTempTuesdays = r.avg_temp_tuesday_may_aug_bridgeton_mo !== undefined && r.avg_temp_tuesday_may_aug_bridgeton_mo !== null && r.avg_temp_tuesday_may_aug_bridgeton_mo !== ''
      ? Number(r.avg_temp_tuesday_may_aug_bridgeton_mo)
      : null
    const avgHighHeatIndexTuesdays = r.avg_heat_index_tuesday_may_aug_bridgeton_mo !== undefined && r.avg_heat_index_tuesday_may_aug_bridgeton_mo !== null && r.avg_heat_index_tuesday_may_aug_bridgeton_mo !== ''
      ? Number(r.avg_heat_index_tuesday_may_aug_bridgeton_mo)
      : null
    return [season, {
      weather_cancels: weatherCancels,
      blinds,
      blind_perentage: blindPerentage,
      avg_high_temp_tuesdays: avgHighTempTuesdays,
      avg_high_heat_index_tuesdays: avgHighHeatIndexTuesdays
    }]
  })
)

const rows = seasonAverages.map(r => ({
  season: String(r.season_year || r.season || '').replace(/,/g, ''),
  rounds: r.rounds !== undefined && r.rounds !== null && r.rounds !== '' ? Number(r.rounds) : null,
  teams: r.teams !== undefined && r.teams !== null && r.teams !== '' ? Number(r.teams) : null,
  weather_cancels: rainoutBySeason.get(String(r.season_year || r.season || '').replace(/,/g, ''))?.weather_cancels ?? null,
  blinds: rainoutBySeason.get(String(r.season_year || r.season || '').replace(/,/g, ''))?.blinds ?? null,
  blind_perentage: rainoutBySeason.get(String(r.season_year || r.season || '').replace(/,/g, ''))?.blind_perentage ?? null,
  avg_high_temp_tuesdays: rainoutBySeason.get(String(r.season_year || r.season || '').replace(/,/g, ''))?.avg_high_temp_tuesdays ?? null,
  avg_high_heat_index_tuesdays: rainoutBySeason.get(String(r.season_year || r.season || '').replace(/,/g, ''))?.avg_high_heat_index_tuesdays ?? null,
  gross_avg: r.gross_avg !== undefined && r.gross_avg !== null && r.gross_avg !== '' ? Number(r.gross_avg) : null,
  net_avg: r.net_avg !== undefined && r.net_avg !== null && r.net_avg !== '' ? Number(r.net_avg) : null,
  round_index_avg: r.round_index_avg !== undefined && r.round_index_avg !== null && r.round_index_avg !== '' ? Number(r.round_index_avg) : null
}))

if (rows.length === 0) {
  display(htl.html`<div style="color:var(--theme-foreground-muted);">No season summary data available.</div>`)
} else {
  const tableNode = Inputs.table(rows, {
    columns: ["season", "rounds", "teams", "weather_cancels", "blinds", "blind_perentage", "gross_avg", "net_avg", "round_index_avg", "avg_high_temp_tuesdays", "avg_high_heat_index_tuesdays"],
    header: {
      season: "Season",
      rounds: "Rounds",
      teams: "Teams",
      weather_cancels: "Weather Cancels",
      blinds: "Blinds",
      blind_perentage: "Blind Percentage",
      avg_high_temp_tuesdays: "Average High Temp Tuesdays",
      avg_high_heat_index_tuesdays: "Average High Heat Index Tuesdays",
      gross_avg: "Gross Avg",
      net_avg: "Net Avg",
      round_index_avg: "Round Index Average"
    },
    format: {
      blind_perentage: d => d == null ? '' : `${(d * 100).toFixed(1)}%`,
      avg_high_temp_tuesdays: d => d == null ? '' : d.toFixed(1),
      avg_high_heat_index_tuesdays: d => d == null ? '' : d.toFixed(1),
      gross_avg: d => d == null ? '' : d.toFixed(2),
      net_avg: d => d == null ? '' : d.toFixed(2),
      round_index_avg: d => d == null ? '' : d.toFixed(2)
    },
    align: {
      season: "left",
      rounds: "center",
      teams: "center",
      weather_cancels: "center",
      blinds: "center",
      blind_perentage: "center",
      avg_high_temp_tuesdays: "center",
      avg_high_heat_index_tuesdays: "center",
      gross_avg: "center",
      net_avg: "center",
      round_index_avg: "center"
    },
    rows: 20,
    layout: "auto"
  })

  display(tableNode)
}
```