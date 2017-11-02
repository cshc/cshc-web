import { PositionOptions } from 'util/constants';
import reduce from 'lodash/reduce';
import concat from 'lodash/concat';
import uniq from 'lodash/uniq';

/**
 * Utility object for common logic related to a club member.
 */
const Member = {
  firstNameAndInitial(member) {
    return `${member.firstName} ${member.lastName[0].toUpperCase()}`;
  },

  fullName(member) {
    return `${member.firstName} ${member.lastName}`;
  },

  /**
   * Converts an array of 'Position' strings to a string of comma-separated integer pref_position values
   * 
   * Ref: core/models/utils.py for integer values 
   */
  getPreferredPositions(positions) {
    if (!positions || !positions.length) return undefined;
    const values = reduce(positions, (acc, position) => concat(acc, PositionOptions[position]), []);
    return uniq(values).join(',');
  },
};

export default Member;
