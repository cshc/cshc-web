import React from 'react';
import PropTypes from 'prop-types';

const displayBreakpoints = {
  xl: { abbr: 'g-hidden-xl-up', verbose: 'g-hidden-lg-down' },
  lg: { abbr: 'g-hidden-lg-up', verbose: 'g-hidden-md-down' },
  md: { abbr: 'g-hidden-md-up', verbose: 'g-hidden-sm-down' },
  sm: { abbr: 'g-hidden-sm-up', verbose: 'g-hidden-xs-down' },
};

/**
 * Abbreviates the verbose text if below the specified breakpoint.
 * 
 * Breakpoint can be 'sm', 'md', 'lg' or 'xl'
 */
const ResponsiveAbbr = ({ breakpoint, verbose, abbreviated }) => (
  <span>
    <abbr className={displayBreakpoints[breakpoint].abbr} title={verbose}>
      {abbreviated}
    </abbr>
    <span className={displayBreakpoints[breakpoint].verbose}>{verbose}</span>
  </span>
);

ResponsiveAbbr.propTypes = {
  breakpoint: PropTypes.oneOf(['sm', 'md', 'lg', 'xl']),
  verbose: PropTypes.string.isRequired,
  abbreviated: PropTypes.string.isRequired,
};

ResponsiveAbbr.defaultProps = {
  breakpoint: 'lg',
};

export default ResponsiveAbbr;
