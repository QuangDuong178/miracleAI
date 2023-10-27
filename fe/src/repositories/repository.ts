import {RepositoryLogin} from './repository-login'
import {RepositoryMessage} from "@/repositories/repository-message";

export interface RepositoriesInterface {
    login: typeof RepositoryLogin
    message: typeof RepositoryMessage
}

const repositories: RepositoriesInterface = {
    login: RepositoryLogin,
    message: RepositoryMessage
}

export const RepositoryFactory = {
    create: (key: keyof RepositoriesInterface) => repositories[key]
}

export type RepositoriesType = <K extends keyof RepositoriesInterface>(
    key: K
) => ReturnType<RepositoriesInterface[K]>
