import React from 'react';
import PropTypes from 'prop-types';

/**
 * A React implementation of the Unify Accordion component. 
 * 
 * Ref: https://htmlstream.com/preview/unify-v2.2/unify-main/shortcodes/shortcode-base-accordions.html#shortcode10
 */
const Accordion = ({ children, accordionId, multiselectable }) => (
  <div
    id={accordionId}
    className="u-accordion u-accordion-color-primary u-accordion-brd-primary"
    role="tablist"
    aria-multiselectable={multiselectable}
  >
    {children}
  </div>
);

Accordion.propTypes = {
  accordionId: PropTypes.string.isRequired,
  children: PropTypes.oneOfType([PropTypes.arrayOf(PropTypes.element), PropTypes.element])
    .isRequired,
  multiselectable: PropTypes.bool,
};

Accordion.defaultProps = {
  multiselectable: false,
};

export default Accordion;
