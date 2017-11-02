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
    if (nextProps.items) {
      if (nextProps.items.edges.length === 1) {
        this.setState({ openIndex: 0 });
      } else if (this.props.items.edges.length !== nextProps.items.edges.length) {
        this.setState({ openIndex: undefined });
      }
    }
  }

  onToggleItemOpen(index) {
    this.setState({ openIndex: index });
  }

  render() {
    const childrenWithProps = React.Children.map(this.props.children, (child, index) =>
      React.cloneElement(child, {
        isOpen: this.state.openIndex === index || false,
        onToggleOpen: this.onToggleItemOpen,
      }),
    );
    return (
      <GoogleMap
        defaultZoom={8}
        defaultCenter={DefaultMapCenter}
        onClick={() => this.onToggleItemOpen(null)}
      >
        {childrenWithProps}
      </GoogleMap>
    );
  }
}

Map.propTypes = {
  items: PropTypes.shape().isRequired,
  children: PropTypes.node.isRequired,
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
