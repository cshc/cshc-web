import React from 'react';
import PropTypes from 'prop-types';
import { SlideListPropType } from '../PropTypes';
import styles from './NavigationNode/style.scss';

/**
 * Wrapper around the row of navigation nodes. Clicking on a navigation
 * node will select the corresponding slide in the slider.
 */
class MultiStepFormNavigation extends React.PureComponent {
  constructor(props) {
    super(props);
    this.state = {
      currentSlideIndex: 0,
    };
  }

  onSlideChange(oldIndex, newIndex) {
    this.setState({ currentSlideIndex: newIndex });
  }

  render() {
    const { slides, onSelectSlide } = this.props;
    const { currentSlideIndex } = this.state;
    const navStyle = { maxWidth: `${slides.length * 150}px` };
    return (
      <div className={styles.msNav} style={navStyle}>
        {slides.map((slide, index) => (
          <slide.navigationNode
            key={slide.label}
            current={currentSlideIndex === index}
            onClick={() => {
              onSelectSlide(index);
            }}
          />
        ))}
      </div>
    );
  }
}

MultiStepFormNavigation.propTypes = {
  slides: SlideListPropType.isRequired,
  onSelectSlide: PropTypes.func.isRequired,
};

export default MultiStepFormNavigation;
