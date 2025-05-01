import { defineStore } from "pinia";
import { ref } from "vue";

export const useUsersStore = defineStore("usersStore", () => {

    const selectedUserId = ref(null);

    return { selectedUserId };

});
