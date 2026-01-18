// See https://observablehq.com/framework/config for documentation.
export default {
  // The app’s title; used in the sidebar and webpage titles.
  title: "Berry Hill Golf",

  // The pages and sections in the sidebar. If you don’t specify this option,
  // all pages will be listed in alphabetical order. Listing pages explicitly
  // lets you organize them into sections and have unlisted pages.
  pages: [
    {
      name: "",
      pages: [
        {name: "Weekly Results", path: "/weekly_results"},
        {name: "Standings", path: "/standings"},
        {name: "Roster", path: "/roster"},
        {name: "Player Data", path: "/player_data"},
        {name: "Season Records", path: "/records"},
        {name: "Hole Averages", path: "/hole_data"},
        //{name: "Scoring History", path: "/historical_data"},
      ]
    }
  ],

  // Content to add to the head of the page, e.g. for a favicon:
  head: '<link rel="icon" href="pngtree-sport-ball-golf-ball-png-png-image_13030039.png" type="image/png" sizes="32x32">',

  // The path to the source root.
  root: "src",

  // Some additional configuration options and their defaults:
  //dark theme options coffee deep-space ink midnight near-midnight (default) ocean-floor slate stark sun-faded
 
  theme: "light", // try "light", "dark", "slate", etc.
   //header: "Berry Hill Golf", // what to show in the header (HTML)
   footer: "Built with Observable.", // what to show in the footer (HTML)
   sidebar: true, // whether to show the sidebar
   toc: false, // whether to show the table of contents
   pager: false, // whether to show previous & next links in the footer
   output: "dist", // path to the output root for build
  // search: true, // activate search
  // linkify: true, // convert URLs in Markdown to links
  // typographer: false, // smart quotes and other typographic improvements
  // cleanUrls: true, // drop .html from URLs
};
