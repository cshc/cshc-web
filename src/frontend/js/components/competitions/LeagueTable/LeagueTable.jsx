import React from 'react';
import PropTypes from 'prop-types';
import Urls from 'util/urls';

// eslint-disable-next-line no-nested-ternary
const relative = value => `${value === 0 ? '' : value < 0 ? '-' : '+'}${Math.abs(value)}`;

const teamNameCell = (row, isCSHCTeam, isOurTeam) => {
  if (isOurTeam) {
    return row.teamName;
  }
  return row.oppTeam ? (
    <a href={Urls.opposition_club_detail(row.oppTeam.club.slug)} title="Club Details">
      {row.teamName}
    </a>
  ) : (
    <a href={Urls.clubteam_detail(row.ourTeam.slug)} title="Team Details">
      {row.teamName}
    </a>
  );
};

/**
 * Represents a League Table. 
 * 
 * Teams are either Opposition.Team or Team.ClubTeam instances.
 */
class LeagueTable extends React.PureComponent {
  constructor(props) {
    super(props);
    this.state = {
      error: null,
    };
  }

  componentDidCatch(error) {
    console.error('Unhandled exception caught by component', error);
    this.setState({ error });
  }

  render() {
    const { data, teamName } = this.props;
    const { error } = this.state;

    return (
      <div className="table-responsive">
        {!error && data.results && data.results.length ? (
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
                    <td>{relative(row.goalDifference)}</td>
                    <td>{row.points}</td>
                    <td>{row.notes}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        ) : (
          <p className="lead g-font-style-italic">Sorry - league table not available</p>
        )}
      </div>
    );
  }
}

LeagueTable.propTypes = {
  data: PropTypes.shape(),
  teamName: PropTypes.string.isRequired,
};

LeagueTable.defaultProps = {
  data: undefined,
};

export default LeagueTable;
