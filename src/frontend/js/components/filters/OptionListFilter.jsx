import React from 'react';
import PropTypes from 'prop-types';
import classnames from 'classnames';
import without from 'lodash/without';
import concat from 'lodash/concat';
import { FilterValuePropType } from 'components/common/PropTypes';
import OptionList from 'components/common/OptionList';
import styles from './style.scss';

const OptionListFilter = ({
  options,
  filterName,
  filterValue,
  onSetFilter,
  multiselect,
  inline,
}) => {
  const onChange = (ev) => {
    let newValue = ev.target.value;
    if (multiselect) {
      newValue = ev.target.checked
        ? concat(filterValue || [], ev.target.value)
        : without(filterValue || [], ev.target.value);
    }
    onSetFilter(filterName, newValue);
  };
  const filterClass = classnames('g-py-10', {
    [styles.inline]: inline,
  });
  return (
    <OptionList
      className={filterClass}
      name={filterName}
      selectedValue={filterValue}
      onChange={onChange}
      options={options}
      multiselect={multiselect}
      inline={inline}
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
  inline: PropTypes.bool,
};

OptionListFilter.defaultProps = {
  filterValue: undefined,
  multiselect: false,
  inline: false,
};

export default OptionListFilter;
