import React from 'react';
import PropTypes from 'prop-types';
import { NetworkStatus as NS } from 'apollo-client';
import { SwitchableView, ViewType } from 'util/constants';
import ErrorDisplay from 'components/common/ErrorDisplay';
import Loading from 'components/common/Loading';
import ViewSwitcher from 'components/common/ViewSwitcher';
import SquadRosterCard from '../SquadRosterCard';
import SquadRosterTable from '../SquadRosterTable';

/**
 * Represents a list of club members (typically this is filtered by season and team). 
 * 
 * The list of club members can be represented in a table or 'cards' - with a view switcher
 * to switch between these views.
 */
const SquadRoster = ({ networkStatus, error, squadStats, viewType, onSelectViewType }) => {
  if (error) return <ErrorDisplay errorMessage="Failed to load squad roster" />;
  if (!squadStats || networkStatus === NS.loading) {
    return <Loading message="Fetching squad roster..." />;
  }
  const views = [
    {
      iconClass: 'fa fa-th-large',
      label: ViewType.Cards,
      onSelect: () => onSelectViewType(SwitchableView.SquadRoster, ViewType.Cards),
    },
    {
      iconClass: 'fa fa-table',
      label: ViewType.Table,
      onSelect: () => onSelectViewType(SwitchableView.SquadRoster, ViewType.Table),
    },
  ];
  return (
    <div>
      <ViewSwitcher className="g-mb-15" views={views} currentView={viewType} />
      {viewType === ViewType.Cards ? (
        <div className="row">
          {squadStats.squad.map(memberStats => (
            <SquadRosterCard
              key={memberStats.member.modelId}
              memberStats={memberStats}
              teamTotals={squadStats.totals}
            />
          ))}
        </div>
      ) : (
        <SquadRosterTable squadStats={squadStats} />
      )}
    </div>
  );
};

SquadRoster.propTypes = {
  networkStatus: PropTypes.number.isRequired,
  error: PropTypes.instanceOf(Error),
  squadStats: PropTypes.shape({
    totals: PropTypes.shape(),
    squad: PropTypes.arrayOf(PropTypes.shape()),
  }),
  viewType: PropTypes.string.isRequired,
  onSelectViewType: PropTypes.func.isRequired,
};

SquadRoster.defaultProps = {
  error: undefined,
  squadStats: undefined,
};

export default SquadRoster;
