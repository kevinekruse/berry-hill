const fs = require('fs');
const path = 'src/data/BerryHillScores_All_Latest.csv';
const data = fs.readFileSync(path, 'utf8').split('\n');
const header = data[0].split(',');
const rows = data.slice(1);
const targetDate = '2026-07-28  16:00:00';
for (const line of rows) {
  if (!line) continue;
  const cols = line.split(/,(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)/);
  const obj = {};
  for (let i = 0; i < header.length; i++) obj[header[i]] = cols[i] || '';
  const year = parseInt(parseFloat(obj['season_year'] || 0));
  if (year !== 2026) continue;
  if (!(obj['team_num'] === '6' || obj['team_num'] === '6.0')) continue;
  const date = obj['date'] || '';
  if (date !== targetDate) continue;
  const name = obj['display_name'] || '';
  const net = parseFloat(obj['net_score']);
  if (!isFinite(net)) continue;
  console.log(name, net);
}
