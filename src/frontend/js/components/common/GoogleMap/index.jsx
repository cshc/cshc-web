import React from 'react';
import PropTypes from 'prop-types';
import { compose, withProps } from 'recompose';
import { DefaultMapCenter } from 'util/constants';
import { withScriptjs, withGoogleMap, GoogleMap } from 'react-google-maps';

class Map extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      openIndex: undefined,
    };
    this.onToggleItemOpen = this.onToggleItemOpen.bind(this);
  }

  componentWillReceiveProps(nextProps) {
    if (nextProps.markers) {
      if (nextProps.markers.length === 1) {
        this.setState({ openIndex: 0 });
      } else if (this.props.markers.length !== nextProps.markers.length) {
        this.setState({ openIndex: undefined });
      }
    }
  }

  onToggleItemOpen(index) {
    if (!this.state.openIndex) {
      this.setState({ openIndex: index });
    } else {
      this.setState({ openIndex: undefined });
    }
  }

  render() {
    const markersWithProps = React.Children.map(this.props.markers, (child, index) =>
      React.cloneElement(child, {
        isOpen: this.state.openIndex === index || false,
        onClick: () => this.onToggleItemOpen(index),
      }),
    );
    return (
      <GoogleMap
        defaultZoom={8}
        defaultCenter={DefaultMapCenter}
        onClick={() => this.onToggleItemOpen(null)}
      >
        {markersWithProps}
        {this.props.children}
      </GoogleMap>
    );
  }
}

Map.propTypes = {
  children: PropTypes.node,
  markers: PropTypes.node,
};

Map.defaultProps = {
  children: undefined,
  markers: undefined,
};

const ComposedMap = compose(
  withProps({
    googleMapURL: `https://maps.googleapis.com/maps/api/js?v=3.exp&key=${window.gmapsApiKey}`,
    loadingElement: <div style={{ height: '100%' }} />,
    containerElement: <div style={{ height: '800px' }} />,
    mapElement: <div style={{ height: '100%' }} />,
  }),
  withScriptjs,
  withGoogleMap,
)(Map);

export default ComposedMap;
