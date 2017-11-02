import React from 'react';
import PropTypes from 'prop-types';
import without from 'lodash/without';
import concat from 'lodash/concat';
import { FilterValuePropType } from 'components/common/PropTypes';
import OptionList from 'components/common/OptionList';
import filtered from './filterContainer';

const OptionListFilter = ({ options, filterName, filterValue, onSetFilter, multiselect }) => {
  const onChange = (ev) => {
    let newValue = ev.target.value;
    if (multiselect) {
      newValue = ev.target.checked
        ? concat(filterValue || [], ev.target.value)
        : without(filterValue || [], ev.target.value);
    }
    onSetFilter(filterName, newValue);
  };
  return (
    <OptionList
      className="g-py-10"
      options={options}
      name={filterName}
      selectedValue={filterValue}
      onChange={onChange}
      multiselect={multiselect}
    />
  );
};

OptionListFilter.propTypes = {
  filterName: PropTypes.string.isRequired,
  onSetFilter: PropTypes.func.isRequired,
  filterValue: FilterValuePropType,
  options: PropTypes.arrayOf(
    PropTypes.shape({
      label: PropTypes.string,
      value: FilterValuePropType,
    }),
  ).isRequired,
  multiselect: PropTypes.bool,
};

OptionListFilter.defaultProps = {
  filterValue: undefined,
  multiselect: false,
};

export default filtered(OptionListFilter);
