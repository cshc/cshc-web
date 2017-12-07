import React from 'react';
import PropTypes from 'prop-types';

/**
 * React implementation of a Unify subheading
 * 
 * Should correspond to /cshc/templates/blocks/_subheading.html
 */
const Subheading = ({ text, id }) => (
  <div id={id} className="u-heading-v1-4 g-bg-main g-brd-gray-light-v2 g-my-20">
    <h2 className="h3 u-heading-v1__title">{text}</h2>
  </div>
);

Subheading.propTypes = {
  text: PropTypes.string.isRequired,
  id: PropTypes.string,
};

Subheading.defaultProps = {
  id: undefined,
};

export default Subheading;
