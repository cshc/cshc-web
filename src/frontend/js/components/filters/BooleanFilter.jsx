import React from 'react';
import PropTypes from 'prop-types';
import classnames from 'classnames';
import { FilterValuePropType } from 'components/common/PropTypes';
import styles from './style.scss';

const BooleanFilter = ({ label, filterName, filterValue, onSetFilter, falseValue, trueValue }) => {
  const wrapperClass = classnames(styles.filter, 'g-py-10');
  const onChange = (ev) => {
    onSetFilter(filterName, ev.target.checked ? trueValue : falseValue);
  };
  return (
    <div className={wrapperClass}>
      <div className={styles.filterLabel}>{label}</div>
      <div className={styles.filterControl}>
        <label htmlFor={filterName} className="form-check-inline u-check g-mr-20 mx-0 mb-0">
          <input
            id={filterName}
            className="g-hidden-xs-up g-pos-abs g-top-0 g-right-0"
            name="radGroup1_1"
            type="checkbox"
            value={filterValue || false}
            checked={filterValue || false}
            onChange={onChange}
          />
          <div className="u-check-icon-radio-v7">
            <i className="d-inline-block" />
          </div>
        </label>
      </div>
    </div>
  );
};

BooleanFilter.propTypes = {
  label: PropTypes.string.isRequired,
  filterName: PropTypes.string.isRequired,
  onSetFilter: PropTypes.func.isRequired,
  filterValue: FilterValuePropType,
  falseValue: FilterValuePropType,
  trueValue: FilterValuePropType,
};

BooleanFilter.defaultProps = {
  filterValue: false,
  falseValue: false,
  trueValue: true,
};

export default BooleanFilter;
