import React, {PureComponent} from 'react';
import ReactMapGL, {Marker, NavigationControl} from 'react-map-gl';

import 'mapbox-gl/dist/mapbox-gl.css'


const ICON = `
M20.2,15.7L20.2,15.7c1.1-1.6,1.8-3.6,1.8-5.7c0-5.6-4.5-10-10-10S2,4.5,2,10c0,2,
0.6,3.9,1.6,5.4c0,0.1,0.1,0.2,0.2,0.3c0,0,0.1,0.1,0.1,0.2c0.2,0.3,0.4,0.6,0.7,
0.9c2.6,3.1,7.4,7.6,7.4,7.6s4.8-4.5,7.4-7.5c0.2-0.3,0.5-0.6,0.7-0.9C20.1,15.8,
20.2,15.8,20.2,15.7z
`

class Pin extends PureComponent {
    render() {
        const {size = 20, onClick} = this.props
        const pin_props = {
            height: size,
            viewBox: "0 0 24 24",
            onClick: onClick,
            style: {
                fill: '#d00',
                stroke: 'none',
                cursor: 'pointer',
                transform: `translate(${-size / 2}px,${-size}px)`,
            }
        }        

        return (
            <svg {...pin_props}>
               <path d={ICON} />
            </svg>
        )
    }
}

export class MapComponent extends PureComponent {
    constructor(props) {
        super(props)
        this.state = {
            viewport: {
                width: '100%',
                height: '100%',
                latitude: 40.654089,
                longitude: -73.942423,
                zoom: 11.5
            }
        }
    }

    renderMarker(listing, index) {
        const marker_props = {
            key: `marker-${index}`,
            latitude: parseFloat(listing.latitude),
            longitude: parseFloat(listing.longitude),
        }

        return (
            <Marker {...marker_props}>
                <Pin size={25} onClick={() => console.log(listing)} />
            </Marker>
        )
    }

    render() {
        const {listings, map_key} = this.props

        return (
            <ReactMapGL {...this.state.viewport}
                        mapStyle="mapbox://styles/mapbox/streets-v8"
                        mapboxApiAccessToken={map_key}
                        onViewportChange={(viewport) => this.setState({viewport})} >

                <div style={{position: 'absolute', right: 0}}>
                    <NavigationControl />
                </div>

                {listings.map(this.renderMarker)}

            </ReactMapGL>
        )
    }
}



