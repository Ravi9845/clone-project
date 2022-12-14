import * as actions from './actions';
import * as getters from './getters';
import * as mutations from './mutations';
import type { UserState } from './type';

export const STORAGE_KEY = 'store/user';

let storedUserState: Partial<UserState> = {};

try {
    storedUserState = JSON.parse(window.localStorage.getItem(STORAGE_KEY) || '{}');
} catch (e) {
    window.localStorage.removeItem(STORAGE_KEY);
}

const state: UserState = {
    isSessionExpired: undefined,
    userId: storedUserState.userId,
    userType: storedUserState.userType,
    backend: storedUserState.backend,
    name: storedUserState.name,
    email: storedUserState.email,
    language: storedUserState.language || 'en',
    timezone: storedUserState.timezone,
    roles: storedUserState.roles,
    requiredActions: storedUserState.requiredActions,
};

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations,
};
