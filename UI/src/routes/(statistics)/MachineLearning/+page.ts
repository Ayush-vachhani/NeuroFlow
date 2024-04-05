import type {PageLoad} from "../../../../.svelte-kit/types/src/routes/(statistics)/DeepLearning/$types";
import axios from 'axios';

export const load: PageLoad = async ({params}) => {
    const response = await axios.get("http://localhost:8000/api/files");
    return {
        files: response.data
    };
};