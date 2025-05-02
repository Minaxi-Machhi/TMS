import { axiosUtility } from "@/utilities/axios-utility";
import { errorHandlerUtility } from "@/utilities/error-handler-utility";

// ====================== user-profile services ====================
export const userProfileServices = {
    async getUserProfileList(params) {
        try {
            const response = await axiosUtility.getResponse({
                apiName: `/user_profile/`,
                methodType: 'get',
                payload: {},
                queryParams: params,
                headers: {}
            });
            return response;
        } catch (error) {
            const { messages } = errorHandlerUtility.handleError(error);
            throw messages;
        }
    },
    async createUserProfile(payload) {
        try {
            const response = await axiosUtility.getResponse({
                apiName: `/user_profile/`,
                methodType: 'post',
                payload: payload,
                queryParams: {},
                headers: {}
            });
            return response;
        } catch (error) {
            const { messages } = errorHandlerUtility.handleError(error);
            throw messages;
        }
    },
    async updateUserProfile(id, payload) {
        try {
            const response = await axiosUtility.getResponse({
                apiName: `/user_profiles/${id}/`,
                methodType: 'put',
                payload: payload,
                queryParams: {},
                headers: {}
            });
            return response;
        } catch (error) {
            const { messages } = errorHandlerUtility.handleError(error);
            throw messages;
        }
    },
    async getUserProfileDetail(id) {
        try {
            const response = await axiosUtility.getResponse({
                apiName: `/user_profiles/${id}/`,
                methodType: 'get',
                payload: {},
                queryParams: {},
                headers: {}
            });
            return response;
        } catch (error) {
            const { messages } = errorHandlerUtility.handleError(error);
            throw messages;
        }
    },
    async getLoggedInUserDetails() {
        try {
            const response = await axiosUtility.getResponse({
                apiName: `/user_profiles/my_profile/`,
                methodType: 'get',
                payload: {},
                queryParams: {},
                headers: {}
            });
            return response;
        } catch (error) {
            const { messages } = errorHandlerUtility.handleError(error);
            throw messages;
        }
    },
    async changePassword(payload) {
        try {
            const response = await axiosUtility.getResponse({
                apiName: `/user_profiles/change_password/`,
                methodType: 'post',
                payload: payload,
                queryParams: {},
                headers: {}
            });
            return response;
        } catch (error) {
            const { messages } = errorHandlerUtility.handleError(error);
            throw messages;
        }
    },
}
// =================================================================
