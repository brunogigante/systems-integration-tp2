import Stores from "../Procedures/Stores";
import NumberStoresCountry from "../Procedures/NumberStoresCountry";
import NumberStoresOwnership from "../Procedures/NumberStoresOwnership";
import PortugueseCitiesStores from "../Procedures/PortugueseCitiesStores";
import StoresContacts from "../Procedures/StoresContacts";
import CitiesStores from "../Procedures/StoresCity";

const Sections = [

    {
        id: "stores",
        label: "Stores",
        content: <Stores/>
    },

    {
        id: "countries-stores",
        label: "Number of stores by country",
        content: <NumberStoresCountry/>
    },

    {
        id: "ownership-stores",
        label: "Number of stores by ownership",
        content: <NumberStoresOwnership/>
    },

    {
        id: "portuguese-cities-stores",
        label: "Portuguese cities stores",
        content: <PortugueseCitiesStores/>
    },
    {
        id: "store-contacts",
        label: "Stores contacts",
        content: <StoresContacts/>
    },

    {
        id: "stores-by-city",
        label: "City stores",
        content: <CitiesStores/>
    }

];

export default Sections;