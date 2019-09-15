import axios from 'axios';
import { BASE_URL } from './endpoints';

const instance = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': '*'
  }
});

export default instance;
