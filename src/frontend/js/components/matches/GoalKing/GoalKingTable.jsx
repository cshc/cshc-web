import React from 'react';
import PropTypes from 'prop-types';
import { NetworkStatus as NS } from 'apollo-client';
import cloneDeep from 'lodash/cloneDeep';
import ErrorDisplay from 'components/common/ErrorDisplay';
import Loading from 'components/common/Loading';
import { FilterName } from 'util/constants';
import GoalKingTableRow from './GoalKingTableRow';

const GoalKingTable = ({ networkStatus, error, entries, activeFilters }) => {
  if (error) return <ErrorDisplay errorMessage="Failed to load goal king entries" />;
  if (!entries && networkStatus === NS.loading) {
    return <Loading message="Fetching goal king entries..." />;
  }
  const filteredEntries = cloneDeep(
    entries.edges.filter(entry =>
      activeFilters[FilterName.GoalKingGender].includes(entry.node.member.gender),
    ),
  );
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
            <GoalKingTableRow key={entry.node.member.modelId} entry={entry.node} />
          ))}
        </tbody>
      </table>
    </div>
  );
};

GoalKingTable.propTypes = {
  networkStatus: PropTypes.number.isRequired,
  error: PropTypes.instanceOf(Error),
  entries: PropTypes.shape(),
  activeFilters: PropTypes.shape(),
};

GoalKingTable.defaultProps = {
  error: undefined,
  entries: undefined,
  activeFilters: undefined,
};

export default GoalKingTable;
