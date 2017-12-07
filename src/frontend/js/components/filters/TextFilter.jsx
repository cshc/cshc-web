import React from 'react';
import PropTypes from 'prop-types';
import classnames from 'classnames';
import styles from './style.scss';

class TextFilter extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      value: props.filterValue,
    };
    this.onSearch = this.onSearch.bind(this);
    this.onChange = this.onChange.bind(this);
    this.onReset = this.onReset.bind(this);
    this.onKeyPress = this.onKeyPress.bind(this);
  }

  onSearch() {
    this.props.onSetFilter(this.props.filterName, this.textInput.value);
  }

  onChange(ev) {
    this.setState({ value: ev.target.value });
  }

  onReset() {
    this.setState({ value: '' }, this.onSearch);
  }

  onKeyPress(e) {
    if (e.key === 'Enter') {
      this.onSearch();
    }
  }

  render() {
    const { placeholder, filterName } = this.props;
    const wrapperClass = classnames(styles.filter, 'g-py-10');
    return (
      <div className={wrapperClass}>
        <div className="input-group g-brd-primary--focus">
          <input
            id={filterName}
            ref={(input) => {
              this.textInput = input;
            }}
            className="form-control form-control-md rounded-0"
            type="text"
            value={this.state.value}
            placeholder={placeholder}
            onChange={this.onChange}
            onKeyPress={this.onKeyPress}
          />
          <span className="input-group-btn">
            <button
              className="btn btn-md u-btn-primary rounded-0"
              type="button"
              disabled={!this.state.value}
              onClick={this.onSearch}
            >
              <i className="fa fa-search" />
            </button>
          </span>
          <button
            className="btn btn-md btn-link"
            disabled={!this.props.filterValue && !this.state.value}
            onClick={this.onReset}
            title="Reset"
          >
            <i className="fa fa-times" />
          </button>
        </div>
      </div>
    );
  }
}

TextFilter.propTypes = {
  placeholder: PropTypes.string,
  filterName: PropTypes.string.isRequired,
  onSetFilter: PropTypes.func.isRequired,
  filterValue: PropTypes.string,
};

TextFilter.defaultProps = {
  placeholder: 'Search...',
  filterValue: '',
};

export default TextFilter;
