import reduce from 'lodash/reduce';
import uniqWith from 'lodash/uniqWith';
import sortBy from 'lodash/sortBy';

const getAllTeams = data => sortBy(
  uniqWith(
    reduce(
      data,
      (acc, seasonStats) =>
        acc.concat(seasonStats.memberStats.teamRepresentations.map(tr => tr.team)),
      [],
    ),
    (a, b) => !a.slug.localeCompare(b.slug),
  ),
  t => t.position,
);

module.exports = {
  getAllTeams,
};
