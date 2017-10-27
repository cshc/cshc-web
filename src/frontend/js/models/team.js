/**
 * Utility object for common logic related to a club team.
 */
const Team = {
  genderlessName(team) {
    return team.name.replace('Ladies', '').replace('Mens', '');
  },
};

export default Team;
