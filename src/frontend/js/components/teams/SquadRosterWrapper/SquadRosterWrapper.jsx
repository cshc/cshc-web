import React from 'react';
import PropTypes from 'prop-types';
import { OptionListFilter } from 'components/filters';
import { FilterName, NoFilter, ViewType } from 'util/constants';
import { ViewSwitcher, ViewSwitcherView } from 'components/common/ViewSwitcher';
import SquadRoster from '../SquadRoster';

const fixtureTypeOptions = [
  { value: NoFilter, label: 'All matches' },
  { value: 'League', label: 'League matches only' },
];

const SquadRosterWrapper = ({ teamId, seasonId, viewType, onSelectViewType, activeFilters }) => (
  <div>
    <div className="row g-mb-15">
      <div className="col-md-8">
        <OptionListFilter filterName={FilterName.FixtureType} options={fixtureTypeOptions} inline />
      </div>
      <div className="col-md-4">
        <ViewSwitcher className="g-pt-6" currentView={viewType} onSelectViewType={onSelectViewType}>
          <ViewSwitcherView iconClass="fa fa-th-large" label={ViewType.Cards} />
          <ViewSwitcherView iconClass="fa fa-table" label={ViewType.Table} />
        </ViewSwitcher>
      </div>
    </div>
    <SquadRoster
      teamId={teamId}
      seasonId={seasonId}
      fixtureType={activeFilters[FilterName.FixtureType]}
      viewType={viewType}
    />
  </div>
);

SquadRosterWrapper.propTypes = {
  teamId: PropTypes.number.isRequired,
  seasonId: PropTypes.number.isRequired,
  viewType: PropTypes.string.isRequired,
  onSelectViewType: PropTypes.func.isRequired,
  activeFilters: PropTypes.shape(),
};

SquadRosterWrapper.defaultProps = {
  activeFilters: undefined,
};

export default SquadRosterWrapper;
