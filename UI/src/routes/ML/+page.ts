import type { PageLoad } from './$types';
import axios from 'axios';

export const load: PageLoad = async ({params}) => {
    const response = await axios.get("http://localhost:8000/api/files");
    return {
        files: response.data
    };
};