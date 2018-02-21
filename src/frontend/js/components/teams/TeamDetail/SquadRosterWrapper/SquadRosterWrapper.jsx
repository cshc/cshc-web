import React from 'react';
import PropTypes from 'prop-types';
import { OptionListFilter } from 'components/filters';
import { FilterName, NoFilter, ViewType } from 'util/constants';
import { ViewSwitcher, ViewSwitcherView } from 'components/common/ViewSwitcher';
import SquadRoster from './SquadRoster';

const fixtureTypeOptions = [
  { value: NoFilter, label: 'All matches' },
  { value: 'League', label: 'League matches only' },
];

class SquadRosterWrapper extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      fixtureType: NoFilter,
    };
    this.onSetFixtureType = this.onSetFixtureType.bind(this);
  }

  onSetFixtureType(filterName, fixtureType) {
    this.setState({ fixtureType });
  }

  render() {
    const { teamId, seasonId, viewType, onSelectViewType } = this.props;
    return (
      <div>
        <div className="row g-mb-15">
          <div className="col-md-8">
            <OptionListFilter
              filterName={FilterName.FixtureType}
              options={fixtureTypeOptions}
              inline
              filterValue={this.state.fixtureType}
              onSetFilter={this.onSetFixtureType}
            />
          </div>
          <div className="col-md-4">
            <ViewSwitcher
              className="g-pt-6"
              currentView={viewType}
              onSelectViewType={onSelectViewType}
            >
              <ViewSwitcherView iconClass="fas fa-th-large" label={ViewType.Cards} />
              <ViewSwitcherView iconClass="fas fa-table" label={ViewType.Table} />
            </ViewSwitcher>
          </div>
        </div>
        <SquadRoster
          teamId={teamId}
          seasonId={seasonId}
          fixtureType={this.state.fixtureType}
          viewType={viewType}
        />
      </div>
    );
  }
}

SquadRosterWrapper.propTypes = {
  teamId: PropTypes.number.isRequired,
  seasonId: PropTypes.number.isRequired,
  viewType: PropTypes.string.isRequired,
  onSelectViewType: PropTypes.func.isRequired,
};

export default SquadRosterWrapper;
