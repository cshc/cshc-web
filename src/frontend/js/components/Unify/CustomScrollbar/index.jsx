import React from 'react';
import PropTypes from 'prop-types';

/**
 * Represents a custom scrollbar.
 * 
 * Notes: 
 *  - jquery.mCustomScrollbar.min.css must be included in the page head
 *  - jquery.min.js and jquery.mCustomScrollbar.concat.min.js must be included in the body
 *  - Assumes window.jQuery is accessible
 * 
 * Ref: http://manos.malihu.gr/jquery-custom-content-scroller/
 */
class CustomScrollbar extends React.Component {
  componentDidMount() {
    window.jQuery('.mCustomScrollbar').mCustomScrollbar();
  }

  render() {
    const { maxHeight, children } = this.props;
    return (
      <div
        ref={(scrollbar) => {
          this.scrollbar = scrollbar;
        }}
        className="js-scrollbar  u-info-v1-1 g-bg-white-gradient-v1--after mCustomScrollbar"
        style={maxHeight ? { maxHeight } : {}}
        data-mcs-theme="minimal-dark"
      >
        {children}
      </div>
    );
  }
}

CustomScrollbar.propTypes = {
  maxHeight: PropTypes.string,
  children: PropTypes.node.isRequired,
};

CustomScrollbar.defaultProps = {
  maxHeight: '200px',
};

export default CustomScrollbar;
