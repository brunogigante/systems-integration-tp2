import {Avatar, List, ListItem, ListItemIcon, ListItemText} from "@mui/material";
import HomeIcon from '@mui/icons-material/Home';
import AssignmentIndIcon from '@mui/icons-material/AssignmentInd';
import PlaceIcon from '@mui/icons-material/Place';
import PictureInPictureAltIcon from '@mui/icons-material/PictureInPictureAlt';
import ContactsIcon from '@mui/icons-material/Contacts';
import React from "react";
import {Marker, Popup} from 'react-leaflet';
import {icon as leafletIcon, point} from "leaflet";

const LIST_PROPERTIES = [
    {"key": "number", Icon: AssignmentIndIcon},
    {"key": "city", Icon: PlaceIcon},
];

export function ObjectMarker({geoJSON}) {
    const properties = geoJSON?.properties
    const {city, number, store, image} = properties;
    const coordinates = geoJSON?.geometry?.coordinates;

    return (
        <Marker
            position={coordinates}
            icon={leafletIcon({
                iconUrl: image,
                iconRetinaUrl: image,
                iconSize: point(50, 50),
            })}
        >
            <Popup>
                <List dense={true}>
                    <ListItem>
                        <ListItemIcon>
                            <Avatar alt={store} src={image}/>
                        </ListItemIcon>
                        <ListItemText primary={store}/>
                    </ListItem>
                    {
                        LIST_PROPERTIES
                            .map(({key, label, Icon}) =>
                                <ListItem key={key}>
                                    <ListItemIcon>
                                        <Icon style={{color: "black"}}/>
                                    </ListItemIcon>
                                    <ListItemText
                                        primary={<span>
                                        {properties[key]}<br/>

                                    </span>}
                                    />
                                </ListItem>
                            )
                    }

                </List>

            </Popup>
        </Marker>
    )
}