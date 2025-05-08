import { axiosUtility } from "@/utilities/axios-utility";
import { errorHandlerUtility } from "@/utilities/error-handler-utility";

export const taskServices = {
  async getTaskList(params) {
    try {
      const response = await axiosUtility.getResponse({
        apiName: `/tasks/`,
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
  async createTask(payload) {
    try {
      const response = await axiosUtility.getResponse({
        apiName: `/tasks/`,
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
  async updateTask(id, payload) {
    try {
      const response = await axiosUtility.getResponse({
        apiName: `/tasks/${id}/`,
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
  async getTaskDetail(id) {
    try {
      const response = await axiosUtility.getResponse({
        apiName: `/tasks/${id}/`,
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
        apiName: `/tasks/select/`,
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
        apiName: `/tasks/select_for_random_data_generation/`,
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
  async addUserInTask(id, payload) {
    try {
      const response = await axiosUtility.getResponse({
        apiName: `/tasks/${id}/add_user/`,
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
};
// =================================================================
