const fs=require('fs');
const path='src/data/BerryHillScores_All_Latest.csv';
const data=fs.readFileSync(path,'utf8').split('\n');
const header=data[0].split(',');
const rows=data.slice(1);
const bydate={};
for(const line of rows){
  if(!line) continue;
  // naive CSV split - fields may contain commas, but our file seems consistent
  const cols=line.split(/,(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)/);
  const obj={};
  for(let i=0;i<header.length;i++) obj[header[i]]=cols[i]||'';
  const year=parseInt(parseFloat(obj['season_year']||0));
  if(year!==2026) continue;
  const team=obj['team_num']||'';
  if(!(team==='6' || team==='6.0')) continue;
  const date=obj['date']||'';
  if(!date.includes('2026-07')) continue;
  const net=parseFloat(obj['net_score']);
  if(!isFinite(net)) continue;
  if(!(date in bydate)) bydate[date]= {sum:0,count:0};
  bydate[date].sum+=net; bydate[date].count+=1;
}
const keys=Object.keys(bydate).sort();
if(keys.length===0) console.log('no entries for team 6 in July 2026');
for(const k of keys) console.log(k,'sum=',bydate[k].sum,'count=',bydate[k].count);
