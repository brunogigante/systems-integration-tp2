import React, {useEffect, useState} from "react";
import {Box, CircularProgress, Container, FormControl, InputLabel, MenuItem, Select} from "@mui/material";
import {
    Pagination,
    Paper,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow
} from "@mui/material";


function CitiesStores() {
    const [apiData, setApiData] = useState(null)
    const PAGE_SIZE = 10;
    const [page, setPage] = useState(1);
    const [maxDataSize, setMaxDataSize] = useState(0);
    const [selectedCity, setSelectedCity] = useState('');
    const [cities, setCities] = useState(null)

    const handleChange = async (event) => {
        setSelectedCity(event.target.value)
        const data = await fetch(`http://localhost:20004/api/stores_cities/${event.target.value}`)
        const json = await data.json()
        setApiData(json.filter((item, index) => Math.floor(index / PAGE_SIZE) === (page - 1)));
        setMaxDataSize(json.length)
    }
    useEffect(() => {
        const getStores = async () => {
            const cities = await fetch('http://localhost:20004/api/cities');
            const citiesJson = await cities.json();
            setCities(citiesJson);
        }
        getStores()
    }, [page]);

    return (
        <>
            <h1>City Stores</h1>
            <FormControl fullWidth>
                <InputLabel id="demo-simple-select-label">City</InputLabel>
                <Select
                    labelId="demo-simple-select-label"
                    id="demo-simple-select"
                    value={selectedCity}
                    label="City"
                    onChange={handleChange}
                >
                    {
                        cities ?
                            cities.map((city, index) =>  <MenuItem key={index} value={city}>{city}</MenuItem>)
                            :
                            <MenuItem value='nothing'>Wait for responses</MenuItem>
                    }
                </Select>
            </FormControl>
            <TableContainer component={Paper}>
                <Table sx={{minWidth: 650}} aria-label="simple table">
                    <TableHead>
                        <TableRow>
                            <TableCell>Store_name</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {
                            apiData ?
                                apiData.map((row, index) => (
                                    <TableRow
                                        key={index}
                                        style={{background: "gray", color: "black"}}
                                    >
                                        <TableCell component="td" scope="row">
                                            {row[0]}
                                        </TableCell>
                                    </TableRow>
                                ))
                                :
                                <TableRow>
                                    <TableCell colSpan={1}>
                                        <CircularProgress/>
                                    </TableCell>
                                </TableRow>
                        }
                    </TableBody>
                </Table>
            </TableContainer>
            {
                maxDataSize && <div style={{background: "black", padding: "1rem"}}>
                    <Pagination style={{color: "black"}}
                                variant="outlined" shape="rounded"
                                color={"primary"}
                                onChange={(e, v) => {
                                    setPage(v)
                                }}
                                page={page}
                                count={Math.ceil(maxDataSize / PAGE_SIZE)}
                    />
                </div>
            }


        </>
    );
}

export default CitiesStores;
