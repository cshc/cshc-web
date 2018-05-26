import React from 'react';
import PropTypes from 'prop-types';
import uniqBy from 'lodash/uniqBy';
import { FilterName, NoFilter } from 'util/constants';
import { UrlQueryParamTypes } from 'react-url-query';
import { FilterGroup } from 'components/filters';
import {
  BooleanFilter,
  TextFilter,
  OptionListFilter,
  SelectFilter,
} from 'components/filters/UrlFilter';

export const urlPropsQueryConfig = {
  [FilterName.TextSearch]: {
    type: UrlQueryParamTypes.string,
  },
  [FilterName.HomeGround]: {
    type: UrlQueryParamTypes.boolean,
  },
  [FilterName.CurrentSeason]: {
    type: UrlQueryParamTypes.string,
  },
  [FilterName.Team]: {
    type: UrlQueryParamTypes.string,
  },
  [FilterName.Division]: {
    type: UrlQueryParamTypes.string,
  },
};

const VenueFilterSet = ({ currentSeason, teams, divisions }) => {
  const teamOptions = teams.map(team => ({ value: team.slug, label: team.long_name }));
  const divisionOptions = uniqBy(divisions, 'id').map(division => ({
    value: division.id.toString(),
    label: division.name,
  }));

  teamOptions.unshift({ value: NoFilter, label: 'All' });
  return (
    <div>
      <TextFilter
        filterName={FilterName.TextSearch}
        urlQueryConfig={urlPropsQueryConfig[FilterName.TextSearch]}
      />
      <BooleanFilter
        filterName={FilterName.HomeGround}
        defaultValue={false}
        label="Home Grounds only"
        urlQueryConfig={urlPropsQueryConfig[FilterName.HomeGround]}
      />
      <BooleanFilter
        filterName={FilterName.Season}
        label="Current Season only"
        defaultValue={false}
        trueValue={currentSeason}
        urlQueryConfig={urlPropsQueryConfig[FilterName.CurrentSeason]}
      />
      <FilterGroup title="Team">
        <OptionListFilter
          filterName={FilterName.Team}
          defaultValue={NoFilter}
          options={teamOptions}
          urlQueryConfig={urlPropsQueryConfig[FilterName.Team]}
        />
      </FilterGroup>
      <FilterGroup title="Division">
        <SelectFilter
          filterName={FilterName.Division}
          options={divisionOptions}
          urlQueryConfig={urlPropsQueryConfig[FilterName.Division]}
          placeholder="Select a division..."
          openUpwards
        />
      </FilterGroup>
    </div>
  );
};

VenueFilterSet.propTypes = {
  currentSeason: PropTypes.string.isRequired,
  teams: PropTypes.arrayOf(
    PropTypes.shape({
      slug: PropTypes.string,
      long_name: PropTypes.string,
    }),
  ).isRequired,
  divisions: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number,
      name: PropTypes.string,
    }),
  ).isRequired,
};

export default VenueFilterSet;
