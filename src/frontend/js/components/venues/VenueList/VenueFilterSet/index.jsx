import React from 'react';
import PropTypes from 'prop-types';
import uniqBy from 'lodash/uniqBy';
import { FilterName, NoFilter } from 'util/constants';
import { UrlQueryParamTypes, pushUrlQuery } from 'react-url-query';
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
  [FilterName.Season]: {
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
  divisionOptions.unshift({ value: NoFilter, label: 'All' });
  return (
    <div class="g-mt-40">
      <FilterGroup title="Search" className="g-mb-20">
        <TextFilter
          filterName={FilterName.TextSearch}
          placeholder="Venue name..."
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
          urlQueryConfig={urlPropsQueryConfig[FilterName.Season]}
        />
        <SelectFilter
          label="Team"
          filterName={FilterName.Team}
          defaultValue={NoFilter}
          options={teamOptions}
          urlQueryConfig={urlPropsQueryConfig[FilterName.Team]}
          stacked
        />
        <SelectFilter
          label="Division"
          filterName={FilterName.Division}
          defaultValue={NoFilter}
          options={divisionOptions}
          urlQueryConfig={urlPropsQueryConfig[FilterName.Division]}
          stacked
        />
      </FilterGroup>
      <div className="text-right g-mt-15 g-mb-20">
        <button
          className="btn btn-outline-secondary"
          onClick={() => {
            pushUrlQuery({});
          }}
        >Clear all</button>
      </div>
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
