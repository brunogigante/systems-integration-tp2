import Stores from "../Tables/Stores";
import City from "../Tables/City";

const Sections = [

    {
        id: "stores",
        label: "Stores",
        content: <Stores/>
    },

    {
        id: "cities",
        label: "Cities",
        content: <City/>
    }

];

export default Sections;