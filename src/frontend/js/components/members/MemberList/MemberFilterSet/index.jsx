import React from 'react';
import PropTypes from 'prop-types';
import { UrlQueryParamTypes } from 'react-url-query';
import { FilterName, Position, NoFilter } from 'util/constants';
import { FilterGroup } from 'components/filters';
import { BooleanFilter, TextFilter, OptionListFilter } from 'components/filters/UrlFilter';

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
  [FilterName.Gender]: {
    type: UrlQueryParamTypes.string,
  },
  [FilterName.Team]: {
    type: UrlQueryParamTypes.string,
  },
  [FilterName.Position]: {
    type: UrlQueryParamTypes.array,
  },
};

const MemberFilterSet = ({ teams }) => {
  const teamOptions = teams.map(team => ({ value: team.slug, label: team.long_name }));
  teamOptions.unshift({ value: NoFilter, label: 'All' });
  const genderOptions = [
    { value: NoFilter, label: 'Men & Ladies' },
    { value: 'Male', label: 'Men' },
    { value: 'Female', label: 'Ladies' },
  ];
  const positionOptions = [
    { value: Position.Goalkeeper, label: Position.Goalkeeper },
    { value: Position.Defence, label: Position.Defence },
    { value: Position.Midfield, label: Position.Midfield },
    { value: Position.Forward, label: Position.Forward },
    { value: Position.Unknown, label: Position.Unknown },
  ];
  return (
    <div>
      <TextFilter
        filterName={FilterName.TextSearch}
        urlQueryConfig={urlPropsQueryConfig[FilterName.TextSearch]}
      />
      <BooleanFilter
        filterName={FilterName.Current}
        urlQueryConfig={urlPropsQueryConfig[FilterName.Current]}
        label="Current"
      />
      <BooleanFilter
        filterName={FilterName.Captains}
        urlQueryConfig={urlPropsQueryConfig[FilterName.Captains]}
        label="Captains/Vice-Captains only"
      />
      <FilterGroup title="Gender">
        <OptionListFilter
          filterName={FilterName.Gender}
          urlQueryConfig={urlPropsQueryConfig[FilterName.Gender]}
          defaultValue={NoFilter}
          options={genderOptions}
        />
      </FilterGroup>
      <FilterGroup title="Current Squad">
        <OptionListFilter
          filterName={FilterName.Team}
          urlQueryConfig={urlPropsQueryConfig[FilterName.Team]}
          defaultValue={NoFilter}
          options={teamOptions}
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
};

export default MemberFilterSet;
