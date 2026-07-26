import React from 'react';
import PropTypes from 'prop-types';
import { UrlQueryParamTypes, pushUrlQuery } from 'react-url-query';
import { FilterName, Position, NoFilter } from 'util/constants';
import { FilterGroup } from 'components/filters';
import { BooleanFilter, TextFilter, OptionListFilter, SelectFilter } from 'components/filters/UrlFilter';

export const urlPropsQueryConfig = {
  [FilterName.TextSearch]: {
    type: UrlQueryParamTypes.string,
  },
  [FilterName.Current]: {
    type: UrlQueryParamTypes.boolean,
  },
  [FilterName.Captains]: {
    type: UrlQueryParamTypes.boolean,
  },
  [FilterName.Umpires]: {
    type: UrlQueryParamTypes.boolean,
  },
  [FilterName.Coaches]: {
    type: UrlQueryParamTypes.boolean,
  },
  [FilterName.Gender]: {
    type: UrlQueryParamTypes.string,
  },
  [FilterName.Team]: {
    type: UrlQueryParamTypes.string,
  },
  [FilterName.Season]: {
    type: UrlQueryParamTypes.string,
  },
  [FilterName.Position]: {
    type: UrlQueryParamTypes.array,
  },
};

const MemberFilterSet = ({ teams, seasons }) => {
  const teamOptions = teams.map(team => ({ value: team.slug, label: team.long_name }));
  const genderOptions = [
    { value: 'Male', label: 'Men' },
    { value: 'Female', label: 'Ladies' },
  ];
  const seasonOptions = seasons.map(season => ({ value: season, label: season }));
  seasonOptions.unshift({ value: NoFilter, label: 'All' });
  const positionOptions = [
    { value: Position.Goalkeeper, label: Position.Goalkeeper },
    { value: Position.Defence, label: Position.Defence },
    { value: Position.Midfield, label: Position.Midfield },
    { value: Position.Forward, label: Position.Forward },
    { value: Position.Unknown, label: Position.Unknown },
  ];
  return (
    <div>
      <div className="text-right">
        <button
          className="btn btn-link"
          onClick={() => {
            pushUrlQuery({});
          }}
        >
          Clear all
        </button>
      </div>
      <TextFilter
        filterName={FilterName.TextSearch}
        urlQueryConfig={urlPropsQueryConfig[FilterName.TextSearch]}
      />
      <FilterGroup title="Only show...">
        <BooleanFilter
          filterName={FilterName.Current}
          urlQueryConfig={urlPropsQueryConfig[FilterName.Current]}
          label="Current players"
        />
        <BooleanFilter
          filterName={FilterName.Captains}
          urlQueryConfig={urlPropsQueryConfig[FilterName.Captains]}
          label="Captains/Vice-Captains"
        />
        <BooleanFilter
          filterName={FilterName.Umpires}
          urlQueryConfig={urlPropsQueryConfig[FilterName.Umpires]}
          label="Umpires"
        />
        <BooleanFilter
          filterName={FilterName.Coaches}
          urlQueryConfig={urlPropsQueryConfig[FilterName.Coaches]}
          label="Coaches"
        />
      </FilterGroup>
      <FilterGroup title="Gender">
        <SelectFilter
          filterName={FilterName.Gender}
          options={genderOptions}
          urlQueryConfig={urlPropsQueryConfig[FilterName.Gender]}
          stacked
        />
      </FilterGroup>
      <FilterGroup title="Season">
        <SelectFilter
          filterName={FilterName.Season}
          options={seasonOptions}
          urlQueryConfig={urlPropsQueryConfig[FilterName.Season]}
          stacked
        />
      </FilterGroup>
      <FilterGroup title="Team">
        <SelectFilter
          filterName={FilterName.Team}
          options={teamOptions}
          urlQueryConfig={urlPropsQueryConfig[FilterName.Team]}
          stacked
        />
      </FilterGroup>
      <FilterGroup title="Position">
        <OptionListFilter
          filterName={FilterName.Position}
          urlQueryConfig={urlPropsQueryConfig[FilterName.Position]}
          options={positionOptions}
          multiselect
        />
      </FilterGroup>
    </div>
  );
};

MemberFilterSet.propTypes = {
  teams: PropTypes.arrayOf(
    PropTypes.shape({
      slug: PropTypes.string,
      long_name: PropTypes.string,
    }),
  ).isRequired,
  seasons: PropTypes.arrayOf(PropTypes.string).isRequired,
};

export default MemberFilterSet;
