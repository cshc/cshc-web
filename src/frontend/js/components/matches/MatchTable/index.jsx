import React from 'react';
import PropTypes from 'prop-types';
import MatchTableRow from './MatchTableRow';

const MatchTable = ({ matches, excludeColumns, dateFormat, priorities }) => {
  const incl = columnName => !excludeColumns.includes(columnName);
  const priority = (columnName, defaultPriority = 1) =>
    `priority${priorities[columnName] || defaultPriority}`;
  return (
    <table className="table table-sm table-hover table-responsive">
      <thead>
        <tr>
          {incl('fixtureType') && <th className={priority('fixtureType', 3)}>&nbsp;</th>}
          {incl('date') && <th className={priority('date')}>Date</th>}
          {incl('opposition') && <th className={priority('opposition')}>Opposition</th>}
          {incl('time') && <th className={priority('time', 2)}>Time</th>}
          {incl('venue') && <th className={priority('venue', 2)}>Venue</th>}
          {incl('result') && (
            <th className={`g-text-center ${priority('result')}`}>
              Result<br />(CS-Op)
            </th>
          )}
          {incl('scorers') && <th className={priority('scorers', 3)}>Scorers</th>}
          {incl('awards') && (
            <th className={priority('awards', 3)}>
              <abbr title="Man of the Match">
                <i className="fa fa-star-o" />
              </abbr>
            </th>
          )}
          {incl('awards') && (
            <th className={priority('awards', 3)}>
              <abbr title="Lemon of the Match">
                <i className="fa fa-lemon-o" />
              </abbr>
            </th>
          )}
          {incl('report') && (
            <th className={`g-text-center ${priority('report')}`}>
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
            priorities={priorities}
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
  priorities: PropTypes.shape(),
  dateFormat: PropTypes.string,
};

MatchTable.defaultProps = {
  excludeColumns: [],
  priorities: {},
  dateFormat: 'Do MMM',
};

export default MatchTable;
