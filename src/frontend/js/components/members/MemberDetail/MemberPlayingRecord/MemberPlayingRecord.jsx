import React from 'react';
import PropTypes from 'prop-types';
import keys from 'lodash/keys';
import { UrlQueryParamTypes } from 'react-url-query';
import { Subheading } from 'components/Unify';
import { ViewSwitcher, ViewSwitcherView } from 'components/common/ViewSwitcher';
import { ViewType, NoFilter, FixtureType, FilterName } from 'util/constants';
import { SelectFilter } from 'components/filters';
import MemberPlayingRecordDisplay from './MemberPlayingRecordDisplay';

/**
 * The fixture type and view type are stored as URL query params.
 * 
 * This means we can link directly to a particular view of filtered data
 */
export const urlPropsQueryConfig = {
  fixtureType: {
    type: UrlQueryParamTypes.string,
    validate: fixtureType => FixtureType[fixtureType] !== undefined,
  },
  viewType: {
    type: UrlQueryParamTypes.string,
    validate: viewType => viewType === ViewType.Table || viewType === ViewType.Chart,
  },
};

/**
 * Top-level component for a member's Playing Record. 
 * 
 * Contains:
 * - Filters (fixture type)
 * - View Switcher (table/chart)
 * - Data display (wrapped in Apollo query)
 */
const MemberPlayingRecord = ({
  memberId,
  fixtureType,
  onChangeFixtureType,
  viewType,
  onChangeViewType,
}) => {
  // Create the fixture type options (including 'All')
  const fixtureTypeOptions = keys(FixtureType).map(ft => ({ value: ft, label: ft }));
  fixtureTypeOptions.unshift({ value: NoFilter, label: 'All' });
  return (
    <div>
      <Subheading text="Playing Record" />
      <div className="d-flex flex-wrap justify-content-between g-mb-15">
        <SelectFilter
          className="g-min-width-130"
          label="Fixture type"
          filterName={FilterName.FixtureType}
          options={fixtureTypeOptions}
          onSetFilter={(filterName, filterValue) =>
            onChangeFixtureType(filterValue === NoFilter ? undefined : filterValue)}
          filterValue={fixtureType}
          inline
        />
        <ViewSwitcher className="g-pt-6" currentView={viewType} onSelectViewType={onChangeViewType}>
          <ViewSwitcherView iconClass="fas fa-table" label={ViewType.Table} />
          <ViewSwitcherView iconClass="fas fa-chart-area" label={ViewType.Chart} />
        </ViewSwitcher>
      </div>
      <MemberPlayingRecordDisplay
        fixtureType={fixtureType}
        memberId={memberId}
        viewType={viewType}
      />
    </div>
  );
};

MemberPlayingRecord.propTypes = {
  memberId: PropTypes.number.isRequired,
  fixtureType: PropTypes.string,
  viewType: PropTypes.string,
  onChangeFixtureType: PropTypes.func.isRequired,
  onChangeViewType: PropTypes.func.isRequired,
};

MemberPlayingRecord.defaultProps = {
  fixtureType: NoFilter,
  viewType: ViewType.Table,
};

export default MemberPlayingRecord;
