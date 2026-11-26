# Temp Team 5 Data

```js
const allScores = await FileAttachment("data/BerryHillScores_Rounds_NoBlind.csv").csv({typed: true});

const team5Scores = allScores
  .filter((row) =>
    String(row.row_type || "").toLowerCase() === "round" &&
    Number(row.season_year) === 2026 &&
    Number(row.team_num) === 5 &&
    Number.isFinite(Number(row.net_score))
  )
  .map((row) => ({
    ...row,
    date: row.date ? String(row.date).slice(0, 10) : "",
    week_num: Number(row.week_num),
    gross_score: Number(row.gross_score),
    round_index: Number(row.round_index),
    net_score: Number(row.net_score)
  }))
  .sort((left, right) =>
    left.display_name.localeCompare(right.display_name) ||
    left.week_num - right.week_num
  );

const playerAverages = Array.from(
  team5Scores.reduce((players, row) => {
    const player = players.get(row.display_name) || {
      display_name: row.display_name,
      rounds: 0,
      netTotal: 0,
      session1Rounds: 0,
      session1NetTotal: 0,
      session2Rounds: 0,
      session2NetTotal: 0
    };
    player.rounds += 1;
    player.netTotal += row.net_score;
    if (row.week_num >= 1 && row.week_num <= 8) {
      player.session1Rounds += 1;
      player.session1NetTotal += row.net_score;
    } else if (row.week_num >= 9 && row.week_num <= 16) {
      player.session2Rounds += 1;
      player.session2NetTotal += row.net_score;
    }
    players.set(row.display_name, player);
    return players;
  }, new Map()).values()
)
  .map((player) => ({
    display_name: player.display_name,
    rounds: player.rounds,
    average_net_score: player.netTotal / player.rounds,
    session_1_average_net_score: player.session1Rounds ? player.session1NetTotal / player.session1Rounds : null,
    session_2_average_net_score: player.session2Rounds ? player.session2NetTotal / player.session2Rounds : null
  }))
  .sort((left, right) => left.average_net_score - right.average_net_score);
```

## Season Average Net Scores

```js
Inputs.table(playerAverages, {
  columns: ["display_name", "rounds", "session_1_average_net_score", "session_2_average_net_score", "average_net_score"],
  header: {
    display_name: "Player",
    rounds: "Rounds",
    session_1_average_net_score: "Session 1 Average Net",
    session_2_average_net_score: "Session 2 Average Net",
    average_net_score: "Average Net Score"
  },
  format: {
    average_net_score: (value) => value.toFixed(1),
    session_1_average_net_score: (value) => value === null ? "" : value.toFixed(1),
    session_2_average_net_score: (value) => value === null ? "" : value.toFixed(1)
  },
  align: {
    rounds: "center",
    session_1_average_net_score: "center",
    session_2_average_net_score: "center",
    average_net_score: "center"
  }
})
```

## 2026 Scores

```js
Inputs.table(team5Scores, {
  columns: ["display_name", "date", "week_num", "gross_score", "round_index", "net_score"],
  header: {
    display_name: "Player",
    date: "Date",
    week_num: "Week",
    gross_score: "Gross Score",
    round_index: "Round Index",
    net_score: "Net Score"
  },
  format: {
    gross_score: (value) => value.toFixed(1),
    round_index: (value) => value.toFixed(1),
    net_score: (value) => value.toFixed(1)
  },
  align: {
    date: "center",
    week_num: "center",
    gross_score: "center",
    round_index: "center",
    net_score: "center"
  }
})
```
