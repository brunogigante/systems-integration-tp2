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


function Stores() {
    const [apiData, setApiData] = useState(null)
    const PAGE_SIZE = 10;
    const [page, setPage] = useState(1);
    const [maxDataSize, setMaxDataSize] = useState(0);


    useEffect(() => {
        const getStores = async () => {
            const data = await fetch('http://localhost:20004/api/stores')
            const json = await data.json()
            setApiData(json.filter((item, index) => Math.floor(index / PAGE_SIZE) === (page - 1)));
            setMaxDataSize(json.length)
        }
        getStores()
    }, [page]);

    return (
        <>
            <h1>Stores</h1>
            <TableContainer component={Paper}>
                <Table sx={{minWidth: 650}} aria-label="simple table">
                    <TableHead>
                        <TableRow>
                            <TableCell>Store Name</TableCell>
                            <TableCell align="center">Store Number</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {
                            apiData ?
                                apiData.map((row, index) => (
                                    <TableRow
                                        key={row.index}
                                        style={{background: "gray", color: "black"}}
                                    >
                                        <TableCell component="td" scope="row">
                                            {row[0]}
                                        </TableCell>
                                        <TableCell component="td" align="center" scope="row">
                                            {row[1]}
                                        </TableCell>
                                    </TableRow>
                                ))
                                :
                                <TableRow>
                                    <TableCell colSpan={2}>
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

export default Stores;
