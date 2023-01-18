import React, {useEffect, useState} from 'react';
import {LayerGroup, useMap} from 'react-leaflet';
import {ObjectMarker} from "./ObjectMarker";


const DEMO_DATA = [
    {
        "type": "feature",
        "geometry": {
            "type": "Point",
            "coordinates": [41.69462, -8.84679]
        },
        "properties": {
            id: "7674fe6a-6c8d-47b3-9a1f-18637771e23b",
            name: "Ronaldo",
            country: "Portugal",
            position: "Striker",
            imgUrl: "https://cdn-icons-png.flaticon.com/512/805/805401.png",
            number: 7
        }
    },

    {
        "type": "feature",
        "geometry": {
            "type": "Point",
            "coordinates": [41.69662, -8.84979]
        },
        "properties": {
            id: "36ee2d0f-a918-472a-8e2e-ad5f567cdb89",
            name: "Messi",
            country: "Argentina",
            position: "Forward",
            imgUrl: "https://cdn-icons-png.flaticon.com/512/805/805404.png",
            number: 10
        }
    },

    {
        "type": "feature",
        "geometry": {
            "type": "Point",
            "coordinates": [41.69562, -8.84979]
        },
        "properties": {
            id: "4cb5b2f0-343d-4250-ba5c-3a235343cb01",
            name: "Ibrahimovic",
            country: "Sweden",
            position: "Striker",
            imgUrl: "https://cdn-icons-png.flaticon.com/512/805/805409.png",
            number: 11
        }
    }
];

function ObjectMarkersGroup() {

    const map = useMap();
    const [geom, setGeom] = useState([]);
    const [bounds, setBounds] = useState(map.getBounds());
    /**
     * Gets the Markes for the map
     */
    const getMarkers = async () => {
        console.log("olaaaaaaaaaaa");
        const data = await fetch("http://172.30.0.7:8080/api/markers")
        const parsedData = data.json()
        console.log("adddeeeeuusssss", parsedData);
        setGeom(parsedData);
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
        console.log('yo')
    }, [bounds])

    return (
        <LayerGroup>
            {
                geom.map(geoJSON => <ObjectMarker key={geoJSON.properties.id} geoJSON={geoJSON}/>)
            }
        </LayerGroup>
    );
}

export default ObjectMarkersGroup;
