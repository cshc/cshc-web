import Member from 'models/member';

/**
 * Utility object for common logic related to Match Award Winners
 */
const MatchAwardWinner = {
  /**
   * Returns true if the given award object is valid
   */
  isValid(awardWinner) {
    return (awardWinner.member || awardWinner.awardee) && awardWinner.comment;
  },

  /**
   * Maps a list of Match Award Winners to a list of MatchAwardWinnerInput objects.
   * Match Award Winners with no member or awardee are ignored.
   * 
   * Ref: awards/schema/MatchAwardWinnerInput Python class
   */
  toAwardWinnerInputList(awardWinners) {
    return awardWinners
      .filter(awardWinner => awardWinner.member || awardWinner.awardee)
      .map(awardWinner => ({
        memberId: awardWinner.member ? Member.decode(awardWinner.member).id : undefined,
        awardee: awardWinner.awardee || undefined,
        comment: awardWinner.comment,
        award: awardWinner.award,
      }));
  },
};

export default MatchAwardWinner;
