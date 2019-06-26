import React, {PureComponent} from 'react'
import ReactMapboxGl, {
    Layer, Feature, Popup, RotationControl, ZoomControl
} from 'react-mapbox-gl'



export const coordinates = (listing) =>
    [parseFloat(listing.longitude), parseFloat(listing.latitude)]


const blue = ['#98CCFD', '#4788C7']
const gold = ['#FFD700', '#4C4000']

const svg_str = (color) => `
<svg xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" width="30" height="30"
viewBox="0 0 40 40" style=" fill:#000000;"><g id="surface1"><path style=" fill:${color[0]};"
d="M 20 38.25 C 17.894531 35.875 7.5 23.628906 7.5 14 C 7.5 7.105469 13.105469
1.5 20 1.5 C 26.894531 1.5 32.5 7.105469 32.5 14 C 32.5 23.578125 22.101563 35.867188
20 38.25 Z "></path><path style=" fill:${color[1]};" d="M 20 2 C 26.617188 2 32 7.382813
32 14 C 32 22.933594 22.710938 34.347656 20 37.492188 C 17.285156 34.359375 8 22.976563
8 14 C 8 7.382813 13.382813 2 20 2 M 20 1 C 12.820313 1 7 6.820313 7 14 C 7 24.980469
20 39 20 39 C 20 39 33 24.925781 33 14 C 33 6.820313 27.179688 1 20 1 Z "></path>
<path style=" fill:#FFFFFF;" d="M 25.5 14 C 25.5 17.039063 23.039063 19.5 20 19.5 C
16.960938 19.5 14.5 17.039063 14.5 14 C 14.5 10.960938 16.960938 8.5 20 8.5 C 23.039063
8.5 25.5 10.960938 25.5 14 Z "></path><path style=" fill:${color[1]};" d="M 20 9 C 22.761719
9 25 11.238281 25 14 C 25 16.761719 22.761719 19 20 19 C 17.238281 19 15 16.761719 15 14
C 15 11.238281 17.238281 9 20 9 M 20 8 C 16.691406 8 14 10.691406 14 14 C 14 17.308594
16.691406 20 20 20 C 23.308594 20 26 17.308594 26 14 C 26 10.691406 23.308594 8 20 8 Z ">
</path></g></svg>
`

const blue_marker = new Image()
blue_marker.src = 'data:image/svg+xml;charset=utf-8;base64,' + btoa(svg_str(blue))

const gold_marker = new Image()
gold_marker.src = 'data:image/svg+xml;charset=utf-8;base64,' + btoa(svg_str(gold))

const images = [['listing_marker', blue_marker], ['listing_highlighted', gold_marker]]

const layoutBlueLayer = { 'icon-image': 'listing_marker' }
const layoutGoldLayer = { 'icon-image': 'listing_highlighted' }



const Mapbox = ReactMapboxGl({
    minZoom: 11,
    maxZoom: 17,
    accessToken: global.props.map_key
})

const maxBounds = [[-74.363101, 40.400624], [-73.600364, 40.993590]]


export class MapComponent extends PureComponent {
    constructor(props) {
        super(props)
        this.state = {
            popup_listing: undefined,
        }
    }

    markerHover(map, popup_listing, cursor) {
        map.getCanvas().style.cursor = cursor
        this.setState({popup_listing})
    }

    render() {
        const {listings, center, zoom, listing_highlighted, clickOn} = this.props
        const {popup_listing} = this.state

        const blue_listings = listings.filter(listing => listing.id != listing_highlighted.id)
        const gold_listings = listings.filter(listing => listing.id == listing_highlighted.id)

        return (
            <Mapbox
                style="mapbox://styles/mapbox/light-v9"
                maxBounds={maxBounds}
                center={center}
                zoom={zoom}
                className="mapbox-component"
                movingMethod="easeTo"
              >
                <RotationControl />
                <ZoomControl />
                <Layer type="symbol" id="blue_markers" layout={layoutBlueLayer} images={images}>
                    {blue_listings.map(listing => (
                        <Feature
                            key={`feature-${listing.id}`}
                            onMouseEnter={({map}) => this.markerHover(map, listing, 'pointer')}
                            onMouseLeave={({map}) => this.markerHover(map, undefined, '')}
                            onClick={() => clickOn(listing)}
                            coordinates={coordinates(listing)}
                        />
                    ))}
                </Layer>
                <Layer type="symbol" id="gold_markers" layout={layoutGoldLayer} images={images}>
                    {gold_listings.map(listing => (
                        <Feature
                            key={`feature-${listing.id}`}
                            onMouseEnter={({map}) => this.markerHover(map, listing, 'pointer')}
                            onMouseLeave={({map}) => this.markerHover(map, undefined, '')}
                            onClick={() => clickOn(listing)}
                            coordinates={coordinates(listing)}
                        />
                    ))}
                </Layer>
                {popup_listing && (
                    <Popup key={`popup-${popup_listing.id}`} coordinates={coordinates(popup_listing)} offset={{'bottom': [0,-15]}}>
                        <div class="card card-smallcard-post card-post--1 card-listing overlay-parent">
                            <div class="card-post__image text-center">
                                <img style={{width: '24vw', maxHeight: 170}} src={popup_listing.default_image} />
                                {popup_listing.no_fee_listing &&
                                    <span class="card-post__category left-badge badge badge-pill badge-info">no fee</span>
                                }
                                <span class="card-post__category badge badge-pill badge-dark">${popup_listing.price}</span>
                            </div>
                            <div class="card-body p-0 text-center">
                                <table class="table mb-0 listing-info">
                                    <tbody>
                                        <tr>
                                            <td class="wrap-info">
                                                {parseFloat(popup_listing.bedrooms).toString()} Beds / {parseFloat(popup_listing.bathrooms).toString()} Bath
                                            </td>
                                            <td class="wrap-info">
                                                {popup_listing.pets}
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </Popup>
                )}
            </Mapbox>
        )
    }
}



