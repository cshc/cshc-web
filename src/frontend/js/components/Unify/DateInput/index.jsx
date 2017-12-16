import React from 'react';
import PropTypes from 'prop-types';
import styles from './style.scss';

class DateInput extends React.PureComponent {
  constructor(props) {
    super(props);
    this.onClose = this.onClose.bind(this);
    this.onSelect = this.onSelect.bind(this);
  }

  componentDidMount() {
    window.jQuery.HSCore.components.HSDatepicker.init(`#datepicker-${this.props.name}`, {
      dateFormat: 'dd-mm-yy',
      onSelect: this.onSelect,
    });
    window.jQuery.HSCore.helpers.HSFocusState.init();
  }

  componentWillUnmount() {
    window.jQuery(this.input).datepicker('destroy');
  }

  onClose(dateText) {
    this.props.onChange(dateText);
  }

  onSelect(dateText) {
    this.props.onChange(dateText);
  }

  render() {
    const { name, value, onChange, clearable } = this.props;
    return (
      <div className="input-group g-brd-primary--focus">
        <input
          ref={(datepicker) => {
            this.datepicker = datepicker;
          }}
          id={`datepicker-${name}`}
          type="text"
          placeholder="Select..."
          name={name}
          value={value}
          onChange={newValue => onChange(newValue.target.value)}
          className="form-control form-control-md u-datepicker-v1 g-brd-right-none rounded-0 unify-datepicker"
        />
        {clearable &&
          value && (
            <div
              title="Clear value"
              aria-label="Clear value"
              role="button"
              tabIndex="0"
              className={`${styles.clear} input-group-addon d-flex align-items-center g-bg-white g-color-gray-dark-v5 rounded-0`}
              onClick={() => onChange(undefined)}
            >
              ×
            </div>
          )}
        <div className="input-group-addon d-flex align-items-center g-bg-white g-color-gray-dark-v5 rounded-0">
          <i className="icon-calendar" />
        </div>
      </div>
    );
  }
}

DateInput.propTypes = {
  name: PropTypes.string.isRequired,
  onChange: PropTypes.func.isRequired,
  value: PropTypes.string,
  clearable: PropTypes.bool,
};

DateInput.defaultProps = {
  value: '',
  clearable: true,
};

export default DateInput;
