import React from 'react';
import PropTypes from 'prop-types';
import { UrlQueryParamTypes, pushUrlQuery } from 'react-url-query';
import { FilterName } from 'util/constants';
import { SelectFilter } from 'components/filters/UrlFilter';

export const urlPropsQueryConfig = {
  [FilterName.Season]: {
    type: UrlQueryParamTypes.string,
  },
  [FilterName.Award]: {
    type: UrlQueryParamTypes.string,
  },
  [FilterName.Member]: {
    type: UrlQueryParamTypes.string,
  },
};

const EosFilterSet = ({ seasons, awards, awardees }) => {
  const clearAll = () => {
    pushUrlQuery({});
  };
  const seasonOptions = seasons.map(season => ({ value: season, label: season }));
  const awardOptions = awards.map(award => ({ value: String(award.id), label: award.name }));
  const memberOptions = awardees.map(member => ({
    value: String(member.id),
    label: `${member.first_name} ${member.last_name}`,
  }));
  return (
    <div className="g-pb-20">
      <div className="text-right">
        <button className="btn btn-link" onClick={clearAll}>
          Clear all
        </button>
      </div>
      <SelectFilter
        label="Season"
        filterName={FilterName.Season}
        options={seasonOptions}
        urlQueryConfig={urlPropsQueryConfig[FilterName.Season]}
        stacked
      />
      <SelectFilter
        label="Award"
        filterName={FilterName.Award}
        options={awardOptions}
        urlQueryConfig={urlPropsQueryConfig[FilterName.Award]}
        stacked
      />
      <SelectFilter
        label="Member"
        filterName={FilterName.Member}
        options={memberOptions}
        urlQueryConfig={urlPropsQueryConfig[FilterName.Member]}
        stacked
      />
    </div>
  );
};

EosFilterSet.propTypes = {
  seasons: PropTypes.arrayOf(PropTypes.string).isRequired,
  awards: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number,
      name: PropTypes.string,
    }),
  ).isRequired,
  awardees: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number,
      first_name: PropTypes.string,
      last_name: PropTypes.string,
    }),
  ).isRequired,
};

export default EosFilterSet;
