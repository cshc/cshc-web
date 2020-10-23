import React from 'react';
import PropTypes from 'prop-types';
import cloneDeep from 'lodash/cloneDeep';
import { NoFilter } from 'util/constants';
import GoalKingTableRow from './GoalKingTableRow';

const GoalKingTable = ({ data, team, goalKingGender }) => {
  const filteredEntries =
    goalKingGender === NoFilter
      ? data.results
      : cloneDeep(data.results.filter(entry => goalKingGender === entry.member.gender));
  if (filteredEntries.length) {
    let rank = 1;
    let previous = filteredEntries[0];
    previous.rank = 1;
    for (let i = 1; i < filteredEntries.length; i += 1) {
      const entry = filteredEntries[i];
      if (entry.totalGoals !== previous.totalGoals) {
        rank = i + 1;
        entry.rank = `${rank}`;
      } else {
        entry.rank = `${rank}=`;
        previous.rank = entry.rank;
      }
      previous = entry;
    }
  }

  if (!filteredEntries.length) {
    return <div className="d-flex justify-content-center">(No goal scorers)</div>;
  }
  const maxGoals =
    team === NoFilter ? filteredEntries[0].totalGoals : filteredEntries[0][`${team}Goals`];

  return (
    <div className="table-responsive">
      <table className="table table-sm table-hover text-center">
        <thead>
          <tr>
            <th className="text-center">Rank</th>
            <th className="text-left">Name</th>
            <th className="priority3">M1</th>
            <th className="priority3">M2</th>
            <th className="priority3">M3</th>
            <th className="priority3">M4</th>
            <th className="priority3">M5</th>
            <th className="priority3">M6</th>
            <th className="priority3">L1</th>
            <th className="priority3">L2</th>
            <th className="priority3">L3</th>
            <th className="priority3">L4</th>
            <th className="priority3">L5</th>
            <th className="priority3">L6</th>
            <th className="priority3">L7</th>
            <th className="priority3">
              <abbr title="Men's Vets team">MV</abbr>
            </th>
            <th className="priority3">
              <abbr title="Ladies' Vets team">LV</abbr>
            </th>
            <th className="priority3">
              <abbr title="Men's Indoor team">M-In</abbr>
            </th>
            <th className="priority3">
              <abbr title="Ladies' Indoor team">L-In</abbr>
            </th>
            <th className="priority3">
              <abbr title="Mixed A team">Mix-A</abbr>
            </th>
            <th className="priority3">
              <abbr title="Mixed B team">Mix-B</abbr>
            </th>
            <th>Total</th>
            <th>
              <abbr title="Goals per game">GPG</abbr>
            </th>
          </tr>
        </thead>
        <tbody>
          {filteredEntries.map(entry => (
            <GoalKingTableRow
              key={entry.member.id}
              entry={entry}
              teamFilter={team}
              maxGoals={maxGoals}
            />
          ))}
        </tbody>
      </table>
    </div>
  );
};

GoalKingTable.propTypes = {
  data: PropTypes.shape(),
  team: PropTypes.string,
  goalKingGender: PropTypes.string,
};

GoalKingTable.defaultProps = {
  data: undefined,
  team: NoFilter,
  goalKingGender: NoFilter,
};

export default GoalKingTable;
