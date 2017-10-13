import React from 'react';
import PropTypes from 'prop-types';
import MatchTableRow from './MatchTableRow';

const MatchTable = ({ matches, excludeColumns, dateFormat }) => {
  const incl = columnName => !excludeColumns.includes(columnName);
  return (
    <table className="table table-sm table-hover table-responsive">
      <thead>
        <tr>
          {incl('fixtureType') && <th className="priority3">&nbsp;</th>}
          {incl('date') && <th>Date</th>}
          {incl('opposition') && <th>Opposition</th>}
          {incl('time') && <th className="priority2">Time</th>}
          {incl('venue') && <th className="priority2">Venue</th>}
          {incl('result') && (
            <th className="g-text-center">
              Result<br />(CS-Op)
            </th>
          )}
          {incl('scorers') && <th className="priority3">Scorers</th>}
          {incl('awards') && (
            <th className="priority3">
              <abbr title="Man of the Match">
                <i className="fa fa-star-o" />
              </abbr>
            </th>
          )}
          {incl('awards') && (
            <th className="priority3">
              <abbr title="Lemon of the Match">
                <i className="fa fa-lemon-o" />
              </abbr>
            </th>
          )}
          {incl('report') && (
            <th className="g-text-center">
              Match<br />Details
            </th>
          )}
        </tr>
      </thead>
      <tbody>
        {matches.map(match => (
          <MatchTableRow
            key={match.id}
            match={match}
            excludeColumns={excludeColumns}
            dateFormat={dateFormat}
          />
        ))}
      </tbody>
    </table>
  );
};

MatchTable.propTypes = {
  matches: PropTypes.arrayOf(PropTypes.shape()).isRequired,
  excludeColumns: PropTypes.arrayOf(PropTypes.string),
  dateFormat: PropTypes.string,
};

MatchTable.defaultProps = {
  excludeColumns: [],
  dateFormat: 'Do MMM',
};

export default MatchTable;
