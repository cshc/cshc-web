import React from 'react';
import PropTypes from 'prop-types';
import keys from 'lodash/keys';
import { UrlQueryParamTypes, pushUrlQuery } from 'react-url-query';
import { FilterName, FixtureType } from 'util/constants';
import { SelectFilter, DateFilter } from 'components/filters/UrlFilter';

export const urlPropsQueryConfig = {
  [FilterName.Gender]: {
    type: UrlQueryParamTypes.string,
  },
  [FilterName.Team]: {
    type: UrlQueryParamTypes.string,
  },
  [FilterName.Opposition]: {
    type: UrlQueryParamTypes.string,
  },
  [FilterName.Season]: {
    type: UrlQueryParamTypes.string,
  },
  [FilterName.FixtureType]: {
    type: UrlQueryParamTypes.string,
  },
  [FilterName.Division]: {
    type: UrlQueryParamTypes.string,
  },
  [FilterName.Venue]: {
    type: UrlQueryParamTypes.string,
  },
  [FilterName.Players]: {
    type: UrlQueryParamTypes.string,
  },
  [FilterName.MOM]: {
    type: UrlQueryParamTypes.string,
  },
  [FilterName.LOM]: {
    type: UrlQueryParamTypes.string,
  },
  [FilterName.ReportAuthor]: {
    type: UrlQueryParamTypes.string,
  },
  [FilterName.Date]: {
    type: UrlQueryParamTypes.string,
  },
};

const MatchFilterSet = ({ teams, divisions, opposition_clubs, seasons, venues, members }) => {
  const clearAll = () => {
    pushUrlQuery({});
  };
  const teamOptions = teams.map(team => ({ value: team.slug, label: team.long_name }));
  const genderOptions = [
    { value: 'Mens', label: 'Mens' },
    { value: 'Ladies', label: 'Ladies' },
    { value: 'Mixed', label: 'Mixed' },
  ];
  const oppositionOptions = opposition_clubs.map(club => ({
    value: String(club.slug),
    label: club.name,
  }));
  const seasonOptions = seasons.map(season => ({ value: season, label: season }));
  const fixtureTypeOptions = keys(FixtureType).map(ft => ({ value: ft, label: ft }));
  const venueOptions = venues.map(venue => ({ value: String(venue.id), label: venue.name }));
  const memberOptions = members.map(member => ({ value: String(member.id), label: member.name }));
  return (
    <div>
      <div className="text-right">
        <button className="btn btn-link" onClick={clearAll}>
          Clear all
        </button>
      </div>
      <SelectFilter
        label="Gender"
        filterName={FilterName.Gender}
        options={genderOptions}
        urlQueryConfig={urlPropsQueryConfig[FilterName.Gender]}
        stacked
      />
      <SelectFilter
        label="Team"
        filterName={FilterName.Team}
        options={teamOptions}
        urlQueryConfig={urlPropsQueryConfig[FilterName.Team]}
        stacked
      />
      <SelectFilter
        label="Opposition"
        filterName={FilterName.Opposition}
        options={oppositionOptions}
        urlQueryConfig={urlPropsQueryConfig[FilterName.Opposition]}
        stacked
      />
      <SelectFilter
        label="Season"
        filterName={FilterName.Season}
        options={seasonOptions}
        urlQueryConfig={urlPropsQueryConfig[FilterName.Season]}
        stacked
      />
      <SelectFilter
        label="Fixture Type"
        filterName={FilterName.FixtureType}
        options={fixtureTypeOptions}
        urlQueryConfig={urlPropsQueryConfig[FilterName.FixtureType]}
        stacked
      />
      <SelectFilter
        label="Venue"
        filterName={FilterName.Venue}
        options={venueOptions}
        urlQueryConfig={urlPropsQueryConfig[FilterName.Venue]}
        stacked
      />
      <DateFilter
        label="Date"
        filterName={FilterName.Date}
        urlQueryConfig={urlPropsQueryConfig[FilterName.Date]}
        stacked
      />
      <SelectFilter
        label="Players"
        filterName={FilterName.Players}
        options={memberOptions}
        urlQueryConfig={urlPropsQueryConfig[FilterName.Players]}
        stacked
        multi
      />
      <SelectFilter
        label="Man of the Match"
        filterName={FilterName.MOM}
        options={memberOptions}
        urlQueryConfig={urlPropsQueryConfig[FilterName.MOM]}
        stacked
      />
      <SelectFilter
        label="Lemon of the Match"
        filterName={FilterName.LOM}
        options={memberOptions}
        urlQueryConfig={urlPropsQueryConfig[FilterName.LOM]}
        stacked
      />
      <SelectFilter
        label="Match Report Author"
        filterName={FilterName.ReportAuthor}
        options={memberOptions}
        urlQueryConfig={urlPropsQueryConfig[FilterName.ReportAuthor]}
        stacked
      />
    </div>
  );
};

MatchFilterSet.propTypes = {
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
  opposition_clubs: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number,
      name: PropTypes.string,
    }),
  ).isRequired,
  seasons: PropTypes.arrayOf(PropTypes.string).isRequired,
  venues: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number,
      name: PropTypes.string,
    }),
  ).isRequired,
  members: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number,
      name: PropTypes.string,
    }),
  ).isRequired,
};

export default MatchFilterSet;
