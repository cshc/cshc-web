import React from 'react';
import PropTypes from 'prop-types';
import classnames from 'classnames';

/**
 *  A touch-friendly component for entering a numeric value using up/down buttons
 *  to increment/decrement the value.
 * 
 *  Note: this component does not currently support entering a value directly.
 */
const NumberInput = ({
  disabled,
  horizontal,
  upIcon,
  downIcon,
  iconClass,
  value,
  valueClass,
  onChangeValue,
}) => {
  const outerClass = classnames('d-flex align-items-center g-mx-4', {
    'flex-column': !horizontal,
    'flex-row-reverse': horizontal,
  });
  const upIconClass = classnames(upIcon, iconClass, {
    'g-pr-10 g-py-10': horizontal,
    'g-pt-10 g-px-10': !horizontal,
  });
  const downIconClass = classnames(downIcon, iconClass, {
    'g-pl-10 g-py-10': horizontal,
    'g-pb-10 g-px-10': !horizontal,
  });
  return (
    <div className={outerClass}>
      <button
        disabled={disabled}
        className="btn btn-link g-pa-0"
        onClick={() => onChangeValue((value || 0) + 1)}
      >
        <i className={upIconClass} />
      </button>
      <div className={`g-py-5 g-px-8 ${valueClass}`}>
        {value === undefined || value === null ? <span>&nbsp;</span> : value}
      </div>
      <button
        disabled={disabled || !value}
        className="btn btn-link g-pa-0"
        onClick={() => onChangeValue(value - 1)}
      >
        <i className={downIconClass} />
      </button>
    </div>
  );
};

NumberInput.propTypes = {
  disabled: PropTypes.bool,
  horizontal: PropTypes.bool,
  value: PropTypes.number,
  upIcon: PropTypes.string,
  downIcon: PropTypes.string,
  iconClass: PropTypes.string,
  valueClass: PropTypes.string,
  onChangeValue: PropTypes.func.isRequired,
};

NumberInput.defaultProps = {
  disabled: false,
  horizontal: false,
  value: undefined,
  upIcon: 'fa fa-caret-up',
  downIcon: 'fa fa-caret-down',
  iconClass:
    'g-color-gray-dark-v4 g-color-gray-dark-v1--hover g-font-size-18 g-font-size-24--md g-font-size-35--lg',
  valueClass: 'g-bg-primary g-color-white',
};

export default NumberInput;
