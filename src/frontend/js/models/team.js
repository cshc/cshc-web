const Team = {
  genderlessName(team) {
    return team.name.replace('Ladies', '').replace('Mens', '');
  },
};

export default Team;
