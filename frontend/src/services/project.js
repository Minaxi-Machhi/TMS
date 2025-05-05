import { axiosUtility } from "@/utilities/axios-utility";
import { errorHandlerUtility } from "@/utilities/error-handler-utility";

export const projectServices = {
  async getProjectList(params) {
    try {
      const response = await axiosUtility.getResponse({
        apiName: `/projects/`,
        methodType: "get",
        payload: {},
        queryParams: params,
        headers: {},
      });
      return response;
    } catch (error) {
      const { messages } = errorHandlerUtility.handleError(error);
      throw messages;
    }
  },
  async createProject(payload) {
    try {
      const response = await axiosUtility.getResponse({
        apiName: `/projects/`,
        methodType: "post",
        payload: payload,
        queryParams: {},
        headers: {},
      });
      return response;
    } catch (error) {
      const { messages } = errorHandlerUtility.handleError(error);
      throw messages;
    }
  },
  async updateProject(id, payload) {
    try {
      const response = await axiosUtility.getResponse({
        apiName: `/projects/${id}/`,
        methodType: "put",
        payload: payload,
        queryParams: {},
        headers: {},
      });
      return response;
    } catch (error) {
      const { messages } = errorHandlerUtility.handleError(error);
      throw messages;
    }
  },
  async getProjectDetail(id) {
    try {
      const response = await axiosUtility.getResponse({
        apiName: `/projects/${id}/`,
        methodType: "get",
        payload: {},
        queryParams: {},
        headers: {},
      });
      return response;
    } catch (error) {
      const { messages } = errorHandlerUtility.handleError(error);
      throw messages;
    }
  },
  async getSelectionList(params) {
    try {
      const response = await axiosUtility.getResponse({
        apiName: `/projects/select/`,
        methodType: "get",
        payload: {},
        queryParams: params,
        headers: {},
      });
      return response;
    } catch (error) {
      const { messages } = errorHandlerUtility.handleError(error);
      throw messages;
    }
  },
  async getSelectionListForRandomDataGeneration(params) {
    try {
      const response = await axiosUtility.getResponse({
        apiName: `/projects/select_for_random_data_generation/`,
        methodType: "get",
        payload: {},
        queryParams: params,
        headers: {},
      });
      return response;
    } catch (error) {
      const { messages } = errorHandlerUtility.handleError(error);
      throw messages;
    }
  },
  async addUserInProject(id, payload) {
    try {
      const response = await axiosUtility.getResponse({
        apiName: `/projects/${id}/add_user`,
        methodType: "patch",
        payload: payload,
        queryParams: {},
        headers: {},
      });
      return response;
    } catch (error) {
      const { messages } = errorHandlerUtility.handleError(error);
      throw messages;
    }
  },
};
// =================================================================
