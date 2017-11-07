import React from 'react';
import PropTypes from 'prop-types';
import { SelectFilter } from 'components/filters';
import { FilterName, Gender } from 'util/constants';
import OptionListFilter from 'components/filters/OptionListFilter';
import GoalKingTable from './GoalKingTable';

const genderOptions = [
  { value: Gender.Male, label: 'Men' },
  { value: Gender.Female, label: 'Ladies' },
];

const GoalKingWrapper = ({ networkStatus, error, entries, seasons, activeFilters }) => (
  <div>
    <div className="row d-flex align-items-end g-mb-40">
      <div className="col-12 col-lg-3">
        <SelectFilter
          label="Season"
          filterName={FilterName.Season}
          inline
          clearable={false}
          options={seasons.map(season => ({ value: season, label: season }))}
        />
      </div>
      <div className="col-12 col-lg-8">
        <OptionListFilter
          filterName={FilterName.GoalKingGender}
          options={genderOptions}
          inline
          multiselect
        />
      </div>
    </div>
    <GoalKingTable
      networkStatus={networkStatus}
      error={error}
      activeFilters={activeFilters}
      entries={entries}
    />
  </div>
);

GoalKingWrapper.propTypes = {
  networkStatus: PropTypes.number.isRequired,
  error: PropTypes.instanceOf(Error),
  entries: PropTypes.shape(),
  seasons: PropTypes.arrayOf(PropTypes.string).isRequired,
  activeFilters: PropTypes.shape(),
};

GoalKingWrapper.defaultProps = {
  error: undefined,
  entries: undefined,
  activeFilters: undefined,
};

export default GoalKingWrapper;
