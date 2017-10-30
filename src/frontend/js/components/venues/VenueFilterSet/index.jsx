import React from 'react';
import PropTypes from 'prop-types';
import uniqBy from 'lodash/uniqBy';
import { FilterName } from 'util/constants';
import Subheading from 'components/common/Subheading';
import { BooleanFilter, TextFilter, RadioGroupFilter } from 'components/filters';
import filtered from 'components/filters/filterContainer';

const VenueFilterSet = ({ currentSeason, teams, divisions }) => {
  const SearchFilter = filtered(FilterName.TextSearch)(TextFilter);
  const HomeGroundFilter = filtered(FilterName.HomeGround)(BooleanFilter);
  const CurrentSeasonFilter = filtered(FilterName.Season)(BooleanFilter);
  const TeamFilter = filtered(FilterName.VenueTeam)(RadioGroupFilter);
  const teamOptions = teams.map(team => ({ value: team.slug, label: team.long_name }));
  const DivisionFilter = filtered(FilterName.VenueDivision)(RadioGroupFilter);
  const divisionOptions = uniqBy(divisions, 'id').map(division => ({
    value: division.id,
    label: division.name,
  }));

  teamOptions.unshift({ value: undefined, label: 'All' });
  divisionOptions.unshift({ value: undefined, label: 'Any' });
  return (
    <div>
      <SearchFilter />
      <HomeGroundFilter label="Home Grounds" />
      <CurrentSeasonFilter label="Current Season" trueValue={currentSeason} />
      <Subheading>Team</Subheading>
      <TeamFilter options={teamOptions} />
      <Subheading>Division</Subheading>
      <DivisionFilter options={divisionOptions} />
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

VenueFilterSet.defaultProps = {};

export default VenueFilterSet;
