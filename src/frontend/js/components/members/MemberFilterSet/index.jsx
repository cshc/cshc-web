import React from 'react';
import PropTypes from 'prop-types';
import { FilterName, Gender, Position, NoFilter } from 'util/constants';
import { FilterGroup, BooleanFilter, TextFilter, OptionListFilter } from 'components/filters';

const MemberFilterSet = ({ teams }) => {
  const teamOptions = teams.map(team => ({ value: team.slug, label: team.long_name }));
  teamOptions.unshift({ value: NoFilter, label: 'All' });
  const genderOptions = [
    { value: NoFilter, label: 'Men & Ladies' },
    { value: Gender.MALE, label: 'Men' },
    { value: Gender.FEMALE, label: 'Ladies' },
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
      <TextFilter filterName={FilterName.TextSearch} />
      <BooleanFilter filterName={FilterName.Current} label="Current" />
      <BooleanFilter filterName={FilterName.Captains} label="Captains/Vice-Captains only" />
      <FilterGroup title="Gender">
        <OptionListFilter filterName={FilterName.Gender} options={genderOptions} />
      </FilterGroup>
      <FilterGroup title="Current Squad">
        <OptionListFilter filterName={FilterName.Team} options={teamOptions} />
      </FilterGroup>
      <FilterGroup title="Position">
        <OptionListFilter filterName={FilterName.Position} options={positionOptions} multiselect />
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
