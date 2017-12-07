import chroma from 'chroma-js';
import { Gender } from 'util/constants';

/**
 * Color scales for the different gender teams
 * 
 * These colors are named ColorBrewer scales that work with the chroma library
 * Ref: http://colorbrewer2.org/
 */
const genderColorScales = {
  [Gender.Mens]: 'Blues',
  [Gender.Ladies]: 'Greens',
  [Gender.Mixed]: 'Oranges',
};

/**
 * Create (and return) a color scale for the specified team gender.
 * 
 * The scale 'domain' (min/max) is determined by the number of teams of that gender.
 */
const getGenderColorScale = (teams, gender) => {
  const genderTeams = teams.filter(t => t.gender === gender);
  return {
    teams: genderTeams,
    scale: chroma.scale(genderColorScales[gender]).domain([0, genderTeams.length]),
  };
};

/**
 * Get a dictionary of color scales, keyed by team gender, for the specified list of teams
 */
const getTeamColorScales = (teams) => {
  const colorScales = {};

  [Gender.Mens, Gender.Ladies, Gender.Mixed].forEach((gender) => {
    colorScales[gender] = getGenderColorScale(teams, gender);
  });

  return colorScales;
};

/**
 * Get the color representing the given team.
 * 
 * Note: the color scales dictionary (created with 'getTeamColorScales') and the list of teams
 *       must be supplied as well.
 */
const getTeamColor = (colorScales, teams, teamSlug) => {
  const team = teams.find(t => t.slug === teamSlug);
  const index = colorScales[team.gender].teams.findIndex(t => t.slug === teamSlug);
  return colorScales[team.gender].scale(colorScales[team.gender].teams.length - index);
};

module.exports = {
  getTeamColorScales,
  getTeamColor,
};
