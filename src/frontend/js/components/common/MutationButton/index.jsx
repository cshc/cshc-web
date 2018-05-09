import React from 'react';
import PropTypes from 'prop-types';
import classnames from 'classnames';

/**
 * A button that handles a mutation action. 
 * 
 * The actual mutation function and a function to retrieve/build
 * the mutation payload is injected via props. The mutation function
 * should be a promise (as this component calls then().catch() on it).
 * 
 * An optional function can be passed in to check if the mutation
 * response is valid. Otherwise the default implementation just checks
 * if the errors field has been populated.
 * 
 * When the mutation is initiated, the button is disabled and the 
 * intermediate text is displayed with a spinner icon.
 * 
 * When the mutation completes, the mutation result is briefly displayed
 * (by default for 1000ms) before the button is re-enabled and returned
 * to its initial state.
 */
class MutationButton extends React.PureComponent {
  constructor(props) {
    super(props);
    this.state = {
      locked: false,
      icon: props.icon,
      label: props.label,
    };
    this.onClick = this.onClick.bind(this);
    this.setDefault = this.setDefault.bind(this);
    this.setInProgress = this.setInProgress.bind(this);
    this.setSuccess = this.setSuccess.bind(this);
    this.setFail = this.setFail.bind(this);
  }

  /**
   * When the button is pressed, we call the 'getMutationInput' callback to retrieve
   * the mutation payload, then call the mutation. 
   * 
   * If the mutation succeeds, we call the 'onSuccess' callback (if set). 
   * 
   * If the mutation fails, we call the 'onFail' callback (if set).
   */
  onClick() {
    const { mutate, getMutationInput, validateData, onSuccess, onFail } = this.props;
    this.setInProgress(() => {
      mutate(getMutationInput())
        .then(({ data }) => {
          const errors = validateData(data);
          if (errors) {
            this.setFail(() => {
              if (onFail) onFail(errors);
              this.setDefault();
            });
          } else {
            this.setSuccess(() => {
              if (onSuccess) onSuccess(data);
              this.setDefault();
            });
          }
        })
        .catch((errors) => {
          this.setFail(onFail ? () => onFail(errors) : this.setDefault);
        });
    });
  }

  setDefault() {
    this.setState({ locked: false, label: this.props.label, icon: this.props.icon });
  }

  setInProgress(callback = undefined) {
    this.setState(
      { locked: true, label: this.props.inProgressLabel, icon: 'fas fa-spinner fa-spin' },
      callback,
    );
  }

  setSuccess(callback = undefined) {
    this.setState({ locked: true, label: this.props.successLabel, icon: 'fas fa-check' }, () => {
      window.setTimeout(callback, this.props.feedbackDelayMs);
    });
  }

  setFail(callback = undefined) {
    this.setState({ locked: true, label: this.props.failLabel, icon: 'fas fa-exclamation' }, () => {
      window.setTimeout(callback, this.props.feedbackDelayMs);
    });
  }

  mutate() {
    this.onClick();
  }

  render() {
    const { buttonClass, title, disabled, passive } = this.props;
    const { locked, icon, label } = this.state;
    const btnClass = classnames(buttonClass);
    return (
      <button
        title={title}
        className={btnClass}
        disabled={passive || disabled || locked}
        onClick={this.onClick}
      >
        {icon ? <i className={`${icon} g-mr-5`} /> : null}
        {label}
      </button>
    );
  }
}

MutationButton.propTypes = {
  buttonClass: PropTypes.string,
  passive: PropTypes.bool,
  title: PropTypes.string,
  label: PropTypes.string,
  icon: PropTypes.node,
  disabled: PropTypes.bool,
  mutate: PropTypes.func.isRequired,
  getMutationInput: PropTypes.func.isRequired,
  validateData: PropTypes.func,
  onSuccess: PropTypes.func,
  onFail: PropTypes.func,
  inProgressLabel: PropTypes.string,
  failLabel: PropTypes.string,
  successLabel: PropTypes.string,
  feedbackDelayMs: PropTypes.number,
};

MutationButton.defaultProps = {
  buttonClass: 'btn btn-block u-btn-primary',
  passive: false,
  title: undefined,
  label: undefined,
  icon: undefined,
  disabled: false,
  onSuccess: undefined,
  onFail: undefined,
  validateData: data => data.errors && data.errors.length > 0,
  inProgressLabel: 'Saving...',
  failLabel: 'Failed to save',
  successLabel: 'Saved!',
  feedbackDelayMs: 1000,
};

export default MutationButton;
