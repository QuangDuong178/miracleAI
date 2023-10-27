// import type { ParamsLogin } from '@/modal/login'
export interface RepositoryLoginProps {
    login: () => Promise<any>
}

//
// export const RepositoryLogin = ($axios: AxiosInstance): RepositoryLoginProps => ({
//   login(params: ParamsLogin): Promise<any> {
//     return $axios.post('/login', params)
//   }
// })

import type {AxiosInstance} from "axios";

export const RepositoryLogin = ($axios: AxiosInstance): RepositoryLoginProps => ({
    login(): Promise<any> {
        return $axios.get('/message/chat')
    }
})
