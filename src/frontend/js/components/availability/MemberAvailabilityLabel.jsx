import React from 'react';
import PropTypes from 'prop-types';
import classnames from 'classnames';
import { MatchAvailability } from 'util/constants';

const MemberAvailabilityLabel = ({ className, availability }) => {
  let labelClass = classnames('u-label', className);
  let iconClass = null;
  let title = null;
  switch (availability) {
    case MatchAvailability.Available:
      title = 'Available';
      labelClass += ' g-bg-green';
      iconClass = 'fas fa-check';
      break;
    case MatchAvailability.NotAvailable:
      title = 'Not available';
      labelClass += ' g-bg-red';
      iconClass = 'fas fa-times';
      break;
    case MatchAvailability.Unsure:
      title = 'Not sure';
      labelClass += ' g-bg-gray-dark-v4';
      iconClass = 'fas fa-question';
      break;
    case MatchAvailability.AwaitingResponse:
    default:
      title = 'Awaiting response';
      labelClass += ' g-bg-secondary g-color-black';
      iconClass = 'fas fa-ellipsis-h';
      break;
  }
  return (
    <span className={labelClass} title={title}>
      <i className={iconClass} />
    </span>
  );
};

MemberAvailabilityLabel.propTypes = {
  className: PropTypes.string,
  availability: PropTypes.string.isRequired,
};

MemberAvailabilityLabel.defaultProps = {
  className: undefined,
};

export default MemberAvailabilityLabel;
