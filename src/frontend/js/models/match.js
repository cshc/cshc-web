import { isPast } from 'date-fns';
import sortBy from 'lodash/sortBy';
import reduce from 'lodash/reduce';
import { toTitleCase } from 'util/cshc';
import { HomeAway, MatchAward, AltOutcome } from 'util/constants';

/**
 * Utility object for common logic related to a match.
 */
const Match = {
  WALKOVER_SCORE_W1: 3,
  WALKOVER_SCORE_W2: 5,
  WALKOVER_SCORE_L: 0,

  resultErrors(result) {
    const errors = [];
    switch (result.altOutcome) {
      case AltOutcome.Walkover:
        if (!Match.isWalkoverScore(result)) {
          errors.push('A walk-over score must be 3-0, 5-0, 0-3 or 0-5');
        }
        if (result.ourHtScore !== undefined || result.oppHtScore !== undefined) {
          errors.push('Half-time scores are not valid for walkover matches');
        }
        break;

      case AltOutcome.Cancelled:
      case AltOutcome.Postponed:
      case AltOutcome.BYE:
        if (result.ourScore || result.oppScore || result.ourHtScore || result.oppHtScore) {
          errors.push('A cancelled, postponed or BYE match should not have scores');
        }
        break;

      default:
        // You can't specify one score without the other
        if (result.ourScore === undefined || result.oppScore === undefined) {
          errors.push('Both scores must be provided');
        } else if (result.ourHtScore === undefined || result.oppHtScore === undefined) {
          errors.push('Both half-time scores must be provided');
        } else if (result.ourHtScore > result.ourScore || result.oppHtScore > result.oppScore) {
          // Half-time scores must be <= the final scores
          errors.push('Half-time scores cannot be greater than final scores');
        }
        break;
    }

    return errors;
  },

  isWalkoverScore(result) {
    if (
      [Match.WALKOVER_SCORE_W1, Match.WALKOVER_SCORE_W2].find(
        v => v === parseInt(result.ourScore, 10),
      )
    ) {
      return result.oppScore === Match.WALKOVER_SCORE_L;
    } else if (
      [Match.WALKOVER_SCORE_W1, Match.WALKOVER_SCORE_W2].find(
        v => v === parseInt(result.oppScore, 10),
      )
    ) {
      return result.ourScore === Match.WALKOVER_SCORE_L;
    }
    return false;
  },

  isHome(match) {
    return match.homeAway === HomeAway.Home;
  },

  isPast(match) {
    return isPast(`${match.date} ${match.time}`);
  },

  datetime(match) {
    if (!match) return undefined;
    return new Date(`${match.date} ${match.time}`);
  },

  simpleVenueName(match) {
    if (match.venue) {
      if (Match.isHome(match)) {
        return match.venue.shortName || match.venue.name;
      }
      return 'Away';
    } else if (Match.isPast(match)) return '???';
    return 'TBD';
  },

  finalScoresProvided(match) {
    return (
      (match.ourScore === 0 || match.ourScore > 0) && (match.oppScore === 0 || match.oppScore > 0)
    );
  },

  scoreDisplay(match) {
    if (match.altOutcome) {
      return toTitleCase(match.altOutcome);
    }
    if (!Match.finalScoresProvided(match)) {
      return '-';
    }
    return `${match.ourScore}-${match.oppScore}`;
  },

  resultClass(match) {
    if (match.altOutcome || !Match.finalScoresProvided(match)) return '';
    if (match.ourScore > match.oppScore) return 'g-bg-green g-color-white';
    else if (match.ourScore < match.oppScore) return 'g-bg-red g-color-white';
    return 'g-bg-black-opacity-0_3 g-color-white';
  },

  scorers(match) {
    if (!match.appearances || !match.appearances.results) return [];
    return sortBy(match.appearances.results.filter(a => a.goals > 0), m => -m.goals);
  },

  mom(match) {
    if (!match.awardWinners || !match.awardWinners.results) return [];
    return match.awardWinners.results.filter(aw => aw.award.name === MatchAward.MOM);
  },

  lom(match) {
    if (!match.awardWinners || !match.awardWinners.results) return [];
    return match.awardWinners.results.filter(aw => aw.award.name === MatchAward.LOM);
  },

  toResultsAndFixtures(matches) {
    const matchStructure = {
      results: [],
      fixtures: [],
    };
    // Sort by past results vs future fixtures and by team
    reduce(
      matches.results,
      (acc, match) => {
        const list = Match.isPast(match) ? acc.results : acc.fixtures;
        let teamMatches = list.find(md => md.team.id === match.ourTeam.id);
        if (!teamMatches) {
          teamMatches = { team: match.ourTeam, matches: [] };
          list.push(teamMatches);
        }
        teamMatches.matches.push(match);
        return acc;
      },
      matchStructure,
    );
    // Sort by team position
    matchStructure.results = sortBy(matchStructure.results, ['team.position']);
    matchStructure.fixtures = sortBy(matchStructure.fixtures, ['team.position']);
    return matchStructure;
  },
};

export default Match;
