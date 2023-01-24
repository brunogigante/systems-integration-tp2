import React, {useEffect, useState} from 'react';
import {LayerGroup, useMap} from 'react-leaflet';
import {ObjectMarker} from "./ObjectMarker";
import {closestPointOnSegment} from "leaflet/src/geometry/LineUtil";


function ObjectMarkersGroup() {

    const map = useMap();
    const [geom, setGeom] = useState([]);
    const [bounds, setBounds] = useState(map.getBounds());
    /**
     * Gets the Markers for the map
     */

    const getMarkers = async () => {
        fetch(`http://localhost:20002/api/markers?neLat=${bounds['_northEast']['lat']}&neLng=${bounds['_northEast']['lng']}&swLat=${bounds['_southWest']['lat']}&swLng=${bounds['_southWest']['lng']}`)
            .then(response => response.json())
            .then(geoJSON => {
                console.log(geoJSON);
            setGeom(geoJSON.flat());
        })

    }

    /**
     * Setup the event to update the bounds automatically
     */
    useEffect(() => {
        const cb = () => {
            setBounds(map.getBounds());
        }
        map.on('moveend', cb);

        return () => {
            map.off('moveend', cb);
        }
    }, []);

    /* Updates the data for the current bounds */
    useEffect(() => {
        getMarkers().then(() => console.log('resolvido')).catch()

        console.log(`> getting data for bounds`, bounds);
    }, [bounds])

    return (
        <LayerGroup>
            {
                geom&& geom.map(geoJSON => <ObjectMarker key={geoJSON.properties.store} position={geoJSON.properties.geometry} geoJSON={geoJSON}/>)
            }
        </LayerGroup>
    );
}

export default ObjectMarkersGroup;
