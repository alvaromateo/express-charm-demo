/// <reference types="vite/client" />

import { ApiSSRResponse } from "./types/apiResponseTypes";

declare global {
  interface Window {
    __INITIAL_DATA__: ApiSSRResponse;
  }
}
