import React from 'react';
import PropTypes from 'prop-types';
import cloneDeep from 'lodash/cloneDeep';
import { NoFilter } from 'util/constants';
import GoalKingTableRow from './GoalKingTableRow';

const GoalKingTable = ({ data, team, goalKingGender }) => {
  const filteredEntries =
    goalKingGender === NoFilter
      ? data.edges
      : cloneDeep(data.edges.filter(entry => goalKingGender === entry.node.member.gender));
  if (filteredEntries.length) {
    let rank = 1;
    let previous = filteredEntries[0].node;
    previous.rank = 1;
    for (let i = 1; i < filteredEntries.length; i += 1) {
      const entry = filteredEntries[i].node;
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

  return (
    <div className="table-responsive">
      <table className="table table-sm table-hover">
        <thead>
          <tr>
            <th className="text-center">Rank</th>
            <th>Name</th>
            <th className="priority3">M1</th>
            <th className="priority3">M2</th>
            <th className="priority3">M3</th>
            <th className="priority3">M4</th>
            <th className="priority3">M5</th>
            <th className="priority3">L1</th>
            <th className="priority3">L2</th>
            <th className="priority3">L3</th>
            <th className="priority3">L4</th>
            <th className="priority3">
              <abbr title="Mixed team">Mix</abbr>
            </th>
            <th className="priority3">
              <abbr title="Indoor team">Ind</abbr>
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
              key={entry.node.member.modelId}
              entry={entry.node}
              teamFilter={team}
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
