import { AltOutcome } from 'util/constants';

/**
 * Utility object for common logic related to Appearances
 */
const Appearance = {
  /**
   * Map a list of appearances (received from the server) to a list of
   * more verbose objects (with cards expanded to individual boolean props) 
   */
  initAppearances(appearances) {
    return appearances.map((app) => {
      const s = app.member.split(':');
      return {
        id: s[0],
        name: s[1],
        member: app.member,
        greenCard: app.cards.includes('g'),
        yellowCard: app.cards.includes('y'),
        redCard: app.cards.includes('r'),
        goals: app.goals,
      };
    });
  },

  /**
   * Maps a list of appearances to a list of AppearanceInput objects
   * 
   * Note: If the match is cancelled/postponed etc, we'll return an empty
   * array of appearances instead.
   * 
   * Ref: matches/schema/AppearanceInput
   */
  toAppearanceInputArray(appearances, altOutcome) {
    if (altOutcome && altOutcome !== AltOutcome.Abandoned) {
      return [];
    }
    return appearances.map(app => ({
      memberId: parseInt(app.id, 10),
      goals: app.goals,
      greenCard: app.greenCard,
      yellowCard: app.yellowCard,
      redCard: app.redCard,
    }));
  },
};

export default Appearance;
