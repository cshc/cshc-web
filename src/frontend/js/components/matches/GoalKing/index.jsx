import React from 'react';
import PropTypes from 'prop-types';
import { SelectFilter, OptionListFilter } from 'components/filters';
import { FilterName, NoFilter, Gender } from 'util/constants';
import GoalKingTable from './GoalKingTable';

const genderOptions = [
  { value: Gender.Male, label: 'Men' },
  { value: Gender.Female, label: 'Ladies' },
];

const GoalKingWrapper = ({ seasons, teams }) => {
  const teamOptions = teams.map(team => ({ value: team.slug, label: team.long_name }));
  teamOptions.unshift({ value: NoFilter, label: 'All' });
  return (
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
        <div className="col-12 col-lg-3">
          <SelectFilter
            label="Team"
            filterName={FilterName.Team}
            inline
            clearable={false}
            options={teamOptions}
          />
        </div>
        <div className="col-12 col-lg-5">
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
};

GoalKingWrapper.propTypes = {
  seasons: PropTypes.arrayOf(PropTypes.string).isRequired,
  teams: PropTypes.arrayOf(
    PropTypes.shape({
      slug: PropTypes.string,
      long_name: PropTypes.string,
    }),
  ).isRequired,
};

export default GoalKingWrapper;
