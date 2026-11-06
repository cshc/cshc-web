import chroma from 'chroma-js';

/**
 * Categorical team colors, assigned in this (fixed) order.
 *
 * The order matters: it has been validated so that neighbouring colors remain distinguishable
 * for people with red-green or blue-yellow color blindness.
 */
const teamColors = [
  '#2a78d6', // blue
  '#eb6834', // orange
  '#1baf7a', // aqua
  '#eda100', // yellow
  '#e87ba4', // magenta
  '#008300', // green
  '#6250d6', // violet
  '#e34948', // red
  '#b20d8f', // fuchsia
  '#813a30', // brown
];

/**
 * Get a dictionary of colors, keyed by team slug, for the specified list of teams.
 *
 * Colors are assigned in the order the teams are supplied. If there are more teams than colors,
 * the palette is re-used with progressively darker variants.
 */
const getTeamColors = teams => teams.reduce((acc, team, index) => {
  const color = teamColors[index % teamColors.length];
  const variant = Math.floor(index / teamColors.length);
  acc[team.slug] = variant ? chroma(color).darken(0.8 * variant).hex() : color;
  return acc;
}, {});

module.exports = {
  getTeamColors,
};
