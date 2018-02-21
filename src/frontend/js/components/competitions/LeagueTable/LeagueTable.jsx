import React from 'react';
import PropTypes from 'prop-types';
import Urls from 'util/urls';

/**
 * Represents a League Table. 
 * 
 * Teams are either Opposition.Team or Team.ClubTeam instances.
 */
const LeagueTable = ({ data, teamName }) => {
  const teamNameCell = (row, isCSHCTeam, isOurTeam) => {
    if (isOurTeam) {
      return row.teamName;
    }
    return (
      <a href={Urls.opposition_club_detail(row.oppTeam.club.slug)} title="Club Details">
        {row.teamName}
      </a>
    );
  };

  return (
    <div className="table-responsive">
      <table className="table table-sm table-hover">
        <thead>
          <tr>
            <th>Team</th>
            <th>
              <abbr title="Played">P</abbr>
            </th>
            <th>
              <abbr title="Won">W</abbr>
            </th>
            <th>
              <abbr title="Drawn">D</abbr>
            </th>
            <th>
              <abbr title="Lost">L</abbr>
            </th>
            <th>
              <abbr title="Goals For">GF</abbr>
            </th>
            <th>
              <abbr title="Goals Against">GA</abbr>
            </th>
            <th>
              <abbr title="Goal Difference">GD</abbr>
            </th>
            <th>
              <abbr title="Points">Pts</abbr>
            </th>
            <th>&nbsp;</th>
          </tr>
        </thead>
        <tbody>
          {data.results.map((row) => {
            const isCSHCTeam = row.teamName.startsWith('Cambridge South');
            const isOurTeam = row.teamName === teamName;
            const rowClass = isOurTeam ? 'table-success g-color-black g-font-weight-600' : '';
            return (
              <tr key={row.teamName} className={rowClass}>
                <td>{teamNameCell(row, isCSHCTeam, isOurTeam)}</td>
                <td>{row.played}</td>
                <td>{row.won}</td>
                <td>{row.drawn}</td>
                <td>{row.lost}</td>
                <td>{row.goalsFor}</td>
                <td>{row.goalsAgainst}</td>
                <td>{row.goalDifference}</td>
                <td>{row.points}</td>
                <td>{row.notes}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};

LeagueTable.propTypes = {
  data: PropTypes.shape(),
  teamName: PropTypes.string.isRequired,
};

LeagueTable.defaultProps = {
  data: undefined,
};

export default LeagueTable;
