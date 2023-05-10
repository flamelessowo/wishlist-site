import type { AxiosResponse } from "axios";
import axios from "axios";
import { SERVER_URI } from "./constants";

export async function get(path: string, config={}): Promise<AxiosResponse>  {
    return await axios.get(`${SERVER_URI}${path}`, config);
}

export async function post(path: string, body={}, config={}): Promise<AxiosResponse> {
    return await axios.post(`${SERVER_URI}${path}`, body, config);
}