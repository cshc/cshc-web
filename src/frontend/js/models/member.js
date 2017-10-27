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
};

export default Member;
