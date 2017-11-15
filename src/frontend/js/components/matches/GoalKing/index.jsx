import React from 'react';
import PropTypes from 'prop-types';
import { SelectFilter, OptionListFilter } from 'components/filters';
import { FilterName, Gender } from 'util/constants';
import GoalKingTable from './GoalKingTable';

const genderOptions = [
  { value: Gender.Male, label: 'Men' },
  { value: Gender.Female, label: 'Ladies' },
];

const GoalKingWrapper = ({ seasons }) => (
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
    <GoalKingTable />
  </div>
);

GoalKingWrapper.propTypes = {
  seasons: PropTypes.arrayOf(PropTypes.string).isRequired,
};

export default GoalKingWrapper;
