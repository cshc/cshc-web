import React from 'react';
import PropTypes from 'prop-types';
import { saturdaysBetweenDates } from 'util/cshc';
import { MatchItem as TC } from 'util/constants';
import MatchTableRow from './MatchTableRow';

/**
 * Tabular representation of a list of matches
 */
const MatchTable = ({ matches, excludeColumns, dateFormat, priorities, fillBlankSaturdays }) => {
  const incl = columnName => !excludeColumns.includes(columnName);
  const priority = (columnName, defaultPriority = 1) =>
    `priority${priorities[columnName] || defaultPriority}`;
  return (
    <div className="table-responsive">
      <table className="table table-sm table-hover">
        <thead>
          <tr>
            {incl(TC.fixtureType) && <th className={priority(TC.fixtureType, 3)}>&nbsp;</th>}
            {incl(TC.date) && <th className={priority(TC.date)}>Date</th>}
            {incl(TC.opposition) && <th className={priority(TC.opposition)}>Opposition</th>}
            {incl(TC.time) && <th className={priority(TC.time, 2)}>Time</th>}
            {incl(TC.venue) && <th className={priority(TC.venue, 2)}>Venue</th>}
            {incl(TC.result) && (
              <th className={`g-text-center ${priority(TC.result)}`}>
                Result<br />(CS-Op)
              </th>
            )}
            {incl(TC.scorers) && <th className={priority(TC.scorers, 3)}>Scorers</th>}
            {incl(TC.awards) && (
              <th className={priority(TC.awards, 3)}>
                <abbr title="Man of the Match">
                  <i className="fa fa-star-o" />
                </abbr>
              </th>
            )}
            {incl(TC.awards) && (
              <th className={priority(TC.awards, 3)}>
                <abbr title="Lemon of the Match">
                  <i className="fa fa-lemon-o" />
                </abbr>
              </th>
            )}
            {incl(TC.report) && (
              <th className={`g-text-center ${priority(TC.report)}`}>
                Match<br />Details
              </th>
            )}
          </tr>
        </thead>
        <tbody>
          {matches.map((match, index) => {
            const rows = [];
            // If we should display saturdays without matches,
            // work out all the saturdays between the previous match and this match
            // and add a spacer row for each one.
            if (fillBlankSaturdays) {
              const prevDate = index > 0 ? matches[index - 1].date : undefined;
              const saturdays = saturdaysBetweenDates(prevDate, match.date);
              if (saturdays) {
                saturdays.forEach((saturday) => {
                  rows.push(
                    <MatchTableRow
                      key={saturday}
                      match={{ date: saturday, isSpacer: true }}
                      excludeColumns={excludeColumns}
                      priorities={priorities}
                      dateFormat={dateFormat}
                    />,
                  );
                });
              }
            }
            rows.push(
              <MatchTableRow
                key={match.id}
                match={match}
                excludeColumns={excludeColumns}
                priorities={priorities}
                dateFormat={dateFormat}
              />,
            );
            return rows;
          })}
        </tbody>
      </table>
    </div>
  );
};

MatchTable.propTypes = {
  matches: PropTypes.arrayOf(PropTypes.shape()).isRequired,
  excludeColumns: PropTypes.arrayOf(PropTypes.string),
  priorities: PropTypes.shape(),
  dateFormat: PropTypes.string,
  fillBlankSaturdays: PropTypes.bool,
};

MatchTable.defaultProps = {
  excludeColumns: [],
  priorities: {},
  dateFormat: 'Do MMM',
  fillBlankSaturdays: false,
};

export default MatchTable;
