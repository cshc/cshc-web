import { PositionOptions } from 'util/constants';
import reduce from 'lodash/reduce';
import concat from 'lodash/concat';
import uniq from 'lodash/uniq';

/**
 * Utility object for common logic related to a club member.
 */
const Member = {
  /**
   * Encode a member as a string value with both ID and the member's name included.
   */
  encode(id, name) {
    return `${id}:${name}`;
  },

  /**
   * Decode an encoded member string into ID and name. 
   * 
   * Returns {id, name}
   */
  decode(member) {
    const s = member.split(':');
    return { id: s[0], name: s[1] };
  },

  firstNameAndInitial(member) {
    return `${member.firstName} ${member.lastName[0].toUpperCase()}`;
  },

  fullName(member) {
    return `${member.firstName} ${member.lastName}`.trim();
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
