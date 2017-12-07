import React from 'react';
import PropTypes from 'prop-types';
import { UrlQueryParamTypes } from 'react-url-query';
import { Gender, NoFilter, FilterName } from 'util/constants';
import { SelectFilter, OptionListFilter } from 'components/filters/UrlFilter';

export const urlPropsQueryConfig = {
  [FilterName.Season]: {
    type: UrlQueryParamTypes.string,
    validate: seasonSlug => /[\d]{4}-[\d]{4}/.test(seasonSlug),
  },
  [FilterName.Team]: {
    type: UrlQueryParamTypes.string,
  },
  [FilterName.GoalKingGender]: {
    type: UrlQueryParamTypes.string,
  },
};

const genderOptions = [
  { value: NoFilter, label: 'Men & Ladies' },
  { value: Gender.Male, label: 'Men' },
  { value: Gender.Female, label: 'Ladies' },
];

const GoalKingFilterSet = ({ currentSeason, seasons, teams }) => {
  const teamOptions = teams.map(t => ({ value: t.slug, label: t.long_name }));
  teamOptions.unshift({ value: NoFilter, label: 'All' });
  return (
    <div className="row d-flex align-items-end g-mb-40">
      <div className="col-12 col-lg-3">
        <SelectFilter
          label="Season"
          filterName={FilterName.Season}
          defaultValue={currentSeason}
          urlQueryConfig={urlPropsQueryConfig[FilterName.Season]}
          inline
          clearable={false}
          options={seasons.map(s => ({ value: s, label: s }))}
        />
      </div>
      <div className="col-12 col-lg-3">
        <SelectFilter
          label="Team"
          filterName={FilterName.Team}
          urlQueryConfig={urlPropsQueryConfig[FilterName.Team]}
          inline
          clearable
          options={teamOptions}
        />
      </div>
      <div className="col-12 col-lg-5">
        <OptionListFilter
          filterName={FilterName.GoalKingGender}
          defaultValue={NoFilter}
          urlQueryConfig={urlPropsQueryConfig[FilterName.GoalKingGender]}
          options={genderOptions}
          inline
        />
      </div>
    </div>
  );
};

GoalKingFilterSet.propTypes = {
  currentSeason: PropTypes.string.isRequired,
  seasons: PropTypes.arrayOf(PropTypes.string).isRequired,
  teams: PropTypes.arrayOf(
    PropTypes.shape({
      slug: PropTypes.string,
      long_name: PropTypes.string,
    }),
  ).isRequired,
};

export default GoalKingFilterSet;
