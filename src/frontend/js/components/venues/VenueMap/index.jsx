import React from 'react';
import PropTypes from 'prop-types';
import { compose, withProps } from 'recompose';
import { DefaultMapCenter } from 'util/constants';
import { withScriptjs, withGoogleMap, GoogleMap } from 'react-google-maps';
import VenueMarker from './VenueMarker';

class Map extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      openVenue: undefined,
    };
    this.onToggleVenueOpen = this.onToggleVenueOpen.bind(this);
  }

  componentWillReceiveProps(nextProps) {
    if (nextProps.venues) {
      if (nextProps.venues.edges.length === 1) {
        this.setState({ openVenue: nextProps.venues.edges[0].node });
      } else if (this.props.venues.edges.length !== nextProps.venues.edges.length) {
        this.setState({ openVenue: null });
      }
    }
  }

  onToggleVenueOpen(venue) {
    this.setState({ openVenue: venue });
  }

  render() {
    return (
      <GoogleMap
        defaultZoom={8}
        defaultCenter={DefaultMapCenter}
        onClick={() => this.onToggleVenueOpen(null)}
      >
        {this.props.venues.edges.map(venueEdge => (
          <VenueMarker
            key={venueEdge.node.slug}
            venue={venueEdge.node}
            isOpen={
              (this.state.openVenue && this.state.openVenue.slug === venueEdge.node.slug) || false
            }
            onToggleOpen={this.onToggleVenueOpen}
          />
        ))}
      </GoogleMap>
    );
  }
}

Map.propTypes = {
  venues: PropTypes.shape().isRequired,
};

const VenueMap = compose(
  withProps({
    googleMapURL: `https://maps.googleapis.com/maps/api/js?v=3.exp&key=${window.gmapsApiKey}`,
    loadingElement: <div style={{ height: '100%' }} />,
    containerElement: <div style={{ height: '800px' }} />,
    mapElement: <div style={{ height: '100%' }} />,
  }),
  withScriptjs,
  withGoogleMap,
)(Map);

VenueMap.defaultProps = {};

export default VenueMap;
