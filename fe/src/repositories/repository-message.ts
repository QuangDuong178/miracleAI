// import type { ParamsLogin } from '@/modal/login'
export interface RepositoryMessageProps {
    message: () => Promise<any>
}

//
// export const RepositoryLogin = ($axios: AxiosInstance): RepositoryLoginProps => ({
//   login(params: ParamsLogin): Promise<any> {
//     return $axios.post('/login', params)
//   }
// })

import type {AxiosInstance} from "axios";

export const RepositoryMessage = ($axios: AxiosInstance): RepositoryMessageProps => ({
    message(): Promise<any> {
        return $axios.get('/message/chat')
    }
})
